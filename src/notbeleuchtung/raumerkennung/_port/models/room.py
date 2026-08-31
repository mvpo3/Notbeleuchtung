"""
room.py — Raum-Datenmodell / Room data model.

Pure dataclasses; geometry stored as lists of (x, y) tuples in
millimetres rather than shapely objects, so the model stays
serialisable and framework-free.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum


class RoomType(str, Enum):
    """Canonical room types used by the placement engine.

    German label → canonical code. Mapping table lives in
    :data:`GERMAN_ROOM_TYPE_MAP`.
    """
    LIVING_ROOM = "LIVING_ROOM"
    BEDROOM = "BEDROOM"
    CHILDREN_ROOM = "CHILDREN_ROOM"
    GENERIC_ROOM = "GENERIC_ROOM"          # "Zimmer" catch-all, bedroom-equivalent
    KITCHEN = "KITCHEN"
    BATHROOM = "BATHROOM"
    WC = "WC"
    CORRIDOR = "CORRIDOR"
    ENTRANCE_HALL = "ENTRANCE_HALL"        # "Vorraum"
    STAIRCASE = "STAIRCASE"                # "Stiegenhaus"
    STORAGE = "STORAGE"
    BALCONY = "BALCONY"
    TERRACE = "TERRACE"
    UNKNOWN = "UNKNOWN"


# German label (lowercased) → RoomType. Order matters: substring-matching
# walks this in insertion order, so more specific keys must precede their
# substrings. "stiegenhaus" before "gang"; "kinderzimmer" and
# "wohnzimmer" before the generic "zimmer"; "einlagerungsraum" before
# "abstellraum" so both still resolve to STORAGE.
GERMAN_ROOM_TYPE_MAP: dict[str, RoomType] = {
    # Most specific first ─────────────────────────────────────
    "stiegenhaus": RoomType.STAIRCASE,
    "einlagerungsraum": RoomType.STORAGE,
    "abstellraum": RoomType.STORAGE,
    "kinderzimmer": RoomType.CHILDREN_ROOM,
    "schlafzimmer": RoomType.BEDROOM,
    "schlafraum": RoomType.BEDROOM,
    "wohnzimmer": RoomType.LIVING_ROOM,
    "wohnraum": RoomType.LIVING_ROOM,
    "badezimmer": RoomType.BATHROOM,
    "vorraum": RoomType.ENTRANCE_HALL,
    # Short specific ────────────────────────────────────────
    "küche": RoomType.KITCHEN,
    "kueche": RoomType.KITCHEN,
    "bad": RoomType.BATHROOM,
    "wc": RoomType.WC,
    "abstell": RoomType.STORAGE,
    "balkon": RoomType.BALCONY,
    "terrasse": RoomType.TERRACE,
    # Catch-alls LAST — generic "zimmer" must not pre-empt
    # kinderzimmer/schlafzimmer/wohnzimmer above.
    "zimmer": RoomType.GENERIC_ROOM,
    "flur": RoomType.CORRIDOR,
    "gang": RoomType.CORRIDOR,
    "diele": RoomType.CORRIDOR,
}


# Komposita-Köpfe, die über die Wortgrenze hinaus matchen dürfen (Wohn-KÜCHE,
# Gäste-ZIMMER) — und der Abstell-Prefix (Abstell-raum/-kammer/-fläche → STORAGE).
_SUFFIX_SAFE = ("zimmer", "küche", "kueche")
_PREFIX_SAFE = ("abstell",)
_WORD_RE = re.compile(r"[a-zäöüß]+")


def classify_room(label: str) -> RoomType:
    """Classify a free-form German room label; fall back to UNKNOWN.

    Token/Wortgrenze statt rohem Substring: `needle in key` würde „gang" in
    „Ein**gang**"/„Zu**gang**"/„Aus**gang**" als CORRIDOR fehltypisieren — mit
    Notlicht-Folge, da CORRIDOR=Fluchtweg (real beobachtet: „Zugang Müllraum"→GANG).
    Nur Komposita-Köpfe (…zimmer/…küche) und der Abstell-Prefix matchen über die
    Wortgrenze hinaus; alles andere muss ein eigenständiges Token sein.
    """
    key = (label or "").strip().lower()
    if key in GERMAN_ROOM_TYPE_MAP:
        return GERMAN_ROOM_TYPE_MAP[key]
    tokens = _WORD_RE.findall(key)
    for t in tokens:                       # exaktes Token: Gang, Bad, WC, Wohnzimmer …
        if t in GERMAN_ROOM_TYPE_MAP:
            return GERMAN_ROOM_TYPE_MAP[t]
    for t in tokens:                       # Komposita-Kopf/-Prefix
        for needle in _SUFFIX_SAFE:
            if t.endswith(needle):
                return GERMAN_ROOM_TYPE_MAP[needle]
        for needle in _PREFIX_SAFE:
            if t.startswith(needle):
                return GERMAN_ROOM_TYPE_MAP[needle]
    return RoomType.UNKNOWN


@dataclass
class Room:
    """One detected room.

    Attributes
    ----------
    id : str
        Stable identifier (e.g. "WZ", "BAD-01") — ideally matched against
        the Leistungsbeschreibung's Raumbuchnummer.
    name : str
        German label as found in the DXF / Leistungsbeschreibung.
    room_type : RoomType
        Canonical type; drives OVE-rule selection.
    boundary : list[tuple[float, float]]
        Closed polygon in mm, CCW orientation, first point != last.
    area_m2 : float
        Convenience field; can be recomputed from boundary.
    centroid : tuple[float, float] | None
        Optional precomputed centroid in mm.
    """
    id: str
    name: str
    room_type: RoomType
    boundary: list[tuple[float, float]] = field(default_factory=list)
    area_m2: float = 0.0
    centroid: tuple[float, float] | None = None
