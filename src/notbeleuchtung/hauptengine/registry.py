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

from .photometrie_befund import (
    KONSERVATIV_SATZ,
    BundleMitPhotometrie,
    PhotometrieBefund,
)


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
            # `c_grad is None` heißt: der Aufrufer kennt die Richtung NICHT
            # (z.B. `max_leuchtenabstand_mm`, das über eine abstrakte Reihe
            # rechnet). Dann wird auch hier konservativ gerechnet — ein Default
            # von 0° wäre wieder die C0-Annahme, also genau der behobene Fehler.
            if c_grad is None:
                return photometrie.min_intensitaet(gamma_grad)
            return photometrie.intensitaet(gamma_grad, c_grad - c0_azimut_grad)
        i_cd.hinweis = (
            f"Photometrie anisotrop, C0-Azimut {c0_azimut_grad:g}° zugesichert — "
            "gerechnet mit der tatsächlichen C-Ebene je Rasterpunkt; wo ein "
            "Aufrufer keine Richtung kennt, konservativ das Minimum über C."
        )
    i_cd.rotationssymmetrisch = rotationssymmetrisch
    return i_cd


def photometrie_je_key() -> dict[str, Callable[..., float]]:
    """`catalog_key → Lichtstärke-Callable` aus dem Photometrie-Katalog.

    Jede Leuchtenfamilie rechnet ihren Lux-Nachweis mit IHRER LDT (Antipanik =
    Rundlinse, nicht die Corridor-Optik des Fluchtweg-Defaults). Callables ohne
    Ausrichtungs-Zusicherung: rotationssymmetrische Verteilungen sind exakt,
    anisotrope konservativ (Minimum über C) — nie eine Überschätzung. Gleiche
    LDT-Datei → dasselbe Callable (dedupe). Fehlender Katalog → leeres Dict.
    """
    from notbeleuchtung.symbols.photometrie_katalog import katalog_zuordnung

    je_pfad: dict[str, Callable[..., float]] = {}
    out: dict[str, Callable[..., float]] = {}
    for key, pfad in katalog_zuordnung().items():
        p = str(pfad.resolve())
        if p not in je_pfad:
            je_pfad[p] = photometrie_i_cd_fn(pfad)
        out[key] = je_pfad[p]
    return out


def default_photometrie(
    ldt_path: str | Path | None = None,
    *,
    photometrie_katalog: bool = True,
    c0_azimut_grad: float | None = None,
    optik_aus_achse: bool = False,
) -> tuple[Callable[..., float] | None, PhotometrieBefund]:
    """Lichtstärke-Callable **und** der dazugehörige Befund — immer im Paar.

    Die einzige Stelle, die entscheidet, womit der Lux-Nachweis rechnet. Sie
    liefert die Aussage über die Rechengrundlage gleich mit, damit ein
    Rückfall auf die isotrope 200-cd-Annahme (fehlender/nicht auflösbarer
    Katalog) nicht als Hersteller-Nachweis durchgehen kann.

    **`optik_aus_achse` (Ausrichtungs-Naht zum Platzierer):** der Fluchtweg-
    Verdichter (`platzierung/deckung.py`) leitet je Sicherheitsleuchte den
    Korridor-Achsen-Azimut ab (`leuchten_auf_linie_mit_richtung`), rechnet den
    Lux-Nachweis mit der C-Ebene RELATIV zu dieser Optik-Ausrichtung und
    schreibt denselben Azimut als Montage-Rotation an die Platzierung — der
    Plan selbst IST damit die Ausrichtungs-Zusicherung. Das Callable wird auf
    `I(γ, C-relativ)` gestellt (identisch zu `c0_azimut_grad=0.0`); Aufrufer
    ohne Azimut fragen `C=None` und bekommen weiterhin konservativ das Minimum
    über alle C-Ebenen. Nicht mit `c0_azimut_grad` kombinieren.
    """
    if optik_aus_achse and c0_azimut_grad is not None:
        raise ValueError("optik_aus_achse und c0_azimut_grad schließen sich aus")
    if ldt_path is None and photometrie_katalog:
        from notbeleuchtung.symbols.photometrie_katalog import fluchtweg_default_ldt

        ldt_path = fluchtweg_default_ldt()   # None wenn Katalog nicht auflösbar
    if ldt_path is None:
        grund = (
            "Photometrie-Katalog abgeschaltet (photometrie_katalog=False)"
            if not photometrie_katalog
            else "Photometrie-Katalog nicht auflösbar (CAD_Symbole/photometrie fehlt "
                 "oder der Fluchtweg-Default ist nicht im Mapping)"
        )
        return None, PhotometrieBefund(
            quelle="isotrope_annahme",
            hinweis=(
                f"{grund} — gerechnet mit der isotropen Annahme 200 cd. "
                "Das ist KEIN Hersteller-Nachweis; vollständiger Nachweis offen."
            ),
            vollstaendiger_nachweis=False,
            rotationssymmetrisch=None,
            einschraenkungen=("keine Hersteller-Photometrie", "isotrope Annahme 200 cd"),
        )
    effektiv_c0 = 0.0 if optik_aus_achse else c0_azimut_grad
    i_cd_fn = photometrie_i_cd_fn(ldt_path, c0_azimut_grad=effektiv_c0)
    rotsym = bool(i_cd_fn.rotationssymmetrisch)
    ausgerichtet = effektiv_c0 is not None
    vollstaendig = rotsym or ausgerichtet
    hinweis = i_cd_fn.hinweis if vollstaendig else KONSERVATIV_SATZ
    if optik_aus_achse and not rotsym:
        hinweis = (
            "Photometrie anisotrop; Optik-Ausrichtung je Fluchtweg-Leuchte aus "
            "der Korridor-Achse abgeleitet und als Montage-Rotation am Symbol "
            "vermerkt — der Lux-Nachweis rechnet die tatsächliche C-Ebene. "
            "Leuchten ohne Achsen-Azimut werden konservativ mit dem Minimum "
            "über alle C-Ebenen gerechnet."
        )
    return i_cd_fn, PhotometrieBefund(
        quelle="hersteller_ldt",
        hinweis=hinweis,
        vollstaendiger_nachweis=vollstaendig,
        rotationssymmetrisch=rotsym,
        ausrichtung_zugesichert=ausgerichtet,
        ldt_name=Path(ldt_path).name,
        einschraenkungen=() if vollstaendig else (
            "anisotrope Lichtverteilung",
            "physische Optik-Ausrichtung nicht zugesichert",
            "gerechnet mit dem Minimum über alle C-Ebenen",
        ),
    )


def build_default_bundle(
    ldt_path: str | Path | None = None,
    *,
    photometrie_katalog: bool = True,
    c0_azimut_grad: float | None = None,
    optik_aus_achse: bool = True,
) -> BundleMitPhotometrie:
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

    # Default-Bundle nutzt IMMER den NotlichtPlatzierer — der liefert die Achsen-
    # Azimute je Fluchtweg-SL (Selbst-Konsistenz der optik_aus_achse-Naht). Ein
    # explizites c0_azimut_grad (globale Ausrichtung) übersteuert den Modus.
    if c0_azimut_grad is not None:
        optik_aus_achse = False
    i_cd_fn, befund = default_photometrie(
        ldt_path, photometrie_katalog=photometrie_katalog,
        c0_azimut_grad=c0_azimut_grad, optik_aus_achse=optik_aus_achse,
    )
    return BundleMitPhotometrie(
        raum=ArchitekturRaumProvider(),
        norm=En1838NormProvider(),
        platzierer=NotlichtPlatzierer(
            i_cd_fn=i_cd_fn, i_cd_fn_je_key=photometrie_je_key() or None
        ),
        lb=LbTextProvider(),
        oib=OibRl2Provider(),
        photometrie=befund,
    )
