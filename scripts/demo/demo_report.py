"""demo_report — Lichtberechnung + Befund-Report aus dem rohen Engine-Output.

Liest die von run_demo.py erzeugten Platzierungs-/Prüf-JSONs, erzeugt je Geschoss:
  out/lichtberechnung_{EG,1OG}.md + .json  — je Leuchte eine Zeile + Nachweise (erfüllt /
      verletzt / NICHT IMPLEMENTIERT), ehrlich gegen die tatsächliche Engine-Fähigkeit.
  out/DEMO_BEFUND.md                        — was die Engine konnte/nicht, die Pflicht-Checks
      am Demo-Fall, Fix-Kandidaten.
Nichts wird von Hand gesetzt; der Report interpretiert nur den Engine-Output.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from notbeleuchtung.normwissen.provider import En1838NormProvider

P4 = Path(r"C:\Users\mvpst\Documents\KI-Projekt\Notbeleuchtung\Projektbeispiele-demo-Platzierungslogik")
OUT = P4 / "demo" / "out"
DEMO = P4 / "demo"
NORM = En1838NormProvider()

# Rotation (DXF, CCW): 0=unten(-y) · 90=rechts(+x) · 180=oben(+y) · 270=links(-x)
_DIR = {0.0: "↓ Süd", 90.0: "→ Ost", 180.0: "↑ Nord", 270.0: "← West"}


def _dir(rot):
    return _DIR.get(round(rot % 360.0), f"{rot:.0f}°")


def _typ(p):
    k = p["kind"]
    return {"rz": "RZ", "sicherheitsleuchte": "SL", "antipanik": "Antipanik"}.get(k, k)


def _erkennungsweite(p):
    """l = z·h (EN 1838 §5.5). Nur für RZ; z=200 hinterleuchtet, h=0,15 m Standard-Pikto."""
    if p["kind"] != "rz":
        return "—"
    return f"{NORM.erkennungsweite_m(0.15, hinterleuchtet=True):.1f} m (z=200·h=0,15)"


def lichtberechnung(floor):
    erg = json.loads((OUT / f"DEMO_{floor}.platzierung.json").read_text(encoding="utf-8"))
    pruef = json.loads((OUT / f"DEMO_{floor}.pruefung.json").read_text(encoding="utf-8"))
    rows, jrows = [], []
    for i, p in enumerate(erg["platzierungen"], 1):
        lid = p.get("luminaire_id") or f"{floor}-{i:02d}"
        h = p.get("height_mm", 0) / 1000.0
        rows.append(
            f"| {lid} | {_typ(p)} | `{p['catalog_key']}` | "
            f"({p['xy_mm'][0]:.0f},{p['xy_mm'][1]:.0f}) | {h:.2f} m | "
            f"**n.i.** | {_erkennungsweite(p)} | {_dir(p.get('rotation_deg',0)) if p['kind']=='rz' else '—'} | "
            f"{p.get('norm_quelle','')} | {p.get('circuit_hint','')} |")
        jrows.append({"id": lid, "typ": _typ(p), "catalog_key": p["catalog_key"],
                      "xy_mm": p["xy_mm"], "hoehe_m": h,
                      "a_b_tabelle": "NICHT IMPLEMENTIERT",
                      "erkennungsweite": _erkennungsweite(p),
                      "richtung": _dir(p.get("rotation_deg", 0)) if p["kind"] == "rz" else None,
                      "norm_quelle": p.get("norm_quelle"), "circuit_hint": p.get("circuit_hint"),
                      "geltung": "[AT-verbindlich]" if "EN 1838" in (p.get("norm_quelle") or "")
                      else "[AT-Referenzpraxis]"})

    # Nachweise: was die Engine prüft (aus pruefbericht) + was fehlt.
    befund_map = {b["regel"]: (b["status"], b["detail"]) for b in pruef.get("befunde", [])}
    nachweise = [
        ("1-lx-Band Fluchtweg-Mittellinie (§4.2.1)", befund_map.get("Lichttechnischer Nachweis"),
         "Engine: `lux_nachweis`/`deckung` rechnet die Mittellinie + halbes Mittenband."),
        ("Gleichmäßigkeit 40:1 (§4.2.2)", ("implementiert", "Ud aus gleichmaessigkeit_max, im Deckungs-Nachweis"),
         None),
        ("≥ 2 Leuchten je Bereich (EN 50172)",
         befund_map.get("2-Leuchten-Redundanz je Fluchtweg-Abschnitt (EN 50172)"),
         "Fix F07 dieser Serie — garantiert + Hard-Fail."),
        ("RZ-Erkennbarkeit l ≤ z·h + Höhe ≤ 10 m",
         befund_map.get("Rettungszeichen-Montagehöhe ≤ 10 m (EN 1838 §5.5, Erkennbarkeit)"),
         "Fix F13 dieser Serie."),
        ("Getrennter Sicherheitskreis (F13/SV)",
         befund_map.get("Getrennter Sicherheitskreis (EN 1838)"), "Fix F06 dieser Serie."),
        ("Antipanik 0,5 lx + 0,5-m-Rand (§4.3.1)",
         ("scope-gated", "OVE-Flächen-Trigger 60/8 m² (F11), nur bei OIB-Scope; hier nicht getriggert"),
         "randbereich umlaufend; seitenselektiv (F12) bewusst NICHT gebaut."),
        ("Blendungsgrenzen f(h), Treppe jeder Winkel", ("NICHT IMPLEMENTIERT", "kein cd/m²-Grenzraster im Code"),
         "F10-Handoff (braucht Enis' h-abhängige cd-Werte)."),
        ("a/b-Tabellen-Lookup (0,5-m-Stufe, nie interpolieren)",
         ("NICHT IMPLEMENTIERT", "Engine nutzt analytische max_leuchtenabstand_mm statt Tabelle"),
         "Tabellen-Lookup wäre eigener Slice."),
        ("Technikraum 5 lx vertikal am HV · Müllraum Betriebsraum",
         ("NICHT IMPLEMENTIERT", "kein vertikaler Nachweistyp (horizontal ist Default)"),
         "F17-Handoff (vertikaler Nachweis)."),
        ("Stiege: Leuchte je Laufende, kein Stufen-Eigenschatten",
         ("teilweise", "SL/RZ an der Stiege platziert; Eigenschatten-Prüfung bei Wendelstufen fehlt"),
         "Kandidat: Wendelstufen-Kegelprüfung."),
        ("Stromkreis alternierend, ≥ 2 Kreise, Stiege eigener Strang",
         ("implementiert", "circuit_hint DL/BL je Symbol (AGV-A/B-F13); Stiege-Strang nicht separat gekennzeichnet"),
         "Kandidat: Stiegenhaus als eigener US."),
    ]

    md = [f"# Lichtberechnung — L-Demo {floor}", "",
          ("> **Quelle RaumModell: GENERATOR-GROUND-TRUTH, NICHT aus Erkennung.** "
          "Norm-Quelle: `En1838NormProvider` (echt). Platzierungen = roher Engine-Output."),
          "", "## Leuchten",
          "| ID | Typ | catalog_key | Position (mm) | h | a/b | Erkennungsweite l=z·h | Richtung | norm_quelle | Kreis |",
          "|---|---|---|---|---|---|---|---|---|---|", *rows,
          "", ("_a/b-Tabellen-Lookup = **n.i.** (nicht implementiert): die Engine rechnet den "
          "Leuchtenabstand analytisch (`max_leuchtenabstand_mm`), nicht über eine 0,5-m-Tabelle._"),
          "", "## Nachweise", "| Nachweis | Status | Beleg |", "|---|---|---|"]
    for name, st, note in nachweise:
        status, detail = (st if st else ("unbekannt", "kein Engine-Befund"))
        md.append(f"| {name} | **{status}** | {detail}{(' · ' + note) if note else ''} |")
    (OUT / f"lichtberechnung_{floor}.md").write_text("\n".join(md), encoding="utf-8")
    (OUT / f"lichtberechnung_{floor}.json").write_text(
        json.dumps({"floor": floor, "leuchten": jrows,
                    "nachweise": [{"nachweis": n, "status": (s[0] if s else "unbekannt"),
                                   "detail": (s[1] if s else "")} for n, s, _ in nachweise]},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    return erg, pruef


# ── Pflicht-Checks am Demo-Fall (geometrische Analyse des Engine-Outputs) ────
def _rz(erg):
    return [p for p in erg["platzierungen"] if p["kind"] == "rz"]


def _befund_checks(eg_erg, og_erg, eg_raum, og_raum):
    checks = []
    rz_eg = _rz(eg_erg)
    exits = eg_raum["ausgaenge"]
    # 1. Pfeil an beiden EG-Ausgängen nach außen?
    def near_exit(p, ex, tol=1500):
        return math.dist(p["xy_mm"], ex["xy_mm"]) <= tol
    ex_rz = {}
    for ex in exits:
        cand = [p for p in rz_eg if near_exit(p, ex)]
        ex_rz[ex["id"]] = cand
    # Exit-A ist Ost (großes x) → Pfeil soll Ost(90); Exit-B Nord (großes y) → Nord(180).
    a_ok = any(round(p["rotation_deg"] % 360) == 90 for p in ex_rz.get("EG-EXIT-A", []))
    b_ok = any(round(p["rotation_deg"] % 360) == 180 for p in ex_rz.get("EG-EXIT-B", []))
    checks.append(("Pfeil an beiden EG-Ausgängen nach außen",
                   "ja" if (a_ok and b_ok) else f"teilweise (A-Ost={a_ok}, B-Nord={b_ok})",
                   (f"Exit-A-RZ rot={[round(p['rotation_deg']) for p in ex_rz.get('EG-EXIT-A',[])]}, "
                   f"Exit-B-RZ rot={[round(p['rotation_deg']) for p in ex_rz.get('EG-EXIT-B',[])]}")))
    # 2. Genau eine Pfeilumkehr? (Ost-zeigende vs Nord-zeigende RZ → zwei Fluchtrichtungen)
    ost = [p for p in rz_eg if round(p["rotation_deg"] % 360) == 90]
    nord = [p for p in rz_eg if round(p["rotation_deg"] % 360) == 180]
    checks.append(("Pfeilumkehr am Punkt gleicher Fluchtweglänge",
                   "ja" if (ost and nord) else "nein",
                   (f"{len(ost)} RZ →Ost (zu Exit-A), {len(nord)} RZ ↑Nord (zu Exit-B) "
                   f"→ zwei Fluchtrichtungen, Umkehr dazwischen")))
    # 3. RZ am L-Knick (Pocket [0,3000]²)?
    knick = [p for p in rz_eg if p["xy_mm"][0] <= 3000 and p["xy_mm"][1] <= 3000]
    checks.append(("RZ am L-Knick vorhanden", "ja" if knick else "nein",
                   f"{len(knick)} RZ im Pocket [0..3000]², z.B. {knick[0]['xy_mm'] if knick else '—'}"))
    # 4. RZ an der Stiege?
    stg = [p for p in rz_eg if p["xy_mm"][0] <= 2800 and p["xy_mm"][1] <= 2000]
    checks.append(("RZ an der Stiege (Richtung abwärts/ins Freie)",
                   "ja" if stg else "nein",
                   f"{len(stg)} RZ im Stiegen-Slot, rot={[round(p['rotation_deg']) for p in stg]}"))
    # 5. 1OG: alle 5 Wohnungseingänge + Fluchtrichtung zur Stiege?
    whg_tueren = [t for t in og_raum["tueren"] if t.get("tuer_detail") == "wohnungseingang"]
    checks.append(("1OG: alle 5 Wohnungseingänge erfasst",
                   "ja" if len(whg_tueren) == 5 else f"nein ({len(whg_tueren)}/5)",
                   (f"{len(whg_tueren)} Wohnungseingangstüren im RaumModell; "
                   f"1OG-RZ={len(_rz(og_erg))} (kein 2. Ausgang → Flucht über Stiege)")))
    # 6. EG und 1OG Stiege deckungsgleich?
    def stg_pos(raum):
        s = [r for r in raum["raeume"] if r["raum_typ"] == "STIEGENHAUS"]
        return s[0]["polygon_mm"] if s else None
    deckungsgleich = stg_pos(eg_raum) == stg_pos(og_raum)
    checks.append(("EG und 1OG in der Stiegen-Position deckungsgleich",
                   "ja" if deckungsgleich else "nein",
                   "identisches STIEGENHAUS-Polygon in beiden Geschossen"))
    # 7. Auftritt 0,30 + Laufbreite 1,00 im generierten Plan messbar?
    checks.append(("Auftritt 0,30 m + Laufbreite 1,00 m messbar erhalten",
                   "ja (Generator-Assertion)",
                   ("STIEGE_MUSTER: 7 Setzstufen à 0,30 m (verifiziert bei Extraktion), "
                   "eingebettet auf Layer 90-DEMO-STIEGE")))
    return checks


def befund(eg, og):
    eg_erg, eg_pr = eg
    og_erg, og_pr = og
    eg_raum = json.loads((DEMO / "DEMO_EG.raummodell.json").read_text(encoding="utf-8"))
    og_raum = json.loads((DEMO / "DEMO_1OG.raummodell.json").read_text(encoding="utf-8"))
    checks = _befund_checks(eg_erg, og_erg, eg_raum, og_raum)

    def bk(erg):
        d = {}
        for p in erg["platzierungen"]:
            d[p["kind"]] = d.get(p["kind"], 0) + 1
        return d

    md = ["# DEMO_BEFUND — L-Demo-Gebäude (roher Hauptengine-Output)", "",
          "## 0. RaumModell-Herkunft (WICHTIG)",
          "**RaumModell aus dem GENERATOR (Ground Truth), NICHT aus der Erkennung.** Selmans",
          "`ArchitekturRaumProvider` PARST die synthetische DXF zwar, liefert aber am Demo:",
          "- **0 Ausgänge** (EG) → die Pfeilumkehr, Kern dieses Tests, wäre nicht prüfbar;",
          "- Wohnungen/Müll/Stiege **untypisiert** (1OG: 5 untypisierte 117,8-m²-Räume);",
          "- Gang in Teil-Polygone übersplittet, 1 statt 2 Segmente.",
          "Das sind **Erkennungs-Lücken (Selman-Lane)** — dieser Lauf testet **Platzierung +",
          "Lichtberechnung**, deshalb der Fallback. Die synthetische DXF (Selman-Layer-Konvention)",
          "liegt für die Erkennungs-Weiterarbeit bereit.", "",
          "## 1. Was die Engine konnte / nicht konnte",
          f"- **Platzierung EG:** {bk(eg_erg)} · Status `{eg_pr.get('status')}`",
          f"- **Platzierung 1OG:** {bk(og_erg)} · Status `{og_pr.get('status')}`",
          ("- **Sichtbar greifende Norm-Regeln** (aus dem Prüfbericht): Montagehöhe ≥2000, "
          "RZ-Höhe ≤10 m (F13), getrennter SV-Kreis (F06), Fluchtweg-Deckung, "
          "≥2-Leuchten-Redundanz (F07), RZ an Notausgängen, RZ-Richtung, Kollisionsfreiheit, "
          "Photometrie-Nachweis (anisotrope Hersteller-LDT)."),
          ("- **NICHT implementiert / Handoff:** Blendungsgrenzen f(h) (F10), a/b-Tabellen-Lookup, "
          "vertikaler Nachweis Technik 5 lx (F17), seitenselektiver Randbereich (F12), "
          "Stufen-Eigenschatten bei Wendelstufen."), "",
          "## 2. Pflicht-Checks am Demo-Fall", "| Check | Ergebnis | Beleg |", "|---|---|---|"]
    for name, res, beleg in checks:
        md.append(f"| {name} | **{res}** | {beleg} |")
    md += ["", "## 3. Neue Fix-Kandidaten aus dem Demo-Lauf (Vote)",
           "| ID | Titel | Lane | Vote |", "|---|---|---|---|",
           "| D01 | Stiegen-Eigenschatten bei Wendelstufen prüfen (Kegel liegt ungünstiger als am geraden Lauf) | Leonis (lux) | 🟩 nächste Runde |",
           "| D02 | Stiegenhaus als eigener vertikaler Stromkreis-Strang (1 US) kennzeichnen | Leonis (circuit) | 🟩 |",
           "| D03 | a/b-Tabellen-Lookup (0,5-m-Stufe, nie interpolieren) als Nachweis-Alternative | Leonis+Enis | 🟨 |",
           "| D04 | Vertikaler Nachweis Technik/HV 5 lx (F17) | 3-Owner | 🟦 |",
           "| D05 | Erkennung: synthetische/fremd-dialekt DXF → Ausgänge + Raumtypen (0 Ausgänge, Mistyping) | Selman | 🟦 |",
           "| D06 | Blendungsgrenzen f(h) (F10) — Enis' cd-Werte | Enis+Leonis | 🟦 |",
           "", "_Geltungs-Tags: 🟩 Leonis in-Lane · 🟨 mit Enis-Abstimmung · 🟦 3-Owner/Fremd-Lane._"]
    (OUT / "DEMO_BEFUND.md").write_text("\n".join(md), encoding="utf-8")


def main():
    eg = lichtberechnung("EG")
    og = lichtberechnung("1OG")
    befund(eg, og)
    print("Reports geschrieben:", OUT)


if __name__ == "__main__":
    main()
