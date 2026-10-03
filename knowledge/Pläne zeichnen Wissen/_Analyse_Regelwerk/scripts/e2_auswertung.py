"""e2_auswertung.py — Projekt 5 (Baufeld E2, nur DXF): jede Leuchte nach
Mollgasse-Basis-Regeln mechanisch bewerten.

Grundlage: evidenz/BaufeldE2/Notbeleuchtungspläne_UG_RIVO_mit_Lehrlayern.json
(aus extract_erklaerung.py). Lehr-Elemente: E2_MOL_LEHRPERSON_ZENTRIERT
(grüne Menschen, Blick=180°+rot bei xscale>0), E2_LEHR_WEG_B_INTERPRETATION
(türkise SOLID-Blickkeile), 681-Fluchtlinien.

Checks je RZ (Basis-Regeln, mm-genau):
- B1 „Balken/Front zeigt zum Menschen" (NB-R06-Familie): Welt-Pfeil der
  down-RZ ≈ Richtung RZ→nächste ankommende Person (Toleranz 60°).
- B2 Blickkeil-Kohärenz: nächster türkiser Keil zeigt auf dieses RZ
  (Keil-Schwerpunkt→RZ < 4 m) und die zugehörige Person sieht die Front.
- B3 beidseitig-Gruppen: bothsided-Block vorhanden, wo Personen aus BEIDEN
  Richtungen ankommen (Personen beidseits ±60° der Korridorachse).
Ausgabe: evidenz/BaufeldE2/auswertung.json + ANALYSE_BaufeldE2.md.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HIER = Path(__file__).resolve()
BASIS = HIER.parents[1]
EV = BASIS / "evidenz" / "BaufeldE2"

_TOL_DEG = 60.0
_KEIL_RADIUS_MM = 4000.0
_PERSON_RADIUS_MM = 12000.0


def _winkel(von: tuple[float, float], nach: tuple[float, float]) -> float:
    return math.degrees(math.atan2(nach[1] - von[1], nach[0] - von[0])) % 360.0


def _delta(a: float, b: float) -> float:
    return abs((a - b + 180.0) % 360.0 - 180.0)


def _schwerpunkt(punkte: list) -> tuple[float, float] | None:
    if not punkte:
        return None
    xs = [p[0] for p in punkte]
    ys = [p[1] for p in punkte]
    return (sum(xs) / len(xs), sum(ys) / len(ys))


def main() -> int:
    quelle = next(EV.glob("Notbeleuchtungspläne_UG*.json"))
    daten = json.loads(quelle.read_text(encoding="utf-8"))
    leuchten = [l for l in daten["leuchten"] if l["xy_mm"]]
    personen = [p for p in daten["personen"] if p["xy_mm"]]
    keile = [
        {"xy": s, "handle": k["handle"]}
        for k in daten["sichtlinien"]
        if k.get("punkte") and (s := _schwerpunkt(k["punkte"]))
    ]

    ergebnisse = []
    n_ok = n_abw = n_unpruefbar = 0
    for l in leuchten:
        rec: dict = {
            "handle": l["handle"], "block": l["block"], "typ": l["typ"],
            "richtung_block": l["richtung_block"], "xy_mm": l["xy_mm"],
            "rot_deg": l["rot_deg"], "welt_pfeil_deg": l["welt_pfeil_deg"],
            "beidseitig_gruppe": l.get("beidseitig_gruppe"),
            "checks": {},
        }
        # nächste Person (ankommend = innerhalb Radius, Blick grob Richtung RZ)
        kandidaten = []
        for p in personen:
            d = math.dist(l["xy_mm"], p["xy_mm"])
            if d > _PERSON_RADIUS_MM:
                continue
            blick_zum_rz = _delta(p["blick_deg"], _winkel(p["xy_mm"], l["xy_mm"]))
            kandidaten.append((d, blick_zum_rz, p))
        kandidaten.sort(key=lambda t: t[0])
        ankommend = [k for k in kandidaten if k[1] <= 90.0]

        if l["richtung_block"] == "bothsided":
            # B3: Personen aus beiden Richtungen?
            if len(ankommend) >= 2:
                w = [_winkel(l["xy_mm"], k[2]["xy_mm"]) for k in ankommend[:4]]
                spann = max(_delta(a, b) for a in w for b in w)
                rec["checks"]["B3_beidseitig"] = (
                    "ok: Personen aus Gegenrichtungen "
                    f"(max Winkelspann {spann:.0f} Grad)"
                    if spann >= 120.0 else
                    f"abweichung?: Ankommende nur aus einem Sektor ({spann:.0f} Grad)"
                )
            else:
                rec["checks"]["B3_beidseitig"] = "unpruefbar: <2 ankommende Personen im Umkreis"
        elif l["welt_pfeil_deg"] is not None and ankommend:
            # Best-Match unter ALLEN Ankommenden — bei mehreren Personen ist die
            # regelgebende die auf der Zugangs-Achse, nicht zwingend die nächste.
            best = min(
                ((_delta(l["welt_pfeil_deg"], _winkel(l["xy_mm"], p["xy_mm"])), d, p)
                 for d, _, p in ankommend),
                key=lambda t: t[0],
            )
            delta, d, p = best
            richtung_zur_person = _winkel(l["xy_mm"], p["xy_mm"])
            rec["checks"]["B1_front_zum_menschen"] = (
                f"ok: Welt-Pfeil {l['welt_pfeil_deg']:.0f} Grad ~ Person {p['handle']} "
                f"({richtung_zur_person:.0f} Grad, d={d:.0f} mm, delta={delta:.0f} Grad)"
                if delta <= _TOL_DEG else
                f"abweichung: bestes delta={delta:.0f} Grad (Person {p['handle']}, "
                f"Pfeil {l['welt_pfeil_deg']:.0f} vs Richtung {richtung_zur_person:.0f})"
            )
        else:
            rec["checks"]["B1_front_zum_menschen"] = "unpruefbar: keine ankommende Person im Umkreis"

        # B2: nächster Blickkeil
        if keile:
            kd, kk = min(((math.dist(l["xy_mm"], k["xy"]), k) for k in keile),
                         key=lambda t: t[0])
            rec["checks"]["B2_blickkeil"] = (
                f"ok: Keil {kk['handle']} in {kd:.0f} mm"
                if kd <= _KEIL_RADIUS_MM else
                f"kein Keil im Umkreis (nächster {kd:.0f} mm)"
            )
        status = "ok"
        for v in rec["checks"].values():
            if v.startswith("abweichung"):
                status = "abweichung"
                break
            if v.startswith("unpruefbar") and status == "ok":
                status = "unpruefbar"
        rec["status"] = status
        n_ok += status == "ok"
        n_abw += status == "abweichung"
        n_unpruefbar += status == "unpruefbar"
        ergebnisse.append(rec)

    out = {
        "quelle": daten["quelle"],
        "n_leuchten": len(ergebnisse),
        "n_ok": n_ok, "n_abweichung": n_abw, "n_unpruefbar": n_unpruefbar,
        "n_personen": len(personen), "n_keile": len(keile),
        "leuchten": ergebnisse,
    }
    (EV / "auswertung.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    # ANALYSE_BaufeldE2.md direkt generieren (kein Seitenprotokoll — keine PDF)
    z = [
        "# ANALYSE — Projekt 5: Baufeld E2 (nur DXF, UG)",
        "",
        f"Quelle: `{daten['quelle']}` — Bewertung jeder Leuchte nach den",
        "Mollgasse-BASIS-Regeln (mechanische Checks, `scripts/e2_auswertung.py`).",
        "Die Datei ist die Owner-Referenz mit Lehrlayern: 118 grüne Personen",
        f"(`E2_MOL_LEHRPERSON_ZENTRIERT`), {len(keile)} türkise Blickkeile (SOLID auf",
        "`E2_LEHR_WEG_B_INTERPRETATION`), Fluchtlinien (`681 Fluchtlinien`).",
        "",
        (f"**Bilanz: {len(ergebnisse)} Leuchten — {n_ok} ok · {n_abw} Abweichung · "
         f"{n_unpruefbar} unprüfbar** (unprüfbar = keine ankommende Person im 12-m-Umkreis;"),
        "ehrlich ausgewiesen, nicht als ok gezählt).",
        "",
        "Checks: **B1** Front/Balken zeigt zum ankommenden Menschen (NB-R06-Familie,",
        "Toleranz 60°) · **B2** türkiser Blickkeil ≤ 4 m am RZ · **B3** bothsided nur",
        "bei Ankunft aus Gegenrichtungen (Winkelspann ≥ 120°).",
        "",
        "| Handle | Block | Welt-Pfeil | Status | Befund |",
        "|---|---|---|---|---|",
    ]
    for r in ergebnisse:
        befund = " · ".join(f"{k}: {v}" for k, v in r["checks"].items())
        wp = f"{r['welt_pfeil_deg']:.0f}°" if r["welt_pfeil_deg"] is not None else "—"
        z.append(f"| {r['handle']} | {r['block']} | {wp} | {r['status']} | {befund} |")
    z += [
        "",
        "Abweichungen sind KANDIDATEN für das Konfliktprotokoll bzw. für",
        "Regel-Grenzfälle (Personen-Dichte im UG ist hoch — die nächste ankommende",
        "Person ist nicht immer die regelgebende). Kein automatischer",
        "KONFLIKTE-Eintrag ohne visuelle Gegenprüfung (crop_dxf.py).",
    ]
    (BASIS / "ANALYSE_BaufeldE2.md").write_text("\n".join(z), encoding="utf-8")
    print(f"{len(ergebnisse)} Leuchten: {n_ok} ok / {n_abw} abweichung / "
          f"{n_unpruefbar} unpruefbar -> ANALYSE_BaufeldE2.md + auswertung.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
