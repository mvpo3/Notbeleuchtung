"""Placement-Decision-Matrix — Query-API über `data/platzierung_regeln.yaml`.

WANN welche Notleuchte WO hin muss. Ergänzt `En1838NormProvider` (der sagt, WELCHE
Anforderung ein Raumtyp hat) um die Situations-Sicht: welcher **Auslöser** erzeugt
welche Platzierung, mit welcher Priorität, welchem Konfliktverhalten und welcher
Entscheidungs-Quelle.

Leonis fragt hier — er liest die YAML nicht (CLAUDE.md: „Leonis parst kein YAML").
Alle Fachwerte stehen in der YAML, dieses Modul enthält nur die Mechanik.

**Contract-Status:** `PlatzierungsRegel` ist ein **Contract-Kandidat** und liegt
bewusst noch in `normwissen/`. Der Weg in `hauptengine/contracts/` ist ein
3-Owner-Slice (siehe `docs/PLACEMENT_DECISION_MATRIX.md`, Abschnitt „Übergabe").
Bis dahin konsumiert Track A die Regeln über diese API, nicht über einen Import
des Modells.

Entscheidungs-Hierarchie (CLAUDE.md, BINDEND)::

    LB-explizit → Referenz-Praxis → EN-1838/ÖNorm-Default → Hard Stops

`hard_stop` ist die einzige Stufe, die auch LB-explizit schlägt.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field

DATA_DIR = Path(__file__).parent / "data"
DATEI = "platzierung_regeln.yaml"

Leuchtenart = Literal["rz", "sicherheitsleuchte", "antipanik", "keine"]
DecisionSource = Literal["norm_default", "referenz_praxis", "lb_explizit", "hard_stop"]
EngineStatus = Literal["unterstuetzt", "teilweise", "input_fehlt"]
Beleg = Literal["BELEGT", "AUSLEGUNG", "PRAXIS", "LB"]

#: Kein Norm-Wert vorhanden → die Regel liefert bewusst keinen stillen Default.
MANUELL_PRUEFEN = "MANUELL_PRUEFEN"


class PlatzierungsRegel(BaseModel):
    """Eine Zeile der Decision-Matrix. Contract-Kandidat (s. Modul-Docstring)."""

    id: str
    ausloeser: str
    kontext: str
    leuchtenart: Leuchtenart
    positionierungsziel: str
    orientierung: str
    abstand: dict = Field(default_factory=dict)
    prioritaet: int
    ausnahmen: list[str] = Field(default_factory=list)
    konfliktregel: str
    quelle: str
    norm_ref: str
    beleg: Beleg
    review_erforderlich: bool
    decision_source: DecisionSource
    engine_input: list[str] = Field(default_factory=list)
    engine_status: EngineStatus

    @property
    def erzeugt_leuchte(self) -> bool:
        """Regeln mit `leuchtenart == "keine"` sind Abgrenzungs- und Review-Regeln:
        sie verhindern eine Platzierung, statt eine zu erzeugen."""
        return self.leuchtenart != "keine"


class HardStop(BaseModel):
    """Unübersteuerbare Norm-Grenze. Schlägt auch eine explizite LB-Vorgabe."""

    id: str
    regel: str
    quelle: str
    norm_ref: str
    beleg: Beleg
    verletzung: str
    wert_ref: str | None = None
    aufloesung: str | None = None
    hinweis: str | None = None


class PlatzierungsRegelwerk:
    """Query-API über die Decision-Matrix.

    Konstruktion ist billig (YAML wird je `data_dir` einmal gelesen und gecacht),
    damit der Aufrufer sie nicht durchreichen muss.
    """

    def __init__(self, data_dir: Path | None = None) -> None:
        self._dir = data_dir or DATA_DIR
        self._cfg = _lade(self._dir)
        self._regeln = [
            PlatzierungsRegel.model_validate(r)
            for abschnitt in ("rettungszeichen", "sicherheitsleuchten")
            for r in self._cfg.get(abschnitt, [])
        ]
        self._hard_stops = [HardStop.model_validate(h) for h in self._cfg.get("hard_stops", [])]

    # ── Abfragen ────────────────────────────────────────────────────────────
    def alle(self) -> list[PlatzierungsRegel]:
        """Alle Regeln, aufsteigend nach `prioritaet` (0 = schlägt alles)."""
        return sorted(self._regeln, key=lambda r: (r.prioritaet, r.id))

    def regel(self, regel_id: str) -> PlatzierungsRegel:
        for r in self._regeln:
            if r.id == regel_id:
                return r
        raise KeyError(f"Unbekannte Regel-ID: {regel_id!r}")

    def fuer_leuchtenart(self, art: Leuchtenart) -> list[PlatzierungsRegel]:
        return [r for r in self.alle() if r.leuchtenart == art]

    def umsetzbar(self) -> list[PlatzierungsRegel]:
        """Regeln, die das heutige `RaumModell` trägt — Track-A-Arbeitsvorrat."""
        return [r for r in self.alle() if r.engine_status != "input_fehlt"]

    def blockiert_durch_contract(self) -> list[PlatzierungsRegel]:
        """Regeln, die an einem fehlenden `RaumModell`-Merkmal hängen.

        Das ist keine Lücke im Normwissen, sondern eine Contract-Frage (Contract 1,
        3-Owner). Solange sie offen ist, KANN die Engine diese Stellen nicht
        bestücken — sie darf das nicht durch eine Heuristik ersetzen.
        """
        return [r for r in self.alle() if r.engine_status == "input_fehlt"]

    def review_faelle(self) -> list[PlatzierungsRegel]:
        """Regeln, die eine Entscheidung NICHT still treffen dürfen."""
        return [r for r in self.alle() if r.review_erforderlich]

    def hard_stops(self) -> list[HardStop]:
        return list(self._hard_stops)

    # ── Hierarchie ──────────────────────────────────────────────────────────
    def rang(self, quelle: DecisionSource) -> int:
        """Vorrang-Rang einer Entscheidungs-Quelle; größer schlägt kleiner."""
        return int(self._cfg["decision_sources"][quelle]["rang"])

    def gewinner(self, a: PlatzierungsRegel, b: PlatzierungsRegel) -> PlatzierungsRegel | None:
        """Welche der beiden Regeln setzt sich durch?

        Entscheidet zuerst die Entscheidungs-Quelle (LB schlägt Norm-Default,
        Hard Stop schlägt alles), bei Gleichstand die Priorität. Bleibt es
        gleichauf, gibt es **keinen** Gewinner: `None` heißt Review, nicht
        „irgendeine nehmen".
        """
        ra, rb = self.rang(a.decision_source), self.rang(b.decision_source)
        if ra != rb:
            return a if ra > rb else b
        if a.prioritaet != b.prioritaet:
            return a if a.prioritaet < b.prioritaet else b
        return None


@lru_cache(maxsize=4)
def _lade(data_dir: Path) -> dict:
    with open(data_dir / DATEI, encoding="utf-8") as fh:
        return yaml.safe_load(fh)
