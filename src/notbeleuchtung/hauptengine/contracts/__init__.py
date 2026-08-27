"""Die 3 Contracts + Ports = das einzige Modul-übergreifende Vokabular.

Owner-Module importieren NUR hieraus, nie voneinander.
"""
from .norm_regelwerk import (
    ErkennungsweiteParameter,
    Klassifikation,
    NormAnforderung,
    NormRegelwerk,
    RaumRegel,
)
from .platzierung_ergebnis import (
    Kind,
    Platzierung,
    PlatzierungsErgebnis,
    Richtung,
)
from .ports import NormProvider, Platzierer, ProviderBundle, RaumProvider
from .raum_modell import (
    Ausgang,
    BBox,
    Edge,
    FluchtwegSegment,
    Node,
    Raum,
    RaumModell,
    Tuer,
    ZirkulationsGraph,
)

# Modelle, die als versioniertes JSON-Schema eingecheckt werden (Drift-Gate).
SCHEMA_MODELS = {
    "raum_modell": RaumModell,
    "norm_regelwerk": NormRegelwerk,
    "platzierung_ergebnis": PlatzierungsErgebnis,
}

__all__ = [
    "SCHEMA_MODELS",
    "Ausgang",
    "BBox",
    "Edge",
    "ErkennungsweiteParameter",
    "FluchtwegSegment",
    "Kind",
    "Klassifikation",
    "Node",
    "NormAnforderung",
    "NormProvider",
    "NormRegelwerk",
    "Platzierer",
    "Platzierung",
    "PlatzierungsErgebnis",
    "ProviderBundle",
    "Raum",
    "RaumModell",
    "RaumProvider",
    "RaumRegel",
    "Richtung",
    "Tuer",
    "ZirkulationsGraph",
]
