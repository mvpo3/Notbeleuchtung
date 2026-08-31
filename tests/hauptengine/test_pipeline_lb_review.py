"""pipeline — Fail-Closed-Naht zu Enis' LB-Parser (`LbReviewRequired`).

Wirft `parse_lb` bei blockierendem Zweifel, darf `run()` NICHT crashen: der Plan
wird mit Norm-Default erzeugt, aber `render_summary["lb_review"]` macht sichtbar,
dass die LB-Vorgaben nicht angewendet wurden (Fail-Closed statt stillem Verlust).
"""
from __future__ import annotations

import dataclasses

from fakes import build_fake_bundle
from notbeleuchtung.hauptengine.pipeline import run
from notbeleuchtung.normwissen.lb import LbFehler


class _RaisingLb:
    """LB-Provider, der wie Enis' Parser bei blockierendem Befund abbricht."""

    def parse_lb(self, lb_path: str):
        raise LbFehler("LB erfordert manuelle Prüfung (test.pdf) — kein Notbeleuchtungs-Abschnitt")


def test_lb_review_required_crasht_nicht_und_wird_geflaggt(tmp_path):
    bundle = dataclasses.replace(build_fake_bundle(), lb=_RaisingLb())
    out = run(bundle, dxf_path="<fake>", floor="4OG",
              out_path=tmp_path / "x.dxf", lb_path="egal.pdf")
    # Plan trotzdem erzeugt (Norm-Default greift) …
    assert out.platzierung.platzierungen
    # … und der Review-Bedarf ist sichtbar geflaggt, nicht still verloren.
    rev = out.render_summary.get("lb_review")
    assert rev is not None and rev["status"] == "review_erforderlich"
    assert "manuelle Prüfung" in rev["meldung"]


def test_ohne_lb_kein_review_flag(tmp_path):
    # Ohne LB-Pfad: kein Review-Flag (Norm-Default, aber nichts zu prüfen).
    out = run(build_fake_bundle(), dxf_path="<fake>", floor="4OG", out_path=tmp_path / "y.dxf")
    assert "lb_review" not in out.render_summary
