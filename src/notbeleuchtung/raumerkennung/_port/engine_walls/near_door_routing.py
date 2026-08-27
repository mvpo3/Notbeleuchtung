"""near_door_routing.py — Zirkulations-basiertes Routing von near-door-Symbolen
auf die Türen eines Raums (Slice 16.6.0).

Hintergrund: GSP / Klingel / Wechselschalter sind alle als symbolische near-door-
``wall_ref`` (``near_door_lock_side`` / ``wall_mid_near_door``) markiert. Ohne
Tür-Zuordnung ankern sie alle an derselben (ersten) Tür → 4-fach-Stack.

Modell (menschliche Zirkulation, NICHT Tür-Zählung —
feedback_placement_follows_human_circulation):
- **Eingang** (= Wohnungseingangstür, Block ``WET`` → ``"WET"`` in ``source_ref``):
  GSP (Öffnungsseite) + Klingel + *erster* Wechselschalter. Dort kommt der
  Bewohner an und schaltet beim Reinkommen ein.
- **Durchgang** (Nicht-WET-Tür, z.B. Schiebetür Richtung Wohnzimmer): *weitere*
  Wechselschalter — dort geht man weiter und schaltet das VR-Licht aus.
- **Fallback:** kein Durchgang → alle am Eingang verteilt. Kein Eingang (WET) →
  erste vorhandene Tür wird als Anker genutzt (degeneriert, aber kein Stack).

Pure Funktionen — keine ezdxf-/Report-Kopplung, voll unit-testbar. Geometrie-
Helfer werden aus ``position_resolver`` wiederverwendet (Single-Source).
"""
from __future__ import annotations

from typing import Optional

from engine.walls.door_opening import DoorOpening
from engine.walls.position_resolver import _polygon_centroid, _polygon_min_dist

# wall_refs die über _position_near_door aufgelöst werden (Tür-verankert).
_NEAR_DOOR_EXACT = frozenset({"near_door_lock_side", "wall_mid_near_door"})
# Block-Token das die Wohnungseingangstür identifiziert (Drehtür mit Öffnungsseite).
ENTRANCE_BLOCK_TOKEN = "WET"
# Tür gilt als "zum Raum gehörig" wenn ihr Centroid ≤ dieser Distanz am Polygon.
ROOM_DOOR_MAX_DIST_MM = 400.0
# Slice 2.10.0: Raumnamen-Token der Zirkulationsflächen (Vorraum/Gang) — die
# Tür dorthin ist der RAUMEINGANG. Referenz 4.OG: Raumthermostat sitzt an der
# Eingangs-, nicht an einer Durchgangstür zum Nachbarzimmer (A_25 WOHNZIMMER).
CIRCULATION_ROOM_TOKENS = ("VORRAUM", "GANG", "FLUR", "DIELE")
CIRCULATION_ROOM_EXACT = frozenset({"VR"})
# Dedup-Raster: dieselbe physische Tür taucht pro angrenzendem Raum erneut auf
# (door_opening_loader lädt aus rooms[].doors[]) → über gerundeten Centroid dedupen.
DOOR_DEDUP_TOL_MM = 100.0


def is_near_door_ref(wall_ref: Optional[str]) -> bool:
    """True wenn die ``wall_ref`` tür-verankert ist (near_door-Familie)."""
    wr = (wall_ref or "").lower().strip()
    return wr in _NEAR_DOOR_EXACT or wr.startswith("near_door")


def _door_centroid(d: DoorOpening) -> tuple[float, float]:
    poly = d.polygon_mm
    return (sum(p[0] for p in poly) / len(poly), sum(p[1] for p in poly) / len(poly))


def is_entrance_door(d: DoorOpening) -> bool:
    """Wohnungseingangstür = WET-Block (Token im ``source_ref``)."""
    return ENTRANCE_BLOCK_TOKEN in (d.source_ref or "").upper()


def doors_in_room(
    doors: list[DoorOpening],
    room_polygon: list[tuple[float, float]],
    *,
    max_dist_mm: float = ROOM_DOOR_MAX_DIST_MM,
) -> list[DoorOpening]:
    """Türen deren Centroid am/im Raum-Polygon liegt, dedupliziert über
    gerundeten Centroid (entfernt die per-Raum-Mehrfachladung derselben Tür)."""
    seen: set[tuple[int, int]] = set()
    out: list[DoorOpening] = []
    for d in doors:
        c = _door_centroid(d)
        if _polygon_min_dist(c, room_polygon) > max_dist_mm:
            continue
        key = (round(c[0] / DOOR_DEDUP_TOL_MM), round(c[1] / DOOR_DEDUP_TOL_MM))
        if key in seen:
            continue
        seen.add(key)
        out.append(d)
    return out


def classify_doors(
    room_doors: list[DoorOpening],
) -> tuple[list[DoorOpening], list[DoorOpening]]:
    """(entrance_doors, onward_doors) — Eingang via WET-Token, Rest = Durchgang."""
    entrance = [d for d in room_doors if is_entrance_door(d)]
    onward = [d for d in room_doors if not is_entrance_door(d)]
    return entrance, onward


def is_circulation_room_name(name: str) -> bool:
    """True wenn der Raumname eine Zirkulationsfläche (Vorraum/Gang) bezeichnet."""
    up = (name or "").upper().strip()
    return up in CIRCULATION_ROOM_EXACT or any(tok in up for tok in CIRCULATION_ROOM_TOKENS)


def circulation_door(
    room_doors: list[DoorOpening],
    circulation_polygons: list[list[tuple[float, float]]],
    *,
    max_dist_mm: float = ROOM_DOOR_MAX_DIST_MM,
) -> Optional[DoorOpening]:
    """Erste Nicht-WET-Tür deren Centroid an einem Zirkulations-Raum-Polygon
    liegt (= Raumeingang von Vorraum/Gang aus). None wenn keine — Caller fällt
    auf das bisherige onward-Verhalten zurück."""
    for d in room_doors:
        if is_entrance_door(d):
            continue
        c = _door_centroid(d)
        for poly in circulation_polygons:
            if len(poly) >= 3 and _polygon_min_dist(c, poly) <= max_dist_mm:
                return d
    return None


def _is_klingel(symbol: dict) -> bool:
    return "klingel" in str(symbol.get("catalog_entry_id", "")).lower()


def _is_gsp(symbol: dict) -> bool:
    return str(symbol.get("wall_ref", "")).lower().strip() == "wall_mid_near_door"


def _is_freilauf(symbol: dict) -> bool:
    """Freilauftürschließer — sitzt an der Eingangstür (Türleiste/hinge_side)."""
    return "freilauf" in str(symbol.get("catalog_entry_id", "")).lower()


def _is_ato(symbol: dict) -> bool:
    """ATÖ-Türöffnertaster (aus GSP abgeleitet) — gehört an die Eingangstür."""
    return "ato_tueroeffner" in str(symbol.get("decision_source", "")).lower()


def _is_thermostat(symbol: dict) -> bool:
    """Raumthermostat — sitzt beim Raumeingang, unten im Stack unter den Schaltern."""
    return "raumthermostat" in str(symbol.get("catalog_entry_id", "")).lower()


def _anchor_side(symbol: dict) -> str:
    """Anker-Seite der Tür: GSP=Türmitte, Freilauf=Türleiste, Rest=Öffnungs-/Griffseite.
    Symbole verschiedener Seiten stapeln NICHT übereinander (eigener Anker)."""
    wr = str(symbol.get("wall_ref", "")).lower().strip()
    if wr == "wall_mid_near_door":
        return "mid"
    if wr == "near_door_hinge_side":
        return "hinge"
    if wr == "near_door_outside":
        # Slice 18.13.0: Flurseite — eigener Anker, stapelt nicht mit Innen-Symbolen.
        return "outside"
    return "handle"


def _stack_rank(symbol: dict) -> int:
    """Stapel-Reihenfolge an EINER Anker-Seite, unten→oben:
    Thermostat → Schalter → Klingel → ATÖ → Steckdose."""
    if _is_thermostat(symbol):
        return 0
    if _is_klingel(symbol):
        return 2
    if _is_ato(symbol):
        return 3
    cid = str(symbol.get("catalog_entry_id", "")).lower()
    if "schuko" in cid or "steckdose" in cid or "kraftsteckdose" in cid:
        return 4
    return 1  # Schalter (Default Griffseite)


def assign_symbols_to_doors(
    symbols: list[dict],
    room_doors: list[DoorOpening],
    thermostat_door: Optional[DoorOpening] = None,
) -> list[Optional[tuple[DoorOpening, int, int]]]:
    """Ordne jedem near-door-Symbol seine Ziel-Tür + (within_index, within_count) zu.

    ``symbols`` ist eine Liste von Decision-Dicts (mit ``wall_ref`` +
    ``catalog_entry_id``), Reihenfolge stabil. Rückgabe ist parallel: pro Symbol
    ``(target_door, within_index, within_count)`` oder ``None`` (keine Tür im Raum
    → Caller fällt auf bestehende Resolver-Heuristik zurück).

    Zuordnung (Zirkulation): GSP + Klingel + erster Schalter → Eingang;
    weitere Schalter → Durchgang (oder Eingang als Fallback).

    ``room_doors`` muss bereits via ``doors_in_room`` gefiltert+dedupliziert sein.

    ``thermostat_door`` (Slice 2.10.0): explizite Ziel-Tür für Raumthermostate —
    der RAUMEINGANG von der Zirkulationsfläche aus (via ``circulation_door``).
    None → bisheriges Verhalten (onward-Tür). Hintergrund: ohne WET im Raum
    degeneriert entrance/onward zur ERSTEN Tür der Liste; im A_25-WOHNZIMMER
    landete der Thermostat dadurch an der Durchgangstür zum ZIMMER (3,3 m von
    der Referenz an der Vorraum-Tür).
    """
    entrance_doors, onward_doors = classify_doors(room_doors)

    entrance = entrance_doors[0] if entrance_doors else (
        onward_doors[0] if onward_doors else None
    )
    onward = onward_doors[0] if onward_doors else entrance

    if entrance is None:
        return [None] * len(symbols)

    # Schalter werden über ALLE Türen verteilt (Eingang + jede Durchgangstür),
    # round-robin. Slice 18.4.0: vorher kollabierten alle Schalter nach dem
    # ersten auf EINE onward-Tür → injizierte Raum-Minimum-Schalter stapelten.
    switch_doors = [entrance] + [d for d in onward_doors if d is not entrance]

    # Ziel-Tür pro Symbol bestimmen.
    targets: list[DoorOpening] = []
    switch_seen = 0
    for s in symbols:
        if _is_thermostat(s):
            # Slice 18.14.0: Raumthermostat an die RAUMEIGENE Durchgangstür, NICHT
            # die Wohnungseingangstür (WET). Sonst landet z.B. ein Wohnzimmer-
            # Thermostat über die geteilte WET-Tür im Vorraum (Partition-Mismatch).
            # Slice 2.10.0: hat der Raum eine Tür zur Zirkulationsfläche
            # (Vorraum/Gang), ist DIE der Raumeingang → Thermostat dorthin.
            targets.append(thermostat_door or onward)
        elif (
            _is_gsp(s) or _is_klingel(s) or _is_freilauf(s) or _is_ato(s)
        ):
            # GSP/Klingel/ATÖ am Eingang (Öffnungsseite), Freilauf an der Türleiste.
            targets.append(entrance)
        else:  # Schalter: erster am Eingang, weitere reihum auf die Durchgänge
            targets.append(switch_doors[switch_seen % len(switch_doors)])
            switch_seen += 1

    # within-Index je (Ziel-Tür, Anker-Seite) in Stack-Reihenfolge
    # (Thermostat→Schalter→Klingel→ATÖ→Steckdose). Entlang der Wand versetzt =
    # gestapelt (Referenz-Geometrie ~165–210mm). Verschiedene Anker-Seiten
    # (Türmitte/Griffseite/Türleiste) stapeln NICHT übereinander.
    groups: dict[tuple[int, str], list[int]] = {}
    for i, (s, t) in enumerate(zip(symbols, targets)):
        groups.setdefault((id(t), _anchor_side(s)), []).append(i)
    within = [0] * len(symbols)
    count = [1] * len(symbols)
    for idxs in groups.values():
        ordered = sorted(idxs, key=lambda i: (_stack_rank(symbols[i]), i))
        for pos, i in enumerate(ordered):
            within[i] = pos
            count[i] = len(idxs)

    return [(targets[i], within[i], count[i]) for i in range(len(symbols))]
