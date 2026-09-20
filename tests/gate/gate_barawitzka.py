"""Barawitzka EG: hängt der ABSTELLRAUM 1,98 m² noch an einer Tür? — Bedingung (10).

Von den acht Räumen, die durch S5b auf 0 Verbindungen fallen (§ 8e in
docs/GATE_TUERSTAPEL.md), ist dieser der einzige mit einer **echten Tür ohne
Ersatz**: die 830er Bogenöffnung hat keine eigene Tür, sie steckt in einem
„doppelfluegel" 1660 mm (Fehlpaarung zweier Einzeltüren, S4a-Rest). Die übrigen
sieben verlieren nur synthetische Durchgänge, deren echte Tür im Modell steht.

Gemessen, nicht geurteilt — das Urteil fällt ``gate_regel`` (10). **Heute ist
die Bedingung verletzt** (``anzahl`` 0); sie dreht erst, wenn der S4a-Rest
(Doppelflügel-Paarung) gebaut ist.

Der Raum wird wie in ``gate_referenz`` über ``raum_typ`` + Fläche identifiziert,
nicht über die ID: IDs wandern zwischen Codeständen, Typ und Fläche nicht. Passt
kein oder mehr als ein Raum, ist der Fall NICHT messbar (``anzahl`` None mit
``grund``) — und kein stilles Bestehen.

Neben dem Zähler stehen zwei Messwerte, damit ein Befund ohne neuen Lauf lesbar
bleibt: die nächste erkannte Tür überhaupt (id, quelle, breite, Abstand zum
Raumpolygon) und die „doppelfluegel"-Türen innerhalb von 2 m.
"""
from __future__ import annotations

# ``_raum_id`` ist dieselbe Auflösung wie bei den Referenz-Verbindungen (Typ +
# Fläche ± FLAECHE_TOL_M2, eindeutig oder gar nicht) — einmal reicht.
from gate_referenz import _bezeichnung, _raum_id
from shapely.geometry import Point, Polygon

ABSTELLRAUM = ("ABSTELLRAUM", 1.98)
DOPPELFLUEGEL_NAH_MM = 2000.0


def _tuer(t, poly) -> dict:
    return {"id": t.id, "quelle": t.quelle or "", "breite_mm": t.breite_mm,
            "tuer_detail": t.tuer_detail,
            "abstand_mm": round(poly.distance(Point(t.xy_mm)), 1)}


def _ist_doppelfluegel(t) -> bool:
    """Gemessen 2026-09-20: der Doppelflügel steht in ``quelle``, nicht in
    ``tuer_detail`` (``tuer_38``: quelle »doppelfluegel«, tuer_detail None).
    Beide Felder werden gelesen, damit der Messwert nicht an dieser Ablage hängt."""
    return "doppelfluegel" in f"{t.quelle or ''} {t.tuer_detail or ''}"


def verbindung_abstellraum(modell) -> dict:
    """Türen am ABSTELLRAUM 1,98 m² des Barawitzka-EG-Plans (Bedingung (10))."""
    raum_typ, flaeche = ABSTELLRAUM
    eintrag = {"raum": {"raum_typ": raum_typ, "flaeche_m2": flaeche, "id": None},
               "bezeichnung": _bezeichnung(raum_typ, flaeche)}
    raum_id, grund = _raum_id(modell, raum_typ, flaeche)
    raum = next((r for r in modell.raeume if r.id == raum_id), None)
    if raum is not None and len(raum.polygon_mm) < 3:
        raum_id, grund = None, f"{eintrag['bezeichnung']} hat kein Polygon (< 3 Stützpunkte)"
    if raum_id is None:
        return {**eintrag, "anzahl": None, "ids": [], "grund": grund,
                "naechste_tuer": None, "doppelfluegel_nah": []}
    eintrag["raum"]["id"] = raum_id
    poly = Polygon(raum.polygon_mm)
    tueren = [t for t in modell.tueren if raum_id in (t.von_raum, t.nach_raum)]
    nach_abstand = sorted(modell.tueren, key=lambda t: poly.distance(Point(t.xy_mm)))
    return {**eintrag,
            "anzahl": len(tueren),
            "ids": sorted(t.id for t in tueren),
            "grund": "",
            "naechste_tuer": _tuer(nach_abstand[0], poly) if nach_abstand else None,
            "doppelfluegel_nah": [
                _tuer(t, poly) for t in nach_abstand
                if _ist_doppelfluegel(t)
                and poly.distance(Point(t.xy_mm)) <= DOPPELFLUEGEL_NAH_MM]}
