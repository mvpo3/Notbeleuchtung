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
"""
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
    assert len(rm.raeume) >= 98, f"nur {len(rm.raeume)} Räume (Ist 114)"
    assert len(rm.tueren) >= 280, f"nur {len(rm.tueren)} Türen (Ist 291)"
    assert len(rm.zirkulation.segmente) >= 100, (
        f"nur {len(rm.zirkulation.segmente)} Segmente (Ist 143)"
    )
    assert len(rm.stiegenhaeuser) >= 5, (
        f"nur {len(rm.stiegenhaeuser)} Stiegenhäuser (Ist 9)"
    )


# ── Zielbilder ──────────────────────────────────────────────────────────────

@pytest.mark.xfail(
    strict=True,
    reason="Soll ≥ 9 stair_exit — Ist Muthgasse E2 2026-09-10: 5 (vorher 12). "
    "Das Band bleibt bei 9 und wird NICHT abgesenkt: siehe Docstring — es gibt "
    "keinen gemessenen Ersatz-Zielwert, nur den Ist-Stand, und aus dem Ist "
    "abgeleitete Bänder sind hier verboten. Der fachlich belegte Zielwert steht "
    "in test_soll_stair_exit_aus_echter_blocktuer (≥ 1, Ist 0).",
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
    genau 1 LINE und keinen ARC."""
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
    "Kontaktzonen-Artefakten aus durchgaenge_ohne_tuerblatt.",
)
def test_soll_stair_exit_aus_echter_blocktuer(plan, rm):
    """Fachliches Zielbild als Ersatz für das reine Zählband oben.

    Gemessen 2026-09-10 auf beiden Ständen (``0d7c5db`` und ``1d9c03a``): von
    den 18 Türen, die an ihrer Position einen echten ``A-DOOR``/``A-GLAZ``-Block
    mit Türblatt-ARC (r = 900/950/1020 mm) tragen, hat **0** eine STIEGENHAUS-
    Seite — also stammt **0** ``stair_exit`` aus einer echten Blocktür, weder
    vorher (12 Stück) noch heute (5 Stück). Das ist der eigentliche Defekt
    hinter der Kennzahl, und er ist älter als der Fahnen-Ausschluss.

    Konkreter Ansatzpunkt, gemessen: ``tuer_50`` bei 334453 / 106403
    (``quelle='arc_aussen+text:E2-VF-12a'``) liegt mit ``von_raum=stiegenhaus_1``
    (STIEGENHAUS) an einem echten Stiegenhaus und bleibt untypisiert, weil die
    Gegenseite ``raum_65`` keinen ``raum_typ`` trägt — die Regel
    ``tuer_typisierung.py:154-156`` scheitert an der Raumtypisierung der
    Gegenseite, nicht an der Türregel. Zielwert 1 ist damit nicht aus dem Ist
    abgeleitet, sondern aus einer benennbaren echten Stiegenhaustür im Plan.
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
