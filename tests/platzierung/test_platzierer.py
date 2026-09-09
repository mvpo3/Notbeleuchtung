"""Slice 2 — der echte NotlichtPlatzierer reproduziert die 5 echten 4OG-RZ.

Akzeptanz = **Struktur-Match** (Owner-Entscheid: generativ statt faithful): Position,
Anzahl, kind, covers_segment, norm_quelle ∈ Regelwerk, catalog_key ∈ Mapping. Die
exakten Sub-Grad-Rotationen des Fixtures (180.1° …) sind DXF-Extraktions-Artefakte
und werden bewusst NICHT geprüft — der Platzierer leitet die Orientierung generativ
aus der Segment-Geometrie ab.
"""
import json
from pathlib import Path

from fakes import FakeNormProvider, FakeRaumProvider
from notbeleuchtung.hauptengine.contracts import (
    NormRegelwerk,
    Platzierer,
    PlatzierungsErgebnis,
)
from notbeleuchtung.platzierung import NotlichtPlatzierer
from notbeleuchtung.symbols import catalog_keys

FIXTURES = Path(__file__).parents[1] / "fixtures"


def _load(name: str) -> dict:
    with open(FIXTURES / name, encoding="utf-8") as fh:
        return json.load(fh)


def _place() -> PlatzierungsErgebnis:
    raum = FakeRaumProvider().parse("<fake>", "4OG")
    return NotlichtPlatzierer().place(raum, FakeNormProvider())


def test_erfuellt_platzierer_protocol():
    assert isinstance(NotlichtPlatzierer(), Platzierer)


def test_reproduziert_fuenf_rettungszeichen():
    out = _place()
    assert out.floor == "4OG"
    rz = [p for p in out.platzierungen if p.kind == "rz"]
    assert len(rz) == 5


def test_platziert_aufheller_je_stiegenhaus():
    # Beide STIEGENHÄUSER sind norm-seitig 'sicherheitsleuchte' → je 1 Aufheller
    # am Raum-Zentrum, mit Kein-Segment-Bindung. Dazu kommen seit Slice 2.3 die
    # fachpraxis-B1-Aufheller (je RZ einer, eigene norm_quelle) — hier getrennt
    # gezählt, damit der Stiegenhaus-Teil scharf bleibt.
    out = _place()
    sl = [p for p in out.platzierungen if p.kind == "sicherheitsleuchte"]
    norm_sl = [p for p in sl if not p.norm_quelle.startswith("fachpraxis:")]
    fach_sl = [p for p in sl if p.norm_quelle.startswith("fachpraxis:")]
    assert len(norm_sl) == 2
    assert len(fach_sl) == 4  # 5 RZ, 1 Position läge außerhalb → nicht gesetzt
    assert all(p.catalog_key == "sicherheitsleuchte_aufheller" for p in sl)
    assert all(p.covers_segment == [] for p in sl)


def test_rz_nutzen_direktionale_bloecke():
    # Richtungs-Fix: rechts/links-RZ tragen den dedizierten Block, ohne Rotation/Spiegelung.
    out = _place()
    for p in out.platzierungen:
        if p.kind == "rz" and p.richtung in {"links", "rechts"}:
            assert p.catalog_key == f"notlicht_ks_stiege_{p.richtung}"
            assert p.rotation_deg == 0.0
            assert p.mirror_x is False


def test_positionen_und_covers_matchen_fixture():
    out = _place()
    fixture = PlatzierungsErgebnis.model_validate(_load("platzierung_4og.json"))

    # Golden ist RZ-only → nur die RZ-Platzierungen vergleichen.
    got = {tuple(p.xy_mm): tuple(p.covers_segment) for p in out.platzierungen if p.kind == "rz"}
    want = {tuple(p.xy_mm): tuple(p.covers_segment) for p in fixture.platzierungen}
    assert got == want


def test_naht_norm_quelle_und_catalog_key():
    out = _place()
    quellen = set(NormRegelwerk.model_validate(_load("norm_regelwerk_snapshot.json")).quellen)
    keys = catalog_keys()
    for p in out.platzierungen:
        # Praxis-Platzierungen tragen ihre Quelle im Audit-Trail — bis ein
        # decision_source-Feld existiert (3-Owner-Contract, handoff(contracts)),
        # sind die Präfixe die dokumentierte Ausnahme: "fachpraxis:" (Owner-Wort,
        # Slice 2.3) und "Referenz-Praxis:" (belegte Praxis, z.B. Technik-/Müll-SL).
        _PRAXIS = ("fachpraxis:", "Referenz-Praxis:")
        assert p.norm_quelle in quellen or p.norm_quelle.startswith(_PRAXIS), (
            f"norm_quelle {p.norm_quelle!r} nicht im Regelwerk"
        )
        assert p.catalog_key in keys, f"catalog_key {p.catalog_key!r} fehlt im Mapping"
        if p.kind == "rz":
            assert set(p.covers_segment)  # jedes RZ deckt genau sein Segment
        else:
            assert p.covers_segment == []  # Raum-Leuchten sind nicht segmentgebunden


def test_richtung_ist_gueltiger_kardinal():
    """Orientierung generativ (Kardinal), nicht die GT-Sub-Grad-Werte."""
    out = _place()
    for p in out.platzierungen:
        assert p.richtung in {"links", "rechts", "oben", "unten", "gerade"}
        assert p.rotation_deg in {0.0, 90.0, 180.0, 270.0}


def _rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def _og_mit_arm(kurz_fragment: bool = False):
    """OG mit langem Gang-Arm + oberem Riegel (Stiegenhaus als Fluchtziel).

    Ein Fluchtweg-Segment endet am Stiegenhaus → Segment-Pfad setzt dort 1 RZ; der
    lange Arm bekommt seinen RZ erst durch die Sichtlinien-Garantie."""
    from notbeleuchtung.hauptengine.contracts import (
        Ausgang,
        BBox,
        FluchtwegSegment,
        Raum,
        RaumModell,
        Tuer,
    )
    arm = _rect(8000.0, 1000.0, 9800.0, 23000.0)          # 22 m langer vertikaler Arm
    top = _rect(8000.0, 22000.0, 36000.0, 23800.0)
    stgh = _rect(20000.0, 16000.0, 23000.0, 22000.0)
    raeume = [
        Raum(id="GANG-ARM", raum_typ="GANG", polygon_mm=arm, ist_fluchtweg=True, ist_communal=True),
        Raum(id="GANG-TOP", raum_typ="GANG", polygon_mm=top, ist_fluchtweg=True, ist_communal=True),
        Raum(id="STGH", raum_typ="STIEGENHAUS", polygon_mm=stgh, ist_communal=True),
    ]
    if kurz_fragment:
        raeume.append(Raum(id="GANG-FRAG", raum_typ="GANG",   # 3 m Fragment < 6 m
                           polygon_mm=_rect(30000.0, 1000.0, 33000.0, 2800.0),
                           ist_fluchtweg=True, ist_communal=True))
    tueren = [Tuer(id="STGH-T", xy_mm=(21500.0, 22000.0), von_raum="STGH", nach_raum="GANG-TOP",
                   ist_notausgang=True, tuer_detail="stiegenhaustuer")]
    ausg = [Ausgang(id="STAIR", xy_mm=(21500.0, 22000.0), typ="stair_exit")]
    seg = [FluchtwegSegment(segment_id="s1", polyline_mm=[(8900.0, 1000.0), (8900.0, 22900.0),
                                                          (21500.0, 22900.0)],
                            reason="exit", ziel_ausgang="STAIR")]
    return RaumModell(
        floor="1OG", bounds_mm=BBox(min_xy=(8000.0, 1000.0), max_xy=(36000.0, 23800.0)),
        raeume=raeume, tueren=tueren, ausgaenge=ausg,
        zirkulation={"nodes": [], "edges": [], "segmente": seg},
    )


def test_sichtlinien_garantie_fuellt_langen_arm():
    """Owner-Regel 2026-09-09: der lange Gang-Arm bekommt trotz Segment-Pfad (1 RZ am
    Stiegenhaus) ein eigenes RZ IN seinem Polygon — sonst sieht ein Bewohner beim
    Verlassen der Wohnung im Arm kein Rettungszeichen."""
    from notbeleuchtung.platzierung.geometry import point_in_polygon
    raum = _og_mit_arm()
    out = NotlichtPlatzierer().place(raum, FakeNormProvider())
    arm_poly = raum.raeume[0].polygon_mm
    im_arm = [p for p in out.platzierungen if p.kind == "rz" and point_in_polygon(p.xy_mm, arm_poly)]
    assert im_arm, "langer Gang-Arm ohne RZ — Sichtlinien-Garantie griff nicht"


def test_kurzes_fragment_wird_nicht_gefuellt():
    """Klein-Fragmente (fragmentierte Erkennung, Längsseite < 6 m) werden NICHT
    aufgefüllt — sonst Überproduktion auf realen Plänen (Mollgasse)."""
    from notbeleuchtung.platzierung.geometry import point_in_polygon
    raum = _og_mit_arm(kurz_fragment=True)
    out = NotlichtPlatzierer().place(raum, FakeNormProvider())
    frag_poly = raum.raeume[-1].polygon_mm
    im_frag = [p for p in out.platzierungen if p.kind == "rz" and point_in_polygon(p.xy_mm, frag_poly)]
    assert not im_frag, "Klein-Fragment sollte kein eigenes RZ bekommen"
