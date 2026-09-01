"""circuit_zuordnung — Dauer-/Bereitschaftslicht trennen + je Kreis deckeln (#78)."""
from notbeleuchtung.hauptengine.contracts import Platzierung
from notbeleuchtung.platzierung import circuit_zuordnung as CZ


def _p(kind: str, kreis: str = "AGV-A-F13") -> Platzierung:
    return Platzierung(xy_mm=(0.0, 0.0), catalog_key="k", kind=kind, circuit_hint=kreis)


def test_dauer_und_bereitschaftslicht_getrennt():
    out = CZ.zuordnen([_p("rz"), _p("sicherheitsleuchte"), _p("antipanik")])
    hints = [p.circuit_hint for p in out]
    assert hints[0] == "AGV-A-F13-DL-1"      # RZ = Dauerlicht → eigener Kreis
    assert hints[1] == "AGV-A-F13-BL-1"      # SL = Bereitschaftslicht → getrennter Kreis
    assert hints[2] == "AGV-A-F13-BL-1"      # AP = BL → selber Kreis wie SL
    assert all("F13" in h for h in hints)    # SV-Kennung bleibt (Naht zu validierung)


def test_gebaeude_bleibt_erhalten():
    out = CZ.zuordnen([_p("rz", "AGV-B-F13"), _p("rz", "AGV-A-F13")])
    assert out[0].circuit_hint == "AGV-B-F13-DL-1"
    assert out[1].circuit_hint == "AGV-A-F13-DL-1"


def test_deckel_bricht_auf_zweiten_kreis():
    # 25 RZ, selbes Gebäude/Art → 2 Kreise (Deckel 20 je Kreis).
    out = CZ.zuordnen([_p("rz") for _ in range(25)])
    assert {p.circuit_hint for p in out} == {"AGV-A-F13-DL-1", "AGV-A-F13-DL-2"}
    assert sum(1 for p in out if p.circuit_hint.endswith("-DL-1")) == 20