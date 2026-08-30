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

from .lb_vorgabe import LBVorgabe
from .norm_regelwerk import NormAnforderung, NormRegelwerk
from .oib_ergebnis import OibBefund
from .platzierung_ergebnis import PlatzierungsErgebnis
from .projekt_kontext import ProjektKontext
from .raum_modell import FluchtwegSegment, RaumModell


@runtime_checkable
class RaumProvider(Protocol):
    """Selman — Grundriss-DXF -> RaumModell."""

    def parse(self, dxf_path: str, floor: str) -> RaumModell: ...


@runtime_checkable
class LBProvider(Protocol):
    """Enis — Leistungsbeschreibung (2. Input) -> LBVorgabe.

    Parst die explizite Auftraggeber-LB in die strukturierten Vorgaben, die
    Norm-Defaults übersteuern. Implementierung folgt (`normwissen/lb/`) — hier nur
    das Protocol. Fehlt der 2. Input, gibt es keine LBVorgabe → reines Norm-Verhalten.
    """

    def parse_lb(self, lb_path: str) -> LBVorgabe: ...


@runtime_checkable
class NormProvider(Protocol):
    """Enis — Query-API über das Normwissen."""

    def fuer_raum(self, raum_typ: str, ist_fluchtweg: bool) -> NormAnforderung: ...

    def fuer_fluchtweg_abschnitt(self, segment: FluchtwegSegment) -> NormAnforderung: ...

    def erkennungsweite_m(self, piktogramm_hoehe_m: float, hinterleuchtet: bool) -> float: ...

    def regelwerk_snapshot(self) -> NormRegelwerk: ...


@runtime_checkable
class Platzierer(Protocol):
    """Leonis — Platzierer(Raum, Norm[, LB]) -> PlatzierungsErgebnis.

    `lb` ist der optionale 2. Input: die explizite Leistungsbeschreibung, die
    Norm-Defaults übersteuert (z.B. `bereiche_exklusion` → keine Sicherheitsleuchte
    trotz Norm-Default). `lb=None` = kein 2. Input → reines Norm-Verhalten.
    """

    def place(
        self, raum: RaumModell, norm: NormProvider, lb: LBVorgabe | None = None
    ) -> PlatzierungsErgebnis: ...


@runtime_checkable
class OibProvider(Protocol):
    """OIB-Richtlinie 2 Tabelle 6 — ProjektKontext -> OibBefund.

    Getrennt vom EN-1838-NormProvider: anderer Input (gebäudeweiter Projektkontext)
    und anderer Output (Erforderlichkeits-Befund je Gebäudeteil). Resolver folgt in
    einem späteren Slice — hier nur das Protocol.
    """

    def bewerte_oib(self, projekt: ProjektKontext) -> OibBefund: ...


@dataclass
class ProviderBundle:
    """Das von registry.py verdrahtete Trio (echt oder Fake) + optionaler LB-Parser.

    `lb` ist optional: der 2. Input (Leistungsbeschreibung) ist projektspezifisch und
    kann fehlen. Ohne LB-Provider läuft die Engine rein norm-getrieben (wie bisher).
    """

    raum: RaumProvider
    norm: NormProvider
    platzierer: Platzierer
    lb: LBProvider | None = None
