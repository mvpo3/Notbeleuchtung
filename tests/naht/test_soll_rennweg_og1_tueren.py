"""Soll-Tests Rennweg OG1 — ArchiCAD-Weltkoordinaten-Türblöcke als Türen
(Diagnose U12, Slice S4a „Lage").

Plan-Befund (selbst gemessen, OG1, ``plan.factor`` 1.0): 12 INSERTs mit
Tür/Door/Opening-Token liegen EINE Ebene tief in ``Wall_*``-Blöcken. Ihr
INSERT-Punkt ist für alle derselbe gemeinsame Anker weit außerhalb des
Planbereichs; die Geometrie (``virtual_entities``) liegt in Weltkoordinaten
mitten im Grundriss. Aufteilung der 12:

  * 7 × ``Zargentür_1_Fl 10[n]`` (n = 1,2,3,4,8,9,10) — je 1 Schwenkbogen
    (r = 940 bei [1], sonst 840; Sweep 90°) + 30 LINE + 1 Marker-INSERT,
  * 2 × ``Schiebetür_Typ1_1_Fl[5]/[7]`` — 89 LINE + 9 WIPEOUT, KEIN Bogen,
  * 3 × ``Rectangular Door Opening 27[6]/[11]/[12]`` — 2 LINE, kein Bogen.

Die 3 ``Rectangular Door Opening`` sind Öffnungen ohne Türblatt und liegen
AUSSERHALB des Tür-Vokabulars (``_ist_tuer_block`` = False, DOOR/OPENING sind
keine Tokens) — sie sind NICHT Teil von S4a und werden hier nur gezählt.

Soll dieses Slices: mindestens die 9 Türblöcke (7 Zargen- + 2 Schiebetüren)
erscheinen als Türen mit ``quelle == "block"``, jede mit Lage in der Wand,
Sehnenwinkel, Wandsegment (``wand_block``) und Breite ohne Standardwert.

Zwei Messgrenzen dieser Datei, damit die Zahlen nicht überinterpretiert werden:

  * Die Sehnenmitte (``xy_mm``) liegt PER KONSTRUKTION in der Wandlücke — der
    Wandkörper hat an der Öffnung eine Lücke von genau der Türbreite. Ihr
    Abstand zur Wand ist deshalb kein Beleg; das Maß sind die SEHNEN-ENDEN
    (Scharnier und Wandseite, je ≤ 250 mm vom nächsten Wandkörper).
  * Welches ARC-Ende die Wandseite ist, entscheidet die MEHRHEIT der
    blattlangen Linien am Scharnier (``tueren._blockgeometrie``), nicht die
    Port-Regel „start_angle-Endpunkt": die wählte auf Rennweg OG1 in 7/7
    Fällen das falsche Ende (die offene Blattspitze statt der Wand).
"""
from __future__ import annotations

import math
from pathlib import Path

import pytest

PLAN = Path("Projekte/Rennweg/OG1 - Rennweg 15_1030 Wien_Ausfürung-2026-06-12.dxf")

_WAND_NAH_MM = 250.0        # Sehnen-Ende „liegt an der Wand"
_TREFFER_MM = 1.0           # Tür ↔ Öffnung derselben Lage


@pytest.fixture(scope="module")
def og1():
    """(RaumModell, DxfPlan, KaskadeErgebnis) eines echten Provider-Laufs.

    Wrapper-Muster wie ``scripts/analyse/raumerkennung_darstellung._erkennen``:
    ``lade_dxf``/``raeume_aus_kaskade`` kurz umhängen, damit Plan und Kaskade
    des EINEN Laufs greifbar sind (kein zweiter Parse).
    """
    if not PLAN.exists():                    # pragma: no cover — CAD-Asset fehlt
        pytest.skip(f"Architekturplan nicht vorhanden: {PLAN}")
    import notbeleuchtung.raumerkennung.provider as pm

    gefangen: dict = {}
    orig_lade, orig_kask = pm.lade_dxf, pm.raeume_aus_kaskade

    def lade(pfad):
        gefangen["plan"] = orig_lade(pfad)
        return gefangen["plan"]

    def kask(plan, *a, **kw):
        gefangen["k"] = orig_kask(plan, *a, **kw)
        return gefangen["k"]

    pm.lade_dxf, pm.raeume_aus_kaskade = lade, kask
    try:
        modell = pm.ArchitekturRaumProvider().parse(str(PLAN), "")
    finally:
        pm.lade_dxf, pm.raeume_aus_kaskade = orig_lade, orig_kask
    return modell, gefangen["plan"], gefangen["k"]


def _block_tueren(modell):
    return [t for t in modell.tueren if t.quelle == "block"]


def _oeffnung_zu(tuer, kaskade):
    """Die Block-Öffnung der Kaskade an derselben Lage (oder None)."""
    for o in kaskade.tueroeffnungen:
        if o.quelle == "block" and math.dist(o.xy_mm, tuer.xy_mm) <= _TREFFER_MM:
            return o
    return None


def _raum(modell, typ: str, flaeche: float):
    """Raum über Typ + Fläche identifizieren — nie über eine ID."""
    treffer = [r for r in modell.raeume
               if r.raum_typ == typ and abs(r.flaeche_m2 - flaeche) < 0.05]
    assert len(treffer) == 1, f"{typ} {flaeche} m²: {len(treffer)} Treffer"
    return treffer[0]


def test_tuerbloecke_werden_tueren(og1):
    """Die 9 Türblöcke (7 Zargen- + 2 Schiebetüren) sind Türen mit quelle 'block'."""
    modell, _plan, _k = og1
    bloecke = _block_tueren(modell)
    assert len(bloecke) >= 9, (
        f"nur {len(bloecke)} Türen mit quelle 'block': "
        f"{[(t.id, t.xy_mm) for t in bloecke]}"
    )


def test_tuerbloecke_liegen_in_der_wand(og1):
    """Jede Block-Tür liegt an einem Wandkörper und trägt Wandsegment + Sehne.

    Gemessen wird an den SEHNEN-ENDEN (Scharnier und Wandseite), nicht an der
    Sehnenmitte: der Wandkörper hat an der Öffnung per Konstruktion eine Lücke
    von genau der Türbreite (Wandflanken enden beidseits der Öffnung), die
    Sehnenmitte liegt also planmäßig eine halbe Türbreite von jedem Wandstück
    entfernt. Ohne messbare Breite (Schiebetür) wird ``xy_mm`` selbst geprüft.
    """
    from shapely.geometry import Point, Polygon

    modell, _plan, k = og1
    polys = [Polygon(w.polygon_mm).buffer(0) for w in k.wandkoerper
             if len(w.polygon_mm) >= 3]
    assert polys, "keine Wandkörper — Messung wertlos"
    bloecke = _block_tueren(modell)
    assert bloecke, "keine Block-Türen — Messung wertlos"

    def abstand(p):
        return min(q.distance(Point(p)) for q in polys)

    for t in bloecke:
        o = _oeffnung_zu(t, k)
        assert o is not None, f"{t.id}: keine Block-Öffnung an {t.xy_mm}"
        assert o.wand_block and o.wand_block.startswith("Wall_"), (
            f"{t.id}: wand_block = {o.wand_block!r}")
        assert o.winkel_grad is not None, f"{t.id}: keine Sehne (winkel_grad None)"
        if o.breite_mm is None:
            d = abstand(t.xy_mm)
            assert d <= _WAND_NAH_MM, f"{t.id} ({o.wand_block}): xy {d:.1f} mm von der Wand"
            continue
        w = math.radians(o.winkel_grad)
        halb = o.breite_mm / 2.0
        for sgn in (1.0, -1.0):
            ende = (t.xy_mm[0] + sgn * halb * math.cos(w),
                    t.xy_mm[1] + sgn * halb * math.sin(w))
            d = abstand(ende)
            assert d <= _WAND_NAH_MM, (
                f"{t.id} ({o.wand_block}): Sehnen-Ende {d:.1f} mm von der Wand "
                f"(Sehnenmitte {abstand(t.xy_mm):.1f} mm)")


def test_tuerbloecke_breite_ohne_standardwert(og1):
    """Keine Block-Tür bekommt einen Standardwert; ohne Bogen bleibt die Breite None."""
    from notbeleuchtung.raumerkennung import tueren

    modell, _plan, _k = og1
    bloecke = _block_tueren(modell)
    assert not [t for t in bloecke if t.breite_quelle == "STANDARDWERT"]

    mit_bogen = [t for t in bloecke if t.breite_quelle == "GEOMETRIE_SCHWENKRADIUS"]
    assert len(mit_bogen) >= 7, f"nur {len(mit_bogen)} Türen mit Schwenkradius-Breite"
    assert {t.breite_mm for t in mit_bogen} == {840.0, 940.0}, (
        f"Breiten: {sorted({t.breite_mm for t in mit_bogen})}")

    ohne_bogen = [t for t in bloecke if t not in mit_bogen]
    assert len(ohne_bogen) >= 2, f"nur {len(ohne_bogen)} Türen ohne Schwenkbogen"
    for t in ohne_bogen:
        assert t.breite_mm is None, f"{t.id}: Breite {t.breite_mm} ohne Schwenkbogen"
        assert t.breite_quelle == "UNBEKANNT", f"{t.id}: {t.breite_quelle}"
        assert t.breite_grund == tueren._GRUND_OHNE_BOGEN, (
            f"{t.id}: unspezifischer Grund {t.breite_grund!r}")


def test_m17_04_c_wc_tuer_an_o(og1):
    """M17-04-c: genau EINE Block-Tür aus ``Wall_20`` verbindet WC und Vorraum.

    ``Zargentür_1_Fl 10[9]`` ist der einzige Türblock in ``Wall_20``; die Räume
    werden über Typ + Fläche identifiziert, nie über IDs. Die Fläche allein ist
    hier eindeutig — ``wohnung_id`` taugt NICHT als Merkmal: mit der neuen
    WC-Tür gruppiert ``bilde_wohnungen`` den Vorraum (10,94 m²) in eine Wohnung,
    vorher stand er ohne ``wohnung_id``.
    """
    modell, _plan, k = og1
    wc = _raum(modell, "WC", 3.50)
    vorraum = _raum(modell, "VORRAUM", 10.94)

    treffer = [t for t in _block_tueren(modell)
               if (o := _oeffnung_zu(t, k)) is not None and o.wand_block == "Wall_20"]
    assert len(treffer) == 1, (
        f"{len(treffer)} Block-Türen aus Wall_20: {[t.id for t in treffer]}")
    t = treffer[0]
    assert {t.von_raum, t.nach_raum} == {wc.id, vorraum.id}, (
        f"{t.id}: von={t.von_raum} nach={t.nach_raum}, "
        f"erwartet WC={wc.id} + Vorraum={vorraum.id}")


@pytest.mark.xfail(strict=True, reason=(
    "S4b: feste 300-mm-Seitenprobe in tuer_zuordnung._PROBE_MM. Gemessen nach "
    "S4a: 8 von 9 Block-Türen tragen zwei Raum-IDs, die Wohnungseingangstür aus "
    "Wall_9 (940 mm, Sehne 66,64°) nicht — ihr Probepunkt auf der "
    "Stiegenhaus-Seite liegt 70 mm VOR dem STIEGENHAUS-Polygon (11,21 m²) und "
    "wird KEIN_RAUM; die Gegenseite trifft den VORRAUM (10,94 m²) mit 0 mm. "
    "Die Sehne liegt auf EINER Wandflanke, die Probe muss dort die ganze "
    "Wanddicke queren."))
def test_tuerbloecke_haben_beide_raumseiten(og1):
    """Jede Block-Tür trägt zwei Raum-IDs (nicht None, nicht AUSSEN/KEIN_RAUM).

    Eigenständig, damit das Ergebnis isoliert lesbar bleibt: der Test ist ein
    S4b-Befund (feste 300-mm-Seitenprobe in ``tuer_zuordnung``), kein
    Lage-Befund von S4a — deshalb xfail(strict) und NICHT hochgezogen.
    """
    from notbeleuchtung.raumerkennung.tuer_zuordnung import AUSSEN, KEIN_RAUM

    modell, _plan, _k = og1
    ids = {r.id for r in modell.raeume}
    schlecht = [(t.id, t.von_raum, t.nach_raum) for t in _block_tueren(modell)
                if t.von_raum not in ids or t.nach_raum not in ids
                or AUSSEN in (t.von_raum, t.nach_raum)
                or KEIN_RAUM in (t.von_raum, t.nach_raum)]
    assert not schlecht, f"Block-Türen ohne zwei Raumseiten: {schlecht}"
