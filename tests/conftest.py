"""Gemeinsame Regeln der ganzen Suite (auch Gate und Naht).

KI-Zweitmeinung (Auftrag 2026-10-01 § 3): „Suite und Gate rufen die KI nie live auf." Ein in
der Umgebung gesetztes ``NOTBEL_KI=an`` (z. B. für die Prüfstrecke) darf pytest nicht
einschalten — sonst führe jeder ``provider.parse`` einen echten ``codex exec`` aus. Tests, die
die KI brauchen, geben ``KiKonfig``/Backend ausdrücklich mit. Nur ``NOTBEL_KI_LIVE=1``
(der ausdrückliche Live-Schalter des Live-Tests) lässt die Umgebung unangetastet.
"""
from __future__ import annotations

import os

import pytest


@pytest.fixture(autouse=True, scope="session")
def _ki_nie_live_aus_der_umgebung():
    if os.environ.get("NOTBEL_KI_LIVE") == "1":
        yield
        return
    gesichert = {k: os.environ.pop(k) for k in list(os.environ) if k.startswith("NOTBEL_KI")}
    yield
    os.environ.update(gesichert)
