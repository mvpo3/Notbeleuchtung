# Stromkreisbeschriftung für Wohnungen — Zeichenmethode (Ground-Truth)

> **⚠️ KORRIGIERT (Slice 2.8.0, 13.08.2026): Autorität sind jetzt die realen
> WHG-Verteilerblätter** `WHG_Verteiler/Typ 1.pdf` (≤75 m²) + `Typ 2.pdf`
> (>75 m²) und das Korrektur-DXF `output_korrigiert_mit_Stromkreise.dxf`
> (TOP 24). Das Lehr-PDF hatte **1F6/1F7 VERTAUSCHT**: richtig ist
> **1F6 = Schuko Wohnbereich, 1F7 = Licht Wohnbereich** (Typ 1). Weitere
> Korrekturen: Steckdosen-Sammelkreise tragen **kein `.S`**; Licht-`.S` pro
> **Schaltgruppe** (Spots eines Raums teilen einen Sub, Schalter erben ihn);
> **RT/LÜ sind Kürzel ohne F-Kreis**; Typ 2 hat **KEIN 2F7** (Bad bleibt 2F4),
> 1F7 = Schuko ab 2. Schlafzimmer, Licht rückt auf 1F8. Die Tabellen unten
> sind auf den Verteilerblatt-Stand korrigiert.

**Quelle (historisch):** `knowledge/Elektropläne-zeichnen Wissen/Stromkreisbeschriftungen_für_Wohnungen.pdf`
(von Leonis erstellt, 25 Seiten) — bei Konflikt gewinnen die Verteilerblätter
(siehe Banner).

> **⚠️ Konflikt mit `backend/rules/circuit_label_policy.yaml` (Track B, status:
> draft 0.1.0):** Die yaml kodiert die führende Ziffer als *Wohnungsnummer* und
> eine *durchgehende* F1..F13-Kette (FI als F1/F2). Das ist **inkompatibel** mit
> dieser Zeichenmethode. Entscheidung: **PDF gewinnt.** yaml-Angleichung liegt bei
> Track B (`handoff(B)`).

## Label-Format

    <FI>F<N>.<S>

| Teil | Bedeutung |
|------|-----------|
| `<FI>` | **FI-Gruppe / FI-Schutzschalter-Nummer** (`1` = 1. FI, `2` = 2. FI). **NICHT** Wohnungsnummer. |
| `F<N>` | Laufende LS-/Sicherungsnummer **innerhalb der FI-Gruppe**, in Montage-Reihenfolge im Verteiler. `F1` = der FI-Schutzschalter selbst. |
| `.<S>` | **Nur Licht-Kreise:** laufende SCHALTGRUPPE (alle Spots eines Raums = ein Sub, jeder Decken-/Wandauslass eigener Sub). Licht-Schalter erben den Sub ihrer Gruppe. **Steckdosen-Sammelkreise und dedizierte Lasten tragen KEIN `.S`.** |

**Beispiele:** `1F2` = E-Herd. `1F7.1` = 1. Licht-Schaltgruppe Wohnzimmer (Typ 1).
`1F6` = Wohnbereich-Schuko (ohne Sub). `2F2` = Waschmaschine. `2F5.3` = Bad-Licht.

**Format-Regex (Guard):** `^[A-Z0-9_-]+F[0-9]+\.[0-9]+$` (für `.S`-Labels;
reine LS-Labels ohne Sub wie `1F2` matchen `^\d+F\d+$`).

## Ordnungsregel

- Jede FI-Gruppe beginnt mit den **stärksten Verbrauchern** (16A) zuerst.
- **Küche zuerst**, E-Herd IMMER direkt nach dem FI.
- Faustregel: **~8–10 Steckdosen pro Sicherung**, nicht mehr.
- Reihenfolge der `.S` bei Licht = Betretungs-/Raumreihenfolge; innerhalb egal,
  aber konsistent halten.

## FI-Gruppe 1 — Küche + Wohn-/Schlafbereich

| Label | Verbraucher | Kürzel |
|-------|-------------|--------|
| `1F1` | FI-Schutzschalter 1 | — |
| `1F2` | E-Herd (eigene Sicherung, immer) | — |
| `1F3` | Geschirrspüler | GS |
| `1F4` | Mikrowellenherd | MW |
| `1F5` | Küchensteckdosen (Kühlschrank, Arbeitsplatte, Dunstabzug) — ohne `.S` | KS, AR, DA |
| `1F6` | **Steckdosen** Wohnzimmer + Schlafzimmer + Terrasse — ohne `.S` | — |
| `1F7` | **Licht** Wohnzimmer + Schlafzimmer + Küche + Terrasse (Typ 1; bei Typ 2 → `1F8`) | — |

**Licht-Sub-Nummerierung** (`1F7.x` Typ 1 / `1F8.x` Typ 2, Betretungsreihenfolge
Wohnzimmer → Küche → Außen → Zimmer): ein Sub pro SCHALTGRUPPE — jeder
Deckenauslass/Wandauslass eigener Sub, alle Spots eines Raums teilen EINEN Sub.
Wechselschalter/Schalter erben das Label ihrer Gruppe.

## FI-Gruppe 2 — Nassräume + Nebenräume + Großgeräte

| Label | Verbraucher | Kürzel |
|-------|-------------|--------|
| `2F1` | FI-Schutzschalter 2 | — |
| `2F2` | Waschmaschine | WM |
| `2F3` | Wäschetrockner | WT |
| `2F4` | Steckdosen Vorraum + Bad + Abstellraum + Flur/Gang + WC — ohne `.S`, **in BEIDEN Typen inkl. Bad** | — |
| `2F5` | Licht Resträume (siehe Sub) | — |
| `2F6` | Heizungssteuerung (Heizkörper Bad) | HT |

**`2F5` Sub-Nummerierung** (Betretungsreihenfolge, Schaltgruppen wie oben):
Vorraum → Gang/Flur → **Bad** (Deckenauslass/Spots vor Wandleuchte, je eigene
Gruppe) → Abstellraum → WC. (Korrektur-DXF TOP 24: Bad vor ASR.)

## Typ 2 — Variante >75 m² (WHG-Verteilerblatt Typ 2)

- Steckdosen **ab dem ZWEITEN Schlafzimmer** aus `1F6` abtrennen → **`1F7`**
  (SZ2+SZ3+…); das erste Schlafzimmer bleibt auf `1F6`.
- Wohnbereich-**Licht rückt auf `1F8`**.
- **KEIN `2F7`** — Bad-Steckdosen bleiben auch bei Typ 2 auf `2F4`.
- Schwelle: Netto-Wohnfläche >75 m² (Balkon/Loggia/Terrasse zählen nicht).

## Zusatz-Kürzel am Symbol (ergänzend, keine F-Kreis-Nummer)

| Kürzel | Bedeutung |
|--------|-----------|
| `KS` | Kühlschrank (in `1F5`) |
| `AR` | Arbeitssteckdose (in `1F5`) |
| `WM` | Waschmaschine |
| `WT` | Wäschetrockner |
| `GS` | Geschirrspüler |
| `MW` | Mikrowellenherd |
| `LÜ` | Lüftung (Bad/WC) — **NUR Kürzel, kein F-Kreis** (Korrektur-DXF) |
| `RT` | Raumthermostat — **NUR Kürzel, kein F-Kreis** (Korrektur-DXF) |
| `LD` | Leerdose — NUR Kürzel |
| `TV` | TV-Anschluss (Wohnzimmer) — NUR Kürzel |
| `HT` | Heizungssteuerung (trägt `2F6`) |

## Spots / Rauchmelder-Bezug (aus PDF)

Bei gewünschten Spots werden so viele platziert, wie der Raum hergibt — ABER ein
Rauchmelder muss **60 cm vom Deckenauslass** platziert werden (begrenzt Spot-Zahl).
Relevanz hier: die Spot-Deckenauslässe teilen sich das Licht-Label ihres Raums.

## Engine-Mapping (`backend/engine/circuit_zeichenmethode.py`, Slice 2.8.0)

Kategorie → (FI-Gruppe, F-Rang innerhalb Gruppe):

```
FI-1:  eherd=2, geschirrspueler=3, mikrowelle=4, kuechensteckdose=5 (KS/AR/DA),
       steckdose_wohnbereich=6, licht_wohnbereich=7
       [Typ 2:] steckdose_schlafzimmer2=7 (bedroom_rank>=1), licht_wohnbereich=8
FI-2:  waschmaschine=2, waeschetrockner=3, steckdose_restraeume=4 (inkl. Bad),
       licht_restraeume=5, heizungssteuerung=6
FI-0 (nur Kürzel): raumthermostat=RT, lueftung=LÜ, tv=TV, leerdose=LD
```

`.S` = Schaltgruppen-Pass nur für Licht-Kreise (Spots eines Raums = ein Sub);
Licht-Schalter erben den Sub per Block-Zuteilung (`is_light_switch`).
