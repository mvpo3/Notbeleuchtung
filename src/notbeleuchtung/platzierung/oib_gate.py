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

## Zwei Fragen, die auseinandergehalten werden müssen

**1. Räumliche Zuordnung** (`raum_zuordnung`): Erfasst ein Gebäudeteil mit
positivem OIB-Befund genau diesen Raum? Das beantwortet der `OibBefund` samt
`raum_referenzen` — `bestaetigt` / `nicht_bestaetigt` / `ungeklaert`.

**2. Fachliche Anwendbarkeit der OVE-Regel** (`sanitaer_scope`): Gehört der Raum
zu „Räumen, Anlagen oder Gebäuden, an die **erhöhte Anforderungen nach der Art
der Nutzung** (siehe OVE-Richtlinie **R 12-2** bzw. OIB-Richtlinie 2) gestellt
werden"? **Das beantwortet der OibBefund nicht.** Er sagt nur, ob nach
**OIB-RL 2 Tabelle 6** eine Sicherheitsbeleuchtung erforderlich ist
(`eingeschraenkt` = auf Fluchtwege beschränkt, `uneingeschraenkt` = darüber
hinaus). Dass „Tabelle-6-Erforderlichkeit" dasselbe meint wie „erhöhte
Anforderungen nach der Art der Nutzung", ist eine **Auslegung ohne Beleg**:
R 12-2 liegt nicht im Repo, und die OIB-Erläuterungen verweisen darauf nur
„je nach Zutreffen".

⚠️ **Folge in beide Richtungen.** Eine bestätigte Raumzuordnung allein macht die
OVE-Regel **nicht** anwendbar — und eine fehlende oder negative Zuordnung macht
sie ebenso wenig **un**anwendbar. „Nach Tabelle 6 nicht erforderlich" schließt
den in der Klausel zuerst genannten **R-12-2-Zweig** nicht aus, und ein gar nicht
gefahrener OIB-Pfad sagt über die Sache nichts. `sanitaer_scope` vergibt deshalb
**weder `anwendbar` noch `nicht_anwendbar`**: bewertet → `ungeklaert`, nicht
bewertet → `nicht_bewertet`. Die Fälle sind nicht verloren: sie stehen als
`ungeklaert` im Prüfbericht und im Audit-Block, mit dem Grund. Erst wenn R 12-2
vorliegt oder die drei Owner die Gleichsetzung ausdrücklich als Auslegung
beschließen, kann daraus `anwendbar` werden.

Korrektur-Slice Enis, 2026-09-05 — **Änderung in Leonis' Lane, bitte @mvpo3
reviewen.** Analyse: `docs/proposals/BLOCKER2_FLAECHEN_SCOPE.md`.
"""
from __future__ import annotations

from typing import Literal

from notbeleuchtung.hauptengine.contracts import OibBefund

#: Fachliche Anwendbarkeit eines Triggers auf einen Raum.
#:
#: `nicht_bewertet` = es lief gar keine Auswertung (kein ProjektKontext/OIB-Pfad)
#: — daraus wird KEINE fachliche Aussage abgeleitet, weder positiv noch negativ.
#: `nicht_anwendbar` wäre eine positive Ausschluss-Aussage und braucht einen
#: eigenen Beleg; heute wird sie nirgends vergeben (siehe `sanitaer_scope`).
Scope = Literal["anwendbar", "nicht_anwendbar", "ungeklaert", "nicht_bewertet"]

#: Räumliche Zuordnung eines Raums zu einem Gebäudeteil mit OIB-Befund.
Zuordnung = Literal["bestaetigt", "nicht_bestaetigt", "ungeklaert"]

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


def _aussage(stufe: str) -> Zuordnung:
    """Stufe → Aussage-Richtung der räumlichen Zuordnung (nicht die Stufe selbst)."""
    if stufe in _OFFEN:
        return "bestaetigt"
    if stufe == _UNGEKLAERT_STUFE:
        return "ungeklaert"
    return "nicht_bestaetigt"


def _referenziert(eintrag, floor: str, raum_id: str) -> bool:
    return any(r.floor == floor and r.raum_id == raum_id for r in eintrag.raum_referenzen)


def raum_zuordnung(oib: OibBefund | None, floor: str, raum_id: str) -> Zuordnung:
    """**Frage 1 — räumlich:** Erfasst ein Gebäudeteil mit positivem OIB-Befund
    genau diesen Raum?

    Reihenfolge — die erste zutreffende Aussage gewinnt:

    1. kein OIB-Pfad → `nicht_bestaetigt` — eine Tatsachen-, keine Wertungsaussage:
       es liegt schlicht keine Zuordnung vor (die fachliche Frage beantwortet
       `sanitaer_scope` mit `nicht_bewertet`);
    2. der Raum ist referenziert und die referenzierenden Teile sind sich
       **uneinig** → `ungeklaert` (ein bestätigender Teil überstimmt einen
       ungeklärten oder gegenteiligen **nicht**);
    3. alle referenzierenden Teile bestätigen → `bestaetigt`;
    4. alle referenzierenden Teile sind `review_required` → `ungeklaert`;
    5. alle referenzierenden Teile verneinen → `nicht_bestaetigt`;
    6. der Raum ist nirgends referenziert, aber ein bestätigender oder
       ungeklärter Teil trägt **keine** Zuordnung → `ungeklaert`;
    7. sonst → `nicht_bestaetigt`.

    Schritt 6 ersetzt den früheren Rückfall auf „alle Räume": ein Befund ohne
    Raumzuordnung sagt nichts über diesen Raum — er darf ihn weder freigeben noch
    stillschweigend ausschließen.
    """
    if oib is None:
        return "nicht_bestaetigt"
    treffer = [e for e in oib.ergebnisse if _referenziert(e, floor, raum_id)]
    if treffer:
        # Nach Aussage-Richtung gruppieren, nicht nach Stufe: `eingeschraenkt` und
        # `uneingeschraenkt` sagen beide „erforderlich" und widersprechen einander
        # nicht.
        aussagen = {_aussage(e.stufe) for e in treffer}
        if len(aussagen) > 1:
            return "ungeklaert"
        return aussagen.pop()
    ohne_zuordnung = [
        e for e in (*_bestaetigende(oib), *_ungeklaerte(oib)) if not e.raum_referenzen
    ]
    return "ungeklaert" if ohne_zuordnung else "nicht_bestaetigt"


def sanitaer_scope(oib: OibBefund | None, floor: str, raum_id: str) -> Scope:
    """**Frage 2 — fachlich:** Ist der 8-m²-Trigger (OVE Punkt 1) hier anwendbar?

    Getrennt von `raum_zuordnung`, und beide Richtungen brauchen einen Beleg:

    * **`anwendbar`** setzt voraus, dass der Raum zu „Räumen, Anlagen oder
      Gebäuden mit erhöhten Anforderungen **nach der Art der Nutzung**" gehört.
      Der `OibBefund` belegt das nicht — er sagt nur, ob Tabelle 6 eine
      Sicherheitsbeleuchtung verlangt. → wird heute **nie** vergeben.
    * **`nicht_anwendbar`** ist die Gegenrichtung und genauso begründungspflichtig:
      es hieße „diese OVE-Regel gilt hier nachweislich nicht". Weder ein fehlender
      noch ein negativer OIB-Befund belegt das — die Klausel nennt
      **R 12-2 bzw. OIB-RL 2**, und ein „nach Tabelle 6 nicht erforderlich"
      schließt den R-12-2-Zweig nicht aus. → wird heute ebenfalls **nie** vergeben.
    * **`nicht_bewertet`** heißt: es lief keine Auswertung (kein OIB-Pfad). Das ist
      eine Aussage über den Vorgang, nicht über die Sache — und darf in der
      Ausgabe nicht als Nicht-Erforderlichkeit erscheinen.
    * **`ungeklaert`** ist damit der Regelfall, sobald überhaupt bewertet wurde.

    Die Unterscheidung, die trotzdem Wert hat, steckt in `raum_zuordnung`: sie
    sagt, ob die **räumliche** Frage beantwortet ist. Nur sie steuert, was der
    Prüfbericht als offenen Punkt meldet.
    """
    if oib is None:
        return "nicht_bewertet"
    return "ungeklaert"


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
        return "nicht_bewertet"
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


def unbekannte_raum_referenzen(
    oib: OibBefund | None, floor: str, raum_ids: list[str]
) -> list[str]:
    """Referenzen dieses Geschosses, die auf einen **nicht vorhandenen** Raum zeigen.

    Sie geben nichts frei — `sanitaer_scope` findet für sie keinen Raum, und der
    betroffene (nicht existente) Raum wird nie bestückt. Sichtbar müssen sie
    trotzdem sein: eine ins Leere zeigende Zuordnung ist ein Datenfehler im
    ProjektKontext und bedeutet, dass der gemeinte Raum **ohne** Zuordnung
    dasteht. `OibBefund.nicht_zugeordnete_raum_referenzen` hilft dabei nicht —
    der Provider bekommt kein RaumModell und lässt das Feld bewusst leer.
    """
    if oib is None:
        return []
    bekannt = set(raum_ids)
    return sorted({
        ref.raum_id
        for e in oib.ergebnisse
        for ref in e.raum_referenzen
        if ref.floor == floor and ref.raum_id not in bekannt
    })


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
        unbekannt = unbekannte_raum_referenzen(oib, floor, raum_ids)
        if unbekannt:
            hinweise.append(
                "raum_referenzen zeigen auf unbekannte Räume dieses Geschosses "
                f"({', '.join(unbekannt[:5])}) — sie geben nichts frei; der gemeinte "
                "Raum steht damit ohne Zuordnung da."
            )
        zuordnungen = [raum_zuordnung(oib, floor, r) for r in raum_ids]
        block["raum_zuordnung"] = {
            z: zuordnungen.count(z)
            for z in ("bestaetigt", "nicht_bestaetigt", "ungeklaert")
        }
        zustaende = [sanitaer_scope(oib, floor, r) for r in raum_ids]
        block["sanitaer_scope"] = {
            z: zustaende.count(z)
            for z in ("anwendbar", "nicht_anwendbar", "ungeklaert", "nicht_bewertet")
        }
        hinweise.append(
            "Fachliche Anwendbarkeit der OVE-Flächen-Trigger: weder bejaht noch "
            "verneint. Ein fehlender oder negativer OIB-Befund belegt keinen "
            "Ausschluss — die Klausel nennt R 12-2 bzw. OIB-RL 2, und Tabelle 6 "
            "deckt nur den zweiten Zweig ab."
        )
        if zuordnungen.count("bestaetigt"):
            hinweise.append(
                f"{zuordnungen.count('bestaetigt')} Raum/Räume sind einem "
                "Gebäudeteil mit positivem OIB-Befund zugeordnet — die fachliche "
                "Anwendbarkeit der OVE-Regel bleibt trotzdem UNGEKLÄRT: Tabelle 6 "
                "belegt die Erforderlichkeit einer Sicherheitsbeleuchtung, nicht "
                "die erhoehten Anforderungen nach der Art der Nutzung (R 12-2 "
                "liegt nicht vor)."
            )
        block["verkehr_scope"] = {"anwendbar": 0, "ungeklaert": len(raum_ids)}
        block["unbekannte_raum_referenzen"] = unbekannt
    return block
