"""Balkon- und Loggiatüren im Obergeschoss sind kein Fluchtweg.

Owner-Auftrag 2026-09-12 zu Leonis' Einwand 5, gemessen auf ``91ad7cc``: eine
Tür mit ``AUSSEN`` auf einer Seite wurde zum ``final_exit``, ohne zu fragen, ob
dahinter Gelände oder eine Balkonplatte liegt.

**Diese Datei trägt auch einen Fehler von mir und seine Korrektur.** Die erste
Fassung der Regel griff in JEDEM Geschoss. Damit hat sie einen belegten
Fluchtweg zerstört: Mollgasse ``tuer_68`` ist die Südgarten-Tür (Cluster B,
800 mm) an einem Hof, der laut Außen-Analyse Wege ins Freie hat — über die
nördliche Grundstücksgrenze und die Garagentor-Ostkante. ``test_soll_mollgasse``
hält das scharf fest und wurde rot. Der Owner-Auftrag sagt genau das, was ich
übergangen hatte: *im EG mit Ausgang ins Gelände bleiben sie möglich.*

Die Regel gilt deshalb **nur außerhalb des Erdgeschosses**, und die Bedingung
lautet ``not ist_erdgeschoss(geschoss)``, nicht ``ist_obergeschoss(geschoss)``:
``geschoss_aus(None, "Muthgasse_E2.dxf")`` liefert einen leeren String, und dort
sind **beide** Prädikate False. Mit ``ist_obergeschoss`` wäre die Regel genau auf
den 41 von 62 Korpusplänen wirkungslos, deren Geschoss nicht erkannt wird — also
gerade dort, wo Balkone im Obergeschoss liegen.

**Wirkung im Bestand: 0 Fälle.** Mollgasse und Barawitzka sind EG, Rennweg_OG3
hat 0 ``final_exit``, Muthgasse trägt keine Freiflächentür mit ``AUSSEN``-Seite.
Die Regel ist damit **Vorsorge**, und ihre Wirksamkeit hängt an der kaputten
Geschoss-Erkennung — das ist keine Beschönigung, sondern der gemessene Stand.

Nicht messbar und daher nicht Teil der Regel: Geländeniveau (``dxf_load``
verwirft die z-Koordinate, es gibt kein Höhen-Datum) und ein umlaufendes
Geländer (einzige Fundstelle im Quellbaum ist ein Dialekt-TEXT-Hinweis).
``loggia`` fällt per ``raumtyp.py`` auf ``BALKON``, ist also mit abgedeckt.
"""
import pytest

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer
from notbeleuchtung.raumerkennung.ausgaenge import leite_ausgaenge
from notbeleuchtung.raumerkennung.tuer_typisierung import (
    ist_erdgeschoss,
    ist_obergeschoss,
    typisiere_tueren,
)


def _raum(rid: str, typ: str, x: float = 0.0) -> Raum:
    return Raum(id=rid, raum_typ=typ,
                polygon_mm=[(x, 0.0), (x + 4000.0, 0.0),
                            (x + 4000.0, 3000.0), (x, 3000.0)])


def _lauf(raeume, tueren, geschoss, fluchtweg_enden=()):
    typisiere_tueren(tueren, raeume, geschoss, fluchtweg_enden=fluchtweg_enden)
    ausgaenge, _ = leite_ausgaenge(tueren, raeume, geschoss,
                                   fluchtweg_enden=fluchtweg_enden)
    return ausgaenge


def _aussentuer(nach: str, breite: float) -> Tuer:
    return Tuer(id="t1", xy_mm=(4000.0, 1500.0), von_raum="AUSSEN",
                nach_raum=nach, breite_mm=breite)


# ── Die Regel greift außerhalb des Erdgeschosses ────────────────────────────

def test_balkontuer_im_obergeschoss_ist_kein_ausgang():
    """Gemessene Lücke: die Gegenseite ist kein Raum, also griff keine der
    Klassenregeln — aber das Notausgang-Flag aus der Doppelflügel-Breite
    überlebte und ``leite_ausgaenge`` feuerte darauf."""
    t = _aussentuer("r1", 1500.0)
    assert _lauf([_raum("r1", "BALKON")], [t], "OG3") == []
    assert t.tuer_detail == "balkontuer"
    assert t.ist_notausgang is False


def test_terrassentuer_im_obergeschoss_ist_kein_hauseingang():
    """Zweite Lücke: ``nutzungsklasse`` bildet TERRASSE auf ``AUSSEN`` ab,
    damit wurde AUSSEN × ALLGEMEIN_ERSCHLIESSUNG zum ``hauseingang``."""
    t = _aussentuer("r1", 900.0)
    assert _lauf([_raum("r1", "TERRASSE")], [t], "OG1") == []
    assert t.tuer_detail == "balkontuer"


def test_regel_greift_auch_ohne_erkanntes_geschoss():
    """Der Fall Muthgasse_E2: ``geschoss_aus`` liefert einen leeren String.

    Dort sind ``ist_erdgeschoss`` UND ``ist_obergeschoss`` False. Die Regel muss
    trotzdem greifen, sonst ist sie auf 41 von 62 Korpusplänen wirkungslos.
    """
    assert not ist_erdgeschoss("")
    assert not ist_obergeschoss("")
    t = _aussentuer("r1", 1500.0)
    assert _lauf([_raum("r1", "BALKON")], [t], "") == []


# ── Im Erdgeschoss greift sie NICHT ─────────────────────────────────────────

def test_suedgarten_im_erdgeschoss_bleibt_final_exit():
    """Regressionstest für meinen eigenen Fehler.

    Nachbau von Mollgasse ``tuer_68``: TERRASSE, 800 mm, Erdgeschoss, das
    Notausgang-Flag kommt aus einem Fluchtweg-Ende in der Nähe. Diese Tür ist
    der Südgarten-Ausgang (Cluster B) und MUSS ein Endausgang bleiben — die
    erste Fassung der Regel hatte sie entfernt und ``test_soll_mollgasse``
    gebrochen.
    """
    t = Tuer(id="tuer_68", xy_mm=(4000.0, 1500.0), von_raum="AUSSEN",
             nach_raum="raum_61", breite_mm=800.0)
    ausgaenge = _lauf([_raum("raum_61", "TERRASSE")], [t], "EG",
                      fluchtweg_enden=[(4200.0, 1500.0)])
    assert [a.typ for a in ausgaenge] == ["final_exit"]
    # Der Ausgang entsteht über den Notausgang-Pfad (``ausgaenge.py:59``,
    # ``ist_notausgang and ins_freie``), NICHT über ``hauseingang``: bei
    # Sentinel-AUSSEN gegen TERRASSE tragen beide Seiten die Nutzungsklasse
    # AUSSEN, und der hauseingang-Zweig verlangt ALLGEMEIN_ERSCHLIESSUNG.
    # ``tuer_detail`` bleibt deshalb None mit ``untypisiert_grund``
    # ``unbekannte_kombination`` — genau so steht es auch im Prüfbericht.
    assert t.tuer_detail is None
    assert t.ist_notausgang is True


# ── Gegenproben in die gefährliche Richtung ─────────────────────────────────

def test_echte_haustuer_bleibt_final_exit():
    """Ohne Freiflächen-Raum auf einer Seite bleibt die Tür ins Freie ein
    Endausgang — auch im Obergeschoss-Zweig der Typisierung."""
    t = _aussentuer("r1", 1500.0)
    ausgaenge = _lauf([_raum("r1", "GANG")], [t], "EG")
    assert [a.typ for a in ausgaenge] == ["final_exit"]
    assert t.tuer_detail == "hauseingang"


def test_stiegenhaustuer_bleibt_stair_exit():
    """Der andere Ausgangszweig ist unberührt."""
    raeume = [_raum("r1", "STIEGENHAUS"), _raum("r2", "GANG", 5000.0)]
    t = Tuer(id="t1", xy_mm=(4500.0, 1500.0), von_raum="r1", nach_raum="r2",
             breite_mm=900.0)
    assert [a.typ for a in _lauf(raeume, [t], "EG")] == ["stair_exit"]


@pytest.mark.xfail(strict=True, reason=(
    "ZIELBILD, kein Fehler. Gemessen auf 91ad7cc: 14 der 19 final_exit über die "
    "fünf Prüfpläne sitzen am AUSSEN-Sentinel, ihre Gegenseite ist also kein "
    "Raum — ob dahinter Gelände oder eine Balkonplatte liegt, ist mit heutigen "
    "Daten UNENTSCHEIDBAR (kein Höhen-Datum, dxf_load verwirft z). Dazu haben 4 "
    "der 19 gar keinen Türbezug (footprint.hauptausgaenge, provider.py:102, "
    "erzeugt final_exit ohne Raum-, Typ- und Geschossbezug). Solange das so "
    "ist, kann die Regel nur typisierte Freiflächen erfassen."))
def test_soll_sentinel_aussen_ist_entscheidbar():
    """Sobald Gelände oder Geschoss verlässlich vorliegen, muss auch eine Tür
    mit Sentinel-Gegenseite entscheidbar sein."""
    t = _aussentuer("r1", 1500.0)
    typisiere_tueren([t], [_raum("r1", "GANG")], "")
    assert t.tuer_detail in ("hauseingang", "balkontuer"), (
        "Sentinel-AUSSEN bleibt ohne Höhen- oder Geschoss-Datum unentscheidbar"
    )
