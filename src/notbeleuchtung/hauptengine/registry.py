"""Registry — der EINE Ort, an dem konkrete Owner-Impls an die Ports gebunden werden.

Dependency-Inversion-Verdrahtung. `build_default_bundle()` bindet die echten Provider
der drei Owner. Test-Doubles injiziert `tests/fakes.py` direkt über `ProviderBundle`,
nie hierüber.

**Lazy-Import (bewusst):** die Owner-Packages werden erst *beim Aufruf* importiert,
nicht beim Modul-Import. So bleibt die Engine (und die API) importierbar, solange ein
Provider-Package noch Scaffold ist (Enis' `normwissen`-Slice-1 / Selman's
`raumerkennung`-Slice-4 noch nicht auf main). Fehlt ein Provider, schlägt der Aufruf
mit `ImportError` fehl — die API übersetzt das in ein sauberes 503 „noch nicht
verdrahtet". Sind #6 (Norm) + #13 (Raum) gemergt, liefert `build_default_bundle()`
ohne weitere Änderung das echte Trio.
"""
from __future__ import annotations

from .contracts import ProviderBundle


def build_default_bundle() -> ProviderBundle:
    """Das echte Owner-Trio: ArchitekturRaumProvider (Selman) + En1838NormProvider
    (Enis) + NotlichtPlatzierer (Leonis). Lazy-Import — s. Modul-Docstring."""
    from notbeleuchtung.normwissen import En1838NormProvider
    from notbeleuchtung.platzierung import NotlichtPlatzierer
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    return ProviderBundle(
        raum=ArchitekturRaumProvider(),
        norm=En1838NormProvider(),
        platzierer=NotlichtPlatzierer(),
    )
