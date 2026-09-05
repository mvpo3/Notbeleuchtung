# Wissens-Digest — Fluchtwegplan-Zimmeraushang (Hotel-Referenzfoto)

Quelle: `knowledge/sonstiges Wissen Notbeleuchtung/photo_2026-09-04_21-54-12.jpg`
(Elitoria Hotel, Zimmer-Aushang 1514, „Yangın Kaçış Planı / Fire Escape Plan",
fotografiert 2026-09-04). Extrahiert 2026-09-05.

**Einordnung:** Das ist KEIN Normwissen für die Platzierung, sondern die Referenz
für ein **zweites Render-Ziel** derselben Pipeline: der aushangfertige
Fluchtwegplan (Zimmer/Etagen-Aushang nach DIN ISO 23601-Art) — ein anderes
Artefakt als der E-Installationsplan (DXF für den Elektriker), aber aus
denselben Modelldaten (RaumModell + PlatzierungsErgebnis) erzeugbar.

---

## 1. Aufbau des Aushangs (was der Profi-Aushang zeigt)

| Element | Beobachtung am Referenzfoto |
|---|---|
| **Kopf** | Zimmernummer groß (1514) · Titel zweisprachig (Landessprache + EN) · Hotel-Logo |
| **Grundriss** | stark vereinfachte Etagen-Silhouette: nur Wände/Raumkonturen, KEINE Möblierung, keine Bemaßung, keine Layer-Detail |
| **You-are-here** | violetter Punkt („Buradasınız / You Are Here") am Standort des Aushangs |
| **Fluchtweg** | helle Linie vom Standort zu BEIDEN Treppenhäusern/Ausgängen (redundante Wege) |
| **Fluchtweg-Ziele** | Exit-Piktogramme (grün, ISO 7010 E001/E002) an den Treppenhäusern |
| **Brandschutz-POIs** | rote Piktogramme im Grundriss: Feuermelder-Taster (Fire Button), Wandhydrant/Löschschlauch (Fire Hose Cabinet) — an den realen Positionen |
| **Legende** | rechts, Piktogramm + Bezeichnung zweisprachig: You are here · Escape Route Direction · Fire Exit · Fire Button · Fire Hose Cabinet |
| **Verhaltenstext** | unten dreispaltig: Alarmfall-Anweisung + Sicherheitshinweise (zweisprachig) + Barrierefreiheits-Hinweis (Rollstuhl-/Gehörlosen-Icons) |

## 2. Ableitungen für die Engine (wenn der Slice kommt)

1. **Datenlage reicht heute fast:** Raumkonturen (`RaumModell.raeume`), Fluchtweg-
   Zirkulation (`segmente`), Ausgänge (`ausgaenge`) und RZ-Positionen existieren im
   Contract. **Fehlt:** Brandschutz-POIs (Feuertaster/Hydrant/Löscher) — genau der
   blockierte Sonderstellen-Contract (#93, `RaumModell.sonderstellen[]`, Typen
   feuerloescher/hydrant/brandmelder). Der Aushang-Slice wäre der zweite Konsument.
2. **You-are-here ist parametrisch:** ein Aushang PRO Standort (Zimmer/Flurpunkt)
   — Render-Input `standort_xy` + gedrehte Ausrichtung (Aushang hängt so, dass
   „geradeaus am Plan" = „geradeaus im Flur"; Profi-Praxis: Plan wird je
   Hängeposition rotiert).
3. **Route = kürzester Weg im Zirkulationsgraph** vom Standort zu ≥1 Ausgang
   (NetworkX liegt schon in `platzierung/graph.py`); Redundanz: beide Richtungen
   zeigen, wie am Referenzfoto.
4. **Render-Stil eigenständig:** vereinfachte Konturen (nur Außen-/Raumkanten),
   Piktogramme statt CAD-Symbole, Legende + Verhaltenstext als feste Blöcke,
   Mehrsprachigkeit als Parameter. → eigener Renderer (`render/aushang_…`), NICHT
   der DXF-Renderer; Ziel-Format eher PDF/PNG als DXF.
5. **Norm-Anker für Enis:** DIN ISO 23601 (Flucht- und Rettungspläne),
   ASR A2.3/ÖNORM Z 1000-Familie — noch NICHT in `normwissen/data` kodiert
   (heutige Digests decken EN 1838/50172/OVE = Beleuchtung, nicht Aushang-Pläne).

## 3. Status

- Foto committet (`6986d71`), dieser Digest = Sichtung 2026-09-05.
- Slice ist NICHT eingeplant — Produktidee im Backlog; braucht Owner-Priorisierung.
  Kleinster Anfang ohne Contract: Aushang-Renderer mit den heutigen Feldern
  (Konturen + Route + Exits), POIs folgen mit #93.
