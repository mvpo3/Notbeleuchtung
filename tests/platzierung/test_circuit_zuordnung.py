"""circuit_zuordnung — DL/BL trennen + deckeln (#78) + Symbol-Datenmodell füllen (v1.2.0)."""
from notbeleuchtung.hauptengine.contracts import Platzierung
from notbeleuchtung.platzierung import circuit_zuordnung as CZ


def _p(kind: str, kreis: str = "AGV-A-F13", key: str = "k") -> Platzierung:
    return Platzierung(xy_mm=(0.0, 0.0), catalog_key=key, kind=kind, circuit_hint=kreis)


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


# ── Symbol-Datenmodell (v1.2.0) ───────────────────────────────────────────────


def test_schaltungsart_wird_gefuellt():
    out = CZ.zuordnen([_p("rz"), _p("sicherheitsleuchte"), _p("antipanik")])
    assert [p.schaltungsart for p in out] == ["DL", "BL", "BL"]


def test_luminaire_id_je_art_gezaehlt():
    out = CZ.zuordnen([_p("rz"), _p("sicherheitsleuchte"), _p("rz"), _p("antipanik")])
    assert [p.luminaire_id for p in out] == ["RZ-001", "SL-001", "RZ-002", "AP-001"]


def test_typ_letter_je_catalog_key_in_auftretens_reihenfolge():
    out = CZ.zuordnen([
        _p("rz", key="rz_typ_1"),
        _p("sicherheitsleuchte", key="sl_typ"),
        _p("rz", key="rz_typ_1"),          # gleicher Key → gleicher Letter
        _p("antipanik", key="ap_typ"),
    ])
    assert [p.typ_letter for p in out] == ["A", "B", "A", "C"]


def test_typ_letter_ueber_26_keys_eindeutig():
    out = CZ.zuordnen([_p("rz", key=f"key_{i}") for i in range(28)])
    letters = [p.typ_letter for p in out]
    assert letters[0] == "A" and letters[25] == "Z"
    assert letters[26] == "T27" and letters[27] == "T28"
    assert len(set(letters)) == 28