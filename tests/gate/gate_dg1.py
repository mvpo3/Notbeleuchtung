"""Rennweg DG1: behält das Geschoss einen Ausgang, der nicht durch den Liftschacht führt? — Bedingung (11).

Owner-Entscheid 2026-09-26 (VA-5, § 6g.11 in docs/GATE_TUERSTAPEL.md): „DG1 hat
nach dem Stapel mindestens einen Ausgang, und keiner davon führt durch den
Liftschacht." Heute ist der einzige DG1-Ausgang ``exit_durchgang_9`` — ein
Phantom-Durchgang ``rest_2`` ↔ ``rest_3`` um die Wandenden des Liftkerns, sein
Türpunkt (Schwerpunkt des freien Teils) liegt in der Kabine ``lift_1``. Die
Bedingung schützt davor, dass S5c ihn entfernt und das Geschoss ausgangslos
zurücklässt.

„Durch den Liftschacht" heißt hier: der Türpunkt des Ausgangs liegt in einem
LIFT-Polygon (``raum_typ == "LIFT"``) oder näher als ``LIFT_NAH_MM`` daran. Das
deckt den Phantom-Durchgang (0 mm) und die Lifttür-Ausgänge (gemessen 199,9-208,9
mm: EG ``exit_durchgang_21``, UG ``exit_durchgang_2``, OG1 ``exit_durchgang_8``);
der nächste andere Ausgang auf UG/EG/OG1/DG1 liegt 873 mm vom Schacht (OG1
``exit_durchgang_6``).
Türpunkt = ``xy_mm`` der Tür hinter ``exit_<tuer_id>``; ohne Tür (footprint-
Ausgang) der Punkt des Ausgangs selbst.

Gemessen, nicht geurteilt — das Urteil fällt ``gate_regel`` (11). Ohne LIFT-
Polygon ist ``ausgaenge_durch_liftschacht`` None mit ``grund``: ohne Schacht
lässt sich die Aussage nicht prüfen, und ein Phantom-Ausgang darf nicht still
bestehen.
"""
from __future__ import annotations

from shapely.geometry import Point, Polygon

LIFT_NAH_MM = 250.0


def ausgaenge_lift(modell) -> dict:
    """Ausgänge des Modells und ihr Abstand zum Liftschacht (Bedingung (11))."""
    tueren = {t.id: t for t in modell.tueren}
    lifte = [(r.id, Polygon(r.polygon_mm)) for r in modell.raeume
             if r.raum_typ == "LIFT" and len(r.polygon_mm) >= 3]
    liste = []
    for a in modell.ausgaenge:
        t = tueren.get(a.id.removeprefix("exit_"))
        punkt = Point(t.xy_mm if t is not None else a.xy_mm)
        abstand = min((p.distance(punkt) for _, p in lifte), default=None)
        liste.append({
            "id": a.id, "typ": a.typ, "tuer_id": t.id if t is not None else None,
            "raumpaar": [t.von_raum, t.nach_raum] if t is not None else None,
            "breite_mm": t.breite_mm if t is not None else None,
            "abstand_lift_mm": None if abstand is None else round(abstand, 1),
            "im_lift": any(p.covers(punkt) for _, p in lifte),
            "durch_liftschacht": abstand is not None and abstand < LIFT_NAH_MM,
        })
    return {
        "ausgaenge": len(liste),
        "ausgaenge_liste": liste,
        "ausgaenge_durch_liftschacht":
            sum(1 for e in liste if e["durch_liftschacht"]) if lifte else None,
        "lifte": [i for i, _ in lifte],
        "grund": "" if lifte else "kein LIFT-Polygon im Modell",
    }
