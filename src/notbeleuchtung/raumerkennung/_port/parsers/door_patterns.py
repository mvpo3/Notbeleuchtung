"""Block-name pattern constants for door identification in
architecture DXFs. Extracted as a separate leaf module so that both
`parsers.architecture_dxf` and `parsers.scale_detector` can import
them without forming a circular import.
"""
from __future__ import annotations

# Block-name prefixes that indicate door-like INSERTs.
# "WET" = Wohnungs-Eingangstür (apartment entrance door). Swing door with an
# ARC (→ generic ARC-geometry extraction yields hinge/handle/open-side, same
# as TÜR). Without this it was dropped by the name-filter, leaving every VR
# without its entrance anchor (see project_wet_entrance_door_gap). Matched as
# substring like the others; verified the only "WET"-named block is the door
# (6×/floor = 1/apartment). NOT a sliding door — kept out of SLIDING_DOOR_PATTERNS.
DOOR_NAME_PATTERNS: tuple[str, ...] = (
    "TÜR", "TUER", "SCHIEBETÜR", "SCHIEBETUER", "WET",
)

# Slice 9.2.7: blocks whose name matches DOOR_NAME_PATTERNS but are
# actually labels (Türlisten-Stempel) and must be filtered out. They
# live on text/position layers and contain ATTDEFs, no ARC, no wall
# geometry.
DOOR_LABEL_PATTERNS: tuple[str, ...] = ("TÜRACHSE", "TUERACHSE")

# Sliding doors. Excluded from scale-detection because their widths vary
# 800-1200 mm and would skew the median; in placement they get
# rectangle-fallback geometry instead of a swing arc.
SLIDING_DOOR_PATTERNS: tuple[str, ...] = ("SCHIEBETÜR", "SCHIEBETUER")

# Slice N15: default excludes for the block-based door detector
# (parsers.door_blocks). "BS_*" = Fischamender Beschriftungs-Stempel
# (BS_Tuer_PP - links/rechts/… on A_Beschriftung_) — label blocks, no door
# geometry. NOTE a documented accident: auto_marker's name path matches
# "TÜR" only WITH umlaut, so "BS_Tuer_PP" slips through there purely
# because of its ASCII spelling ("TUER" != "TÜR"). The block detector
# excludes them explicitly instead of relying on that.
DOOR_BLOCK_EXCLUDE_PATTERNS: tuple[str, ...] = ("^BS_",) + DOOR_LABEL_PATTERNS
