"""Bauteil-aware Wohnungs-Inventur aus TOP-Türschild-Stempeln.

Slice 1.0.0. Generisch über das Profil-System (`layer_profiles`):
Stempel-Blocknamen, Attrib-Tag, Bauteil-Zahl und Soll-TOP-IDs kommen aus
`profiles/<id>.yaml` (`building_units:`-Sektion) — kein Projekt-Hardcode.

Kernproblem: mehrere Bauteile im selben Plan nummerieren ihre Wohnungen
jeweils eigenständig ab TOP 1. "TOP 4" ist daher erst mit Bauteil-Kontext
eindeutig. Trennung über Konflikt-Partition: zwei Stempel mit derselben
TOP-ID im selben Geschoss können nicht zum selben Bauteil gehören.

Kombi-Stempel ("TOP 4 + 5") = EINE zusammengelegte Wohnung. Wohnungen mit
überlappenden TOP-IDs im selben Bauteil werden über Geschosse hinweg zu
einer Einheit gemerged (Maisonetten + Notations-Drift "2+3" vs "2 + 3").
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from itertools import permutations
from pathlib import Path
from typing import Any, Iterable

import ezdxf

from parsers.layer_profiles import LayerProfile, load_profile

# "TOP 4 + 5", "TOP 11+12", "TOP 9 (SONDERWUNSCH)", "top 7" → ID-Tupel.
_PAREN_RE = re.compile(r"\([^)]*\)")
_TOP_RE = re.compile(r"\bTOP\b\s*[:#\-]*\s*([0-9][0-9+/ ]*)", re.IGNORECASE)
_ID_SPLIT_RE = re.compile(r"[+/]")


@dataclass(frozen=True)
class TopStamp:
    floor: str
    x: float
    y: float
    raw: str
    top_ids: tuple[int, ...]


@dataclass(frozen=True)
class AreaStamp:
    """Wohnflächen-Summen-Stempel des Architekten ("TOP 24 (SONDERWUNSCH) 54.55 m²")."""
    floor: str
    x: float
    y: float
    top_ids: tuple[int, ...]
    area_m2: float
    variant: str  # "standard" | "sonderwunsch"


@dataclass
class BuildingUnit:
    bauteil: str
    top_ids: tuple[int, ...]
    floors: tuple[str, ...]
    stamp_count: int
    # Offizielle Architekten-Wohnfläche (Innenfläche) aus dem Summen-Stempel.
    # None wenn der Plan keinen liefert. Entscheid 25.07.: Sonderwunsch-
    # Variante gewinnt über Standard (SW = gebauter Zustand).
    wohnflaeche_m2: float | None = None
    area_variant: str | None = None
    # Mittelpunkt der Türschild-Stempel (Zeichnungs-Einheiten) — bauteil-
    # sicherer Anker für spätere Zuordnungen (match_unit).
    anchor_xy: tuple[float, float] | None = None


@dataclass
class UnitInventory:
    profile_id: str
    units: list[BuildingUnit]
    coverage: dict[str, dict[str, Any]]
    unassigned: list[TopStamp] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(c["missing"] == [] and c["extra"] == [] for c in self.coverage.values())

    def units_of(self, bauteil: str) -> list[BuildingUnit]:
        return [u for u in self.units if u.bauteil == bauteil]

    def match_unit(self, top_ids: tuple[int, ...],
                   xy: tuple[float, float] | None = None) -> BuildingUnit | None:
        """Einheit zu TOP-IDs finden; bei Bauteil-Duplikaten entscheidet
        die räumliche Nähe zum Türschild-Anker (xy in Zeichnungs-Einheiten)."""
        cands = [u for u in self.units if set(top_ids) & set(u.top_ids)]
        if len(cands) <= 1 or xy is None:
            return cands[0] if cands else None
        def dist(u: BuildingUnit) -> float:
            if u.anchor_xy is None:
                return float("inf")
            return (u.anchor_xy[0] - xy[0]) ** 2 + (u.anchor_xy[1] - xy[1]) ** 2
        return min(cands, key=dist)


def parse_top_ids(text: str) -> tuple[int, ...]:
    """Extract sorted TOP ids from a stamp text; () when no TOP found."""
    cleaned = _PAREN_RE.sub(" ", text or "")
    m = _TOP_RE.search(cleaned)
    if not m:
        return ()
    ids: set[int] = set()
    for part in _ID_SPLIT_RE.split(m.group(1)):
        part = part.strip()
        if part.isdigit():
            ids.add(int(part))
    return tuple(sorted(ids))


def extract_stamps(dxf_path: Path, floor: str,
                   cfg: dict[str, Any]) -> list[TopStamp]:
    """Read TOP door-plate stamps (INSERT + ATTRIB) from one floor DXF."""
    blocks = set(cfg.get("stamp_blocks") or [])
    attrib_tag = str(cfg.get("stamp_attrib") or "TOP")
    doc = ezdxf.readfile(str(dxf_path))
    return stamps_from_msp(doc.modelspace(), floor, blocks, attrib_tag)


def stamps_from_msp(msp: Iterable, floor: str, blocks: set[str],
                    attrib_tag: str) -> list[TopStamp]:
    out: list[TopStamp] = []
    for e in msp:
        if e.dxftype() != "INSERT" or e.dxf.name not in blocks:
            continue
        for a in e.attribs:
            if a.dxf.tag != attrib_tag:
                continue
            raw = re.sub(r"\s+", " ", a.dxf.text or "").strip()
            ids = parse_top_ids(raw)
            if ids:
                p = e.dxf.insert
                out.append(TopStamp(floor=floor, x=float(p.x), y=float(p.y),
                                    raw=raw, top_ids=ids))
    return out


_AREA_RE = re.compile(r"([0-9]+(?:[.,][0-9]+)?)\s*m", re.IGNORECASE)


def parse_area_m2(text: str) -> float | None:
    m = _AREA_RE.search(text or "")
    return float(m.group(1).replace(",", ".")) if m else None


def area_stamps_from_msp(msp: Iterable, floor: str, blocks: set[str],
                         room_tag: str, area_tag: str) -> list[AreaStamp]:
    """Per-TOP Wohnflächen-Summen-Stempel aus den Raum-Stempel-Blocks lesen.

    Der Architekt setzt neben die Raum-Stempel einen Summen-Stempel, dessen
    ROOM-Attribut der TOP-Name ist ("TOP 24 (SONDERWUNSCH)") und dessen
    AREA-Attribut die offizielle Wohnfläche trägt.
    """
    out: list[AreaStamp] = []
    for e in msp:
        if e.dxftype() != "INSERT" or e.dxf.name not in blocks:
            continue
        at = {a.dxf.tag: re.sub(r"\s+", " ", a.dxf.text or "").strip()
              for a in e.attribs}
        room = at.get(room_tag, "")
        # Nur echte Summen-Stempel: ROOM beginnt mit "TOP ..." — Raum-Namen
        # wie "TERRASSE TOP 1" sind Raum-Stempel, keine Wohnflächen-Summen.
        if not re.match(r"^\s*TOP\b", room, re.IGNORECASE):
            continue
        ids = parse_top_ids(room)
        if not ids:
            continue
        area = parse_area_m2(at.get(area_tag, "")) or parse_area_m2(room)
        if area is None:
            continue
        variant = "sonderwunsch" if "SONDERWUNSCH" in room.upper() else "standard"
        p = e.dxf.insert
        out.append(AreaStamp(floor=floor, x=float(p.x), y=float(p.y),
                             top_ids=ids, area_m2=area, variant=variant))
    return out


def _conflict(a: TopStamp, b: TopStamp) -> bool:
    return a.floor == b.floor and bool(set(a.top_ids) & set(b.top_ids))


def partition_bauteile(stamps: list[TopStamp], n: int) -> list[int]:
    """Assign each stamp a cluster index 0..n-1.

    Constrained k-means: same-floor stamps with overlapping TOP ids are
    cannot-link pairs. Seeds = the farthest-apart conflict pair (falls
    back to the farthest pair overall). Deterministic, no RNG.
    """
    if n <= 1 or len(stamps) <= 1:
        return [0] * len(stamps)
    if n != 2:
        raise ValueError(f"partition_bauteile supports 1-2 Bauteile, got {n}")

    def d2(a: TopStamp, b: TopStamp) -> float:
        return (a.x - b.x) ** 2 + (a.y - b.y) ** 2

    pairs = [(i, j) for i in range(len(stamps)) for j in range(i + 1, len(stamps))]
    conflict_pairs = [(i, j) for i, j in pairs if _conflict(stamps[i], stamps[j])]
    seed_pool = conflict_pairs or pairs
    si, sj = max(seed_pool, key=lambda p: d2(stamps[p[0]], stamps[p[1]]))
    centroids = [(stamps[si].x, stamps[si].y), (stamps[sj].x, stamps[sj].y)]

    assign = [0] * len(stamps)
    for _ in range(20):
        prev = list(assign)
        for i, s in enumerate(stamps):
            dists = [(s.x - cx) ** 2 + (s.y - cy) ** 2 for cx, cy in centroids]
            assign[i] = dists.index(min(dists))
        # cannot-link reparieren: den zentroid-ferneren Konflikt-Partner umsetzen
        for i, j in conflict_pairs:
            if assign[i] == assign[j]:
                c = centroids[assign[i]]
                di = (stamps[i].x - c[0]) ** 2 + (stamps[i].y - c[1]) ** 2
                dj = (stamps[j].x - c[0]) ** 2 + (stamps[j].y - c[1]) ** 2
                move = i if di >= dj else j
                assign[move] = 1 - assign[move]
        for k in range(2):
            members = [s for s, a in zip(stamps, assign) if a == k]
            if members:
                centroids[k] = (sum(m.x for m in members) / len(members),
                                sum(m.y for m in members) / len(members))
        if assign == prev:
            break
    return assign


def _name_clusters(stamps: list[TopStamp], assign: list[int],
                   bauteile: list[dict[str, Any]]) -> dict[int, str]:
    """Map cluster index → Bauteil name by best Soll-ID coverage."""
    n = len(bauteile)
    found: dict[int, set[int]] = {k: set() for k in range(n)}
    for s, a in zip(stamps, assign):
        found[a].update(s.top_ids)
    expected = {b["name"]: set(range(1, int(b["soll_top_ids"]) + 1))
                for b in bauteile}
    names = [b["name"] for b in bauteile]
    best: tuple[float, tuple[str, ...]] | None = None
    for perm in permutations(names):
        score = sum(len(found[k] & expected[nm]) - len(found[k] - expected[nm])
                    for k, nm in enumerate(perm))
        if best is None or score > best[0]:
            best = (score, perm)
    assert best is not None
    return {k: nm for k, nm in enumerate(best[1])}


def _assign_wohnflaeche(units: list[BuildingUnit],
                        unit_member_stamps: list[list[TopStamp]],
                        area_stamps_by_floor: dict[str, list[AreaStamp]]) -> None:
    """Wohnflächen-Stempel den Einheiten zuordnen (in-place).

    Zuordnung über den räumlich nächsten Türschild-Stempel mit ID-Overlap
    (bauteil-sicher trotz doppelter TOP-Nummern). Pro Einheit + Geschoss
    gewinnt die Sonderwunsch-Variante über Standard (Entscheid 25.07.);
    Maisonetten summieren über ihre Geschosse.
    """
    per_unit: dict[int, list[AreaStamp]] = {}
    for floor_stamps in area_stamps_by_floor.values():
        for a in floor_stamps:
            best: tuple[float, int] | None = None
            for ui, members in enumerate(unit_member_stamps):
                for s in members:
                    if not set(a.top_ids) & set(s.top_ids):
                        continue
                    d = (a.x - s.x) ** 2 + (a.y - s.y) ** 2
                    if best is None or d < best[0]:
                        best = (d, ui)
            if best is not None:
                per_unit.setdefault(best[1], []).append(a)

    for ui, stamps in per_unit.items():
        by_floor: dict[str, list[AreaStamp]] = {}
        for a in stamps:
            by_floor.setdefault(a.floor, []).append(a)
        total = 0.0
        used_sw = False
        for floor_group in by_floor.values():
            sw = [a for a in floor_group if a.variant == "sonderwunsch"]
            chosen = sw[0] if sw else floor_group[0]
            used_sw = used_sw or bool(sw)
            total += chosen.area_m2
        units[ui].wohnflaeche_m2 = round(total, 2)
        units[ui].area_variant = "sonderwunsch" if used_sw else "standard"


def build_inventory(stamps_by_floor: dict[str, list[TopStamp]],
                    profile: LayerProfile,
                    area_stamps_by_floor: dict[str, list[AreaStamp]] | None = None,
                    ) -> UnitInventory:
    cfg = profile.building_units
    bauteile = list(cfg.get("bauteile") or [])
    if not bauteile:
        raise ValueError(
            f"Profile {profile.profile_id!r} has no building_units.bauteile")

    stamps = [s for floor in sorted(stamps_by_floor)
              for s in stamps_by_floor[floor]]
    assign = partition_bauteile(stamps, len(bauteile))
    cluster_name = _name_clusters(stamps, assign, bauteile)

    # Union-Find über ID-Overlap pro Bauteil: Maisonetten + Kombi-Drift mergen.
    by_bauteil: dict[str, list[TopStamp]] = {b["name"]: [] for b in bauteile}
    for s, a in zip(stamps, assign):
        by_bauteil[cluster_name[a]].append(s)

    units: list[BuildingUnit] = []
    unit_member_stamps: list[list[TopStamp]] = []
    for name, group in by_bauteil.items():
        merged: list[dict[str, Any]] = []  # {ids, floors, count, stamps}
        for s in group:
            hits = [m for m in merged if m["ids"] & set(s.top_ids)]
            if hits:
                target = hits[0]
                for other in hits[1:]:
                    target["ids"] |= other["ids"]
                    target["floors"] |= other["floors"]
                    target["count"] += other["count"]
                    target["stamps"].extend(other["stamps"])
                    merged.remove(other)
            else:
                target = {"ids": set(), "floors": set(), "count": 0, "stamps": []}
                merged.append(target)
            target["ids"] |= set(s.top_ids)
            target["floors"].add(s.floor)
            target["count"] += 1
            target["stamps"].append(s)
        for m in merged:
            sx = sum(s.x for s in m["stamps"]) / len(m["stamps"])
            sy = sum(s.y for s in m["stamps"]) / len(m["stamps"])
            units.append(BuildingUnit(bauteil=name,
                                      top_ids=tuple(sorted(m["ids"])),
                                      floors=tuple(sorted(m["floors"])),
                                      stamp_count=m["count"],
                                      anchor_xy=(sx, sy)))
            unit_member_stamps.append(m["stamps"])

    _assign_wohnflaeche(units, unit_member_stamps, area_stamps_by_floor or {})
    order = sorted(range(len(units)), key=lambda i: (units[i].bauteil, units[i].top_ids))
    units = [units[i] for i in order]

    # Soll-informierte Reparatur (BAB-first): eine Einheit, deren IDs das
    # Soll ihres Bauteils sprengen, aber exakt in die Lücke genau EINES
    # anderen Bauteils passen, wird umgehängt. Fängt räumliche Fehl-Cluster
    # an Gebäude-Ecken (z.B. MOLL TOP 21/22 neben dem AGG-Flügel).
    expected_by_name = {b["name"]: set(range(1, int(b["soll_top_ids"]) + 1))
                        for b in bauteile}
    for _ in range(len(units)):
        got = {name: {i for u in units if u.bauteil == name for i in u.top_ids}
               for name in expected_by_name}
        moved = False
        for idx, u in enumerate(units):
            ids = set(u.top_ids)
            if ids <= expected_by_name[u.bauteil]:
                continue
            targets = [name for name, exp in expected_by_name.items()
                       if name != u.bauteil and ids <= exp
                       and not (ids & got[name])]
            if len(targets) == 1:
                units[idx] = BuildingUnit(bauteil=targets[0], top_ids=u.top_ids,
                                          floors=u.floors,
                                          stamp_count=u.stamp_count,
                                          wohnflaeche_m2=u.wohnflaeche_m2,
                                          area_variant=u.area_variant,
                                          anchor_xy=u.anchor_xy)
                moved = True
                break
        if not moved:
            break
    units.sort(key=lambda u: (u.bauteil, u.top_ids))

    coverage: dict[str, dict[str, Any]] = {}
    for b in bauteile:
        name = b["name"]
        expected = set(range(1, int(b["soll_top_ids"]) + 1))
        got = {i for u in units if u.bauteil == name for i in u.top_ids}
        coverage[name] = {
            "soll_top_ids": len(expected),
            "found_top_ids": sorted(got),
            "missing": sorted(expected - got),
            "extra": sorted(got - expected),
            "physical_units": sum(1 for u in units if u.bauteil == name),
        }
    return UnitInventory(profile_id=profile.profile_id, units=units,
                         coverage=coverage)


@dataclass
class RoomAreaCheck:
    """Plausibilitäts-Abgleich Raum-Summe vs. Architekten-Wohnfläche pro Einheit."""
    bauteil: str
    top_ids: tuple[int, ...]
    innen_m2: float
    aussen_m2: float
    room_count: int
    wohnflaeche_m2: float | None
    delta_m2: float | None
    flag: bool


AREA_CHECK_TOLERANCE_M2 = 2.0


def _is_outdoor(room_name: str, outdoor_patterns: tuple[str, ...]) -> bool:
    up = (room_name or "").upper()
    return any(p in up for p in outdoor_patterns)


def aggregate_room_areas(inventory: UnitInventory,
                         apartments: Iterable[tuple[str, tuple[float, float] | None,
                                                    list[tuple[str, float]]]],
                         outdoor_patterns: tuple[str, ...],
                         ) -> list[RoomAreaCheck]:
    """Cluster-Räume pro Einheit summieren + gegen Wohnflächen-Stempel prüfen.

    `apartments`: (top_label, anchor_xy in Zeichnungs-Einheiten, [(raum, m²)]).
    Innen/Außen getrennt (Entscheid 25.07.); flag wenn |innen − Stempel| >
    AREA_CHECK_TOLERANCE_M2. Deckt Fehl-Zuordnungen des Clusterings auf.
    """
    acc: dict[int, dict[str, Any]] = {}
    for top_label, xy, rooms in apartments:
        ids = parse_top_ids(f"TOP {top_label}")
        if not ids:
            continue
        unit = inventory.match_unit(ids, xy)
        if unit is None:
            continue
        ui = inventory.units.index(unit)
        slot = acc.setdefault(ui, {"innen": 0.0, "aussen": 0.0, "count": 0})
        for name, area in rooms:
            if _is_outdoor(name, outdoor_patterns):
                slot["aussen"] += area or 0.0
            else:
                slot["innen"] += area or 0.0
            slot["count"] += 1

    checks: list[RoomAreaCheck] = []
    for ui, slot in sorted(acc.items()):
        u = inventory.units[ui]
        delta = (round(slot["innen"] - u.wohnflaeche_m2, 2)
                 if u.wohnflaeche_m2 is not None else None)
        checks.append(RoomAreaCheck(
            bauteil=u.bauteil, top_ids=u.top_ids,
            innen_m2=round(slot["innen"], 2),
            aussen_m2=round(slot["aussen"], 2),
            room_count=slot["count"],
            wohnflaeche_m2=u.wohnflaeche_m2,
            delta_m2=delta,
            flag=delta is not None and abs(delta) > AREA_CHECK_TOLERANCE_M2))
    return checks


def inventory_from_dir(project_dir: Path,
                       profile_id: str = "mollgasse") -> UnitInventory:
    """Scan every *.dxf floor file in `project_dir` → UnitInventory."""
    profile = load_profile(profile_id)
    cfg = profile.building_units
    blocks = set(cfg.get("stamp_blocks") or [])
    attrib_tag = str(cfg.get("stamp_attrib") or "TOP")
    area_blocks = set(cfg.get("area_stamp_blocks") or [])
    room_tag = str(cfg.get("area_room_attrib") or "ROOM")
    area_tag = str(cfg.get("area_attrib") or "AREA")

    stamps_by_floor: dict[str, list[TopStamp]] = {}
    area_by_floor: dict[str, list[AreaStamp]] = {}
    for path in sorted(project_dir.glob("*.dxf")):
        doc = ezdxf.readfile(str(path))
        msp = list(doc.modelspace())
        stamps_by_floor[path.stem] = stamps_from_msp(
            msp, path.stem, blocks, attrib_tag)
        if area_blocks:
            area_by_floor[path.stem] = area_stamps_from_msp(
                msp, path.stem, area_blocks, room_tag, area_tag)
    return build_inventory(stamps_by_floor, profile, area_by_floor)
