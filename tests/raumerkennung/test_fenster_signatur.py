"""Fenster-Signatur (Rahmenpaar + Scheibenlinien in der Wandunterbrechung) auf
synthetischen Wandsegmenten. Maße wie auf Barawitzka_EG gemessen: Rahmentiefe
90 mm, Scheibenabstand 20 mm (docs/ENIS_UEBERGABE_0908.md § 4.5)."""
from __future__ import annotations

from shapely.geometry import Polygon
from shapely.ops import unary_union

from notbeleuchtung.raumerkennung.fenster_signatur import (
    Segment,
    finde_rahmenfenster,
)

LAYER = "0._EG PP_2_110 Wand Aussen"


def _waagrecht(y: float, x0: float, x1: float) -> Segment:
    return ((x0, y), (x1, y), LAYER)


def _fenster(x0: float, x1: float, tiefe: float = 90.0,
             scheiben: int = 2) -> list[Segment]:
    """Rahmenpaar über die volle Länge, dazwischen ``scheiben`` Innenlinien."""
    segs = [_waagrecht(0.0, x0, x1), _waagrecht(tiefe, x0, x1)]
    mitte = tiefe / 2
    segs += [_waagrecht(mitte - 10 + 20 * i, x0, x1) for i in range(scheiben)]
    return segs


def _wandstuecke(*spannen: tuple[float, float]) -> Polygon:
    """Geschlossene Wandkörper (Schraffur) links/rechts der Öffnung."""
    return unary_union([Polygon([(a, 0), (b, 0), (b, 90), (a, 90)])
                        for a, b in spannen])


def test_rahmen_mit_scheiben_in_der_oeffnung_ist_ein_fenster() -> None:
    wand = _wandstuecke((-2000, 600), (1928, 4000))
    treffer = finde_rahmenfenster(_fenster(600, 1927), wand)
    assert len(treffer) == 1
    f = treffer[0]
    assert f.breite_mm == 1327.0
    assert f.rahmentiefe_mm == 90.0
    assert f.scheibenlinien == 2
    assert f.layer == LAYER
    assert f.hat_tuerbogen is None          # ohne Plan nicht ausgewertet
    assert f.mitte_mm == (1263.5, 45.0)


def test_rahmen_ohne_scheibenlinien_ist_kein_fenster() -> None:
    """Nacktes Doppellinienpaar = Wandaufbau, kein Fenster."""
    wand = _wandstuecke((-2000, 600), (1928, 4000))
    assert finde_rahmenfenster(_fenster(600, 1927, scheiben=0), wand) == []


def test_eine_scheibenlinie_reicht_nicht() -> None:
    wand = _wandstuecke((-2000, 600), (1928, 4000))
    assert finde_rahmenfenster(_fenster(600, 1927, scheiben=1), wand) == []


def test_falsche_rahmentiefe_ist_kein_fenster() -> None:
    """250 mm Abstand = Wandquerschnitt, nicht Rahmentiefe 80-100 mm."""
    wand = _wandstuecke((-2000, 600), (1928, 4000))
    assert finde_rahmenfenster(_fenster(600, 1927, tiefe=250.0), wand) == []


def test_in_geschlossener_wand_ist_kein_fenster() -> None:
    """Öffnungsbedingung: Mittelpunkt in der Wandschraffur → verworfen."""
    wand = _wandstuecke((-2000, 4000))
    assert finde_rahmenfenster(_fenster(600, 1927), wand) == []


def test_zu_kurz_ist_kein_fenster() -> None:
    wand = _wandstuecke((-2000, 600), (850, 4000))
    assert finde_rahmenfenster(_fenster(600, 849), wand) == []


def test_ohne_wandflaeche_bleibt_es_ein_rohbefund() -> None:
    """wandflaeche=None: Öffnungsbedingung NICHT geprüft — kein Ersatzwert,
    der Treffer ist ausdrücklich ungeprüft."""
    assert len(finde_rahmenfenster(_fenster(600, 1927), None)) == 1
