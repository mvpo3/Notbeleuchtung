"""S0 — Package-Scaffold: Provider existiert + erfüllt das RaumProvider-Protocol."""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts.ports import RaumProvider
from notbeleuchtung.raumerkennung import ArchitekturRaumProvider


def test_provider_erfuellt_protocol():
    assert isinstance(ArchitekturRaumProvider(), RaumProvider)
