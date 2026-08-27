"""Ports — die Protocol-Interfaces, gegen die die 3 Owner-Module implementieren.

Dependency-Inversion: die Hauptengine besitzt diese Interfaces; jeder Owner
liefert eine Klasse, die ihr Protocol erfüllt. Kein Owner importiert einen
anderen — Kommunikation läuft ausschließlich über die Contract-Objekte
(RaumModell, NormRegelwerk/NormAnforderung, PlatzierungsErgebnis), die durch die
Pipeline fließen. Das ist die technische Umsetzung von „Selman-Leonis-Enis →
Hauptengine".
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from .norm_regelwerk import NormAnforderung, NormRegelwerk
from .platzierung_ergebnis import PlatzierungsErgebnis
from .raum_modell import FluchtwegSegment, RaumModell


@runtime_checkable
class RaumProvider(Protocol):
    """Selman — Grundriss-DXF -> RaumModell."""

    def parse(self, dxf_path: str, floor: str) -> RaumModell: ...


@runtime_checkable
class NormProvider(Protocol):
    """Enis — Query-API über das Normwissen."""

    def fuer_raum(self, raum_typ: str, ist_fluchtweg: bool) -> NormAnforderung: ...

    def fuer_fluchtweg_abschnitt(self, segment: FluchtwegSegment) -> NormAnforderung: ...

    def erkennungsweite_m(self, piktogramm_hoehe_m: float, hinterleuchtet: bool) -> float: ...

    def regelwerk_snapshot(self) -> NormRegelwerk: ...


@runtime_checkable
class Platzierer(Protocol):
    """Leonis — Platzierer(Raum, Norm) -> PlatzierungsErgebnis."""

    def place(self, raum: RaumModell, norm: NormProvider) -> PlatzierungsErgebnis: ...


@dataclass
class ProviderBundle:
    """Das von registry.py verdrahtete Trio (echt oder Fake)."""

    raum: RaumProvider
    norm: NormProvider
    platzierer: Platzierer
