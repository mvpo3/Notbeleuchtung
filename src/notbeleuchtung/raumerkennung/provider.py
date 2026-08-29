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


class ArchitekturRaumProvider:
    """Erfüllt das ``RaumProvider``-Protocol (``parse(dxf_path, floor)``)."""

    def parse(self, dxf_path: str, floor: str) -> RaumModell:
        raise NotImplementedError("Slice S1–S6 — noch nicht verdrahtet.")
