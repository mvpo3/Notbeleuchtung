"""raumtyp — Raumstempel (MTEXT/TEXT) → raum_typ + Flags, per Point-in-Polygon.

Der Textstempel wird über den Port-Klassifikator ``classify_room`` einem
``RoomType`` zugeordnet und auf das Contract-Feld ``raum_typ`` (Freitext,
deutsch, Uppercase) plus die Flags ``ist_fluchtweg`` / ``ist_communal``
abgebildet. Die Zuordnung Stempel→Raum läuft per Point-in-Polygon.

Grenze: braucht brauchbare Raum-Polygone (S2 clean-DXF-Pfad). Auf echten
Plänen ohne Gap-Healing gibt es nur wenige — dort bleibt raum_typ leer.
"""
from __future__ import annotations

from shapely.geometry import Point, Polygon

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum

from ._port.models.room import RoomType, classify_room
from .dxf_load import DxfPlan

TEXT_PREFIXES: tuple[str, ...] = (
    "01-TXT", "02-TXT", "03-TXT", "04-TXT", "05-TXT",
)

# RoomType → (raum_typ-Label, ist_fluchtweg, ist_communal).
_TYP_MAP: dict[RoomType, tuple[str, bool, bool]] = {
    RoomType.STAIRCASE: ("STIEGENHAUS", True, True),
    RoomType.CORRIDOR: ("GANG", True, True),
    RoomType.ENTRANCE_HALL: ("VORRAUM", True, True),
    RoomType.LIVING_ROOM: ("WOHNZIMMER", False, False),
    RoomType.BEDROOM: ("SCHLAFZIMMER", False, False),
    RoomType.CHILDREN_ROOM: ("KINDERZIMMER", False, False),
    RoomType.GENERIC_ROOM: ("ZIMMER", False, False),
    RoomType.KITCHEN: ("KÜCHE", False, False),
    RoomType.BATHROOM: ("BAD", False, False),
    RoomType.WC: ("WC", False, False),
    RoomType.STORAGE: ("ABSTELLRAUM", False, False),
    RoomType.BALCONY: ("BALKON", False, False),
    RoomType.TERRACE: ("TERRASSE", False, False),
}


def _stempel(plan: DxfPlan) -> list[tuple[str, tuple[float, float]]]:
    """(Text, xy_mm) aller MTEXT/TEXT auf den Text-Layern."""
    out: list[tuple[str, tuple[float, float]]] = []
    for e in plan.entities(TEXT_PREFIXES):
        t = e.dxftype()
        if t == "MTEXT":
            txt = e.plain_text()
            xy = plan._scale(e.dxf.insert)
        elif t == "TEXT":
            txt = e.dxf.text
            xy = plan._scale(e.dxf.insert)
        else:
            continue
        if txt and txt.strip():
            out.append((txt.strip(), xy))
    return out


def beschrifte_raeume(plan: DxfPlan, raeume: list[Raum]) -> list[Raum]:
    """Setzt ``raum_typ`` + Flags je Raum aus dem enthaltenen Stempel."""
    stempel = _stempel(plan)
    polys = [(r, Polygon(r.polygon_mm)) for r in raeume if len(r.polygon_mm) >= 3]
    for txt, xy in stempel:
        rt = classify_room(txt)
        if rt is RoomType.UNKNOWN:
            continue
        label, flucht, communal = _TYP_MAP.get(rt, (txt.upper(), False, False))
        pt = Point(xy)
        for r, poly in polys:
            if r.raum_typ:  # bereits gesetzt
                continue
            if poly.covers(pt):
                r.raum_typ = label
                r.ist_fluchtweg = flucht
                r.ist_communal = communal
                break
    return raeume
