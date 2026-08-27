"""
component.py — Elektrokomponenten-Datenmodell / component data model.

Supports both the simple per-room component list from the original prompt
and the VDMA 24186 attribute schema observed inside the E-Symbole-CAD
legend blocks. VDMA fields are optional; unknown-tag attributes land in
``extra_attrs`` so we never lose data we do not yet understand.
"""
from __future__ import annotations

from dataclasses import dataclass, field


# Known VDMA 24186 tag names observed so far (11 of 29). Extend as we
# confirm additional tags from the real symbol library / plans.
KNOWN_VDMA_TAGS: tuple[str, ...] = (
    "RAUMBUCHNUMMER",
    "ANLAGE",
    "TEILANLAGE_NR",
    "KOMPONENTE",
    "BEZEICHNUNG",
    "TYP",
    "HERSTELLER",
    "MODEL",
    "LV_POS",
    "JOBLISTE_VDMA",
)


@dataclass
class VDMA24186:
    """Attribute payload attached to a placed BIM/CAFM component.

    Stores the ten currently-known VDMA 24186 fields explicitly; the
    remaining ~19 tags land in :attr:`extra_attrs` until we confirm them.
    """
    raumbuchnummer: str = ""
    anlage: str = ""
    teilanlage_nr: str = ""
    komponente: str = ""
    bezeichnung: str = ""
    typ: str = ""
    hersteller: str = ""
    model: str = ""
    lv_pos: str = ""
    joblist_vdma: str = ""
    extra_attrs: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_attribs(cls, attribs: dict[str, str]) -> "VDMA24186":
        """Build from a raw {TAG: value} dict (e.g. from an INSERT)."""
        known = {t.lower(): attribs.get(t, "") for t in KNOWN_VDMA_TAGS}
        # Tag names that aren't in KNOWN_VDMA_TAGS
        extras = {k: v for k, v in attribs.items() if k not in KNOWN_VDMA_TAGS}
        # joblist_vdma maps from JOBLISTE_VDMA
        return cls(
            raumbuchnummer=known["raumbuchnummer"],
            anlage=known["anlage"],
            teilanlage_nr=known["teilanlage_nr"],
            komponente=known["komponente"],
            bezeichnung=known["bezeichnung"],
            typ=known["typ"],
            hersteller=known["hersteller"],
            model=known["model"],
            lv_pos=known["lv_pos"],
            joblist_vdma=known["joblist_vdma"],
            extra_attrs=extras,
        )


@dataclass
class Component:
    """One electrical component to place (or already placed).

    Attributes
    ----------
    kind : str
        Canonical component kind from the Leistungsbeschreibung, e.g.
        "STECKDOSE_2F", "SCHALTER_1F", "LEUCHTE_DECKE". Maps to a block
        name via symbol_service once the real library is resolved.
    quantity : int
        Count for an aggregated line in the Leistungsbeschreibung. For
        individual placed instances this is always 1.
    circuit : str | None
        Circuit label, e.g. "K1". None until assigned.
    room_id : str | None
        Links this component to a :class:`Room`. Unassigned components
        come from LV lines without a room column and must be resolved.
    position : tuple[float, float] | None
        Planar placement in mm. None until the placement engine runs.
    rotation_deg : float
        Block insertion rotation in degrees, 0 by default.
    layer : str
        Target DXF layer, e.g. "E-INSTALLATION".
    vdma : VDMA24186 | None
        Optional VDMA 24186 attribute payload.
    purpose : str | None
        Free-text appliance / usage tag extracted from the LV, e.g.
        "Kühlschrank" for a Schuko socket serving the fridge. Drives
        label text and attribute metadata downstream; does not change
        the inserted block.
    """
    kind: str
    quantity: int = 1
    circuit: str | None = None
    room_id: str | None = None
    position: tuple[float, float] | None = None
    rotation_deg: float = 0.0
    layer: str = "E-INSTALLATION"
    vdma: VDMA24186 | None = None
    purpose: str | None = None
