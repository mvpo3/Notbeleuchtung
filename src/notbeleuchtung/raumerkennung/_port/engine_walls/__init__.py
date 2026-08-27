"""engine.walls — Wand-Datenmodell + Loader (M2-Track 11.x.x)."""
from engine.walls.door_opening import (
    DEFAULT_WALL_THICKNESS_MM,
    DoorOpening,
    build_door_polygon,
)
from engine.walls.door_opening_index import (
    DoorOpeningIndex,
    point_in_polygon,
)
from engine.walls.door_opening_loader import (
    DEFAULT_DOOR_WIDTH_MM,
    DoorLoadStats,
    REASON_DEGENERATE_WIDTH,
    REASON_MALFORMED as REASON_MALFORMED_DOOR,
    REASON_MISSING_HINGE,
    REASON_SLIDING_UNSUPPORTED,
    load_door_openings_from_arch,
)
from engine.walls.loader import (
    LoadStats,
    REASON_DEGENERATE_ZERO_LENGTH,
    REASON_MALFORMED,
    load_walls_from_arch,
)
from engine.walls.opening_bridge import (
    DEFAULT_OPENING_CLEARANCE_MM,
    BridgeStats,
    bridge_walls_across_openings,
    distribute_distance_avoiding_openings,
    logical_wall_by_source_id,
    nearest_distance_avoiding_openings,
    opening_free_intervals,
    opening_free_length,
)
from engine.walls.resolver import (
    ResolveResult,
    STATUS_AMBIGUOUS,
    STATUS_NEEDS_CORNER_ANCHOR,
    STATUS_NEEDS_FURNITURE,
    STATUS_NOT_A_WALL_ANCHOR,
    STATUS_NOT_FOUND,
    STATUS_OK,
    STATUS_UNKNOWN_REF,
    resolve_wall_ref,
)
from engine.walls.position_resolver import (
    CORNER_ANCHOR_INSET_MM,
    CORNER_INSET_MM,
    NEAR_DOOR_OFFSET_MM,
    PERP_INSET_MM,
    VERTEILER_SIBLING_SPACING_MM,
    WINDOW_PERP_INSET_MM,
    PositionResult,
    STATUS_POS_NEEDS_DOOR_ANCHOR,
    STATUS_POS_NEEDS_FURNITURE,
    STATUS_POS_NO_WALL_FOUND,
    STATUS_POS_OK,
    STATUS_POS_UNKNOWN_REF,
    filter_walls_by_room_polygon,
    position_verteiler_at_anchor,
    position_verteiler_entrance_wall,
    resolve_position,
)
from engine.walls.sliding_door_loader import (
    DEFAULT_SLIDING_DOOR_WIDTH_MM,
    REASON_MALFORMED_SLIDING,
    REASON_SLIDING_DEGENERATE_WIDTH,
    REASON_SLIDING_MISSING_ROTATION,
    SlidingDoorLoadStats,
    load_sliding_door_openings_from_arch,
)
from engine.walls.wall import OpeningSpan, Wall
from engine.walls.window_opening import (
    WindowOpening,
    build_window_polygon,
)
from engine.walls.window_opening_index import WindowOpeningIndex
from engine.walls.window_opening_loader import (
    DEFAULT_WINDOW_WIDTH_MM,
    REASON_DEGENERATE_WIDTH as REASON_WINDOW_DEGENERATE_WIDTH,
    REASON_MALFORMED as REASON_MALFORMED_WINDOW,
    REASON_MISSING_ROTATION,
    WindowLoadStats,
    load_window_openings_from_arch,
)

__all__ = [
    # Wand-Datenmodell + Loader (Slice 11.1.0/11.2.0)
    "Wall",
    "OpeningSpan",
    "LoadStats",
    "load_walls_from_arch",
    "BridgeStats",
    "bridge_walls_across_openings",
    "logical_wall_by_source_id",
    "opening_free_intervals",
    "opening_free_length",
    "distribute_distance_avoiding_openings",
    "nearest_distance_avoiding_openings",
    "DEFAULT_OPENING_CLEARANCE_MM",
    "REASON_DEGENERATE_ZERO_LENGTH",
    "REASON_MALFORMED",
    # Wand-Resolver (Slice 11.4.0 + 11.5.2)
    "ResolveResult",
    "resolve_wall_ref",
    "STATUS_OK",
    "STATUS_AMBIGUOUS",
    "STATUS_NOT_FOUND",
    "STATUS_NOT_A_WALL_ANCHOR",
    "STATUS_NEEDS_FURNITURE",
    "STATUS_NEEDS_CORNER_ANCHOR",
    "STATUS_UNKNOWN_REF",
    # Position-Resolver (Slice 11.5.0)
    "PositionResult",
    "resolve_position",
    "position_verteiler_entrance_wall",
    "position_verteiler_at_anchor",
    "filter_walls_by_room_polygon",
    "STATUS_POS_OK",
    "STATUS_POS_NEEDS_DOOR_ANCHOR",
    "STATUS_POS_NEEDS_FURNITURE",
    "STATUS_POS_NO_WALL_FOUND",
    "STATUS_POS_UNKNOWN_REF",
    "CORNER_INSET_MM",
    "PERP_INSET_MM",
    "NEAR_DOOR_OFFSET_MM",
    "CORNER_ANCHOR_INSET_MM",
    "VERTEILER_SIBLING_SPACING_MM",
    "WINDOW_PERP_INSET_MM",
    # Tür-Aussparungs-Polygone + Avoidance-Index (Slice 11.3.0-redo)
    "DoorOpening",
    "DoorOpeningIndex",
    "DoorLoadStats",
    "build_door_polygon",
    "point_in_polygon",
    "load_door_openings_from_arch",
    "DEFAULT_DOOR_WIDTH_MM",
    "DEFAULT_WALL_THICKNESS_MM",
    "REASON_SLIDING_UNSUPPORTED",
    "REASON_MISSING_HINGE",
    "REASON_DEGENERATE_WIDTH",
    "REASON_MALFORMED_DOOR",
    # Fenster-Aussparungs-Polygone (Slice 11.3.1)
    "WindowOpening",
    "WindowOpeningIndex",
    "WindowLoadStats",
    "build_window_polygon",
    "load_window_openings_from_arch",
    "DEFAULT_WINDOW_WIDTH_MM",
    "REASON_MISSING_ROTATION",
    "REASON_WINDOW_DEGENERATE_WIDTH",
    "REASON_MALFORMED_WINDOW",
    # Sliding-Tür-Aussparungs-Polygone (Slice 11.3.2)
    "SlidingDoorLoadStats",
    "load_sliding_door_openings_from_arch",
    "DEFAULT_SLIDING_DOOR_WIDTH_MM",
    "REASON_SLIDING_DEGENERATE_WIDTH",
    "REASON_SLIDING_MISSING_ROTATION",
    "REASON_MALFORMED_SLIDING",
]
