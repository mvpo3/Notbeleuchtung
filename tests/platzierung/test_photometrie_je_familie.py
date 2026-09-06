"""Per-Familie-Photometrie: jeder Lux-Nachweis rechnet mit der LDT SEINER Leuchte.

Befund 2026-09-06: `photometrie_mapping.yaml` mappte längst je catalog_key,
aber `ldt_pfad_fuer` war toter Code — der Antipanik-0,5-lx-Nachweis rechnete
isotrop (200 cd), obwohl die Rundlinsen-LDT im Katalog lag. Jetzt baut die
Registry je Familie ein Callable (`photometrie_je_key`) und der Platzierer
reicht es bis in `_antipanik_punkte` durch.

Kontext AP3 (din Concept 2): deren LDT ist NICHT öffentlich (Produktportal nur
Datenblätter, kein Relux/DIALux) — sobald der Owner sie beim Hersteller anfragt,
ist sie eine 1-Zeilen-Ergänzung im YAML und wirkt sofort über diese Naht.
"""
from __future__ import annotations

import pytest

from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import BBox, Raum, RaumModell
from notbeleuchtung.hauptengine.registry import photometrie_je_key
from notbeleuchtung.platzierung.flaechen_strategy import plan_antipanik

SAAL_POLY = [(0.0, 0.0), (12000.0, 0.0), (12000.0, 9000.0), (0.0, 9000.0)]


def _saal_raum() -> RaumModell:
    return RaumModell(
        floor="EG", bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(12000.0, 9000.0)),
        raeume=[Raum(id="saal", raum_typ="SAAL", polygon_mm=SAAL_POLY, flaeche_m2=108.0)],
    )


# ── Registry: Katalog → Callables ───────────────────────────────────────────
def test_registry_liefert_callable_je_katalog_key():
    je_key = photometrie_je_key()
    if not je_key:
        pytest.skip("Photometrie-Katalog nicht vorhanden")
    assert "antipanik_leuchte" in je_key
    fn = je_key["antipanik_leuchte"]
    # Rundlinse: an den Daten geprüft rotationssymmetrisch → C-Ebene folgenlos.
    assert getattr(fn, "rotationssymmetrisch", None) is True
    assert fn(30.0) > 0


def test_registry_dedupliziert_gleiche_ldt():
    je_key = photometrie_je_key()
    if not je_key:
        pytest.skip("Photometrie-Katalog nicht vorhanden")
    # sicherheitsleuchte_aufheller + notlicht_kw_garage teilen die Rundlinsen-LDT.
    assert je_key["sicherheitsleuchte_aufheller"] is je_key["notlicht_kw_garage"]


# ── Durchfädelung bis in den Antipanik-Nachweis ─────────────────────────────
def test_antipanik_nachweis_nutzt_familien_callable():
    aufrufe = []

    def spion(gamma, c=None):
        aufrufe.append(gamma)
        return 200.0

    ergebnis = plan_antipanik(
        _saal_raum(), FakeNormProvider(),
        i_cd_fn_je_key={"antipanik_leuchte": spion},
    )
    assert any(p.kind == "antipanik" for p in ergebnis)
    assert aufrufe, "Familien-Callable wurde vom Lux-Nachweis nicht befragt"


def test_ohne_zuordnung_bleibt_isotrop():
    """Kein Mapping für den Key → Nachweis wie bisher (isotrope Annahme)."""
    mit = plan_antipanik(_saal_raum(), FakeNormProvider(), i_cd_fn_je_key={})
    ohne = plan_antipanik(_saal_raum(), FakeNormProvider())
    assert [p.xy_mm for p in mit] == [p.xy_mm for p in ohne]


def test_schwache_leuchte_verdichtet_staerker():
    """Physik-Probe: eine schwächere Familien-LDT muss MEHR Antipanik-Punkte
    erzwingen als die isotrope 200-cd-Annahme — nie weniger Nachweis.
    (5 cd verfehlt im 12×9-Saal die 0,5 lx / Ud mit dem 4er-Norm-Raster.)"""
    ohne = plan_antipanik(_saal_raum(), FakeNormProvider())
    schwach = plan_antipanik(
        _saal_raum(), FakeNormProvider(),
        i_cd_fn_je_key={"antipanik_leuchte": lambda g, c=None: 5.0},
    )
    assert len(schwach) > len(ohne), f"{len(schwach)} !> {len(ohne)}"
