"""resolver.py - Wand-Resolver `wall_ref -> Wall` (Slice 11.4.0).

Mappt symbolische ``wall_ref``-Strings (gesetzt in
``engine/strategies/*.py``) auf konkrete ``Wall``-Instanzen aus dem
Loader (Slice 11.2.0). Modul-Funktion analog ``loader.py`` -
state-less, dependency-injected via ``room_walls``-Subset.

Kein Konsumenten-Touch in dieser Slice. Erster Konsument ist der
Position-Resolver in Slice 11.5.0; die M2-Vorgaenger-Pipeline
(``coordinate_assigner._bucket_for``) blieb parallel-existent bis zur
Konsumenten-Migration in 11.8.0 und wurde in 11.8.2 sunset.

Live-Pre-Read (``placement_all_good_apartments.json``, 138 Decisions,
16 distinct wall_refs) klassifiziert die Strings in 6 Kategorien:

- ``longest_wall`` (43): ``wall_bwu_*``
- ``not_a_wall_anchor`` (43): ``ceiling_*``, ``door_frame``
- ``needs_furniture`` (39): ``wall_appliance_*``, ``worktop_*``,
  ``wall_high_bwo``, ``wall_mid_inner``
- ``needs_door_context`` (7): ``near_door_*``, ``wall_mid_near_door``,
  ``wall_corner_or_door_adjacent``
- ``needs_window_context`` (6): ``wall_top_window``
- ``unknown_ref`` (0 in Live)

Door-/Window-Aware-Resolution ist Slice 11.5.0 (Position-Resolver hat
dort ``DoorOpeningIndex`` / ``WindowOpeningIndex``); hier wird der
Status mit explizitem ``reason`` propagiert.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from engine.walls.wall import Wall

# Length-tolerance for ambiguity check between longest walls (mm).
_LONGEST_AMBIGUITY_TOL_MM = 1.0

# ---- Status constants -------------------------------------------------

STATUS_OK = "ok"
STATUS_AMBIGUOUS = "ambiguous"
STATUS_NOT_FOUND = "not_found"
STATUS_NOT_A_WALL_ANCHOR = "not_a_wall_anchor"
STATUS_NEEDS_FURNITURE = "needs_furniture"
STATUS_NEEDS_CORNER_ANCHOR = "needs_corner_anchor"
STATUS_UNKNOWN_REF = "unknown_ref"


# ---- Result dataclass -------------------------------------------------


@dataclass(frozen=True)
class ResolveResult:
    """Ausgang einer ``wall_ref``-Resolution.

    Felder
    ------
    wall
        Gewaehlte Wand bei ``status == STATUS_OK`` oder
        ``STATUS_AMBIGUOUS`` (dort ist es die rang-erste). Sonst None.
    status
        Eines der ``STATUS_*``-Konstanten.
    reason
        Frei-Text-Detail (z.B. ``empty_room_walls``,
        ``needs_door_context:near_door_lock_side``,
        ``non_wall_anchor:ceiling_center``).
    candidates
        Geordnete Liste plausibler Wall-Instanzen. Bei
        ``STATUS_AMBIGUOUS`` enthaelt sie mehrere; sonst entweder
        ``(wall,)`` (OK) oder leer.
    """

    wall: Optional[Wall]
    status: str
    reason: str
    candidates: tuple[Wall, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict:
        return {
            "wall_id": self.wall.id if self.wall else None,
            "status": self.status,
            "reason": self.reason,
            "candidate_ids": [w.id for w in self.candidates],
        }


# ---- Public dispatcher ------------------------------------------------


def resolve_wall_ref(
    wall_ref: Optional[str],
    room_walls: list[Wall],
) -> ResolveResult:
    """Resolve einen symbolischen ``wall_ref``-String gegen die Walls
    eines Raums.

    Parameters
    ----------
    wall_ref
        String aus ``PlacementDecision.wall_ref``. None oder leer ->
        ``STATUS_UNKNOWN_REF``.
    room_walls
        Subset der globalen ``list[Wall]`` aus
        ``load_walls_from_arch``, gefiltert auf die Walls die den Raum
        umranden. Filterung ist Caller-Job (Slice 11.5.0).

    Strategie
    ---------
    Lower-case Prefix-Match dispatcht auf eine private Strategie-
    Funktion. Reihenfolge im if-elif-Block ist signifikant: spezifische
    Prefixe vor generischen.

    Returns
    -------
    ResolveResult
        Siehe Klassen-Docstring.
    """
    if wall_ref is None or not wall_ref.strip():
        return ResolveResult(
            wall=None,
            status=STATUS_UNKNOWN_REF,
            reason="wall_ref_empty_or_none",
        )

    wr = wall_ref.lower().strip()

    if wr == "door_frame" or wr.startswith("ceiling"):
        return _strategy_not_a_wall(wr)
    # Slice 11.5.2: wall_corner_or_door_adjacent ist Verteiler-Eck-Anker,
    # NICHT door-anchored - eigener Status fuer corner-Strategy.
    if wr == "wall_corner_or_door_adjacent":
        return _strategy_needs_corner_anchor(wr)
    if (
        wr.startswith("near_door")
        or wr == "wall_mid_near_door"
    ):
        return _strategy_needs_door_context(wr)
    if wr == "wall_top_window":
        return _strategy_needs_window_context(wr)
    if wr.startswith("wall_bwu"):
        return _strategy_longest_wall(room_walls)
    if (
        wr.startswith("wall_appliance")
        or wr == "worktop_wall_bwm"
        or wr == "wall_high_bwo"
        or wr == "wall_mid_inner"
    ):
        return _strategy_needs_furniture(wr)

    return ResolveResult(
        wall=None,
        status=STATUS_UNKNOWN_REF,
        reason=f"no_strategy_for_ref:{wall_ref}",
    )


# ---- Private strategies -----------------------------------------------


def _strategy_longest_wall(room_walls: list[Wall]) -> ResolveResult:
    """``wall_bwu_*`` - laengste Wand des Raums.

    Konvention aus der M2-Vorgaenger-Pipeline (distribute_along_wall /
    longest_wall_segment, sunset in 11.8.2): BWu wird auf der laengsten
    Wand distribiert.
    """
    if not room_walls:
        return ResolveResult(
            wall=None,
            status=STATUS_NOT_FOUND,
            reason="empty_room_walls",
        )

    sorted_walls = sorted(
        room_walls, key=lambda w: w.length_mm, reverse=True
    )
    longest = sorted_walls[0]

    if len(sorted_walls) >= 2:
        second = sorted_walls[1]
        if abs(longest.length_mm - second.length_mm) < _LONGEST_AMBIGUITY_TOL_MM:
            tied = tuple(
                w
                for w in sorted_walls
                if abs(w.length_mm - longest.length_mm)
                < _LONGEST_AMBIGUITY_TOL_MM
            )
            return ResolveResult(
                wall=longest,
                status=STATUS_AMBIGUOUS,
                reason=f"multiple_longest_within_{_LONGEST_AMBIGUITY_TOL_MM:.0f}mm",
                candidates=tied,
            )

    return ResolveResult(
        wall=longest,
        status=STATUS_OK,
        reason="longest_wall",
        candidates=(longest,),
    )


def _strategy_not_a_wall(wr: str) -> ResolveResult:
    """``ceiling_*`` und ``door_frame`` - referenziert keine Wand.
    Caller muss Decken-/Tuer-Geometrie als Platzierungs-Ziel nutzen.
    """
    return ResolveResult(
        wall=None,
        status=STATUS_NOT_A_WALL_ANCHOR,
        reason=f"non_wall_anchor:{wr}",
    )


def _strategy_needs_door_context(wr: str) -> ResolveResult:
    """``near_door_*`` und ``wall_mid_near_door`` - braucht
    ``DoorOpeningIndex``, der dem Position-Resolver in Slice 11.5.0/11.5.1
    zur Verfuegung steht. Hier explizit als ``NOT_FOUND`` mit Reason
    zurueckgegeben (Slice 11.5.2: wall_corner_or_door_adjacent ist
    eigener Status, siehe ``_strategy_needs_corner_anchor``).
    """
    return ResolveResult(
        wall=None,
        status=STATUS_NOT_FOUND,
        reason=f"needs_door_context:{wr}",
    )


def _strategy_needs_corner_anchor(wr: str) -> ResolveResult:
    """``wall_corner_or_door_adjacent`` (Slice 11.5.2) - Verteiler-Eck-
    Anker. Pre-Read-Befund: 2 Live-Decisions (e_verteiler +
    schwachstrom_verteiler) sind 1400-1700mm vom naechsten Door-Handle
    entfernt - semantisch Wand-Ecke nahe Eingangstuer, NICHT door-
    anchored. Position-Resolver implementiert
    ``_position_corner_anchor`` mit Polygon-Eck-Pickung (Reference-
    Pattern: near_corner aus der M2-Vorgaenger-Pipeline, sunset in
    11.8.2).
    """
    return ResolveResult(
        wall=None,
        status=STATUS_NEEDS_CORNER_ANCHOR,
        reason=f"needs_corner_anchor:{wr}",
    )


def _strategy_needs_window_context(wr: str) -> ResolveResult:
    """``wall_top_window`` - analog needs_door_context fuer
    ``WindowOpeningIndex`` (Slice 11.3.1).
    """
    return ResolveResult(
        wall=None,
        status=STATUS_NOT_FOUND,
        reason=f"needs_window_context:{wr}",
    )


def _strategy_needs_furniture(wr: str) -> ResolveResult:
    """``wall_appliance_*``, ``worktop_*``, ``wall_high_bwo``,
    ``wall_mid_inner`` - referenziert Moebel-/Sanitaer-Geometrie
    (Geschirrspueler, Backofen, Badewanne, etc.) die heute nicht im
    Wand-Datenmodell modelliert ist. Punt auf spaeteren Furniture-
    Slice (vermutlich 11.6.0+).
    """
    return ResolveResult(
        wall=None,
        status=STATUS_NEEDS_FURNITURE,
        reason=f"needs_furniture_geometry:{wr}",
    )
