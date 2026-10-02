"""KI-Zweitmeinung (Abschnitt 3 Teil A, Entscheid 3) — Schnittstelle, Backends, Konfiguration, Cache.

Alles synthetisch oder aus gespeicherten Antworten; kein Test ruft die KI live auf.
Der einzige Test mit echtem Binary läuft nur mit ``NOTBEL_KI_LIVE=1`` (Standard: skip).
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from notbeleuchtung.raumerkennung import ki_backends, ki_zweitmeinung
from notbeleuchtung.raumerkennung.ki_backends import (
    BACKENDS,
    CodexAboBackend,
    OpenaiApiBackend,
    backend_aus_konfig,
    finde_codex,
)
from notbeleuchtung.raumerkennung.ki_zweitmeinung import (
    UNBESTIMMT,
    Antwort,
    GeschossAnfrage,
    KiCache,
    KiFehler,
    KiKonfig,
    RaumAnfrage,
    RaumAntwort,
    Zweitmeinung,
    ZweitmeinungBackend,
    baue_prompt,
    kanon_typen,
    parse_antwort,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "ki"
LIMIT_JSONL = (FIXTURES / "codex_limit.jsonl").read_text(encoding="utf-8")


def _anfrage(tmp_path: Path, *, bilder: tuple[Path, ...] = (), geschoss: str = "OG4",
             quadrant: str = "") -> GeschossAnfrage:
    dxf = tmp_path / "plan.dxf"
    if not dxf.exists():
        dxf.write_bytes(b"0\nSECTION\n0\nEOF\n")
    return GeschossAnfrage(
        plan_datei=dxf, geschoss=geschoss, quadrant=quadrant, bilder=bilder,
        raeume=(
            RaumAnfrage("rest_2", "STIEGENHAUS", "kuerzel", {"flaeche_m2": 40.2,
                                                              "texte": ["STGH", "VR"]}),
            RaumAnfrage("frei_1", "", "", {"flaeche_m2": 5.4, "texte": []}),
        ),
    )


def _gueltig(*raeume: dict) -> str:
    return json.dumps({"raeume": list(raeume)})


R_OK = {"raum_id": "rest_2", "raum_typ": "STIEGENHAUS", "sicherheit": 0.95,
        "bestaetigt": True, "begruendung": "Stempel STGH, Treppenlauf sichtbar"}
R_UNB = {"raum_id": "frei_1", "raum_typ": "UNBESTIMMT", "sicherheit": 0.3,
         "bestaetigt": False, "begruendung": "kein Stempel, keine Möbel"}


class ZaehlBackend:
    """Backend-Mock: zählt Aufrufe, liefert eine feste Antwort (oder einen Fehler)."""

    name = "mock"

    def __init__(self, antwort: Antwort | None = None):
        self.aufrufe: list[tuple[str, str | None]] = []
        self.antwort = antwort or Antwort(
            raeume=[RaumAntwort("rest_2", "STIEGENHAUS", 0.95, True, "STGH"),
                    RaumAntwort("frei_1", UNBESTIMMT, 0.3, False, "nichts zu sehen")],
            roh=_gueltig(R_OK, R_UNB))

    def frage(self, anfrage: GeschossAnfrage, modell: str | None = None) -> Antwort:
        self.aufrufe.append((anfrage.geschoss, modell))
        return self.antwort


# --- Kanon und Schnittstelle --------------------------------------------------------------

def test_kanon_ist_der_raumtyp_kanon_plus_unbestimmt():
    kanon = kanon_typen()
    assert {"STIEGENHAUS", "GANG", "VORRAUM", "BAD", "WC", "GARAGE", "SCHLEUSE",
            "KINDERWAGENRAUM", "WASCHKÜCHE"} <= kanon
    assert UNBESTIMMT not in kanon  # UNBESTIMMT ist kein Raumtyp, nur die erlaubte Enthaltung
    assert "UNBEKANNT" not in kanon and "BÜRO" not in kanon


def test_mock_erfuellt_protocol():
    assert isinstance(ZaehlBackend(), ZweitmeinungBackend)
    assert isinstance(CodexAboBackend(KiKonfig()), ZweitmeinungBackend)
    assert isinstance(OpenaiApiBackend(KiKonfig()), ZweitmeinungBackend)


# --- Antwort-Parsing ----------------------------------------------------------------------

def test_parse_gueltig():
    raeume, verworfen, fehler = parse_antwort(_gueltig(R_OK, R_UNB), {"rest_2", "frei_1"})
    assert fehler is None and verworfen == []
    assert [(r.raum_id, r.raum_typ, r.sicherheit, r.bestaetigt) for r in raeume] == [
        ("rest_2", "STIEGENHAUS", 0.95, True), ("frei_1", UNBESTIMMT, 0.3, False)]
    assert raeume[0].begruendung.startswith("Stempel STGH")


def test_parse_toleriert_codefence_liste_und_kleinschreibung():
    text = "```json\n" + json.dumps([dict(R_OK, raum_typ="stiegenhaus ")]) + "\n```"
    raeume, verworfen, fehler = parse_antwort(text, {"rest_2"})
    assert fehler is None and verworfen == [] and raeume[0].raum_typ == "STIEGENHAUS"


def test_parse_ungueltiges_json_ist_formatfehler():
    raeume, _verworfen, fehler = parse_antwort("Das ist kein JSON", {"rest_2"})
    assert raeume == [] and fehler is not None and fehler.art == "format"
    raeume, _verworfen, fehler = parse_antwort(json.dumps({"x": 1}), {"rest_2"})
    assert fehler is not None and fehler.art == "format"


def test_parse_verwirft_ausserhalb_kanon_unbekannte_id_und_schlechte_felder():
    text = _gueltig(
        R_OK,
        dict(R_UNB, raum_typ="BÜRO"),                       # außerhalb Kanon
        dict(R_OK, raum_id="raum_999"),                     # unbekannte raum_id
        dict(R_OK, raum_id="frei_1", sicherheit=1.5),       # sicherheit > 1
        dict(R_OK, raum_id="frei_1", bestaetigt="ja"),      # kein bool
        dict(R_OK, raum_id="frei_1", begruendung=""),       # leer
        {"raum_id": "frei_1"},                              # Felder fehlen
        "kein objekt",
    )
    raeume, verworfen, fehler = parse_antwort(text, {"rest_2", "frei_1"})
    assert fehler is None
    assert [r.raum_id for r in raeume] == ["rest_2"]
    assert len(verworfen) == 7
    assert any("BÜRO" in v and "Kanon" in v for v in verworfen)
    assert any("raum_999" in v for v in verworfen)


def test_parse_doppelte_raum_id_zaehlt_einmal():
    raeume, verworfen, _ = parse_antwort(_gueltig(R_OK, dict(R_OK, sicherheit=0.5)), {"rest_2"})
    assert len(raeume) == 1 and raeume[0].sicherheit == 0.95 and len(verworfen) == 1


# --- Konfiguration ------------------------------------------------------------------------

def test_konfig_standard_ist_aus_und_nie_xhigh():
    k = KiKonfig()
    assert k.an is False and k.backend == "codex_abo"
    assert (k.modell, k.effort, k.fallback_modell) == ("gpt-6-astra", "high", "gpt-5.6-sol")
    assert k.zeitlimit_s > 0 and k.prompt_version == ki_zweitmeinung.PROMPT_VERSION
    assert k.cache_pfad.name == "ki_cache" and k.cache_pfad.parent.name == "knowledge"
    with pytest.raises(ValueError):
        KiKonfig(effort="xhigh")


def test_konfig_aus_umgebung(monkeypatch):
    for v in ("NOTBEL_KI", "NOTBEL_KI_BACKEND", "NOTBEL_KI_MODELL", "NOTBEL_KI_CODEX"):
        monkeypatch.delenv(v, raising=False)
    assert KiKonfig.aus_umgebung().an is False
    monkeypatch.setenv("NOTBEL_KI", "an")
    monkeypatch.setenv("NOTBEL_KI_BACKEND", "openai_api")
    monkeypatch.setenv("NOTBEL_KI_MODELL", "gpt-5.6-sol")
    k = KiKonfig.aus_umgebung()
    assert (k.an, k.backend, k.modell) == (True, "openai_api", "gpt-5.6-sol")
    monkeypatch.setenv("NOTBEL_KI", "aus")
    assert KiKonfig.aus_umgebung().an is False


# --- Cache --------------------------------------------------------------------------------

def test_cache_schluessel_enthaelt_alle_teile(tmp_path):
    cache = KiCache(tmp_path / "c")
    a = _anfrage(tmp_path, geschoss="OG4", quadrant="NW")
    s = cache.schluessel("codex_abo", "gpt-6-astra", a, "1")
    assert s.backend == "codex_abo" and s.modell == "gpt-6-astra" and s.geschoss == "OG4"
    assert s.quadrant == "NW" and s.prompt_version == "1" and len(s.plan_sha) == 16
    pfad = cache.pfad(s)
    assert pfad.suffix == ".json" and "plan" in pfad.parent.name and s.plan_sha in pfad.parent.name
    # anderer Inhalt der Plan-Datei → anderer Schlüssel; andere Prompt-Version → anderer Pfad
    a.plan_datei.write_bytes(b"anders")
    assert cache.schluessel("codex_abo", "gpt-6-astra", a, "1").plan_sha != s.plan_sha
    assert cache.pfad(cache.schluessel("codex_abo", "gpt-6-astra", a, "2")) != pfad


def test_cache_treffer_verhindert_aufruf(tmp_path):
    backend = ZaehlBackend()
    konfig = KiKonfig(an=True, cache_pfad=tmp_path / "c")
    zm = Zweitmeinung(konfig, backend=backend)
    a = _anfrage(tmp_path)
    erste = zm.frage(a)
    assert erste.fehler is None and len(erste.raeume) == 2 and erste.quelle == "backend"
    assert len(backend.aufrufe) == 1 and zm.anfragen == 1 and zm.treffer == 0
    zweite = zm.frage(a)
    assert len(backend.aufrufe) == 1, "Cache-Treffer darf keinen Aufruf auslösen"
    assert zm.anfragen == 1 and zm.treffer == 1 and zweite.quelle == "cache"
    assert [(r.raum_id, r.raum_typ) for r in zweite.raeume] == [("rest_2", "STIEGENHAUS"),
                                                                 ("frei_1", UNBESTIMMT)]
    # ein neuer Lauf (neue Instanz) liest denselben Cache
    zm2 = Zweitmeinung(konfig, backend=backend)
    assert zm2.frage(a).quelle == "cache" and len(backend.aufrufe) == 1
    # andere Frage (Quadrant) → neuer Aufruf
    zm2.frage(_anfrage(tmp_path, quadrant="SO"))
    assert len(backend.aufrufe) == 2
    dateien = list((tmp_path / "c").rglob("*.json"))
    assert len(dateien) == 2
    inhalt = json.loads(dateien[0].read_text(encoding="utf-8"))
    assert set(inhalt) >= {"schluessel", "roh", "raeume", "gespeichert"}
    assert "\\" not in inhalt["schluessel"]["plan"] and ":" not in inhalt["schluessel"]["plan"]


def test_fehler_wird_nicht_gecacht_und_bricht_nicht_ab(tmp_path):
    backend = ZaehlBackend(Antwort(fehler=KiFehler("limit", "You’ve hit your usage limit.")))
    zm = Zweitmeinung(KiKonfig(an=True, cache_pfad=tmp_path / "c"), backend=backend)
    a = _anfrage(tmp_path)
    antwort = zm.frage(a)
    assert antwort.fehler is not None and antwort.fehler.art == "limit" and antwort.raeume == []
    assert zm.warnungen and "limit" in zm.warnungen[0] and "Engine-Ergebnis bleibt" in zm.warnungen[0]
    zm.frage(a)
    assert len(backend.aufrufe) == 2 and not list((tmp_path / "c").rglob("*.json"))
    assert zm.anfragen == 2


def test_fallback_modell_bei_sonstigem_fehler_nicht_bei_limit(tmp_path):
    class Wechsel(ZaehlBackend):
        def frage(self, anfrage, modell=None):
            self.aufrufe.append((anfrage.geschoss, modell))
            if modell == "gpt-6-astra":
                return Antwort(fehler=KiFehler("sonstig", "model not available"))
            return ZaehlBackend().antwort

    b = Wechsel()
    zm = Zweitmeinung(KiKonfig(an=True, cache_pfad=tmp_path / "c"), backend=b)
    antwort = zm.frage(_anfrage(tmp_path))
    assert antwort.fehler is None and antwort.modell == "gpt-5.6-sol"
    assert [m for _, m in b.aufrufe] == ["gpt-6-astra", "gpt-5.6-sol"] and zm.anfragen == 2
    b2 = ZaehlBackend(Antwort(fehler=KiFehler("limit", "limit")))
    zm2 = Zweitmeinung(KiKonfig(an=True, cache_pfad=tmp_path / "c2"), backend=b2)
    zm2.frage(_anfrage(tmp_path))
    assert [m for _, m in b2.aufrufe] == ["gpt-6-astra"], "Limit gilt kontoweit: kein Fallback"


def test_backend_ausnahme_wird_fehler_sonstig(tmp_path):
    class Kaputt(ZaehlBackend):
        def frage(self, anfrage, modell=None):
            raise RuntimeError("Backend explodiert")

    zm = Zweitmeinung(KiKonfig(an=True, cache_pfad=tmp_path / "c", fallback_modell=""),
                      backend=Kaputt())
    antwort = zm.frage(_anfrage(tmp_path))
    assert antwort.fehler is not None and antwort.fehler.art == "sonstig"
    assert "Backend explodiert" in antwort.fehler.meldung and len(zm.warnungen) == 1


def test_ki_aus_kein_aufruf_kein_cache(tmp_path):
    backend = ZaehlBackend()
    zm = Zweitmeinung(KiKonfig(an=False, cache_pfad=tmp_path / "c"), backend=backend)
    antwort = zm.frage(_anfrage(tmp_path))
    assert antwort.raeume == [] and antwort.fehler is None and antwort.quelle == "aus"
    assert backend.aufrufe == [] and zm.anfragen == 0 and not (tmp_path / "c").exists()


# --- Registry -----------------------------------------------------------------------------

def test_registry_kennt_beide_backends_und_nimmt_claude_abo_als_klasse(monkeypatch):
    assert set(BACKENDS) == {"codex_abo", "openai_api"}
    assert isinstance(backend_aus_konfig(KiKonfig(backend="codex_abo")), CodexAboBackend)
    assert isinstance(backend_aus_konfig(KiKonfig(backend="openai_api")), OpenaiApiBackend)

    class ClaudeAbo:
        name = "claude_abo"

        def __init__(self, konfig):
            self.konfig = konfig

        def frage(self, anfrage, modell=None):
            return Antwort()

    monkeypatch.setitem(BACKENDS, "claude_abo", ClaudeAbo)
    b = backend_aus_konfig(KiKonfig(backend="claude_abo"))
    assert isinstance(b, ClaudeAbo) and isinstance(b, ZweitmeinungBackend)
    with pytest.raises(ValueError, match="unbekannt"):
        backend_aus_konfig(KiKonfig(backend="gibt_es_nicht"))


def test_openai_api_ist_geruest_und_liest_keinen_key(monkeypatch, tmp_path):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-nie-benutzen")
    antwort = OpenaiApiBackend(KiKonfig(backend="openai_api")).frage(_anfrage(tmp_path))
    assert antwort.fehler is not None and antwort.fehler.art == "sonstig"
    assert "openai_api" in antwort.fehler.meldung and "sk-test" not in antwort.fehler.meldung
    quelle = Path(ki_backends.__file__).read_text(encoding="utf-8")
    assert "sk-" not in quelle, "kein API-Key im Repo"


# --- Backend codex_abo (subprocess gemockt) -----------------------------------------------

class _Lauf:
    """Mock für subprocess.run: merkt sich Argumentliste und kwargs, liefert feste Ausgabe."""

    def __init__(self, stdout: str = "", returncode: int = 0, ausnahme: Exception | None = None,
                 letzte_nachricht: str | None = None):
        self.stdout, self.returncode, self.ausnahme = stdout, returncode, ausnahme
        self.letzte_nachricht = letzte_nachricht
        self.aufrufe: list[tuple[list[str], dict]] = []

    def __call__(self, args, **kw):
        self.aufrufe.append((list(args), kw))
        if self.ausnahme is not None:
            raise self.ausnahme
        if "--output-schema" in args:  # Temp-Datei lebt nur während des Aufrufs
            self.schema = json.loads(
                Path(args[args.index("--output-schema") + 1]).read_text(encoding="utf-8"))
        if self.letzte_nachricht is not None:
            i = args.index("-o")
            Path(args[i + 1]).write_text(self.letzte_nachricht, encoding="utf-8")
        return subprocess.CompletedProcess(args, self.returncode, self.stdout, "")


def _codex(tmp_path: Path, lauf: _Lauf, **konfig) -> CodexAboBackend:
    exe = tmp_path / "bin" / "codex.exe"
    exe.parent.mkdir(exist_ok=True)
    exe.write_bytes(b"MZ")
    return CodexAboBackend(KiKonfig(an=True, codex_binary=str(exe), **konfig), run=lauf)


def test_codex_argumente_und_kindprozess_ohne_keys(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-geheim")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-geheim")
    monkeypatch.setenv("PATH", os.environ.get("PATH", ""))
    bild = tmp_path / "OG4 Quadrant NW.png"
    bild.write_bytes(b"\x89PNG")
    lauf = _Lauf(stdout=_jsonl_agent(_gueltig(R_OK, R_UNB)))
    backend = _codex(tmp_path, lauf, zeitlimit_s=42.0)
    antwort = backend.frage(_anfrage(tmp_path, bilder=(bild,)))
    assert antwort.fehler is None and len(antwort.raeume) == 2
    assert len(lauf.aufrufe) == 1
    args, kw = lauf.aufrufe[0]
    assert isinstance(args, list) and args[0].endswith("codex.exe") and args[1] == "exec"
    assert kw.get("shell", False) is False, "Argumentliste, nie Shell-String"
    for flag in ("--json", "--ephemeral", "--skip-git-repo-check", "--output-schema", "-o"):
        assert flag in args, flag
    assert args[args.index("-s") + 1] == "read-only"
    assert args[args.index("-m") + 1] == "gpt-6-astra"
    assert args[args.index("-c") + 1] == "model_reasoning_effort=high"
    assert f"--image={bild}" in args, "Bild per -i/--image, Pfad mit Leerzeichen als EIN Argument"
    assert args[-1] == "-", "Prompt kommt über stdin, nicht als Argument"
    assert str(tmp_path) not in kw["input"], "keine lokalen Pfade im Prompt"
    assert "rest_2" in kw["input"] and "STIEGENHAUS" in kw["input"]
    assert kw["timeout"] == 42.0 and kw["cwd"] != str(tmp_path)
    env = kw["env"]
    assert "OPENAI_API_KEY" not in env and "ANTHROPIC_API_KEY" not in env
    assert env.get("PATH") == os.environ.get("PATH")
    assert lauf.schema["required"] == ["raeume"]
    assert set(lauf.schema["properties"]["raeume"]["items"]["required"]) == {
        "raum_id", "raum_typ", "sicherheit", "bestaetigt", "begruendung"}
    # Modell/Effort immer explizit, auch beim Fallback-Aufruf
    backend.frage(_anfrage(tmp_path), modell="gpt-5.6-sol")
    args2, _ = lauf.aufrufe[1]
    assert args2[args2.index("-m") + 1] == "gpt-5.6-sol"
    assert args2[args2.index("-c") + 1] == "model_reasoning_effort=high"


def _jsonl_agent(text: str) -> str:
    return "\n".join(json.dumps(e) for e in (
        {"type": "thread.started", "thread_id": "00000000-0000-0000-0000-000000000000"},
        {"type": "turn.started"},
        {"type": "item.completed", "item": {"id": "item_0", "type": "agent_message", "text": text}},
        {"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 5}},
    )) + "\n"


def test_codex_limit_fixture_ist_warnung_kein_abbruch(tmp_path):
    lauf = _Lauf(stdout=LIMIT_JSONL, returncode=1)
    backend = _codex(tmp_path, lauf)
    antwort = backend.frage(_anfrage(tmp_path))
    assert antwort.fehler is not None and antwort.fehler.art == "limit"
    assert "usage limit" in antwort.fehler.meldung and antwort.raeume == []
    zm = Zweitmeinung(KiKonfig(an=True, cache_pfad=tmp_path / "c"), backend=backend)
    ergebnis = zm.frage(_anfrage(tmp_path))  # darf nicht werfen
    assert ergebnis.fehler is not None and ergebnis.fehler.art == "limit"
    assert len(zm.warnungen) == 1 and zm.warnungen[0].startswith("ki:")
    assert "UNBESTIMMT" in zm.warnungen[0] and len(lauf.aufrufe) == 2  # kein Fallback bei limit


def test_codex_login_fehlt_ist_warnung(tmp_path):
    # synthetisch — die echte Meldung ohne Login ist nicht aufgezeichnet
    jsonl = "\n".join(json.dumps(e) for e in (
        {"type": "thread.started", "thread_id": "00000000-0000-0000-0000-000000000000"},
        {"type": "error", "message": "Not logged in. Run `codex login` to authenticate."},
        {"type": "turn.failed", "error": {"message": "Not logged in."}},
    ))
    antwort = _codex(tmp_path, _Lauf(stdout=jsonl, returncode=1)).frage(_anfrage(tmp_path))
    assert antwort.fehler is not None and antwort.fehler.art == "login"


def test_codex_timeout_und_formatfehler(tmp_path):
    lauf = _Lauf(ausnahme=subprocess.TimeoutExpired(cmd="codex", timeout=1))
    antwort = _codex(tmp_path, lauf).frage(_anfrage(tmp_path))
    assert antwort.fehler is not None and antwort.fehler.art == "timeout"
    antwort = _codex(tmp_path, _Lauf(stdout=_jsonl_agent("Ich weiß es nicht."))).frage(
        _anfrage(tmp_path))
    assert antwort.fehler is not None and antwort.fehler.art == "format"
    antwort = _codex(tmp_path, _Lauf(stdout="", returncode=3)).frage(_anfrage(tmp_path))
    assert antwort.fehler is not None and antwort.fehler.art == "format"


def test_codex_letzte_nachricht_datei_als_rueckfall(tmp_path):
    """Kein agent_message-Event im JSONL, aber die -o-Datei trägt die Antwort."""
    jsonl = json.dumps({"type": "turn.completed", "usage": {}})
    lauf = _Lauf(stdout=jsonl, letzte_nachricht=_gueltig(R_OK))
    antwort = _codex(tmp_path, lauf).frage(_anfrage(tmp_path))
    assert antwort.fehler is None and [r.raum_id for r in antwort.raeume] == ["rest_2"]


def test_codex_verwirft_ungueltige_raeume_aus_jsonl(tmp_path):
    text = _gueltig(R_OK, dict(R_UNB, raum_typ="BÜRO"), dict(R_OK, raum_id="x"))
    antwort = _codex(tmp_path, _Lauf(stdout=_jsonl_agent(text))).frage(_anfrage(tmp_path))
    assert [r.raum_id for r in antwort.raeume] == ["rest_2"] and len(antwort.verworfen) == 2


def test_codex_binary_suche(tmp_path, monkeypatch):
    exe = tmp_path / "eigen" / "codex.exe"
    exe.parent.mkdir()
    exe.write_bytes(b"MZ")
    assert finde_codex(str(exe)) == exe
    assert finde_codex(str(tmp_path / "fehlt.exe")) is None
    monkeypatch.setattr(ki_backends.shutil, "which", lambda name: str(exe) if name == "codex" else None)
    assert finde_codex(None) == exe
    monkeypatch.setattr(ki_backends.shutil, "which", lambda name: None)
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "lad"))
    assert finde_codex(None) is None
    bundle = tmp_path / "lad" / "OpenAI" / "Codex" / "bin" / "abc123" / "codex.exe"
    bundle.parent.mkdir(parents=True)
    bundle.write_bytes(b"MZ")
    assert finde_codex(None) == bundle
    fehlt = CodexAboBackend(KiKonfig(codex_binary=str(tmp_path / "nix.exe")), run=_Lauf())
    antwort = fehlt.frage(_anfrage(tmp_path))
    assert antwort.fehler is not None and antwort.fehler.art == "sonstig"
    assert "codex" in antwort.fehler.meldung.lower()


def test_codex_fehlendes_bild_ist_fehler_kein_aufruf(tmp_path):
    lauf = _Lauf(stdout=_jsonl_agent(_gueltig(R_OK)))
    antwort = _codex(tmp_path, lauf).frage(_anfrage(tmp_path, bilder=(tmp_path / "fehlt.png",)))
    assert antwort.fehler is not None and antwort.fehler.art == "sonstig" and lauf.aufrufe == []


# --- Prompt -------------------------------------------------------------------------------

def test_prompt_traegt_kanon_ausgangsdefinition_und_raeume(tmp_path):
    p = baue_prompt(_anfrage(tmp_path, quadrant="NW"))
    assert "UNBESTIMMT" in p and "STIEGENHAUS" in p and "KINDERWAGENRAUM" in p
    assert "Innenhof" in p and "ins Freie" in p
    assert '"rest_2"' in p and '"frei_1"' in p and "OG4" in p and "NW" in p
    assert "sicherheit" in p and "bestaetigt" in p and "begruendung" in p
    assert "plan.dxf" not in p and str(tmp_path) not in p, "keine lokalen Pfade im Prompt"


# --- Live (Standard: skip) ----------------------------------------------------------------

@pytest.mark.skipif(os.environ.get("NOTBEL_KI_LIVE") != "1",
                    reason="echter codex-exec-Aufruf nur mit NOTBEL_KI_LIVE=1")
def test_codex_live_minimal(tmp_path):
    backend = CodexAboBackend(KiKonfig(an=True, zeitlimit_s=180))
    antwort = backend.frage(_anfrage(tmp_path))
    assert antwort.fehler is None or antwort.fehler.art in {"limit", "login", "timeout", "format",
                                                             "sonstig"}
