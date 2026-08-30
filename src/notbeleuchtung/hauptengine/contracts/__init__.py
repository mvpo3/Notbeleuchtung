"""Die 3 Contracts + Ports = das einzige Modul-übergreifende Vokabular.

Owner-Module importieren NUR hieraus, nie voneinander.
"""
from .lb_vorgabe import (
    BereichsRegel,
    LBVorgabe,
    Pruefung,
    RzStelle,
    SonderLux,
    SystemTyp,
    Ueberwachung,
)
from .norm_regelwerk import (
    ErkennungsweiteParameter,
    Klassifikation,
    NormAnforderung,
    NormRegelwerk,
    RaumRegel,
)
from .oib_ergebnis import OibBefund, OibErgebnis, OibStufe
from .platzierung_ergebnis import (
    Kind,
    Platzierung,
    PlatzierungsErgebnis,
    Richtung,
)
from .ports import (
    LBProvider,
    NormProvider,
    OibProvider,
    Platzierer,
    ProviderBundle,
    RaumProvider,
)
from .projekt_kontext import (
    Bundesland,
    Gebaeudeklasse,
    Gebaeudeteil,
    LageZurWohnung,
    Nutzungsart,
    ProjektKontext,
    RaumReferenz,
)
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
    "projekt_kontext": ProjektKontext,
    "oib_ergebnis": OibBefund,   # Port-Output; OibErgebnis/RaumReferenz als $defs
    "lb_vorgabe": LBVorgabe,
}

__all__ = [
    "SCHEMA_MODELS",
    "Ausgang",
    "BBox",
    "BereichsRegel",
    "Bundesland",
    "Edge",
    "ErkennungsweiteParameter",
    "FluchtwegSegment",
    "Gebaeudeklasse",
    "Gebaeudeteil",
    "Kind",
    "Klassifikation",
    "LBProvider",
    "LBVorgabe",
    "LageZurWohnung",
    "Node",
    "NormAnforderung",
    "NormProvider",
    "NormRegelwerk",
    "Nutzungsart",
    "OibBefund",
    "OibErgebnis",
    "OibProvider",
    "OibStufe",
    "Platzierer",
    "Platzierung",
    "PlatzierungsErgebnis",
    "ProjektKontext",
    "ProviderBundle",
    "Pruefung",
    "Raum",
    "RaumModell",
    "RaumProvider",
    "RaumReferenz",
    "RaumRegel",
    "Richtung",
    "RzStelle",
    "SonderLux",
    "SystemTyp",
    "Tuer",
    "Ueberwachung",
    "ZirkulationsGraph",
]
