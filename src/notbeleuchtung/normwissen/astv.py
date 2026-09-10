"""astv — Arbeitsstätten-Pfad: AStV § 9 (Ebene A) und OVE-Fachinformation E08 (D).

Beantwortet **eine** Frage: *welche Prüfpunkte des Arbeitsstätten-Pfades sind für
diesen Gebäudeteil offen, und welche Projektangabe braucht jeder von ihnen?*

Sie beantwortet ausdrücklich **nicht**, ob eine Sicherheitsbeleuchtung nach AStV
erforderlich **ist**. Alle drei Tatbestände des § 9 Abs. 1 hängen an Angaben, die
diese Engine nicht hat — eine Belichtungsangabe (Z 1), eine Beurteilung (Z 2) und
eine Gefahrenbeurteilung (Z 3). Fehlt die Angabe, bleibt der Punkt `ungeprueft`:
nie still erfüllt, nie still „nicht erforderlich".

**Es aktiviert nichts.** Kein Contract-Wert, keine Schwelle, keine Platzierung,
keine OIB-Stufe. Die Prüfpunkte begründen ausschließlich **Hinweise** im
Prüfbericht bzw. in der Plan-Ausgabe.

**Ebenen bleiben getrennt** (`docs/NORMQUELLEN_AT.md`): AStV und ASchG sind
amtliche Rechtsquellen (**A**), EN 1838 ist Norm (**C**), die OVE-Fachinformation
E08 ist **Auslegungshilfe (D) und ersetzt keine Norm**. Eine E08-Angabe belegt
daher keine Rechtspflicht; umgekehrt nennt § 9 weder Beleuchtungsart noch
Lux-Wert.

Quellen und Wortlaute: `data/astv_arbeitsstaetten.yaml`; fachliche Herleitung:
`docs/proposals/ASTV_E08_ENTSCHEIDUNGSREGELN.md`.
"""
from __future__ import annotations

from functools import cached_property
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

DATA_DIR = Path(__file__).parent / "data"
DATEI = "astv_arbeitsstaetten.yaml"

#: Status eines Prüfpunkts, solange die tragende Projektangabe fehlt.
UNGEPRUEFT = "ungeprueft"


class AstvPruefpunkt(BaseModel):
    """Ein offener Prüfpunkt des Arbeitsstätten-Pfades.

    `erfuellt` gibt es hier bewusst nicht: das Modul stellt die **Frage** und
    benennt die fehlende Angabe. Die Antwort gibt das Projekt (bzw. die LB).
    """

    kennung: str
    ebene: str                       # "A" Rechtsquelle · "C" Norm · "D" Fachinformation
    fundstelle: str
    wortlaut: str
    gilt_fuer: list[str] = Field(default_factory=list)
    folge_wenn_erfuellt: str = ""
    benoetigte_angabe: list[str] = Field(default_factory=list)
    status: str = UNGEPRUEFT
    hinweis: str = ""
    #: Wogegen der Punkt ausdrücklich NICHT abgegrenzt werden darf.
    abgrenzung: str = ""


class AstvWahlrecht(BaseModel):
    """§ 9 Abs. 4 — nachleuchtende Orientierungshilfen statt Sicherheitsbeleuchtung.

    Ein **Wahlrecht**, keine Regel: die Engine darf es weder ausüben noch
    unterstellen. Sie weist es aus, damit es nicht unbemerkt bleibt.
    """

    fundstelle: str
    wortlaut: str
    entscheider: str
    bedingungen: list[str] = Field(default_factory=list)
    reichweite: str = ""
    benoetigte_angabe: list[str] = Field(default_factory=list)
    status: str = UNGEPRUEFT
    hinweis: str = ""


class E08Angabe(BaseModel):
    """Eine Ausführungsangabe der OVE-Fachinformation E08 — **Ebene D**."""

    kennung: str
    fundstelle: str
    art: str
    gegenstand: str = ""
    angaben: list[str] = Field(default_factory=list)
    #: Was die Engine davon heute trägt und was nicht.
    deckung_mit_engine: dict[str, str] = Field(default_factory=dict)
    status: str = ""
    grenze: str = ""

    @property
    def ist_rechtspflicht(self) -> bool:
        """Immer `False` — E08 ist Auslegungshilfe, keine Rechtsquelle."""
        return False


class Betriebspflicht(BaseModel):
    """Betriebs-/Wartungsanforderung — außerhalb der Plangenerierung."""

    fundstelle: str
    ebene: str
    angabe: str
    funktionsbereich: str


class ArbeitsstaettenWissen:
    """Query-API über `data/astv_arbeitsstaetten.yaml`.

    Der Ladevorgang ist **lazy** (`cached_property`): wer das Modul nur
    importiert, bekommt keine neue Dateiabhängigkeit und keinen neuen Fehlerfall.
    """

    def __init__(self, data_dir: Path | None = None) -> None:
        self._dir = data_dir or DATA_DIR

    @cached_property
    def _doc(self) -> dict:
        with open(self._dir / DATEI, encoding="utf-8") as fh:
            return yaml.safe_load(fh)

    # ── Rechtsquelle (Ebene A) ────────────────────────────────────────────
    def pruefpunkte(self, arbeitsstaette_nach_aschg: bool | None) -> list[AstvPruefpunkt]:
        """Die offenen § 9-Prüfpunkte für einen Gebäudeteil.

        * `True` / `None` → alle drei Tatbestände des Abs. 1. Bei `None` ist
          zusätzlich der Arbeitsstätten-Status selbst offen; das sagt
          `reichweite_vorbehalt()`.
        * `False` → **leere Liste**. ⚠️ Das ist **kein** „nichts erforderlich":
          § 1 Abs. 2 kann Gebäudeteile **außerhalb** einer anderen Arbeitsstätte
          erfassen. Der Vorbehalt bleibt über `reichweite_vorbehalt()` sichtbar.
        """
        if arbeitsstaette_nach_aschg is False:
            return []
        return [
            AstvPruefpunkt(
                kennung=e["kennung"],
                ebene=e["ebene"],
                fundstelle=e["fundstelle"],
                wortlaut=" ".join(e["wortlaut"].split()),
                gilt_fuer=list(e.get("gilt_fuer", [])),
                folge_wenn_erfuellt=e.get("folge_wenn_erfuellt", ""),
                benoetigte_angabe=list(e.get("benoetigte_angabe", [])),
                status=e.get("status", UNGEPRUEFT),
                hinweis=" ".join(e.get("hinweis_ausgabe", "").split()),
                abgrenzung=" ".join(e.get("abgrenzung", "").split()),
            )
            for e in self._doc["tatbestaende"]
        ]

    def wahlrecht(self) -> AstvWahlrecht:
        """§ 9 Abs. 4 — die zulässige Ausführungswahl, unentschieden ausgewiesen."""
        w = self._doc["wahlrecht_abs4"]
        return AstvWahlrecht(
            fundstelle=w["fundstelle"],
            wortlaut=" ".join(w["wortlaut"].split()),
            entscheider=w["entscheider"],
            bedingungen=list(w.get("bedingungen", [])),
            reichweite=" ".join(w.get("reichweite", "").split()),
            benoetigte_angabe=list(w.get("benoetigte_angabe", [])),
            status=w.get("status", UNGEPRUEFT),
            hinweis=" ".join(w.get("hinweis_ausgabe", "").split()),
        )

    def reichweite_vorbehalt(self, arbeitsstaette_nach_aschg: bool | None) -> list[str]:
        """Was zur Reichweite (§ 1) offen bleibt — je nach Angabe.

        ⚠️ `False` erzeugt hier **mehr** Text, nicht weniger: gerade dann greift
        der Vorbehalt aus § 1 Abs. 2/3.
        """
        r = self._doc["reichweite"]
        aus = [" ".join(t.split()) for t in r["klarstellungen"]]
        if arbeitsstaette_nach_aschg is None:
            aus.insert(0, (
                "Der Arbeitsstätten-Status dieses Gebäudeteils ist nicht erhoben "
                "(`arbeitsstaette_nach_aschg` = None) — ob die AStV überhaupt "
                "greift, ist damit offen."
            ))
        if arbeitsstaette_nach_aschg is False:
            aus.insert(0, (
                "Dieser Gebäudeteil ist als 'keine Arbeitsstätte nach ASchG' "
                "angegeben. ⚠️ Daraus folgt nicht, dass die AStV ohne Bedeutung "
                "ist: nach § 1 Abs. 2 müssen auch die außerhalb einer "
                "Arbeitsstätte gelegenen, von Arbeitnehmer/innen benutzten "
                "Gebäudeteile dem 1. und 2. Abschnitt entsprechen; § 1 Abs. 3 "
                "nimmt davon nur unter vier kumulativen Bedingungen aus."
            ))
        return aus

    # ── Fachinformation (Ebene D) ─────────────────────────────────────────
    def ausfuehrung_e08(self) -> list[E08Angabe]:
        """Die E08-Ausführungsangaben — **Auslegungshilfe, keine Rechtspflicht**."""
        return [
            E08Angabe(
                kennung=e["kennung"],
                fundstelle=e["fundstelle"],
                art=e["art"],
                gegenstand=e.get("gegenstand", ""),
                angaben=list(e.get("angaben", [])),
                deckung_mit_engine=dict(e.get("deckung_mit_engine", {})),
                status=e.get("status", ""),
                grenze=" ".join(e.get("grenze", "").split()),
            )
            for e in self._doc["ausfuehrung_e08"]
        ]

    def betriebspflichten(self) -> list[Betriebspflicht]:
        """Betrieb/Instandhaltung — kein Planungsgegenstand, kein Symbol im Plan."""
        block = self._doc["betrieb_wartung"]
        return [
            Betriebspflicht(
                fundstelle=e["fundstelle"],
                ebene=e["ebene"],
                angabe=" ".join(e["angabe"].split()),
                funktionsbereich=block["funktionsbereich"],
            )
            for e in block["eintraege"]
        ]

    # ── Ausgabe ───────────────────────────────────────────────────────────
    def hinweise_fuer_ausgabe(self, arbeitsstaette_nach_aschg: bool | None) -> list[str]:
        """Die Sätze, die in einen Prüfbericht gehören — ohne Wertung.

        Jeder Satz nennt seine Fundstelle und sagt, dass der Punkt **offen** ist.
        Kein Satz behauptet Erfüllung, Erforderlichkeit oder Entfall.
        """
        punkte = self.pruefpunkte(arbeitsstaette_nach_aschg)
        aus = [p.hinweis for p in punkte if p.hinweis]
        if punkte:
            aus.append(self.wahlrecht().hinweis)
        return aus
