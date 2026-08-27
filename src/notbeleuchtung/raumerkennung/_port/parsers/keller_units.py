"""keller_units.py — Kellergeschoss-Inventar (Mollgasse) aus geparsten Räumen.

Baut auf der bestehenden KG-Namens-Klassifikation
(``diagnostics.check_building_units._classify_by_name`` / ``_KELLERABTEIL_RE``)
auf und VERTIEFT sie zu einem strukturierten, elektro-nutzbaren Inventar:

  * **Kellerabteile** (ER 01…48) mit geparsten ER-Nummern (inkl. kombinierter
    Labels ``ER 09+10``) + Fläche/Position + Bauteil-Seite (KG-Floor).
  * **Elektro-relevante Technikräume** (Niederspannung, Technik, Wasserzähler,
    Medienraum) getaggt mit ``elektro_typ`` + Position = künftige Verteiler-/
    Zähler-Standorte.
  * **Garage / Doppelparker** — Zählung + Flächen (Cross-Check BAB
    ``pflichtstellplaetze``).
  * **ER↔Wohnung-Validierung** als COUNT (BAB: „je Wohnung 1 ER im KG").
    Eine per-ER→TOP-Zuordnung ist aus den Plänen NICHT ableitbar (kein
    Mapping-Feld, ER-Nummerierung ≠ TOP-Nummerierung) → als offener Punkt
    markiert, nicht geraten.

Dieses Modul LIEST/importiert nur aus den Parser-/Diagnostik-Modulen — es
editiert ``apartment_clustering``/``building_units``/``architecture_dxf``/
``check_building_units`` NICHT (Track-Boundary, Fenster-1-Parallelarbeit).
Die Platzierungs-Engine wird nicht berührt.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

# Single-Source der ER-Erkennung: die bestehende Regex aus check_building_units
# wiederverwenden (nur importieren, nicht ändern).
from diagnostics.check_building_units import _KELLERABTEIL_RE  # noqa: E402

# Elektro-relevante Technikräume → (elektro_typ, Name-Substrings). Reihenfolge =
# Priorität (spezifisch vor generischem "technik").
_ELEKTRO_TYP_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("niederspannung", ("NIEDERSP",)),
    ("wasserzaehler", ("WASSERZÄHLER", "WASSERZAEHLER", "WASSERZ")),
    ("medienraum", ("MEDIENRAUM", "MEDIEN")),
    ("technik", ("TECHNIK",)),
)

_GARAGE_TOKENS = ("GARAGE",)          # Garagen-Fläche (inkl. GARAGENRAMPE)
_DOPPELPARKER_TOKEN = "DOPPELPARKER"   # Doppelparker-Stellplätze/-Gruben
# Doppelparker-Anchors, die KEINE zählbaren Stellplätze sind (Luftraum/Grube-Void)
_DOPPELPARKER_NONCOUNT = ("LUFTRAUM", "GRUBE")

# BAB Mollgasse: 48 Wohnungen gesamt, „je Wohnung 1 Einlagerungsraum im KG".
DEFAULT_EXPECTED_APARTMENTS = 48
# BAB Mollgasse: 33 Pflichtstellplätze in der gemeinsamen Tiefgarage.
DEFAULT_EXPECTED_STELLPLAETZE = 33


# ---------------------------------------------------------------------------
# Datenmodell
# ---------------------------------------------------------------------------


@dataclass
class Kellerabteil:
    label: str                    # Roh-Label, z.B. "ER 27" / "ER 09+10"
    er_numbers: list[int]         # geparste Nummern, z.B. [27] / [9, 10]
    area_m2: float                # gestempelte Plan-Fläche
    x_mm: float | None
    y_mm: float | None
    kg: str                       # KG-Floor (Bauteil-Seite)
    # Rekonstruierte mm-Geometrie (Slice E, aus keller_geometry) — optional:
    polygon_mm: list | None = None
    polygon_area_m2: float | None = None
    area_ratio: float | None = None       # rekonstruiert / gestempelt
    fidelity: str | None = None           # high | coarse | unmatched | zone | None


@dataclass
class ElektroRaum:
    name: str
    elektro_typ: str              # niederspannung | technik | wasserzaehler | medienraum
    area_m2: float
    x_mm: float | None
    y_mm: float | None
    kg: str
    polygon_mm: list | None = None
    polygon_area_m2: float | None = None
    area_ratio: float | None = None
    fidelity: str | None = None


@dataclass
class GarageInfo:
    garage_rooms: list[dict[str, Any]] = field(default_factory=list)
    doppelparker_count: int = 0
    doppelparker_rooms: list[dict[str, Any]] = field(default_factory=list)
    expected_stellplaetze: int = DEFAULT_EXPECTED_STELLPLAETZE


@dataclass
class KellerInventory:
    kellerabteile: list[Kellerabteil] = field(default_factory=list)
    elektro_raeume: list[ElektroRaum] = field(default_factory=list)
    garage: GarageInfo = field(default_factory=GarageInfo)
    er_numbers: list[int] = field(default_factory=list)     # sortierte Union aller ER-Nummern
    expected_apartments: int = DEFAULT_EXPECTED_APARTMENTS
    flags: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "kellerabteile": [vars(a) for a in self.kellerabteile],
            "elektro_raeume": [vars(r) for r in self.elektro_raeume],
            "garage": {
                "garage_rooms": self.garage.garage_rooms,
                "doppelparker_count": self.garage.doppelparker_count,
                "doppelparker_rooms": self.garage.doppelparker_rooms,
                "expected_stellplaetze": self.garage.expected_stellplaetze,
            },
            "er_numbers": self.er_numbers,
            "er_count": len(self.er_numbers),
            "expected_apartments": self.expected_apartments,
            "flags": self.flags,
        }


# ---------------------------------------------------------------------------
# Klassifikations-Helfer
# ---------------------------------------------------------------------------


def is_kellerabteil(name: str) -> bool:
    """True wenn der Raumname ein Kellerabteil ist (ER…/EINLAGERUNG)."""
    return bool(_KELLERABTEIL_RE.match((name or "").strip().upper()))


def parse_er_numbers(name: str) -> list[int]:
    """Extrahiere ER-Nummern aus einem Kellerabteil-Label.

    ``"ER 27"`` → ``[27]``, ``"ER 09+10"`` → ``[9, 10]``,
    ``"ER 1.05"`` → ``[5]`` (Fischamender: Bauteil.Nummer — NN-Teil zählt),
    ``"ER-GESAMT"`` → ``[]`` (Aggregat, keine Einzel-Nummer).
    """
    up = (name or "").strip().upper()
    if "GESAMT" in up:
        return []
    dot = re.match(r"^ER[\s\-]*(\d+)\.(\d+)$", up)
    if dot:
        return [int(dot.group(2))]
    # Nur den Zahl-Teil nach dem ER-Präfix betrachten (nicht z.B. Flächen).
    match = re.match(r"^ER[\s\-]*([0-9+\s]+)", up)
    if not match:
        return []
    nums = re.findall(r"\d+", match.group(1))
    return [int(n) for n in nums]


def elektro_typ(name: str) -> str | None:
    """Elektro-Relevanz eines Raums → Typ oder None."""
    up = (name or "").strip().upper()
    for typ, tokens in _ELEKTRO_TYP_PATTERNS:
        if any(tok in up for tok in tokens):
            return typ
    return None


def is_garage(name: str) -> bool:
    up = (name or "").strip().upper()
    return any(tok in up for tok in _GARAGE_TOKENS)


def is_doppelparker(name: str) -> bool:
    up = (name or "").strip().upper()
    return _DOPPELPARKER_TOKEN in up


def _is_countable_doppelparker(name: str) -> bool:
    up = (name or "").strip().upper()
    if _DOPPELPARKER_TOKEN not in up:
        return False
    return not any(tok in up for tok in _DOPPELPARKER_NONCOUNT)


# ---------------------------------------------------------------------------
# Inventar-Aufbau
# ---------------------------------------------------------------------------


def _room_xy(room: dict[str, Any]) -> tuple[float | None, float | None]:
    return room.get("x_mm"), room.get("y_mm")


def build_keller_inventory(
    kg_rooms: dict[str, list[dict[str, Any]]],
    expected_apartments: int = DEFAULT_EXPECTED_APARTMENTS,
    expected_stellplaetze: int = DEFAULT_EXPECTED_STELLPLAETZE,
) -> KellerInventory:
    """Baue das KG-Inventar aus klassifizierten Räumen je KG-Floor.

    ``kg_rooms`` = ``{kg_floor_name: [room_dict, …]}``; jeder ``room_dict`` trägt
    mindestens ``name``, ``area_m2``, ``x_mm``, ``y_mm`` (wie die Einträge aus
    ``check_building_units.classify_floor_rooms``).
    """
    inv = KellerInventory(
        expected_apartments=expected_apartments,
        garage=GarageInfo(expected_stellplaetze=expected_stellplaetze),
    )
    er_union: set[int] = set()

    for kg, rooms in kg_rooms.items():
        for room in rooms:
            name = str(room.get("name") or "")
            area = float(room.get("area_m2") or 0.0)
            x, y = _room_xy(room)
            # optionale rekonstruierte Geometrie (vom Aufrufer eingemischt)
            geo = dict(
                polygon_mm=room.get("polygon_mm"),
                polygon_area_m2=room.get("polygon_area_m2"),
                area_ratio=room.get("area_ratio"),
                fidelity=room.get("fidelity"),
            )

            if is_kellerabteil(name):
                nums = parse_er_numbers(name)
                inv.kellerabteile.append(
                    Kellerabteil(label=name.strip(), er_numbers=nums,
                                 area_m2=area, x_mm=x, y_mm=y, kg=kg, **geo)
                )
                er_union.update(nums)
                continue

            typ = elektro_typ(name)
            if typ is not None:
                inv.elektro_raeume.append(
                    ElektroRaum(name=name.strip(), elektro_typ=typ,
                                area_m2=area, x_mm=x, y_mm=y, kg=kg, **geo)
                )
                # Technik-/Garage-Räume können sich überschneiden — Garage separat unten.

            if is_garage(name):
                inv.garage.garage_rooms.append(
                    {"name": name.strip(), "area_m2": area, "x_mm": x, "y_mm": y, "kg": kg}
                )
            if _is_countable_doppelparker(name):
                inv.garage.doppelparker_count += 1
                inv.garage.doppelparker_rooms.append(
                    {"name": name.strip(), "area_m2": area, "x_mm": x, "y_mm": y, "kg": kg}
                )

    inv.er_numbers = sorted(er_union)

    # Validierung: ER-Count vs. erwartete Wohnungen (BAB „1 pro Wohnung").
    er_count = len(inv.er_numbers)
    missing = sorted(set(range(1, expected_apartments + 1)) - er_union)
    extra = sorted(n for n in er_union if n > expected_apartments)
    inv.flags = {
        "er_count": er_count,
        "er_complete": er_count == expected_apartments and not missing and not extra,
        "er_missing_vs_expected": missing,
        "er_extra_vs_expected": extra,
        # Per-ER→TOP-Zuordnung ist aus den Plänen nicht deterministisch ableitbar.
        "er_to_top_mapping": "unavailable_needs_source",
        "er_to_top_note": (
            "ER-Nummerierung ist nicht an TOP-Nummerierung gekoppelt; keine "
            "Mapping-Quelle (Verkaufs-/Möbelplan 07_MOB oder kuratierte Tabelle "
            "nötig). Nur Count-Validierung möglich."
        ),
        "elektro_raum_count": len(inv.elektro_raeume),
        "elektro_typen": sorted({r.elektro_typ for r in inv.elektro_raeume}),
        "doppelparker_count": inv.garage.doppelparker_count,
    }
    # Geometrie-Fidelity (Slice E): wie viele Abteile haben ein mm-Polygon?
    graded = [a for a in inv.kellerabteile if a.fidelity is not None]
    if graded:
        inv.flags["geometry_fidelity"] = {
            "high": sum(1 for a in graded if a.fidelity == "high"),
            "coarse": sum(1 for a in graded if a.fidelity == "coarse"),
            "unmatched": sum(1 for a in graded if a.fidelity == "unmatched"),
            # ER-GESAMT-Summenstempel läuft als Zone (Slice M) — zählt zu
            # graded_abteile, aber nicht in die high/coarse/unmatched-Wertung.
            "zone": sum(1 for a in graded if a.fidelity == "zone"),
            "graded_abteile": len(graded),
        }
    return inv
