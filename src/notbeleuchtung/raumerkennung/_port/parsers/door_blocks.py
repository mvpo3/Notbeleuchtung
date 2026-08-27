"""door_blocks — Block-basierter Tür-Detektor (Slice N15).

Ergänzt den geometrischen ARC-Detektor (``parsers.door_arcs``, N2) um
Projekte, die Türen als benannte Blöcke kodieren:

  - Fischamender: Top-Level-INSERTs auf Layer ``A_Tueren``
    (``Tür_Blockzarge_1 Flügel - 90x200_RB …``); die Beschriftungs-Stempel
    ``BS_Tuer_PP - links/…`` liegen auf ``A_Beschriftung_`` und werden
    explizit ausgeschlossen.
  - Rennweg: Türen VERSCHACHTELT in Wand-Blöcken (``Wall_N`` enthält je einen
    INSERT ``Zargentür_1_Fl 10[N]``) — 0 ARCs im Modelspace, der N2-Detektor
    ist dort blind. Braucht 2-Ebenen-INSERT-Auflösung mit komponiertem
    Transform.

Vokabular kommt aus der Profil-Sektion ``roles.doors`` (Track-A-Konvention:
Block-Namens-/Layer-Muster, keine Norm-Werte); ohne Profil greift ein
Default aus ``door_patterns.DOOR_NAME_PATTERNS``.

Geometrie-Fallback-Kette pro Tür-Block:
  (a) Innen-ARC + Türblatt (Wiederverwendung ``door_arcs._match_leaf``)
      → volles ``opening`` (hinge, band_end) wie beim ARC-Detektor
  (b) Breite aus dem Blocknamen (``90x200`` → 900 mm) + Welt-Rotation
      → approximierte Öffnungs-Sehne (``approx_chord``)
  (c) nur Position (Insert-Punkt in Welt-mm)

Dieser Detektor speist NICHTS in die Raum-Rekonstruktion ein — Konsum durch
``auto_marker``/Placement ist ein Folge-Slice. Read-only-Diagnose + QC.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass

from parsers.door_arcs import (
    DOOR_RADIUS_MM,
    DOOR_SPAN_DEG,
    DoorArc,
    Seg,
    _arc_endpoints_mm,
    _insert_transform,
    _match_leaf,
)
from parsers.door_patterns import (
    DOOR_BLOCK_EXCLUDE_PATTERNS,
    DOOR_NAME_PATTERNS,
)

# Rekursions-Limit der INSERT-Auflösung: Tiefe 2 deckt die Rennweg-Konvention
# (Wall_N → Zargentür); tiefer verschachtelte Marker ("T Marker …" in den
# Zargentür-Blöcken) sind bewusst außerhalb.
MAX_NESTING_DEPTH = 2

# Breite aus Blocknamen: "90x200" (cm) bzw. "106x208". (?<!\d)/(?!\d) hält
# mm-Maße wie "RB_1680x2220" aus dem cm-Pfad raus (1680 → unplausibel → None).
_WIDTH_RE = re.compile(r"(?<!\d)(\d{2,4})\s*[xX]\s*\d{2,4}(?!\d)")


@dataclass(frozen=True)
class DoorBlockVocab:
    """Match-Vokabular des Block-Detektors (aus ``roles.doors`` oder Default).

    Regel: (Name matcht ``block_name_patterns`` ODER Layer matcht
    ``layer_patterns``) UND NICHT ``exclude_block_patterns``. Alle Muster
    sind Regexe, case-insensitiv per ``re.search``.
    """
    block_name_patterns: tuple[str, ...] = DOOR_NAME_PATTERNS
    layer_patterns: tuple[str, ...] = ()
    exclude_block_patterns: tuple[str, ...] = DOOR_BLOCK_EXCLUDE_PATTERNS
    nested_max_depth: int = MAX_NESTING_DEPTH

    def matches(self, block_name: str, layer: str) -> str | None:
        """Trefferart: ``"block_name"`` / ``"block_layer"`` / None."""
        if any(re.search(p, block_name, re.IGNORECASE)
               for p in self.exclude_block_patterns):
            return None
        if any(re.search(p, block_name, re.IGNORECASE)
               for p in self.block_name_patterns):
            return "block_name"
        if any(re.search(p, layer, re.IGNORECASE)
               for p in self.layer_patterns):
            return "block_layer"
        return None


@dataclass
class DoorBlock:
    position: tuple[float, float]        # Geometrie-Zentroid in Welt-mm
                                         # (Insert-Punkt nur bei leerem Block)
    rotation_deg: float                  # Welt-Rotation (aus tf-Richtung)
    width_mm: float | None               # Kette (a): ARC-Radius, (b): Name
    opening: tuple[tuple[float, float], tuple[float, float]] | None
    block_name: str
    layer: str
    depth: int                           # 1 = top-level, 2 = nested
    source: str                          # "block_name" | "block_layer"

    @property
    def anchor(self) -> tuple[float, float]:
        """Referenzpunkt für Dedup/QC: Öffnungs-Mitte, sonst Position."""
        if self.opening is not None:
            (x1, y1), (x2, y2) = self.opening
            return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)
        return self.position

    @property
    def approx_chord(self) -> Seg | None:
        """Öffnungs-Sehne: echt (a) oder aus Breite+Rotation approximiert (b)."""
        if self.opening is not None:
            return self.opening
        if self.width_mm is None:
            return None
        half = self.width_mm / 2.0
        rad = math.radians(self.rotation_deg)
        dx, dy = math.cos(rad) * half, math.sin(rad) * half
        px, py = self.position
        return ((px - dx, py - dy), (px + dx, py + dy))


def door_block_vocab_for(profile_id: str | None) -> DoorBlockVocab:
    """Vokabular aus ``roles.doors`` des Profils; None → Default-Vokabular."""
    if profile_id is None:
        return DoorBlockVocab()
    from parsers.layer_profiles import load_profile

    section = load_profile(profile_id).roles.get("doors") or {}
    names = tuple(section.get("block_name_patterns") or DOOR_NAME_PATTERNS)
    # block_layer_patterns übersteuert layer_patterns für den Block-Detektor
    # (generic_kg: dessen breites "T.{0,2}r" matcht auch "A_Sanitaer").
    layers = tuple(section.get("block_layer_patterns")
                   or section.get("layer_patterns") or ())
    excludes = tuple(section.get("exclude_block_patterns")
                     or DOOR_BLOCK_EXCLUDE_PATTERNS)
    depth = int(section.get("nested_max_depth", MAX_NESTING_DEPTH))
    return DoorBlockVocab(names, layers, excludes, depth)


def _block_base_point(doc, block_name: str) -> tuple[float, float]:
    """Basispunkt der Block-Definition (DXF: wird beim INSERT abgezogen).

    ArchiCAD-Exporte (Rennweg) zeichnen Block-Inhalte in Welt-Koordinaten
    und setzen base_point ≈ Insert-Punkt — ohne Abzug verdoppelt sich die
    Translation pro Ebene (Pre-Read-Befund: Tür-y bei 7.1e8 statt 3.6e8).
    """
    try:
        bp = doc.blocks[block_name].block.dxf.base_point
        return float(bp.x), float(bp.y)
    except Exception:
        return 0.0, 0.0


def _compose(parent_tf, parent_scale, ins, base: tuple[float, float]):
    """Block→Welt-Transform des INSERT hinter ``parent_tf`` komponieren.

    ``base`` = base_point der Block-Definition, auf die ``ins`` zeigt —
    Block-Koordinaten sind relativ dazu (world = tf(local − base)).
    """
    own_tf, own_scale = _insert_transform(ins)
    bx0, by0 = base

    def tf(bx: float, by: float) -> tuple[float, float]:
        p = own_tf(bx - bx0, by - by0)
        return parent_tf(*p) if parent_tf is not None else p

    return tf, (parent_scale * own_scale
                if parent_tf is not None else own_scale)


def _world_rotation_deg(tf) -> float:
    """Welt-Rotation aus dem tf-Richtungsvektor — Spiegelungs-robust
    (Winkel-Addition wäre bei negativem xscale falsch)."""
    ox, oy = tf(0.0, 0.0)
    ux, uy = tf(1.0, 0.0)
    return math.degrees(math.atan2(uy - oy, ux - ox)) % 360.0


def _geometry_centroid(doc, block_name: str, tf,
                       f: float) -> tuple[float, float] | None:
    """Zentroid der Block-Geometrie (LINE/LWPOLYLINE/ARC), world-mm.

    Nötig weil ArchiCAD-Exporte (Rennweg) Insert-Punkt ≡ base_point auf
    einen gemeinsamen Ursprungs-Anker setzen — die echte Tür-Lage steckt
    ausschließlich in der in-place gezeichneten Geometrie.
    """
    try:
        blk = doc.blocks[block_name]
    except Exception:
        return None
    xs: list[float] = []
    ys: list[float] = []
    for e in blk:
        t = e.dxftype()
        if t == "LINE":
            pts = [(e.dxf.start.x, e.dxf.start.y), (e.dxf.end.x, e.dxf.end.y)]
        elif t == "LWPOLYLINE":
            pts = [(p[0], p[1]) for p in e.get_points()]
        elif t == "ARC":
            pts = [(e.dxf.center.x, e.dxf.center.y)]
        else:
            continue
        for bx, by in pts:
            wx, wy = tf(bx, by)
            xs.append(wx)
            ys.append(wy)
    if not xs:
        return None
    return (sum(xs) / len(xs) * f, sum(ys) / len(ys) * f)


def _width_from_name(block_name: str) -> float | None:
    """``90x200`` → 900 mm (cm-Konvention); mm-Angaben direkt; sonst None."""
    m = _WIDTH_RE.search(block_name)
    if not m:
        return None
    n = float(m.group(1))
    lo, hi = DOOR_RADIUS_MM
    if lo <= n * 10.0 <= hi:
        return n * 10.0
    if lo <= n <= hi:
        return n
    return None


def _opening_from_block(doc, block_name: str, tf, scale: float,
                        f: float):
    """Kette (a): Innen-ARC + Türblatt im Block, world-transformiert.

    Gleiches Muster wie ``detect_door_arcs`` Pfad (b), nur mit komponiertem
    Transform. Rückgabe ``(hinge, band_end, radius_mm)`` oder None.
    """
    try:
        blk = doc.blocks[block_name]
    except Exception:
        return None
    blk_segs: list[Seg] | None = None
    for be in blk:
        if be.dxftype() != "ARC":
            continue
        r = float(be.dxf.radius) * scale * f
        span = (float(be.dxf.end_angle) - float(be.dxf.start_angle)) % 360.0
        if not (DOOR_RADIUS_MM[0] <= r <= DOOR_RADIUS_MM[1]
                and DOOR_SPAN_DEG[0] <= span <= DOOR_SPAN_DEG[1]):
            continue
        if blk_segs is None:
            blk_segs = []
            for le in blk:
                t = le.dxftype()
                if t == "LINE":
                    a = tf(le.dxf.start.x, le.dxf.start.y)
                    b = tf(le.dxf.end.x, le.dxf.end.y)
                    blk_segs.append(((a[0] * f, a[1] * f),
                                     (b[0] * f, b[1] * f)))
                elif t == "LWPOLYLINE":
                    pts = [tf(p[0], p[1]) for p in le.get_points()]
                    for i in range(len(pts) - 1):
                        blk_segs.append(((pts[i][0] * f, pts[i][1] * f),
                                         (pts[i + 1][0] * f,
                                          pts[i + 1][1] * f)))
        e0_b, e1_b = _arc_endpoints_mm(
            float(be.dxf.center.x), float(be.dxf.center.y),
            float(be.dxf.radius),
            float(be.dxf.start_angle), float(be.dxf.end_angle))
        hinge_w = tf(float(be.dxf.center.x), float(be.dxf.center.y))
        hinge = (hinge_w[0] * f, hinge_w[1] * f)
        e0_w, e1_w = tf(*e0_b), tf(*e1_b)
        e0 = (e0_w[0] * f, e0_w[1] * f)
        e1 = (e1_w[0] * f, e1_w[1] * f)
        band = _match_leaf(hinge, r, e0, e1, blk_segs)
        if band is not None:
            return hinge, band, r
    return None


def detect_door_blocks(doc, factor_to_mm: float,
                       vocab: DoorBlockVocab | None = None
                       ) -> list[DoorBlock]:
    """Alle Tür-Blöcke des Modelspace, bis ``nested_max_depth`` aufgelöst.

    Ein gematchter INSERT wird emittiert und NICHT weiter abgestiegen
    (vermeidet Doppelzählung innerer Marker-Blöcke); Nicht-Treffer werden
    bis zum Tiefenlimit rekursiv durchsucht.
    """
    v = vocab or DoorBlockVocab()
    f = float(factor_to_mm)
    out: list[DoorBlock] = []

    def visit(ins, parent_tf, parent_scale, depth: int) -> None:
        name = str(ins.dxf.name or "")
        layer = str(ins.dxf.layer or "")
        hit = v.matches(name, layer)
        if hit is not None:
            tf, scale = _compose(parent_tf, parent_scale, ins,
                                 _block_base_point(doc, name))
            position = _geometry_centroid(doc, name, tf, f)
            if position is None:
                pos_w = (parent_tf(ins.dxf.insert.x, ins.dxf.insert.y)
                         if parent_tf is not None
                         else (float(ins.dxf.insert.x),
                               float(ins.dxf.insert.y)))
                position = (pos_w[0] * f, pos_w[1] * f)
            rotation = _world_rotation_deg(tf)
            opening = None
            width = None
            found = _opening_from_block(doc, name, tf, scale, f)
            if found is not None:
                hinge, band, r = found
                opening = (hinge, band)
                width = r
            else:
                width = _width_from_name(name)
            out.append(DoorBlock(position, rotation, width, opening,
                                 name, layer, depth, hit))
            return
        if depth >= v.nested_max_depth:
            return
        try:
            blk = doc.blocks[name]
        except Exception:
            return
        tf, scale = _compose(parent_tf, parent_scale, ins,
                             _block_base_point(doc, name))
        for child in blk:
            if child.dxftype() == "INSERT":
                visit(child, tf, scale, depth + 1)

    for ins in doc.modelspace():
        if ins.dxftype() == "INSERT":
            visit(ins, None, 1.0, 1)
    return out


def dedupe_against_arcs(blocks: list[DoorBlock], arcs: list[DoorArc],
                        tol_mm: float = 600.0) -> list[DoorBlock]:
    """Block-Türen entfernen, die der ARC-Detektor schon liefert (ARC ist
    geometrisch präziser). Nähe über anchor ↔ opening_mid/hinge."""
    if not arcs:
        return list(blocks)
    keep: list[DoorBlock] = []
    for b in blocks:
        ax, ay = b.anchor
        near = any(
            math.hypot(ax - px, ay - py) <= tol_mm
            for a in arcs
            for px, py in (a.opening_mid, a.hinge)
        )
        if not near:
            keep.append(b)
    return keep
