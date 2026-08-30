"""OibRl2Provider — Enis' Query-API über OIB-Richtlinie 2, Punkt 5.4 + Tabelle 6.

Erfüllt das Protocol `hauptengine.contracts.ports.OibProvider`
(`bewerte_oib(projekt) -> OibBefund`). Beantwortet die Frage, die dem EN-1838-Pfad
vorgelagert ist: **braucht dieses Bauvorhaben überhaupt Sicherheitsbeleuchtung —
eingeschränkt oder uneingeschränkt?**

Alle fachlichen Werte (Zeilen, Schwellen, Fundstellen, Fußnoten, Ausführungs-
verweise) stehen in `data/oib_rl2_tabelle6.yaml`; dieses Modul hardcodet nichts.
Die Auswertungs-Logik liegt render- und contract-frei in `tabelle6.py`.

Jedes `OibErgebnis` trägt einen vollständigen Audit-Trail: welche Tabellenzeile,
welche Quelle und Ausgabe, welche Fundstelle, welcher Schwellenwert, welche
Projektfakten — und bei einem Review, welche Fakten fehlen bzw. welche
Unsicherheit die Entscheidung blockiert.

`nicht_erforderlich` gibt dieser Provider **nie** zurück: keines der im Repo
liegenden Dokumente sagt das für einen automatisierbaren Fall wörtlich.
"""
from __future__ import annotations

from pathlib import Path

import yaml

from notbeleuchtung.hauptengine.contracts import (
    Gebaeudeteil,
    OibBefund,
    OibErgebnis,
    ProjektKontext,
)

from . import tabelle6
from .tabelle6 import REVIEW, Auswertung

DATA_DIR = Path(__file__).parent.parent / "data"
DATEI = "oib_rl2_tabelle6.yaml"


class OibRl2Provider:
    """OibProvider-Impl gegen data/oib_rl2_tabelle6.yaml (OIB-RL 2, Mai 2023)."""

    def __init__(self, data_dir: Path | None = None) -> None:
        self._dir = data_dir or DATA_DIR
        with open(self._dir / DATEI, encoding="utf-8") as fh:
            self._doc = yaml.safe_load(fh)
        self._meta = self._doc["meta"]
        self._zeilen = self._doc["zeilen"]

    # ── Lesezugriff auf die Datengrundlage (Audit/Tests, nicht Teil des Ports) ──
    @property
    def abgedeckte_nutzungsarten(self) -> set[str]:
        """Nutzungsarten mit auswertbarer Tabellenzeile."""
        return {a for z in self._zeilen for a in z["nutzungsarten"]}

    @property
    def review_nutzungsarten(self) -> set[str]:
        """Nutzungsarten, für die Tabelle 6 keine auswertbare Zeile trägt."""
        return set(self._doc["review_nutzungsarten"])

    # ── OibProvider-Protocol ────────────────────────────────────────────────
    def bewerte_oib(self, projekt: ProjektKontext) -> OibBefund:
        """ProjektKontext → je Gebäudeteil ein OibErgebnis mit Audit-Trail.

        `nicht_zugeordnete_raum_referenzen` bleibt leer: diese Schnittstelle
        bekommt kein RaumModell, die Raumzuordnung ist hier NICHT prüfbar. Der
        entsprechende Hinweis hängt an jedem Ergebnis (`hinweise_global`).
        """
        return OibBefund(
            ergebnisse=[self._ergebnis(t, projekt) for t in projekt.gebaeudeteile],
            nicht_zugeordnete_raum_referenzen=[],
        )

    # ── Ergebnis-Bau ────────────────────────────────────────────────────────
    def _ergebnis(self, teil: Gebaeudeteil, projekt: ProjektKontext) -> OibErgebnis:
        aus = self._werte_aus(teil)
        self._pruefe_jurisdiktion(projekt, aus)

        zeile = aus.zeile or {}
        stufe = aus.stufe
        return OibErgebnis(
            gebaeudeteil_id=teil.id,
            stufe=stufe,
            zeile=zeile.get("zeile"),
            quelle=self._meta["quelle"],
            norm_ausgabe=self._meta["norm_ausgabe"],
            fundstelle_seite=zeile.get("fundstelle_seite", self._meta["fundstelle_seite"]),
            angewandter_schwellenwert=aus.angewandter_schwellenwert,
            eingangswerte=aus.eingangswerte,
            fehlende_fakten=aus.fehlende_fakten,
            hinweise=[*aus.hinweise, *self._astv_hinweise(teil), *self._doc["hinweise_global"]],
            ausfuehrungs_verweise=list(self._doc["ausfuehrungs_verweise"].get(stufe, [])),
        )

    def _werte_aus(self, teil: Gebaeudeteil) -> Auswertung:
        """Zeilenauswahl + Auswertung, inkl. der Nutzungsarten ohne Tabellenzeile."""
        review_arten = self._doc["review_nutzungsarten"]
        if teil.nutzungsart in review_arten:
            eintrag = review_arten[teil.nutzungsart]
            return Auswertung(
                stufe=REVIEW,
                eingangswerte={"nutzungsart": teil.nutzungsart},
                hinweise=[eintrag["grund"], eintrag["hinweis"]],
            )

        zeile, fehlende, hinweise = tabelle6.waehle_zeile(self._zeilen, teil)
        if zeile is None:
            return Auswertung(
                stufe=REVIEW,
                eingangswerte={
                    "nutzungsart": teil.nutzungsart,
                    "fluchtniveau_m": tabelle6.wert_text(teil.fluchtniveau_m),
                },
                fehlende_fakten=list(fehlende),
                hinweise=list(hinweise) or [
                    (
                        "Für diese Nutzungsart trägt Tabelle 6 keine auswertbare "
                        "Zeile (kein Umkehrschluss)."
                    )
                ],
            )
        return tabelle6.werte_zeile_aus(zeile, teil)

    def _pruefe_jurisdiktion(self, projekt: ProjektKontext, aus: Auswertung) -> None:
        """Ohne eindeutig 'AT' keine verbindliche OIB-RL-2-Stufe."""
        jur = self._doc["jurisdiktion"]
        aus.eingangswerte["jurisdiction"] = tabelle6.wert_text(projekt.jurisdiction)
        if projekt.jurisdiction == jur["erforderlich"]:
            return
        if aus.stufe != REVIEW:
            aus.kandidat_stufe = aus.stufe
            aus.hinweise.append(
                "Kandidatenstufe (NICHT verbindlich, nur Audit-Information): "
                f"{aus.stufe}."
            )
        aus.stufe = REVIEW
        aus.hinweise.append(jur["grund"])
        if jur["fehlender_fakt"] not in aus.fehlende_fakten:
            aus.fehlende_fakten.append(jur["fehlender_fakt"])

    def _astv_hinweise(self, teil: Gebaeudeteil) -> list[str]:
        """AStV-Parallelpfad — ergänzt nur, senkt nie (Erl.-S. 48)."""
        astv = self._doc["astv_parallelpfad"]
        if teil.arbeitsstaette_nach_aschg is True:
            return [astv["wenn_arbeitsstaette"]]
        if teil.arbeitsstaette_nach_aschg is None:
            return [astv["wenn_unbekannt"]]
        return []
