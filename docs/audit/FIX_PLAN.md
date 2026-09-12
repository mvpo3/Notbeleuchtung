# FIX_PLAN — leonis/wissensabgleich-engine

Reihenfolge-Logik (Vorgabe): **Korrektheit → Norm-Aktivierung → Lichtberechnung → Enis-Wissens-Integration.**
Jeder Fix: ein Commit, ein maschineller Test (exakte Assertion). Neue/geänderte Regeln über
NormProvider-Lookup, nicht als Code-Konstante. Contract-Touch → `contract_version`-Bump +
`gen_schema.py` + Protokoll in `docs/audit/HANDOFF_B_ENIS.md`.

`Vote`: 🟩 diese Runde (Leonis, in-Lane, hohe Konfidenz) · 🟨 diese Runde mit Enis-YAML-Abstimmung
(protokolliert) · 🟦 an Selman/3-Owner übergeben (nicht einseitig).

| Fix-ID | Titel | Befund-IDs | Dateien | Umfang | Abhängigkeit | Testname | Vote |
|--------|-------|-----------|---------|--------|--------------|----------|------|
| **F01** | Wartungsfaktor im Nachweis aus EINER Quelle (`anf.wartungsfaktor`), 0,80 nicht mehr hart | W09 (S2) | `render/lux_nachweis_bericht.py` | S | — | `test_lux_nachweis_wf_eine_quelle` | 🟩 |
| **F02** | Deckungs-WF konsumiert `anf.wartungsfaktor` statt Default 1,0 (Divergenz zum Bericht schließen) | W09/A3-Zusatz (S2) | `deckung.py`, `lux.py` | S | F01 | `test_deckung_wf_aus_norm` | 🟩 |
| **F03** | Pfeil-Rotationsformel in einen Helper (`bausteine`), 3 Aufrufer ziehen ihn | W16 (S4) | `bausteine.py`, `anker_strategy.py`, `gang_strategy.py`, `fachpraxis.py` | S | — | `test_rotation_helper_ein_ort` | 🟩 |
| **F04** | `_REDUNDANZ_REICHWEITE_MM` durch `norm.erkennungsweite_m()` ersetzen | W08 (S4) | `validierung.py` | S | — | `test_redundanz_radius_aus_norm` | 🟩 |
| **F05** | Toiletten-Scope aus Provider/YAML statt hartkodiertem `_TOILETTEN_TYPEN` | W10 (S4) | `sonderstellen_strategy.py`, `normwissen/provider.py` | S | — | `test_toiletten_scope_single_source` | 🟩 |
| **F06** | Getrennter-Sicherheitskreis-Prüfung von Warnung auf Hard-Stop (Kernmission) | W13 (S3) | `validierung.py` | S | — | `test_getrennter_kreis_hardstop` | 🟩 |
| **F07** | ≥2-Leuchten-Redundanz: Platzierungs-Garantie je Abschnitt + Prüf-Hard-Fail | W19 (S2) | `deckung.py`, `validierung.py` | M | F04 | `test_redundanz_garantie_und_hardfail` | 🟩 |
| **F08** | `erkennungsweite_m` im place()-Pfad verdrahten ODER sichtlinie-Pfad als deaktiviert dokumentieren | W17 (S3) | `platzierer.py`, `anker_strategy.py` | M | F03 | `test_erkennungsweite_im_prod_pfad` | 🟩 |
| **F09** | Wartungsfaktor bereichsabhängig innen 0,80 / außen 0,57 (Referenz-Praxis, Fallback Single-WF) | W07 (S3), A1 F02 | `normwissen/data/en1838_grundwerte.yaml`, `provider.py`, `deckung.py` | M | F02 | `test_wf_innen_aussen` | 🟨 |
| **F10** | Blendungsgrenzen f(h) als Norm-Werte + QA-Prüfung (Treppe = jeder Winkel) | W04 (S3) | `normwissen/data/*.yaml`, `validierung.py` | M | Enis-cd-Werte | `test_blendung_grenze_je_hoehe` | 🟨 |
| **F11** | Antipanik-Flächen-Trigger 60/8 m² als **Referenz-Praxis** füllen (nicht Norm-Default, OVE-scope-gated) | W11 (S3), A1 F15 | `normwissen/data/ove_e8101_zusatz.yaml`, `flaechen_strategy.py` | M | — | `test_antipanik_trigger_referenzpraxis` | 🟨 |
| **F12** | Seitenselektiver Randbereich (nur Längsseiten, Stirn bis Tür) statt umlaufend | A3-Randbereich (S3) | `lux.py`, `deckung.py` | M | — | `test_randbereich_seitenselektiv` | 🟨 |
| **F13** | Stiege podest-gestaffelte Montagehöhe + 10-m-Warnung (statt fixem Floor) | W01 (S2), A1 F07/08 | `provider.py`, `flaechen_strategy.py`/`communal_stgh_strategy.py` | M | — | `test_stiege_podest_hoehe` | 🟨 |
| **F14** | Grün=RZ / Gelb=SL Layer-Trennung (Referenz-Praxis) — Abgleich mit bereits gebautem astv-fremdem Stand | W06 (S4), A1 F18 | `render/dxf_renderer.py` | S | — | `test_layer_gruen_gelb` | 🟨 |
| **F15** | `decision_source`-Feld am Contract (echter Audit-Trail statt Praxis-Präfixe in `norm_quelle`) | norm_quelle-Naht 🟡 (S3) | `hauptengine/contracts/**` (+Bump+Schema) | L | 3-Owner | `test_decision_source_trail` | 🟦 |
| **F16** | `sonderstellen`/Möbel/Flags aus Selmans Provider produzieren (§4.1.2 h/i + Verschattung) | W12/W03 (S3), Naht 🔴 | `raumerkennung/**` | L | Selman | `test_provider_liefert_sonderstellen` | 🟦 |
| **F17** | Vertikaler Rettungsweg-Nachweistyp an Objekthöhen (horizontal bleibt Pflicht) | W02 (S3), A1 F05 | `lux.py`, contracts? | L | F15? | `test_vertikaler_nachweis` | 🟦 |
| **F18** | Totes YAML entscheiden: `platzierung_regeln.yaml`/`regel_deckung.yaml` verdrahten ODER als Doku/Contract deklarieren | W18 (S4) | `normwissen/**`, docs | M | 3-Owner | `test_platzierung_regeln_konsumiert` | 🟦 |

## Nicht-Fixes (aufgelöst als „so lassen")
- **W15** a/b-Tabellen-Lookup ist **DE-only** → wird NICHT Default; die analytische Bisektion der Engine
  bleibt. Kein Fix, dokumentiert.
- **id()-Cache (A3 c):** existiert nicht — nichts zu tun.
- **Fixture-Drift (A3 d):** keine — nichts zu tun.

## Mein Vote (Reihenfolge diese Runde)
**Block 1 — Korrektheit/Drift (🟩, keine Fremd-Lane, keine Contracts):** F01 → F02 → F03 → F04 → F05 → F06.
Das schließt den einen echten Datenfehler (WF-Divergenz), härtet Kernmission (getrennter Kreis) und
entfernt die Konstanten-Drift. Klein, testbar, risikoarm.

**Block 2 — Norm-Aktivierung (🟩):** F08 (erkennungsweite im Prod-Pfad) → F07 (Redundanz-Garantie).
F07 ist S2, aber Verhaltensänderung (Platzierung dichter) → nach F08, mit E2E-Sichtprüfung.

**Block 3 — Lichtberechnung (🟨, Enis-YAML abstimmen + HANDOFF_B_ENIS.md):** F09 (Außen-WF) → F11
(Antipanik-Trigger) → F12 (Randbereich) → F13 (Stiege) → F10 (Blendung, braucht Enis-cd-Werte) → F14 (Layer).

**Block 4 — NICHT diese Runde (🟦, an Owner):** F15 (decision_source, 3-Owner-Contract), F16
(Selman-Provider für sonderstellen/Möbel/Flags), F17 (vertikaler Nachweis), F18 (totes YAML — Owner-Entscheid).
Grund: echte Fremd-Lane-Arbeit (Selman) bzw. 3-Owner-Contract — Leonis darf nicht einseitig.

**Empfehlung:** Block 1 + Block 2 fest zusagen (10 Fixes, alle 🟩, in-Lane). Block 3 nur mit deinem OK,
weil er `normwissen/data` berührt (protokolliere ich für Enis). Block 4 als Handoff an Enis/Selman
formulieren, nicht implementieren.
