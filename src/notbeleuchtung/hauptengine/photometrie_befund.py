"""photometrie_befund — womit der Lux-Nachweis gerechnet wurde, typisiert bis zur Ausgabe.

Der Lux-Nachweis (`platzierung/lux.py`) bekommt von der Registry ein
Lichtstärke-Callable. Was hinter diesem Callable steckt — echte Hersteller-LDT
oder die isotrope 200-cd-Annahme, richtungsrichtig oder konservativ genähert —
entscheidet, **wie belastbar** ein bestandener Grenzwert ist. Diese Information
darf nicht im Callable stecken bleiben: sie gehört in den Prüfbericht und in die
Ausgabe.

Deshalb dieses kleine Integrations-Objekt:

* es ist **typisiert** (kein Dict, kein `getattr` auf fremde Attribute),
* es reist **mit dem Bundle** (`BundleMitPhotometrie`), das die Registry gebaut
  hat — Befund und tatsächlich verdrahtetes Callable können nicht auseinander-
  laufen,
* es berührt **keinen Contract**: `hauptengine/contracts/**` bleibt unverändert,
  `BundleMitPhotometrie` ist eine reine Erweiterung des bestehenden
  `ProviderBundle` (jeder Konsument des Contracts funktioniert weiter).

Fehlt der Befund (Fake-Bundle, fremd verdrahtete Provider), wird **nichts
behauptet** — die Regel im Prüfbericht entfällt, statt einen Nachweis zu
unterstellen.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from .contracts import ProviderBundle

#: Wortlaut für den einen Fall, der einen bestandenen Grenzwert relativiert.
KONSERVATIV_SATZ = (
    "Konservative Photometrie-Abschätzung bei unbekannter Optik-Ausrichtung; "
    "vollständiger Nachweis offen."
)

Quelle = Literal["hersteller_ldt", "isotrope_annahme"]


@dataclass(frozen=True)
class PhotometrieBefund:
    """Grundlage des Lux-Nachweises — eine Aussage, die der Plan mitführt.

    `vollstaendiger_nachweis` ist **kein** Urteil über die Lux-Werte selbst,
    sondern darüber, ob die Rechengrundlage einen vollständigen lichttechnischen
    Nachweis überhaupt trägt. Ein bestandener Grenzwert hebt eine offene
    Grundlage nicht auf.
    """

    quelle: Quelle
    hinweis: str
    vollstaendiger_nachweis: bool
    rotationssymmetrisch: bool | None = None      # None = keine Verteilung geladen
    ausrichtung_zugesichert: bool = False
    ldt_name: str = ""
    einschraenkungen: tuple[str, ...] = field(default_factory=tuple)

    @property
    def status(self) -> str:
        """Prüfbericht-Status: offene Grundlage = Warnung, nie stilles 'ok'."""
        return "ok" if self.vollstaendiger_nachweis else "warnung"

    def als_zeile(self) -> str:
        """Eine Zeile für Ausgabe-Kanäle ohne Struktur (DXF-Zeichnungseigenschaft)."""
        quelle = "Hersteller-LDT" if self.quelle == "hersteller_ldt" else "isotrope Annahme"
        name = f" ({self.ldt_name})" if self.ldt_name else ""
        return f"{quelle}{name}: {self.hinweis}"


@dataclass
class BundleMitPhotometrie(ProviderBundle):
    """`ProviderBundle` + der Befund zu dem Callable, das darin verdrahtet ist.

    Erweiterung, keine Contract-Änderung: alle Contract-Felder bleiben, jeder
    bestehende Konsument arbeitet unverändert weiter.
    """

    photometrie: PhotometrieBefund | None = None


def photometrie_des_bundles(bundle: ProviderBundle) -> PhotometrieBefund | None:
    """Befund eines Bundles — typisiert, ohne `getattr` und ohne Privat-Attribute.

    Ein gewöhnliches `ProviderBundle` (Fakes, fremde Verdrahtung) trägt keinen
    Befund; dann bleibt die Aussage aus.
    """
    if isinstance(bundle, BundleMitPhotometrie):
        return bundle.photometrie
    return None
