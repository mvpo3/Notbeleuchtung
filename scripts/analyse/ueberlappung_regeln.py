"""ueberlappung_regeln — kumulative Wirkung der fünf Bereinigungsregeln messen.

Aufruf:
    python scripts/analyse/ueberlappung_regeln.py [--ergebnis DIR]
        [--plan Muthgasse_E2 ...] [--regeln 0 1 12 123 1234 12345]

Datenquelle sind die EINGECHECKTEN Laufergebnisse
``Projekte/_ergebnis/<Plan>/raeume.json`` (dieselbe Basis wie
``tests/naht/test_ueberlappung_riegel.py``). Regel- und Messlogik kommen
AUSSCHLIESSLICH aus ``raumerkennung.bereinigung`` — dieses Skript hält keine
eigene Kopie, sonst misst es sich selbst statt des Produktionscodes.

``--regeln`` nimmt Ziffernfolgen als Stufen: ``0`` = keine Regel, ``12`` =
Regeln 1 und 2. Default ist die kumulative Reihe {} {1} {1,2} {1,2,3} {1,2,3,4}
{1,2,3,4,5}.

Läufe vor der ersten Neuerzeugung der Ergebnisse fallen auf die Altfelder
zurück: fehlt ``polygon_roh``, gilt ``polygon_mm`` als Roh-Ring; fehlt
``raum_typ``, gilt das Stempel-Feld ``typ`` als Typ-Quelle (nachweislich
deckungsgleich, aber nicht per Konstruktion — die Stufe ``{1}`` prüft das).

Akzeptanzkriterien (§ 6 der Umsetzungs-Spezifikation):
  (a) Stufe {} reproduziert die Riegel-Bänder des Laufs exakt — dazu wird die
      Riegel-Basis (nur ``raeume[]``, ``polygon_mm``) separat gemessen.
  (b) Stufe {1} trifft genau die Paare, bei denen ``raum_typ`` EINER Seite
      LIFT/SCHACHT ist (gegengerechnet über die Roh-Paare).
  (c) Stufe {1,2,3,4,5} lässt kein Paar > 1 mm² übrig.
  (d) Für jeden Raum gilt die Flächen-Buchhaltung.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8")

from shapely.geometry import Polygon
from shapely.strtree import STRtree

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum
from notbeleuchtung.raumerkennung.bereinigung import (
    LIFT_SCHACHT,
    RAUSCH_MM2,
    bereinige,
    ueberlappung,
)

STUFEN = ("0", "1", "12", "123", "1234", "12345")


def _laden(pfad: Path) -> tuple[list[Raum], dict[str, str], dict[str, float | None],
                                list[list]]:
    """(Räume auf Roh-Ringen, quelle, stempel_m2, Riegel-Basis-Ringe)."""
    daten = json.loads(pfad.read_text(encoding="utf-8"))
    raeume: list[Raum] = []
    quelle: dict[str, str] = {}
    stempel: dict[str, float | None] = {}
    for e in list(daten.get("raeume", [])) + list(daten.get("entfallen", [])):
        # polygon_roh gewinnt: nach einem Bereinigungs-Lauf steht dort der
        # Zustand VOR der Bereinigung, den diese Messung braucht.
        ring = e.get("polygon_roh") or e.get("polygon_mm") or []
        if len(ring) < 3:
            continue
        rid = e["id"]
        raeume.append(Raum(id=rid,
                           raum_typ=(e.get("raum_typ") or e.get("typ") or ""),
                           polygon_mm=[(float(x), float(y)) for x, y in ring]))
        quelle[rid] = e.get("quelle") or ""
        stempel[rid] = e.get("flaeche_stempel")
    riegel = [e.get("polygon_mm") or [] for e in daten.get("raeume", [])]
    return raeume, quelle, stempel, riegel


def _paare(ringe: dict[str, list]) -> list[tuple[str, str, float]]:
    """Alle Paare mit Schnittfläche > Rauschschwelle, in mm²."""
    geo = {i: Polygon(r) for i, r in ringe.items() if len(r) >= 3}
    geo = {i: (p if p.is_valid else p.buffer(0)) for i, p in geo.items()}
    ids = sorted(i for i, p in geo.items() if not p.is_empty and p.area > 0)
    reihe = [geo[i] for i in ids]
    if not reihe:
        return []
    baum = STRtree(reihe)
    out = []
    for k, i in enumerate(ids):
        for m in baum.query(reihe[k]):
            m = int(m)
            if m <= k:
                continue
            flaeche = reihe[k].intersection(reihe[m]).area
            if flaeche > RAUSCH_MM2:
                out.append((i, ids[m], flaeche))
    return out


def _stufe(text: str) -> frozenset[int]:
    return frozenset(int(c) for c in text if c in "12345")


def _messe_plan(pfad: Path, stufen: tuple[str, ...]) -> dict:
    raeume, quelle, stempel, riegel_ringe = _laden(pfad)
    roh_ringe = {r.id: list(r.polygon_mm) for r in raeume}
    typ = {r.id: (r.raum_typ or "").strip().upper() for r in raeume}

    riegel_idx, riegel_flaeche = ueberlappung(riegel_ringe)
    basis_n = None
    zeilen = []
    for text in stufen:
        regeln = _stufe(text)
        erg = bereinige(raeume, quelle, stempel, regeln=regeln)
        ringe = [erg[r.id].polygon_mm for r in raeume if r.id in erg]
        idx, doppelt = ueberlappung(ringe)
        if basis_n is None:
            basis_n = len(idx)
        regel_n = Counter()
        zerfall = 0.0
        for b in erg.values():
            for e in b.eintraege:
                regel_n[e.regel] += 1
                if e.regel == "ZERFALL":
                    zerfall += e.flaeche_m2
        zeilen.append({
            "stufe": "{" + ",".join(sorted(str(r) for r in regeln)) + "}",
            "ueberlapper": len(idx),
            "geloest": basis_n - len(idx),
            "doppelt_mm2": doppelt,
            "regeln": dict(sorted(regel_n.items())),
            "entfallen": sum(1 for b in erg.values() if b.entfallen),
            "zerfall_m2": zerfall,
            "_erg": erg,
        })

    voll = zeilen[-1]["_erg"]
    voll_ringe = {r.id: voll[r.id].polygon_mm for r in raeume if r.id in voll}
    # (b) Regel-1-Paare unabhängig nachgerechnet.
    xor_paare = [(a, b) for a, b, _ in _paare(roh_ringe)
                 if (typ.get(a, "") in LIFT_SCHACHT) != (typ.get(b, "") in LIFT_SCHACHT)]
    nur1 = next(z for z in zeilen if z["stufe"] == "{1}")
    # (d) Buchhaltung je Raum.
    bilanz_fehler = []
    for r in raeume:
        b = voll.get(r.id)
        if b is None:
            continue
        roh = Polygon(r.polygon_mm).area / 1e6
        gebucht = sum(e.flaeche_m2 for e in b.eintraege)
        if abs((roh - b.flaeche_m2) - gebucht) > 1e-6:
            bilanz_fehler.append((r.id, roh, b.flaeche_m2, gebucht))
    return {
        "zeilen": zeilen,
        "riegel": (len(riegel_idx), riegel_flaeche / 1e6),
        "stufe0": (zeilen[0]["ueberlapper"], zeilen[0]["doppelt_mm2"] / 1e6),
        "rest_paare": _paare(voll_ringe),
        "offene_ids": sorted(ueberlappung([voll_ringe[i] for i in sorted(voll_ringe)])[0]),
        "xor_paare": xor_paare,
        "regel1_eintraege": nur1["regeln"].get("LIFT_SCHACHT", 0),
        "bilanz_fehler": bilanz_fehler,
        "entfallen_ids": sorted(i for i, b in voll.items() if b.entfallen),
    }


def _tabelle(titel: str, zeilen: list[dict]) -> None:
    print(f"\n{titel}")
    print(f"  {'Stufe':<12}{'Überlapper':>11}{'gelöst':>8}{'doppelt mm²':>14}"
          f"{'entfallen':>10}{'Zerfall m²':>12}  Einträge je Regel")
    for z in zeilen:
        print(f"  {z['stufe']:<12}{z['ueberlapper']:>11}{z['geloest']:>8}"
              f"{z['doppelt_mm2']:>14.2f}{z['entfallen']:>10}{z['zerfall_m2']:>12.3f}"
              f"  {z['regeln'] or '—'}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ergebnis", type=Path, default=REPO / "Projekte" / "_ergebnis")
    ap.add_argument("--plan", action="append", default=None,
                    help="Planname (mehrfach); Default: alle mit raeume.json")
    ap.add_argument("--regeln", nargs="+", default=list(STUFEN),
                    help="Stufen als Ziffernfolgen, '0' = keine Regel")
    args = ap.parse_args()

    plaene = args.plan or sorted(
        p.parent.name for p in args.ergebnis.glob("*/raeume.json"))
    if not plaene:
        print(f"keine raeume.json unter {args.ergebnis}")
        return 1
    stufen = tuple(args.regeln)

    ergebnisse = {}
    for plan in plaene:
        pfad = args.ergebnis / plan / "raeume.json"
        if not pfad.exists():
            print(f"übersprungen (fehlt): {pfad}")
            continue
        ergebnisse[plan] = _messe_plan(pfad, stufen)
        m = ergebnisse[plan]
        _tabelle(f"== {plan} ==", m["zeilen"])
        print(f"  Riegel-Basis (nur raeume[], polygon_mm): "
              f"{m['riegel'][0]} Überlapper / {m['riegel'][1]:.3f} m²")
        print(f"  Stufe {{}} auf der Messbasis:              "
              f"{m['stufe0'][0]} Überlapper / {m['stufe0'][1]:.3f} m²")
        if m["offene_ids"]:
            print(f"  verbleibende Überlapper: {m['offene_ids']}")
        if m["rest_paare"]:
            print("  Rest-Paare > 1 mm²: " + ", ".join(
                f"{a}∩{b} {f:.2f} mm²" for a, b, f in m["rest_paare"]))
        if m["entfallen_ids"]:
            print(f"  entfallen: {m['entfallen_ids']}")

    # Summenzeile über alle Pläne, Stufe für Stufe.
    print("\n== Summe ==")
    summe = []
    for k, text in enumerate(stufen):
        regeln = _stufe(text)
        regel_n: Counter = Counter()
        for m in ergebnisse.values():
            regel_n.update(m["zeilen"][k]["regeln"])
        summe.append({
            "stufe": "{" + ",".join(sorted(str(r) for r in regeln)) + "}",
            "ueberlapper": sum(m["zeilen"][k]["ueberlapper"] for m in ergebnisse.values()),
            "geloest": sum(m["zeilen"][k]["geloest"] for m in ergebnisse.values()),
            "doppelt_mm2": sum(m["zeilen"][k]["doppelt_mm2"] for m in ergebnisse.values()),
            "regeln": dict(sorted(regel_n.items())),
            "entfallen": sum(m["zeilen"][k]["entfallen"] for m in ergebnisse.values()),
            "zerfall_m2": sum(m["zeilen"][k]["zerfall_m2"] for m in ergebnisse.values()),
        })
    _tabelle("kumulativ über alle Pläne", summe)
    print(f"  Riegel-Basis gesamt: "
          f"{sum(m['riegel'][0] for m in ergebnisse.values())} Überlapper / "
          f"{sum(m['riegel'][1] for m in ergebnisse.values()):.3f} m²")

    # Akzeptanzkriterien.
    print("\n== Akzeptanzkriterien ==")
    a_ok = all(m["stufe0"] == m["riegel"] for m in ergebnisse.values())
    print(f"  (a) Stufe {{}} == Riegel-Basis je Plan: {'OK' if a_ok else 'ABWEICHUNG'}")
    for plan, m in ergebnisse.items():
        if m["stufe0"] != m["riegel"]:
            print(f"      {plan}: Stufe {{}} {m['stufe0']} vs Riegel {m['riegel']}")
    b_ok = all(len(m["xor_paare"]) == m["regel1_eintraege"] for m in ergebnisse.values())
    print(f"  (b) Stufe {{1}}-Einträge == LIFT/SCHACHT-Paare: "
          f"{'OK' if b_ok else 'ABWEICHUNG'} "
          f"({sum(m['regel1_eintraege'] for m in ergebnisse.values())} Einträge / "
          f"{sum(len(m['xor_paare']) for m in ergebnisse.values())} Paare)")
    for plan, m in ergebnisse.items():
        if len(m["xor_paare"]) != m["regel1_eintraege"]:
            print(f"      {plan}: {m['regel1_eintraege']} Einträge, "
                  f"Paare {m['xor_paare']}")
    offen = {p: m["rest_paare"] for p, m in ergebnisse.items() if m["rest_paare"]}
    print(f"  (c) kein Paar > 1 mm² nach dem vollen Lauf: "
          f"{'OK' if not offen else 'ABWEICHUNG in ' + ', '.join(offen)}")
    fehler = {p: m["bilanz_fehler"] for p, m in ergebnisse.items() if m["bilanz_fehler"]}
    print(f"  (d) Flächen-Buchhaltung je Raum: "
          f"{'OK' if not fehler else 'ABWEICHUNG'}")
    for plan, liste in fehler.items():
        for rid, roh, ber, gebucht in liste:
            print(f"      {plan} {rid}: roh {roh:.6f} − ber {ber:.6f} "
                  f"!= gebucht {gebucht:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
