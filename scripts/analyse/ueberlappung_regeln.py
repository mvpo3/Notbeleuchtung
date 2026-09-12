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

Stufenbedeutung = angewandte Kaskade aus § 14.6.1 (Owner-Entscheid; die
Nummern haben sich gegenüber dem Lauf `6ebf676` verschoben, die Buchungsnamen
NICHT):
  1 = ``LIFT_SCHACHT``     LIFT/SCHACHT ausstanzen
  2 = ``RESTFLAECHE``      genau eine Seite quelle R → diese Seite verliert
  3 = ``ENTHALTENSEIN``    Ringloch, MIT 10-%-Stempelschutz
  4 = ``QUELLE_RANG`` / ``STEMPEL_NAEHE``
  5 = ``SCHWERPUNKT``
Die Spalte „Warn" zählt die Stempelschutz-Meldungen der Stufe: Paare, die
Regel 3 bewusst NICHT ausgestanzt hat, weil der äußere Raum dadurch um mehr als
10 % von seinem Stempelwert abgewichen wäre.

Läufe vor der ersten Neuerzeugung der Ergebnisse fallen auf die Altfelder
zurück: fehlt ``polygon_roh``, gilt ``polygon_mm`` als Roh-Ring; fehlt
``raum_typ``, gilt das Stempel-Feld ``typ`` als Typ-Quelle (nachweislich
deckungsgleich, aber nicht per Konstruktion — die Stufe ``{1}`` prüft das).

Akzeptanzkriterien (§ 6 der Umsetzungs-Spezifikation):
  (a) Die VOLLE Stufe reproduziert die Riegel-Bänder des Laufs — dazu wird
      die Riegel-Basis (nur ``raeume[]``, ``polygon_mm``) separat gemessen.
      Korrektur 2026-09-12: geprüft wurde bis dahin Stufe ``{}`` gegen die
      Riegel-Basis. Das kann seit der integrierten Bereinigung nicht mehr
      aufgehen, weil ``polygon_mm`` den BEREINIGTEN Stand trägt und Stufe
      ``{}`` die Roh-Ringe misst — die Abweichung war kein Fehler, sondern
      ein veraltetes Kriterium. Eine Abweichung heißt jetzt: die
      eingecheckten Ergebnisse sind älter als der aktuelle Regelstand,
      Prüfstrecke neu laufen lassen.
  (b) Stufe {1} trifft genau die Paare, bei denen ``raum_typ`` EINER Seite
      LIFT/SCHACHT ist (gegengerechnet über die Roh-Paare).
  (c) Stufe {1,2,3,4,5} lässt kein Paar > 1 mm² übrig — AUSSER den Paaren, die
      der Stempelschutz der Regel 3 bewusst offen lässt (Owner-Entscheid). Die
      werden getrennt und namentlich ausgewiesen, nicht stillschweigend
      verrechnet.
  (d) Für jeden Raum gilt die Flächen-Buchhaltung.
  (e) Nach dem vollen Lauf ragt kein R-Polygon über ein Nicht-R-Polygon. Das ist
      die Nachfolge-Prüfung für den entfallenen Regel-5-Schlusspass — geleistet
      jetzt von Regel 2 als Paar-Regel.
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


def _schutz_paare(warnungen: list[str]) -> set[frozenset[str]]:
    """Paare, die der Stempelschutz offen gelassen hat — aus den Warnzeilen.

    Format von ``bereinigung._schutz_warnung``: „<aussen> nicht ausgestanzt
    (enthaelt <innen>): ...". Ändert sich das Format, findet diese Funktion
    nichts und Kriterium (c) meldet die Paare als ABWEICHUNG — fail-loud, nicht
    stillschweigend „OK".
    """
    marke = " nicht ausgestanzt (enthaelt "
    out: set[frozenset[str]] = set()
    for w in warnungen:
        if marke not in w:
            continue
        aussen, rest = w.split(marke, 1)
        out.add(frozenset((aussen, rest.split(")", 1)[0])))
    return out


def _messe_plan(pfad: Path, stufen: tuple[str, ...]) -> dict:
    raeume, quelle, stempel, riegel_ringe = _laden(pfad)
    roh_ringe = {r.id: list(r.polygon_mm) for r in raeume}
    typ = {r.id: (r.raum_typ or "").strip().upper() for r in raeume}

    riegel_idx, riegel_flaeche = ueberlappung(riegel_ringe)
    basis_n = None
    zeilen = []
    for text in stufen:
        regeln = _stufe(text)
        warn: list[str] = []
        erg = bereinige(raeume, quelle, stempel, regeln=regeln, warnungen=warn)
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
            "warn_n": len(warn),
            "_erg": erg,
            "_warn": warn,
        })

    voll = zeilen[-1]["_erg"]
    voll_warn = zeilen[-1]["_warn"]
    voll_ringe = {r.id: voll[r.id].polygon_mm for r in raeume if r.id in voll}
    rest_paare = _paare(voll_ringe)
    schutz = _schutz_paare(voll_warn)
    # (c) alles, was der Stempelschutz NICHT erklärt.
    offen_ohne_schutz = [(a, b, f) for a, b, f in rest_paare
                         if frozenset((a, b)) not in schutz]
    # (e) R gegen Nicht-R nach dem vollen Lauf — Nachfolge des Schlusspasses.
    ist_r = {i: (quelle.get(i) or "").strip().upper() == "R" for i in voll_ringe}
    r_ueber = [(a, b, f) for a, b, f in rest_paare
               if ist_r.get(a, False) != ist_r.get(b, False)]
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
        "rest_paare": rest_paare,
        "warnungen": voll_warn,
        "schutz_paare": schutz,
        "offen_ohne_schutz": offen_ohne_schutz,
        "r_ueber": r_ueber,
        "offene_ids": sorted(ueberlappung([voll_ringe[i] for i in sorted(voll_ringe)])[0]),
        "xor_paare": xor_paare,
        "regel1_eintraege": nur1["regeln"].get("LIFT_SCHACHT", 0),
        "bilanz_fehler": bilanz_fehler,
        "entfallen_ids": sorted(i for i, b in voll.items() if b.entfallen),
    }


def _tabelle(titel: str, zeilen: list[dict]) -> None:
    print(f"\n{titel}")
    print(f"  {'Stufe':<12}{'Überlapper':>11}{'gelöst':>8}{'doppelt mm²':>14}"
          f"{'entfallen':>10}{'Zerfall m²':>12}{'Warn':>6}  Einträge je Regel")
    for z in zeilen:
        print(f"  {z['stufe']:<12}{z['ueberlapper']:>11}{z['geloest']:>8}"
              f"{z['doppelt_mm2']:>14.2f}{z['entfallen']:>10}{z['zerfall_m2']:>12.3f}"
              f"{z['warn_n']:>6}  {z['regeln'] or '—'}")


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
        if m["warnungen"]:
            print(f"  Stempelschutz ({len(m['warnungen'])}) — nicht ausgestanzt:")
            for w in m["warnungen"]:
                print(f"    - {w}")
        if m["r_ueber"]:
            print("  R über Nicht-R: " + ", ".join(
                f"{a}∩{b} {f:.2f} mm²" for a, b, f in m["r_ueber"]))
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
            "warn_n": sum(m["zeilen"][k]["warn_n"] for m in ergebnisse.values()),
        })
    _tabelle("kumulativ über alle Pläne", summe)
    print(f"  Riegel-Basis gesamt: "
          f"{sum(m['riegel'][0] for m in ergebnisse.values())} Überlapper / "
          f"{sum(m['riegel'][1] for m in ergebnisse.values()):.3f} m²")

    # Akzeptanzkriterien.
    print("\n== Akzeptanzkriterien ==")
    # Geprüft wird die VOLLE Stufe, nicht Stufe {} — siehe Modul-Docstring (a).
    # Toleranz, weil die Ringe beim Schreiben der raeume.json gerundet werden.
    tol_m2 = 1e-4

    def _voll(m: dict) -> tuple[int, float]:
        zeile = m["zeilen"][-1]              # letzte angeforderte Stufe
        return (zeile["ueberlapper"], zeile["doppelt_mm2"] / 1e6)

    def _deckt(a: tuple[int, float], b: tuple[int, float]) -> bool:
        return a[0] == b[0] and abs(a[1] - b[1]) <= tol_m2

    a_ok = all(_deckt(_voll(m), m["riegel"]) for m in ergebnisse.values())
    print(f"  (a) volle Stufe == Riegel-Basis je Plan (+-{tol_m2} m²): "
          f"{'OK' if a_ok else 'ABWEICHUNG'}")
    for plan, m in ergebnisse.items():
        if not _deckt(_voll(m), m["riegel"]):
            print(f"      {plan}: volle Stufe {_voll(m)} vs Riegel "
                  f"{m['riegel']} — eingecheckte Ergebnisse älter als der "
                  f"Regelstand?")
    b_ok = all(len(m["xor_paare"]) == m["regel1_eintraege"] for m in ergebnisse.values())
    print(f"  (b) Stufe {{1}}-Einträge == LIFT/SCHACHT-Paare: "
          f"{'OK' if b_ok else 'ABWEICHUNG'} "
          f"({sum(m['regel1_eintraege'] for m in ergebnisse.values())} Einträge / "
          f"{sum(len(m['xor_paare']) for m in ergebnisse.values())} Paare)")
    for plan, m in ergebnisse.items():
        if len(m["xor_paare"]) != m["regel1_eintraege"]:
            print(f"      {plan}: {m['regel1_eintraege']} Einträge, "
                  f"Paare {m['xor_paare']}")
    offen = {p: m["offen_ohne_schutz"] for p, m in ergebnisse.items()
             if m["offen_ohne_schutz"]}
    schutz_n = sum(len(m["warnungen"]) for m in ergebnisse.values())
    print(f"  (c) kein Paar > 1 mm² ausser Stempelschutz: "
          f"{'OK' if not offen else 'ABWEICHUNG in ' + ', '.join(offen)} "
          f"({schutz_n} Stempelschutz-Meldungen, Paare bewusst offen)")
    for plan, m in ergebnisse.items():
        for a, b, f in m["rest_paare"]:
            if frozenset((a, b)) in m["schutz_paare"]:
                print(f"      {plan} {a}∩{b} {f:.2f} mm² — Stempelschutz, gewollt")
    for plan, paare in offen.items():
        for a, b, f in paare:
            print(f"      {plan} {a}∩{b} {f:.2f} mm² — OHNE Stempelschutz")
    fehler = {p: m["bilanz_fehler"] for p, m in ergebnisse.items() if m["bilanz_fehler"]}
    print(f"  (d) Flächen-Buchhaltung je Raum: "
          f"{'OK' if not fehler else 'ABWEICHUNG'}")
    for plan, liste in fehler.items():
        for rid, roh, ber, gebucht in liste:
            print(f"      {plan} {rid}: roh {roh:.6f} − ber {ber:.6f} "
                  f"!= gebucht {gebucht:.6f}")
    r_fehler = {p: m["r_ueber"] for p, m in ergebnisse.items() if m["r_ueber"]}
    print(f"  (e) kein R-Polygon über einem Nicht-R-Polygon: "
          f"{'OK' if not r_fehler else 'ABWEICHUNG'}")
    for plan, paare in r_fehler.items():
        for a, b, f in paare:
            print(f"      {plan} {a}∩{b} {f:.2f} mm²")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
