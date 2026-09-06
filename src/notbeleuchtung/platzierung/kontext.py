"""kontext — die querschneidenden Eingaben EINER Platzierung, als ein Objekt.

Architektur-Slice 2026-09-06 (Hot-Spot-Befund): `platzierer.py` war mit 14
Änderungen in zwei Wochen das meistgeänderte Modul des Packages — fast immer,
weil eine neue Naht (LB, OIB, Photometrie-Callable, Familien-Callables …) als
weiterer Parameter durch 2–3 Signatur-Ebenen gefädelt werden musste (#121: EIN
Callable → vier Signaturen). Dieses Objekt bündelt die querschneidenden
Eingaben; der Orchestrator reicht es EINMAL an die Strategien, künftige Nähte
sind ein neues Feld statt N Signatur-Änderungen.

Bewusst NICHT im Kontext: `raum` und `norm` — das sind die Domänen-Eingaben,
die jede Strategie sowieso positional nimmt. Die bestehenden Einzel-kwargs der
Strategie-Einstiege (`oib=`, `i_cd_fn=` …) bleiben für Tests/Direktaufrufer
erhalten; explizit übergebene Werte gewinnen gegen den Kontext.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field

from notbeleuchtung.hauptengine.contracts import LBVorgabe, OibBefund


@dataclass(frozen=True)
class PlatzierungsKontext:
    """Querschneidende Eingaben eines `place()`-Laufs (unveränderlich)."""

    lb: LBVorgabe | None = None
    oib: OibBefund | None = None
    #: Lichtstärke-Callable der Fluchtweg-Deckungs-Leuchte (Corridor-Optik).
    i_cd_fn: Callable | None = None
    #: catalog_key → Lichtstärke-Callable je Leuchtenfamilie (Registry-Katalog).
    i_cd_fn_je_key: Mapping[str, Callable] = field(default_factory=dict)


#: Leerer Default — Strategien ohne expliziten Kontext verhalten sich wie bisher.
LEER = PlatzierungsKontext()
