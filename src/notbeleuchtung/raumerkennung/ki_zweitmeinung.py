"""ki_zweitmeinung — anbieterneutrale zweite Meinung je Geschoss (Entscheid 3, 2026-10-01).

„KI (GPT) als zweite Meinung je Geschoss. Engine misst, KI liest und bestätigt."
(``docs/AUFTRAG_2026-10-01.md`` § 3). Die Engine findet und misst (Wände, Flächen,
Türen); die KI liest den Plan wie ein Planer (Stempel, Möbel, Sanitär, Anordnung)
und bestätigt oder widerspricht je Raum. Dieses Modul kennt KEINEN Anbieter: ein
Backend (``ki_backends``) bekommt eine ``GeschossAnfrage`` und liefert eine
``Antwort`` — mehr muss die Engine nicht wissen.

Teil A (Phase A, ohne Live-Aufrufe): Schnittstelle, Konfiguration, Cache,
Antwort-Parsing. Die Verdrahtung in ``provider.parse`` (Herkunft je Raum im
Bericht, Entscheidungsregeln „Erscheinungsbild ist Wahrheit") ist Teil B.

Grundsätze (Auftrag § 3):

- KI per Konfiguration an/aus (``KiKonfig.an``, Standard aus; Umgebung
  ``NOTBEL_KI=an``). Ohne KI läuft alles wie bisher.
- Antwort je Raum: ``raum_id``, ``raum_typ`` (nur Kanon aus ``raumtyp.py`` =
  ``docs/VOKABULAR.md`` § 1, oder ``UNBESTIMMT``), ``sicherheit`` 0–1,
  ``bestaetigt``, ``begruendung``. Außerhalb des Kanons, unbekannte ``raum_id``
  oder nicht lesbar → für diesen Raum verworfen (``Antwort.verworfen``).
- Fehler, Zeitüberschreitung oder Kontingent-Limit → ``KiFehler`` (``art`` in
  timeout | limit | login | format | sonstig), Warnung, kein Abbruch; das
  Engine-Ergebnis bleibt unverändert.
- Cache im Repo (``knowledge/ki_cache/``): Schlüssel Backend + Modell + Plan-Datei
  (SHA-256) + Geschoss + Quadrant + Prompt-Version → gespeicherte Antwort. Gleiche
  Frage → keine neue Anfrage. Suite und Gate laufen nur mit dem Cache. Fehler
  werden nie gecacht. Zähler ``anfragen`` / ``treffer`` je Lauf für den Bericht.
- Modell und Stufe immer explizit (Standard ``gpt-6-astra`` high, Fallback
  ``gpt-5.6-sol`` high; nie xhigh für die Engine — ``KiKonfig`` lehnt es ab).

Cache-Ort ``knowledge/ki_cache/``: die Engine liest ihn zur Laufzeit (nicht nur die
Tests), also weder unter ``tests/`` noch im Paket; ``knowledge/`` ist der
getrackte Ort für Wissensdaten außerhalb des Codes, ``scripts/wissen_index.py``
indiziert dort nur ``extracted/**/*.md``, die JSON-Dateien stören den Index nicht.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol, runtime_checkable

from . import raumtyp

_REPO = Path(__file__).resolve().parents[3]

UNBESTIMMT = "UNBESTIMMT"
PROMPT_VERSION = "1"
FEHLER_ARTEN = ("timeout", "limit", "login", "format", "sonstig")
_EFFORTS = ("low", "medium", "high")  # nie xhigh für die Engine (Auftrag „Modell und Denkstufe")


def kanon_typen() -> frozenset[str]:
    """Die kanonischen Raumtypen — dieselbe Maschinen-Quelle wie ``docs/VOKABULAR.md`` § 1."""
    return frozenset(
        v[0] for d in (raumtyp._TYP_MAP, raumtyp._EXTRA_DIRECT, raumtyp._EXTRA_OVERRIDE)
        for v in d.values()
    )


# --- Konfiguration ------------------------------------------------------------------------

@dataclass(frozen=True)
class KiKonfig:
    """Konfiguration der KI-Schicht. Kein Key, kein Login-Datum — nur Schalter und Namen."""

    an: bool = False
    backend: str = "codex_abo"
    modell: str = "gpt-6-astra"
    effort: str = "high"
    fallback_modell: str = "gpt-5.6-sol"   # "" = kein Fallback
    zeitlimit_s: float = 300.0
    cache_pfad: Path = _REPO / "knowledge" / "ki_cache"
    prompt_version: str = PROMPT_VERSION
    codex_binary: str | None = None        # None → PATH → App-Bundle (ki_backends.finde_codex)

    def __post_init__(self) -> None:
        if self.effort not in _EFFORTS:
            raise ValueError(f"effort {self.effort!r} — erlaubt {_EFFORTS}, nie xhigh für die Engine")
        if self.zeitlimit_s <= 0:
            raise ValueError("zeitlimit_s muss > 0 sein")

    @classmethod
    def aus_umgebung(cls, env: dict[str, str] | None = None) -> KiKonfig:
        """``NOTBEL_KI=an`` schaltet ein; ``NOTBEL_KI_BACKEND/_MODELL/_CODEX`` übersteuern."""
        env = os.environ if env is None else env
        werte: dict[str, object] = {
            "an": env.get("NOTBEL_KI", "aus").strip().lower() in {"an", "1", "true", "ja"},
        }
        for schluessel, feld in (("NOTBEL_KI_BACKEND", "backend"), ("NOTBEL_KI_MODELL", "modell"),
                                 ("NOTBEL_KI_CODEX", "codex_binary")):
            if env.get(schluessel):
                werte[feld] = env[schluessel].strip()
        return cls(**werte)  # type: ignore[arg-type]


# --- Anfrage und Antwort ------------------------------------------------------------------

@dataclass(frozen=True)
class RaumAnfrage:
    """Ein Raum, wie ihn die Engine sieht: Typ + Beleg + Merkmale (Fläche, Texte, Objekte …)."""

    raum_id: str
    engine_typ: str = ""        # "" = ohne Typ (UNBEKANNT)
    beleg: str = ""             # stempel | kuerzel | geometrie | "" (unbelegt)
    merkmale: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class GeschossAnfrage:
    """Eine Frage = ein Geschoss (oder ein Quadrant davon) mit Bild(ern) und Räumen."""

    plan_datei: Path
    geschoss: str
    raeume: tuple[RaumAnfrage, ...]
    quadrant: str = ""
    bilder: tuple[Path, ...] = ()

    @property
    def raum_ids(self) -> frozenset[str]:
        return frozenset(r.raum_id for r in self.raeume)


@dataclass(frozen=True)
class RaumAntwort:
    raum_id: str
    raum_typ: str          # Kanon oder UNBESTIMMT
    sicherheit: float      # 0–1
    bestaetigt: bool       # ja/nein zum Engine-Typ
    begruendung: str


@dataclass(frozen=True)
class KiFehler:
    art: str               # timeout | limit | login | format | sonstig
    meldung: str

    def __post_init__(self) -> None:
        if self.art not in FEHLER_ARTEN:
            raise ValueError(f"Fehlerart {self.art!r} — erlaubt {FEHLER_ARTEN}")


@dataclass
class Antwort:
    raeume: list[RaumAntwort] = field(default_factory=list)
    verworfen: list[str] = field(default_factory=list)   # "raum_id: Grund"
    fehler: KiFehler | None = None
    roh: str = ""                                          # Antworttext des Modells
    modell: str = ""
    quelle: str = ""                                       # backend | cache | aus


@runtime_checkable
class ZweitmeinungBackend(Protocol):
    """Ein Backend liefert pro Geschoss eine Antwort — mehr muss die Engine nicht wissen."""

    name: str

    def frage(self, anfrage: GeschossAnfrage, modell: str | None = None) -> Antwort: ...


# --- Antwort-Schema und Parsing -----------------------------------------------------------

ANTWORT_SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {
        "raeume": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "raum_id": {"type": "string"},
                    "raum_typ": {"type": "string"},
                    "sicherheit": {"type": "number"},
                    "bestaetigt": {"type": "boolean"},
                    "begruendung": {"type": "string"},
                },
                "required": ["raum_id", "raum_typ", "sicherheit", "bestaetigt", "begruendung"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["raeume"],
    "additionalProperties": False,
}

_FENCE = re.compile(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", re.DOTALL)


def parse_antwort(text: str, raum_ids: set[str] | frozenset[str],
                  kanon: frozenset[str] | None = None,
                  ) -> tuple[list[RaumAntwort], list[str], KiFehler | None]:
    """Antworttext → (gültige Räume, verworfene „raum_id: Grund", Formatfehler oder None).

    Ein Raum wird verworfen, wenn ein Feld fehlt oder den falschen Typ hat, ``raum_typ``
    weder im Kanon noch UNBESTIMMT ist, ``raum_id`` unbekannt ist, ``sicherheit`` außerhalb
    0–1 liegt oder die ``raum_id`` schon beantwortet wurde. Kein JSON / kein Objekt mit
    ``raeume`` (oder Liste) → Formatfehler, keine Räume.
    """
    kanon = kanon_typen() if kanon is None else kanon
    m = _FENCE.match(text or "")
    roh = m.group(1) if m else (text or "")
    try:
        daten = json.loads(roh)
    except (json.JSONDecodeError, TypeError) as e:
        return [], [], KiFehler("format", f"Antwort ist kein JSON: {e}")
    if isinstance(daten, dict):
        daten = daten.get("raeume")
    if not isinstance(daten, list):
        return [], [], KiFehler("format", "Antwort ohne Liste 'raeume'")
    raeume: list[RaumAntwort] = []
    verworfen: list[str] = []
    gesehen: set[str] = set()
    for eintrag in daten:
        if not isinstance(eintrag, dict):
            verworfen.append(f"?: kein Objekt ({str(eintrag)[:40]!r})")
            continue
        rid = eintrag.get("raum_id")
        grund = _pruefe_raum(eintrag, raum_ids, kanon, gesehen)
        if grund:
            verworfen.append(f"{rid}: {grund}")
            continue
        gesehen.add(rid)
        raeume.append(RaumAntwort(
            raum_id=rid, raum_typ=str(eintrag["raum_typ"]).strip().upper(),
            sicherheit=float(eintrag["sicherheit"]), bestaetigt=bool(eintrag["bestaetigt"]),
            begruendung=str(eintrag["begruendung"]).strip()))
    return raeume, verworfen, None


def _pruefe_raum(e: dict, raum_ids, kanon: frozenset[str], gesehen: set[str]) -> str:
    fehlend = [k for k in ("raum_id", "raum_typ", "sicherheit", "bestaetigt", "begruendung")
               if k not in e]
    if fehlend:
        return "Felder fehlen: " + ", ".join(fehlend)
    rid, typ, sich, best, begr = (e["raum_id"], e["raum_typ"], e["sicherheit"], e["bestaetigt"],
                                  e["begruendung"])
    if not isinstance(rid, str) or rid not in raum_ids:
        return "unbekannte raum_id"
    if rid in gesehen:
        return "raum_id doppelt"
    if not isinstance(typ, str) or (typ.strip().upper() not in kanon
                                    and typ.strip().upper() != UNBESTIMMT):
        return f"raum_typ {typ!r} außerhalb Kanon"
    if isinstance(sich, bool) or not isinstance(sich, (int, float)) or not 0 <= sich <= 1:
        return f"sicherheit {sich!r} nicht in 0–1"
    if not isinstance(best, bool):
        return f"bestaetigt {best!r} kein bool"
    if not isinstance(begr, str) or not begr.strip():
        return "begruendung leer"
    return ""


# --- Prompt -------------------------------------------------------------------------------

AUSGANGS_DEFINITION = (
    "Ausgang (final_exit) = Übergang aus dem Gebäude ins Freie: eine Straße oder eine Fläche, "
    "die nicht von Gebäuden umschlossen ist und von der man weg kann; eine Tür ist dafür nicht "
    "nötig. Innenhof = vom Gebäude umschlossene Fläche; Türen und Durchgänge in den Innenhof "
    "sind keine Ausgänge. Wohnungstür = Wohnungsausgang in Stiegenhaus oder Gang, kein Ausgang "
    "ins Freie."
)


def baue_prompt(anfrage: GeschossAnfrage, kanon: frozenset[str] | None = None) -> str:
    """Prompt-Version ``PROMPT_VERSION`` — Änderungen hier = neue Version = neuer Cache-Schlüssel.

    Keine lokalen Pfade im Prompt: weder die Plan-Datei noch Bildpfade (Bilder hängen als
    Datei am Aufruf, nicht im Text).
    """
    kanon = kanon_typen() if kanon is None else kanon
    raeume = [{"raum_id": r.raum_id, "engine_typ": r.engine_typ or None, "beleg": r.beleg or None,
               **r.merkmale} for r in anfrage.raeume]
    wo = anfrage.geschoss + (f", Quadrant {anfrage.quadrant}" if anfrage.quadrant else "")
    rolle = (
        "Du bist Elektroplaner und prüfst die Raumerkennung eines Geschossplans für die "
        "Notbeleuchtung. Die Engine hat gemessen (Wände, Flächen, Türen, Koordinaten); du liest "
        "den Plan wie ein Planer (Stempel, Möbel, Sanitär, Anordnung der Räume, Lage zur "
        "Wohnungseingangstür, Nachbarräume) und bestätigst oder widersprichst je Raum."
    )
    form = (
        "Antworte NUR mit JSON dieser Form, ein Eintrag je Raum-ID aus der Liste, keine anderen "
        'IDs: {"raeume": [{"raum_id": "...", "raum_typ": "<Kanon oder UNBESTIMMT>", '
        '"sicherheit": <0 bis 1>, "bestaetigt": <true, wenn du dem engine_typ zustimmst>, '
        '"begruendung": "<gesehene Belege: Stempel, Möbel, Lage, Nachbarn>"}]}'
    )
    erlaubt = (
        "Erlaubte Raumtypen (Kanon) — genau einer davon oder UNBESTIMMT, wenn du es nicht sicher "
        f"erkennst: {', '.join(sorted(kanon))}."
    )
    return "\n".join((
        rolle,
        f"Geschoss: {wo}. Das angehängte Bild zeigt das Geschoss mit den Raum-IDs.",
        erlaubt,
        AUSGANGS_DEFINITION,
        "Räume (engine_typ null = die Engine hat keinen Typ; beleg = woher ihr Typ kommt):",
        json.dumps(raeume, ensure_ascii=False, indent=1),
        form,
    ))


# --- Cache --------------------------------------------------------------------------------

@dataclass(frozen=True)
class CacheSchluessel:
    backend: str
    modell: str
    plan: str           # Dateiname ohne Pfad
    plan_sha: str       # SHA-256 der Plan-Datei (16 Hex)
    geschoss: str
    quadrant: str
    prompt_version: str


_UNSICHER = re.compile(r"[^A-Za-z0-9_.\-]+")


def _sauber(s: str) -> str:
    return _UNSICHER.sub("_", s).strip("_") or "-"


def plan_sha(pfad: Path) -> str:
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()[:16]


class KiCache:
    """Eine JSON-Datei je Frage: ``<plan>_<sha>/<geschoss>_<quadrant>_<backend>_<modell>_v<n>.json``."""

    def __init__(self, wurzel: Path):
        self.wurzel = Path(wurzel)
        self._sha: dict[str, str] = {}

    def schluessel(self, backend: str, modell: str, anfrage: GeschossAnfrage,
                   prompt_version: str) -> CacheSchluessel:
        key = str(anfrage.plan_datei.resolve())
        stat = anfrage.plan_datei.stat()
        marke = f"{key}|{stat.st_size}|{stat.st_mtime_ns}"
        if marke not in self._sha:
            self._sha[marke] = plan_sha(anfrage.plan_datei)
        return CacheSchluessel(backend, modell, anfrage.plan_datei.name, self._sha[marke],
                               anfrage.geschoss, anfrage.quadrant, prompt_version)

    def pfad(self, s: CacheSchluessel) -> Path:
        ordner = f"{_sauber(Path(s.plan).stem)}_{s.plan_sha}"
        name = "_".join(_sauber(t) for t in (s.geschoss, s.quadrant or "ganz", s.backend, s.modell))
        return self.wurzel / ordner / f"{name}_v{_sauber(s.prompt_version)}.json"

    def lies(self, s: CacheSchluessel, raum_ids: frozenset[str]) -> Antwort | None:
        p = self.pfad(s)
        if not p.is_file():
            return None
        daten = json.loads(p.read_text(encoding="utf-8"))
        raeume, verworfen, fehler = parse_antwort(daten.get("roh", ""), raum_ids)
        if fehler is not None:
            return None
        return Antwort(raeume=raeume, verworfen=verworfen, roh=daten.get("roh", ""),
                       modell=s.modell, quelle="cache")

    def schreibe(self, s: CacheSchluessel, antwort: Antwort) -> Path:
        p = self.pfad(s)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({
            "schluessel": asdict(s),
            "gespeichert": datetime.now(UTC).isoformat(timespec="seconds"),
            "raeume": [asdict(r) for r in antwort.raeume],
            "verworfen": antwort.verworfen,
            "roh": antwort.roh,
        }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        return p


# --- Orchestrierung -----------------------------------------------------------------------

class Zweitmeinung:
    """Cache → Backend → Cache. Zählt ``anfragen`` (echte Aufrufe) und ``treffer`` je Lauf.

    Fehler landen als ``ki:``-Warnung in ``warnungen`` (für bericht.md), nie als Ausnahme.
    """

    def __init__(self, konfig: KiKonfig, backend: ZweitmeinungBackend | None = None,
                 cache: KiCache | None = None):
        self.konfig = konfig
        self.backend = backend
        if self.backend is None and konfig.an:
            from .ki_backends import backend_aus_konfig
            self.backend = backend_aus_konfig(konfig)
        self.cache = cache or KiCache(konfig.cache_pfad)
        self.anfragen = 0
        self.treffer = 0
        self.warnungen: list[str] = []

    def frage(self, anfrage: GeschossAnfrage) -> Antwort:
        if not self.konfig.an or self.backend is None:
            return Antwort(quelle="aus")
        modelle = [self.konfig.modell] + (
            [self.konfig.fallback_modell]
            if self.konfig.fallback_modell and self.konfig.fallback_modell != self.konfig.modell
            else [])
        schluessel = [self.cache.schluessel(self.backend.name, m, anfrage, self.konfig.prompt_version)
                      for m in modelle]
        for s in schluessel:
            treffer = self.cache.lies(s, anfrage.raum_ids)
            if treffer is not None:
                self.treffer += 1
                return treffer
        antwort = Antwort()
        for modell, s in zip(modelle, schluessel):
            self.anfragen += 1
            antwort = self._rufe(anfrage, modell)
            antwort.modell, antwort.quelle = modell, "backend"
            if antwort.fehler is None:
                self.cache.schreibe(s, antwort)
                return antwort
            if antwort.fehler.art in ("limit", "login"):
                break  # gilt kontoweit — ein zweites Modell hilft nicht
        f = antwort.fehler
        self.warnungen.append(
            f"ki: {f.art} — {f.meldung} (Backend {self.backend.name}, Modell {antwort.modell}, "
            f"{anfrage.geschoss}{' ' + anfrage.quadrant if anfrage.quadrant else ''}); "
            "Engine-Ergebnis bleibt unverändert, Räume ohne Typ bleiben UNBESTIMMT mit Notlicht")
        return antwort

    def _rufe(self, anfrage: GeschossAnfrage, modell: str) -> Antwort:
        try:
            return self.backend.frage(anfrage, modell)
        except Exception as e:  # noqa: BLE001 — jede Backend-Ausnahme wird Warnung, kein Abbruch (Auftrag § 3)
            return Antwort(fehler=KiFehler("sonstig", f"{type(e).__name__}: {e}"))
