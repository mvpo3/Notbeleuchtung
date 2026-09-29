# Dateiwegweiser

Alle Pfade in der Tabelle sind relativ zum Paketordner.

| Datei/Ordner | Zweck |
| --- | --- |
| `START_HIER.md` | Schneller Einstieg, Befehle und Grenzen |
| `CLAUDE.md` | Projekt- und Arbeitsregeln für Claude Code |
| `PROMPT_FUER_CLAUDE_CODE.md` | Vollständiger Auftrag: einlesen, echter Lauf, Fehler beheben, vergleichen |
| `pdf/2OG_Lernbuch.pdf` | Freigegebene 36 Seiten, unverändert |
| `pdf/2OG_Mauern_rot.pdf` | Rote Lernkonturen im großen Originalformat |
| `pdf/2OG_Gehflaechen_gruen.pdf` | Grüne Bodenflächen im großen Originalformat |
| `pdf/2OG_Architekturbasis.pdf` | Vektorplan mit ausgeblendeten elektrischen Überlagerungen und alter Revisionswolke |
| `pdf/2OG_Erklaerte_Details.pdf` | 25 reine Detailpanels mit 100 Rahmen und Pfeilen |
| `quellen/` | Unveränderte Original-PDF und Original-DXF |
| `wissen/01_...` bis `wissen/07_...` | Erkennungswissen und Gegenbeispiele |
| `wissen/08_...` bis `wissen/12_...` | Daten, Umsetzung, Abnahme, Grenzen und parallele Arbeit |
| `wissen/13_ALLE_BEISPIELE.md` | Vollständiger Text sämtlicher Lernbeispiele |
| `daten/01_QUELLEN.json` | Freigabestand, Quellen-Hashes und Dateibindung |
| `daten/02_KOORDINATEN.json` | Einheiten, Ursprung und DXF/PDF-Transformation |
| `daten/03_BEISPIELE.json` | Beispielindex, Ausschnitte, Seiten, Bilder und Fachtexte |
| `daten/04_ANNOTATIONEN.json` | Benannte Erklärungen und Pfeilziele |
| `daten/05_ERKLAERRAHMEN.geojson` | 100 geschlossene Erklärrahmen, keine Objektkonturen |
| `daten/06_WAND_LERNKONTUREN.geojson` | Visuelle Materialumrisse |
| `daten/07_BODEN_LERNFLAECHEN.geojson` | Interpretierte Bodenfüllung |
| `daten/08_FLAECHEN_HERKUNFT.geojson` | Manuelle Bereiche und ausgeschlossene Sonderflächen |
| `daten/09_EINBAU_REFERENZEN.geojson` | Erfasste geschlossene Einbaukonturen |
| `daten/10_WAND_HERKUNFT.json` | Herkunft und Grenzen der Materialheuristik |
| `daten/11_PRUEFFAELLE.json` | 25 noch nicht an einer Engine bewertete Fälle |
| `daten/12_TREPPEN_UND_HOEHEN.json` | Vier Treppenbeispiele und nicht bestätigte Anschlussgeschosse |
| `daten/13_OFFENE_PUNKTE.json` | Konkrete noch offene Fragen |
| `daten/14_KLASSEN_UND_REGELN.json` | Bauteilklassen, Beleganforderungen und Wegwirkung |
| `daten/15_LAUFZEIT.json` | Tatsächlich verwendete Python-/Paketversionen |
| `daten/roh/` | Vollständige extrahierte Texte, Linien und Ellipsen sowie Buchrohdaten |
| `bilder/` | 25 Detail-PNGs und zwei Übersichten für visuelles Einlesen |
| `schemata/ERKENNUNGSERGEBNIS.schema.json` | Austauschformat für den späteren Versuch |
| `vorlagen/` | Leeres Ergebnis, BEFUND.md und OFFEN.md |
| `skripte/pruefe_paket.py` | Dateiintegrität und interne Verweise prüfen |
| `skripte/zeige_beispiel.py` | Ein Beispiel samt nahe liegenden Originaltexten ausgeben |
| `skripte/pruefe_erkennung.py` | Ergebnisformat und Objektverweise prüfen, keine Qualitätsbewertung |
| `skripte/reproduziere.py` | Lernansichten aus den Originalquellen erneut aufbauen |
| `skripte/extrahiere_dxf.py` | Original-Entities in Suchdaten ausgeben |
| `skripte/bereite_geometrie_vor.py` | Material-/Einbau-Lernreferenzen vorbereiten |
| `skripte/baue_lernbuch.py` und `skripte/lessons.py` | Geschossspezifische Lernansichten rekonstruieren |
| `skripte/fonts/` | Verwendete Schriftdateien und Lizenz |
| `requirements.txt` | Exakte verwendete Abhängigkeiten |
| `MANIFEST.json`, `PRUEFSUMMEN.txt`, `PRUEFUNG.json` | Dateiverzeichnis, Hashes und tatsächlicher Paketprüfbericht |

Die großen Plan-PDFs unter `pdf/` verwenden dieselben Farben wie das Lernbuch. Die Legende und Bedeutungsgrenzen stehen auf Buchseite 3. Für Nahansichten die Vektor-PDFs verwenden; PNGs sind Zusatzansichten.

Die Original-DXF und vollständigen Rohlisten gezielt mit Skripten oder Dateisuche durchsuchen, nicht komplett als Chattext laden. `zeige_beispiel.py` verbindet Beispiel, Quellenposition und Originalbeschriftung.
