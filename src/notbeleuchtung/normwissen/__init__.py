"""Normwissen (Enis) — implementiert NormProvider, OibProvider und LBProvider.

`PlatzierungsRegelwerk` ergänzt sie um die Placement-Decision-Matrix (WANN welche
Leuchte WO hin muss); `SonderstellenKatalog` trägt den Contract-VORSCHLAG für die
hervorzuhebenden Stellen nach EN 1838 §4.1.2. Beide sind Contract-Kandidaten und
noch nicht im Ports-Protocol.
"""
from .lb import LbTextProvider
from .oib import OibRl2Provider
from .platzierungsregeln import HardStop, PlatzierungsRegel, PlatzierungsRegelwerk
from .provider import En1838NormProvider
from .sonderstellen import Sonderstelle, SonderstellenKatalog

__all__ = [
    "En1838NormProvider",
    "HardStop",
    "LbTextProvider",
    "OibRl2Provider",
    "PlatzierungsRegel",
    "PlatzierungsRegelwerk",
    "Sonderstelle",
    "SonderstellenKatalog",
]
