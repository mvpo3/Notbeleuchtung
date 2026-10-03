"""review_visuell — visuelle Regel-Review eines Engine-Outputs, Bild je Geschoss.

Rendert das erkannte Raumschema (Erkennungs-Output) + die platzierten Symbole +
markierte Befunde, damit SICHTBAR wird, WO der Plan nicht passt:

- ROT  = harter Verstoß (Ausgang ohne RZ §4.1.2 g, Leuchte in Privatraum,
         Fluchtweg-Segment ohne RZ, RZ ohne Pfeilrichtung, Kollision).
- ORANGE = Unterdeckung (Allgemein-/Fluchtweg-Bereich ohne Notlicht & ohne
         Zirkulation) — fängt den Fall, den die Validierung mangels erkannter
         Segmente NICHT als Fehler sieht („ungeprüft ≠ erfüllt").

Das ist ein Diagnose-/Loop-Werkzeug (kein Plan-Output). Der GT-Vergleich gegen
fertige Experten-Pläne bleibt `mollgasse_gt_vergleich.py` (nur Mollgasse hat Soll).

Aufruf:  python scripts/analyse/review_visuell.py <floor> <dxf> <out.png>
"""
from __future__ import annotations

import math
import sys
from collections import Counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPoly
from shapely.geometry import Point, Polygon

from notbeleuchtung.hauptengine.photometrie_befund import photometrie_des_bundles
from notbeleuchtung.hauptengine.registry import build_default_bundle
from notbeleuchtung.hauptengine.validierung import pruefbericht

_AUSGANG_RZ_RADIUS_MM = 2000.0
_KOLLISION_MM = 250.0
_UNTERDECKT_MIN_M2 = 5.0                       # kleinere Allgemeinräume nicht flaggen
KIND_COLOR = {"rz": "#1EB350", "sicherheitsleuchte": "#1f77b4", "antipanik": "#ff7f0e"}
_KORRIDOR_TYPEN = {"GANG", "FLUR", "STIEGENHAUS", "VORRAUM", "KORRIDOR"}


def _dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _poly(r):
    return Polygon(r.polygon_mm).buffer(0) if len(r.polygon_mm) >= 3 else None


def _ist_privat(r):
    return (r.nutzungsklasse == "WOHNUNG_PRIVAT"
            and not r.ist_fluchtweg and not r.ist_communal)


def _befunde_lokal(raum, plz):
    """Konkrete Befunde mit (x, y, label, 'hart'|'weich')."""
    rz = [p for p in plz.platzierungen if p.kind == "rz"]
    privat = [(r.id, _poly(r)) for r in raum.raeume if _ist_privat(r) and _poly(r)]
    out: list[tuple[float, float, str, str]] = []

    for a in raum.ausgaenge:                   # #5 Ausgang ohne RZ in 2 m
        if a.typ in ("final_exit", "stair_exit") and not any(
                _dist(a.xy_mm, p.xy_mm) <= _AUSGANG_RZ_RADIUS_MM for p in rz):
            out.append((a.xy_mm[0], a.xy_mm[1], "Ausgang ohne RZ (§4.1.2g)", "hart"))

    for p in plz.platzierungen:                # Checkliste 8: Leuchte in Privatraum
        for rid, poly in privat:
            if poly.covers(Point(p.xy_mm)):
                out.append((p.xy_mm[0], p.xy_mm[1], f"Leuchte in Privatraum {rid}", "hart"))

    gedeckt: set[str] = set()                  # #3 Fluchtweg-Segment ohne RZ
    for p in plz.platzierungen:
        gedeckt.update(p.covers_segment)
    for s in raum.zirkulation.segmente:
        if s.segment_id not in gedeckt and s.polyline_mm:
            mx = sum(q[0] for q in s.polyline_mm) / len(s.polyline_mm)
            my = sum(q[1] for q in s.polyline_mm) / len(s.polyline_mm)
            out.append((mx, my, "Segment ohne RZ", "hart"))

    for p in rz:                               # #6 RZ ohne Richtung
        if p.richtung is None:
            out.append((p.xy_mm[0], p.xy_mm[1], "RZ ohne Pfeilrichtung", "hart"))

    plzg = plz.platzierungen                    # #7 Kollision
    for i in range(len(plzg)):
        for j in range(i + 1, len(plzg)):
            if _dist(plzg[i].xy_mm, plzg[j].xy_mm) < _KOLLISION_MM:
                out.append((plzg[i].xy_mm[0], plzg[i].xy_mm[1], "Kollision", "hart"))

    # Unterdeckung: Allgemein-/Fluchtweg-Bereich ohne Symbol UND ohne Zirkulation.
    seg_pts = [q for s in raum.zirkulation.segmente for q in s.polyline_mm]
    for r in raum.raeume:
        poly = _poly(r)
        if poly is None or _ist_privat(r):
            continue
        braucht = (r.ist_communal or r.ist_fluchtweg
                   or (r.raum_typ or "").upper() in _KORRIDOR_TYPEN)
        if not braucht or poly.area / 1e6 < _UNTERDECKT_MIN_M2:
            continue
        hat_symbol = any(poly.covers(Point(p.xy_mm)) for p in plzg)
        hat_zirk = any(poly.covers(Point(q)) for q in seg_pts)
        if not hat_symbol and not hat_zirk:
            c = poly.representative_point()
            out.append((c.x, c.y, f"Allgemeinbereich ohne Notlicht ({r.id})", "weich"))
    return out


def main(floor: str, dxf: str, out_png: str) -> None:
    bundle = build_default_bundle()
    raum = bundle.raum.parse(dxf, floor)
    plz = bundle.platzierer.place(raum, bundle.norm, None)
    photo = photometrie_des_bundles(bundle)
    bericht = pruefbericht(raum, plz, None, norm=bundle.norm, photometrie=photo)
    befunde = _befunde_lokal(raum, plz)
    hart = [b for b in befunde if b[3] == "hart"]
    weich = [b for b in befunde if b[3] == "weich"]

    fig, ax = plt.subplots(figsize=(16, 15))
    for r in raum.raeume:
        if len(r.polygon_mm) < 3:
            continue
        istp = _ist_privat(r)
        ax.add_patch(MplPoly(r.polygon_mm, closed=True, fill=istp,
                             facecolor="#ffd9d9" if istp else "none",
                             edgecolor="#b0b0b0", linewidth=0.5, zorder=1))
    for s in raum.zirkulation.segmente:
        if len(s.polyline_mm) >= 2:
            ax.plot([q[0] for q in s.polyline_mm], [q[1] for q in s.polyline_mm],
                    color="#1EB350", linewidth=0.8, alpha=0.5, zorder=2)
    for a in raum.ausgaenge:
        ax.plot([a.xy_mm[0]], [a.xy_mm[1]], marker="s", color="black", ms=7,
                mfc="yellow", zorder=5)
    for p in plz.platzierungen:
        ax.plot([p.xy_mm[0]], [p.xy_mm[1]], marker="o",
                color=KIND_COLOR.get(p.kind, "gray"), ms=8, mec="black",
                mew=0.6, zorder=6)
    for vx, vy, label, sev in befunde:
        col = "red" if sev == "hart" else "#ff8c00"
        ax.plot([vx], [vy], marker="o", mfc="none", mec=col, ms=22, mew=2.5, zorder=8)
        ax.annotate(label, (vx, vy), textcoords="offset points", xytext=(14, 8),
                    fontsize=7.5, color=col, fontweight="bold", zorder=9)

    ax.set_aspect("equal")
    ax.autoscale_view()
    kinds = dict(Counter(p.kind for p in plz.platzierungen))
    komm = sum(1 for r in raum.raeume if r.ist_communal or r.ist_fluchtweg)
    duenn = " ⚠ ZIRKULATION DÜNN" if komm > 2 * max(1, len(raum.zirkulation.segmente)) else ""
    ax.set_title(
        f"Brünnerstraße {floor} — Regel-Review   STATUS={bericht['status'].upper()}"
        f"   {len(hart)} hart / {len(weich)} Unterdeckung{duenn}\n"
        f"Räume={len(raum.raeume)} (komm/flw={komm}) Türen={len(raum.tueren)} "
        f"Ausgänge={len(raum.ausgaenge)} Segmente={len(raum.zirkulation.segmente)} | "
        f"Symbole={len(plz.platzierungen)} {kinds}\n"
        f"rot=harter Verstoß · orange=Allgemeinbereich ohne Notlicht · gelb=Ausgang · "
        f"rosa=Privatraum (kein Licht) · grün=RZ · blau=SL", fontsize=10)
    ax.set_xlabel("x [mm]"); ax.set_ylabel("y [mm]")
    plt.tight_layout()
    plt.savefig(out_png, dpi=110)
    plt.close(fig)
    print(f"{floor}: STATUS={bericht['status']} hart={len(hart)} unterdeckt={len(weich)} "
          f"Symbole={len(plz.platzierungen)}{duenn} -> {out_png}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
