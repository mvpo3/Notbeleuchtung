"""
project.py — Projekt-Metadaten / Project metadata dataclasses.

Pure dataclasses — keep CAD/PDF imports out of this module so the
models stay trivially serialisable (JSON, persistence, API payloads).
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date


DEFAULT_SCALE = "1:50"
DEFAULT_STANDARD_REF = "OVE E 8101:2025"


@dataclass
class Project:
    """One electrical-installation plan job.

    Attributes
    ----------
    id : str
        UUID4 string generated on construction.
    name : str
        Projektname — free text shown in the title block.
    address : str
        Objekt / Adresse.
    planner : str
        Planersteller — draftsperson or firm.
    date : date
        Plan date; defaults to today.
    scale : str
        Maßstab, always "1:50" per project rules.
    standard_ref : str
        ÖNORM reference — defaults to "OVE E 8101:2025".
    revision_index : str
        Plan-Revisionsindex, e.g. "A", "B", or "10".
    source_arch_plan : str | None
        Absolute path of the input architectural DXF.
    source_leistungsbeschreibung : str | None
        Absolute path of the input spec PDF.
    source_reference_plan : str | None
        Optional reference plan PDF from general contractor.
    """
    name: str
    address: str = ""
    planner: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    date: date = field(default_factory=date.today)
    scale: str = DEFAULT_SCALE
    standard_ref: str = DEFAULT_STANDARD_REF
    revision_index: str = "01"
    source_arch_plan: str | None = None
    source_leistungsbeschreibung: str | None = None
    source_reference_plan: str | None = None
