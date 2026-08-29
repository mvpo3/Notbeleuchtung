# Bild-Lehren — Beispiel-Notbeleuchtungspläne (Web-Fundstücke)

**Methode:** Vom Owner gesammelte Beispiel-Visualisierungen aus dem Netz, 2026-08-29
visuell ausgewertet. Quelle-Ordner (lokal): `DIN-Notbeleuchtungspläne(Beispiele)/`.
Die 3 Gold-Bilder liegen als `beispiel_*.jpg` neben dieser Datei.
**Einordnung:** Referenz-Praxis + eine Norm-Abbildung (OVE R 12-2). Marketing-/Lehr-
Visualisierungen (INOTEC-Stil, licht.de, uds) — gut für **Regeln/Intent**, NICHT als
koordinaten-genaue Ground-Truth (dafür bleibt `Projekte/Baufeld E2` die echte Referenz).
„DIN" im Ordnernamen ist irreführend: real ein Mix DIN/EN 1838/**OVE (AT)** — für unser
AT-Projekt zählt OVE/ÖNORM vor DIN.

## Schlüssel-Abbildungen

### beispiel_krankenhaus_luxzonen.jpg — Lux-Zonierung je Raumtyp
3D-Grundriss Klinik/Ambulanz mit **Beleuchtungsstärke-Label an jedem Bereich**:
**15 lx** über Labor/Behandlungstisch (Arbeitsplatz besonderer Gefährdung), **5 lx**
an Erste-Hilfe (grünes Kreuz) + Feuerlöscher (rot ABC), **1 lx** Gang-Mittellinie,
**0,5 lx** in Behandlungsräumen (Antipanik). Grüne RZ-Richtungspiktogramme an Türen/
Abzweigen, gelbe Punkte = Sicherheitsleuchten.
**LEHRE:** Die EN-1838-Lux-Kategorien (15/5/1/0,5 lx) sind **raumtyp-getrieben** — genau
unsere norm-getriebene `fuer_raum`-Klassifikation, nur um zwei Punkte reicher: (a) die
**15-lx-Klasse „Arbeitsplatz besonderer Gefährdung"** (EN 1838 §4.4) fehlt noch im
`Kind`-Enum (rz/antipanik/sicherheitsleuchte); (b) **5-lx-Anker** an Erste-Hilfe/
Feuerlöscher sind Pflicht-Punkte (§4.1.2 h/i) für die Anker-Strategie.

### beispiel_schule_luxzonen.jpg — Antipanik als Fläche/Raster
3D-Grundriss Schule: **Turnsaal/Mehrzweckraum** trägt ein **Raster vieler gleicher
Leuchten** (0,5 lx flächendeckend), Klassen 0,5 lx, Chemiesaal 0,5 lx + Feuerlöscher
5 lx, Gang 1 lx mit RZ-Pfeilen, Treppen je 1 lx.
**LEHRE:** Antipanik im Großraum ist **kein Einzelpunkt, sondern ein Gitter** —
gleichmäßige Flächenausleuchtung (EN 1838 §4.3, Ud ≥ 1:40). Unsere `plan_antipanik`
setzt bisher 1 Leuchte am Zentroid → **auf Raster erweitern** (Anzahl aus
`norm.mindest_anzahl`, geometrisch verteilt). Kleine Räume (Klasse) = 1 genügt,
Turnsaal = Raster.

### beispiel_OVE_R12-2_Bild8-9.jpg — AT-Norm: Kreis-/Versorgungs-Topologie
OVE-Richtlinie R 12-2:2019 „Ausführung mit baulichen Maßnahmen — Beispiel 3":
4 Geschosse (KG/EG/1.OG/2.OG) + Treppenhaus, je Geschoss = **eigener Brandabschnitt**,
Leuchten (X) entlang der Flure, grüne Pfeile = Fluchtrichtung je Etage, **CPS =
Zentralbatterie** unten, Verkabelung als **E30-Dosen / E30-Leitung** durch den
**Steigschacht (Typ-A-Schacht)**, „Abgeschlossene elektrische Betriebsstätte".
**LEHRE:** Die **Elektro-/Stromkreis-Seite** unseres Plans: getrennter Sicherheitskreis
+ zentrale Stromquelle (CPS) + brandsichere Leitung (E30) + Brandabschnitts-Trennung.
Speist `circuit_hint`/Stromkreis-Logik + einen späteren Elektro-Topologie-Output. **AT-
relevant** — R 12-2 war im Wissens-Index als fehlende AT-Quelle markiert, hier teilweise
bildlich erfasst.

## Sekundär (kurz)
- **LST_Notlicht.jpg** — 3D-Schnitt 3 Etagen, saubere Platzierungs-Übersicht (RZ über
  Türen, Deckenleuchten, Treppe, Zentralgerät). Gute Gesamtschau, keine neuen Regeln.
- **csm_…_INO_Visualisierung.jpg** (licht.de/INOTEC-Monitoring) — 2D-**Grundriss** mit
  gesetzten RZ + Sicherheitsleuchten-Punkten + Gruppen/Linien-Hierarchie. Referenz für
  unser **Output-Format** (2D-Plan wie wir ihn rendern) + Stromkreis-Gruppierung.
- **uds-fluchtweglenkung-simulation.jpg** — **dynamische** Fluchtweglenkung: grüner
  gültiger Weg vs. **rot gesperrter** Weg (adaptive Zeichen). Interessant, aber
  **out of scope** (adaptive Systeme ≠ statischer Plan).

## Engine-Impact (Priorität)
1. **`plan_antipanik` → Raster** (Schule-Turnsaal): Anzahl aus `mindest_anzahl`,
   geometrisch verteilt statt 1 Zentroid. *(direkt umsetzbar)*
2. **5-lx-Anker** Erste-Hilfe/Feuerlöscher als Anker-Ziele (mit `platzierung/graph.py`).
3. **15-lx-Klasse** „Arbeitsplatz besonderer Gefährdung" ins Klassifikations-/Kind-Enum
   (EN 1838 §4.4) — Contract-Erweiterung, 3-Owner.
4. **Stromkreis/CPS-Topologie** (OVE R 12-2) für den Elektro-Output.
