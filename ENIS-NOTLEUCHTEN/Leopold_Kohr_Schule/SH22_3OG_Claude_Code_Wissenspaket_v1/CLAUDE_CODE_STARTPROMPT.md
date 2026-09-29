# Auftrag an Claude Code: SH22 3. OG in die Raumerkennung integrieren

Arbeite mit dem vollständig entpackten Ordner `SH22_3OG_Claude_Code_Wissenspaket_v1`. Ziel ist, das darin erklärte Architekturwissen in die vorhandene Raumerkennung umzusetzen und am tatsächlichen Softwareergebnis zu prüfen. Liefere keine bloße Inhaltszusammenfassung.

## Zuerst verbindlich lesen und prüfen

1. Lies die aktuell geltenden `AGENTS.md`, `CLAUDE.md`, Status-, Architektur- und Zuständigkeitsdateien im tatsächlichen Zielrepository. Ermittle Branch, HEAD und Arbeitsbaum; bewahre fremde Änderungen. Verwende bestehende Schnittstellen und Projektresolver. Dieses Paket ersetzt keine Repository-Anweisung.
2. Lies `00_START_HIER.md`, `03_Wissen/UMSETZUNGSPLAN.md`, `03_Wissen/DATENVERTRAG.md`, `03_Wissen/FREIE_BODENFLAECHE.md`, `03_Wissen/TEXT_UND_HOEHE.md`, `03_Wissen/VISUELLE_AUSGABE.md` und `05_Pruefung/ABNAHME.md`. Für die Adapterfelder nutze `05_Pruefung/CLAIMS_MESSANLEITUNG.md` und `claims_woerterbuch.json`.
3. Führe die offline arbeitende Paketprüfung aus: `python3 06_Werkzeuge/pruefe_paket.py`. Bei fehlerhaften Prüfsummen keine abweichende Quelle stillschweigend verwenden.
4. Lies `04_Daten/lernbeispiele.json` und `04_Daten/erkennungsregeln.json` vollständig. Nutze `03_Wissen/Beispiele/` und die angegebenen PDF-Seiten, wenn ein Detail vertieft werden muss. Lies die 32 Beispiele vor einer globalen Änderung; sie enthalten gezielte Gegenbeispiele.
5. Prüfe den Originalinput in `02_Originale/`. Die PDF hat weitgehend in Kurven aufgelöste Planbeschriftungen; für lesbaren Text die zugehörige DXF verwenden. Erhalte dort auch den räumlichen Bezug. Alte bekannte Laufzahlen oder Dateipfade nicht als aktuellen Repostand behaupten.

## Konkrete Umsetzung

- Ordne Text, Linien, Kurven, Schraffuren, Blöcke und Höhen zuerst ihren Funktionen zu. Ein Layername oder ein einzelner Bogen entscheidet nicht allein über die Klasse.
- Erfasse Wandkörper flächig; unterscheide massive Wände, dünne Kabinenplatten, Brüstungen und Absturzsicherungen. Quelle, Konstruktion und Material getrennt behandeln.
- Zerlege Türen und Fenster in Blatt/Flügel, Drehpunkt, Bogen, Rahmen/Laibung, lichte Öffnung sowie zugehörige Maße und Höhen. Ein Bogen erzeugt weder automatisch eine Tür noch ein massives Viertelkreis-Hindernis.
- Verbinde Bodenflächen nur über eine belegte Öffnung mit passendem Bodenanschluss. Fenster mit Brüstung, Schacht, feste Wand und Absturzsicherung bleiben ohne normalen Durchtritt. Ungeklärte Verbindungen nicht künstlich reparieren.
- Trenne bauliche Raumfläche, Nutzungszone, freie Bodenfläche, benutzerspezifischen Bewegungsraum und Route. Markiere alle freien Teilflächen, Nischen und Aufweitungen grün, einschließlich der belegten freien Zwischenräume zwischen Möbeln.
- Erkenne Möbel, Sanitär, Treppen, Lift, Schacht-/Wartungsbereiche und Gefälle anhand der erklärten Kombinationen. Betrachte die Originaltexte „Ablauf“, „Absturzsicherung raumhoch“, „Garderobe“, „Schachtleiter“ und die Höhenbezüge als konkrete Belege mit geprüfter Zuordnung.
- Treppen benötigen Lauf, Podest, Darstellungsbruch und Richtungsbeleg. Blatt-Richtung, aufwärts/abwärts, relative Höhendifferenz und Zielgeschoss getrennt halten. Kein Zielgeschoss ohne Beleg erfinden.
- Für jede Klassifikation speichern: beobachtete Merkmale, Originalfundstelle, Begründung, Gegenprüfung, offene Eigenschaften, Modellwirkung. Unbekannt bleibt unbekannt.

## Vorgehen und Nachweis

Erstelle nach dem Repository-Abgleich eine kurze Liste der wirklich betroffenen Module. Messe den bisherigen Stand am SH22-Originalinput, soweit die aktuellen Repository-Regeln diesen Lauf erlauben. Setze dann zusammengehörige, überprüfbare Änderungen um: zuerst Evidenz/Text und Wand/Öffnung, dann Boden/Topologie, danach weitere Klassen. Arbeite selbstständig bis zum tatsächlichen Repository-Gate.

Erstelle einen Adapter, der die **tatsächlichen Engine-Ergebnisse** in die Struktur von `05_Pruefung/ergebnis_vorlage.json` übersetzt. Der Adapter darf keine Sollwerte aus `akzeptanzfaelle.json` übernehmen und keine Fälle als bestanden ausgeben, nur weil die Regeln eingelesen wurden. Verweise pro Behauptung auf konkrete Engine-Objekte und Originalbelege. Nicht ausgeführte Fälle bleiben `not_run`.

Führe danach `python3 06_Werkzeuge/pruefe_erkennung.py <tatsaechlicher_ergebnisbericht.json>` aus. Das prüft den bereitgestellten Bericht, ersetzt aber keine unabhängige Geometrie- und Sichtprüfung. Ergänze einen vollständigen Overlay-Plan und die Detailausschnitte der 32 Fälle. Verwende direkte farbige Bauteillinien und Pfeile; keine zusätzlichen Objektkästen. Halte die aktuellen maßlichen Baselines und weitere Pläne getrennt fest.

Zum Abschluss liefern: geänderte Module, neue Entscheidungslogik, vorher/nachher ausgewertete Fälle, Test- und Sichtprüfergebnis, offene Fälle, Originalhashes, tatsächlichen Branch/Commit und reproduzierbare lokale Befehle. Behaupte keine erfolgreiche Umsetzung, wenn nur Dokumentation oder ein noch leerer Adapter vorliegt.

Die Notleuchtenplatzierung und normative Regelwerte sind nicht Gegenstand dieses Pakets. Bestehende Zuständigkeiten, Freigaben und Einschränkungen des aktuellen Repositories beachten; dieses Paket erteilt kein neues Push-/Merge- oder Veröffentlichungsrecht.
