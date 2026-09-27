"""Ein vollständiger Gate-Messlauf: Herkunft, 18 Erwartungen, Referenz, OG1, OG3,
Barawitzka, DG1 (mit Lift-Ausgängen UG/EG/OG1 als Information), M1-M4.

``messung(repo)`` liefert das Vergleichsobjekt des Türstapel-Gates. Es enthält
NUR Zahlen, IDs, Typen und Namen — keine absoluten Pfade, keine Koordinaten und
keine Sondenwerte aus dem Referenzpaket (das Repo ist öffentlich, das Paket
nicht). Die Referenz wird zur Laufzeit gelesen (``gate_m17.referenz_pfad``).

``meta`` trägt die Herkunft, damit eine Zahl später einem Codestand zuzuordnen
ist: Commit, Tree-Hash der Raumerkennung, Vergleich gegen den Basis-Commit
f15d03f, Contract-Version, SHA-256 der Eingabe-DXF und der Referenz sowie die
Toleranzen, mit denen gemessen wurde.

Aufruf (CLI):
  PY tests/gate/gate_messung.py --out <datei.json>
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[2]
# Die venv trägt ein editable install auf einen ANDEREN Checkout — src/ dieses
# Worktrees muss vorne stehen, sonst misst man fremden Code (unten geprüft).
# ``tests`` kommt dazu, weil ``plaene`` dort liegt (unter pytest erledigt das
# ``pythonpath``, beim CLI-Aufruf nicht).
for _pfad in (WURZEL / "src", WURZEL / "tests", Path(__file__).resolve().parent):
    if str(_pfad) not in sys.path:
        sys.path.insert(0, str(_pfad))

import gate_barawitzka
import gate_dg1
import gate_m1_m4
import gate_m17
import gate_og1
import gate_og3
import gate_referenz
from gate_lauf import erkenne, sha256_datei

from plaene import BARAWITZKA_EG, RENNWEG_OG3

BASIS_COMMIT = "f15d03fe1a082c78b180e940b7dcd666fccaf37d"
RAUMERKENNUNG = "src/notbeleuchtung/raumerkennung"


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, check=False).stdout.strip()


def dxf_pfad(repo: Path, plan: str) -> Path:
    return repo / "Projekte" / gate_m1_m4.PROJEKT / gate_m1_m4.DXF_NAME.format(plan)


def _code_pfad(repo: Path) -> str:
    """notbeleuchtung.__file__ relativ zum Repo — und der Beweis, dass es von hier kommt."""
    import notbeleuchtung
    datei = Path(notbeleuchtung.__file__).resolve()
    if repo.resolve() not in datei.parents:
        raise RuntimeError(f"notbeleuchtung kommt aus {datei}, nicht aus {repo}")
    return datei.relative_to(repo.resolve()).as_posix()


def _meta(repo: Path, referenz: Path, laufzeit_s: float) -> dict:
    from notbeleuchtung.hauptengine.contracts import raum_modell
    tree = _git(repo, "rev-parse", f"HEAD:{RAUMERKENNUNG}")
    return {
        "datum": datetime.now().astimezone().isoformat(timespec="seconds"),
        "commit_head": _git(repo, "rev-parse", "HEAD"),
        "arbeitsbaum_src_scripts_sauber":
            not _git(repo, "status", "--porcelain", "--", "src", "scripts"),
        "raumerkennung_tree": tree,
        "basis_commit": BASIS_COMMIT,
        "basis_tree_gleich": tree == _git(repo, "rev-parse", f"{BASIS_COMMIT}:{RAUMERKENNUNG}"),
        "contract_version": raum_modell.CONTRACT_VERSION,
        "code_pfad": _code_pfad(repo),
        "referenz_sha256": sha256_datei(referenz),
        "toleranzen": {"kontakt_mm": gate_m17.KONTAKT_TOL_MM,
                       "ueberlappung_mm2": gate_m17.UEBERLAPPUNG_TOL_MM2,
                       "portal_wand_mm": gate_m17.PORTAL_WAND_MM},
        "dxf": {plan: sha256_datei(dxf_pfad(repo, plan)) for plan in gate_m1_m4.PLAENE},
        "laufzeit_s": laufzeit_s,
    }


def messung(repo: Path) -> dict:
    """Alle Messfälle des Gates: meta, m17, referenz, og1, og3, barawitzka, dg1,
    lift_ausgaenge_info, m1_m4."""
    repo = Path(repo)
    referenz = gate_m17.referenz_pfad()
    if referenz is None:
        raise FileNotFoundError(
            "Referenz-JSON des Übergabepakets nicht gefunden — Pfad über NOTBEL_M17_REFERENZ "
            "setzen (das Paket gehört nicht ins Repo).")
    t0 = time.monotonic()

    lauf = erkenne(dxf_pfad(repo, "OG1"))
    ref = gate_m17.lade_referenz(referenz)
    m17 = gate_m17.messe(ref, lauf.modell.raeume, lauf.modell.tueren,
                         lauf.kaskade.wandkoerper, lauf.plan.factor)
    referenz_verbindungen = gate_referenz.verbindungen(lauf.modell)
    og1 = gate_og1.kennzahlen(lauf.modell)
    # Rennweg OG3 mit floor "OG3" — derselbe Plan, den ``meta.dxf["OG3"]``
    # fingerprintet, und dasselbe ``floor`` wie tests/naht/test_soll_rennweg.py.
    og3 = gate_og3.kennzahlen_og3(erkenne(RENNWEG_OG3, "OG3").modell)
    # Einziger Messfall außerhalb der Rennweg-Familie (Bedingung (10), § 8e):
    # der ABSTELLRAUM 1,98 m² des Barawitzka-EG. Kostet einen zusätzlichen Parse.
    barawitzka = gate_barawitzka.verbindung_abstellraum(erkenne(BARAWITZKA_EG, "EG").modell)
    # Bedingung (11): Rennweg DG1 behält einen Ausgang, keiner durch den Liftschacht.
    # UG/EG/OG1 nur als Information (Lifttür-Ausgänge, Nebenbefund VA-5) — ohne Regel.
    dg1 = gate_dg1.ausgaenge_lift(erkenne(dxf_pfad(repo, "DG1"), "DG1").modell)
    lift_info = {plan: gate_dg1.ausgaenge_lift(erkenne(dxf_pfad(repo, plan), plan).modell)
                 for plan in ("UG", "EG")}
    lift_info["OG1"] = gate_dg1.ausgaenge_lift(lauf.modell)
    # Nur die Kopfzahlen übernehmen: das rohe Ergebnis führt absolute Pfade und Laufzeiten.
    roh = gate_m1_m4.messe(repo, gate_m1_m4.erzeuge_caches(repo))
    m1_m4 = {k: roh[k] for k in ("M1", "M2", "M3", "M4")}

    laufzeit = round(time.monotonic() - t0, 1)
    return {"meta": _meta(repo, referenz, laufzeit), "m17": m17,
            "referenz": referenz_verbindungen, "og1": og1, "og3": og3,
            "barawitzka": barawitzka, "dg1": dg1, "lift_ausgaenge_info": lift_info,
            "m1_m4": m1_m4}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Vollständiger Gate-Messlauf (M17, OG1, OG3, Barawitzka, DG1, M1-M4).")
    ap.add_argument("--repo", default=str(WURZEL))
    ap.add_argument("--out", required=True, help="Zieldatei für die Messung (JSON)")
    a = ap.parse_args(argv)
    ergebnis = messung(Path(a.repo))
    ziel = Path(a.out)
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=1, sort_keys=False),
                    encoding="utf-8")
    for e in ergebnis["m17"]:
        print(f"{e['id']:10s} {e['status']}")
    bestehend = [e for e in ergebnis["referenz"]["verneint"] if e["anzahl"] != 0]
    fehlend = [e for e in ergebnis["referenz"]["gefordert"]
               if e["anzahl"] is None or e["anzahl"] < 1]
    print(f"Referenz: {len(bestehend)} verneinte Verbindungen bestehen, "
          f"{len(fehlend)} geforderte Übergänge fehlen")
    print(f"OG1: {ergebnis['og1']['raeume_gesamt']} Räume, "
          f"{ergebnis['og1']['tueren_gesamt']} Türen, "
          f"a==b {ergebnis['og1']['tueren_raum_a_gleich_b']}, "
          f"Einraum-Wohnungen {ergebnis['og1']['einraum_wohnungen']}")
    print(f"OG3: {ergebnis['og3']['segmente_graph']} GRAPH-Segmente, "
          f"{ergebnis['og3']['anker_gesamt']} Anker, davon "
          f"{ergebnis['og3']['anker_in_wohnung_privat']} in WOHNUNG_PRIVAT")
    bara = ergebnis["barawitzka"]
    print(f"Barawitzka EG: {bara['bezeichnung']} hat {bara['anzahl']} Verbindung(en)"
          + (f" — {bara['grund']}" if bara["grund"] else ""))
    for plan, e in (("DG1", ergebnis["dg1"]), *ergebnis["lift_ausgaenge_info"].items()):
        print(f"{plan}: {e['ausgaenge']} Ausgänge, davon {e['ausgaenge_durch_liftschacht']} "
              "durch den Liftschacht "
              f"{[a['id'] for a in e['ausgaenge_liste'] if a['durch_liftschacht']]}"
              + (f" — {e['grund']}" if e["grund"] else ""))
    print(f"geschrieben: {ziel.name} ({ergebnis['meta']['laufzeit_s']} s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
