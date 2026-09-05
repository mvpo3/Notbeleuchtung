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
5. **Norm-Anker für Enis:** DIN ISO 23601 (gilt in AT direkt — Austrian Standards
   hat KEIN eigenes ÖNORM-Pendant geschaffen) + TRVB O 119 (Fluchtweg-
   Orientierungspläne) + TRVB O 121 (Wien) + AStV/KennV; Piktogramme ÖNORM EN
   ISO 7010 + ÖNORM F 2030 (Brandschutzzeichen) — noch NICHT in `normwissen/data`
   kodiert (heutige Digests decken EN 1838/50172/OVE = Beleuchtung, nicht
   Aushang-Pläne).

## 3. AT-Norm-Vergleich — das TR-Hotel-Foto gegen österreichische Anforderungen

**Normenlage AT (recherchiert 2026-09-05):** Für Flucht-/Rettungspläne gilt in
Österreich **DIN ISO 23601 direkt als Stand der Technik** (kein ÖNORM-Klon);
organisatorischer Rahmen **TRVB O 119**, in Wien zusätzlich **TRVB O 121**;
Rechtspflichten aus **AStV/KennV** (siehe `Fachinfo_E08_Arbeitsstaetten.md`);
Piktogramme **ÖNORM EN ISO 7010**, Brandschutzzeichen ergänzend **ÖNORM F 2030**
(+ Z 1000-2). Hotels/Beherbergung: Aushang **in jedem Zimmer** + an strategischen
Punkten, Montagehöhe ≈ 1,60 m (barrierefrei ≈ 1,30 m), **lagerichtig** gehängt
(links am Plan = links im Raum).

| Element | TR-Foto (Elitoria) | AT/ISO-23601-Anforderung | Bewertung |
|---|---|---|---|
| Hintergrund | dunkles Metall-Braun, helle Linien | **weiß** (oder nachleuchtend weiß, ISO 3864-1) | ❌ Design-Abweichung — in AT so nicht normkonform |
| Fluchtweg-Darstellung | dünne helle Linie | **hellgrün unterlegt**, Richtungspfeile in Sicherheitsgrün | ❌ |
| You-are-here | **violetter** Punkt | Standortpunkt in **Sicherheitsfarbe Blau** | ❌ Farbfehler |
| Exit-Piktogramme | grün, ISO-7010-artig (E001/E002) | ISO 7010 / KennV | ✅ |
| Brandschutz-POIs | Feuertaster + Wandhydrant, rot | ISO 7010 F-Serie / ÖNORM F 2030, an realer Position | ✅ Prinzip; Symbolik prüfen |
| **Sammelstelle** | nur im Text erwähnt, **kein Symbol im Plan** | Pflicht-Inhalt (E007 + Lage) | ❌ fehlt |
| **Erste-Hilfe-Einrichtungen** | nicht im Plan | Pflicht wenn vorhanden | ❌ fehlt |
| Legende | zweisprachig TR/EN, alle Symbole erklärt | Pflicht (Landessprache; Mehrsprachigkeit zulässig/üblich) | ✅ vorbildlich |
| Verhaltensregeln | Brandfall + Sicherheit + Barrierefreiheits-Hinweis | „Verhaltenstafeln" Pflicht | ✅ Barrierefreiheits-Absatz geht ÜBER ISO hinaus |
| Kopf | Zimmernr. + Titel zweisprachig | Überschrift ≥ 7 % der kurzen Blattseite | ✅ |
| Ersteller/Datum/Revision/Geschoss | **nicht erkennbar** | Pflicht-Angaben | ❌ fehlt |
| Maßstab/Format | Zimmeraushang (≈A3) | Einzelraumplan ≥ A4, Maßstab bis 1:350 (Detail 1:100/1:250) | ✅ plausibel |
| Übersichtsplan | keiner | nur nötig bei großen Objekten (≤ 10 % Fläche) | ✅ ok |
| Lesbarkeit bei Stromausfall | unklar (Metallschild, nicht nachleuchtend?) | Sicherheitsbeleuchtung ODER langnachleuchtend ≥ Klasse C (ISO 17398) | ⚠️ prüfungswürdig |

**Fazit:** Der TR-Aushang ist strukturell komplett (Grundriss + Standort + Route
+ POIs + Legende + Verhaltensregeln — gute Vorlage für den Aufbau), aber in der
**Farbcodierung klar nicht AT-konform** (dunkler Grund, violetter Standort,
Route nicht grün) und ihm fehlen **Sammelstelle, Erste-Hilfe, Plan-Metadaten**.
Für die Engine heißt das: **Struktur vom Foto übernehmen, Farb-/Inhalts-Regeln
aus ISO 23601** (weißer Grund, Route hellgrün, Standort blau, Pflicht-Elemente).

**Direkte Engine-Nähte (heute schon relevant):**
- **EN 1838:2025 §4.2:** ≤ 2 m an Flucht-/Rettungsplänen **min. 5 lx**
  (`Handbuch_NotSicherheitsbeleuchtung_2026.md` HB2026-R42; Hotelzimmer-Aushänge
  können ausgenommen sein). Sobald Aushang-Positionen bekannt sind, ist das ein
  SL-Platzierungs-Trigger — Sonderstellen-Typ-Kandidat für #93.
- **Sammelstelle** existiert in keinem Contract-Feld — für den Aushang-Slice
  nötig (RaumModell- oder ProjektKontext-Erweiterung, 3-Owner).
- Aushang-Renderer-Parameter direkt aus ISO 23601 ableitbar: Format ≥ A4/A3,
  Symbole ≥ 7 mm, Schrift ≥ 2 mm, Überschrift ≥ 7 %, Maßstab 1:100/250/350,
  Montagehöhe 1,60/1,30 m, Rotation lagerichtig je Hängeposition.

Quellen: [brandschutz-checkup.de — ISO 23601 in Österreich](https://brandschutz-checkup.de/flucht-und-rettungsplan-nach-din-iso-23601-oesterreich/) ·
[brandschutz-checkup.de — Hotel Österreich](https://brandschutz-checkup.de/flucht-und-rettungsplan-hotel-oesterreich/) ·
[fluchtplan24.de — DIN-ISO-23601-Gestaltung](https://www.fluchtplan24.de/informationen/gestaltung-flucht-und-rettungsplan-din-iso-23601/) ·
[Baudatenbank — ÖNORM F 2030](https://www.bdb.at/Service/NormenDetail?id=666397) ·
[praeventivdienste.at — Fluchtweg-/Orientierungspläne](https://praeventivdienste.at/5211)

## 4. Status

- Foto committet (`6986d71`), dieser Digest = Sichtung 2026-09-05.
- Slice ist NICHT eingeplant — Produktidee im Backlog; braucht Owner-Priorisierung.
  Kleinster Anfang ohne Contract: Aushang-Renderer mit den heutigen Feldern
  (Konturen + Route + Exits), POIs folgen mit #93.
