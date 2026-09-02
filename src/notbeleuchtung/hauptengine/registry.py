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

from collections.abc import Callable
from pathlib import Path

from .contracts import ProviderBundle


def photometrie_i_cd_fn(ldt_path: str | Path) -> Callable[[float], float]:
    """Baut aus einer Hersteller-LDT (F2-Photometrie) das `i_cd_fn(γ_grad) -> cd`-Callable.

    Der EINE Ort, der `platzierung` (F1) an `normwissen.photometrie` (F2) bindet — der
    Platzierer selbst bleibt normwissen-frei (Owner-Grenze). Sobald F2 ein
    `catalog_key → LDT`-Mapping liefert, wird das je Leuchtenfamilie gewählt.
    """
    from notbeleuchtung.normwissen.photometrie import lade_ldt

    photometrie = lade_ldt(ldt_path)
    return lambda gamma_grad: photometrie.intensitaet(gamma_grad)


def build_default_bundle(ldt_path: str | Path | None = None) -> ProviderBundle:
    """Das echte Owner-Trio: ArchitekturRaumProvider (Selman) + En1838NormProvider
    (Enis) + NotlichtPlatzierer (Leonis) + LbTextProvider (Enis, 2. Input). Lazy-Import
    — s. Modul-Docstring.

    `ldt_path` (optional) verdrahtet die richtungsabhängige Hersteller-Photometrie in
    den Platzierer (Lux-Deckung). Ohne LDT rechnet die Deckung konstant-isotrop.
    """
    from notbeleuchtung.normwissen import (
        En1838NormProvider,
        LbTextProvider,
        OibRl2Provider,
    )
    from notbeleuchtung.platzierung import NotlichtPlatzierer
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    i_cd_fn = photometrie_i_cd_fn(ldt_path) if ldt_path is not None else None
    return ProviderBundle(
        raum=ArchitekturRaumProvider(),
        norm=En1838NormProvider(),
        platzierer=NotlichtPlatzierer(i_cd_fn=i_cd_fn),
        lb=LbTextProvider(),
        oib=OibRl2Provider(),
    )
