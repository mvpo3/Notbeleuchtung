"""M1-M4 der Diagnose als Gate-Messung: Caches rechnen, Messskripte starten, Kopfzahlen ziehen.

Die vier Skripte unter ``diagnose_skripte/`` sind der wortgetreue Quelltext aus
``docs/DIAGNOSE_RENNWEG_RAUMERKENNUNG.md`` (Commit 34b5dd0, Anhang A.1-A.4) — hier wird
nur aufgerufen und auf die Kopfzahlen der Tabellen in § 4 der Diagnose reduziert.
Nichts an der Erkennung wird angefasst.

„Wortgetreu" heißt: bis auf genau diese vier Abweichungen Byte für Byte der Anhang
(jede Abweichung steht auch im Kopf des betroffenen Skripts):
  1. Kopfkommentar mit Herkunftsvermerk (Anhang, Commit, „programmatisch extrahiert").
  2. ``# ruff: noqa`` in Zeile 1 — der Anhang ist nicht auf die Lint-Regeln dieses
     Repos geschrieben und wird bewusst nicht nachgezogen.
  3. Die Pfad-Zeilen: Repo-Wurzel aus ``NOTBEL_REPO`` (Pflicht, kein Default) statt
     eines hart verdrahteten Benutzerpfads, Cache-Wurzel aus ``NOTBEL_GATE_CACHES``
     statt ``REPO/Projekte/_ergebnis_raumerkennung``. Der DOCSTRING von A.1 nennt den
     alten Default-Pfad noch wortgetreu — er wurde nicht angefasst, damit der Text der
     Diagnose vergleichbar bleibt; gültig ist der Code darunter.
  4. Bei A.2-A.4 zusätzlich ein ergänztes ``import os`` — diese drei Anhänge importieren
     ``os`` nicht, brauchen es aber für Abweichung 3. A.1 importiert ``os`` selbst.

Herkunft jeder Kopfzahl im Skript-JSON (``p`` = Eintrag des Plans unter ``plaene``):
  M1.hauptwert                p.stiegenhaus.achsparallel_huelle_im_gedrehten.n
  M1.klein_ohne_stempel       p.klein_ohne_stempel.n
  M2.wert                     p.wert
  M2.inkl_freiflaechen        p.wert + p.frei.beruehrt_n
  M2.offen_m2                 p.aussen_offen_m2
  M3.hauptwert                p.rot_flaeche_in_raeumen.raeume_n
  M3.rote_flaeche_m2          p.rot_flaeche_in_raeumen.in_raeumen_m2
  M4.wohnungen                p.zahlen.wohnungen
  M4.einraum                  p.zahlen.einraum
  M4.datenbefund              p.zahlen.wohnungen_daten_erschliessung
  M4.darstellungsbefund       p.zahlen.wohnungen_darstellung_erschliessung
  M4.privatraum_ohne_wohnung  p.zahlen.privat_ohne_wohnung

``plaene`` ist bei M1/M4 eine Liste (Schlüssel ``plan``), bei M2/M3 ein Dict
(Schlüssel ``<Ergebnisordner>/<Plan>``); beides wird auf das Geschosskürzel gekürzt.

Aufruf (CLI):
  PY tests/gate/gate_m1_m4.py                              Caches rechnen und messen
  PY tests/gate/gate_m1_m4.py --caches <wurzel> --out <d>  vorhandene Caches messen
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
SKRIPTE = Path(__file__).resolve().parent / "diagnose_skripte"

PROJEKT = "Rennweg"
PLAENE = ("UG", "EG", "OG1", "OG2", "OG3", "DG1", "DG2")
DXF_NAME = "{} - Rennweg 15_1030 Wien_Ausfürung-2026-06-12.dxf"

# Skript-Kürzel -> (Datei, Argument für die Ausgabedatei; None = erstes Positionsargument)
MESSSKRIPTE = {
    "M1": ("m1_stiegenhaus_achsparallel.py", None),
    "M2": ("m2_aussen_auf_innenraum.py", "--out"),
    "M3": ("m3_schacht_ohne_stanzung.py", "--out"),
    "M4": ("m4_wohnungen.py", None),
}

M4_FELDER = (("wohnungen", "wohnungen"),
             ("einraum", "einraum"),
             ("datenbefund", "wohnungen_daten_erschliessung"),
             ("darstellungsbefund", "wohnungen_darstellung_erschliessung"),
             ("privatraum_ohne_wohnung", "privat_ohne_wohnung"))

# Kopfzahlen, bei denen "höher = schlechter" gilt; nur diese vergleicht das Gate.
# Nicht verglichen (nur berichtet): M4.wohnungen, M2.offen_m2.
# ``M3.rote_flaeche_m2`` ist eine Fläche, also eine Fließkommazahl — ``gate_regel``
# vergleicht sie mit Toleranz 0,001 (nachher <= vorher + 0,001), Ganzzahlen exakt.
GATE_KENNZAHLEN = ("M1.hauptwert", "M1.klein_ohne_stempel",
                   "M2.wert", "M2.inkl_freiflaechen",
                   "M3.hauptwert", "M3.rote_flaeche_m2",
                   "M4.einraum", "M4.datenbefund", "M4.darstellungsbefund",
                   "M4.privatraum_ohne_wohnung")


def _sha256(pfad: Path) -> str:
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _umgebung(repo: Path, **zusatz: str) -> dict[str, str]:
    """PYTHONPATH mit dem src/ DIESES Worktrees zuerst — die venv trägt ein
    editable install auf einen anderen Checkout."""
    e = dict(os.environ)
    e["PYTHONPATH"] = os.pathsep.join(
        p for p in (str(WURZEL / "src"), e.get("PYTHONPATH", "")) if p)
    e["PYTHONIOENCODING"] = "utf-8"
    e.update(zusatz)
    return e


def _pruefe_paket(env: dict[str, str]) -> str:
    """notbeleuchtung muss aus diesem Worktree kommen, sonst misst man fremden Code."""
    datei = subprocess.run([sys.executable, "-c", "import notbeleuchtung as n; print(n.__file__)"],
                           capture_output=True, text=True, check=True, env=env).stdout.strip()
    if WURZEL not in Path(datei).resolve().parents:
        raise RuntimeError(f"notbeleuchtung kommt aus {datei}, nicht aus {WURZEL}")
    return datei


def _schluessel(repo: Path) -> str:
    """Kurz-SHA von HEAD; ungesicherte Änderungen unter src/ oder scripts/ hängen
    ``-dirty-<Inhalts-Hash>`` an — dann ist der SHA nicht der Code, der gerechnet hat.

    Der Hash ist der Inhalt, nicht die Uhrzeit: sha256 über ``git diff HEAD -- src
    scripts`` plus Name und Inhalt jeder untracked Datei darunter. Ein zweiter Lauf
    auf DEMSELBEN Arbeitsstand trifft damit denselben Cache, eine Codeänderung nie.
    """
    def git(*a: str) -> str:
        return subprocess.run(["git", "-C", str(repo), *a],
                              capture_output=True, text=True, check=False).stdout.strip()

    sha = git("rev-parse", "--short", "HEAD") or "?"
    if not git("status", "--porcelain", "--", "src", "scripts"):
        return sha
    h = hashlib.sha256(git("diff", "HEAD", "--", "src", "scripts").encode("utf-8"))
    for rel in git("ls-files", "--others", "--exclude-standard", "--",
                   "src", "scripts").splitlines():
        h.update(rel.encode("utf-8"))
        datei = repo / rel
        h.update(datei.read_bytes() if datei.is_file() else b"")
    return f"{sha}-dirty-{h.hexdigest()[:12]}"


def _status(versionsordner: Path) -> dict[str, str]:
    """Geschosskürzel -> ``status`` aus kennzahlen.json, ``fehlt`` wenn keine da ist."""
    da = {}
    if versionsordner.is_dir():
        for kz in sorted(versionsordner.glob("*/kennzahlen.json")):
            daten = json.loads(kz.read_text(encoding="utf-8"))
            da[kz.parent.name.split(" - ")[0]] = daten.get("status", "?")
    return {g: da.get(g, "fehlt") for g in PLAENE}


def erzeuge_caches(repo: Path) -> Path:
    """Stufe 1 auf den 7 Rennweg-Grundrissen; Rückgabe: der Versionsordner ``Rennweg_v0``.

    Eigener Eingang unter ``_arbeit/gate/eingang/``, weil ``raumerkennung_darstellung.py``
    im Eingang ZIPs entpackt — auf ``Projekte/`` losgelassen zöge das den ganzen Bestand
    auf die Platte. Ein fertiger Versionsordner wird wiederverwendet (das Darstellungs-
    skript überschreibt eine Version ohnehin nie).
    """
    repo = Path(repo)
    quelle = repo / "Projekte" / PROJEKT
    eingang = repo / "_arbeit" / "gate" / "eingang" / PROJEKT
    eingang.mkdir(parents=True, exist_ok=True)
    for geschoss in PLAENE:
        dxf = quelle / DXF_NAME.format(geschoss)
        if not dxf.is_file():
            raise FileNotFoundError(dxf)
        ziel_dxf = eingang / dxf.name
        if not ziel_dxf.is_file() or _sha256(ziel_dxf) != _sha256(dxf):
            shutil.copy2(dxf, ziel_dxf)

    out = repo / "_arbeit" / "gate" / _schluessel(repo)
    versionsordner = out / f"{PROJEKT}_v0"
    if any(s != "ok" for s in _status(versionsordner).values()):
        subprocess.run(
            [sys.executable, str(repo / "scripts" / "analyse" / "raumerkennung_darstellung.py"),
             "--eingang", str(eingang.parent), "--ordner", PROJEKT,
             "--version", "v0", "--slices", "gate", "--out", str(out)],
            cwd=str(repo), env=_umgebung(repo), check=True)
    schlecht = {g: s for g, s in _status(versionsordner).items() if s != "ok"}
    if schlecht:
        raise RuntimeError(f"Stufe 1 nicht für alle 7 Pläne ok: {schlecht}")
    return versionsordner


def _kuerzel(name: str) -> str:
    """``./DG1`` oder ``DG1 - Rennweg 15_…`` -> ``DG1``."""
    return name.rsplit("/", 1)[-1].split(" - ")[0]


def _reduziere(roh: dict) -> dict:
    """Skript-JSONs auf die Kopfzahlen der Diagnose-Tabellen § 4 (siehe Modul-Docstring)."""
    return {
        "M1": {_kuerzel(p["plan"]): {
            "hauptwert": p["stiegenhaus"]["achsparallel_huelle_im_gedrehten"]["n"],
            "klein_ohne_stempel": p["klein_ohne_stempel"]["n"]}
            for p in roh["M1"]["plaene"]},
        "M2": {_kuerzel(k): {
            "wert": p["wert"],
            "inkl_freiflaechen": p["wert"] + p["frei"]["beruehrt_n"],
            "offen_m2": p["aussen_offen_m2"]}
            for k, p in roh["M2"]["plaene"].items()},
        "M3": {_kuerzel(k): {
            "hauptwert": p["rot_flaeche_in_raeumen"]["raeume_n"],
            "rote_flaeche_m2": p["rot_flaeche_in_raeumen"]["in_raeumen_m2"]}
            for k, p in roh["M3"]["plaene"].items()},
        "M4": {_kuerzel(p["plan"]): {kopf: p["zahlen"][feld] for kopf, feld in M4_FELDER}
               for p in roh["M4"]["plaene"]},
    }


def messe(repo: Path, cache_wurzel: Path, ausgabe: Path | None = None) -> dict:
    """Die vier Messskripte auf ``cache_wurzel`` laufen lassen und reduzieren.

    ``ausgabe`` nimmt die vollen Skript-JSONs auf (unverändert, Pfade im Ergebnis unter
    ``dateien``); Vorgabe ist ``<cache_wurzel>/../messung/<Name der Cache-Wurzel>/``.
    Ein fremder Cache-Bestand wird nur gelesen — dann ``ausgabe`` mitgeben.
    """
    repo, cache_wurzel = Path(repo), Path(cache_wurzel)
    ausgabe = Path(ausgabe) if ausgabe else cache_wurzel.parent / "messung" / cache_wurzel.name
    ausgabe.mkdir(parents=True, exist_ok=True)
    env = _umgebung(repo, NOTBEL_REPO=str(repo), NOTBEL_GATE_CACHES=str(cache_wurzel))
    paket = _pruefe_paket(env)

    roh, dateien, dauer = {}, {}, {}
    for kuerzel, (datei, flag) in MESSSKRIPTE.items():
        ziel = ausgabe / f"{kuerzel.lower()}.json"
        t0 = time.time()
        subprocess.run([sys.executable, str(SKRIPTE / datei),
                        *([flag, str(ziel)] if flag else [str(ziel)])],
                       cwd=str(repo), env=env, check=True)
        roh[kuerzel] = json.loads(ziel.read_text(encoding="utf-8"))
        dateien[kuerzel] = str(ziel)
        dauer[kuerzel] = round(time.time() - t0, 1)
    return {**_reduziere(roh), "dateien": dateien, "dauer_s": dauer,
            "repo": str(repo), "cache_wurzel": str(cache_wurzel), "paket": paket}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="M1-M4 der Diagnose auf den 7 Rennweg-Plänen.")
    ap.add_argument("--repo", default=str(WURZEL))
    ap.add_argument("--caches", help="vorhandene Cache-Wurzel; ohne Angabe wird Stufe 1 gerechnet")
    ap.add_argument("--out", help="Ordner für die Skript-JSONs")
    a = ap.parse_args(argv)
    repo = Path(a.repo)
    wurzel = Path(a.caches) if a.caches else erzeuge_caches(repo)
    ergebnis = messe(repo, wurzel, Path(a.out) if a.out else None)
    print(json.dumps(ergebnis, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
