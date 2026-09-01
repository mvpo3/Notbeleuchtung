"""abstand_nachpass — Entzerrung von Symbol-Kollisionen an der Strategie-Naht."""
import math

from notbeleuchtung.hauptengine.contracts import BBox, Platzierung, Raum, RaumModell
from notbeleuchtung.platzierung import abstand_nachpass
from notbeleuchtung.platzierung.abstand_nachpass import _MIN_ABSTAND_MM
from notbeleuchtung.platzierung.geometry import point_in_polygon


def _p(x: float, y: float, kind: str = "rz") -> Platzierung:
    schluessel = {"rz": "notlicht_ks_stiege_unten"}.get(kind, "sicherheitsleuchte_aufheller")
    return Platzierung(xy_mm=(x, y), catalog_key=schluessel, kind=kind, norm_quelle="q")


def _raum(*polygone: list) -> RaumModell:
    raeume = [
        Raum(id=f"r{i}", raum_typ="GANG", polygon_mm=poly)
        for i, poly in enumerate(polygone)
    ]
    return RaumModell(
        floor="T", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(100000.0, 100000.0)),
        raeume=raeume,
    )


def _dist(a, b) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _alle_abstaende_ok(plzg: list[Platzierung]) -> bool:
    return all(
        _dist(plzg[i].xy_mm, plzg[j].xy_mm) >= _MIN_ABSTAND_MM
        for i in range(len(plzg))
        for j in range(i + 1, len(plzg))
    )


def test_zwei_koinzidente_rz_werden_gemergt():
    a, b = _p(0.0, 0.0, "rz"), _p(50.0, 0.0, "rz")   # 50 mm < 250 → Dublette
    out = abstand_nachpass.entzerre([a, b], _raum())
    assert len(out) == 1
    assert out[0].xy_mm == (0.0, 0.0)                 # das erste (früher im Original) bleibt


def test_rz_und_sl_koinzident_beide_bleiben_entzerrt():
    rz, sl = _p(0.0, 0.0, "rz"), _p(0.0, 0.0, "sicherheitsleuchte")
    out = abstand_nachpass.entzerre([rz, sl], _raum())
    assert len(out) == 2
    kinds = {p.kind for p in out}
    assert kinds == {"rz", "sicherheitsleuchte"}
    rz_out = next(p for p in out if p.kind == "rz")
    sl_out = next(p for p in out if p.kind == "sicherheitsleuchte")
    assert rz_out.xy_mm == (0.0, 0.0)                 # höherrangiges RZ bleibt stehen
    assert sl_out.xy_mm != (0.0, 0.0)                 # SL weicht
    assert _dist(rz_out.xy_mm, sl_out.xy_mm) >= _MIN_ABSTAND_MM


def test_nudge_bleibt_im_raumpolygon():
    # Quadratischer Raum; das Paar sitzt an der rechten Wand → der Nudge nach außen
    # verließe den Raum, muss also nach innen ausweichen.
    poly = [(0.0, 0.0), (10000.0, 0.0), (10000.0, 10000.0), (0.0, 10000.0)]
    rz = _p(9900.0, 5000.0, "rz")
    sl = _p(9950.0, 5000.0, "sicherheitsleuchte")    # rechts vom RZ, Richtung Wand
    out = abstand_nachpass.entzerre([rz, sl], _raum(poly))
    sl_out = next(p for p in out if p.kind == "sicherheitsleuchte")
    assert point_in_polygon(sl_out.xy_mm, poly)      # im Raum geblieben
    assert _alle_abstaende_ok(out)


def test_nicht_kollidierende_symbole_unveraendert_und_reihenfolge_stabil():
    a, b, c = _p(0.0, 0.0, "rz"), _p(5000.0, 0.0, "sicherheitsleuchte"), _p(0.0, 5000.0, "antipanik")
    out = abstand_nachpass.entzerre([a, b, c], _raum())
    assert [p.xy_mm for p in out] == [(0.0, 0.0), (5000.0, 0.0), (0.0, 5000.0)]
    assert [p.kind for p in out] == ["rz", "sicherheitsleuchte", "antipanik"]


def test_idempotent():
    plzg = [_p(0.0, 0.0, "rz"), _p(0.0, 0.0, "sicherheitsleuchte"), _p(100.0, 0.0, "antipanik")]
    raum = _raum()
    out1 = abstand_nachpass.entzerre(plzg, raum)
    out2 = abstand_nachpass.entzerre(out1, raum)
    assert [p.xy_mm for p in out1] == [p.xy_mm for p in out2]
    assert [p.kind for p in out1] == [p.kind for p in out2]
    assert _alle_abstaende_ok(out1)


def test_deterministisch_unabhaengig_von_eingabereihenfolge():
    rz, sl = _p(0.0, 0.0, "rz"), _p(0.0, 0.0, "sicherheitsleuchte")

    def signatur(out):
        return sorted((p.kind, round(p.xy_mm[0], 3), round(p.xy_mm[1], 3)) for p in out)

    assert signatur(abstand_nachpass.entzerre([rz, sl], _raum())) == \
        signatur(abstand_nachpass.entzerre([sl, rz], _raum()))


def test_guards_leer_und_einzeln():
    raum = _raum()
    assert abstand_nachpass.entzerre([], raum) == []
    einzeln = _p(1.0, 2.0, "rz")
    out = abstand_nachpass.entzerre([einzeln], raum)
    assert len(out) == 1 and out[0] is einzeln


def test_eingabe_wird_nicht_mutiert():
    rz, sl = _p(0.0, 0.0, "rz"), _p(0.0, 0.0, "sicherheitsleuchte")
    abstand_nachpass.entzerre([rz, sl], _raum())
    assert sl.xy_mm == (0.0, 0.0)                     # Original unverändert (model_copy)
