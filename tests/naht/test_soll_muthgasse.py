"""Soll-Tests Muthgasse 109B E2 — 4. erschlossene CAD-Familie (AIA-Layer, ODA-DWG).

Erschlossen 2026-09-07: WALL_PATTERN um ``(?<![A-Z])[AI]-WALL`` erweitert,
Faktor-Kalibrierung über Tür-ARCs aus A-DOOR-Blöcken (virtual_entities — die
Modelspace-ARCs sind Kurvenwände, ×10-Falle), A-AREA-BNDY als Raum-Layer,
'Ker.Bel.' im Belag-Vokabular, A-FLOR/A-CLNG/Q-SPCQ in der Wandkörper-
Negativliste.

Ist-Stand (selbst gemessen, Provider-Parse E2): factor 10.0 · 4 Wand-Layer ·
98/98 Stempel mit Fläche+Typ (85 mit Belag) · 737 Wandkörper · 114 Räume
(seit der Typ-Rückschreibung in der Kaskade ≥ 90 typisiert, vorher 34) ·
291 Türen · 5 stair_exit / 5 final_exit (vor dem Fahnen-Ausschluss 12 / 0)
· 143 Segmente (139 LINIE) · 9 Stiegenhäuser. Bänder knapp unter Ist —
dürfen nur wachsen.

Türzahl-Korrektur 2026-09-10: 308 → **291** Türen. Die 83 Beschriftungs-Fahnen
(``HNP_Beschriftung Türen … Durchgangslichte…``, keine Türgeometrie) fallen aus
``_DOOR_EXCLUDE``; an ihren Stellen entstehen 66 echte ``durchgang``/``text:``-
Türen neu, weil deren Sperrwirkung wegfällt. Gemessen, nicht abgeleitet
(Provider-Parse E2, 825,6 s): 291 Türen, 113 Räume, 205 typisiert = 70,5 %.
Nebenwirkung, gemessen und NICHT geglättet: stair_exit fällt von 12 auf 5.
Nachmessung 2026-09-10 (zwei Provider-Parses derselben DXF, Stand ``0d7c5db``
vs. ``1d9c03a``): die früher behaupteten „3 echten Türen, die ihre Typisierung
verloren haben" gibt es **nicht** — die 3 war eine Saldo-Zahl (15 Kandidaten
vorher − 5 Fahnen − 7 nachher), keine Menge. Lagebezogen sind 11 Ausgänge weg,
1 geblieben, 4 neu. Von den 11 waren 5 Beschriftungs-Fahnen und 6 Kontaktzonen-
Artefakte aus ``durchgaenge_ohne_tuerblatt`` (Breiten bis 4862 mm — es gibt kein
4,8-m-Türblatt), entstanden zwischen dem Artefakt-Raum ``raum_88`` (vorher 693
Polygonpunkte, 41,3 m², überlappte fünf STIEGENHAUS-Polygone zu 28–41 % und
``raum_79``/LIFT zu 99 %) und den Räumen, die er überdeckte. Kein Regressions-
fehler in ``tuer_typisierung.py`` (zwischen beiden Ständen byte-identisch).

Nachtrag 2026-09-12 (SCHLEUSE-Typisierung, ``raumerkennung/kuerzel_entscheid``):
die Zahlen oben bleiben als Ist ihres Standes stehen. Neu gemessen, nachdem
``raum_65`` (Stempelnummer ``E2-VF-11a``) als SCHLEUSE typisiert wird:
**101 Stempel** -- 99 mit Typ, dazu 2 bewusst TYPLOSE Kuerzel-Stempel
»Schl.« (die Invariante "jeder Stempel traegt einen Typ" gilt damit nicht
mehr; das Band ``>= 98`` bleibt unveraendert) · **7 stair_exit** statt 5 (neu
``exit_tuer_50`` und ``exit_durchgang_141``, beide an ``raum_65``) ·
5 final_exit · **209/291 Tueren typisiert = 71,8 %** statt 205/291 ·
**148 Segmente** statt 143 · 113 Raeume, 104 typisiert · 9 Stiegenhaeuser.
Kein Band nachgezogen, kein xfail gedreht: 7 < 9, kein stair_exit sitzt auf
einer echten Blocktuer, 71,8 % < 90 %.

Nachtrag 2026-09-12 zur Zeile "7 < 9": der Ist nach der Bereinigung ist **6**,
nicht 7 -- die 7 war der Zwischenstand nach der SCHLEUSE-Typisierung, VOR der
Bereinigung; ``exit_durchgang_141`` ist mit den 21 Kontaktzonen-Durchgaengen
weggefallen. Belege: Projekte/_ergebnis/VERLAUF.md (Lauf 2026-09-12, 6ebf676:
"Ausgaenge final_exit:5 stair_exit:6"), Projekte/_ergebnis/Muthgasse_E2/
bericht.md Abschnitt "## Ausgaenge (11)" mit 6 stair_exit-Zeilen
(``exit_tuer_50``, ``exit_tuer_118``, ``exit_durchgang_123/144/147/148``),
docs/ENIS_UEBERGABE_0908.md § 21.4. 6 < 9 -- Band unveraendert.

Nachtrag 2026-09-12 (Tuerband abgeloest, Owner-Entscheidung iii): das alte
``test_soll_tuerzahl_band`` (strict-xfail, >= 280 Tueren) ist ENTFERNT und durch
``test_soll_plan_tuerbloecke_vorhanden`` / ``test_soll_plan_tuerbloecke_im_modell``
(scharf) plus ``test_soll_jeder_plan_tuerblock_ist_tuer`` (strict-xfail) ersetzt.
Nicht abgesenkt, sondern ersetzt: die 280 stammte selbst aus einem alten Ist
(291) und fiel mit jeder Aenderung an den Kontaktzonen-Durchgaengen mit. Die
Zahlen des alten Bandes bleiben als Nachtrag stehen: Tueren **291 -> 270**,
darin ``durchgang_*`` **169 -> 148** (-21, ausschliesslich Kontaktzonen-
Durchgaenge aus ``durchgaenge_ohne_tuerblatt``, ``_KONTAKT_MM`` = 250 mm),
waehrend ``tuer_*`` unveraendert **121** und ``aussenoeffnung_*`` unveraendert
**1** blieben (Ursache: Raumbereinigung, docs/ENIS_UEBERGABE_0908.md § 14.6.1,
Commit 6ebf676). Die neue Groesse zaehlt echte Blocktueren der ZEICHNUNG statt
abgeleiteter Oeffnungen und ist gegen genau diese Bereinigung stabil: die
maximale 1:1-Paarung der 72 Plan-Tuerbloecke gegen die 121 ``tuer_*`` liefert
+-2 mm 13 | <= 250 mm 13 | <= 500 mm 44 | <= 1000 mm 59 | <= 1500 mm 63 --
identisch vor (291 Tueren) und nach (270 Tueren) der Bereinigung. Diese
Staffelung ist 2026-09-12 selbst nachgerechnet (Nachmessung am Ende dieses
Docstrings, Punkt 4).

Was die neue Groesse NICHT abdeckt (gemessen, nicht geglaettet):
- die **148 Kontaktzonen-Durchgaenge** (``durchgang_*``) haben keinen
  Plan-Beleg; die Paarung laeuft nur gegen ``tuer_*``, sie werden also weder
  belohnt noch bestraft.
- **Schiebetueren und Durchgangszargen ohne Schwenkbogen**: 16 der 88
  ``A-DOOR``-INSERTs tragen keinen Tuerblatt-ARC und fallen damit aus der
  Plan-Groesse (nachgerechnet: 3x Durchgangszarge ``HNP_T_DG``, 4x Schiebetuer
  -- 1x ``TU_SF_1``, 3x ``HNP_T80_1T…1SF`` --, 1x Varianten-Schiebetuer,
  7 weitere Varianten-Duplikate mit Suffix ``E2_1-23c``/``E2_2-23``, 1 Grenzfall).
- **Fenstertueren auf A-GLAZ** sind bewusst draussen (Begruendung in
  ``_plan_tuerbloecke``), darunter 3x ``FE TUER 2 tlg``.
- die vier Bloecke auf ``A-GENM``/``A-GENM-HDLN`` (``tuer_18/19/20/21``) sind
  **vom Plan-Filter bewusst ausgeschlossene Marker und Montageoeffnungen** --
  KEINE Deckungsluecke. Korrektur 2026-09-12 (gemessen): es sind keine
  Tuerblaetter. ``tuer_18/19`` sitzen auf
  ``2D_barrierefrei_Türbereich 150_200 - r75`` (``A-GENM``, ein
  Barrierefrei-Marker), ``tuer_20/21`` auf
  ``HNP_Wanddurchbruch - WDB Montageöffnung`` (``A-GENM-HDLN``, zwei
  Montageoeffnungen). Die ID-Zuordnung stammte unveraendert aus dem Altbestand
  und ist 2026-09-12 nachgemessen und bestaetigt: Abstand Fremdlayer-Block zu
  Modelltuer je **0,00 mm**, naechste andere Modelltuer jeweils > 970 mm weg
  (Nachmessung am Ende dieses Docstrings, Punkt 3).
  Sie entstehen ueberhaupt nur, weil ``_DOOR_HINT`` die
  Token ``TÜR``/``ÖFFNUNG`` im Namen findet. Die frueher hier stehende Lesart
  ("4 Block-Tueren auf Fremdlayern, die der Layerfilter nicht sieht") bleibt
  als ueberholte Angabe genannt.
- **Typisierung, Notausgangs-Flag und Ausgaenge** prueft sie nicht -- dafuer
  stehen die eigenen Zielbilder weiter unten.
Beleg-Lage der 121 ``tuer_*`` selbst (gemessen, Feld ``quelle``): **64** haben
einen geometrischen oder Tuerlisten-Beleg -- 18 Block auf A-DOOR/A-GLAZ, 4 Block
auf A-GENM*, 28 ARC mit Breite, 14 Tuernummer ``T-E2-*`` --, die restlichen
**57** nur ein Raumnummern-Token.

Nachmessung 2026-09-12 (EIN Provider-Parse E2, 716,3 s; die Rohdaten des Laufs
sind EINMAL serialisiert und alle Zahlen unten daraus gerechnet, kein zweiter
Parse). Anlass: die Untergrenze der ``arc_aussen``-Spanne stand hier zweimal
als exakter Wert mit zwei Dezimalstellen, war in dieser Datei aber nie selbst
gemessen -- eine Fremdangabe. Lauf-Stand: 270 Tueren (121 ``tuer_*`` ·
148 ``durchgang_*`` · 1 ``aussenoeffnung_*``), 72 Plan-Tuerbloecke, factor 10,0.
Ergebnis: die fuenf nachgemessenen Angaben BESTAETIGEN sich, eine sechste
(die "103") ist widerlegt und oben korrigiert.

1. ``tuer_48`` -> naechster Plan-Tuerblock **399,81 mm** -- genau der Wert, der
   hier stand, jetzt selbst gemessen. ``tuer_48`` liegt bei 325773 / 99550,
   ``quelle='arc_aussen+text:T-E2-11-01-1'``; dass sie im Bericht
   ``tuer_ins_nichts`` ist (beide Seiten KEIN_RAUM), aendert den Abstand nicht.
2. alle **28** ``arc_aussen``-Tueren zum naechsten Plan-Tuerblock: min
   **399,81 mm** (``tuer_48``), Median **405,96 mm**, max **780,57 mm**
   (``tuer_50``); **keine** unter 250 mm -- der kleinste Abstand UNTER DIESEN
   28 ist die 399,81. Korrektur 2026-09-12: hier stand "der kleinste Abstand
   ueberhaupt" -- das ist falsch. Ueber ALLE 121 ``tuer_*`` ist der kleinste
   Abstand 0,105 mm (``tuer_6``), und 13 liegen innerhalb 2 mm (dieselbe 13
   wie in der Paarung). Der Satz gilt nur innerhalb der 28.
   Das bisherige "Median 406" war gerundet richtig, gemessen sind
   405,96 mm (die beiden Mittelwerte der 28 sind 405,95 und 405,96). Die
   780,57 deckt sich mit docs/ENIS_UEBERGABE_0908.md § 13.7 (dort 780,5 mm):
   dieselbe Tuer, derselbe Nachbarblock ``HNP_T_BZ_2-DF``, nur gegen die 209
   ``A-DOOR``/``A-GLAZ``-INSERTs statt gegen die 72 Plan-Tuerbloecke gemessen.
   Die Gegenpruefung aus den Bericht-Koordinaten (780,53 / 781,73 mm) weicht
   ab, weil bericht.md die Lagen auf 10 mm rastert -- 780,57 ist der Wert aus
   den ungerasterten Modell-Koordinaten (334452,75 / 106402,82).
3. Zuordnung der vier Fremdlayer-Bloecke bestaetigt, Abstand je **0,00 mm**:
   ``tuer_18`` (319987 / 108509) und ``tuer_19`` (321346 / 89888) auf den zwei
   ``A-GENM``-Barrierefrei-Markern, beide ``breite_mm=750,0`` mit
   ``breite_quelle='BLOCKNAME'``; ``tuer_20`` (330461 / 105785) und ``tuer_21``
   (330706 / 99453) auf den zwei ``A-GENM-HDLN``-Montageoeffnungen, beide
   ``breite_mm=None`` / ``UNBEKANNT``. Eindeutig, weil die naechste ANDERE
   Modelltuer jeweils > 970 mm entfernt liegt.
4. Paarungs-Staffelung nachgerechnet, unveraendert: +-2 mm 13 | <= 250 mm 13 |
   <= 500 mm 44 | <= 1000 mm 59 | <= 1500 mm 63 von 72.
5. **14** der 72 Plan-Tuerbloecke haben einen ``durchgang_`` <= 250 mm und
   keine ``tuer_`` -- unveraendert. Gegenzahl aus demselben Lauf: 13 Bloecke
   haben eine ``tuer_`` <= 250 mm, was zur +-2-mm-Paarung von 13 passt.
6. KORREKTUR: das "``± 2-mm-Band`` wuerde 103 der 121 realen Tueren als nicht
   plan-belegt behandeln" ist falsch -- gemessen sind es **108** (13 der 121
   ``tuer_*`` sitzen innerhalb 2 mm eines Plan-Tuerblocks). Die 103 bleibt an
   ihrer Stelle als ueberholte Angabe zitiert.
7. Nebenbei im selben Lauf nachgezaehlt und unveraendert: die Beleg-Lage der
   121 ``tuer_*`` oben -- 22 ``block`` (18 auf A-DOOR/A-GLAZ + 4 auf A-GENM*),
   28 ``arc_aussen``, 71 ``text``, davon 14 mit Tuernummer ``T-E2-*``; also
   64 mit Beleg, 57 ohne.

Nachtrag 2026-09-12 (Gegenrechnung): die "23 von 1730 Modelspace-INSERTs" und
die Familien-Aufschluesselung standen hier als NICHT messbar -- das war ein
Fehlschluss ("nicht im Cache" ist nicht "nicht messbar"): sie brauchen keinen
Provider-Parse, nur ``lade_dxf`` (8 s) plus ``_ist_tuer_block``. Gemessen:
1730 Modelspace-INSERTs, 23 Treffer (A-DOOR 15, A-GLAZ 4, A-GENM 2,
A-GENM-HDLN 2); Familien der 72 = 37 ``HNP_T_UZ_1-DF`` / 17 ``HNP_T_BZ_1-DF``
/ 13 ``TU DF 1`` / 5 ``HNP_T_BZ_2-DF``, davon 0/13/0/0 erkannt = 13 von 72;
13 Namen tragen ``WET``, alle 13 erkannt. Die frueher notierte Reihenfolge
"37/13/5/17" war vertauscht, richtig ist 37/17/13/5. Betroffen ist der
xfail-Grund von
``test_soll_jeder_plan_tuerblock_ist_tuer`` -- beides braucht Zahlen ueber ALLE
Modelspace-INSERTs, die dieser Lauf nicht serialisiert hat.

Nebenbefund, gemessen aber NICHT zuordenbar: derselbe Lauf liefert **109
Raeume**, nicht die 113 des SCHLEUSE-Nachtrags oben. Der Arbeitsbaum trug dabei
fremde, unfertige Aenderungen zweier parallel laufender Auftraege an
``bereinigung.py`` (SHA256 f3164795718c…) und ``kaskade.py`` (a68139c9ff74…).
Die 113 bleibt darum als Angabe ihres Standes stehen; die 109 ist KEINE
Korrektur, sondern ein Messwert auf unklarem Code-Stand. Die Tuer-Seite ist
davon unberuehrt: 270 / 121 / 148 sind genau die Zahlen des dokumentierten
Stands nach der Bereinigung, darum gelten die Punkte 1-7 unabhaengig davon.
"""
import math
import re
from pathlib import Path

import pytest

PLAN = Path("Projekte/_eingang/Muthgasse_E2.dxf")


def _skip_ohne_plan():
    if not PLAN.exists():                        # pragma: no cover — CAD-Asset fehlt
        pytest.skip(f"Architekturplan nicht vorhanden: {PLAN}")


@pytest.fixture(scope="module")
def plan():
    _skip_ohne_plan()
    from notbeleuchtung.raumerkennung.dxf_load import lade_dxf

    return lade_dxf(str(PLAN))


@pytest.fixture(scope="module")
def rm(plan):
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    return ArchitekturRaumProvider().parse(str(PLAN), "E2")


# ── scharf: Erschließung der Familie ────────────────────────────────────────

def test_soll_faktor_kalibrierung_x10(plan):
    """Kalibrierungs-Falle: Kurvenwand-ARCs (600–1300 Quell-Einheiten) dürfen den
    Faktor nicht auf ×1 ziehen — Tür-Bögen aus A-DOOR-Blöcken entscheiden."""
    assert plan.factor == 10.0, f"Faktor {plan.factor} statt 10.0 (×10-Falle)"


def test_soll_wand_layer_erkannt(plan):
    assert {"A-WALL", "I-WALL"} <= set(plan.wall_layers), (
        f"AIA-Wand-Layer fehlen: {sorted(plan.wall_layers)}"
    )


def test_soll_98_stempel_mit_flaeche_und_typ(plan):
    from notbeleuchtung.raumerkennung.stempel_anker import finde_stempel

    st = finde_stempel(plan)
    assert len(st) >= 98, f"nur {len(st)} Stempel (Ist 98)"
    assert sum(1 for s in st if s.flaeche_m2) >= 98, "Stempel ohne Fläche"
    assert sum(1 for s in st if s.typ) >= 98, "Stempel ohne Typ"
    assert sum(1 for s in st if s.belag) >= 80, "Belag-Spur ('Ker.Bel.') eingebrochen"


def test_soll_wandkoerper_band(plan):
    from notbeleuchtung.raumerkennung.wandkoerper import finde_wandkoerper

    wk = finde_wandkoerper(plan)
    assert len(wk) >= 650, f"nur {len(wk)} Wandkörper (Ist 737)"


def test_soll_raeume_tueren_ausgaenge(rm):
    """Ohne die Türzahl — die stand seit 2026-09-12 in
    ``test_soll_tuerzahl_band`` (strict-xfail mit Beleg), damit dieses Band
    scharf bleibt, statt am Türband mitzufallen.

    Nachtrag 2026-09-12: ``test_soll_tuerzahl_band`` ist entfernt, die Türzahl
    steht jetzt als Plan-Größe in ``test_soll_plan_tuerbloecke_im_modell``
    (Begründung im Modul-Docstring). Ohne Türzahl bleibt dieses Band aus
    demselben Grund wie vorher."""
    assert len(rm.raeume) >= 98, f"nur {len(rm.raeume)} Räume (Ist 114)"
    assert len(rm.zirkulation.segmente) >= 100, (
        f"nur {len(rm.zirkulation.segmente)} Segmente (Ist 143)"
    )
    assert len(rm.stiegenhaeuser) >= 5, (
        f"nur {len(rm.stiegenhaeuser)} Stiegenhäuser (Ist 9)"
    )


# ── Plan-Türblöcke: Soll-Größe aus der ZEICHNUNG (löst das Türzahl-Band ab) ──

#: Revit-Türfamilien dieses Plans. ``^``-verankert, darum matchen die
#: Fensterfamilien „Fenster 1-flg…", „FE 1 tlg…" und „FE TÜR 2 tlg…" NICHT.
_TUERFAMILIE = re.compile(r"^(HNP_T[_0-9]|TU[ _]|T(?:Ü|UE)R)", re.IGNORECASE)

#: Modell-Türen mit eigener Türgeometrie (Block/ARC/Text). ``durchgang_*``
#: (Kontaktzonen ohne Türblatt) und ``aussenoeffnung_*`` sind ausgenommen.
_TUER_ID = re.compile(r"tuer_\d+$")


def _plan_tuerbloecke(plan):
    """Positionen echter Türblöcke der ZEICHNUNG, auf 1 mm gerundet.

    Drei Filter, alle gemessen: Layer ``A-DOOR`` · Revit-Türfamilie
    (``_TUERFAMILIE``) · die Blockdefinition trägt einen Türblatt-ARC im
    exklusiven Band des Codes (``tueren._ARC_MIN_MM < r < tueren._ARC_MAX_MM``,
    rekursiv über verschachtelte Blockdefs, Tiefe ≤ 2). Reine Plan-Größe:
    unabhängig von Räumen, F-Flutung und Kontaktzonen — und damit stabil gegen
    die Raumbereinigung, an der das alte Türzahl-Band fiel.

    Ist 2026-09-12 (Provider-Parse E2): **72 INSERTs auf 72 verschiedenen
    Positionen**, alle im Planbereich (BBox Wandkörper-Zentren ∪ Raumpolygone
    + 2000 mm Rand, gemessen 0 außerhalb) — darum steht hier kein Lage-Filter.
    Türblatt-Radien auf ``A-DOOR``: 800 mm 52× · 900 mm 14× · 950 mm 5× ·
    655 mm 3× · 700 mm 1× — die Liste summiert auf **75**, nicht auf 72, weil
    sie Radien je INSERT zählt und drei zweiflügelige Blöcke
    (``HNP_T_BZ_2-DF … 2DF_150_5x200``, gemessen) je ZWEI verschiedene
    In-Band-Radien tragen (655 UND 900 mm). Familien:
    ``HNP_T_UZ_1-DF`` 37× · ``HNP_T_BZ_1-DF`` 17× · ``TU DF 1`` 13× ·
    ``HNP_T_BZ_2-DF`` 5×.

    Warum ``A-GLAZ`` NICHT mitzählt: von den 153 INSERTs auf
    ``A-DOOR``/``A-GLAZ`` mit ARC im Türblatt-Band liegen **81 auf A-GLAZ und
    sind Fenster** (60× „Fenster 1-flg - Variabel - Standard", 18× „FE 1 tlg -
    konfigurierbar", 3× „FE TÜR 2 tlg") — ein Fensterflügel-Bogen ist kein
    Türblatt. Nur die 72 auf ``A-DOOR`` sind Türfamilien. Der Namensfilter
    ändert auf ``A-DOOR`` nichts (gemessen: Layer+ARC = Layer+Name+ARC = 72);
    er steht hier, damit eine künftige Fensterfamilie auf ``A-DOOR`` nicht
    mitgezählt wird.

    Nicht enthalten (Details im Modul-Docstring): die 16 ``A-DOOR``-INSERTs
    ohne Türblatt-ARC — Durchgangszargen, Schiebetüren, Varianten-Duplikate und
    ein Grenzfall ``HNP_T38…_1DF_130x200`` (Rohradius 130.0000000000001 →
    1300.0000000000011 mm, fällt knapp aus dem exklusiven Band; erst ein
    rundungstolerantes Band machte daraus 73 statt 72 — 72 ist die
    code-konsistente Zahl).

    Annahme dieses Helfers, gemessen und bewusst nicht abgesichert: er liest
    die Blockdefinition ROH über ``plan.doc.blocks``, während der
    Produktionspfad ``tueren._blattbreite_aus_block`` die ``virtual_entities``
    MIT Insert-Skalierung liest. Auf diesem Plan ist das folgenlos — alle 88
    ``A-DOOR``-INSERTs haben Skalierung 1,0, und beide Wege liefern dieselben
    72 Positionen (symmetrische Differenz 0). Auf einem Plan mit skalierten
    Inserts liefen sie auseinander.
    """
    from notbeleuchtung.raumerkennung import tueren

    cache: dict[tuple[str, int], list[float]] = {}

    def radien(name: str, tiefe: int = 0) -> list[float]:
        key = (name, tiefe)
        if key in cache:
            return cache[key]
        cache[key] = []          # Rekursionsbremse bei zyklischer Blockreferenz
        blk = plan.doc.blocks.get(name)
        out: list[float] = []
        if blk is not None:
            for e in blk:
                if e.dxftype() == "ARC" and e.dxf.radius > 0:
                    out.append(float(e.dxf.radius) * plan.factor)
                elif e.dxftype() == "INSERT" and tiefe < 2:
                    out += radien(str(e.dxf.name), tiefe + 1)
        cache[key] = out
        return out

    aus = set()
    for e in plan.space:
        if e.dxftype() != "INSERT" or str(e.dxf.layer) != "A-DOOR":
            continue
        name = str(e.dxf.name)
        if not _TUERFAMILIE.match(name):
            continue
        if not any(tueren._ARC_MIN_MM < r < tueren._ARC_MAX_MM for r in radien(name)):
            continue
        xy = plan._scale(e.dxf.insert)
        aus.add((round(xy[0]), round(xy[1])))
    return aus


def _paarung(positionen, modell_tueren, tol_mm):
    """Maximale 1:1-Zuordnung Plan-Position → Modell-Tür mit Abstand ≤ ``tol_mm``.

    1:1 ist der Punkt: bei bloßem „hat irgendeine Tür in Reichweite" bekämen
    zwei Plan-Türblöcke dieselbe Modell-Tür gutgeschrieben. Gemessen tritt der
    Unterschied ab 1000 mm auf (61 Positionen mit Kandidat, aber nur 59
    paarbar); bei 500 mm sind beide 44.

    Kuhn (ungarische Methode, augmentierende Pfade) — exakt, also eine echte
    Zahl und keine Untergrenze. Bei 72 Positionen ist die Laufzeit belanglos.
    """
    pos = list(positionen)
    adj = [[t.id for t in modell_tueren
            if math.dist(p, (t.xy_mm[0], t.xy_mm[1])) <= tol_mm] for p in pos]
    paar: dict[str, int] = {}

    def belege(i: int, gesehen: set[str]) -> bool:
        for tid in adj[i]:
            if tid in gesehen:
                continue
            gesehen.add(tid)
            if tid not in paar or belege(paar[tid], gesehen):
                paar[tid] = i
                return True
        return False

    return sum(1 for i in range(len(pos)) if belege(i, set()))


def test_soll_plan_tuerbloecke_vorhanden(plan):
    """Klammer für das Zielbild unten — sonst könnte es xfailen, weil die
    Grundmenge weggebrochen ist, statt weil die Zuordnung fehlt.

    Ist 2026-09-12: 72 Positionen (Messung und Filter siehe
    ``_plan_tuerbloecke``)."""
    bloecke = _plan_tuerbloecke(plan)
    assert len(bloecke) >= 70, f"nur {len(bloecke)} Plan-Türblöcke (Ist 72)"


def test_soll_plan_tuerbloecke_im_modell(plan, rm):
    """Ersatz für das abgelöste ``test_soll_tuerzahl_band``: gezählt wird nicht,
    wie viele Türen das Modell erzeugt, sondern wie viele der 72 Türblöcke des
    PLANS es trifft — eine Größe, die die Zeichnung vorgibt, kein altes Ist.

    Ist 2026-09-12: **44** von 72, maximale 1:1-Paarung gegen die 121
    ``tuer_*`` bei 500 mm Toleranz (am 2026-09-12 selbst nachgerechnet,
    Modul-Docstring Punkt 4). Identisch vor (291 Türen) und nach (270)
    der Raumbereinigung — genau die Stabilität, die der 280er-Zählung fehlte.

    Warum 500 mm und nicht ± 2 mm: bei der ARC-Quelle sitzt die Modell-Tür am
    **Drehpunkt** des Schwenkbogens, der Plan-Block an seinem
    **Einfügepunkt**. Gemessen liegen alle 28 ``arc_aussen``-Türen
    **399,8–780,6 mm** von einem Plan-Türblock entfernt (Median 406) und
    **keine** innerhalb 250 mm. Präzisierung 2026-09-12 der früheren Spanne
    „400–800 mm": exakt 399,81 mm (``tuer_48``) bis 780,57 mm (``tuer_50``) —
    die Untergrenze lag knapp unter 400 mm. Nachmessung 2026-09-12 (eigener
    Provider-Parse, Modul-Docstring Punkt 2): alle vier Werte sind jetzt selbst
    gemessen und bestätigt, der Median exakt **405,96 mm** — die 406 war
    gerundet, die 399,81 bis dahin eine Fremdangabe.
    Ein ± 2-mm-Band würde **108** der 121
    realen Türen als „nicht plan-belegt" behandeln — es prüfte den Versatz,
    nicht die Erkennung. Korrektur 2026-09-12 (gemessen): **108**, nicht die
    hier zuvor genannten **103** — gemessen sitzen 13 der 121 ``tuer_*``
    innerhalb 2 mm eines Plan-Türblocks, also 121 − 13 = 108; es ist dieselbe
    13 wie in der ± 2-mm-Paarung. Die 103 bleibt als überholte Angabe genannt,
    ihre Herkunft ist mit der Nachmessung 2026-09-12 geklärt: **121 − 18 =
    103**, und die **18** ist die Blocktür-Zahl dieser Datei selbst. Die 103
    verwechselt also die 18 echten Blocktüren mit den 72 Plan-Türblöcken —
    zwei verschiedene Kriterien. Die frühere Angabe „Herkunft unbekannt,
    weder 121 − 13 noch 121 − 18" ist damit überholt (121 − 18 ergibt genau
    103). Der ± 2-mm-Wert steht darum als Zielbild darunter,
    nicht hier.
    """
    bloecke = _plan_tuerbloecke(plan)
    modell = [t for t in rm.tueren if _TUER_ID.match(t.id)]
    n = _paarung(bloecke, modell, 500.0)
    assert n >= 40, (
        f"nur {n} von {len(bloecke)} Plan-Türblöcken mit eigener Modell-Tür "
        f"≤ 500 mm (Ist 44/72, {len(modell)} tuer_* im Modell)")


# ── Zielbilder ──────────────────────────────────────────────────────────────

@pytest.mark.xfail(
    strict=True,
    reason="Soll: jeder Plan-Türblock trägt eine eigene Modell-Tür an seiner "
    "Position (± 2 mm) — Ist Muthgasse E2 2026-09-12: 13 von 72 (maximale "
    "1:1-Paarung gegen die 121 tuer_*). Der Sollwert kommt aus dem PLAN (72 "
    "A-DOOR-INSERTs mit Türblatt-ARC, siehe _plan_tuerbloecke), NICHT aus einem "
    "Ist — das unterscheidet ihn von der abgelösten 280er-Türzahl. Zwei "
    "gemessene Ursachen: (1) Drehpunkt gegen Einfügepunkt — alle 28 "
    "arc_aussen-Türen liegen 399,8–780,6 mm neben ihrem Plan-Türblock (Median "
    "406; exakt 399,81 mm tuer_48 bis 780,57 mm tuer_50 — Präzisierung "
    "2026-09-12 der früheren Spanne 400–800 mm), keine unter 250 mm — am "
    "2026-09-12 selbst nachgemessen, Median exakt 405,96 mm; "
    "(2) _ist_tuer_block() trifft nur 23 von "
    "1730 Modelspace-INSERTs und nur 13 der 72 Plan-Türblöcke, weil die "
    "tragenden Türfamilien dieses Plans keinen Token aus _DOOR_HINT/_AUSSENTUER "
    "enthalten: HNP_T_UZ_1-DF (37 der 72, davon 0 erkannt), 'TU DF 1 - "
    "Umfassungszarge flächenbündig' (13, davon 0), HNP_T_BZ_2-DF (5, davon 0) — "
    "nur HNP_T_BZ_1-DF wird über 'WET' aus _AUSSENTUER erkannt (13 von 17). "
    "Deren Türen entstehen darum erst über ARC- und Text-Quellen und damit "
    "versetzt. Die Zahlen in (2) — 23 von 1730 und 13 von 17 über WET — "
    "sind am 2026-09-12 nachgemessen und bestätigt (1730 Modelspace-INSERTs, "
    "23 Treffer: A-DOOR 15, A-GLAZ 4, A-GENM 2, A-GENM-HDLN 2). Korrektur: "
    "die Familien-Kurzform lautet 37/17/13/5, nicht das hier zuvor genannte "
    "37/13/5/17 — die Aufzählung im Satz davor ist richtig. Ebenfalls selbst "
    "gemessen: die 13 von 72 (± 2-mm-Paarung).",
)
def test_soll_jeder_plan_tuerblock_ist_tuer(plan, rm):
    """Fachliches Zielbild der Türerkennung: der Plan zeichnet 72 Türblätter,
    also soll das Modell an 72 Positionen eine Tür führen — positionsgenau, denn
    ein Türblock IST die Tür, nicht bloß ein Hinweis auf eine in der Nähe.

    Gegenprobe zur Einordnung des Ist (gemessen, siehe Modul-Docstring):
    14 der 72 Plan-Türblöcke haben nur einen ``durchgang_`` ≤ 250 mm und keine
    ``tuer_`` — dort zeichnet der Plan ein Türblatt, das Modell führt eine
    Kontaktzone ohne Türblatt. Am 2026-09-12 selbst nachgerechnet: 14,
    unverändert (Modul-Docstring Punkt 5).
    """
    bloecke = _plan_tuerbloecke(plan)
    modell = [t for t in rm.tueren if _TUER_ID.match(t.id)]
    n = _paarung(bloecke, modell, 2.0)
    assert n == len(bloecke), (
        f"nur {n} von {len(bloecke)} Plan-Türblöcken haben eine Modell-Tür auf "
        f"der Position (± 2 mm; Ist 13/72)")


@pytest.mark.xfail(
    strict=True,
    reason="Soll ≥ 9 stair_exit — Ist Muthgasse E2 2026-09-10: 5 (vorher 12). "
    "Das Band bleibt bei 9 und wird NICHT abgesenkt: siehe Docstring — es gibt "
    "keinen gemessenen Ersatz-Zielwert, nur den Ist-Stand, und aus dem Ist "
    "abgeleitete Bänder sind hier verboten. Der fachlich belegte Zielwert steht "
    "in test_soll_stair_exit_aus_echter_blocktuer (≥ 1, Ist 0). Nachtrag "
    "2026-09-12: nach der SCHLEUSE-Typisierung von raum_65 sind es 7 statt 5 "
    "stair_exit — weiter unter 9, Band unverändert. Nachtrag 2026-09-12 nach "
    "der Bereinigung: 6 (die 7 war der Zwischenstand nach der SCHLEUSE-"
    "Typisierung, vor der Bereinigung; exit_durchgang_141 ist mit den 21 "
    "Kontaktzonen-Durchgängen weggefallen). Belege: VERLAUF.md-Zeile des Laufs "
    "2026-09-12 'Ausgaenge final_exit:5 stair_exit:6', bericht.md '## Ausgänge "
    "(11)' mit 6 stair_exit-Zeilen, docs/ENIS_UEBERGABE_0908.md § 21.4. 6 < 9, "
    "Band unverändert.",
)
def test_soll_stair_exits(rm):
    """Zahlenband ohne fachliche Deckung — bewusst unverändert stehen gelassen.

    Herkunft: gesetzt in ``ebf867a`` (2026-09-07) nach der Konvention „Bänder
    knapp unter Ist — dürfen nur wachsen“, Ist damals 12. Nachgemessen
    2026-09-10 (Provider-Parse auf ``0d7c5db``): von diesen 12 entsprach
    **keine einzige** einem echten Türblatt — 5 Beschriftungs-Fahnen
    (Blockdef = 1× LINE, kein ARC, Layer ``A-DOOR-IDEN``, ``breite_mm=0.0``)
    und 7 Kontaktzonen-Artefakte aus ``durchgaenge_ohne_tuerblatt``. Die 9 ist
    also ein eingefrorener Falschpositiv-Stand, kein Fachziel.

    Warum trotzdem 9 stehen bleibt: der einzige Wert, den eine Messung heute
    deckt, ist die 5 — und die ist der Ist-Stand selbst. „Ist ist 5, also
    setze ich 5“ ist keine Begründung, und auch die 5 ruht auf denselben
    Kontaktzonen-Artefakten (4 der 5 haben Stiegenhaus ↔ Stiegenhaus, eine
    davon ``von_raum == nach_raum``). Ein fachlich hergeleiteter Zielwert für
    diese Kennzahl existiert nicht, solange sie über ``provider.py:148-157``
    (1500-mm-Manhattan-Dedupe) Positions-Cluster zählt statt Türen. Der
    Befund bleibt darum sichtbar rot statt still grün gerechnet.
    """
    assert sum(1 for a in rm.ausgaenge if a.typ == "stair_exit") >= 9, (
        "stair_exit-Erkennung eingebrochen (Ist 5, vor dem Fahnen-Ausschluss 12)"
    )


_BLOCKTUER_LAYER = ("A-DOOR", "A-GLAZ")   # Fahnen liegen auf A-DOOR-IDEN


def _blocktuer_positionen(plan):
    """INSERT-Positionen echter Türblöcke (Layer A-DOOR/A-GLAZ), auf 1 mm
    gerundet. Deren Blockdefinitionen tragen 8–110 LINEs und den Türblatt-ARC
    (r = 900/950/1020 mm); die 83 Fahnen-Blöcke auf ``A-DOOR-IDEN`` tragen
    genau 1 LINE und keinen ARC.

    **Korrektur 2026-09-12 zu „8–110 LINEs“ (die alte Angabe oben bleibt
    stehen):** gemessen sind es **2–110** LINEs über genau diese 209 INSERTs.
    Neun Blockdefinitionen liegen unter 8 (2× ``HNP_T_DG``, ``HNP_T_1T_1-SF``
    und 2× ``Fenster 1-flg`` mit je 2 LINEs). Die Untergrenze 8 war damit
    falsch; die Obergrenze 110 ist bestätigt.

    **Nachtrag 2026-09-12 zu „r = 900/950/1020 mm" (die alte Angabe oben
    bleibt stehen):** die Liste beschreibt diese Menge — sie umfasst A-DOOR
    UND A-GLAZ — nicht und verfehlt beide HÄUFIGSTEN Radien. Gemessen
    (In-Band-Radien je INSERT, ``600 < r < 1300 mm``) — ``A-DOOR``: 800 mm
    52× · 900 mm 14× · 950 mm 5× · 655 mm 3× · 700 mm 1×; ``A-GLAZ``:
    740 mm 33× · 1020 mm 21× · 940 mm 10× · 970/971/972/973 mm 16× ·
    890 mm 1×. Auf ``A-GLAZ`` existiert **weder 900 noch 950 mm** — die alte
    Liste mischt also zwei Layer. Die reine Türmenge des Plans zählt
    ``_plan_tuerbloecke`` (nur ``A-DOOR``, 72 Positionen).
    """
    aus = set()
    for e in plan.entities():
        if e.dxftype() != "INSERT" or str(e.dxf.layer) not in _BLOCKTUER_LAYER:
            continue
        xy = plan._scale(e.dxf.insert)
        aus.add((round(xy[0]), round(xy[1])))
    return aus


def _tueren_auf_blocktuer(plan, rm):
    """Türen im Modell, die auf einem echten Türblock sitzen (± 2 mm)."""
    pos = _blocktuer_positionen(plan)
    return [t for t in rm.tueren
            if any((round(t.xy_mm[0]) + dx, round(t.xy_mm[1]) + dy) in pos
                   for dx in range(-2, 3) for dy in range(-2, 3))]


def test_soll_echte_blocktueren_im_modell(plan, rm):
    """Klammer für das Zielbild darunter — sonst könnte es xfailen, weil es gar
    keine echten Türblöcke mehr gibt.

    Ist 2026-09-10 (Provider-Parse E2, Dump ``_p2_nachher.json``): 18 Türen
    sitzen auf einem ``A-DOOR``/``A-GLAZ``-INSERT; 16 davon tragen eine
    Türblatt-Breite (8× 900, 5× 950, 3× 1000 mm), 2 haben ``breite_mm=None``
    mit ``breite_quelle='UNBEKANNT'`` (``tuer_8`` Schiebetür-Block, ``tuer_17``
    4-tlg. Fenstertür) — das ist regelkonform und wird hier NICHT als Fehler
    gewertet.
    """
    echte = _tueren_auf_blocktuer(plan, rm)
    assert len(echte) >= 15, f"nur {len(echte)} Türen auf echten Türblöcken (Ist 18)"
    mit_breite = [t for t in echte if t.breite_mm]
    assert len(mit_breite) >= 14, (
        f"nur {len(mit_breite)} von {len(echte)} Blocktüren mit Breite (Ist 16/18)")


@pytest.mark.xfail(
    strict=True,
    reason="Soll ≥ 1 stair_exit an einer echten Blocktür — Ist Muthgasse E2 "
    "2026-09-10: 0 von 5. Gemessen: von den 18 Türen mit echtem A-DOOR/A-GLAZ-"
    "Block hat keine eine STIEGENHAUS-Seite; alle 5 stair_exit ruhen auf "
    "Kontaktzonen-Artefakten aus durchgaenge_ohne_tuerblatt. Der frühere "
    "Anker tuer_50 ist widerlegt (keine Blocktür, 780,5 mm zum nächsten "
    "A-DOOR-INSERT) — Belege in docs/ENIS_UEBERGABE_0908.md § 13.7. Nachtrag "
    "2026-09-12: mit der SCHLEUSE-Typisierung sind es 7 stair_exit (vorher 5), "
    "davon 0 auf einer echten Blocktür — der Befund ist unverändert. Nachtrag "
    "2026-09-12 nach der Bereinigung: 6 (die 7 war der Zwischenstand nach der "
    "SCHLEUSE-Typisierung, vor der Bereinigung; exit_durchgang_141 ist mit den "
    "21 Kontaktzonen-Durchgängen weggefallen; Belege: VERLAUF.md-Zeile des "
    "Laufs 2026-09-12 'Ausgaenge final_exit:5 stair_exit:6', bericht.md "
    "'## Ausgänge (11)', docs/ENIS_UEBERGABE_0908.md § 21.4) — davon weiter 0 "
    "auf einer echten Blocktür, Band unverändert.",
)
def test_soll_stair_exit_aus_echter_blocktuer(plan, rm):
    """Fachliches Zielbild als Ersatz für das reine Zählband oben.

    Gemessen 2026-09-10 auf beiden Ständen (``0d7c5db`` und ``1d9c03a``): von
    den 18 Türen, die an ihrer Position einen echten ``A-DOOR``/``A-GLAZ``-Block
    mit Türblatt-ARC (r = 900/950/1020 mm) tragen, hat **0** eine STIEGENHAUS-
    Seite — also stammt **0** ``stair_exit`` aus einer echten Blocktür, weder
    vorher (12 Stück) noch heute (5 Stück). Das ist der eigentliche Defekt
    hinter der Kennzahl, und er ist älter als der Fahnen-Ausschluss.

    **Nachtrag 2026-09-12 zur Radien-Angabe „r = 900/950/1020 mm":** die Liste
    ist unvollständig und für Türen teils falsch. Gemessen über alle 72
    Türblöcke auf ``A-DOOR`` sind die Türblatt-Radien 800 mm (52×), 900 mm
    (14×), 950 mm (5×), 655 mm (3×) und 700 mm (1×) — die 800 mm, der häufigste
    Türradius des Plans, fehlte ganz. **1020 mm ist kein Türradius, sondern ein
    Fensterradius auf ``A-GLAZ``** (3× „FE TÜR 2 tlg - waagrecht geteilt -
    1000 x 2550"); er steht hier nur, weil dieser Helfer ``A-GLAZ`` mitnimmt.
    **Korrektur 2026-09-12 zu den Trägern dieses Radius** (die Angabe „3× FE
    TÜR 2 tlg" war zu eng und bleibt oben stehen): gemessen tragen **21**
    ``A-GLAZ``-INSERTs einen Radius um 1020 mm — 18× „FE 1 tlg -
    konfigurierbar - 1000 x 1520" und 3× „FE TÜR 2 tlg - waagrecht geteilt -
    1000 x 2550". Die tragende Aussage bleibt unberührt: auf ``A-DOOR``
    existiert **kein einziger** 1020er Radius (gemessen 0 von 88 INSERTs).
    Die reine Türmenge des Plans zählt darum ``_plan_tuerbloecke`` (nur
    ``A-DOOR``, 72 Positionen).

    **Korrektur 2026-09-10 (Schritt 3, docs/ENIS_UEBERGABE_0908.md § 13.7):**
    der frühere Ansatzpunkt ``tuer_50`` trägt diesen Zielwert NICHT. ``tuer_50``
    bei 334453 / 106403 stammt aus ``quelle='arc_aussen+text:E2-VF-12a'``, also
    aus einem ARC, und sitzt auf **keinem** Türblock — der nächste der 209
    ``A-DOOR``/``A-GLAZ``-INSERTs liegt 780,5 mm entfernt. Sie fällt damit gar
    nicht in die Menge ``_tueren_auf_blocktuer``. Der Ursprungsbefund hatte den
    Abstand einer echten Blocktür zu einem STIEGENHAUS-*Polygon* gemessen
    (``tuer_22``, 0 mm zu ``raum_88`` — dem Artefaktraum aus § 11.4), nicht zu
    ``stiegenhaus_1``.

    Ein ``raum_typ`` auf ``raum_65`` würde diesen Test folglich nicht drehen:
    von den 18 echten Blocktüren hat keine eine STIEGENHAUS-Seite, und die drei
    mit untypisierter Gegenseite (``tuer_11/12/13`` → ``raum_70/59/48``, alle
    Stempelname ``Vorr.``) haben gegenüber GANG, lieferten also ``VORRAUM`` →
    ``WOHNUNG_PRIVAT`` → ``wohnungseingang`` und ebenfalls keinen
    ``stair_exit``. Der Zielwert 1 ruht damit derzeit auf keinem benannten
    Anker; das Band bleibt trotzdem unverändert, weil ein aus dem Ist
    abgeleitetes Band hier verboten ist (§ 11.5). Der belegte Defekt dahinter
    ist unverändert: alle 5 ``stair_exit`` stammen aus Kontaktzonen-Artefakten.
    """
    echte = {(round(t.xy_mm[0]), round(t.xy_mm[1]))
             for t in _tueren_auf_blocktuer(plan, rm)}
    treffer = [a.id for a in rm.ausgaenge if a.typ == "stair_exit"
               and any((round(a.xy_mm[0]) + dx, round(a.xy_mm[1]) + dy) in echte
                       for dx in range(-2, 3) for dy in range(-2, 3))]
    assert treffer, (
        "kein stair_exit sitzt auf einer echten Blocktür "
        f"({sum(1 for a in rm.ausgaenge if a.typ == 'stair_exit')} stair_exit gesamt)")


def test_soll_raeume_flaechendeckend_typisiert(rm):
    """Erreicht 2026-09-08: die Kaskade schreibt den Stempel-Typ auf L-/H-Räume
    zurück (``kaskade.raeume_aus_kaskade``) — vorher blieb der Typ im Stempel
    stecken und nur 34 der Räume waren typisiert (xfail-Zielbild)."""
    typisiert = sum(1 for r in rm.raeume if r.raum_typ)
    assert typisiert >= 90, f"nur {typisiert} Räume typisiert"


@pytest.mark.xfail(
    strict=True,
    reason="Soll ≥ 90 % typisierte Türen je Familie — Ist Muthgasse E2 "
    "2026-09-10: 70,5 % (205/291; vor dem Fahnen-Ausschluss 218/308 = 70,8 %, "
    "vor der Typ-Rückschreibung 8 %). Rest sind "
    "Türen ohne typisierte Gegenseite; Gründe-Tabelle in bericht.md",
)
def test_soll_90_prozent_tueren_typisiert(rm):
    typ = sum(1 for t in rm.tueren if t.tuer_detail)
    assert rm.tueren and typ / len(rm.tueren) >= 0.9, (
        f"nur {typ}/{len(rm.tueren)} Türen typisiert")


def test_soll_schl_nur_mit_entscheidung_typisiert(rm):
    """`Schl.` typisiert NUR dort, wo eine Owner-Entscheidung vorliegt.

    Entscheidung Enis 2026-09-11 (docs/OFFENE_FRAGEN.md): Stempelnummer
    `E2-VF-11a` = SCHLEUSE. Die Lagen sind die gemessenen MTEXT-Positionen der
    beiden `Schl.`-Stempel auf `A-AREA-IDEN` (Inventar 2026-09-11):
    335 239 / 108 646 (`E2-VF-11a`, 13,04 m²) und 333 017 / 97 219
    (`E2-VF-11b`, 3,73 m² — Entscheidung ausstehend, bleibt untypisiert).

    Der zweite Punkt liegt in ZWEI Räumen (zu 99,3 % im F-Artefakt `raum_88`,
    STIEGENHAUS) — deshalb wird nicht auf „untypisiert" geprüft, sondern
    darauf, dass dort KEIN Raum SCHLEUSE trägt.
    """
    from shapely.geometry import Point, Polygon

    def deckende(xy):
        p = Point(xy)
        return [r for r in rm.raeume if len(r.polygon_mm) >= 3
                and Polygon(r.polygon_mm).buffer(0).covers(p)]

    entschieden = deckende((335239.0, 108646.0))
    assert entschieden, "kein Raum an der Lage von E2-VF-11a"
    assert any(r.raum_typ == "SCHLEUSE" for r in entschieden), (
        "E2-VF-11a nicht als SCHLEUSE typisiert: "
        + repr([(r.id, r.raum_typ) for r in entschieden]))
    offen = deckende((333017.0, 97219.0))
    assert not any(r.raum_typ == "SCHLEUSE" for r in offen), (
        "E2-VF-11b typisiert, obwohl die Entscheidung aussteht: "
        + repr([(r.id, r.raum_typ) for r in offen]))


def test_soll_keine_beschriftungsfahnen_als_tueren(plan, rm):
    """Muthgasse trägt 83 INSERTs ``HNP_Beschriftung Türen … Durchgangslichte…``
    (Blockdef = 1× LINE, keine Türgeometrie). Sie standen bis 2026-09-10 als
    Türen im Modell — ``_DOOR_EXCLUDE`` verwirft sie jetzt. Klammer: keine Tür
    sitzt mehr auf einem Fahnen-INSERT-Punkt."""
    fahnen = [plan._scale(e.dxf.insert) for e in plan.entities()
              if e.dxftype() == "INSERT" and "beschrift" in str(e.dxf.name).lower()]
    assert len(fahnen) >= 83, f"nur {len(fahnen)} Fahnen-INSERTs im Plan"
    treffer = [(t.id, t.xy_mm) for t in rm.tueren
               if any(abs(t.xy_mm[0] - f[0]) < 1.0 and abs(t.xy_mm[1] - f[1]) < 1.0
                      for f in fahnen)]
    assert not treffer, f"Beschriftungs-Fahnen wieder als Türen: {treffer}"
