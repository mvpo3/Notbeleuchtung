"""oib_gate — Geltungsbereich der OVE-scope-gebundenen Flächen-Trigger.

Die Flächen-Schwellen des Antipanik-Triggers stammen aus **OVE E 8101:2019/2025
718.560.9.001.AT** (am Original geprüft, Teil 7-718 Seite 4). Der Einleitungssatz
bindet sie an **„Räume, Anlagen oder Gebäude, an die erhöhte Anforderungen nach
der Art der Nutzung (siehe OVE-Richtlinie R 12-2 bzw. OIB-Richtlinie 2) gestellt
werden"** — die Bezugseinheit ist der Raum bzw. Gebäudeteil, **nicht das Projekt**.

Die Klausel führt zwei getrennte Aufzählungspunkte mit **verschiedenen**
Nutzungs-Scopes:

* **Punkt 1)** „in Sanitärbereichen ab 8 m² Größe …" — gilt für **jede** Nutzung
  mit erhöhten Anforderungen.
* **Punkt 3)** „**in verkehrstechnischen Einrichtungen wie zB Flughäfen und
  Bahnhöfen** … Geschäftsflächen über 60 m², Arbeitsräume und Räume über 60 m²,
  die zur Aufrechterhaltung des Betriebes notwendig sind" — gilt **nur** dort und
  hängt zusätzlich an einer Raumkategorie.

Deshalb hat dieses Modul **zwei getrennte Auswertungen**. Ein bestätigter
Verkaufsteil öffnet den 60-m²-Trigger nicht.

**Drei Zustände statt eines Booleans** (`Scope`):

* `anwendbar` — ein bestätigender Gebäudeteil erfasst genau diesen Raum;
* `nicht_anwendbar` — der Raum ist erfasst und nicht bestätigt, oder es läuft gar
  kein OIB-Pfad (dann sind die scope-gebundenen Zusatz-Trigger nicht in Frage);
* `ungeklaert` — der Geltungsbereich lässt sich für diesen Raum nicht bestimmen
  (Gebäudeteil `review_required`, oder ein bestätigender Teil ohne
  `raum_referenzen`). **Ungeklärt ist nicht „nicht erforderlich"** — der Fall
  gehört sichtbar in den Prüfbericht (Regel 13) und löst keine Platzierung aus.

Fail closed: nur `anwendbar` platziert. Das frühere Verhalten „ein bestätigender
Teil öffnet alle Räume aller Geschosse" ist damit weg.

Korrektur-Slice Enis, 2026-09-05 — **Änderung in Leonis' Lane, bitte @mvpo3
reviewen.** Analyse: `docs/proposals/BLOCKER2_FLAECHEN_SCOPE.md`.
"""
from __future__ import annotations

from typing import Literal

from notbeleuchtung.hauptengine.contracts import OibBefund

#: Auswertung je Raum und je Trigger.
Scope = Literal["anwendbar", "nicht_anwendbar", "ungeklaert"]

# Stufen, die die „erhöhten Anforderungen" des OVE-Scopes bestätigen.
_OFFEN = {"eingeschraenkt", "uneingeschraenkt"}
_UNGEKLAERT_STUFE = "review_required"

_HINWEIS_RAUM_GENAU = (
    "OIB-Scope raum-genau: die OVE-Flächen-Trigger gelten nur für die in "
    "raum_referenzen benannten Räume bestätigender Gebäudeteile."
)
_HINWEIS_OHNE_ZUORDNUNG = (
    "Mindestens ein bestätigender Gebäudeteil trägt keine raum_referenzen — für "
    "die nicht zugeordneten Räume bleibt der Geltungsbereich UNGEKLÄRT (früher: "
    "projekt-global freigegeben)."
)
_HINWEIS_VERKEHR = (
    "60-m²-Trigger (OVE 718.560.9.001.AT Punkt 3) bleibt zu: er gilt nur für "
    "verkehrstechnische Einrichtungen; die Nutzungsart ist im OibBefund nicht "
    "zugesichert und die geforderte Raumkategorie fehlt im RaumModell."
)


def _bestaetigende(oib: OibBefund):
    return [e for e in oib.ergebnisse if e.stufe in _OFFEN]


def _ungeklaerte(oib: OibBefund):
    return [e for e in oib.ergebnisse if e.stufe == _UNGEKLAERT_STUFE]


def _referenziert(eintrag, floor: str, raum_id: str) -> bool:
    return any(r.floor == floor and r.raum_id == raum_id for r in eintrag.raum_referenzen)


def sanitaer_scope(oib: OibBefund | None, floor: str, raum_id: str) -> Scope:
    """Geltungsbereich des **8-m²-Triggers** (OVE Punkt 1) für genau diesen Raum.

    Reihenfolge der Prüfung — die erste zutreffende Aussage gewinnt:

    1. kein OIB-Pfad → `nicht_anwendbar` (die Zusatz-Trigger stehen nicht in Frage);
    2. ein **bestätigender** Teil referenziert den Raum → `anwendbar`;
    3. ein **review_required**-Teil referenziert ihn → `ungeklaert`;
    4. der Raum ist von irgendeinem Teil referenziert (also bewertet und nicht
       bestätigt) → `nicht_anwendbar`;
    5. der Raum ist nirgends referenziert, aber ein bestätigender oder
       ungeklärter Teil trägt **keine** Zuordnung → `ungeklaert`;
    6. sonst → `nicht_anwendbar`.

    Schritt 5 ersetzt den früheren Rückfall auf „alle Räume": ein Befund ohne
    Raumzuordnung sagt nichts über diesen Raum — er darf ihn weder freigeben noch
    stillschweigend ausschließen.
    """
    if oib is None:
        return "nicht_anwendbar"
    if any(_referenziert(e, floor, raum_id) for e in _bestaetigende(oib)):
        return "anwendbar"
    if any(_referenziert(e, floor, raum_id) for e in _ungeklaerte(oib)):
        return "ungeklaert"
    if any(_referenziert(e, floor, raum_id) for e in oib.ergebnisse):
        return "nicht_anwendbar"
    ohne_zuordnung = [
        e for e in (*_bestaetigende(oib), *_ungeklaerte(oib)) if not e.raum_referenzen
    ]
    return "ungeklaert" if ohne_zuordnung else "nicht_anwendbar"


def verkehr_scope(oib: OibBefund | None, floor: str, raum_id: str) -> Scope:
    """Geltungsbereich des **60-m²-Triggers** (OVE Punkt 3) für diesen Raum.

    Heute nie `anwendbar`. Zwei Gründe, beide belegt in
    `docs/proposals/BLOCKER2_FLAECHEN_SCOPE.md`:

    * Die Nutzungsart „verkehrstechnische Einrichtung" ist im `OibBefund` **nicht
      zugesichert** — sie steht nur im Audit-Dict `eingangswerte`, und darauf darf
      keine Platzierung aufbauen.
    * Punkt 3 verlangt zusätzlich eine **Raumkategorie** (Wartezone,
      Abfertigungshalle, Geschäftsfläche, betriebsnotwendiger Arbeitsraum), die
      das `RaumModell` nicht führt.

    Ein bestätigter Verkaufs- oder Wohnteil sagt über diesen Trigger **nichts** —
    deshalb wird aus ihm auch keine Freigabe abgeleitet. Läuft ein OIB-Pfad,
    bleibt der Fall `ungeklaert` (sichtbar im Prüfbericht), sonst
    `nicht_anwendbar`.
    """
    if oib is None:
        return "nicht_anwendbar"
    return "ungeklaert"


def raeume_ohne_geklaerten_scope(
    oib: OibBefund | None, floor: str, raum_ids: list[str]
) -> list[str]:
    """Räume dieses Geschosses, deren Geltungsbereich **ungeklärt** ist.

    Für den Prüfbericht (Regel 13): diese Räume sind weder freigegeben noch
    ausgeschlossen. Sie erscheinen auch dann, wenn ein **anderer** Gebäudeteil
    bestätigt ist — genau der Fall, der vorher unsichtbar blieb.
    """
    if oib is None:
        return []
    return [r for r in raum_ids if sanitaer_scope(oib, floor, r) == "ungeklaert"]


def gate_summary(oib: OibBefund, floor: str = "", raum_ids: list[str] | None = None) -> dict:
    """Audit-Block für `render_summary["oib"]` — Stufen je Gebäudeteil + Scope-Lage.

    `floor`/`raum_ids` optional: sind sie gesetzt, zählt der Block die Räume je
    Scope-Zustand aus, statt nur ein Gate-Flag zu melden.
    """
    bestaetigend = _bestaetigende(oib)
    raum_genau = bool(bestaetigend) and all(e.raum_referenzen for e in bestaetigend)
    hinweise: list[str] = []
    if bestaetigend and raum_genau:
        hinweise.append(_HINWEIS_RAUM_GENAU)
    if any(not e.raum_referenzen for e in (*bestaetigend, *_ungeklaerte(oib))):
        hinweise.append(_HINWEIS_OHNE_ZUORDNUNG)
    if _ungeklaerte(oib):
        hinweise.append(
            "OIB-Erforderlichkeit review_required — betroffene Räume gelten als "
            "UNGEKLÄRT (weder erforderlich noch nicht erforderlich), auch wenn ein "
            "anderer Gebäudeteil bestätigt ist."
        )
    hinweise.append(_HINWEIS_VERKEHR)

    block: dict = {
        "stufen": {e.gebaeudeteil_id: e.stufe for e in oib.ergebnisse},
        "raum_genau": bool(bestaetigend) and raum_genau,
        "hinweise": hinweise,
    }
    if raum_ids:
        zustaende = [sanitaer_scope(oib, floor, r) for r in raum_ids]
        block["sanitaer_scope"] = {
            z: zustaende.count(z)
            for z in ("anwendbar", "nicht_anwendbar", "ungeklaert")
        }
        block["verkehr_scope"] = {"anwendbar": 0, "ungeklaert": len(raum_ids)}
    return block
