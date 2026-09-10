"""Freigabeprüfung `contract-freeze`: die Prüfgrundlage gehört dem BASE, nicht dem PR.

Der Check entscheidet, ob ein Contract-PR gemergt werden darf. Läse er
`.github/CODEOWNERS` aus dem Arbeitsbaum, könnte ein PR im selben Commit die
Owner-Liste umschreiben und sich die eigene Freigabe erteilen. Diese Tests
halten fest, dass die Liste am `base_sha` gelesen wird und dass jeder Weg, auf
dem die Grundlage fehlt, in einem **Abbruch** endet — nie in einer Freigabe.
"""
from __future__ import annotations

import base64
import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

SKRIPT = Path(__file__).resolve().parents[2] / ".github/scripts/contract_freeze_check.py"
BASE = "1e0b38d5247938b96baead81ee213a97425d4b87"
HEAD = "6a96eb5ca025d1224043705c60e9599b231d2552"
OWNER_ZEILE = "/src/notbeleuchtung/hauptengine/contracts/  @mvpo3 @EnisAMG @polatselman\n"
ECHTE_OWNER = ["mvpo3", "EnisAMG", "polatselman"]


def _laden(monkeypatch, base_sha=BASE, head_sha=HEAD):
    """Modul frisch laden — REPO/PR/HEAD_SHA/BASE_SHA werden beim Import gelesen."""
    for k, v in {"REPO": "mvpo3/Notbeleuchtung", "PR": "152",
                 "HEAD_SHA": head_sha, "BASE_SHA": base_sha,
                 "NO_COMMENT": "1"}.items():
        monkeypatch.setenv(k, v)
    spec = importlib.util.spec_from_file_location("cfc", SKRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _inhalt(text: str) -> dict:
    return {"encoding": "base64",
            "content": base64.b64encode(text.encode("utf-8")).decode("ascii")}


def _codeowners_im_arbeitsbaum(tmp_path, monkeypatch, zeile: str) -> Path:
    """Eine CODEOWNERS-Datei, wie ein PR sie mitliefern könnte."""
    d = tmp_path / ".github"
    d.mkdir(parents=True)
    (d / "CODEOWNERS").write_text(zeile, encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    return d / "CODEOWNERS"


# ── 1. Ein PR kann die benötigte Zustimmung nicht wegdefinieren ──────────────
def test_owner_kommen_vom_base_nicht_aus_dem_arbeitsbaum(tmp_path, monkeypatch):
    mod = _laden(monkeypatch)
    # Der PR liefert eine manipulierte Liste mit nur einem (dem eigenen) Owner:
    _codeowners_im_arbeitsbaum(
        tmp_path, monkeypatch,
        "/src/notbeleuchtung/hauptengine/contracts/  @polatselman\n")
    gerufen = []

    def fake_gh(pfad, *a):
        gerufen.append(pfad)
        assert f"?ref={BASE}" in pfad, f"CODEOWNERS nicht am Base gelesen: {pfad}"
        return _inhalt(OWNER_ZEILE)

    monkeypatch.setattr(mod, "gh", fake_gh)
    assert mod.owners() == ECHTE_OWNER          # Base gewinnt, nicht der PR
    assert gerufen and ".github/CODEOWNERS" in gerufen[0]


def test_arbeitsbaum_datei_wird_gar_nicht_geoeffnet(tmp_path, monkeypatch):
    """Härter als der Test darüber: die lokale Datei darf nicht einmal gelesen
    werden — sonst hinge das Ergebnis an der Reihenfolge von Fallbacks."""
    mod = _laden(monkeypatch)
    pfad = _codeowners_im_arbeitsbaum(tmp_path, monkeypatch, "/x @wer-auch-immer\n")
    pfad.chmod(0o000)                            # jeder Lesezugriff scheitert
    monkeypatch.setattr(mod, "gh", lambda p, *a: _inhalt(OWNER_ZEILE))
    try:
        assert mod.owners() == ECHTE_OWNER
    finally:
        pfad.chmod(0o644)


# ── 2. Fehlende oder unlesbare Grundlage ⇒ Abbruch, niemals Freigabe ─────────
@pytest.mark.parametrize("fall", ["base_sha_leer", "api_fehler", "kein_json",
                                  "falsches_encoding", "kaputtes_base64",
                                  "zeile_fehlt", "zeile_ohne_owner"])
def test_unlesbare_grundlage_fuehrt_nie_zur_freigabe(monkeypatch, fall, capsys):
    mod = _laden(monkeypatch, base_sha="" if fall == "base_sha_leer" else BASE)

    def fake_gh(pfad, *a):
        if fall == "api_fehler":
            raise subprocess.CalledProcessError(1, "gh", stderr="HTTP 404: Not Found")
        if fall == "kein_json":
            raise json.JSONDecodeError("kaputt", "", 0)
        if fall == "falsches_encoding":
            return {"encoding": "none", "content": ""}
        if fall == "kaputtes_base64":
            return {"encoding": "base64", "content": "###kein-base64###"}
        if fall == "zeile_fehlt":
            return _inhalt("/src/notbeleuchtung/normwissen/  @EnisAMG\n")
        return _inhalt("/src/notbeleuchtung/hauptengine/contracts/\n")

    monkeypatch.setattr(mod, "gh", fake_gh)
    with pytest.raises(SystemExit) as exc:
        mod.owners()
    # sys.exit(<text>) → Code ist der Text, Rueckgabecode des Prozesses = 1.
    assert exc.value.code not in (0, None), "Abbruch darf nicht als Erfolg enden"
    assert "Abbruch statt Freigabe" in str(exc.value.code)


# ── 3. Fehlende und veraltete Zustimmungen bleiben abgelehnt ─────────────────
def _stub_api(mod, monkeypatch, reviews, dateien=None, commits=None):
    dateien = dateien if dateien is not None else [
        {"filename": "src/notbeleuchtung/hauptengine/contracts/raum_modell.py",
         "patch": "@@ -18 +18 @@\n-CONTRACT_VERSION = \"1.3.0\"\n+CONTRACT_VERSION = \"1.4.0\""}]
    commits = commits if commits is not None else [{"sha": "aaaaaaa"}, {"sha": HEAD}]

    def fake_gh(pfad, *a):
        if "/contents/" in pfad:
            assert f"?ref={BASE}" in pfad
            return _inhalt(OWNER_ZEILE)
        if pfad.endswith("/files"):
            return dateien
        if pfad.endswith("/reviews"):
            return reviews
        if pfad.endswith("/commits"):
            return commits
        raise AssertionError(f"unerwarteter API-Pfad: {pfad}")

    monkeypatch.setattr(mod, "gh", fake_gh)
    monkeypatch.setattr(mod, "upsert_comment", lambda body: None)


def _review(login, state, commit_id, wann="2026-09-10T10:00:00Z"):
    return {"user": {"login": login}, "state": state,
            "commit_id": commit_id, "submitted_at": wann}


def test_fehlende_zustimmung_bleibt_abgelehnt(monkeypatch, capsys):
    mod = _laden(monkeypatch)
    _stub_api(mod, monkeypatch, reviews=[_review("EnisAMG", "APPROVED", HEAD)])
    assert mod.main() == 1                       # zwei Owner fehlen
    assert "FEHLGESCHLAGEN" in capsys.readouterr().out


def test_veraltete_zustimmung_bleibt_abgelehnt(monkeypatch, capsys):
    mod = _laden(monkeypatch)
    _stub_api(mod, monkeypatch, reviews=[
        _review(o, "APPROVED", "aaaaaaa") for o in ECHTE_OWNER])
    assert mod.main() == 1                       # alle drei auf altem Stand
    aus = capsys.readouterr().out
    assert "veraltet" in aus and "FEHLGESCHLAGEN" in aus


def test_changes_requested_zaehlt_nicht_als_zustimmung(monkeypatch):
    mod = _laden(monkeypatch)
    _stub_api(mod, monkeypatch, reviews=[
        _review("mvpo3", "APPROVED", HEAD, "2026-09-10T09:00:00Z"),
        _review("EnisAMG", "APPROVED", HEAD, "2026-09-10T09:00:00Z"),
        _review("polatselman", "APPROVED", HEAD, "2026-09-10T09:00:00Z"),
        _review("polatselman", "CHANGES_REQUESTED", HEAD, "2026-09-10T11:00:00Z"),
    ])
    assert mod.main() == 1


# ── 4. Gültige Zustimmung am tatsächlich geprüften Head wird anerkannt ───────
def test_gueltige_zustimmung_am_head_wird_anerkannt(monkeypatch, capsys):
    mod = _laden(monkeypatch)
    _stub_api(mod, monkeypatch, reviews=[
        _review(o, "APPROVED", HEAD) for o in ECHTE_OWNER])
    assert mod.main() == 0
    aus = capsys.readouterr().out
    assert "**OK**" in aus
    assert BASE in aus, "Herkunft der Owner-Liste gehoert in die Zusammenfassung"


def test_ohne_contract_touch_gruen_und_ohne_owner_abfrage(monkeypatch):
    """Der Check taugt nur als Required Status Check, wenn er sonst grün ist —
    und darf dafür die Owner-Liste gar nicht erst brauchen."""
    mod = _laden(monkeypatch)

    def fake_gh(pfad, *a):
        if pfad.endswith("/files"):
            return [{"filename": "docs/CONTRACTS.md", "patch": "+CONTRACT_VERSION als Prosa"}]
        raise AssertionError(f"kein weiterer API-Aufruf erwartet: {pfad}")

    monkeypatch.setattr(mod, "gh", fake_gh)
    assert mod.main() == 0
