"""schacht_abgleich — Owner-Regel b (Slice K2): Schächte laufen senkrecht.

Synthetisch: drei Geschosse, der Schacht fehlt im mittleren → Warnung mit
Position, kein Raum wird erzeugt oder umtypisiert.
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum
from notbeleuchtung.raumerkennung.schacht_abgleich import (
    WARNUNG,
    geschoss_rang,
    gleiche_schaechte_ab,
)


def _r(rid: str, typ: str, x: float, y: float, w: float = 1000.0) -> Raum:
    return Raum(id=rid, raum_typ=typ, flaeche_m2=w * w / 1e6,
                polygon_mm=[(x, y), (x + w, y), (x + w, y + w), (x, y + w)])


def test_luecke_im_mittleren_geschoss_gibt_warnung_und_erfindet_nichts():
    ug = [_r("s_ug", "SCHACHT", 0, 0), _r("z", "ZIMMER", 5000, 0, 4000)]
    eg = [_r("sh", "STIEGENHAUS", -1000, -1000, 3000)]       # deckt die Schachtlage
    og = [_r("s_og", "SCHACHT", 150, -100)]                   # 180 mm versetzt: dieselbe Lage
    vorher = [[(r.id, r.raum_typ) for r in g] for g in (ug, eg, og)]

    lagen = gleiche_schaechte_ab([("UG", ug), ("EG", eg), ("1OG", og)])

    assert len(lagen) == 1
    lage = lagen[0]
    assert lage.xy == (500, 500)
    assert lage.belegt == {"UG": "s_ug", "1OG": "s_og"}
    assert lage.warnungen == [f"{WARNUNG}: EG bei (500, 500) — belegt in UG, 1OG; "
                              "an der Stelle: STIEGENHAUS sh"]
    assert [[(r.id, r.raum_typ) for r in g] for g in (ug, eg, og)] == vorher


def test_nur_zwischen_belegten_geschossen_gesucht():
    """Oberhalb/unterhalb der belegten Geschosse keine Warnung; NISCHE und
    Lagen jenseits der Toleranz (300 mm) zählen nicht als derselbe Schacht."""
    a = [_r("n", "NISCHE", 0, 0)]
    b = [_r("s1", "SCHACHT", 0, 0)]
    c = [_r("s2", "SCHACHT", 0, 0), _r("s3", "SCHACHT", 20000, 0)]
    d = [_r("s4", "SCHACHT", 400, 0)]                         # 400 mm → neue Lage
    lagen = gleiche_schaechte_ab([("EG", a), ("1OG", b), ("2OG", c), ("3OG", d)])
    assert [(lg.belegt, lg.warnungen) for lg in lagen] == [
        ({"1OG": "s1", "2OG": "s2"}, []),
        ({"2OG": "s3"}, []),
        ({"3OG": "s4"}, []),
    ]


def test_mehrere_luecken_je_eine_warnung():
    s = [_r("s", "SCHACHT", 0, 0)]
    lagen = gleiche_schaechte_ab([("UG", s), ("EG", []), ("1OG", s), ("2OG", []),
                                  ("3OG", []), ("DG", s)])
    assert [w.split(" bei ")[0] for w in lagen[0].warnungen] == [
        f"{WARNUNG}: EG", f"{WARNUNG}: 2OG", f"{WARNUNG}: 3OG"]
    assert "an der Stelle: kein Raum" in lagen[0].warnungen[0]


def test_geschoss_rang_unten_nach_oben():
    namen = [("2KG", "2.Kellergeschoß"), ("1KG", "1.Kellergeschoß"), ("UG", "UG - x"),
             ("EG", "EG - x"), ("1OG", "OG1 - x"), ("9OG", "E9"),
             ("DG", "DG1 - Rennweg"), ("DG", "DG2 - Rennweg")]
    raenge = [geschoss_rang(g, n) for g, n in namen]
    assert raenge == [-2, -1, -1, 0, 1, 9, 101, 102]
    assert geschoss_rang("DG", "Dachgeschoß") == 101
    assert geschoss_rang("", "Plan") is None
