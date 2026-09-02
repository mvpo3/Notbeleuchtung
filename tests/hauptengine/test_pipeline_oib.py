"""pipeline — OIB-Pfad (3. Input): ProjektKontext → bewerte_oib → Gate + Audit.

Defensiv-Nachweis: ohne ProjektKontext (oder ohne OIB-Provider) ruft die Pipeline
`place` exakt wie bisher und der Summary trägt keinen "oib"-Block — das Ergebnis
ist bit-identisch zum Stand vor dem OIB-Anschluss.
"""
from __future__ import annotations

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


def test_oib_summary_gate_offen():
    out = run(build_fake_bundle_mit_oib("eingeschraenkt"), dxf_path="<fake>",
              floor="4OG", projekt_kontext=_KONTEXT)
    oib = out.render_summary["oib"]
    assert oib["flaechen_trigger_gate"] == "offen"
    assert oib["stufen"] == {"teil_1": "eingeschraenkt"}
    assert any("projekt-global" in h for h in oib["hinweise"])


def test_oib_summary_gate_zu_bei_review_required():
    out = run(build_fake_bundle_mit_oib("review_required"), dxf_path="<fake>",
              floor="4OG", projekt_kontext=_KONTEXT)
    oib = out.render_summary["oib"]
    assert oib["flaechen_trigger_gate"] == "zu"
    assert any("review_required" in h for h in oib["hinweise"])
    # Fail-closed heißt: der Plan selbst entsteht trotzdem (nur ohne Flächen-Trigger).
    assert out.platzierung.platzierungen
