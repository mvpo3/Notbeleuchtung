"""nutzungsklasse — statische Zuordnung raum_typ → Nutzungsklasse / Regel-Schlüssel.

Basiszuordnung je Kanon-Typ (docs/VOKABULAR.md §1). Verfeinerung „privat, weil
in Wohnung" (BAD/WC/VORRAUM) macht die Wohnungsbildung — hier steht nur der
statische Default. FAHRRAD ist bewusst KEIN Typ: Fahrrad-/Kinderwagenraum-
Stempel typen in `raumtyp.py` als ABSTELLRAUM.
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts.raum_modell import Nutzungsklasse

_MAP: dict[str, Nutzungsklasse] = {
    # WOHNUNG_PRIVAT — Räume innerhalb einer Wohnung. BAD/WC/VORRAUM sind hier
    # statisch privat; communale Fälle verfeinert die Wohnungsbildung.
    "ZIMMER": "WOHNUNG_PRIVAT",
    "SCHLAFZIMMER": "WOHNUNG_PRIVAT",
    "KINDERZIMMER": "WOHNUNG_PRIVAT",
    "WOHNZIMMER": "WOHNUNG_PRIVAT",
    "KÜCHE": "WOHNUNG_PRIVAT",
    "BAD": "WOHNUNG_PRIVAT",
    "WC": "WOHNUNG_PRIVAT",
    "ABSTELLRAUM": "WOHNUNG_PRIVAT",
    "VORRAUM": "WOHNUNG_PRIVAT",
    # ALLGEMEIN_ERSCHLIESSUNG — communale Fluchtweg-/Erschließungsflächen.
    "GANG": "ALLGEMEIN_ERSCHLIESSUNG",
    "STIEGENHAUS": "ALLGEMEIN_ERSCHLIESSUNG",
    "AUFZUGSVORPLATZ": "ALLGEMEIN_ERSCHLIESSUNG",
    # ALLGEMEIN_NEBENRAUM — communale Nebenräume.
    "KELLER": "ALLGEMEIN_NEBENRAUM",
    "TECHNIK": "ALLGEMEIN_NEBENRAUM",
    "GARAGE": "ALLGEMEIN_NEBENRAUM",
    "LAGER": "ALLGEMEIN_NEBENRAUM",
    "MUELLRAUM": "ALLGEMEIN_NEBENRAUM",
    "WASCHKÜCHE": "ALLGEMEIN_NEBENRAUM",
    # AUSSEN — Freibereiche (LOGGIA typt in raumtyp.py als BALKON).
    "BALKON": "AUSSEN",
    "TERRASSE": "AUSSEN",
    # KEIN_RAUM — nicht begehbare Flächen.
    "LIFT": "KEIN_RAUM",
    "SCHACHT": "KEIN_RAUM",
}

# raum_typ → heutiger Schlüssel in normwissen/data/raumtyp_regeln.yaml
# (STIEGENHAUS/GANG/SAAL/AUFENTHALTSRAUM). None = keine Regel ableitbar.
_REGELTYP: dict[str, str] = {
    "STIEGENHAUS": "STIEGENHAUS",
    "GANG": "GANG",
    # Quelle fehlt, Enis: KELLER/TECHNIK/GARAGE/LAGER/AUFZUGSVORPLATZ haben
    # heute keinen eigenen Regel-Schlüssel im Regelwerk → None (default greift).
}


def nutzungsklasse_fuer(raum_typ: str) -> Nutzungsklasse | None:
    """Kanon-Typ → Nutzungsklasse; None für leer/unbekannt (untypisiert)."""
    return _MAP.get(raum_typ)


def regeltyp_fuer(raum_typ: str) -> str | None:
    """Kanon-Typ → Regel-Schlüssel des heutigen Regelwerks, sonst None."""
    return _REGELTYP.get(raum_typ)
