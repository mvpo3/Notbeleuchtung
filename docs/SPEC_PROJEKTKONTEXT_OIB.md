# Spec — ProjektKontext + OibErgebnis (Enis → Leonis)

**Absender:** Enis (`src/notbeleuchtung/normwissen/`) · **Adressat:** Leonis (Owner
`hauptengine/contracts/`) · **Stand:** 2026-08-30 · **Status:** **RATIFIZIERT** —
die Contracts liegen auf main (PR #14), der Resolver fehlt noch.

Fachliche Grundlage: [`OIB_RL2_TABELLE6.md`](OIB_RL2_TABELLE6.md) (Tabelle 6,
Punkt 5.4, Erläuterungen, RL 2.1/2.2/2.3, Begriffsbestimmungen).

## 0. Ratifizierung durch PR #14 — was gegenüber diesem Entwurf gilt

PR #14 (`9376e5f`) hat `ProjektKontext`, `Gebaeudeteil`, `RaumReferenz`,
`OibErgebnis`, `OibBefund` + `OibProvider` angelegt — bewusst **ohne Resolver und
ohne Tabelle-6-Grenzwerte** (das ist Enis' Lane). Drei Punkte weichen vom Entwurf
unten ab; **es gilt der Contract auf main**, nicht der Entwurfstext:

| Entwurf (unten) | Contract auf main | Warum |
|---|---|---|
| `raum_ids: list[str]` + `floors: list[str]` | `raum_referenzen: list[RaumReferenz]` mit `RaumReferenz(floor, raum_id)` | Raum↔Geschoss bleibt über mehrere Geschosse eindeutig |
| `arbeitsstaette_nach_aschg` auf `ProjektKontext` (global) | auf `Gebaeudeteil` | ein Gebäudeteil kann Arbeitsstätte sein, ein anderer nicht |
| `nicht_zugeordnete_raum_ids` | `nicht_zugeordnete_raum_referenzen` | Folge von Punkt 1 |

Analog heißt die Naht-Invariante jetzt: `∀ gt, ∀ rr ∈ gt.raum_referenzen:
rr.floor == RaumModell.floor ∧ rr.raum_id ∈ {r.id}` (Testgrundlage liegt in
`tests/contract/test_projekt_kontext_contract.py`).

**Frage 1 ist beantwortet:** eigenes `OibProvider`-Protocol
(`bewerte_oib(projekt) -> OibBefund`), `NormProvider` bleibt unberührt.
**Frage 2 (`GebaeudeModell` für mehrgeschoßige Kennzahlen) bleibt offen** — der
Contract kommentiert nur „gebäudeweit, NICHT geschossweise", ohne die Quelle der
Kennzahlen zu klären. Solange niemand sie liefert, endet der Resolver bei
`review_required` + `fehlende_fakten` — das ist gewollt, aber keine Antwort.

**Noch offen (nicht Teil von PR #14):** `OibProvider` ist in keinem
`ProviderBundle` verdrahtet und `pipeline.run()` nimmt keinen `ProjektKontext`
entgegen. Der `OibBefund` hat also heute keinen Abnehmer — die Verdrahtung fasst
`ports.py`/`pipeline.py` an und braucht 3-Owner-Konsens.

**Problem:** Die Entscheidung „braucht dieses Bauvorhaben Sicherheitsbeleuchtung —
und in welcher Stufe?" hängt an Gebäude- und Nutzungsfakten (Nutzungsart,
Gebäudeklasse, Fluchtniveau, Betten/Personen/Flächen). Das System kennt heute
**keinen einzigen** davon: `RaumModell` ist reine Geometrie/Topologie,
`pipeline.run()` nimmt nur `bundle, dxf_path, floor, out_path`, ein
Projekt-/Gebäudekontext existiert nicht.

## 1. Felder — was gebraucht wird, was entfällt

Entfallen (sauber aus `nutzungsart` ableitbar, keine redundanten bools):
`wohngebaeude`, `krankenhaus`, `betriebsbau`, `garage/stellplatz/parkdeck` als
eigenes Feld, `innerhalb_ausserhalb_gebaeude`, `schutzhuette_extremlage`,
`raum_fuer_mehr_als_60_personen`.

**Kein bool für Unbekanntes:** jedes Kennzahlfeld ist `Optional[...] = None`;
`None` = „nicht erhoben" ⇒ Resolver liefert `review_required`, nie eine Annahme.

```
ProjektKontext
  contract:            Literal["ProjektKontext"]
  contract_version:    str
  jurisdiction:        Literal["AT"] | None
  bundesland:          Enum[W,NOE,OOE,SBG,STMK,KTN,TIR,VBG,BGLD] | None
  projekt_stichtag:    datetime.date | None
  arbeitsstaette_nach_aschg: bool | None
  gebaeudeteile:       list[Gebaeudeteil]

Gebaeudeteil
  id:                  str
  bezeichnung:         str = ""
  nutzungsart:         Nutzungsart                    # Pflicht
  gebaeudeklasse:      Enum[GK1..GK5] | None          # Zeilen 1.1, 1.2
  fluchtniveau_m:      float | None                   # Gruppe 1 vs 12; Stufe 32 m
  lage_zur_wohnung:    Enum[AUSSERHALB_WOHNUNG, INNERHALB_WOHNUNG] | None
  netto_grundflaeche_m2:  float | None                # Zeilen 2, 10 — Fußnote (1)
  verkaufsflaeche_m2:     float | None                # Zeile 4 — Fußnote (2)
  nutzflaeche_garage_m2:  float | None                # Zeilen 11.1, 11.2 — Fußnote (3)
  betten_anzahl:          int | None                  # Zeilen 3, 6, 7
  schlafplaetze_anzahl:   int | None                  # Punkt 7.9.12 (Schutzhütte)
  verabreichungsplaetze_anzahl: int | None            # Zeile 5.1
  personen_anzahl_bestimmt:     int | None            # Zeilen 5.2, 9.1, 9.2
  raum_ids:            list[str] = []                 # -> RaumModell.raeume[].id
  floors:              list[str] = []                 # -> RaumModell.floor
```

Die drei Flächenfelder werden **nicht** zusammengelegt: Netto-Grundfläche,
Verkaufsfläche und Nutzfläche (Garage) sind in den Begriffsbestimmungen
unterschiedlich definiert.
`betten_anzahl` ≠ `schlafplaetze_anzahl`: Tabelle 6 sagt „Betten", Punkt 7.9.12 sagt
„Schlafplätze" — Gleichsetzung ist nicht belegt.

`jurisdiction`, `bundesland`, `projekt_stichtag`, `arbeitsstaette_nach_aschg`
werden von Tabelle 6 **nicht** gefordert; sie sind Anwendbarkeits-/Audit-Felder
(welche Ausgabe gilt, ist die OIB-Richtlinie hier überhaupt übernommen, läuft
zusätzlich der AStV-Pfad).

### Nutzungsart — Werte ausschließlich aus Tabelle 6 / den Erläuterungen

| Wert | Zeile |
|---|---|
| `WOHNGEBAEUDE` | 1.1 bzw. 12.1 (Auswahl über `fluchtniveau_m`) |
| `SONSTIGES_GEBAEUDE` | 1.2 bzw. 12.2 |
| `SCHULE_KINDERGARTEN` | 2 |
| `BEHERBERGUNG_STUDENTENHEIM` | 3 |
| `SCHUTZHUETTE_EXTREMLAGE` | 3 + Punkt 7.9.12 (Schwelle 30 Schlafplätze) |
| `VERKAUFSSTAETTE_AUSSTELLUNGSSTAETTE` | 4 |
| `SCHANK_SPEISEWIRTSCHAFT` | 5.1 |
| `DISKOTHEK_TANZCAFE` | 5.2 |
| `ALTEN_SENIORENHEIM` | 6 |
| `PFLEGEHEIM` | 7 |
| `KRANKENHAUS` | 8 |
| `VERSAMMLUNG_INNERHALB_GEBAEUDE` | 9.1 |
| `VERSAMMLUNG_AUSSERHALB_GEBAEUDE` | 9.2 |
| `BETRIEBSBAU` | 10 |
| `GARAGE` | 11.1 |
| `PARKDECK` | 11.1 (eigener Begriff) |
| `UEBERDACHTER_STELLPLATZ` | 11.2 |
| `VERKEHRSEINRICHTUNG` | keine Zeile — Erl. S.48: „sinngemäß **können** … gleichgestellt werden" ⇒ immer `review_required` |
| `NICHT_IN_TABELLE_6` | Auffangwert ⇒ `review_required` (AStV kann dennoch fordern) |

## 2. Gemischte Nutzung

Punkt 5.4 Satz 2 verlangt Nutzungs-getrennte Betrachtung ⇒ Entscheidung **je
Gebäudeteil**, nie fürs ganze Projekt.

```
ProjektKontext
 ├─ gt_wohnen   WOHNGEBAEUDE  GK5  fluchtniveau_m=18.0  raum_ids=[stgh_a, stgh_b]
 ├─ gt_garage   GARAGE        nutzflaeche_garage_m2=980  raum_ids=[garage_ug1]
 └─ gt_gewerbe  NICHT_IN_TABELLE_6
```

**Verknüpfung zum RaumModell:** `Gebaeudeteil.raum_ids` gegen
`RaumModell.raeume[].id` — dasselbe Muster wie die bestehende Naht
`Platzierung.covers_segment ∈ zirkulation.segmente[].segment_id`. Daraus folgt eine
**vierte Naht-Invariante** für `tests/contract/`:

> `∀ gt: set(gt.raum_ids) ⊆ {r.id für r ∈ RaumModell.raeume}`

Verworfen: Zuordnung über `Raum.raum_typ` (freier String, kein Vokabular) und über
Polygon-Containment (würde eine Nutzungswidmung aus Geometrie erraten).
Räume ohne Gebäudeteil-Zuordnung ⇒ eigener Befund `review_required`, nie stilles
Durchfallen.

**Offen:** `RaumModell` ist geschoßweise (`floor: str`), Fluchtniveau und
Netto-Grundfläche sind gebäudeweit. Deshalb `floors: list[str]`. Ob wir später ein
`GebaeudeModell` brauchen, entscheidet Leonis.

## 3. Ergebnis

```
OibStufe = Literal["nicht_erforderlich","eingeschraenkt","uneingeschraenkt","review_required"]
```
(Kleinschreibung analog zu den bestehenden `Klassifikation`/`Kind`/`Richtung`-Literals.)

```
OibErgebnis                       # je Gebäudeteil
  contract, contract_version
  gebaeudeteil_id:       str
  stufe:                 OibStufe
  zeile:                 str | None      # "11.1", "3 (i.V.m. 7.9.12)"
  quelle:                str             # "OIB-Richtlinie 2, Tabelle 6"
  norm_ausgabe:          str             # "Ausgabe Mai 2023 (OIB-330.2-029/23)"
  fundstelle_seite:      str | None      # "Norm-S. 32 / PDF-S. 34"
  angewandter_schwellenwert: str | None
  eingangswerte:         dict[str,str]   # welche Fakten die Zeile ausgewählt haben
  fehlende_fakten:       list[str] = []
  hinweise:              list[str] = []
  ausfuehrungs_verweise: list[str] = []

OibBefund
  ergebnisse:            list[OibErgebnis]
  nicht_zugeordnete_raum_ids: list[str] = []
```

`ausfuehrungs_verweise` = wörtlich aus RL 2-Erl S.48: EN 1838 · EN 50172 ·
OVE E 8101 · R 12-2 Punkte 3/4/5.1–5.3 · Funktionserhalt R 12-2 Punkt 6
(bei `eingeschraenkt` mit Abweichungsmöglichkeit, bei `uneingeschraenkt` ohne).

**Befund zur Reichweite:** `nicht_erforderlich` ist mit den heutigen Quellen
faktisch **unerreichbar** — die Tabelle sagt „nicht erforderlich" nur in der
Spalte *uneingeschränkt* (Zeilen 1.1, 1.2, 11.2), wo die eingeschränkte Stufe
gleichzeitig erforderlich ist. Der Resolver v1 wird nur `eingeschraenkt`,
`uneingeschraenkt` und `review_required` liefern. Der Wert bleibt im Contract für
spätere Quellen.

## 4. Keine gefährlichen Umkehrschlüsse

`nicht_erforderlich` nur, wenn ein Dokument es **wörtlich** sagt. Unterhalb der
Eingangsschwelle schweigt Tabelle 6 ⇒ `review_required` in diesen Fällen:

| Zeile | nicht abgedeckt |
|---|---|
| 1.1 / 1.2 | Gebäude der GK 1, 2, 3 |
| 3 | ≤ 10 Betten |
| 3 + 7.9.12 | Schutzhütte < 30 Schlafplätze |
| 4 | ≤ 200 m² Verkaufsfläche |
| 5.1 | ≤ 60 Verabreichungsplätze |
| 6 | ≤ 10 Betten |
| 9.1 | Räume für ≤ 60 Personen bestimmt |
| 9.2 | ≤ 120 Personen |
| 10 | ≤ 200 m² Netto-Grundfläche |
| 11.1 | ≤ 250 m² Nutzfläche (RL 2.2 Kap. 2/3 schweigen dazu) |
| 11.2 | ≤ 1.600 m² |
| — | `NICHT_IN_TABELLE_6`, `VERKEHRSEINRICHTUNG`, `jurisdiction` unklar, Pflichtfakt `None` |

Ohne Lücke nach unten (kein Review nötig): Zeilen 2, 5.2, 7, 8, 12.1, 12.2.

## 5. Ownership

| Feld / Wissen | Owner |
|---|---|
| `jurisdiction`, `bundesland`, `projekt_stichtag`, `arbeitsstaette_nach_aschg` | Hauptengine / Projektinput (später LB-Parser) |
| `nutzungsart`, `gebaeudeklasse`, `fluchtniveau_m`, alle Flächen- und Zählfelder | Hauptengine / Projektinput (später LB-Parser) |
| `lage_zur_wohnung` | Projektinput; Vorbelegungs-Kandidat aus `Raum.ist_communal` (Semantik ≠ identisch) |
| Rohflächen, `raum_ids`-Werte, Fluchtweg-/Ausgangs-Topologie | Selman / Raumerkennung |
| **Alle Schwellenwerte** (10/16/60/100/120/200/240/250/1.600/3.000/3.200/5000; 22 m, 32 m; 30 Schlafplätze) | **Enis / Normwissen** |
| Zeilenauswahl, Stufenlogik, Review-Regeln, Ausführungsverweise | **Enis / Normwissen** |

Merksatz: **Projektinput sagt, *was gebaut wird*; Normwissen sagt, *was das
bedeutet*.** Keine Norm-Zahl in den Projektinput.

## 6. Konkrete Änderungen (Leonis)

Empfehlung: **zwei neue Contract-Module**, `RaumModell` und `NormRegelwerk` bleiben
unverändert auf 1.0.0.

| Datei | Änderung |
|---|---|
| `src/notbeleuchtung/hauptengine/contracts/projekt_kontext.py` | **neu** — `ProjektKontext`, `Gebaeudeteil`, Enums |
| `src/notbeleuchtung/hauptengine/contracts/oib_ergebnis.py` | **neu** — `OibStufe`, `OibErgebnis`, `OibBefund` |
| `src/notbeleuchtung/hauptengine/contracts/__init__.py` | Re-Exports + `SCHEMA_MODELS["projekt_kontext"|"oib_ergebnis"]` |
| `.../contracts/schema/*.json` | `python scripts/gen_schema.py` (sonst bricht `tests/contract/test_schema_drift.py`) |
| `.../contracts/ports.py` | `NormProvider` um `oib_stufe(kontext) -> OibBefund` **oder** eigenes `OibProvider`-Protocol |
| `.../hauptengine/pipeline.py` | `run()` um `projekt: ProjektKontext \| None` |
| `tests/fakes.py`, `tests/fixtures/` | Fake-Projektkontext + Golden-Fixture (Fake-first) |
| `tests/contract/` | neue Naht-Invariante `raum_ids ⊆ raeume[].id` |
| `docs/CONTRACTS.md`, `docs/PROGRAMM_NOTBELEUCHTUNG.md` | Contract-Version-Tabelle + zwei Zeilen |

`CODEOWNERS`: `/src/notbeleuchtung/hauptengine/contracts/` = `@mvpo3 @EnisAMG
@polatselman` ⇒ PR braucht alle drei Approvals.

**Warum nicht `RaumModell` erweitern:** dessen Docstring sagt ausdrücklich „Reines
Geometrie-/Topologie-Ergebnis … KEIN Norm-Urteil"; Nutzung/Gebäudeklasse/
Fluchtniveau sind nicht geometrisch und für Selman nicht lieferbar. Außerdem ist
`RaumModell` geschoßweise.
**Warum nicht in `NormRegelwerk`:** das ist der Ausgabe-Contract Norm → Engine; der
Projektkontext läuft in die Gegenrichtung.

**Zwei Fragen an Leonis:**
1. ~~Methode auf `NormProvider` oder eigenes `OibProvider`-Protocol?~~
   **Beantwortet (PR #14): eigenes `OibProvider`-Protocol.**
2. Brauchen wir mittelfristig ein `GebaeudeModell` (mehrgeschoßige Kennzahlen)?
   **Weiterhin offen** — siehe Abschnitt 0.

**Erledigt durch PR #14:** `projekt_kontext.py`, `oib_ergebnis.py`, `__init__.py`,
Schemas, `ports.py` (`OibProvider`), `tests/contract/`. **Noch offen:**
`pipeline.py` (`run()` ohne `projekt`-Parameter), `ProviderBundle` (kein
`oib`-Feld), Fake-Projektkontext in `tests/fakes.py`.

## 7. Beispiel

Wohngebäude GK 5, Fluchtniveau 18 m, mit Tiefgarage als gemischter Nutzung:

```json
{
  "contract": "ProjektKontext",
  "contract_version": "1.0.0",
  "jurisdiction": "AT",
  "bundesland": "W",
  "projekt_stichtag": "2026-08-30",
  "arbeitsstaette_nach_aschg": null,
  "gebaeudeteile": [
    {
      "id": "gt_wohnen", "bezeichnung": "Wohnteil Bauteil A+B",
      "nutzungsart": "WOHNGEBAEUDE", "gebaeudeklasse": "GK5",
      "fluchtniveau_m": 18.0, "lage_zur_wohnung": "AUSSERHALB_WOHNUNG",
      "netto_grundflaeche_m2": null, "verkaufsflaeche_m2": null,
      "nutzflaeche_garage_m2": null, "betten_anzahl": null,
      "schlafplaetze_anzahl": null, "verabreichungsplaetze_anzahl": null,
      "personen_anzahl_bestimmt": null,
      "floors": ["EG","1OG","2OG","3OG","4OG"],
      "raum_ids": ["stgh_a","stgh_b"]
    },
    {
      "id": "gt_garage", "bezeichnung": "Tiefgarage UG1",
      "nutzungsart": "GARAGE", "gebaeudeklasse": null, "fluchtniveau_m": null,
      "lage_zur_wohnung": null, "netto_grundflaeche_m2": null,
      "verkaufsflaeche_m2": null, "nutzflaeche_garage_m2": 980.0,
      "betten_anzahl": null, "schlafplaetze_anzahl": null,
      "verabreichungsplaetze_anzahl": null, "personen_anzahl_bestimmt": null,
      "floors": ["UG1"], "raum_ids": ["garage_ug1"]
    }
  ]
}
```

Antwortform — **alle Normergebnisse Platzhalter**, der Resolver existiert noch nicht:

```json
{
  "contract": "OibBefund", "contract_version": "1.0.0",
  "ergebnisse": [
    {
      "gebaeudeteil_id": "gt_wohnen",
      "stufe": "<durch OIB-Resolver zu bestimmen>",
      "zeile": "<durch OIB-Resolver zu bestimmen>",
      "quelle": "OIB-Richtlinie 2, Punkt 5.4 i.V.m. Tabelle 6",
      "norm_ausgabe": "Ausgabe Mai 2023 (OIB-330.2-029/23)",
      "fundstelle_seite": "Norm-S. 32 / PDF-S. 34",
      "angewandter_schwellenwert": "<durch OIB-Resolver zu bestimmen>",
      "eingangswerte": {"nutzungsart":"WOHNGEBAEUDE","gebaeudeklasse":"GK5","fluchtniveau_m":"18.0","lage_zur_wohnung":"AUSSERHALB_WOHNUNG"},
      "fehlende_fakten": [], "hinweise": ["<durch OIB-Resolver zu bestimmen>"],
      "ausfuehrungs_verweise": ["<durch OIB-Resolver zu bestimmen>"]
    },
    {
      "gebaeudeteil_id": "gt_garage",
      "stufe": "<durch OIB-Resolver zu bestimmen>",
      "zeile": "<durch OIB-Resolver zu bestimmen>",
      "quelle": "OIB-Richtlinie 2, Tabelle 6 (i.V.m. OIB-Richtlinie 2.2 Punkt 5.5.3)",
      "norm_ausgabe": "Ausgabe Mai 2023",
      "fundstelle_seite": "Norm-S. 32 / PDF-S. 34; RL 2.2 PDF-S. 7",
      "angewandter_schwellenwert": "<durch OIB-Resolver zu bestimmen>",
      "eingangswerte": {"nutzungsart":"GARAGE","nutzflaeche_garage_m2":"980.0"},
      "fehlende_fakten": [], "hinweise": ["<durch OIB-Resolver zu bestimmen>"],
      "ausfuehrungs_verweise": ["<durch OIB-Resolver zu bestimmen>"]
    }
  ],
  "nicht_zugeordnete_raum_ids": []
}
```

## 8. Was Enis danach baut

`normwissen/data/oib_rl2_tabelle6.yaml` (20 Zeilen mit Schwellenwerten, Fußnoten,
Fundstelle, Seite) · Resolver `normwissen/oib/` (ProjektKontext → OibBefund) ·
Review-Regeln aus Abschnitt 4 als harte Vorgabe · Ausführungsverweise als zitierte
Konstanten. Erst danach die Verzahnung mit EN 1838: die OIB-Stufe entscheidet, **ob
und in welchem Umfang** EN 1838 anzuwenden ist, EN 1838 entscheidet die Lichtwerte.
