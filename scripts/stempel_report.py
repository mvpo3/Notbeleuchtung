"""stempel_report — Raumstempel eines Plans finden, Polygonen zuordnen, Tabelle drucken.

Aufruf: python scripts/stempel_report.py <dxf> [--radius N]
Läuft auch ohne Raum-Polygone (dann nur Stempelliste); Exit 0 auch bei 0 Stempeln.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.stdout.reconfigure(encoding="utf-8")

from notbeleuchtung.raumerkennung.dxf_load import lade_dxf
from notbeleuchtung.raumerkennung.raumlayer import raeume_aus_layer
from notbeleuchtung.raumerkennung.stempel_anker import (
    finde_stempel,
    ordne_zu,
    restflaechen,
    zentrum,
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dxf")
    ap.add_argument("--radius", type=float, default=1500.0,
                    help="Gruppier-Radius für lose Stempel-Texte in mm (Default 1500)")
    args = ap.parse_args()

    plan = lade_dxf(args.dxf)
    stempel = finde_stempel(plan, radius_mm=args.radius)

    raeume = raeume_aus_layer(plan)
    if not raeume:
        try:
            from notbeleuchtung.raumerkennung.waende import raeume_aus_waenden
            raeume = raeume_aus_waenden(plan)
        except Exception as exc:  # noqa: BLE001 — Wand-Fallback darf den Report nie killen
            print(f"(Wand-Fallback fehlgeschlagen: {exc})")
            raeume = []

    print(f"{Path(args.dxf).name}: {len(stempel)} Stempel, {len(raeume)} Raum-Polygone\n")
    kopf = f"{'Name':<28} {'Typ':<16} {'m² Stempel':>10} {'m² Polygon':>10} {'Abw %':>7} Flag"
    print(kopf)
    print("-" * len(kopf))
    zuordnungen = ordne_zu(stempel, raeume)
    for z in zuordnungen:
        st = z.stempel
        poly_m2 = f"{z.raum.flaeche_m2:.2f}" if z.raum is not None else "-"
        abw = f"{z.abweichung_prozent:+.1f}" if z.abweichung_prozent is not None else "-"
        m2 = f"{st.flaeche_m2:.2f}" if st.flaeche_m2 is not None else "-"
        print(f"{st.name:<28.28} {st.typ or '-':<16} {m2:>10} {poly_m2:>10} {abw:>7} {z.flag}")

    rest = restflaechen(raeume, zuordnungen)
    if rest:
        print(f"\nRestflächen ohne Stempel ({len(rest)}) — Kandidaten STG/Gang/Schacht/VR:")
        for r in rest:
            cx, cy = zentrum(r)
            print(f"  {r.flaeche_m2:8.2f} m²  Zentrum ({cx / 1000:.2f}, {cy / 1000:.2f}) m")
    return 0


if __name__ == "__main__":
    sys.exit(main())
