# Vollständiges EG-Paket für Claude Code

Dieses Archiv enthält den aktuellen korrigierten EG-Stand der Leopold-Kohr-Schule: scharfe PDFs, Original-DXF, Lernwissen, Regeln, Beispiele, Markierungen, Prüffälle und Hilfsskripte.

## So beginnst du

1. Die gesamte ZIP-Datei entpacken.
2. Claude Code Zugriff auf diesen Ordner und auf das vorhandene Rivoplan-Repository geben.
3. Claude Code auffordern: **„Lies CLAUDE_STARTPROMPT_EG.md in diesem Paket und führe den Auftrag durch.“**

Der Auftrag führt vom vollständigen Einlesen über einen belegten Ausgangslauf zur gezielten Umsetzung und zum Vorher-/Nachher-Vergleich. Die vorhandene produktive Engine befindet sich in eurem Repository; sie ist nicht im ZIP enthalten.

## Zuerst ansehen

- `Leopold_Kohr_Schule_EG_Lernbuch_final.pdf`: freigegebene scharfe Vektorfassung, 39 Seiten. Erst rote Mauern, dann grüne Bodenflächen und anschließend detaillierte Erklärungen mit geschlossenen Rahmen, Pfeilen und farbigen Bögen.
- `plaene/Leopold_Kohr_Schule_EG_Mauern_rot_v1.pdf`: großer roter Gesamtplan.
- `plaene/Leopold_Kohr_Schule_EG_Gehflaechen_gruen.pdf`: großer grüner Gesamtplan mit schwarzen Originalstufen.
- `plaene/EG_Erklaerte_Details_Vektor.pdf`: alle 29 erklärten Originalausschnitte als scharfe Vektorseiten.

## Fachliche und technische Übergabe

`CLAUDE_STARTPROMPT_EG.md` ist der Startauftrag. `02_CLAUDE_AUFTRAG_EG.md` beschreibt die fachliche Aufgabe. `18_UMSETZUNG_UND_UEBERGABE_EG.md` enthält Lesereihenfolge und Umsetzungsnachweis. `DATEIUEBERSICHT_EG.md` listet sämtliche enthaltenen Dateien.

27 Regeln, 29 Beispiele, 120 beschriftete Zeiger, 38 Erklärrahmen, elf zusätzliche Originalbogen-Nachzeichnungen und 20 Prüffallspezifikationen sind enthalten. Originalquellen liegen unter `quellen/`, Daten unter `daten/`, Vorschauen unter `bilder/` und Hilfsskripte unter `skripte/`.

## Koordinaten und Datenbedeutung

`11_DATENVERTRAG_EG.md` lesen. Die roten GeoJSON-Konturen verwenden lokale DXF-Millimeter. Die grünen Flächen, Suchbereiche und Bildmarkierungen verwenden Original-PDF-Punkte mit Ursprung links oben. Beide Systeme nur mit der dokumentierten Transformation verbinden.

Rechteckrahmen, rote Lernkonturen und grüne Flächen dienen der Erklärung. Sie sind keine exakte Trainings- oder Kollisionsmaske. Die 20 Prüffälle wurden bislang nicht an der produktiven Engine ausgeführt. Zielhöhen und Geschossanschlüsse der Treppen bleiben bis zum Abgleich mit den passenden Plänen offen. Details: `09_OFFENE_PUNKTE_EG.md`.

## Paket prüfen und PDFs erneut erzeugen

`python3 skripte/pruefe_paket.py` prüft Dateien, Prüfsummen und Bezüge. Die benötigten Pakete stehen in `skripte/requirements.txt`. Diese Prüfung ist kein Raumerkennungslauf. Vektorexport und Wiederherstellung sind in `17_VEKTOREXPORT.md` dokumentiert. Die enthaltenen PNGs sind Vorschauen; die PDF verwendet echte Vektoren.

## Umfang und Teamarbeit

Dieses Paket betrifft ausschließlich das EG. UG und andere Geschosse bleiben eigene Arbeitsstände. Die früheren Nutzerkorrekturen, die vollständig eingerahmten Wand-Erklärungen und die Behebung der Unschärfe sind enthalten. Notleuchtenplatzierung und Normregeln gehören nicht zu diesem Raumerkennungsauftrag.
