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
    def norm_lux(self, typ: str) -> float | None:
        """Normativer Lux-Wert der Stelle — heute für **keinen** Typ belegt.

        §4.1.2 fordert die Hervorhebung, nennt aber kein Beleuchtungsniveau. Die
        5 lx an Feuerlöscher/Hydrant stammen aus einer Projekt-LB und dürfen nicht
        als Normwert ausgegeben werden.
        """
        return self.eintrag(typ)["lux_anforderung"]["norm_wert"]

    def lb_lux(self, typ: str) -> float | None:
        """Projekttypischer Lux-Wert aus einer realen LB — **kein** Norm-Default."""
        return self.eintrag(typ)["lux_anforderung"]["lb_typisch"]

    def lux_ist_ungeklaert(self, typ: str) -> bool:
        return self.eintrag(typ)["lux_anforderung"]["norm_status"] == MANUELL_PRUEFEN

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
