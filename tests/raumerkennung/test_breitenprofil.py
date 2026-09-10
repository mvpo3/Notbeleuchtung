"""Breitenprofil auf synthetischen Geometrien: L-Gang, Breitensprung,
kurze Engstelle, Türdurchgang."""
from __future__ import annotations

from shapely.geometry import LineString, Polygon

from notbeleuchtung.raumerkennung.breitenprofil import (
    ECKE_FENSTER_MM,
    SNAP_MM,
    begrenzende_flaechen,
    miss_breitenprofil,
)


def _gerader_gang(breite: float, laenge: float) -> Polygon:
    return Polygon([(0, 0), (laenge, 0), (laenge, breite), (0, breite)])


def test_gerader_gang_konstante_breite() -> None:
    flaeche = _gerader_gang(1200, 6000)
    p = miss_breitenprofil("seg_1", [(0, 600), (6000, 600)], flaeche)
    assert p.messbar and p.grund is None
    assert p.laenge_mm == 6000.0
    assert len(p.profil) == 61                      # alle 100 mm inkl. Endpunkt
    assert {m.breite_mm for m in p.profil} == {1200.0}
    assert len(p.abschnitte) == 1
    assert p.abschnitte[0].breite_mm == 1200.0
    assert p.abschnitte[0].laenge_mm == 6000.0
    assert p.engstellen == []
    assert p.breite_min_mm == 1200.0


def test_l_gang_beide_schenkel_messbar() -> None:
    # L: horizontaler Schenkel y 0..1200, vertikaler x 4800..6000
    flaeche = Polygon([(0, 0), (6000, 0), (6000, 5000), (4800, 5000),
                       (4800, 1200), (0, 1200)])
    p = miss_breitenprofil("seg_L", [(0, 600), (5400, 600), (5400, 5000)], flaeche)
    assert p.messbar
    gerade = [m.breite_mm for m in p.profil
              if m.laufmeter_mm < 4000 or m.laufmeter_mm > 7000]
    assert set(gerade) == {1200.0}
    assert len(p.abschnitte) == 1                   # beide Schenkel 1,20 m
    assert p.abschnitte[0].breite_mm == 1200.0


def test_breitensprung_1200_auf_2600_gibt_zwei_abschnitte() -> None:
    flaeche = Polygon([(0, 0), (10000, 0), (10000, 2600), (5000, 2600),
                       (5000, 1200), (0, 1200)])
    p = miss_breitenprofil("seg_2", [(0, 600), (10000, 600)], flaeche)
    breiten = [a.breite_mm for a in p.abschnitte]
    assert breiten == [1200.0, 2600.0], p.abschnitte
    assert p.abschnitte[0].von_mm == 0.0
    assert p.abschnitte[1].bis_mm == 10000.0
    assert p.breite_min_mm == 1200.0
    # kein Mittelwert irgendwo:
    assert all(a.breite_mm in (1200.0, 2600.0) for a in p.abschnitte)


def test_kurze_engstelle_reduziert_die_abschnittsbreite_nicht() -> None:
    # 1,60-m-Gang mit einem 300 mm tiefen Pfeiler auf 400 mm Länge → 1,30 m
    flaeche = Polygon([(0, 0), (8000, 0), (8000, 1600), (4400, 1600),
                       (4400, 1300), (4000, 1300), (4000, 1600), (0, 1600)])
    p = miss_breitenprofil("seg_3", [(0, 650), (8000, 650)], flaeche)
    assert [a.breite_mm for a in p.abschnitte] == [1600.0]
    assert len(p.engstellen) == 1
    eng = p.engstellen[0]
    assert eng.breite_mm == 1300.0
    assert 4000.0 <= eng.position_mm <= 4400.0
    assert eng.laenge_mm <= 500.0
    assert p.breite_min_mm == 1300.0                # Minimum getrennt geführt


def test_tuerdurchgang_ist_eigener_punkt_keine_gangbreite() -> None:
    # Zwei 1,60-m-Räume, dazwischen eine 900-mm-Türöffnung in der Wand
    flaeche = Polygon([(0, 0), (8000, 0), (8000, 1600), (0, 1600)]).difference(
        Polygon([(3900, -10), (4100, -10), (4100, 350), (3900, 350)])
    ).difference(
        Polygon([(3900, 1250), (4100, 1250), (4100, 1610), (3900, 1610)])
    )
    p = miss_breitenprofil("seg_4", [(0, 800), (8000, 800)], flaeche,
                           tueren_mm=[(4000, 800)])
    tuer = [m for m in p.tuerpunkte]
    assert tuer, "Türdurchgang nicht als eigener Punkt geführt"
    assert all(m.ist_tuerdurchgang for m in tuer)
    assert {round(m.breite_mm) for m in tuer} == {900}
    # Türpunkte gehen weder in Abschnitte noch in breite_min_mm ein:
    assert [a.breite_mm for a in p.abschnitte] == [1600.0]
    assert p.breite_min_mm == 1600.0
    assert p.engstellen == []


def test_fehlende_messung_ist_none_mit_grund() -> None:
    leer = miss_breitenprofil("seg_5", [(0, 0)], None)
    assert not leer.messbar and leer.grund == "achse_nicht_ermittelbar"
    assert leer.breite_min_mm is None

    ohne = miss_breitenprofil("seg_6", [(0, 0), (1000, 0)], None)
    assert not ohne.messbar and ohne.grund == "flaeche_fehlt"

    daneben = miss_breitenprofil("seg_7", [(0, 50000), (2000, 50000)],
                                 _gerader_gang(1200, 6000))
    assert not daneben.messbar
    assert daneben.grund == "punkt_ausserhalb_flaeche"
    assert all(m.breite_mm is None and m.grund for m in daneben.profil)


def test_skelett_zickzack_gilt_nicht_als_richtungswechsel() -> None:
    """GRAPH-Achsen sind Skelett-Polylinien mit Mini-Knicken — die dürfen das
    Profil nicht wegfiltern (sonst bleibt kein messbarer Punkt übrig)."""
    flaeche = _gerader_gang(1200, 6000)
    zickzack = [(x, 600 + (20 if i % 2 else -20)) for i, x in enumerate(range(0, 6001, 200))]
    p = miss_breitenprofil("seg_z", zickzack, flaeche)
    assert p.messbar
    assert not any(m.an_richtungswechsel for m in p.profil)
    # Die Sehnen-Normale nimmt dem Zickzack die Schräge: ohne sie wären es
    # 1223.8 mm (1200 / cos 11.3 Grad), mit ihr bleiben 0.8 mm Restfehler.
    assert len(p.abschnitte) == 1
    assert abs(p.abschnitte[0].breite_mm - 1200.0) <= 1.0


def test_abschnitt_traegt_quelle_gemessen() -> None:
    p = miss_breitenprofil("seg_q", [(0, 600), (6000, 600)], _gerader_gang(1200, 6000))
    assert [a.quelle for a in p.abschnitte] == ["gemessen"]


def test_ecke_in_einen_saal_loescht_nicht_das_ganze_profil() -> None:
    """Eckfenster ist auf die halbe typische Segmentbreite gedeckelt.

    Ohne Deckel skaliert es mit der AN DER ECKE gemessenen (dort aufgeblähten)
    Breite — auf Rennweg_EG blieben so 7 von 68 Punkten übrig.
    """
    # 1,20-m-Gang (x 0..8000) mündet in einen 6-m-Saal (x 8000..14000).
    flaeche = Polygon([(0, 0), (14000, 0), (14000, 6000), (8000, 6000),
                       (8000, 1200), (0, 1200)])
    p = miss_breitenprofil("seg_saal", [(0, 600), (11000, 600), (11000, 5000)],
                           flaeche)
    assert p.messbar
    gang = [m for m in p.profil
            if m.laufmeter_mm < 7000 and not m.an_richtungswechsel]
    assert len(gang) > 50, f"Eckfilter frisst den Gang: {len(gang)} Punkte"
    assert p.abschnitte[0].breite_mm == 1200.0


# ── Achse im Wandkörper: Messort schieben, Maß nicht erfinden ────────────────
def _zwei_zimmer_mit_wand(lichte: float, wand: float, laenge: float
                          ) -> list[Polygon]:
    """Zwei lichte Raumpolygone, dazwischen ``wand`` mm Wandkörper (kein Raum)."""
    unten = Polygon([(0, 0), (laenge, 0), (laenge, lichte), (0, lichte)])
    y0 = lichte + wand
    oben = Polygon([(0, y0), (laenge, y0), (laenge, y0 + lichte), (0, y0 + lichte)])
    return [unten, oben]


def test_achse_in_der_wand_wird_gemessen() -> None:
    """Fluchtweglinien liegen oft in der Wandmitte zwischen zwei LICHTEN
    Raumpolygonen. Ohne Snap schneidet die Achse keinen Raum → flaeche_fehlt."""
    raeume = _zwei_zimmer_mit_wand(lichte=2000, wand=200, laenge=6000)
    achse = [(0, 2100), (6000, 2100)]           # exakt Wandmitte, 100 mm daneben

    assert [r for r in raeume if r.intersects(LineString(achse))] == []
    fl = begrenzende_flaechen(raeume, achse)
    assert len(fl) == 2
    assert fl == [raeume[0], raeume[1]]         # unverändert, kein Puffer

    p = miss_breitenprofil("seg_wand", achse, fl)
    assert p.messbar and p.grund is None
    # Gemessen wird die ECHTE lichte Breite des Raums, nicht 2000 + 2*100.
    assert {m.breite_mm for m in p.profil} == {2000.0}
    assert p.breite_min_mm == 2000.0


def test_float_rauschen_auf_der_raumkante_ist_kein_grund() -> None:
    """Achse auf der Polygonkante: ``covers`` scheitert an Float-Rauschen."""
    flaeche = _gerader_gang(1200, 6000)
    p = miss_breitenprofil("seg_kante", [(0, -1e-9), (6000, -1e-9)], [flaeche])
    assert p.messbar
    assert p.breite_min_mm == 1200.0


def test_jenseits_der_snap_toleranz_bleibt_unmessbar() -> None:
    """Kein Default, kein Normwert: weiter weg → None mit Grund."""
    flaeche = _gerader_gang(1200, 6000)
    achse = [(0, 1200 + SNAP_MM + 1), (6000, 1200 + SNAP_MM + 1)]
    assert begrenzende_flaechen([flaeche], achse) == []
    p = miss_breitenprofil("seg_weit", achse, None)
    assert not p.messbar
    assert p.grund == "flaeche_fehlt"
    assert p.breite_min_mm is None


def test_ecke_im_weiten_raum_deckelt_auf_eckfenster() -> None:
    """Regression Mollgasse_EG/seg_72: 62 von 62 Punkten als Richtungswechsel
    verworfen, weil der Deckel Median/2 (≈3500 mm) das ganze Segment abdeckt."""
    raum = Polygon([(0, 0), (12000, 0), (12000, 7000), (0, 7000)])
    p = miss_breitenprofil("seg_weit_raum",
                           [(1000, 1000), (4000, 1000), (4000, 4000)], raum)
    assert p.messbar, p.grund
    ecken = [m for m in p.profil if m.an_richtungswechsel]
    # Fenster ±ECKE_FENSTER_MM um den Knick bei 3000 mm, nicht ±3500 mm.
    assert len(ecken) <= 11, f"{len(ecken)} Punkte verworfen"
    assert all(abs(m.laufmeter_mm - 3000.0) <= ECKE_FENSTER_MM for m in ecken)


# ── breite_max_mm: die breiteste erfasste Stelle eines Abschnitts ────────────
# Der Median einer Abschnittsbreite verdeckt breitere Stellen im selben
# Abschnitt — innerhalb des Toleranzbandes und erst recht über eine
# zusammengezogene kurze Störstelle hinweg. breite_max_mm macht sie sichtbar.
# Es ist das Maximum der ERFASSTEN Punkte, kein Nachweis lückenloser Geometrie.
def test_breite_max_bei_konstanter_breite_gleich_der_abschnittsbreite() -> None:
    p = miss_breitenprofil("seg_max_1", [(0, 600), (6000, 600)],
                           _gerader_gang(1200, 6000))
    assert len(p.abschnitte) == 1
    a = p.abschnitte[0]
    assert a.breite_mm == 1200.0
    assert a.breite_max_mm == 1200.0        # nichts Breiteres vorhanden
    assert a.quelle == "gemessen"


def test_median_unter_2000_aber_messwert_darueber_bleibt_sichtbar() -> None:
    """Aufweitung INNERHALB des Toleranzbandes: ein Abschnitt, Median 1950,
    aber 2030 mm gemessen. Ohne breite_max_mm verschwände die Überschreitung
    der 2-m-Grenze in der Zusammenfassung."""
    flaeche = Polygon([(0, 0), (8000, 0), (8000, 1950), (4600, 1950),
                       (4600, 2030), (4000, 2030), (4000, 1950), (0, 1950)])
    p = miss_breitenprofil("seg_max_2", [(0, 975), (8000, 975)], flaeche)
    assert len(p.abschnitte) == 1, p.abschnitte
    a = p.abschnitte[0]
    assert a.breite_mm < 2000.0             # Median unter der Grenze
    assert a.breite_max_mm is not None and a.breite_max_mm > 2000.0
    # Der Messwert selbst ist unverändert im Profil vorhanden:
    assert max(m.breite_mm for m in p.profil if m.breite_mm is not None) == a.breite_max_mm
    assert p.breite_min_mm == 1950.0        # Minimum unberührt


def test_zusammenfuehrung_ueber_kurze_stoerstelle_behaelt_das_maximum() -> None:
    """Eine 300 mm kurze Aufweitung auf 2100 mm erreicht die Mindestlänge
    nicht und wird dem Nachbarn zugeschlagen. Ihr Messwert darf dabei NICHT
    verlorengehen."""
    flaeche = Polygon([(0, 0), (8000, 0), (8000, 1600), (4300, 1600),
                       (4300, 2100), (4000, 2100), (4000, 1600), (0, 1600)])
    p = miss_breitenprofil("seg_max_3", [(0, 800), (8000, 800)], flaeche)
    assert [a.breite_mm for a in p.abschnitte] == [1600.0], p.abschnitte
    a = p.abschnitte[0]
    assert a.von_mm <= 4000.0 and a.bis_mm >= 4300.0   # Störstelle liegt drin
    assert a.breite_max_mm == 2100.0
    assert p.breite_min_mm == 1600.0
    assert p.engstellen == []               # eine Aufweitung ist keine Engstelle


def test_messluecken_und_tuerpunkte_heben_das_maximum_nicht() -> None:
    """Nicht messbare Punkte und Türdurchgänge gehen nicht in das Maximum ein;
    sie bleiben im Profil sichtbar."""
    # (a) Messlücke: die Fläche endet bei 4000, die Achse läuft bis 8000.
    p = miss_breitenprofil("seg_max_4", [(0, 600), (8000, 600)],
                           _gerader_gang(1200, 4000))
    assert p.messbar
    ohne = [m for m in p.profil if m.breite_mm is None]
    assert ohne and all(m.grund for m in ohne), "Lücke ohne Grund"
    assert all(a.breite_max_mm == 1200.0 for a in p.abschnitte), p.abschnitte

    # (b) Türdurchgang: der schmale Türwert taucht im Maximum nicht auf, der
    # Gangwert bleibt das Maximum.
    flaeche = _gerader_gang(1600, 8000).difference(
        Polygon([(3900, 1250), (4100, 1250), (4100, 1610), (3900, 1610)])
    )
    q = miss_breitenprofil("seg_max_5", [(0, 800), (8000, 800)], flaeche,
                           tueren_mm=[(4000, 800)])
    assert q.tuerpunkte
    assert [a.breite_mm for a in q.abschnitte] == [1600.0]
    assert all(a.breite_max_mm == 1600.0 for a in q.abschnitte)


def test_breite_max_ist_ohne_bestimmung_none() -> None:
    """Default des Modells: nicht bestimmt heißt None, nie 0.0."""
    from notbeleuchtung.raumerkennung.breitenprofil import Abschnitt
    assert Abschnitt(0.0, 100.0, 1200.0).breite_max_mm is None
