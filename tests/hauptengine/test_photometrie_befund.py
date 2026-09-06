"""Grundlage des Lux-Nachweises muss bis in die Ausgabe sichtbar bleiben.

Zwei Fälle, in denen ein bestandener Lux-Grenzwert KEINEN vollständigen
lichttechnischen Nachweis belegt:

1. **anisotrope Optik ohne zugesicherte Ausrichtung** — die Engine rechnet
   konservativ mit dem Minimum über alle C-Ebenen (Fix vom 05.09.2026, s.
   `tests/platzierung/test_lux_c_ebene.py`);
2. **kein auflösbarer Photometrie-Katalog** — Rückfall auf die isotrope
   200-cd-Annahme; das ist kein Hersteller-Nachweis.

Beides muss im Prüfbericht UND in der DXF-Ausgabe stehen und darf durch ein
bestandenes Lux-Ergebnis nicht verschwinden.

⚠️ Betrifft die gemeinsame Integration (`hauptengine/{registry,pipeline,validierung}.py`,
`render/dxf_renderer.py`) — bitte @mvpo3 mit reviewen.
"""
from __future__ import annotations

import pytest

from fakes import build_fake_bundle
from notbeleuchtung.hauptengine.photometrie_befund import (
    KONSERVATIV_SATZ,
    BundleMitPhotometrie,
    PhotometrieBefund,
    photometrie_des_bundles,
)
from notbeleuchtung.hauptengine.pipeline import run
from notbeleuchtung.hauptengine.registry import default_photometrie
from notbeleuchtung.hauptengine.validierung import pruefbericht

_REGEL = "Photometrie-Grundlage"


def _pruef_zeilen(bericht: dict) -> list[str]:
    return [f"{b['regel']} — {b['detail']}" for b in bericht["befunde"]]


# ── Fehlender Katalog am produktiven Einstieg ───────────────────────────────
def test_build_default_bundle_ohne_katalog_weist_isotrope_annahme_aus(monkeypatch):
    """Nicht auflösbarer Katalog am ECHTEN Einstieg — nicht nur ein ungültiger Pfad.

    Der stille Rückfall auf 200 cd bleibt (nichts bricht), er wird aber als
    solcher ausgewiesen und trägt keinen Hersteller-Nachweis.
    """
    from notbeleuchtung.symbols import photometrie_katalog as kat

    monkeypatch.setattr(kat, "_katalog_dir", lambda: None)   # Katalog nicht im Baum
    assert kat.fluchtweg_default_ldt() is None

    from notbeleuchtung.hauptengine.registry import build_default_bundle

    bundle = build_default_bundle()
    befund = photometrie_des_bundles(bundle)
    assert isinstance(bundle, BundleMitPhotometrie)
    assert befund is not None
    assert befund.quelle == "isotrope_annahme"
    assert befund.vollstaendiger_nachweis is False
    assert befund.status == "warnung"
    assert "KEIN Hersteller-Nachweis" in befund.hinweis
    assert befund.ldt_name == ""


def test_katalog_abgeschaltet_ist_ebenfalls_kein_herstellernachweis():
    i_cd_fn, befund = default_photometrie(photometrie_katalog=False)
    assert i_cd_fn is None                      # Platzierer rechnet isotrop 200 cd
    assert befund.quelle == "isotrope_annahme"
    assert befund.vollstaendiger_nachweis is False


def test_produktiver_katalog_ist_anisotrop_und_nicht_ausgerichtet():
    i_cd_fn, befund = default_photometrie()
    if i_cd_fn is None:
        pytest.skip("Photometrie-Katalog nicht vorhanden")
    assert befund.quelle == "hersteller_ldt"
    assert befund.rotationssymmetrisch is False
    assert befund.ausrichtung_zugesichert is False
    assert befund.vollstaendiger_nachweis is False
    assert befund.hinweis == KONSERVATIV_SATZ


def test_zugesicherte_ausrichtung_traegt_den_nachweis():
    i_cd_fn, befund = default_photometrie(c0_azimut_grad=0.0)
    if i_cd_fn is None:
        pytest.skip("Photometrie-Katalog nicht vorhanden")
    assert befund.ausrichtung_zugesichert is True
    assert befund.vollstaendiger_nachweis is True
    assert befund.status == "ok"


# ── Sichtbarkeit im Prüfbericht ─────────────────────────────────────────────
def test_pruefbericht_meldet_die_einschraenkung(monkeypatch):
    out = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG")
    raum, plzg = out.raum, out.platzierung
    _, befund = default_photometrie()
    if befund.quelle != "hersteller_ldt":
        pytest.skip("Photometrie-Katalog nicht vorhanden")

    bericht = pruefbericht(raum, plzg, photometrie=befund)
    zeilen = [z for z in _pruef_zeilen(bericht) if _REGEL in z]
    assert len(zeilen) == 1
    assert KONSERVATIV_SATZ in zeilen[0]
    assert bericht["status"] in {"warnung", "fehler"}


def test_bestandener_lux_grenzwert_hebt_die_einschraenkung_nicht_auf():
    """Alle übrigen Regeln „ok" — die Photometrie-Einschränkung bleibt trotzdem."""
    out = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG")
    _, befund = default_photometrie()
    ohne = pruefbericht(out.raum, out.platzierung)
    mit = pruefbericht(out.raum, out.platzierung, photometrie=befund)
    assert not any(_REGEL in z for z in _pruef_zeilen(ohne))     # ohne Befund: keine Aussage
    assert any(_REGEL in z for z in _pruef_zeilen(mit))
    # Die Einschränkung setzt den Gesamtstatus mindestens auf 'warnung'.
    assert mit["status"] != "ok"


def test_ohne_befund_wird_nichts_behauptet():
    """Fake-Bundle ohne Photometrie-Befund: keine Regel, kein unterstellter Nachweis."""
    out = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG")
    assert "photometrie" not in out.render_summary
    assert not any(_REGEL in z for z in _pruef_zeilen(out.render_summary["pruefung"]))
    assert photometrie_des_bundles(build_fake_bundle()) is None


def test_pipeline_traegt_den_befund_in_summary_und_bericht():
    _, befund = default_photometrie()
    out = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG", photometrie=befund)
    assert out.render_summary["photometrie"]["vollstaendiger_nachweis"] is False
    assert any(_REGEL in z for z in _pruef_zeilen(out.render_summary["pruefung"]))


# ── Sichtbarkeit in der DXF-Ausgabe ─────────────────────────────────────────
def _custom_var(dxf_pfad) -> str | None:
    ezdxf = pytest.importorskip("ezdxf")
    doc = ezdxf.readfile(str(dxf_pfad))
    for tag, wert in doc.header.custom_vars:
        if tag == "NOTBELEUCHTUNG_PHOTOMETRIE":
            return wert
    return None


def test_dxf_traegt_die_einschraenkung_als_zeichnungseigenschaft(tmp_path, monkeypatch):
    pytest.importorskip("ezdxf")
    from notbeleuchtung.hauptengine.render import dxf_renderer as _dr

    monkeypatch.setitem(_dr._blatt_vorlage_cache, "doc", None)   # Fallback-Modus
    _, befund = default_photometrie()
    out_dxf = tmp_path / "plan.dxf"
    out = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG",
              out_path=str(out_dxf), photometrie=befund)

    assert out.render_summary["photometrie_hinweis_drawn"] is True
    wert = _custom_var(out_dxf)
    assert wert is not None and KONSERVATIV_SATZ in wert
    assert wert.startswith("[EINSCHRAENKUNG]")

    # Im Fallback-Modus steht sie zusätzlich in der Prüfbericht-Box.
    doc = pytest.importorskip("ezdxf").readfile(str(out_dxf))
    texte = "\n".join(e.text for e in doc.modelspace() if e.dxftype() == "MTEXT")
    assert KONSERVATIV_SATZ.split(";")[0] in texte


def test_dxf_einschraenkung_auch_ohne_prueberichts_box(tmp_path, monkeypatch):
    """Blatt-Modus unterdrückt laut Owner-Fixierung ALLE Zusatz-Boxen — die
    Einschränkung darf deshalb nicht nur in der Box hängen."""
    pytest.importorskip("ezdxf")
    from notbeleuchtung.hauptengine.render import dxf_renderer as _dr

    _, befund = default_photometrie()
    out_dxf = tmp_path / "plan_blatt.dxf"
    monkeypatch.setattr(_dr, "_draw_pruefbericht", lambda *a, **k: False)
    out = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG",
              out_path=str(out_dxf), photometrie=befund)

    assert out.render_summary["pruefbericht_drawn"] is False
    wert = _custom_var(out_dxf)
    assert wert is not None and KONSERVATIV_SATZ in wert


def test_isotroper_rueckfall_steht_ebenfalls_in_der_dxf(tmp_path):
    pytest.importorskip("ezdxf")
    _, befund = default_photometrie(photometrie_katalog=False)
    out_dxf = tmp_path / "plan_isotrop.dxf"
    run(build_fake_bundle(), dxf_path="<fake>", floor="4OG",
        out_path=str(out_dxf), photometrie=befund)
    wert = _custom_var(out_dxf)
    assert wert is not None
    assert "isotrope Annahme" in wert and "KEIN Hersteller-Nachweis" in wert


def test_vollstaendiger_nachweis_wird_nicht_als_einschraenkung_gemeldet(tmp_path):
    pytest.importorskip("ezdxf")
    befund = PhotometrieBefund(
        quelle="hersteller_ldt", hinweis="rotationssymmetrisch, C-Ebene folgenlos",
        vollstaendiger_nachweis=True, rotationssymmetrisch=True, ldt_name="rund.ldt",
    )
    out_dxf = tmp_path / "plan_ok.dxf"
    out = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG",
              out_path=str(out_dxf), photometrie=befund)
    assert (_custom_var(out_dxf) or "").startswith("[OK]")
    regel = [b for b in out.render_summary["pruefung"]["befunde"] if _REGEL in b["regel"]]
    assert regel and regel[0]["status"] == "ok"
