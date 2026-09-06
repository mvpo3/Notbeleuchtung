"""pipeline — OIB-Pfad (3. Input): ProjektKontext → bewerte_oib → Gate + Audit.

Defensiv-Nachweis: ohne ProjektKontext (oder ohne OIB-Provider) ruft die Pipeline
`place` exakt wie bisher und der Summary trägt keinen "oib"-Block — das Ergebnis
ist bit-identisch zum Stand vor dem OIB-Anschluss.
"""
from __future__ import annotations

import pytest

from fakes import build_fake_bundle, build_fake_bundle_mit_oib
from notbeleuchtung.hauptengine.contracts import Gebaeudeteil, ProjektKontext
from notbeleuchtung.hauptengine.pipeline import run

_KONTEXT = ProjektKontext(
    jurisdiction="AT",
    gebaeudeteile=[Gebaeudeteil(id="teil_1", nutzungsart="SONSTIGES_GEBAEUDE")],
)


def test_ohne_projekt_kontext_kein_oib_block_und_identisches_ergebnis():
    ohne_oib = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG")
    mit_provider = run(build_fake_bundle_mit_oib(), dxf_path="<fake>", floor="4OG")
    # Provider verdrahtet, aber kein ProjektKontext → OIB-Pfad läuft nicht.
    assert "oib" not in ohne_oib.render_summary
    assert "oib" not in mit_provider.render_summary
    a = [(p.xy_mm, p.kind) for p in ohne_oib.platzierung.platzierungen]
    b = [(p.xy_mm, p.kind) for p in mit_provider.platzierung.platzierungen]
    assert a == b


def test_kontext_ohne_provider_laeuft_wie_bisher():
    out = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG",
              projekt_kontext=_KONTEXT)
    assert "oib" not in out.render_summary


def test_oib_summary_zaehlt_scope_je_raum():
    """Seit 05.09.: kein projekt-globales Gate mehr, sondern Scope je Raum. Der
    Fake-Gebäudeteil trägt keine raum_referenzen → alle Räume UNGEKLÄRT."""
    out = run(build_fake_bundle_mit_oib("eingeschraenkt"), dxf_path="<fake>",
              floor="4OG", projekt_kontext=_KONTEXT)
    oib = out.render_summary["oib"]
    assert oib["stufen"] == {"teil_1": "eingeschraenkt"}
    assert oib["sanitaer_scope"]["anwendbar"] == 0
    assert oib["sanitaer_scope"]["ungeklaert"] > 0
    assert any("UNGEKLÄRT" in h for h in oib["hinweise"])


def test_oib_summary_bei_review_required():
    out = run(build_fake_bundle_mit_oib("review_required"), dxf_path="<fake>",
              floor="4OG", projekt_kontext=_KONTEXT)
    oib = out.render_summary["oib"]
    assert any("review_required" in h for h in oib["hinweise"])
    assert oib["sanitaer_scope"]["anwendbar"] == 0
    # Fail-closed heißt: der Plan selbst entsteht trotzdem (nur ohne Flächen-Trigger).
    assert out.platzierung.platzierungen


def test_ungeklaerter_scope_erscheint_im_pruefbericht():
    """Regel 13: der ungeklärte Geltungsbereich darf nicht lautlos verschwinden."""
    out = run(build_fake_bundle_mit_oib("review_required"), dxf_path="<fake>",
              floor="4OG", projekt_kontext=_KONTEXT)
    treffer = [
        b for b in out.render_summary["pruefung"]["befunde"]
        if "Geltungsbereich ungeklärt" in b["regel"]
    ]
    assert len(treffer) == 1 and treffer[0]["status"] == "warnung"


def test_ohne_oib_pfad_kein_scope_befund():
    """Bestehende Pläne ohne ProjektKontext bekommen keine neue Warnung."""
    out = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG")
    assert not [
        b for b in out.render_summary["pruefung"]["befunde"]
        if "Geltungsbereich ungeklärt" in b["regel"]
    ]


def test_regel13_erreicht_den_gezeichneten_pruefbericht(tmp_path, monkeypatch):
    """Sichtbarkeit bis zur Ausgabe: der Befund darf nicht nur im Summary-Dict
    stehen. Er muss im gezeichneten Prüfbericht des Plans landen — und den
    Gesamtstatus mitnehmen. Ein interner Eintrag allein genügt nicht.

    Blatt-Vorlage hier aus: Owner-Fixierung 2026-09-05 unterdrückt im Blatt-Modus
    ALLE Zusatz-Boxen (auch den Prüfbericht — bleibt im Summary/API); die
    Zeichnungs-Naht dieses Tests existiert nur im Fallback-Pfad ohne Vorlage."""
    ezdxf = pytest.importorskip("ezdxf")
    from notbeleuchtung.hauptengine.render import dxf_renderer as _dr
    monkeypatch.setitem(_dr._blatt_vorlage_cache, "doc", None)
    out_dxf = tmp_path / "plan.dxf"
    out = run(build_fake_bundle_mit_oib("review_required"), dxf_path="<fake>",
              floor="4OG", out_path=str(out_dxf), projekt_kontext=_KONTEXT)

    assert out.render_summary["pruefung"]["status"] == "warnung"
    assert out.render_summary["pruefbericht_drawn"] is True

    doc = ezdxf.readfile(str(out_dxf))
    bloecke = [
        e.text for e in doc.modelspace()
        if e.dxftype() == "MTEXT" and "PRÜFBERICHT" in e.text
    ]
    assert len(bloecke) == 1
    assert "Geltungsbereich ungeklärt" in bloecke[0]
    assert bloecke[0].startswith("PRÜFBERICHT (EN 1838): WARNUNG")
