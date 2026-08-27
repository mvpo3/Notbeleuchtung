"""Registry — der EINE Ort, an dem konkrete Owner-Impls an die Ports gebunden werden.

Dependency-Inversion-Verdrahtung. `build_default_bundle()` bindet die echten
Provider (werden Slice 1/2/4 nach und nach real). Test-Doubles injiziert
`tests/fakes.py` direkt über `ProviderBundle`, nie hierüber.
"""
from __future__ import annotations

from .contracts import ProviderBundle


def build_default_bundle() -> ProviderBundle:
    """Echte Provider. Slice 0: noch nicht verdrahtet — echte Impls kommen
    Slice 1 (Norm), 2 (Platzierer), 4 (Raum)."""
    raise NotImplementedError(
        "Echte Provider ab Slice 1/2/4. Slice 0 läuft über tests/fakes.py."
    )
