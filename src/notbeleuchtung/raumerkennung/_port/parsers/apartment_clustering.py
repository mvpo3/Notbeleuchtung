"""apartment_clustering.py — group rooms into apartments via doors.

Slice 9.1.2: replaces broken 'nearest 00-top' room assignment with
proper graph-based clustering. The 00-top blocks are door-plates
(paired in twos), not unit centroids.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Optional


@dataclass
class Apartment:
    apartment_id: str
    room_ids: list[int]
    is_communal: bool = False
    estimated_top: Optional[str] = None
    centroid_mm: Optional[tuple[float, float]] = None
    decision_source: Optional[str] = None
    # Slice 1.8.0: Position des 00-top-Türschild-Ankers, der diese Wohnung
    # geseedet hat (mm). Stabile Identität für Bauteil-Zuordnung — dasselbe
    # physische INSERT wie der Inventur-Stempel in building_units.
    anchor_mm: Optional[tuple[float, float]] = None


def _is_door_on_room_edge(door_pos: tuple[float, float],
                          polygon: list[tuple[float, float]],
                          tol_mm: float = 1500.0) -> bool:
    """True if door position lies on or near any edge of polygon."""
    if not polygon or len(polygon) < 2:
        return False
    px, py = door_pos
    n = len(polygon)
    for i in range(n):
        a = polygon[i]
        b = polygon[(i + 1) % n]
        ax, ay = a
        bx, by = b
        dx, dy = bx - ax, by - ay
        length_sq = dx * dx + dy * dy
        if length_sq < 1e-9:
            continue
        t = ((px - ax) * dx + (py - ay) * dy) / length_sq
        t = max(0.0, min(1.0, t))
        nearest_x = ax + t * dx
        nearest_y = ay + t * dy
        dist = math.hypot(px - nearest_x, py - nearest_y)
        if dist <= tol_mm:
            return True
    return False


COMMUNAL_NAME_PATTERNS = (
    "STGH", "STIEGENHAUS", "PODEST", "AUFZUG", "FLACHDACH",
    "TOP ", "STOCK", "TERRASSE",
)


def _is_communal_by_name(name: str) -> bool:
    upper = (name or "").upper()
    return any(p in upper for p in COMMUNAL_NAME_PATTERNS)


# Slice 18.20.0 — rooms that belong to NO residential unit: outdoor site areas,
# shared building-service rooms, commercial units. They had no communal-by-name
# marker, so nearest-anchor assignment dumped them into the closest unit (EG
# A_1 collapsed to 40 rooms). Bucketing them as communal makes the placement
# consumer (check_placement: not is_communal AND _has_vr) skip them. Unit-owned
# outdoor (BALKON/LOGGIA) is deliberately NOT here — it stays with its unit.
NON_UNIT_NAME_PATTERNS = (
    "GEHWEG", "VORPLATZ", "KLEINKINDER", "SPIELPLATZ", "STAUDE",
    "GRÄSER", "GRAESER", "BLÜHPFLANZ", "BLUEHPFLANZ", "GARAGENRAMPE",
    "EIGENGARTEN", "INNENHOF", "MÜLL", "MUELL", "FAHRRAD", "KIWA",
    "TECHNIK", "GESCHÄFTSLOKAL", "GESCHAEFTSLOKAL", "BRE ABLUFT",
)


def _is_non_unit_by_name(name: str) -> bool:
    upper = (name or "").upper()
    return any(p in upper for p in NON_UNIT_NAME_PATTERNS)


# ── Slice 16.1.6: floor-filter via finished_floor_label ────────
_FOK_RE = re.compile(r"[+-]?\d+[.,]\d+")


def _parse_fok_m(label: str) -> Optional[float]:
    """Extract the finished-floor level (metres) from a FOK label.

    Labels read e.g. ``"FOK WOHNUNG = +12.64"`` / ``"FOK STGH = +12.66"``.
    The WOHNUNG/STGH word is the nearest height-block's caption, NOT a role
    marker (Slice 16.1.6 Hard-Stop 2) — only the numeric value is used.
    """
    if not label:
        return None
    m = _FOK_RE.search(label)
    if not m:
        return None
    return float(m.group(0).replace(",", "."))


def select_target_tops(tops: list, target_fok: Optional[float] = None,
                       tol_m: float = 0.05) -> tuple[Optional[float], list]:
    """Pick the tops[] anchors that sit on the target finished-floor level.

    ``target_fok`` defaults to the modal FOK value across ``tops`` (rounded to
    the centimetre). Anchors within ``tol_m`` of it are kept — so a noisy
    "FOK STGH = +12.66" joins the +12.64 cluster, while a +10.54 anchor of a
    different storey is dropped. Anchors whose label has no parseable number
    are excluded from the target set.
    """
    parsed = [(_parse_fok_m(t.finished_floor_label), t) for t in tops]
    parsed = [(v, t) for v, t in parsed if v is not None]
    if not parsed:
        return None, []
    if target_fok is None:
        counts = Counter(round(v, 2) for v, _ in parsed)
        target_fok = counts.most_common(1)[0][0]
    target = [t for v, t in parsed if abs(v - target_fok) <= tol_m]
    return target_fok, target


def _all_tops_without_parseable_fok(tops: list) -> bool:
    """True when the DXF has TOP anchors but none carries a usable FOK label."""
    return bool(tops) and all(
        _parse_fok_m(getattr(t, "finished_floor_label", "")) is None
        for t in tops
    )


# Slice C1: room names that are ALWAYS apartment-internal — never a communal
# hub. A room with such a name that tripped ONLY the door-count communal rule
# (e.g. a Vorraum wired to 6+ doors of its OWN unit) is reattached to the
# apartment it shares the most doors with (no BFS merge).
_REATTACHABLE_ROOM_NAMES = frozenset({
    "VR", "VORRAUM", "BAD", "WC", "ZIMMER", "KÜCHE", "KUECHE",
    "WOHNZIMMER", "WOHNKÜCHE", "ABSTELLRAUM", "ASR", "LOGGIA", "BALKON",
})


_DOOR_REATTACH_ROOM_NAMES = frozenset({
    "GANG", "FLUR", "CORRIDOR", "WC", "ASR", "ABSTELLRAUM",
})


def _norm_room_name(name: str) -> str:
    return (name or "").strip().upper()


_WET_DOOR_RE = re.compile(r"(^|[^a-z])wet([^a-z]|$)")


def _is_unit_entrance_door(door) -> bool:
    """Wohnungseingangstür (WET) — trennt per Definition Wohnung von
    Allgemeinbereich und darf daher NIE als Cluster-verbindende Kante zählen.

    Slice 2.9.0: seit dem 2.6.1-Tür-Anker-Fix schließen die Raum-Polygone
    an der WET sauber → der Allgemein-GANG vor der Wohnung verband sich über
    die WET-Kante mit dem VR (1.OG/2.OG: COMM_GANG in A_7/A_11 geleakt).
    """
    text = str(getattr(door, "block_name", None)
               or getattr(door, "source_ref", None) or "").lower()
    return bool(_WET_DOOR_RE.search(text))


def _room_has_only_wet_doors(room) -> bool:
    """GANG vor den Wohnungstüren: alle Türen des Raums sind WETs.

    So ein Raum ist Allgemeinfläche (Zugang NUR über Wohnungseingangstüren
    fremder Einheiten) — nie Teil einer Wohnung (Slice 2.9.0).
    """
    doors = getattr(room, "doors", []) or []
    return bool(doors) and all(_is_unit_entrance_door(d) for d in doors)


def _door_pos(door) -> Optional[tuple[float, float]]:
    pos = getattr(door, "position_mm", None)
    if not pos or len(pos) < 2:
        return None
    return (float(pos[0]), float(pos[1]))


def _rooms_share_door(room_a, room_b, tol_mm: float = 350.0) -> bool:
    """True when two parsed rooms reference the same architectural door."""
    doors_a = getattr(room_a, "doors", []) or []
    doors_b = getattr(room_b, "doors", []) or []
    for da in doors_a:
        pa = _door_pos(da)
        if pa is None:
            continue
        for db in doors_b:
            pb = _door_pos(db)
            if pb is None:
                continue
            if math.hypot(pa[0] - pb[0], pa[1] - pb[1]) <= tol_mm:
                return True
    return False


def _reattach_ambiguous_service_rooms_by_doors(
        rooms: list,
        apt_by_top: dict[str, Apartment]) -> None:
    """Move ambiguous GANG/WC/ASR rooms to their door-connected unit."""
    room_top: dict[int, str] = {
        rid: top
        for top, apt in apt_by_top.items()
        for rid in apt.room_ids
    }
    candidate_ids = {
        id(r) for r in rooms
        if _norm_room_name(r.anchor.name) in _DOOR_REATTACH_ROOM_NAMES
        and getattr(r, "review_flag", False)
        and "ambiguous nearest top" in (getattr(r, "review_reason", "") or "")
    }
    if not candidate_ids:
        return

    resolved_candidates: set[int] = set()
    for _ in range(4):
        changed = False
        for room in rooms:
            rid = id(room)
            if rid not in candidate_ids or rid not in room_top:
                continue
            votes: Counter[str] = Counter()
            for other in rooms:
                oid = id(other)
                if oid == rid or oid not in room_top:
                    continue
                if oid in candidate_ids and oid not in resolved_candidates:
                    continue
                if _rooms_share_door(room, other):
                    votes[room_top[oid]] += 1
            if not votes:
                continue
            best_top, best_count = votes.most_common(1)[0]
            if len(votes) > 1 and votes.most_common(2)[1][1] == best_count:
                continue
            current_top = room_top[rid]
            resolved_candidates.add(rid)
            if best_top == current_top:
                continue

            old_apt = apt_by_top.get(current_top)
            new_apt = apt_by_top.get(best_top)
            if old_apt is None or new_apt is None:
                continue
            old_apt.room_ids = [x for x in old_apt.room_ids if x != rid]
            if rid not in new_apt.room_ids:
                new_apt.room_ids.append(rid)
            room_top[rid] = best_top
            room.review_flag = True
            room.review_reason = (
                f"{room.review_reason}; door-connected service-room reattach "
                f"{current_top}->{best_top}"
            )
            changed = True
        if not changed:
            break


def cluster_apartments(rooms: list, doors: list,
                       communal_area_threshold_m2: float = 30.0,
                       communal_door_count_threshold: int = 6,
                       door_edge_tol_mm: float = 1500.0
                       ) -> list[Apartment]:
    """Cluster rooms into apartments via door-connection graph."""
    adj: dict[int, set[int]] = {id(r): set() for r in rooms}
    door_count: dict[int, int] = {id(r): 0 for r in rooms}

    for door in doors:
        rooms_on_door = []
        for r in rooms:
            if r.polygon_mm and _is_door_on_room_edge(
                    door.position_mm, r.polygon_mm, tol_mm=door_edge_tol_mm):
                rooms_on_door.append(r)

        for r in rooms_on_door:
            door_count[id(r)] += 1

        # WET verbindet nie zwei Räume EINER Wohnung — keine Graph-Kante
        # (door_count zählt sie weiter, Slice 2.9.0).
        if _is_unit_entrance_door(door):
            continue

        for i in range(len(rooms_on_door)):
            for j in range(i + 1, len(rooms_on_door)):
                a, b = rooms_on_door[i], rooms_on_door[j]
                adj[id(a)].add(id(b))
                adj[id(b)].add(id(a))

    communal_room_ids: set[int] = set()
    doorcount_communal_ids: set[int] = set()
    for r in rooms:
        if _is_communal_by_name(r.anchor.name):
            communal_room_ids.add(id(r))
        elif r.anchor.area_m2 >= communal_area_threshold_m2:
            communal_room_ids.add(id(r))
        elif door_count[id(r)] >= communal_door_count_threshold:
            communal_room_ids.add(id(r))
            doorcount_communal_ids.add(id(r))
        elif (_norm_room_name(r.anchor.name) == "GANG"
                and _room_has_only_wet_doors(r)):
            # Allgemein-Gang vor den Wohnungseingangstüren (Slice 2.9.0).
            communal_room_ids.add(id(r))

    visited: set[int] = set()
    apartments: list[Apartment] = []
    apt_counter = 0

    for r in rooms:
        rid = id(r)
        if rid in visited or rid in communal_room_ids:
            continue
        component: list[int] = []
        queue = [rid]
        while queue:
            cur = queue.pop(0)
            if cur in visited or cur in communal_room_ids:
                continue
            visited.add(cur)
            component.append(cur)
            for neighbor in adj[cur]:
                if neighbor not in visited and neighbor not in communal_room_ids:
                    queue.append(neighbor)

        if component:
            apt_counter += 1
            apartments.append(Apartment(
                apartment_id=f"A{apt_counter}",
                room_ids=component,
                is_communal=False,
            ))

    # Slice C1: reattach apartment-internal hub-rooms (typ. Vorraum) that
    # tripped the door-count communal rule by connecting 6+ doors of THEIR
    # OWN unit. Assign each to the non-communal apartment it shares the most
    # doors with. The BFS components above stay intact (no apartment merge) —
    # only the misclassified room moves out of the communal bucket. Fixes
    # e.g. TOP 24's Vorraum landing in COMM_VR instead of its apartment.
    apt_index_of_room = {
        rid: i for i, apt in enumerate(apartments) for rid in apt.room_ids
    }
    for r in rooms:
        rid = id(r)
        if rid not in doorcount_communal_ids:
            continue
        if r.anchor.name.strip().upper() not in _REATTACHABLE_ROOM_NAMES:
            continue
        share = Counter(
            apt_index_of_room[nb] for nb in adj[rid]
            if nb in apt_index_of_room
        )
        if not share:
            continue
        best_i = share.most_common(1)[0][0]
        apartments[best_i].room_ids.append(rid)
        communal_room_ids.discard(rid)

    for r in rooms:
        rid = id(r)
        if rid in communal_room_ids and rid not in visited:
            visited.add(rid)
            short_name = r.anchor.name[:10].strip().replace(" ", "_")
            apartments.append(Apartment(
                apartment_id=f"COMM_{short_name}",
                room_ids=[rid],
                is_communal=True,
            ))

    return apartments


def assign_apartment_centroids(apartments: list[Apartment], rooms: list) -> None:
    """Compute centroid of each apartment from its rooms' anchors."""
    rooms_by_id = {id(r): r for r in rooms}
    for apt in apartments:
        xs, ys = [], []
        for rid in apt.room_ids:
            r = rooms_by_id.get(rid)
            if r:
                xs.append(r.anchor.anchor_x_mm)
                ys.append(r.anchor.anchor_y_mm)
        if xs:
            apt.centroid_mm = (sum(xs) / len(xs), sum(ys) / len(ys))


def assign_apartments_to_top(apartments: list[Apartment],
                             top_anchors: list) -> None:
    """For each non-communal apartment, find nearest 00-top anchor."""
    if not top_anchors:
        return
    for apt in apartments:
        if apt.is_communal or apt.centroid_mm is None:
            continue
        cx, cy = apt.centroid_mm
        best = min(top_anchors, key=lambda t: math.hypot(
            cx - t.anchor_mm[0], cy - t.anchor_mm[1]))
        apt.estimated_top = best.top_id


def _partition_anchors_xy(tops: list, n: int) -> list[list]:
    """Deterministische räumliche k-Partition der TOP-Anker (k-means,
    Seeds = fernstes Paar). Für Bauteile auf verschiedenen FOK-Niveaus."""
    if n <= 1 or len(tops) <= 1:
        return [list(tops)]
    if n != 2:
        raise ValueError(f"_partition_anchors_xy supports 1-2 Bauteile, got {n}")

    def d2(a, b) -> float:
        return ((a.anchor_mm[0] - b.anchor_mm[0]) ** 2
                + (a.anchor_mm[1] - b.anchor_mm[1]) ** 2)

    pairs = [(i, j) for i in range(len(tops)) for j in range(i + 1, len(tops))]
    si, sj = max(pairs, key=lambda p: d2(tops[p[0]], tops[p[1]]))
    centroids = [tops[si].anchor_mm, tops[sj].anchor_mm]
    assign = [0] * len(tops)
    for _ in range(20):
        prev = list(assign)
        for i, t in enumerate(tops):
            dists = [(t.anchor_mm[0] - cx) ** 2 + (t.anchor_mm[1] - cy) ** 2
                     for cx, cy in centroids]
            assign[i] = dists.index(min(dists))
        for k in range(2):
            members = [t for t, a in zip(tops, assign) if a == k]
            if members:
                centroids[k] = (
                    sum(t.anchor_mm[0] for t in members) / len(members),
                    sum(t.anchor_mm[1] for t in members) / len(members))
        if assign == prev:
            break
    groups: list[list] = [[], []]
    for t, a in zip(tops, assign):
        groups[a].append(t)
    return [g for g in groups if g]


# ── Slice 1.4.0: Area-Constrained Boundary-Room-Refinement ─────
# Nearest-Anchor-Seeds sind an Wohnungsgrenzen unscharf (Raum liegt näher am
# Nachbar-Türschild). Der Architekten-Wohnflächen-Stempel pro TOP ist die
# Ground-Truth: Grenzräume werden nur umgehängt, wenn Tür-/Polygon-Evidenz
# zur Zielwohnung existiert UND sich die Flächen-Deltas BEIDER Wohnungen
# strikt verbessern. Centgenaue Zuordnungen sind damit Fixpunkt.

_NEVER_MOVE_ROOM_NAMES = frozenset({"VR", "VORRAUM"})
_PARALLEL_SIN_MAX = 0.17          # ≈10° — Kanten gelten als parallel
_EDGE_LATERAL_TOL_MM = 300.0      # Querabstand für "gleiche Wand"
_SHARED_EDGE_MIN_MM = 800.0       # ab dieser Kontaktlänge adjazent


def _room_polygon_shared_edge_mm(room_a, room_b) -> float:
    """Gemeinsame (kollineare, nahe) Polygon-Kantenlänge zweier Räume in mm."""
    pa = getattr(room_a, "polygon_mm", None)
    pb = getattr(room_b, "polygon_mm", None)
    if (not pa or not pb
            or getattr(room_a, "polygon_source", "") == "anchor_only"
            or getattr(room_b, "polygon_source", "") == "anchor_only"):
        return 0.0
    total = 0.0
    na, nb = len(pa), len(pb)
    for i in range(na):
        ax, ay = pa[i]
        bx, by = pa[(i + 1) % na]
        dax, day = bx - ax, by - ay
        la = math.hypot(dax, day)
        if la < 1e-6:
            continue
        ux, uy = dax / la, day / la
        for j in range(nb):
            qx, qy = pb[j]
            rx, ry = pb[(j + 1) % nb]
            dbx, dby = rx - qx, ry - qy
            lb = math.hypot(dbx, dby)
            if lb < 1e-6:
                continue
            cross = abs(ux * dby - uy * dbx) / lb
            if cross > _PARALLEL_SIN_MAX:
                continue
            lateral = abs((qx - ax) * uy - (qy - ay) * ux)
            if lateral > _EDGE_LATERAL_TOL_MM:
                continue
            t1 = (qx - ax) * ux + (qy - ay) * uy
            t2 = (rx - ax) * ux + (ry - ay) * uy
            lo, hi = min(t1, t2), max(t1, t2)
            total += max(0.0, min(hi, la) - max(lo, 0.0))
    return total


def _refine_boundary_rooms_by_area(
        rooms_by_id: dict[int, object],
        units: list[Apartment],
        target_area: dict[str, float],
        outdoor_patterns: tuple[str, ...] = (),
        tol_m2: float = 2.0,
        max_moves_per_unit: int = 3,
        communal_rooms: Optional[list] = None) -> None:
    """Grenzräume greedy umhängen bis Fixpunkt (in-place auf room_ids)."""
    def is_outdoor(name: str) -> bool:
        up = (name or "").upper()
        return any(p in up for p in outdoor_patterns)

    def inner_sum(apt: Apartment) -> float:
        s = 0.0
        for rid in apt.room_ids:
            r = rooms_by_id.get(rid)
            if r is not None and not is_outdoor(r.anchor.name):
                s += r.anchor.area_m2 or 0.0
        return s

    sums = {a.apartment_id: inner_sum(a) for a in units}
    moves: Counter[str] = Counter()

    def evidence(room, target_apt: Apartment) -> Optional[str]:
        for rid in target_apt.room_ids:
            other = rooms_by_id.get(rid)
            if other is None:
                continue
            if _rooms_share_door(room, other):
                return "door"
            if _room_polygon_shared_edge_mm(room, other) >= _SHARED_EDGE_MIN_MM:
                return "edge"
        return None

    def movable(apt: Apartment):
        for rid in apt.room_ids:
            room = rooms_by_id.get(rid)
            if room is None:
                continue
            name = _norm_room_name(room.anchor.name)
            if name in _NEVER_MOVE_ROOM_NAMES or is_outdoor(name):
                continue
            area = room.anchor.area_m2 or 0.0
            if area > 0.0:
                yield rid, room, area

    def apply_transfer(src: Apartment, dst: Apartment, rid: int, room,
                       ev: str) -> None:
        src.room_ids.remove(rid)
        dst.room_ids.append(rid)
        area = room.anchor.area_m2 or 0.0
        sums[src.apartment_id] -= area
        sums[dst.apartment_id] += area
        room.review_flag = True
        prev = getattr(room, "review_reason", "") or ""
        room.review_reason = (
            f"{prev}; area-constrained reattach ({ev}) "
            f"{src.apartment_id}->{dst.apartment_id}").lstrip("; ")

    for _ in range(2 * len(rooms_by_id) or 1):
        best = None  # (sort_key, kind, payload)
        for src in units:
            t_src = target_area.get(src.apartment_id)
            if t_src is None or moves[src.apartment_id] >= max_moves_per_unit:
                continue
            d_src = sums[src.apartment_id] - t_src
            for dst in units:
                if dst is src:
                    continue
                t_dst = target_area.get(dst.apartment_id)
                if (t_dst is None
                        or moves[dst.apartment_id] >= max_moves_per_unit):
                    continue
                d_dst = sums[dst.apartment_id] - t_dst
                if abs(d_src) <= tol_m2 and abs(d_dst) <= tol_m2:
                    continue
                # Einzel-Move src → dst
                for rid, room, area in movable(src):
                    new_src = abs(d_src - area)
                    new_dst = abs(d_dst + area)
                    if not (new_src < abs(d_src) and new_dst < abs(d_dst)):
                        continue
                    ev = evidence(room, dst)
                    if ev is None:
                        continue
                    reduction = (abs(d_src) - new_src) + (abs(d_dst) - new_dst)
                    key = (-reduction, 0, src.apartment_id, dst.apartment_id,
                           room.anchor.name, area)
                    if best is None or key < best[0]:
                        best = (key, "move", (src, dst, rid, room, ev))
                # Slice 1.6.0: Paar-Swap src.r ↔ dst.s — nötig wenn zwei
                # Grenzräume wechselseitig falsch sitzen; Einzel-Moves können
                # dann nie beide Deltas gleichzeitig verbessern.
                for rid_r, room_r, area_r in movable(src):
                    for rid_s, room_s, area_s in movable(dst):
                        diff = area_r - area_s
                        new_src = abs(d_src - diff)
                        new_dst = abs(d_dst + diff)
                        if not (new_src < abs(d_src) and new_dst < abs(d_dst)):
                            continue
                        ev_r = evidence(room_r, dst)
                        ev_s = evidence(room_s, src)
                        if ev_r is None or ev_s is None:
                            continue
                        reduction = ((abs(d_src) - new_src)
                                     + (abs(d_dst) - new_dst))
                        key = (-reduction, 1, src.apartment_id,
                               dst.apartment_id, room_r.anchor.name,
                               room_s.anchor.name)
                        if best is None or key < best[0]:
                            best = (key, "swap",
                                    (src, dst, rid_r, room_r, ev_r,
                                     rid_s, room_s, ev_s))
            # Slice 1.6.0/1.9.0: Eviction — Allgemein-Raum wurde der Wohnung
            # zugeschlagen (Innen-Summe > Stempel). Evidenz, dass der Raum
            # Erschließung/Allgemein ist: (a) Tür-/Kanten-Kontakt zu einem
            # Allgemeinraum ODER (b) Tür-Verbindungen zu ≥2 FREMDEN
            # Wohnungen (Laubengang erschließt mehrere Units — ein privater
            # Gang verbindet nur eigene Räume).
            if communal_rooms is not None and d_src > tol_m2:
                for rid, room, area in movable(src):
                    new_src = abs(d_src - area)
                    if new_src >= abs(d_src):
                        continue
                    ev = None
                    for cr in communal_rooms:
                        if _rooms_share_door(room, cr):
                            ev = "door"
                            break
                        if (_room_polygon_shared_edge_mm(room, cr)
                                >= _SHARED_EDGE_MIN_MM):
                            ev = "edge"
                            break
                    if ev is None:
                        foreign = set()
                        for other in units:
                            if other is src:
                                continue
                            for orid in other.room_ids:
                                oroom = rooms_by_id.get(orid)
                                if oroom is not None and _rooms_share_door(
                                        room, oroom):
                                    foreign.add(other.apartment_id)
                                    break
                            if len(foreign) >= 2:
                                ev = "serves_multiple_units"
                                break
                    if ev is None:
                        continue
                    reduction = abs(d_src) - new_src
                    key = (-reduction, 2, src.apartment_id, "",
                           room.anchor.name, area)
                    if best is None or key < best[0]:
                        best = (key, "evict", (src, rid, room, ev))
        if best is None:
            break
        _, kind, payload = best
        if kind == "move":
            src, dst, rid, room, ev = payload
            apply_transfer(src, dst, rid, room, ev)
            touched = (src, dst)
        elif kind == "swap":
            src, dst, rid_r, room_r, ev_r, rid_s, room_s, ev_s = payload
            apply_transfer(src, dst, rid_r, room_r, f"swap:{ev_r}")
            apply_transfer(dst, src, rid_s, room_s, f"swap:{ev_s}")
            touched = (src, dst)
        else:  # evict → Gemeinschafts-Bucket (communal_rooms-Liste)
            src, rid, room, ev = payload
            src.room_ids.remove(rid)
            sums[src.apartment_id] -= room.anchor.area_m2 or 0.0
            communal_rooms.append(room)
            room.review_flag = True
            prev = getattr(room, "review_reason", "") or ""
            room.review_reason = (
                f"{prev}; area-constrained evict ({ev}) "
                f"{src.apartment_id}->communal").lstrip("; ")
            touched = (src,)
        for apt in touched:
            moves[apt.apartment_id] += 1
            if apt.decision_source and "+area_refine" not in apt.decision_source:
                apt.decision_source += "+area_refine"

    # ── Slice 1.17.0: Ketten-Reassignment nach dem Greedy-Fixpunkt ──
    # Befund 3.OG Mollgasse (16→17→18+19→20): jede Wohnung gibt Grenzräume an
    # die nächste weiter — den Überschuss hat erst das KETTEN-Ende. Pairwise
    # („beide Deltas verbessern") ist dort ein lokales Minimum, weil der
    # erste Einzel-Move immer eine Seite verschlechtert. DFS vom Defizit-
    # Apartment: pro Hop eine Raum-Teilmenge (≤2) des Gebers mit Tür-/
    # Kanten-Evidenz zum Empfänger und Summe ≈ Bedarf; der Geber wird selbst
    # Defizit und rekursiert. Transaktional: angewandt wird nur eine Kette,
    # die ALLE Beteiligten innerhalb chain_tol schließt — offene Ketten
    # (z. B. 2.OG/EG mit Stempel-Varianten-Verdacht) bewegen NICHTS.
    # Eigenes Ketten-Budget statt max_moves_per_unit: der Greedy-Counter ist
    # nach Swaps/Moves oft aufgebraucht (3.OG-Befund), Ketten sind aber
    # transaktional + exakt — jede Wohnung darf an EINER Kette teilnehmen.
    #
    # Bundle-Regel (EG-Befund MOLL 2/3): ein Transfer darf bis zu 4 Räume
    # umfassen, wenn das Bündel intern über Tür-/Kanten-Kontakt zusammen-
    # hängt und mindestens ein Bündel-Raum den Empfänger berührt — Innen-
    # räume (BAD hinter GANG) wandern mit ihrem Erschließungs-Cluster.
    #
    # Communal-Terminal: die Kette darf mit einem Raum aus dem Gemein-
    # schafts-Bucket schließen (Slice-1.9.0-Eviction wirft bei Ketten-
    # Fehlzuordnung auch legitime Wohnräume hinaus — EG: WOHNKÜCHE 35.90).
    # NUR name-neutrale Innenräume (kein STGH/GEHWEG/…, kein Outdoor).
    chain_tol = 0.5
    max_chain_hops = 4
    max_bundle = 4
    chain_used: set[str] = set()
    _pair_ev: dict[tuple[int, int], bool] = {}

    def rooms_touch(a, b) -> bool:
        key = (min(id(a), id(b)), max(id(a), id(b)))
        hit = _pair_ev.get(key)
        if hit is None:
            hit = bool(_rooms_share_door(a, b)
                       or _room_polygon_shared_edge_mm(a, b)
                       >= _SHARED_EDGE_MIN_MM)
            _pair_ev[key] = hit
        return hit

    def bundle_connected(sel_rooms: list, receiver: Apartment) -> bool:
        """Jeder Bündel-Raum hängt (transitiv) an einem Empfänger-Kontakt."""
        seeds = [r for r in sel_rooms if evidence(r, receiver) is not None]
        if not seeds:
            return False
        connected = set(id(r) for r in seeds)
        grew = True
        while grew:
            grew = False
            for r in sel_rooms:
                if id(r) in connected:
                    continue
                if any(rooms_touch(r, o) for o in sel_rooms
                       if id(o) in connected):
                    connected.add(id(r))
                    grew = True
        return len(connected) == len(sel_rooms)

    def chain_subsets(giver: Apartment, receiver: Apartment, need: float):
        from itertools import combinations

        cands = list(movable(giver))
        subs = []
        for size in range(1, min(max_bundle, len(cands)) + 1):
            for combo in combinations(cands, size):
                s = sum(a for _, _, a in combo)
                if abs(s - need) > chain_tol:
                    continue
                sel = [(rid, room) for rid, room, _ in combo]
                if not bundle_connected([r for _, r in sel], receiver):
                    continue
                subs.append((sel, s))
        subs.sort(key=lambda t: (abs(t[1] - need), len(t[0]),
                                 tuple(r.anchor.name for _, r in t[0])))
        return subs

    def communal_terminal(receiver: Apartment, need: float):
        """Ketten-Abschluss aus dem Gemeinschafts-Bucket (nur name-neutral)."""
        if not communal_rooms:
            return None
        from itertools import combinations

        cands = [
            r for r in communal_rooms
            if (r.anchor.area_m2 or 0.0) > 0.0
            and not is_outdoor(r.anchor.name)
            and _norm_room_name(r.anchor.name) not in _NEVER_MOVE_ROOM_NAMES
            and not _is_communal_by_name(r.anchor.name)
            and not _is_non_unit_by_name(r.anchor.name)
        ]
        subs = []
        for size in (1, 2):
            for combo in combinations(cands, size):
                s = sum(r.anchor.area_m2 or 0.0 for r in combo)
                if abs(s - need) > chain_tol:
                    continue
                if not bundle_connected(list(combo), receiver):
                    continue
                subs.append((list(combo), s))
        if not subs:
            return None
        subs.sort(key=lambda t: (abs(t[1] - need), len(t[0]),
                                 tuple(r.anchor.name for r in t[0])))
        return subs[0][0]

    def find_chain(receiver: Apartment, need: float,
                   visited: frozenset, depth: int):
        if depth > max_chain_hops:
            return None
        for giver in sorted(units, key=lambda a: a.apartment_id):
            if (giver is receiver or giver.apartment_id in visited
                    or giver.apartment_id in chain_used):
                continue
            t_g = target_area.get(giver.apartment_id)
            if t_g is None:
                continue
            d_g = sums[giver.apartment_id] - t_g
            for sel, s in chain_subsets(giver, receiver, need):
                rest = d_g - s
                if abs(rest) <= chain_tol:
                    return [(giver, receiver, sel)]
                if rest < -chain_tol:
                    tail = find_chain(giver, s - d_g,
                                      visited | {giver.apartment_id},
                                      depth + 1)
                    if tail is not None:
                        return [(giver, receiver, sel)] + tail
        comm = communal_terminal(receiver, need)
        if comm is not None:
            return [(None, receiver, [(None, r) for r in comm])]
        return None

    for receiver in sorted(units, key=lambda a: a.apartment_id):
        t_r = target_area.get(receiver.apartment_id)
        if t_r is None or receiver.apartment_id in chain_used:
            continue
        d_r = sums[receiver.apartment_id] - t_r
        if d_r >= -tol_m2:
            continue
        chain = find_chain(receiver, -d_r,
                           frozenset({receiver.apartment_id}), 1)
        if not chain:
            continue
        for giver, recv, sel in chain:
            if giver is None:
                for _, room in sel:
                    communal_rooms.remove(room)
                    recv.room_ids.append(id(room))
                    sums[recv.apartment_id] += room.anchor.area_m2 or 0.0
                    room.review_flag = True
                    prev = getattr(room, "review_reason", "") or ""
                    room.review_reason = (
                        f"{prev}; area-constrained reattach (chain:communal) "
                        f"communal->{recv.apartment_id}").lstrip("; ")
            else:
                for rid, room in sel:
                    ev = evidence(room, recv) or "bundle"
                    apply_transfer(giver, recv, rid, room, f"chain:{ev}")
                chain_used.add(giver.apartment_id)
            chain_used.add(recv.apartment_id)
            for apt in ((giver, recv) if giver is not None else (recv,)):
                if (apt.decision_source
                        and "+area_refine" not in apt.decision_source):
                    apt.decision_source += "+area_refine"


def _target_areas_from_stamps(area_stamps: list, tops: list,
                              apt_by_anchor: dict[int, Apartment]
                              ) -> dict[str, float]:
    """Wohnflächen-Stempel → Ziel-Fläche pro apartment_id (SW > Standard)."""
    from parsers.building_units import parse_top_ids

    anchor_ids = {
        id(t): parse_top_ids(f"TOP {t.top_id}") for t in tops
        if id(t) in apt_by_anchor
    }
    chosen: dict[int, object] = {}
    for st in area_stamps:
        st_ids = set(getattr(st, "top_ids", ()) or ())
        if not st_ids:
            continue
        best_aid = None
        best_d = None
        for t in tops:
            aid = id(t)
            if aid not in anchor_ids or not (st_ids & set(anchor_ids[aid])):
                continue
            d = ((t.anchor_mm[0] - st.x_mm) ** 2
                 + (t.anchor_mm[1] - st.y_mm) ** 2)
            if best_d is None or d < best_d:
                best_d, best_aid = d, aid
        if best_aid is None:
            continue
        cur = chosen.get(best_aid)
        st_sw = getattr(st, "variant", "") == "sonderwunsch"
        cur_sw = cur is not None and getattr(cur, "variant", "") == "sonderwunsch"
        if cur is None or (st_sw and not cur_sw):
            chosen[best_aid] = st
    return {
        apt_by_anchor[aid].apartment_id: float(st.area_m2)
        for aid, st in chosen.items()
    }


def cluster_apartments_floor_filtered(
        rooms: list, tops: list,
        target_fok: Optional[float] = None,
        floor_tol_m: float = 0.05,
        ambiguous_tol_mm: float = 250.0,
        n_bauteile: int = 1,
        area_stamps: Optional[list] = None,
        outdoor_patterns: tuple[str, ...] = ()) -> list[Apartment]:
    """Slice 16.1.6 — apartment clustering via tops[] anchors, floor-filtered.

    Replaces the door-graph BFS (which over-merged two physical units that
    share a Stiegenhaus) with deterministic nearest-anchor assignment on the
    target storey:

    1. ``select_target_tops`` keeps only anchors on the target FOK level.
    2. Communal rooms (by name) go to a communal bucket, never a unit. The
       FOK label's STGH/WOHNUNG word is NOT a communal marker — tops[] anchors
       are all genuine unit anchors (Slice 16.1.6 Hard-Stop 2).
    3. Every other room is assigned to its nearest anchor across ALL tops and
       kept only when that nearest anchor is on the target floor — so rooms of
       other storeys (whose nearest anchor is off-floor) fall out cleanly,
       without an arbitrary distance threshold.
    4. One Apartment per target top_id, ``estimated_top`` = that top_id.
    5. A room whose two nearest target-floor anchors tie within
       ``ambiguous_tol_mm`` is flagged for review (still assigned to the
       nearest, but ``review_flag`` set with a reason).
    """
    # Slice 1.3.0: FOK-Filter PRO Bauteil. Zwei Flügel können auf
    # verschiedenen Niveaus liegen (Mollgasse: MOLL +1.93 / AGG +4.03,
    # Hanglage) — ein globaler Modal-FOK warf einen kompletten Flügel raus.
    unit_decision_source = "cluster:floor_filter+nearest_anchor"
    target_tops: list = []
    for group in _partition_anchors_xy(tops, n_bauteile):
        _, group_targets = select_target_tops(group, target_fok, floor_tol_m)
        target_tops.extend(group_targets)
    if n_bauteile > 1:
        unit_decision_source = "cluster:floor_filter_per_bauteil+nearest_anchor"
    if (not target_tops and target_fok is None
            and _all_tops_without_parseable_fok(tops)):
        # Some blank floor plans have valid TOP anchors but no FOK text at all.
        # Then the incoming DXF is already the target floor, so all TOP anchors
        # are used instead of returning zero apartments.
        target_tops = list(tops)
        unit_decision_source = "cluster:all_tops_no_fok_fallback"
    apartments: list[Apartment] = []
    if not target_tops:
        return apartments

    target_ids = {t.top_id for t in target_tops}
    # Slice 1.3.0: EINE Wohnung pro ANKER, nicht pro top_id-String. Zwei
    # Bauteile nummerieren jeweils ab TOP 1 — auf gemischten Geschossen
    # existiert "TOP 4" doppelt; ein Dict-Key pro top_id verlor eine der
    # beiden Wohnungen. Duplikate bekommen deterministische Suffixe
    # (A_4, A_4_2 — sortiert nach Anker-Position), estimated_top bleibt
    # unqualifiziert; Bauteil-Auflösung macht building_units.match_unit.
    apt_by_anchor: dict[int, Apartment] = {}
    id_seen: Counter[str] = Counter()
    for t in sorted(target_tops,
                    key=lambda x: (x.top_id, x.anchor_mm[0], x.anchor_mm[1])):
        id_seen[t.top_id] += 1
        suffix = "" if id_seen[t.top_id] == 1 else f"_{id_seen[t.top_id]}"
        apt = Apartment(
            apartment_id=f"A_{t.top_id}{suffix}",
            room_ids=[],
            is_communal=False,
            estimated_top=t.top_id,
            decision_source=unit_decision_source,
            anchor_mm=(float(t.anchor_mm[0]), float(t.anchor_mm[1])),
        )
        apt_by_anchor[id(t)] = apt
        apartments.append(apt)

    communal_rooms: list = []
    wet_only_ids: set[int] = set()
    for r in rooms:
        if _is_communal_by_name(r.anchor.name) or _is_non_unit_by_name(r.anchor.name):
            communal_rooms.append(r)
            continue
        if (_norm_room_name(r.anchor.name) == "GANG"
                and _room_has_only_wet_doors(r)):
            # Slice 2.9.0: Allgemein-Gang vor den Wohnungseingangstüren —
            # Zugang NUR über WETs = Erschließung, nie Teil einer Wohnung.
            # (Bis 2.6.1 fing das die area-Eviction über die damals mehrfach
            # zugeordneten WET-Türen; der Tür-Anker-Fix nahm ihr die Evidenz.)
            wet_only_ids.add(id(r))
            communal_rooms.append(r)
            continue
        rp = (r.anchor.anchor_x_mm, r.anchor.anchor_y_mm)
        dists = sorted(
            ((math.hypot(t.anchor_mm[0] - rp[0], t.anchor_mm[1] - rp[1]), t)
             for t in tops),
            key=lambda d: d[0],
        )
        if not dists:
            continue
        nearest = dists[0][1]
        if nearest.top_id not in target_ids:
            # nearest anchor is on another storey -> not this floor's unit
            continue
        if id(nearest) not in apt_by_anchor:
            # gleiche top_id, aber Off-Floor-Anker (z.B. Maisonette-Duplikat)
            continue
        target_dists = [(d, t) for d, t in dists if t.top_id in target_ids]
        if len(target_dists) >= 2 and \
                target_dists[1][0] - target_dists[0][0] <= ambiguous_tol_mm:
            r.review_flag = True
            r.review_reason = (
                f"ambiguous nearest top: {target_dists[0][1].top_id} vs "
                f"{target_dists[1][1].top_id} "
                f"(Δ{target_dists[1][0] - target_dists[0][0]:.0f}mm)")
        apt_by_anchor[id(nearest)].room_ids.append(id(r))

    _reattach_ambiguous_service_rooms_by_doors(
        rooms, {apt.apartment_id: apt for apt in apt_by_anchor.values()})

    # Slice 1.4.0: Grenzraum-Refinement gegen die Wohnflächen-Stempel.
    # area_stamps=None ⇒ Verhalten bitidentisch zum bisherigen Pfad.
    if area_stamps:
        targets = _target_areas_from_stamps(area_stamps, tops, apt_by_anchor)
        if targets:
            _refine_boundary_rooms_by_area(
                {id(r): r for r in rooms},
                list(apt_by_anchor.values()),
                targets,
                outdoor_patterns=outdoor_patterns,
                communal_rooms=communal_rooms,
            )

    for r in communal_rooms:
        short_name = r.anchor.name[:10].strip().replace(" ", "_")
        if id(r) in wet_only_ids:
            src = "cluster:gang_wet_only_doors"
        elif _is_communal_by_name(r.anchor.name):
            src = "cluster:communal_by_name"
        else:
            src = "cluster:non_unit_by_name"
        apartments.append(Apartment(
            apartment_id=f"COMM_{short_name}",
            room_ids=[id(r)],
            is_communal=True,
            decision_source=src,
        ))

    return apartments


def filter_good_apartments_with_rooms(apartments: list, rooms: list,
                                      min_rooms: int = 7,
                                      min_area_m2: float = 50.0) -> list:
    """Filter apartments to GOOD quality (full unit with bath/bedroom/living)."""
    rooms_by_id = {id(r): r for r in rooms}
    good = []
    for apt in apartments:
        if apt.is_communal:
            continue
        if len(apt.room_ids) < min_rooms:
            continue
        total_area = sum(
            rooms_by_id[rid].anchor.area_m2
            for rid in apt.room_ids if rid in rooms_by_id
        )
        if total_area < min_area_m2:
            continue
        names_upper = [
            rooms_by_id[rid].anchor.name.upper()
            for rid in apt.room_ids if rid in rooms_by_id
        ]
        has_living = any("WOHN" in n or "KÜCH" in n or "KUECH" in n
                         for n in names_upper)
        has_bath = any("BAD" in n or "WC" in n for n in names_upper)
        has_bedroom = any("ZIMMER" in n for n in names_upper)
        if has_living and has_bath and has_bedroom:
            good.append(apt)
    return good
