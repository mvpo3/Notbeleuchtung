# aus_elektroplaner — gefiltertes Norm-/Praxiswissen aus dem elektro-planer-Projekt

Das elektro-planer-Projekt hatte eine große Wissensbasis (~1140 extrahierte
Dokumente: Normen, Bücher, Hersteller-Kataloge). Daraus wurden **nur die
Notbeleuchtungs-relevanten** Quellen gefiltert und zu fokussierten Digests
verdichtet (2026-08-28). Alles andere (Blitzschutz, RCD/AFDD-Anwendung,
Antennen, Netzwerktechnik, Photovoltaik …) ist für dieses Projekt irrelevant.

**Einordnung in der Hierarchie** (CLAUDE.md): LB → Referenz-Praxis → EN-1838/ÖNorm
→ OVE-Verbote. AT-Quellen (OVE/ÖNORM) stechen die DE-Praxisquellen in `../`.

## Die 5 gefilterten Digests

| Digest | Quelle (elektro-planer) | Warum wertvoll |
|--------|-------------------------|----------------|
| [Schrack_Katalog_NotSicherheitsbeleuchtung.md](Schrack_Katalog_NotSicherheitsbeleuchtung.md) | Schrack „Not- und Sicherheitsbeleuchtung" (k-sibe-at9, 400 S.) | **★ Marke, die die Engine rendert.** Echte Erkennungsweiten je Leuchtenfamilie (AI 15/AM 22/AX 30 m), Aufhellungs-Abstandstabellen je Montagehöhe (1 lx/5 lx, WF 0,80), Konvention **Wand=RZ / Decke=SI**, Linsen-Codes R/F/S/H, Einzel- vs. Gruppen-/Zentralbatterie. Verknüpfbar mit `schrack_symbol_mapping.yaml`. |
| [OVE_E_8101_2025_Deltas.md](OVE_E_8101_2025_Deltas.md) | OVE E 8101:**2025**-10 (852 S.) | **Aktuelle Ausgabe** (unser Haupt-Digest ist 2019). Neu: **Verbot 560.7.13 RCD/AFDD nicht in Sicherheitsstromkreisen** (Hard-Stop!), Versammlungs-Schwelle **400→240 Personen**, Betriebsdauer-Tabelle 56.A jetzt **normativ**, eigener N je SV-Kreis, Batterie-Mindestlebensdauer 10 a/5 a. |
| [OENORM_E_8002_Menschenansammlungen.md](OENORM_E_8002_Menschenansammlungen.md) | ÖVE/ÖNORM E 8002-1/-2/-8 (2007) | Historische AT-Norm (2019 in E 8101 überführt). Liefert das **„WANN"** (Erforderlichkeit/Schwellen je Gebäudetyp), EN 1838 das „WIE". Teil 1 = Basis, Teile 2/8 = Nutzungs-Overlays. Bestandsrelevanz. |
| [OENORM_E_8007_medizinisch.md](OENORM_E_8007_medizinisch.md) | ÖVE/ÖNORM E 8007 (2007) | Medizinische Sicherheitsstromversorgung (Basis für E 8101 Teil 7-710). **SV-Klassen ≤ 0,5 s (OP) / ≤ 15 s (Sicherheitsbel.) / 24 h Betrieb**, Anwendungsgruppe AG 0/1/2 als Weiche. Für medizinische Gebäudetypen. |
| [OVE_Fachinfos_E05_E06_E07.md](OVE_Fachinfos_E05_E06_E07.md) | OVE-Fachinfo E-05/E-06/E-07 | Geschwister zur schon vorhandenen E-08. **E-07: AT-Funktionserhalt = 30 min** (nicht DE-30/90), an Brandabschnittsgrenze, 50%-Restfunktion via alternierende Kreise. E-06: getrenntes Bussystem bevorzugt. E-05: Garagen = brandgefährdet. |

## Wichtigste übergreifende Erkenntnisse

1. **AT-Konzept „WANN vs. WIE":** OVE E 8101 / E 8002 / OIB-RL 2 regeln die
   **Erforderlichkeit** (welcher Gebäudetyp ab welcher Schwelle, welche Betriebsdauer);
   EN 1838 regelt die **Lichttechnik** (Lux, Erkennungsweite, Blendung). Die Engine
   braucht beides getrennt: Vor-Filter (Erforderlichkeit) + Geometrie (Ausleuchtung).
2. **Neuer Hard-Stop (E 8101:2025):** RCD/AFDD nie in Sicherheitsstromkreisen —
   gehört auf die OVE-Verbotsliste der Engine.
3. **AT-Funktionserhalt ist milder als DE:** 30 min, an Brandabschnittsgrenze
   festgemacht, innerhalb verzichtbar (E-07) — anders als DE-MLAR (E30/E90-Staffelung).
4. **Schrack-Produktdaten** liefern die konkreten Erkennungsweiten-/Abstandswerte,
   die den Normen fehlen — und passen zur gerenderten Symbol-Bibliothek.

## Herkunft der Rohdaten

Die Volltext-Extrakte + die ursprünglichen elektro-planer-Teil-Digests lagen unter
`knowledge/_extracted_text/` (Import aus `elektro-planer/knowledge/`). Nur die oben
gelisteten Quellen wurden übernommen; der Rest ist projektfremd.
