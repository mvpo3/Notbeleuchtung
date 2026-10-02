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

#: Montage-Art (`Platzierung.montage_art`, MountingMethod). NB-R14 (PDF S.56):
#: „Notleuchten an Wänden hauptsächlich im Bereich von Stiegen; in normalen
#: Gangbereichen grundsätzlich an der Decke." → Stiegen-/Tür-/Ausgangs-RZ = Wand,
#: Gang-/Flächen-Leuchten (Aufheller/Antipanik) = Decke.
MONTAGE_WAND = "WA"     # Wandaufbau
MONTAGE_DECKE = "DA"    # Deckenaufbau

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


#: Owner-Regel 2026-09-18 (ersetzt R-C-Versatz ~150 mm): die Tür-Notleuchte sitzt
#: „in einer Linie mit der Wand, wo sich die Tür befindet" — es gibt KEINEN fixen
#: Sollwert-Versatz ins Rauminnere. Türposition (Selman) liegt auf der Wandachse
#: → Versatz 0 = Symbol auf der Wandlinie. Konstante bleibt als der EINE Regelort
#: (alle Tür-RZ-Sites konsumieren sie); Rotation Piktogramm-ins-Rauminnere (R-B)
#: ist davon unberührt.
RZ_INS_RAUM_MM = 0.0


#: Obergrenze „das ist noch eine TÜR" (Selmans Nennmaß-Türbereich endet bei 130 cm,
#: raumerkennung/tueren.py::_breite_mm 60–130). Breitere GEOMETRIE_OEFFNUNG-Durchgänge
#: sind Wandlücken, keine Türen (Owner-Befund Müllraum 2026-09-12).
TUER_MAX_BREITE_MM = 1300.0


def ist_echte_tuer(t) -> bool:
    """Phantom-Öffnungen von echten Türen trennen (EINE Quelle; Konsumenten:
    fachpraxis-Türwahl, sichtkette-Türbarrieren)."""
    breite = t.breite_mm
    if breite is not None and breite > TUER_MAX_BREITE_MM:
        return False
    return not (getattr(t, "ohne_tuerblatt", False) and breite is None)


#: Abteil-/Nebenraum-Typen, deren Gang-Türen nach AUSSEN (in den Gang) aufschlagen —
#: nur DIESE Türen sind Sichtbarrieren/Lücken-Trigger der Verlaufs-Kette (Punkt 2,
#: Owner-Bild Kellerabteil-Gang). Wohnungs-/Zimmertüren schlagen in den Raum und
#: sind lt. Fachdoku (S.8: „von den Wohnungstüren aus ist RZ (B) sichtbar") KEINE.
ABTEIL_TYPEN = {"ABSTELLRAUM", "KELLERABTEIL", "KELLER", "LAGER", "TECHNIK",
                "MUELLRAUM", "KINDERWAGENRAUM", "FAHRRADRAUM"}
#: Kleiner Nebenraum ohne klaren Typ zählt ab dieser Fläche NICHT mehr als Abteil.
_ABTEIL_MAX_M2 = 8.0


def ist_abteil_tuer(t, raeume_by_id: dict, korridor_ids: set) -> bool:
    """Tür verbindet einen Korridor mit einem Abteil-/kleinen Nebenraum
    (Aufschlag in den Gang) — die Sichtbarrieren-Klasse der Verlaufs-Kette."""
    if not ist_echte_tuer(t) or not t.breite_mm:
        return False
    seiten = {t.von_raum, t.nach_raum}
    if not (seiten & korridor_ids):
        return False
    ziel = next((x for x in seiten if x not in korridor_ids), None)
    r = raeume_by_id.get(ziel or "")
    if r is None:
        return False                                  # unbekannt → konservativ keine Barriere
    typ = (r.raum_typ or "").upper()
    if typ in ABTEIL_TYPEN:
        return True
    return bool(r.flaeche_m2) and r.flaeche_m2 < _ABTEIL_MAX_M2 and not typ.startswith("WOHN")


def rotation_piktogramm_in_raum(dx_zur_tuer: float, dy_zur_tuer: float) -> float:
    """R-B (Owner-Fachdoku „Notbeleuchtung zeichnen lernen" v2, S.3–5, AUSNAHMSLOS):
    jede Pfeil-unten-RZ an einer Tür wird so rotiert, dass das Piktogramm INS
    RAUMINNERE schaut — die flüchtende Person ist im Raum und muss es lesen
    (Blick = Gegenrichtung der Fluchtachse durch die Tür). Ersetzt die frühere
    Pfeil-zur-Tür-Ableitung (#111) an Tür-RZ; die Pfeilrichtung im 2D-Plan ist
    Darstellung, keine Gehrichtung (R-I).

    Input wie bisher an den Callsites vorhanden: (dx, dy) = Richtung ZUR/DURCH die
    Tür (Fluchtachse raus). Kalibriert am Ground-Truth-DXF Elektroplan DE EG
    (Nebenräume 0° · Hauseingang 0° · Müllraum-Südtür ~180°):
    Pfeil-Achse = Rauminnen-Normale = Gegenrichtung."""
    return rotation_zur_tuer(-dx_zur_tuer, -dy_zur_tuer)


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


# NB-R07: ab welchem Knickwinkel ein Fluchtweg-Punkt als Abzweig (Richtungs-
# wechsel) gilt — darunter ist es „geradeaus" (NB-R06). 45° trennt L-Ecken sauber
# von leichten Achsen-Verschwenkungen. Das IST zugleich das RW-007-Kriterium
# „Vorderseite sichtbar ≤ 45° zur Normalen": bei gerader Fortsetzung (≤45°)
# schaut die Vorderseite des down-Blocks die ankommende Person an; erst ein
# echter Abzweig (>45°) rechtfertigt den gerichteten links/rechts-Block.
ABZWEIG_COS = 0.707   # cos(45°)


def ist_abzweig(in_dx: float, in_dy: float, out_dx: float, out_dy: float) -> bool:
    """True, wenn sich die Laufrichtung am Punkt um > 45° ändert (Abzweig/Ecke).

    Einzige Quelle (Slice M3 2026-10-02): vorher privat in gang_strategy; jetzt
    geteilt, weil stgh_/anker_/communal_stgh dieselbe Frontalsicht-Regel brauchen.
    """
    li = math.hypot(in_dx, in_dy)
    lo = math.hypot(out_dx, out_dy)
    if li < 1.0 or lo < 1.0:
        return False
    return (in_dx * out_dx + in_dy * out_dy) / (li * lo) < ABZWEIG_COS


def frontalsicht_block(
    in_vec: tuple[float, float],
    out_vec: tuple[float, float],
    symbol_katalog_keys: list[str],
) -> tuple[str, float, bool, str]:
    """M3 / RW-007 (Mollgasse-PDF): Pfeiltyp nach der **Frontalsicht der ankommenden
    Person**, nicht nach dem reinen Fluchtvektor. `(catalog_key, rotation_deg,
    mirror_x, richtung)`.

    - **Gerade Fortsetzung** (Ankunft ≤45° zur Achse, `ist_abzweig`=False): down-Typ,
      Pfeil ENTGEGEN der Flucht (`rotation_piktogramm_in_raum`) → die Vorderseite
      schaut die ankommende Person an. richtung="unten".
    - **Echter Abzweig** (>45°): gerichteter links/rechts-Block, der den Weg zeigt
      (`richtung_und_rotation(out)` → `key_und_rotation`).

    `in_vec` = Ankunftsrichtung (von wo die Person kommt → zum Punkt), `out_vec` =
    Fluchtrichtung (Punkt → nächstes Ziel/Ausgang). Ist `in_vec` nicht ableitbar
    (|in|<1), fällt `ist_abzweig` auf False → sicherer down-Fallback. Wortgleich zur
    abgenommenen gang_strategy-Regel (NB-R06/R07, 710b859), damit beide EINE Quelle
    teilen; Guard: gang-Band + tests/platzierung/test_frontalsicht.py."""
    out_dx, out_dy = out_vec
    if ist_abzweig(in_vec[0], in_vec[1], out_dx, out_dy):
        richtung, _ = richtung_und_rotation(out_dx, out_dy)
        catalog_key, rotation, mirror_x = key_und_rotation(symbol_katalog_keys, richtung)
        return catalog_key, rotation, mirror_x, richtung
    catalog_key, _, _ = key_und_rotation(symbol_katalog_keys, "unten")
    return catalog_key, rotation_piktogramm_in_raum(out_dx, out_dy), False, "unten"


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


# Untergeschoss-Label-Familien (NB-R13, PDF S.43/54-55): Personen fluechten
# in UG-Geschossen HINAUF — die Stiegen-Fluchtrichtung kehrt sich gegenueber
# den Obergeschossen um. Erkannt wird das am Geschoss-Label (KG/UG/Keller);
# kein Projekt-Hardcode, nur das uebliche Label-Vokabular.
_UG_MARKER = ("KG", "UG", "KELLER", "UNTERGESCH")


def ist_untergeschoss(floor: str | None) -> bool:
    """True fuer Untergeschoss-Labels ("1KG", "2.UG", "Kellergeschoss", ...)."""
    if not floor:
        return False
    norm = floor.strip().upper()
    return any(m in norm for m in _UG_MARKER)
