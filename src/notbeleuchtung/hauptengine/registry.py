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


def photometrie_i_cd_fn(
    ldt_path: str | Path, *, c0_azimut_grad: float | None = None
) -> Callable[..., float]:
    """Baut aus einer Hersteller-LDT das Lichtstärke-Callable für den Lux-Nachweis.

    Der EINE Ort, der `platzierung` (F1) an `normwissen.photometrie` (F2) bindet — der
    Platzierer selbst bleibt normwissen-frei (Owner-Grenze).

    **Korrektur 05.09.2026 — verlorene C-Ebene.** Bis dahin lautete die Rückgabe
    `lambda gamma: photometrie.intensitaet(gamma)`; der zweite Parameter blieb auf
    seinem Default **0°**. Der Lux-Nachweis rechnete damit jeden Rasterpunkt so, als
    läge er in der **C0-Ebene**. Für die Fluchtweg-Default-Leuchte (Corridor-Optik)
    ist C0 die **stärkste** Richtung: bei γ = 60° stehen dort 149,93 cd gegen
    19,53 cd in C90 — ein Punkt mit tatsächlich 0,39 lx wurde als 3,00 lx gerechnet
    und bestand einen 1-lx-Grenzwert, den er nicht erfüllt (Faktor 7,7).

    Das zurückgegebene Callable nimmt **`(γ, C)`** entgegen (C optional, damit
    bestehende Aufrufer nicht brechen) und verhält sich nach Datenlage:

    * **rotationssymmetrische** Verteilung (an den Daten geprüft, nicht am
      Produktnamen) → `I(γ)` wie bisher, C ist folgenlos;
    * **anisotrope** Verteilung **ohne zugesicherte Ausrichtung** → **kleinste**
      Lichtstärke über alle C-Ebenen. Konservativ, nie ein falsch bestandener
      Nachweis — und bewusst **kein** Mittelwert und **kein** fester C-Winkel;
    * **anisotrope** Verteilung **mit** `c0_azimut_grad` → echtes `I(γ, C)`, wobei
      C = Plan-Azimut − Azimut der C0-Ebene.

    `c0_azimut_grad` ist die **physische Ausrichtung der Optik** im Plan. Sie ist
    heute **nirgends zugesichert**: `Platzierung.rotation_deg` ist die
    CAD-**Symbol**-Rotation für den Render und darf dafür nicht ungeprüft
    herhalten. Solange sie fehlt, greift der konservative Zweig; `.hinweis` am
    Callable sagt, was gerechnet wurde.
    """
    from notbeleuchtung.normwissen.photometrie import lade_ldt

    photometrie = lade_ldt(ldt_path)
    rotationssymmetrisch = photometrie.ist_rotationssymmetrisch()

    if rotationssymmetrisch:
        def i_cd(gamma_grad: float, c_grad: float | None = None) -> float:
            return photometrie.intensitaet(gamma_grad)
        i_cd.hinweis = (
            "Photometrie rotationssymmetrisch (an den Daten geprüft) — die "
            "C-Ebene ist folgenlos."
        )
    elif c0_azimut_grad is None:
        def i_cd(gamma_grad: float, c_grad: float | None = None) -> float:
            return photometrie.min_intensitaet(gamma_grad)
        i_cd.hinweis = (
            "Photometrie anisotrop, physische Ausrichtung der Optik NICHT "
            "zugesichert (Platzierung.rotation_deg ist die CAD-Symbol-Rotation, "
            "keine Optik-Ausrichtung) — gerechnet wird die kleinste Lichtstärke "
            "über alle C-Ebenen. Das ist eine konservative Abschätzung, kein "
            "vollständiger Nachweis."
        )
    else:
        def i_cd(gamma_grad: float, c_grad: float | None = None) -> float:
            return photometrie.intensitaet(gamma_grad, (c_grad or 0.0) - c0_azimut_grad)
        i_cd.hinweis = (
            f"Photometrie anisotrop, C0-Azimut {c0_azimut_grad:g}° zugesichert — "
            "gerechnet mit der tatsächlichen C-Ebene je Rasterpunkt."
        )
    i_cd.rotationssymmetrisch = rotationssymmetrisch
    return i_cd


def build_default_bundle(
    ldt_path: str | Path | None = None, *, photometrie_katalog: bool = True
) -> ProviderBundle:
    """Das echte Owner-Trio: ArchitekturRaumProvider (Selman) + En1838NormProvider
    (Enis) + NotlichtPlatzierer (Leonis) + LbTextProvider (Enis, 2. Input). Lazy-Import
    — s. Modul-Docstring.

    Photometrie (Lux-Deckung): `ldt_path` übersteuert; ohne `ldt_path` greift per
    Default der Schrack-Katalog (`CAD_Symbole/photometrie/`, Fluchtweg-Leuchte =
    KB-Corridor-Optik im 3h-Notbetrieb, s. QUELLEN.md) — die reale Verteilung ist
    strenger als die alte isotrope 200-cd-Annahme (Mollgasse EG: 21 → 28 SL).
    `photometrie_katalog=False` erzwingt das alte isotrope Verhalten; fehlt der
    Katalog im Baum (schlankes Deployment), fällt die Engine still darauf zurück.
    """
    from notbeleuchtung.normwissen import (
        En1838NormProvider,
        LbTextProvider,
        OibRl2Provider,
    )
    from notbeleuchtung.platzierung import NotlichtPlatzierer
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    if ldt_path is None and photometrie_katalog:
        from notbeleuchtung.symbols.photometrie_katalog import fluchtweg_default_ldt

        ldt_path = fluchtweg_default_ldt()   # None wenn Katalog nicht im Baum
    i_cd_fn = photometrie_i_cd_fn(ldt_path) if ldt_path is not None else None
    return ProviderBundle(
        raum=ArchitekturRaumProvider(),
        norm=En1838NormProvider(),
        platzierer=NotlichtPlatzierer(i_cd_fn=i_cd_fn),
        lb=LbTextProvider(),
        oib=OibRl2Provider(),
    )
