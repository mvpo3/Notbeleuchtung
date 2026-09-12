"""Punkt 3 (Owner-Reihe 2026-09-12): Bestands-Leuchten-Extraktor — die
R1-/R6-Lichtlinien-Regeln liegen ohne Runner-Handarbeit auf jedem Plan an."""
import ezdxf

from notbeleuchtung.hauptengine import bestand_leuchten
from notbeleuchtung.hauptengine.contracts import BBox, RaumModell


def _raum(max_mm=(20000.0, 10000.0)) -> RaumModell:
    return RaumModell(floor="EG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=max_mm),
                      raeume=[], tueren=[], ausgaenge=[],
                      zirkulation={"nodes": [], "edges": [], "segmente": []})


def _dxf(tmp_path, punkte_m, name="spots", extra_ausreisser=False):
    doc = ezdxf.new()
    blk = doc.blocks.new(name=name)
    blk.add_circle((0.0, 0.0), radius=0.05)
    ms = doc.modelspace()
    for x, y in punkte_m:
        ms.add_blockref(name, (x, y))
    if extra_ausreisser:
        ms.add_blockref(name, (34600.0, 1200.0))   # 34,6-km-Insel (Am-Rain-Klasse)
    pfad = tmp_path / "quelle.dxf"
    doc.saveas(pfad)
    return pfad


def test_meter_quelle_wird_auf_mm_kalibriert(tmp_path):
    # Quelle in METERN (Elektroplan-DE-Klasse): Faktor 1000 legt alle Punkte
    # in die RaumModell-Bounds.
    pfad = _dxf(tmp_path, [(2.0, 5.0), (6.0, 5.0), (10.0, 5.0)])
    pts = bestand_leuchten.extrahiere_fuer(_raum(), pfad)
    assert pts == ((2000.0, 5000.0), (6000.0, 5000.0), (10000.0, 5000.0))


def test_ausreisser_fliegen_mit_der_kalibrierung(tmp_path):
    pfad = _dxf(tmp_path, [(2.0, 5.0), (6.0, 5.0), (10.0, 5.0)], extra_ausreisser=True)
    pts = bestand_leuchten.extrahiere_fuer(_raum(), pfad)
    assert len(pts) == 3 and all(x <= 20000.0 for x, _ in pts)


def test_fremdes_vokabular_bleibt_leer(tmp_path):
    pfad = _dxf(tmp_path, [(2.0, 5.0)], name="irgendein_moebel")
    assert bestand_leuchten.extrahiere_fuer(_raum(), pfad) == ()


def test_unplausible_skala_bleibt_leer(tmp_path):
    # Punkte, die mit KEINEM Faktor in die Bounds passen → fail-open ().
    pfad = _dxf(tmp_path, [(900000.0, 900000.0), (950000.0, 950000.0)])
    assert bestand_leuchten.extrahiere_fuer(_raum(max_mm=(5000.0, 5000.0)), pfad) == ()
