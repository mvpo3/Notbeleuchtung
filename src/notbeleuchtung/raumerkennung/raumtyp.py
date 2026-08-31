"""raumtyp — Raumstempel (MTEXT/TEXT) → raum_typ + Flags, per Point-in-Polygon.

Der Textstempel wird über den Port-Klassifikator ``classify_room`` einem
``RoomType`` zugeordnet und auf das Contract-Feld ``raum_typ`` (Freitext,
deutsch, Uppercase) plus die Flags ``ist_fluchtweg`` / ``ist_communal``
abgebildet. Die Zuordnung Stempel→Raum läuft per Point-in-Polygon.

Grenze: braucht brauchbare Raum-Polygone (S2 clean-DXF-Pfad). Auf echten
Plänen ohne Gap-Healing gibt es nur wenige — dort bleibt raum_typ leer.
"""
from __future__ import annotations

import re

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


# Österreichische Plan-Abkürzungen/Labels, die `classify_room` (Port) nicht kennt.
# TOKEN-EXAKT geprüft (nicht Substring): „ar" steckt sonst in „Garten", „vr" in
# fremden Wörtern. So typt „VR"/„AR"/„TRH BT1 EG" korrekt, „Garten" bleibt UNKNOWN.
_EXTRA_LABELS: dict[str, RoomType] = {
    "vr": RoomType.ENTRANCE_HALL,    # Vorraum
    "ar": RoomType.STORAGE,          # Abstellraum
    "trh": RoomType.STAIRCASE,       # Treppenhaus / Stiegenhaus (sicherheitskritisch)
    "loggia": RoomType.BALCONY,      # überdachter Freisitz ~ Balkon
}
_WORT = re.compile(r"[A-Za-zÄÖÜäöüß]+")

# LB-Vokabular-Typen OHNE Port-RoomType (GARAGE/TECHNIK/LAGER/MUELLRAUM aus
# `_BEREICH_VOCAB` im LB-Parser). Token-exakt, direkt als (label, ist_fluchtweg,
# ist_communal). Ohne diese Labels feuert die `lb_override`-Inklusion/Exklusion für
# genau diese Raumtypen NIE (tote Regel — der kanonische „Garage → SL"-LB-Fall).
_EXTRA_DIRECT: dict[str, tuple[str, bool, bool]] = {
    "garage": ("GARAGE", False, True),
    "tiefgarage": ("GARAGE", False, True),
    "technik": ("TECHNIK", False, True),
    "haustechnik": ("TECHNIK", False, True),
    "lager": ("LAGER", False, True),
    "müll": ("MUELLRAUM", False, True),
    "müllraum": ("MUELLRAUM", False, True),
    "restmüll": ("MUELLRAUM", False, True),
}


def raumtyp_flags(text: str) -> tuple[str, bool, bool] | None:
    """Freitext-Label → (raum_typ, ist_fluchtweg, ist_communal); None bei UNKNOWN."""
    rt = classify_room(text)
    if rt is not RoomType.UNKNOWN:
        return _TYP_MAP.get(rt, (text.upper(), False, False))
    # Fallback token-exakt (kein Substring-Bleed): österr. Abkürzungen …
    tokens = {t.lower() for t in _WORT.findall(text)}
    rt = next((v for k, v in _EXTRA_LABELS.items() if k in tokens), None)
    if rt is not None:
        return _TYP_MAP[rt]
    # … dann LB-Vokabular-Typen ohne Port-RoomType.
    return next((v for k, v in _EXTRA_DIRECT.items() if k in tokens), None)


def beschrifte_raeume(plan: DxfPlan, raeume: list[Raum]) -> list[Raum]:
    """Setzt ``raum_typ`` + Flags je Raum aus dem enthaltenen Stempel."""
    stempel = _stempel(plan)
    polys = [(r, Polygon(r.polygon_mm)) for r in raeume if len(r.polygon_mm) >= 3]
    for txt, xy in stempel:
        tf = raumtyp_flags(txt)
        if tf is None:
            continue
        label, flucht, communal = tf
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
