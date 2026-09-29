# 2. OG - vollständiges Lern- und Übergabepaket

Projekt: Leopold-Kohr-Schule / SH22-LKS. Geschoss: **2. OG**. Stand: 21.09.2026.
Der Nutzer hat das 36-seitige Lernbuch akzeptiert und dieses ZIP beauftragt. Die freigegebene PDF liegt unverändert in [pdf/2OG_Lernbuch.pdf](pdf/2OG_Lernbuch.pdf).

## So startest du

1. Das ZIP vollständig entpacken. Den Paketordner in Claude Code verfügbar machen.
2. [PROMPT_FUER_CLAUDE_CODE.md](PROMPT_FUER_CLAUDE_CODE.md) als Arbeitsauftrag verwenden.
3. Claude liest zuerst [CLAUDE.md](CLAUDE.md), das Lernbuch und die Dateien unter [wissen/](wissen/).
4. Danach den echten 2OG-Plan mit der bestehenden Raumerkennung untersuchen und einen nachvollziehbaren Umsetzungsversuch durchführen.

## Enthalten

- **6 PDFs:** freigegebenes Lernbuch, Originalplan, Architekturbasis, rote Mauern, grüne Bodenflächen und 25 erklärte Detailausschnitte.
- Original-DXF, 25 kommentierte PNG-Detailbilder und zwei Gesamtansichten.
- Markdown-Lernwissen zu Mauern, Türen, Fenstern, Wegen, Grenzen, Treppen und typischen Verwechslungen.
- JSON/GeoJSON mit Quellen, Koordinaten, 25 Lernbeispielen, 100 Rahmen, Materialkonturen, Bodenreferenzen, Regeln, Prüffällen und offenen Punkten.
- Ausführbare Hilfen für Paketprüfung, Belegsuche, Ergebniskontrolle und Reproduktion der Lernansichten.

## Was bereits erledigt ist

Das Lernmaterial wurde erstellt und visuell kontrolliert. **Es wurde noch keine bestehende Raumerkennungs-Engine an diesem 2OG-Paket ausgeführt oder verbessert.** Das ZIP gibt Claude die Grundlagen und den Auftrag dafür. Einlesen bedeutet hier Regeln und Belege verstehen; es ist kein automatisches Modelltraining.

Die roten/grünen Konturen sind Lerninterpretationen. Erklärrahmen sind Suchbereiche, keine Objektgrenzen. Ein positives Paketprüfergebnis bestätigt Datenintegrität und Verweise, nicht die Güte einer späteren Raumerkennung.

## Befehle aus dem entpackten Paketordner

```bash
python3 skripte/pruefe_paket.py
python3 skripte/zeige_beispiel.py D01
```

Für die erweiterte Prüfung oder Reproduktion mit Python 3.12:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 skripte/pruefe_paket.py --erweitert
python3 skripte/reproduziere.py
```

Die Reproduktion schreibt in `_build/` und `reproduziert/`; die freigegebenen Dateien werden nicht überschrieben. Sie ist zur Nutzung des vorhandenen Lernbuchs nicht erforderlich.

## Fachliche Grenze

Dieses Paket behandelt Raumerkennung und geometrische Verbindungen im 2. OG. Normgerechte Notleuchtenplatzierung und baurechtliche Breitenprüfungen sind ein nachgelagerter, getrennter Bereich. Angaben zur Körperbreite dienen hier ausschließlich einer gegebenenfalls vereinbarten geometrischen Kollisionsprüfung.
