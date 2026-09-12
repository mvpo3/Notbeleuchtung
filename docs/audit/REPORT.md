# REPORT — Wissens-/Normabgleich + Engine-Audit (Branch leonis/wissensabgleich-engine)

Synthese aus A1 (Plan-Forensik P1) · A2 (Wissens-Coverage) · A3 (Engine-Ist + Lichtberechnung) ·
A4 (Widerspruchs-Matrix) · A5 (Naht/Owner). Volldetail: `01_…`–`06_…` in diesem Ordner.

## Summary (≤20 Zeilen)
1. **Kein S1** — kein OVE/EN-Hard-Stop im aktiven Codepfad verletzt.
2. **Drei S2 (Code tut nachweislich Falsches):** W09 doppelter Wartungsfaktor im Lux-Nachweis
   (0,80 hart vs. `anf.wartungsfaktor or 1.0`) · W19 ≥2-Leuchten-Redundanz nur QA-Warnung statt
   Garantie · W01 fixe Norm-Höhe/Floor 2000 statt podest-gestaffelter Stiegen-Montage (real bis 10,8 m).
3. **Wartungsfaktor-Divergenz** ist der konkreteste Bug: Engine-Deckung rechnet Default **1,0**
   (`deckung.py`), der Bericht schreibt **0,80** — zwei Werte, ein Plan. Beleg A1: WF 0,80 innen ist
   [AT-verbindlich] (3/3 Profi-Berichte), **0,57 außen** ist [AT-Referenzpraxis] und fehlt ganz.
4. **Norm-Aktivierung — totes Wissen:** `platzierung_regeln.yaml` (25 Regeln) und `regel_deckung.yaml`
   (22 Typen) werden von KEINEM Produktivpfad gelesen; das Platzierungs-Verhalten lebt prozedural in
   `*_strategy.py`. `sonderstellen.yaml` 5-lx/2-m/15-lx-Methoden haben keinen src-Aufrufer.
   `erkennungsweite_m` wirkt nur über den Deckungs-Radius; `plan_rettungszeichen_sichtlinie` ist test-only.
5. **Lichtberechnung fehlt/rudimentär:** photometrischer a/b-Tabellen-Lookup (a/b = **DE-only**, Engine
   nutzt analytische Bisektion — bleibt), Blendungsgrenzen f(h), Höhenformel h≤1,5+tan20°·l,
   seitenselektiver Randbereich, Außen-WF, vertikaler Rettungsweg-Nachweis.
6. **Naht 🔴 `sonderstellen`:** Leonis konsumiert das Contract-Feld, Selmans echter Provider setzt es
   nie → der komplette §4.1.2-h/i-Zweig ist auf Realdaten tot (kein Silent-OK, aber wirkungslos).
7. **Naht 🟡 `norm_quelle`:** Invariante durch Praxis-Präfixe (`fachpraxis:`/`Referenz-Praxis:`)
   durchbrochen — kein echter Norm-Trail; braucht `decision_source`-Contract (3-Owner).
8. **Drift (S4):** Konstanten duplizieren die YAML-Single-Source (`_REDUNDANZ_REICHWEITE_MM`,
   `_TOILETTEN_TYPEN`), Pfeil-Rotationsformel 3× kopiert, grün/gelb-Layer als Konvention offen.
9. **id()-Cache: existiert nicht** (Annahme widerlegt). **Golden-Fixtures: keine Wert-Drift**
   (aber nur RZ-Abdeckung, nicht Lux). Import-Grenzen sauber (kein Owner↔Owner-Import).

## Alle S2 (nach Schwere)
- **W09** `lux_nachweis_bericht.py:41,70` vs. `:92,98` — WF 0,80 hart vs. `anf.wartungsfaktor`. [AT-verbindlich]. Owner Leonis/Enis.
- **W19** `validierung.py:159-177` — ≥2 Leuchten nur Warnung. [AT-verbindlich] (EN 50172 §5.1.8). Owner Leonis.
- **W01** `provider.py:141` + `deckungs_zuordnung.py:72` vs. A1 F07/F08 (Baraw. Stiege A S.8–10). [AT-Referenzpraxis]. Owner Enis/Leonis.

## Unbelegt
Leer. Jeder A-/W-Befund trägt Geltungs-Tag + Beleg (datei:zeile bzw. Plan, S.). DWG-Teil von P1
(11 Dateien) blieb ungelesen — ODA File Converter nicht installiert; als Limitation in `01_…` vermerkt,
kein Befund darauf gestützt.
