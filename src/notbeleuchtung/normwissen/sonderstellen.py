"""Sonderstellen — Contract-VORSCHLAG für die hervorzuhebenden Stellen (EN 1838 §4.1.2).

Acht Regeln der Placement-Decision-Matrix sind blockiert, weil das `RaumModell` die
Stellen nicht führt, an denen EN 1838 §4.1.2 eine Betonung verlangt (Feuerlöscher,
Wandhydrant, Erste-Hilfe-Stelle, Meldeeinrichtung) bzw. weil zwei Raum-Eigenschaften
fehlen (§4.3.8 barrierefrei, §4.4.1 besondere Gefährdung).

**Dieses Modul ändert keinen Contract.** `Sonderstelle` ist ein *Prototyp*: er macht
den Vorschlag ausführbar und testbar, bevor über ihn entschieden wird. Nach einem
3-Owner-GO zieht er nach `hauptengine/contracts/raum_modell.py` um — Details in
`docs/SPEC_SONDERSTELLEN_CONTRACT.md`.

Fail closed, wie überall im Normwissen: ein unbekannter Typ und eine fehlende
Position erzeugen **keinen** Default, sondern einen Review-Befund.

**Korrektur 01.09.2026:** §4.1.2 h) und i) nennen sehr wohl einen Lux-Wert —
**5 lx vertikal** am Erste-Hilfe-Kasten bzw. an Brandbekämpfungs- und Melde-
einrichtungen. Die frühere Annahme („§4.1.2 fordert nur die Betonung, die 5 lx
stammen aus der LB") beruhte auf einer unvollständigen Extraktion. Der Wert ist
**vertikal** und darf deshalb nicht als horizontales `min_lux` durchgereicht
werden — dafür trägt die Query-API die Bezugsfläche im Namen. Ohne eigenen Wert
bleibt weiterhin §4.1.2 c) (Niveauänderung).
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field

from .platzierungsregeln import MANUELL_PRUEFEN, Beleg, Leuchtenart, PlatzierungsRegelwerk

DATA_DIR = Path(__file__).parent / "data"
DATEI = "sonderstellen.yaml"

XY = tuple[float, float]

#: Die belegten Typen. Jeder steht hier, weil eine Matrix-Regel ihn braucht —
#: keine hypothetischen Zukunfts-Typen (siehe `beobachtet_ohne_regel` in der YAML).
SonderstellenTyp = Literal[
    "feuerloescher", "hydrant", "erste_hilfe", "brandmelder", "niveauaenderung"
]

Datenquelle = Literal[
    "architektur_dxf_heute", "architektur_dxf_kuenftig",
    "elektro_lb_ohne_position", "elektroplan_kuenftig", "manuell",
]


class Sonderstelle(BaseModel):
    """VORSCHLAG für `RaumModell.sonderstellen[]` — punktförmige Stelle nach §4.1.2.

    Bewusst minimal: `typ` + `xy_mm` sind alles, was die Placement-Regeln brauchen
    (die 2-m-Regel ist ein Abstand zu einem Punkt). `raum_id` und `quelle` sind
    Audit-Trail, keine Steuergrößen.
    """

    id: str
    typ: SonderstellenTyp
    xy_mm: XY
    raum_id: str | None = None
    #: Woher die Angabe stammt — gehört in den Audit-Trail der Platzierung.
    quelle: str = ""


class SonderstellenBefund(BaseModel):
    """Was eine Eingabe fachlich auslöst — inklusive dessen, was sie NICHT auslöst."""

    aktivierte_regeln: list[str] = Field(default_factory=list)
    review: list[str] = Field(default_factory=list)

    @property
    def blockierend(self) -> bool:
        return bool(self.review)


class SonderstellenAnforderung(BaseModel):
    """Was an EINER Sonderstelle bzw. für EIN Raum-Attribut zu tun ist.

    Bewusst **kein** `NormAnforderung`: dessen `min_lux` ist ein horizontaler
    Bodenwert, und EN 1838 §4.1.2 nennt an diesen Stellen entweder einen
    **vertikalen** Wert (h/i: 5 lx am Gerät) oder gar keinen (c). Ein Pflichtwert
    `min_lux` wäre hier nur zu füllen, indem man eine Zahl erfindet oder eine
    fremde Raumregel ausleiht — genau der Fehler, den dieser Typ abstellt.

    `quelle` ist die **echte** Fundstelle des Auslösers und geht als
    `Platzierung.norm_quelle` in den Audit-Trail.
    """

    ausloeser: str                       # Sonderstellen-Typ oder Raum-Attribut
    klassifikation: Leuchtenart
    quelle: str                          # Audit-Trail-String, ∈ NormRegelwerk.quellen
    norm_ref: str                        # dieselbe Fundstelle mit Seite (Doku)
    beleg: Beleg
    symbol_katalog_keys: list[str] = Field(default_factory=list)
    montagehoehe_mm: int = 2000
    #: §4.1.2 ANMERKUNG 1 — „nicht mehr als 2 m in der Horizontalen". Nur für
    #: punktförmige Stellen; ein Raum-Attribut hat keinen Bezugspunkt → None.
    max_abstand_mm: int | None = None
    #: 5 lx AM GERÄT (§4.1.2 h/i). Nie in den Bodenraster einsetzen.
    lux_vertikal: float | None = None
    lux_vertikal_quelle: str | None = None
    #: Horizontal am Boden — nur, wo die Norm einen solchen Wert nennt (§4.3.1
    #: über §4.3.8). Für §4.1.2 immer None.
    lux_horizontal: float | None = None
    lux_horizontal_quelle: str | None = None
    #: True = es gibt eine lichttechnische Anforderung, die die Engine heute
    #: NICHT nachweist. Die Leuchte ist trotzdem zu setzen (Pflichtstelle) —
    #: der offene Nachweis gehört sichtbar in den Prüfbericht.
    nachweis_offen: bool = False
    nachweis_offen_grund: str = ""


class SonderstellenKatalog:
    """Query-API über `data/sonderstellen.yaml`.

    Beantwortet die Fragen, die vor der Contract-Entscheidung zu klären sind:
    welche Typen gibt es, welche Regel schaltet jeder frei, woher kommen die Daten,
    und wo bleibt ein Lux-Wert unbelegt.
    """

    def __init__(self, data_dir: Path | None = None) -> None:
        self._dir = data_dir or DATA_DIR
        self._cfg = _lade(self._dir)
        self._typen = {t["typ"]: t for t in self._cfg["sonderstellen_typen"]}
        self._attribute = {a["attribut"]: a for a in self._cfg["raum_attribute"]}

    # ── Katalog ─────────────────────────────────────────────────────────────
    def typen(self) -> list[str]:
        return list(self._typen)

    def eintrag(self, typ: str) -> dict:
        if typ not in self._typen:
            raise KeyError(f"Unbekannter Sonderstellen-Typ: {typ!r}")
        return self._typen[typ]

    def raum_attribute(self) -> dict[str, dict]:
        return dict(self._attribute)

    def leuchtenart(self, typ: str) -> Leuchtenart:
        return self.eintrag(typ)["leuchtenart"]

    def max_abstand_mm(self, typ: str) -> int:
        return int(self.eintrag(typ)["max_horizontal_zum_punkt_mm"])

    def beleg(self, typ: str) -> Beleg:
        return self.eintrag(typ)["beleg"]

    # ── Lux ─────────────────────────────────────────────────────────────────
    def norm_lux_vertikal(self, typ: str) -> float | None:
        """Normativer Lux-Wert der Stelle — **vertikal am Gerät**, nicht am Boden.

        §4.1.2 h) und i) nennen 5 lx vertikale Beleuchtungsstärke am
        Erste-Hilfe-Kasten bzw. an Brandbekämpfungs- und Meldeeinrichtungen. Für
        Stellen ohne eigenen Wert (§4.1.2 c) Niveauänderung) ist das Ergebnis
        `None` — dort gilt nur die Betonungspflicht.

        Der Methodenname trägt die Bezugsfläche bewusst mit: der Lux-Nachweis der
        Engine (`lux_raster`) rechnet **horizontal am Boden**. Ein vertikaler
        Norm-Wert darf dort nicht als `min_lux` eingesetzt werden — das wäre
        derselbe Kategorienfehler wie Ud gegen Uo.
        """
        return self.eintrag(typ)["lux_anforderung"]["norm_wert"]

    def norm_lux_bezugsflaeche(self, typ: str) -> str | None:
        """Auf welche Fläche sich `norm_lux_vertikal` bezieht (`"vertikal"`).

        `None`, wenn es keinen Norm-Wert gibt — dann gibt es auch keine Fläche.
        """
        return self.eintrag(typ)["lux_anforderung"].get("norm_bezugsflaeche")

    def norm_lux_horizontal(self, typ: str) -> float | None:
        """Horizontaler Norm-Lux-Wert — für **keinen** Typ belegt.

        EN 1838 §4.1.2 macht ausschließlich vertikale Vorgaben an diesen Stellen.
        Wer einen Bodenwert braucht, bekommt hier bewusst `None` statt einer
        stillen Umdeutung des Vertikalwerts.
        """
        return None

    def lb_lux(self, typ: str) -> float | None:
        """Projekttypischer Lux-Wert aus einer realen LB.

        Bei Feuerlöscher/Hydrant wiederholt die LB den Normwert aus §4.1.2 i) —
        sie begründet ihn nicht. Weicht eine LB ab, übersteuert sie (CLAUDE.md).
        """
        return self.eintrag(typ)["lux_anforderung"]["lb_typisch"]

    def lux_ist_ungeklaert(self, typ: str) -> bool:
        """Fehlt der Norm-Lux-Wert für diese Stelle? (Heute nur Niveauänderung.)"""
        return self.eintrag(typ)["lux_anforderung"]["norm_status"] == MANUELL_PRUEFEN

    # ── Norm-Anforderung (Roh-Fakten; der Provider setzt sie zusammen) ──────
    def norm_anforderung_roh(self, ausloeser: str) -> list[dict]:
        """Die Anforderungs-Blöcke eines Typs bzw. Raum-Attributs, in Reihenfolge.

        Ein Typ kann mehr als eine Leuchte auslösen: `niveauaenderung` trägt nach
        §4.1.2 c) sowohl eine Sicherheitsleuchte (SL-04) als auch ein
        Rettungszeichen (RZ-06) — beide mit derselben Fundstelle.
        """
        cfg = self._cfg["norm_anforderung"]
        block = cfg["typen"].get(ausloeser) or cfg["raum_attribute"].get(ausloeser)
        if block is None:
            raise KeyError(f"Kein Auslöser mit Norm-Anforderung: {ausloeser!r}")
        blocks = [block]
        if block.get("zusaetzlich"):
            blocks.append(block["zusaetzlich"])
        return blocks

    def ist_raum_attribut(self, ausloeser: str) -> bool:
        return ausloeser in self._cfg["norm_anforderung"]["raum_attribute"]

    def norm_ref(self, ausloeser: str) -> str:
        """Fundstelle mit Seitenangabe — für Doku und Prüfbericht."""
        eintrag = (self._typen.get(ausloeser) or self._attribute.get(ausloeser))
        if eintrag is None:
            raise KeyError(f"Unbekannter Auslöser: {ausloeser!r}")
        return eintrag["norm_ref"]

    def beleg_von(self, ausloeser: str) -> Beleg:
        eintrag = (self._typen.get(ausloeser) or self._attribute.get(ausloeser))
        if eintrag is None:
            raise KeyError(f"Unbekannter Auslöser: {ausloeser!r}")
        # Raum-Attribute führen `beleg` ebenso wie die Typen.
        return eintrag["beleg"]

    def quellen(self) -> list[str]:
        """Alle Fundstellen-Strings, die dieser Katalog je vergibt.

        Der `En1838NormProvider` nimmt sie in `NormRegelwerk.quellen` auf — sonst
        verletzt jede Sonderstellen-Platzierung die Naht-Invariante
        `Platzierung.norm_quelle ∈ NormRegelwerk.quellen`.
        """
        cfg = self._cfg["norm_anforderung"]
        raus: set[str] = set()
        for block in (*cfg["typen"].values(), *cfg["raum_attribute"].values()):
            raus.add(block["quelle"])
            if block.get("zusaetzlich"):
                raus.add(block["zusaetzlich"]["quelle"])
        return sorted(raus)

    # ── Datenquellen ────────────────────────────────────────────────────────
    def datenquellen(self, typ: str) -> list[str]:
        return list(self.eintrag(typ)["datenquellen"])

    def heute_erkennbar(self, quelle: str) -> bool:
        """Gibt es für diese Quelle einen erprobten Parser? (Meist: nein.)"""
        return bool(self._cfg["datenquellen"][quelle]["erkannt_heute"])

    def typ_ist_heute_automatisch_erkennbar(self, typ: str) -> bool:
        """Nur wahr, wenn eine Quelle die STELLE samt Position liefern kann.

        `elektro_lb_ohne_position` zählt bewusst nicht: die LB kennt den Lux-Wert,
        aber keine Koordinate — sie kann eine Sonderstelle nicht erzeugen.
        """
        return any(self.heute_erkennbar(q) and q != "manuell"
                   and "ohne_position" not in q
                   for q in self.datenquellen(typ))

    # ── Wirkung ─────────────────────────────────────────────────────────────
    def wuerde_freischalten(self) -> set[str]:
        """Alle Regel-IDs, die der Vorschlag insgesamt freischaltet."""
        aus_typen = {r for t in self._typen.values() for r in t["aktiviert_regeln"]}
        aus_attributen = {r for a in self._attribute.values() for r in a["aktiviert_regeln"]}
        return aus_typen | aus_attributen

    def bewerte(self, stellen: list[Sonderstelle | dict]) -> SonderstellenBefund:
        """Was löst diese Eingabe aus — und was ist daran unklar?

        Fail closed: ein unbekannter Typ oder eine fehlende Position werden nicht
        stillschweigend verworfen, sondern als Review-Befund geführt. Eine
        verworfene Sonderstelle ist eine verlorene Pflichtstelle.
        """
        befund = SonderstellenBefund()
        for roh in stellen:
            daten = roh if isinstance(roh, dict) else roh.model_dump()
            kennung = daten.get("id") or "<ohne id>"
            typ = daten.get("typ")
            if typ not in self._typen:
                befund.review.append(
                    f"{kennung}: unbekannter Sonderstellen-Typ {typ!r} — keine Regel "
                    "zugeordnet, Stelle darf nicht still verworfen werden")
                continue
            if not daten.get("xy_mm"):
                befund.review.append(
                    f"{kennung}: Sonderstelle vom Typ {typ!r} ohne Position — die "
                    "2-m-Regel aus §4.1.2 ist ohne Koordinate nicht prüfbar")
                continue
            befund.aktivierte_regeln.extend(self._typen[typ]["aktiviert_regeln"])
            if self.lux_ist_ungeklaert(typ):
                befund.review.append(
                    f"{kennung}: Lux-Niveau für {typ!r} ist normativ unbelegt "
                    f"({MANUELL_PRUEFEN}) — Hervorhebungspflicht gilt trotzdem")
        return befund


@lru_cache(maxsize=4)
def _lade(data_dir: Path) -> dict:
    with open(data_dir / DATEI, encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    _pruefe_regel_ids(cfg)
    return cfg


def _pruefe_regel_ids(cfg: dict) -> None:
    """Jede genannte Regel-ID muss in der Decision-Matrix existieren.

    Ohne diese Prüfung könnte der Katalog Regeln „freischalten", die es nicht gibt —
    der Vorschlag wäre dann nicht überprüfbar.
    """
    matrix = PlatzierungsRegelwerk()
    for eintrag in (*cfg["sonderstellen_typen"], *cfg["raum_attribute"]):
        for rid in eintrag["aktiviert_regeln"]:
            matrix.regel(rid)      # wirft KeyError bei Tippfehler
