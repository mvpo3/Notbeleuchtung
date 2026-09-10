"""bausteine — geteilte Grundbausteine ALLER Platzierungs-Strategien.

Architektur-Slice 2026-09-06 (Deletion-Test-Befund): diese Helfer lebten als
Unterstrich-Privates in `communal_stgh_strategy` bzw. verstreut in
`deckung`/`flaechen_strategy`/`sonderstellen_strategy` und wurden von 7 der 11
Package-Module quer importiert — eine verkappte Common-Lib unter falschem
Namen. Hier heißen sie öffentlich, die Strategien bleiben Strategien.
Implementierungen wortgleich umgezogen (kein Verhalten geändert).

Import-Regel: bausteine importiert NUR contracts + die ezdxf-freien
symbols-Mapping-/Orientierungs-Funktionen (+stdlib) — nie eine Strategie.
"""
from __future__ import annotations

import math

from notbeleuchtung.hauptengine.contracts import NormProvider
from notbeleuchtung.symbols.orientation import transformation as _transformation

#: Stromkreis-Feeder der Sicherheitsversorgung (AGV-<Gebäude>-F<n>).
AGV_SV_F = 13

# Zwei Bauteile annehmen, wenn die RZ-x-Spanne diese Lücke überschreitet.
BUILDING_SPREAD_MM = 20000.0

#: Raumtypen, die als Fluchtweg-Korridor verdichtet werden (Mittellinien-Nachweis).
KORRIDOR_TYPEN = {"GANG", "FLUR", "KORRIDOR"}

#: Sanitär-Raumtypen für den WC-Flächen-Trigger (OVE 718.560.9.001.AT Punkt 1).
WC_TYPEN = {"WC", "SANITAER", "SANITÄR", "BAD", "DUSCHE", "NASSRAUM"}

#: Toiletten-Scope §4.3.8 („Antipanik in Toiletten für Menschen mit Behinderung") —
#: EINE Quelle (W10/F05) für sonderstellen_strategy (Antipanik-Pflicht) UND validierung
#: (Prüfregel 12c). Vorher dreifach hartkodiert (sonderstellen + validierung, wertgleich
#: aber unabhängig → Drift-Risiko). Normativ pflegt Enis das Vokabular in
#: `normwissen/data/sonderstellen.yaml` (raumtypen_eindeutig/-mehrdeutig); bis eine
#: NormProvider-Query es exponiert (Handoff F15/F16, 3-Owner-Port), spiegelt diese
#: Konstante es consumer-seitig.
TOILETTE_EINDEUTIG = {"WC", "TOILETTE"}                  # belegt eine Toilettennutzung
TOILETTE_MEHRDEUTIG = WC_TYPEN - TOILETTE_EINDEUTIG      # Sanitär: weder Beleg noch Ausschluss


def rotation_zur_tuer(dx: float, dy: float) -> float:
    """Rotation des „Pfeil-unten"-Blocks, sodass der Pfeil in Richtung (dx, dy) zeigt —
    auf 90° gerastert, Ergebnis in [0, 360). Unten-Block-Basis 270° → ziel−basis ≡
    atan2(dy,dx)+90. Einzige Quelle der Owner-Regel #111 (F03/W16): vorher 4× wortgleich
    in anker/gang/fachpraxis/communal_stgh dupliziert."""
    return (round((math.degrees(math.atan2(dy, dx)) + 90.0) / 90.0) * 90.0) % 360.0


def richtung_und_rotation(dx: float, dy: float) -> tuple[str, float]:
    """Segment-Laufrichtung → (richtung, rotation_deg), auf die dominante Achse
    gerundet. Pfeil zeigt Richtung Ausgang (= Segment-Endpunkt).

    `rotation_deg` ist die Rotation des **unten-Pfeilblocks** (Block-Konvention,
    verifiziert in docs/REFERENZ_PLATZIERUNG.md §4: der Block zeigt bei rot=0
    nach −Y, Azimut 270°). Soll der Pfeil in Azimut A zeigen, gilt
    rotation = (A + 90) % 360 — dieselbe Formel wie die Tür-Regel (atan2 + 90°)
    und die `_ROT`-Tabelle der Sichtlinien-Strategie. Rotationsfix 2026-09-07:
    vorher wurde der Azimut PUR geschrieben (Pfeil zeigte A−90).
    Guard: tests/platzierung/test_rotation_konvention.py."""
    if abs(dx) >= abs(dy):
        return ("rechts", 90.0) if dx >= 0 else ("links", 270.0)
    return ("oben", 180.0) if dy >= 0 else ("unten", 0.0)


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


def key_und_rotation(
    symbol_katalog_keys: list[str], richtung: str
) -> tuple[str, float, bool]:
    """`(catalog_key, rotation_deg, mirror_x)` aus EINEM Rotationsrahmen.

    Slice 3.1 (Befund 3): der alte Fallback-Pfad drehte den „nach unten"-Block
    mit Achsen-Rotationen einer impliziten rechts-Basis („oben" renderte als
    „rechts") und spiegelte für „rechts" (Relikt der links-Basis-Ära). Jetzt:
    dedizierter Richtungs-Block → (key, 0, False); sonst rechnet
    `symbols.orientation.transformation` die Rotation aus der GEMESSENEN
    Block-Basis. Spiegelung ist nie nötig (alle drei Basen sind eigene Blöcke).
    """
    key, is_directional = select_key(symbol_katalog_keys, richtung)
    if is_directional:
        return key, 0.0, False
    rotation, mirror_x = _transformation(key, richtung)
    return key, rotation, mirror_x


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
