"""bausteine — geteilte Grundbausteine ALLER Platzierungs-Strategien.

Architektur-Slice 2026-09-06 (Deletion-Test-Befund): diese Helfer lebten als
Unterstrich-Privates in `communal_stgh_strategy` bzw. verstreut in
`deckung`/`flaechen_strategy`/`sonderstellen_strategy` und wurden von 7 der 11
Package-Module quer importiert — eine verkappte Common-Lib unter falschem
Namen. Hier heißen sie öffentlich, die Strategien bleiben Strategien.
Implementierungen wortgleich umgezogen (kein Verhalten geändert).

Import-Regel: bausteine importiert NUR contracts (+stdlib) — nie eine Strategie.
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import NormProvider

#: Stromkreis-Feeder der Sicherheitsversorgung (AGV-<Gebäude>-F<n>).
AGV_SV_F = 13

# Zwei Bauteile annehmen, wenn die RZ-x-Spanne diese Lücke überschreitet.
BUILDING_SPREAD_MM = 20000.0

#: Raumtypen, die als Fluchtweg-Korridor verdichtet werden (Mittellinien-Nachweis).
KORRIDOR_TYPEN = {"GANG", "FLUR", "KORRIDOR"}

#: Sanitär-Raumtypen für den WC-Flächen-Trigger (OVE 718.560.9.001.AT Punkt 1).
WC_TYPEN = {"WC", "SANITAER", "SANITÄR", "BAD", "DUSCHE", "NASSRAUM"}


def richtung_und_rotation(dx: float, dy: float) -> tuple[str, float]:
    """Segment-Laufrichtung → (richtung, rotation_deg), auf die dominante Achse
    gerundet. Pfeil zeigt Richtung Ausgang (= Segment-Endpunkt)."""
    if abs(dx) >= abs(dy):
        return ("rechts", 0.0) if dx >= 0 else ("links", 180.0)
    return ("oben", 90.0) if dy >= 0 else ("unten", 270.0)


# Richtung → Key-Suffix des dediziert orientierten Pfeil-Blocks. 'oben' hat keinen
# eigenen Block (kein „nach oben" in der Lib) → Fallback via Rotation.
_RICHTUNG_SUFFIX = {"unten": "_unten", "links": "_links", "rechts": "_rechts"}


def select_key(symbol_katalog_keys: list[str], richtung: str) -> tuple[str, bool]:
    """Richtungs-spezifischen Pfeil-Block wählen, falls die Norm ihn anbietet.

    Rückgabe `(catalog_key, is_directional)`. `is_directional=True` heißt: der Block
    zeigt bereits in die Laufrichtung (links/rechts/unten) → der Platzierer setzt
    rotation/mirror auf 0/False. Sonst der erste Key + generative Rotation/Spiegelung.
    """
    keys = symbol_katalog_keys or ["notlicht_ks_stiege"]
    suffix = _RICHTUNG_SUFFIX.get(richtung)
    if suffix:
        for k in keys:
            if k.endswith(suffix):
                return k, True
    return keys[0], False


def building_assigner(x_coords: list[float]):
    """Cluster-Regel A|B aus der x-Verteilung der RZ (Original 2.46.3).
    A = westlich (kleineres x), B = östlich. Ein Cluster → alles A."""
    if x_coords and (max(x_coords) - min(x_coords) > BUILDING_SPREAD_MM):
        mid = (max(x_coords) + min(x_coords)) / 2.0
        return lambda x: "A" if x < mid else "B"
    return lambda _x: "A"


def referenz_anforderung(norm: NormProvider, klassifikation: str):
    """Erste Regelwerk-Anforderung der Klassifikation mit Symbol — oder None.

    ⚠️ FALLBACK (Enis-Review #95): die zurückgegebene `quelle` ist die der
    Referenz-Regel (§4.1/§4.2.1/§4.3.1) — NICHT der echte Auslöser der
    Pflichtstelle (§4.1.2 c/h/i bzw. §4.3.8/§4.4.1). Die Naht-Invariante
    `norm_quelle ∈ NormRegelwerk.quellen` lässt die echten Fundstellen heute
    nicht zu; Enis liefert Referenz-Anforderungen je Sonderstellen-Typ nach
    (eigener 3-Owner-PR). Bis dahin: Audit-Trail als Näherung lesen — der
    Pipeline-Summary trägt einen entsprechenden `hinweise`-Eintrag."""
    for regel in norm.regelwerk_snapshot().regeln:
        anf = regel.anforderung
        if anf.klassifikation == klassifikation and anf.symbol_katalog_keys:
            return anf
    return None
