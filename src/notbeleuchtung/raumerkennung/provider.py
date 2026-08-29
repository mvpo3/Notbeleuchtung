"""ArchitekturRaumProvider — echter RaumProvider (Selman).

Übersetzt einen leeren Architekturplan (DXF) in das ``RaumModell``-Contract:
Räume/Türen/Ausgänge/Fluchtweg-Zirkulation. Reine Geometrie/Topologie, kein
Norm-Urteil (das machen Enis/Leonis).

Baut inkrementell auf schlanken Modulen dieses Packages auf und verwendet die
sauberen, self-contained Port-Helfer (``._port.parsers.room_faces``,
``._port.models.room``) wieder. Ersetzt schrittweise den ``FakeRaumProvider``.
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import RaumModell

from .dxf_load import bounds_mm, lade_dxf
from .raumtyp import beschrifte_raeume
from .tueren import tueren_aus_dxf
from .waende import raeume_aus_waenden
from .zirkulation import zirkulation_aus_dxf


class ArchitekturRaumProvider:
    """Erfüllt das ``RaumProvider``-Protocol (``parse(dxf_path, floor)``).

    Verdrahtet die Slice-Module zu einem ``RaumModell``. Räume/Türen/Fluchtweg
    aus echter DXF-Geometrie; Norm-Urteile bleiben Enis/Leonis.

    Grenze: Raum-Polygone stammen aus naiver Wand-Polygonisierung (S2) — robust
    nur auf sauber geschlossenen Wänden. Auf echten Doppellinien-Wänden ohne
    Gap-Healing sind sie unvollständig (dokumentiert; eigener Folge-Slice).
    """

    def parse(self, dxf_path: str, floor: str) -> RaumModell:
        plan = lade_dxf(dxf_path)
        bounds = bounds_mm(plan)
        raeume = beschrifte_raeume(plan, raeume_aus_waenden(plan))
        tueren = tueren_aus_dxf(plan)
        zirkulation, ausgaenge = zirkulation_aus_dxf(plan, bounds)
        return RaumModell(
            floor=floor,
            bounds_mm=bounds,
            raeume=raeume,
            tueren=tueren,
            ausgaenge=ausgaenge,
            zirkulation=zirkulation,
        )
