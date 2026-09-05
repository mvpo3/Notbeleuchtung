"""ove_zusatz — belegte Zusatz-Anforderungen aus OVE E 8101 718.560.9.001.AT.

Beantwortet **eine** Frage: *Ist für diesen Gebäudeteil und diesen Raum die
zusätzliche Sicherheitsbeleuchtung nach 718.560.9.001.AT quellenmäßig belegt?*

Sie beantwortet ausdrücklich **nicht**, welche Art von Beleuchtung auszuführen
ist und welcher lichttechnische Nachweis gilt — beides nennt die Klausel nicht
(`OffenerPunkt`). Erforderlichkeit, Beleuchtungsart und Nachweis sind drei
getrennte Fragen; dieses Modul liefert nur die erste.

**Es aktiviert nichts.** `NormRegelwerk.flaechen_schwellen` bleibt leer, es wird
keine Leuchte platziert. Die Werte begründen einen **Befund** im Prüfbericht.

**Ausgabestände.** Die OIB-Ausgabe wird **ausführbar** geprüft
(`OibErgebnis.norm_ausgabe` gegen die geprüfte Ausgabe). Für die OVE-Ausgaben
(E 8101, R 12-2) gibt es im Projekt **keine Auswahl** — der Befund ist deshalb
eine **Vorprüfung** unter der dokumentierten Quellenannahme
(`vorpruefungs_satz`). Dass die Ausgabe 2025 anzuwenden wäre, ist damit weder
behauptet noch ausgeschlossen.

Belegt ist Stand 2026-09-05 genau **ein** Fall: Verkaufs-/Ausstellungsstätten
über 3 000 m² Verkaufsfläche. Die Quellenkette dazu — OVE E 8101:2019 →
R 12-2/AC:2019-07-01 Tabelle 5.1 → OIB-RL 2 Mai 2023 Tabelle 6 Zeile 4 — steht in
`docs/NORMQUELLEN_AT.md` Abschnitt 2d. Ein fehlender Eintrag ist **kein
Ausschluss**, sondern „nicht geprüft".
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

DATA_DIR = Path(__file__).parent / "data"
DATEI = "ove_e8101_zusatz.yaml"


class ZusatzBefund(BaseModel):
    """Ein belegter Erforderlichkeits-Fall für genau einen Raum.

    `erfuellt` gibt es hier bewusst nicht: dieses Modul sagt, was **erforderlich**
    ist. Ob es erfüllt ist, entscheidet der Nachweis — und der ist offen.
    """

    fall_id: str
    raum_id: str
    gebaeudeteil_id: str
    folge: str                       # „Sicherheitsbeleuchtung erforderlich"
    begruendung: str                 # die geprüfte Kette in einem Satz
    quellen: list[str] = Field(default_factory=list)
    #: Was die Quelle NICHT hergibt — Art und Nachweis.
    offen: list[str] = Field(default_factory=list)


class OveZusatzKatalog:
    """Query-API über `data/ove_e8101_zusatz.yaml`."""

    def __init__(self, data_dir: Path | None = None) -> None:
        self._dir = data_dir or DATA_DIR
        self._cfg = _lade(self._dir)

    # ── Quellen ─────────────────────────────────────────────────────────────
    def quellen_mit_ausgabe(self) -> list[str]:
        """Die drei Glieder der Kette, jedes mit Ausgabestand."""
        q = self._cfg["quellen"]
        ove = f"{q['ove_e8101']['ausgabe']} {q['ove_e8101']['fundstelle']}"
        r12 = (
            f"{q['r12_2']['ausgabe']}, {q['r12_2']['fundstelle']}, "
            f"{q['r12_2']['spalte_erhoeht']}"
        )
        oib = (
            f"{q['oib_rl2']['ausgabe']}, {q['oib_rl2']['fundstelle']}, "
            f"{q['oib_rl2']['spalte_uneingeschraenkt']}"
        )
        return [ove, r12, oib]

    def hinweis_2025(self) -> str:
        return (self._cfg["nicht_uebertragbar"]["ove_e8101_2025"] or "").strip()

    # ── Ausgabestand: was prüfbar ist und was nicht ─────────────────────────
    def oib_ausgabe(self) -> str:
        """Der für **diese Zusatzregel** akzeptierte OIB-Ausgabestand.

        Er steht in `ove_e8101_zusatz.yaml` bei der Quelle selbst und wird
        **nicht** aus `oib_rl2_tabelle6.yaml` gelesen: jene Datei trägt die
        Metadaten der allgemeinen OIB-Auswertung. Würde der Vergleichswert von
        dort kommen, würde ein späterer Ausgabenwechsel der Provider-Daten den
        akzeptierten Stand stillschweigend mit erweitern — obwohl die
        Spalten-Entsprechung nur gegen **Mai 2023** geprüft ist.

        Nach einem Ausgabenwechsel muss der Abgleich neu geführt und dieser Wert
        bewusst nachgezogen werden; bis dahin entsteht kein Befund.
        """
        return str(self._cfg["quellen"]["oib_rl2"]["norm_ausgabe_string"])

    def passt_zur_geprueften_oib_ausgabe(self, norm_ausgabe: str | None) -> bool:
        """Stammt dieser Befund aus **der** OIB-Ausgabe, die geprüft wurde?

        Ausführbare Absicherung — `OibErgebnis.norm_ausgabe` ist ein typisiertes
        Contract-Feld. Weicht es ab, gilt die geprüfte Kette nicht und es wird
        **kein** Befund erzeugt (der Fall bleibt dann ungeklärt wie zuvor).
        """
        return bool(norm_ausgabe) and norm_ausgabe.strip() == self.oib_ausgabe()

    def vorpruefungs_satz(self) -> str:
        """Der Vorbehalt, unter dem der Befund steht.

        Für die **OVE**-Ausgaben (E 8101, R 12-2) gibt es im Projekt **keine**
        Auswahl — weder im `ProjektKontext` noch anderswo. Sie sind deshalb nicht
        ausführbar prüfbar; der Befund ist eine **Vorprüfung** unter der
        dokumentierten Quellenannahme. Das ist ausdrücklich keine Aussage
        darüber, dass eine Anwendung der Ausgabe 2025 ausgeschlossen wäre.
        """
        return (self._cfg["ausgaben_pruefung"]["vorpruefungs_satz"] or "").strip()

    def ausgaben_pruefstatus(self) -> dict[str, str]:
        cfg = dict(self._cfg["ausgaben_pruefung"])
        cfg.pop("vorpruefungs_satz", None)
        return {k: str(v) for k, v in cfg.items()}

    # ── Bewertung ───────────────────────────────────────────────────────────
    def faelle(self) -> list[dict]:
        return list(self._cfg["belegte_faelle"])

    def ist_belegte_nutzung(self, nutzungsart: str | None, stufe: str | None) -> dict | None:
        """Der belegte Fall für diese Nutzungsart **und** OIB-Stufe — oder `None`.

        Beide Bedingungen müssen zum **selben** Gebäudeteil gehören; das stellt
        der Aufrufer sicher, indem er Nutzungsart und Stufe aus demselben
        `Gebaeudeteil`/`OibErgebnis`-Paar übergibt.
        """
        for fall in self.faelle():
            if fall["nutzungsart"] == nutzungsart and fall["erforderliche_oib_stufe"] == stufe:
                return fall
        return None

    def kennzahl_erfuellt(self, fall: dict, wert: float | None) -> bool:
        """Reißt die Kennzahl des Gebäudeteils die Schwelle der Tabellenzeile?

        `None` (Angabe fehlt) ist **nicht** erfüllt — ohne Zahl kein Beleg.
        """
        if wert is None:
            return False
        return float(wert) > float(fall["kennzahl"]["ueber"])

    def bereich_erfuellt(self, fall: dict, raum_typ: str, flaeche_m2: float | None) -> bool:
        """Ist dieser Raum der in Punkt 1 genannte Bereich in der genannten Größe?"""
        b = fall["bereich"]
        if raum_typ.upper() not in {t.upper() for t in b["raumtypen"]}:
            return False
        return flaeche_m2 is not None and float(flaeche_m2) >= float(b["min_flaeche_m2"])

    def offene_punkte(self, fall: dict) -> list[str]:
        offen = fall.get("offen") or {}
        return [str(v).strip() for v in offen.values() if str(v).strip()]

    def begruendung(self, fall: dict, gebaeudeteil_id: str, kennzahl_wert: float) -> str:
        k, b = fall["kennzahl"], fall["bereich"]
        return (
            f"Gebäudeteil {gebaeudeteil_id}: {fall['nutzungsart']} mit "
            f"{k['bezeichnung']} {kennzahl_wert:g} m² ({k['schwellentext']}) → "
            f"OIB-Stufe {fall['erforderliche_oib_stufe']} = erhöhte Anforderungen "
            f"nach der Art der Nutzung; Raum ist {b['bezeichnung']} "
            f"({b['schwellentext']})"
        )


@lru_cache(maxsize=4)
def _lade(data_dir: Path) -> dict:
    with open(data_dir / DATEI, encoding="utf-8") as fh:
        return yaml.safe_load(fh)
