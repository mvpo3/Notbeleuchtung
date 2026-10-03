# Am Rain - Prüfdurchgänge (23.09.2026)

## Aktueller Fach- und Darstellungsdurchgang – ausdrücklich unvollständiger Lernbuch-Teilstand

Die geprüfte Zusammenführung `01_PDF/Am_Rain_Notbeleuchtungen_zeichnen_RIVO_TEILSTAND_v1.pdf` hat 118 Seiten mit zehn Lesezeichen. Sie enthält sechs separate A3-CAD-Diagnosen und individuell bebilderte Kapitel für 37 EG-Kandidaten und 37 Kandidaten aus OG1–OG4. `FALLREGISTER.json` verbindet alle 74 Fallseiten mit ID/Bild/PDF/Quell-Handle: 49 davon haben im CAD einen RIVO-RZ-Block, 25 behalten ein offenes Original-SL-Symbol; technische Einzelnachweise: 0. Der OG-Registerabgleich hat 37 IDs, Handles, PDF-Seiten und bearbeitete DXF-Hashes geprüft, während alle 250 nicht-OG-Datensätze unverändert blieben (`05_Pruefung/OG1_OG4_REGISTER_MERGE_QA.json`). Daneben enthält die PDF 13 **vorläufige** UG-Fallnotizen zu 13 von 203 Leuchten-/unklaren UG-Kandidaten; zehn Versorgungseinträge sind davon getrennt. Die übrigen 190 UG-Kandidaten haben noch keine Notiz. Die 13 Notizen erfüllen selbst noch nicht die geforderte vollständige Einzelbegründung und sind nicht als „individuell erklärt“ verbucht. Es gibt keine vollständige geschossübergreifende Fluchtwegkette und keine Abschluss-PDF mit dem bestellten Endtitel.

Alle 118 Seiten der Zusammenführung wurden gerendert; zehn Kontaktbögen wurden visuell gesichtet, die Seiten 1, 60, 106 und 117–118 zusätzlich in voller Rendergröße. Die Einzelkapitel wurden zuvor separat seitenweise gerendert und nach den jeweiligen Kapitelberichten beurteilt. Die Schriften/Symbole in den geprüften Stichproben waren lesbar; die weitläufigen Diagnoseübersichten sind nur Orientierung. `05_Pruefung/GESAMT_PDF_TEILSTAND_V1_SICHTPRUEFUNG.md` nennt Methode und Grenze. Ein Kontaktbogen ersetzt keine Vollgrößenkontrolle jeder Seite. Die EG-Erklärungs-DXF wurde wieder geöffnet und auditiert; UG-/OG-Erklärungs-DXFs fehlen noch.

Die lokale Normnachprüfung nennt tatsächlich gelesene Ausgaben und Abschnitte in `04_Daten_und_Quellen/NORMEN_NACHPRUEFUNG_20260923.md`. ÖNORM EN 1838:2019-11 ist lokal vorhanden, OVE E 8101 wurde 2019 und 2025 unterschieden, OIB 2.2:2023 nur bedingt auf eine belegte Garage bezogen. EN 50172 und der Grundtext von R 12-2 wurden lokal nicht als Volltext belegt. Keine dieser Quellen belegt ohne Raum-/Weg-/Montage-/Photometriedaten die technische Richtigkeit jeder Am-Rain-Position. Licht-, Sicht- und Versorgungsnachweise bleiben offen. Der Vergleich mit der Mollgasse-Vorlage bezieht sich auf Gestaltung und Erklärungsperspektive, nicht auf eine übernommene Planungsregel.

Die zusätzliche `02_DXF_RIVO/Am_Rain_Notbeleuchtungsplaene_Alle_Geschosse_RIVO_Zusammenfuehrung_TEILSTAND_v2.dxf` ist eine abgeleitete Modellbereichs-XREF mit sechs vollständigen, gleichförmig verschobenen Quellen. Sie wurde wieder geöffnet und mit 0 Auditfehlern geprüft. Die genaue Rücktransformation steht in `05_Pruefung/ZUSAMMENFUEHRUNG_XREF_TRANSFORMATIONEN_TEILSTAND_v2.json`. Sie ist **nicht eigenständig**: alle sechs Einzelkopien müssen im selben Ordner bleiben. Papierbereich-Layouts befinden sich nur dort. Durch Modellregionen im Abstand von rund 35 km ist Gesamt-Zoom keine lesbare Gebäudeübersicht. Eine native CAD-Viewer-Prüfung der aufgelösten XREFs ist offen.

Die sechs Originale, RIVO-Bibliothek und weiteren im `INPUT_MANIFEST.json` aufgeführten lokalen Quellen wurden per SHA-256 nachgeprüft. Bei sieben ergänzenden Mollgasse-DXFs wurde der Hash erst nach der diagnostischen Sichtung in das Manifest aufgenommen; ein prälekturaler Hash ist dort nicht nachträglich behauptet. Der Git-Arbeitsbaum mit vorbestehenden Fremdänderungen blieb unberührt; kein Commit oder Push. Ein O/0-Erfolg für tatsächliche betriebliche Kennungen wird mangels belegter Rohkennungen nicht behauptet.

Ein eigener Register-Prüfdurchgang hat die zehn `Versorgungsobjekt`-Zeilen von missverständlichen „Symboltausch offen“-/„Einzelerklärung ausstehend“-Statuswerten auf „für Leuchten nicht anwendbar“ gesetzt. Ihre separate Versorgungsprüfung bleibt offen. Alle 277 Nicht-Versorgungszeilen blieben unverändert; Backup und Hashvergleich stehen in `05_Pruefung/VERSORGUNGSSTATUS_REGISTER_QA.json`. `SYMBOL_MAPPING.json` hatte diese zehn Einträge bereits als `NOT_A_LUMINAIRE` geführt.

## CAD-Prüfdurchgang 2 - proportionale RIVO-Regel und sechs Teilstände

Die neue Größenregel wurde zunächst an einer kleinen bearbeitbaren DXF mit den vier tatsächlich vorhandenen `STANDARD_RZ_*`-/`RIVO_ARR_*`-Paaren geprüft und das Ergebnis erneut geöffnet (0 Auditfehler/0 Fixes). Die sichtbare Originalgrafik wurde ohne ATTDEF und separate QR-Grafik, die vollständige RIVO-Piktogrammgrafik einschließlich funktionsbezogener Elemente in lokalen Blockachsen gemessen. Bei einseitigen Schildern wurde der grafische Original-INSERT am oberen Rahmenrand, bei der beidseitigen Grafik am mittleren Bezug festgehalten; der RIVO-Bibliotheksursprung liegt weit vom sichtbaren Schild entfernt und wurde rechnerisch korrigiert. Das ist ein **grafischer**, nicht unabhängig nachgewiesener realer Montagepunkt. Die funktionsgleiche lokale Pfeil-/Seitenzuordnung der vier Standard-Paare wurde anhand der echten Blockrenderings und der RIVO-Varianten in jeweils vorhandenen Grundrissdrehungen visuell geprüft. Keine Quelle wurde verzerrt oder verschoben.

Danach wurden sechs vollständige Kopien mit Suffix `_RIVO_Symbole_TEILSTAND_v2.dxf` erzeugt. Wirklich ersetzte `STANDARD_RZ_*`-Modell-Darstellungen: UG 46, EG 26, OG1 6, OG2 8, OG3 7, OG4 2, gesamt **95**. Die restlichen **182** funktional ungeklärten Darstellungen/Kandidaten aus sieben Familien blieben original; zehn Versorgungsobjekte wurden nicht als Leuchten getauscht. Diese Bilanz beschreibt Darstellungen, **keine bestätigten physischen Leuchten**. Im UG wurden trotz 62 geometrischer Paarhypothesen 0 physische Dubletten als gesichert abgezogen. Alle Ergebnis-DXFs enthalten weiterhin die ursprünglichen Planköpfe, Layoutnamen, Koordinatenbereiche und nicht betroffenen Instanzen. Der alte Quellblock darf als unbenutzte Definition verbleiben, aber keine erfolgreich ersetzte `STANDARD_RZ_*`-Modellinstanz blieb stehen.

| Geschoss | registrierte Leuchten-/unklare Kandidaten | proportional ersetzt | offen im Original | Versorgung, separat |
|---|---:|---:|---:|---:|
| UG | 203 | 46 | 157 | 10 |
| EG | 37 | 26 | 11 | 0 |
| 1. OG | 9 | 6 | 3 | 0 |
| 2. OG | 13 | 8 | 5 | 0 |
| 3. OG | 12 | 7 | 5 | 0 |
| 4. OG | 3 | 2 | 1 | 0 |
| **Gesamt** | **277** | **95** | **182** | **10** |

„Registriert“ und „ersetzt“ beziehen sich auf CAD-Instanzen/Darstellungen. Das Register enthält somit 287 Datensätze einschließlich Versorgung; eine deduplizierte physische Leuchtenstückzahl ist noch nicht belegt.

**Kennungsprüfung:** Die 287 untersuchten Modell-INSERT-Datensätze enthalten in den erfassten Kennungsattributen keine belegte individuelle Roh-Leuchtenkennung (`original_label_raw` in allen Fällen leer). Daher wurde keine betriebliche Kennung erfunden oder pauschal `O` durch `0` ersetzt; `BESCHRIFTUNGS_AENDERUNGEN.csv` bleibt leer. `AR-EG-...` und `AR-OG...` sind ausdrücklich Lehr-IDs. Eine zusätzliche gezielte Roh-DXF-Textsuche nach Mustern wie `EG OA1`/`EG 0A1` beziehungsweise OG/UG-Analogon ergab in den sechs Quelldateien keinen Treffer; sie ersetzt keine vollständige spätere Produktlistenabstimmung.

Für jede bearbeitete Datei wurde eine unveränderte DXF-No-op-Rundreise mit demselben ezdxf-Werkzeug erstellt. Der Vergleich nach erneutem Öffnen ergab jeweils 0 Unterschiede bei allen vorhandenen nicht betroffenen Layout-Entitäten und ursprünglichen Nicht-Layout-Blockdefinitionen, erhaltene Original-Handles, exakt erhaltene Produkt-ATTRIB-Texte/Positionen sowie genau eine separat erhaltene QR-Referenz je getauschtem Zeichen. Alle sechs DXF-Audits meldeten 0 Fehler/0 Fixes. Pro Handle sind Quell-/RIVO-Grafikmaße, Proportionalfaktor, Restabweichung, grafischer Quellbezug, Ziel-INSERT und Ankerfehler in `05_Pruefung/{G}_RIVO_TEILSTAND_V2_VERIFIKATION.json` dokumentiert. Erwarteter grafischer Positionsfehler war 0; gemessen <1e-7 Zeichnungseinheiten. Die sechs repräsentativen Variantenkontaktbilder aus den **Ergebnis-DXFs** wurden zusätzlich angesehen. Eine AutoCAD-Abnahme ist dies nicht.

Eine erneute Auswertung aller Papierbereiche der sechs **Originale** fand dort keine direkten INSERTs mit `STANDARD_RZ`, `STANDARD_SL`, `STANDARD_SPOT`, `SIMA` im Namen oder `FLUCHTWEG` im Layernamen. Die Papierbereiche enthalten Ansichtsfenster und andere Zeichnungsinstanzen; dieser gezielte Test ist kein Beweis, dass jeder verschachtelte anonyme Block funktionslos ist. In den 95 getauschten Modellinstanzen beträgt der höchste gemessene grafische Ankerfehler 2,91e-11 Zeichnungseinheiten. Durch die freigegebene proportionale Einpassung bleiben höchstens 1,641 Einheiten Breiten- und 7,120 Einheiten Höhenrest (maximal 0,251 % beziehungsweise 1,079 % der jeweiligen Quellabmessung); diese Restabweichung wird nicht als identische Breite/Höhe bezeichnet.

Der EG-V1-Schreibversuch und die rohe DXF-zu-DXF-Signaturprüfung wurden nicht freigegeben: ezdxf normalisiert beim Schreiben auch ohne Bearbeitung viele optionale Attribute. Der V1-Test liegt klar gekennzeichnet unter `05_Pruefung/Tests/`, der korrigierte Vergleich nutzt die No-op-Rundreise. Ursprüngliche Register liegen vor der Aktualisierung mit Prüfsumme unter `05_Pruefung/Backup_Vor_Proportionaler_Korrektur_20260923/`. Die alte dreiseitige Prüf-PDF und das alte ZIP wurden nicht überschrieben.

Noch **nicht bestanden bzw. offen**: Viewer-Prüfung aller tatsächlich gedruckten Layouts und der georeferenzierten UG-Zweitwelt, reale Montagebezüge, funktionale Deutung der sieben übrigen Symbolfamilien, physische Leuchtenzuordnung, vollständige individuelle Erklärungen aller Geschosse, normativer und lichttechnischer Nachweis sowie fertiges Gesamt-Lernbuch. `ENTSCHEIDUNGSBLATT_OFFENE_VARIANTEN_20260923.md` nennt die präzisen Variantenfragen. Keine 2019/2025-Normausgaben wurden als gleichrangige Bestandsprojekt-Grundlage vermischt.

## CAD-Prüfdurchgang 1 - historischer Befund vor der Größenkorrektur

## Bestand

Sechs freigegebene Original-DXFs wurden im bezeichneten Ordner und seinen Unterordnern gefunden: UG, EG, OG1, OG2, OG3, OG4. Alle wurden mit ezdxf geöffnet; Modellbereiche, Layouts, Layer, Blocknamen und DXF-Xref-Blockflags sind in `SOURCE_INVENTORY.json` erfasst. Kein DXF-Xref-Block wurde dabei gemeldet. Die ausdrücklich benannte EG-Datei war vorhanden und wurde nicht durch eine andere Revision ersetzt.

Das bisherige Kandidatenregister zählt pro Geschoss Modell-INSERTs, **nicht** bestätigte physische Leuchten:

| Geschoss | RZ-Kandidaten | SL-Kandidaten | Versorgung | ungeklärt | ersetzt |
|---|---:|---:|---:|---:|---:|
| UG | 101 | 97 | 10 | 5 | 0 |
| EG | 26 | 11 | 0 | 0 | 0 |
| OG1 | 6 | 3 | 0 | 0 | 0 |
| OG2 | 8 | 5 | 0 | 0 | 0 |
| OG3 | 7 | 5 | 0 | 0 | 0 |
| OG4 | 2 | 1 | 0 | 0 | 0 |

Die UG-Zahlen können Mehrfachdarstellungen enthalten. Versorgung ist nicht als Leuchte mitgezählt. Weitere aufgelöste/verschachtelte Kandidaten sind noch nicht ausgeschlossen.

## Symbol-/Geometrieprüfung

Die tatsächlichen Quell- und Bibliotheksblöcke wurden gerendert und die HATCH-/Kontur-Geometrie gemessen. QR-INSERT und ATTDEF sind bei der sichtbaren RZ-Rahmengröße ausdrücklich ausgeschlossen. Vorab wurde 0,01 Quell-Zeichnungseinheiten als Vergleichstoleranz gesetzt. Die kleine Test-DXF `05_Pruefung/Tests/Am_Rain_RZ_Groessen_Konflikt_Test.dxf` wurde erneut geöffnet: 0 Auditfehler, 0 Fixes. Bei proportionaler Breitenanpassung bleibt 2,739 Einheiten Höhenunterschied. Sie ist daher keine zulässige Serienvorlage.

Alle geprüften Zielzuordnungen stehen mit Maßen, Funktionsbefund und Offenstatus in `05_Pruefung/SYMBOL_MAPPING_GATE.json`. Kein Original und keine vollständige Geschosskopie wurde verändert oder als „ersetzt“ ausgegeben. Eine AutoCAD- oder unabhängige Fremdabnahme hat nicht stattgefunden.

## Fach- und Darstellungsprüfung

Eine vollständige Geschossverknüpfung, physische Deduplikation, 0/O-Kennungsprüfung, individuelle Normbegründung und vollständige PDF-Seitenprüfung ist **noch nicht durchgeführt**. Es gibt kein finales Haupt-PDF, keine geschossweisen Erklärungs-DXFs, keine bearbeiteten Geschosskopien und kein End-ZIP. Technischer Test und Symbolblatt dürfen damit nicht verwechselt werden.

Ein separater **vorläufiger** dreiseitiger CAD-Prüfzwischenbericht wurde als PDF erzeugt, alle drei Seiten zu PNG gerendert und visuell auf abgeschnittenen Text und Lesbarkeit kontrolliert. Er enthält keine individuellen Leuchtenerklärungen und keinen RIVO-bearbeiteten Gebäudeplan.

Zusätzlich wurde eine sechsseitige A3-Quell-CAD-Diagnose erzeugt. Ihre Seiten für UG, EG und OG1-OG4 wurden jeweils als PNG gerendert und einzeln angesehen. Sie zeigt nur unmittelbar im Modell gespeicherte Architektursegmente sowie Kandidatenpunkte; verschachtelte Bauteile, Texte, Ansichtsfenster und fachliche Verbindungen können fehlen. Der speicherintensive Vollrenderer wurde nach etwa 3,7 GB RAM ohne Ergebnis gestoppt. Eine georeferenzierte UG-Variante ließ sich mit den ausgewählten Direktsegmenten nicht darstellen. Diese Einschränkungen sind keine CAD-, Fluchtweg- oder Vollständigkeitsabnahme. Der Zwischenstand enthält somit neun visuell kontrollierte PDF-Seiten, aber weiterhin kein Lernbuch.
