# knowledge/extracted — Norm-Digests für die Notbeleuchtungs-Engine

Maschinen-orientierte Extraktion der 14 Norm-/Rechts-PDFs aus `knowledge/`
(Volltext via pypdf, 2026-08-28). Jedes Digest: Regel-Tabelle mit ID,
§/Seite-Referenz, Werten und Typ (**Gebot / Verbot / Grenzwert / Definition /
Empfehlung**). Verbote = Hard Stops der Engine (Entscheidungs-Hierarchie in
`CLAUDE.md`: LB-explizit → Referenz-Praxis → EN-1838/ÖNorm-Default →
OVE-Verbote).

**Nichts wurde erfunden:** jede Regel trägt ihre Fundstelle; Unsicherheiten aus
der PDF-Extraktion sind je Datei unter „Extraktionslücken" markiert (v.a.
zerflossene Tabellen-Layouts — vor Ableitung harter Regeln gegen das
PDF-Original prüfen).

## Platzierungs-relevant (Kern → `normwissen/data/`, Owner Enis)

| Digest | Norm | Regeln | Warum wichtig |
|--------|------|-------:|---------------|
| [EN_1838_notbeleuchtung.md](EN_1838_notbeleuchtung.md) | EN 1838:2019 | 82 | **DIE Platzierungsnorm.** §4.1.2 Pflicht-Orte a–k (Ausgangstüren, Treppen, Richtungsänderungen, Kreuzungen, letzter Ausgang, Erste-Hilfe/Brandmelde-Stellen à 5 lx vertikal…), „nahe" = ≤ 2 m horizontal, Montage ≥ 2 m. Profile: Rettungsweg ≥ 1 lx Mittellinie · Antipanik ≥ 0,5 lx · Arbeitsplätze ≥ 10 %/15 lx. Ud ≥ 1:40, Ra ≥ 40, ≥ 1 h, 50 %/5 s + 100 %/60 s. RZ: l = z·h (z=100 beleuchtet / 200 hinterleuchtet), Leuchtdichte ≥ 2 cd/m². |
| [OVE_E_8101_niederspannungsanlagen.md](OVE_E_8101_niederspannungsanlagen.md) | OVE E 8101:2019 | 146 (17 Verbote) | Teil 5-56 „Sicherheitszwecke" vollständig. **Stromkreis-Constraints:** je Brandabschnitt Leuchten abwechselnd auf ≥ 2 Kreise; ≤ 20 Leuchten/Endstromkreis bei ≤ 60 % Nennstrom; Leuchten-Nummerierungspflicht (560.9.15 → Render!). **Zusatz-Pflichtorte** 718.560.9.001.AT (Fahrtreppen, Sanitär ≥ 8 m², barrierefreie WCs, BMZ/Sprinklerzentrale, Antipanik > 60 m²/Versammlung > 400 P.). **Hard Stops:** keine Primärzellen, Sicherheitskreise nie durch BE3/Ex/Aufzugs-/Kaminschächte, keine Antipanik-Dimmung. Betriebsdauern Tab. 56.A.1.AT (Standard 3 h, Beherbergung/Pflege/Hochhaus 8 h). |
| [OVE_E_8015.md](OVE_E_8015.md) | OVE E 8015:2022 | 63 (2 Verbote) | Wohnbau-Stromkreis-Planung: §4.1 Trigger „Sicherheitsbeleuchtung abklären"; Beleuchtungs-/Steckdosenkreise nicht kombinieren; Verteiler-Verortung + ≥ 30 % Reserve; Orientierungslicht-Schalter in Stiegenhäusern. |

## Rechtsrahmen (Verbindlichkeit / Audit-Trail)

| Digest | Inhalt | Kernaussage für `norm_quelle` |
|--------|--------|-------------------------------|
| [ETV_2002_2010_2020.md](ETV_2002_2010_2020.md) | Elektrotechnikverordnung, 3 Fassungen + Normlisten | **ETV 2020 maßgeblich.** OVE E 8101 = Anhang II (kundgemacht, Konformitätsvermutung). **EN 1838 steht in KEINER ETV-Liste** — wirkt über Baurecht/OIB/Stand der Technik. E 8002 nur historisch (2006–2020). → `norm_quelle` sollte „ETV-kundgemacht" vs. „Stand der Technik" unterscheiden. |
| [ETG_1992.md](ETG_1992.md) | Elektrotechnikgesetz | §3: Konformitätsvermutung bei Norm-Anwendung, Nachweislast bei Abweichung; Strafbewehrung → Basis der OVE-Hard-Stops. Neuanlagen immer gegen aktuellen Normenstand (§4/§6). |
| [ESV_2012.md](ESV_2012.md) | Elektroschutzverordnung | Betrieb nach anerkannten Regeln der Technik; Prüfpflichten (Notbeleuchtung untertage wöchentlich); Plandokumentation aufbewahrungspflichtig → der generierte Plan + Audit-Trail ist Teil davon. |
| [Nullungsverordnung.md](Nullungsverordnung.md) | Nullung | TN-System-Default österreichischer Netze; für Platzierung irrelevant. |
| [RIS_Standesregeln_Elektrotechnik.md](RIS_Standesregeln_Elektrotechnik.md) | Standesregeln Gewerbe | ETG/ETV/OVE/ÖNORM-Einhaltung = Standespflicht. |

## Rand-Relevanz (bewusst NICHT ins NormRegelwerk)

| Digest | Inhalt | Einordnung |
|--------|--------|-----------|
| [OENORM_E_8014.md](OENORM_E_8014.md) | Fundamenterder/Erdung/Potentialausgleich | Kein Notbeleuchtungs-Bezug. |
| [OVE_E_8350.md](OVE_E_8350.md) | Brandbekämpfung in E-Anlagen | Feuerwehr-Einsatzregeln; einziger Bezug: Beleuchtung im Brandfall möglichst lange versorgen (§5.1.3/4). |
| [OVE_E_8351.md](OVE_E_8351.md) | Erste Hilfe bei E-Unfällen | Keine Planungs-Relevanz. |
| [Sicherheitsvorschriften_Elektro.md](Sicherheitsvorschriften_Elektro.md) | WIFI-Schulungsskript (keine Norm!) | Null Notbeleuchtungs-Fachinhalt (grep-verifiziert); nur Norm-Landkarte (E 8002 seit 2019 in E 8101 integriert). Nie als `norm_quelle`. |

## Bekannte Lücken im Quellenbestand

- **OVE-Richtlinie R 12-2** („wo ist Sicherheitsbeleuchtung erforderlich") — von
  E 8101 referenziert, PDF nicht im Repo.
- **EN 50172** (Betrieb/Prüfung Sicherheitsbeleuchtungsanlagen), **TRVB E 102 /
  TRVB 123 S**, **OIB-Richtlinie 2** — mehrfach normativ referenziert, nicht im
  Repo. Bei Bedarf nachlegen → gleiche Extraktion.

## Nutzung

- **Enis (`normwissen/`):** Regel-Tabellen (v.a. EN 1838 + E 8101 Teil 5-56)
  → `normwissen/data/*.yaml`; Regel-IDs (EN1838-R…, OVE8101-R…) als stabile
  Referenzen für `NormRegelwerk.quellen` übernehmen.
- **Leonis (`platzierung/`):** konsumiert weiterhin NUR den `NormProvider` —
  diese Digests sind Enis' Port-Material, kein Import-Ziel.
- **Hauptengine:** Verbots-Zeilen = Hard-Stop-Kandidaten für ein späteres
  Validierungs-Gate im Pipeline-Schritt.
