# Vom Lernpaket zur überprüfbaren Umsetzung

Dieses Paket bündelt den aktuellen, korrigierten EG-Stand. Es enthält die fachlichen Unterlagen und Originalpläne. Die produktive Rivoplan-Engine wird im bereits vorhandenen Repository untersucht und bearbeitet; sie ist nicht Bestandteil dieses Archivs.

## Einstieg

Den gesamten ZIP-Ordner entpacken und Claude Code Zugriff darauf sowie auf das Repository geben. Mit `CLAUDE_STARTPROMPT_EG.md` beginnen. Alle Pfade in den Unterlagen beziehen sich auf den entpackten Paketordner.

## Lesereihenfolge und Zweck

| Schritt | Dateien | Zweck |
|---|---|---|
| 1 | `00_START_HIER.md`, `02_CLAUDE_AUFTRAG_EG.md`, `11_DATENVERTRAG_EG.md` | Ziel, Koordinaten, Bedeutung der Daten und Umsetzungsvorgehen verstehen. |
| 2 | `Leopold_Kohr_Schule_EG_Lernbuch_final.pdf`, `01_LERNWISSEN_EG.md` | Alle 39 Seiten und 29 Originalbeispiele lesen und visuell ansehen. |
| 3 | PDFs unter `plaene/` | Rote Mauern, grüne Bodenflächen, saubere Planbasis und scharfe Vektordetails vergleichen. |
| 4 | `daten/03_REGELN_EG.json`, `daten/04_BEISPIELE_EG.json`, `daten/13_BILDANNOTATIONEN_EG.json` | Regeln mit ihren Belegen, Rahmen, Pfeilen und Originalstellen verbinden. |
| 5 | `daten/05_PRUEFFAELLE_EG.json` | 20 noch nicht ausgeführte Spezifikationen in passende Engine-Tests überführen. |
| 6 | Originale unter `quellen/`; Quellen-, Text- und Layerdaten unter `daten/` | Tatsächliche DXF-Geometrie, Einheiten, Handles und nahe Beschriftungen prüfen. |
| 7 | Markierungs- und Herkunftsdateien unter `daten/` | Rote Konturen, grüne Flächen sowie Einbau- und Möbelumrisse nachvollziehen; ihre dokumentierten Grenzen beachten. |
| 8 | `daten/07_TREPPEN_UEBERGABE_EG.json`, `09_OFFENE_PUNKTE_EG.md` | Treppeninstanzen und ungeklärte Höhen bzw. Anschlüsse berücksichtigen. |
| 9 | `14_AENDERUNGEN_UND_GEHFLAECHEN.md` bis `17_VEKTOREXPORT.md`, Nutzerkorrekturen unter `daten/` | Bisherige Korrekturen erhalten und die aktuelle Vektorfassung verwenden. |

`DATEIUEBERSICHT_EG.md` listet die tatsächlich enthaltenen Dateien. `MANIFEST.json` und `PRUEFSUMMEN.txt` binden den ausgelieferten Stand an seine Prüfsummen. `PRUEFUNG.json` dokumentiert die Paketprüfung. Das Bestehen dieser Prüfung besagt, dass das Paket konsistent ist; Erkennungsergebnisse werden erst mit der Engine geprüft.

## Fachliche Prioritäten

1. **Wände und Hindernisse:** Materialband, beide Wandseiten und Anschlüsse erkennen. Auch breite Außenaufbauten, dünne Trennwände, schräge Mauern und Stützen berücksichtigen. Ein Pfeil oder Rahmen im Lernbuch ist kein CAD-Bauteil.
2. **Öffnungen:** Türblatt, Schwenkbogen, Zarge und Beschriftung zusammen lesen. Fensterbögen nicht allein als Türen klassifizieren. Schiebetüren benötigen keinen Drehbogen. Mehrere Flügel können ein gemeinsames Portal bilden.
3. **Raumgrenzen:** Deckenlinien, Texte, Möbel und technische Einbauten korrekt einordnen. Nahe Beschriftungen als Beleg nutzen und mit der Form vergleichen. Ein bloßes Rechteck ist kein ausreichender Raum- oder Wandnachweis.
4. **Verbindungen:** Eine Öffnung muss tatsächlich durch den Wandaufbau führen und auf beiden Seiten an einen belegten Bereich anschließen. Keine Verbindungen durch feste Wand- oder Glasflächen erzeugen. Eine Sackgasse kann betretbar sein, ohne einen zweiten Ausgang zu besitzen.
5. **Treppen und Lift:** Stufen zu Läufen und Podesten zusammenfassen. Treppenbrüche nicht als Mauern werten. Keine Geschosshöhe aus der Blattrichtung erfinden. Kabine, Schacht und technischer Zwischenraum bleiben getrennte Objekte.

Welche Fehlerklasse zuerst bearbeitet wird, bestimmt der reproduzierte Ausgangsfehler im vorhandenen Code. Bestehende korrekte Erkennung muss erhalten bleiben.

## Nachweis pro Änderung

Für jeden bearbeiteten Fehler dokumentieren:

- Regel-ID, Beispiel-ID, Prüffall-ID und relevante Originalstelle.
- Erwartete Erkennung sowie tatsächlicher Ausgangsbefund.
- Verantwortlicher Verarbeitungsschritt und geänderte Dateien/Funktionen.
- Tatsächlicher Startbefehl, Eingabeprüfsumme, Codeversion und Konfiguration.
- Ergebnis vor/nach der Änderung mit Zwischendaten und Overlay.
- Ausgeführte Tests und deren Ergebnis; nicht ausgeführte Fälle mit Grund kennzeichnen.
- Verbleibende Unsicherheit und nächster sinnvoller Schritt.

Wand- und Portalgrenzen müssen bei geometrischen Tests am Original geprüft werden. Die gelieferten Erklärrahmen und Suchbereiche sind dafür keine millimetergenaue Sollmaske. Die mitgelieferten Testtexte bleiben unveränderte Spezifikationen; echte Laufresultate gehören in einen separaten Ergebnisbericht.

## Abschluss der Claude-Code-Sitzung

Die Übergabe soll verständlich beantworten: Was wurde gelesen? Wo liegt der betroffene Code? Was wurde umgesetzt? Was hat sich nachweisbar verbessert? Was ist noch offen? Mit welchem Befehl und Arbeitsstand kann die nächste Sitzung fortsetzen?
