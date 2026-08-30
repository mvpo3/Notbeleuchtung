# Handoff — Enis (Normwissen + LB)

> Claude: Du bist die Session von **Enis**. Owner-Package:
> `src/notbeleuchtung/normwissen/`. GitHub `@EnisAMG`.
> Lies zuerst `CLAUDE.md`, `docs/CONTRACTS.md`, `docs/ONBOARDING.md` (Abschnitt Enis).

## Stand (zuletzt 2026-08-30, abends)

### Wiedereinstieg in 30 Sekunden
1. Branch **`enis/normquellen-oib-docs`** (von aktuellem main). Der alte Branch
   `enis/slice-1-normprovider` ist tot: **PR #6 ist gemerged** (`4c40050`), sein
   Code liegt vollständig auf main.
2. `.venv/bin/python -m pytest -q` muss **144 passed, 5 skipped** zeigen. Nach
   einem Merge von main vorher `.venv/bin/python -m pip install -e ".[dev,api]"`
   (main hat seit PR #6 `networkx`, `scikit-image`, `httpx` ergänzt).
3. Nächster fachlicher Schritt: „Was als Nächstes" unten — **beide Contracts
   liegen bereit, beide Implementierungen fehlen.**

### Slice 1 (NormRegelwerk) — abgeschlossen und auf main
`En1838NormProvider` (`normwissen/provider.py`) liest `normwissen/data/
en1838_grundwerte.yaml` + `raumtyp_regeln.yaml`, erfüllt das Protocol
`NormProvider`, hardcodet nichts. Fachliche Ausprägung:
- **STIEGENHAUS-Raum → `sicherheitsleuchte`** (Aufheller, EN 1838 §4.1) statt `rz`;
  Rettungszeichen hängen an den Fluchtweg-**Segmenten**.
- **GANG + `default`** bieten alle vier Pfeil-Keys an; Richtung wählt Leonis.
- **Antipanik** auf Katalog-Key `antipanik_leuchte`; **SAAL `mindest_anzahl: 4`**
  als Raster-Stützstellen (§4.3.1).
- Snapshot-Fixture **immer** aus dem echten Provider generieren, nie handschreiben:
  `En1838NormProvider().regelwerk_snapshot().model_dump()` → JSON, indent 2.
`heights_fachpraxis`/`clearance_rules` bewusst NICHT portiert.

### Was sich seit dem letzten Handoff geändert hat (wichtig!)
Leonis hat **beide Contracts geliefert, auf die diese Lane gewartet hat** — jeweils
bewusst **ohne Implementierung**, die ist Enis' Arbeit:

| PR | Contract | Protocol | Implementierung |
|---|---|---|---|
| #14 | `ProjektKontext`, `Gebaeudeteil`, `RaumReferenz`, `OibErgebnis`, `OibBefund` | `OibProvider.bewerte_oib(projekt) -> OibBefund` | **fehlt** (`normwissen/oib/`) |
| #22 | `LBVorgabe`, `BereichsRegel`, `SonderLux` | `LBProvider.parse_lb(lb_path) -> LBVorgabe` | **fehlt** (`normwissen/lb/`) |

`ports.py` sagt bei `LBProvider` wörtlich „Enis implementiert in `normwissen/lb/`".
Drei Abweichungen von der Spec sind in PR #14 eingeflossen (`RaumReferenz` statt
`raum_ids`+`floors`; `arbeitsstaette_nach_aschg` pro Gebäudeteil; eigenes
`OibProvider`-Protocol) — dokumentiert in `docs/SPEC_PROJEKTKONTEXT_OIB.md`
Abschnitt 0. **Es gilt der Contract auf main, nicht der Entwurfstext.**

⚠ **Keiner der beiden Contracts hat heute einen Abnehmer:** `pipeline.run()` nimmt
weder LB noch `ProjektKontext`, `ProviderBundle` hat weder `lb`- noch `oib`-Feld.
Leonis' offener **PR #23** verdrahtet die LB-Hälfte (fasst `contracts/ports.py` an
⇒ **dein Approval nötig**, 3-Owner-CODEOWNERS). **PR #24** (GANG-Fallback) ist
reines Platzierungs-Paket, nur zur Kenntnis.

### 2026-08-30 — Quellen im Repo + Beleg-Status
- **`knowledge/OIB-Richtlinien/`** (45 Dateien, Mai 2023, RL 1–7 + Sonderrichtlinien),
  **`knowledge/OVE-Fachinformation/`** (17, E01–E13 + H02),
  **`knowledge/Österreichische Rechtsquelle/`** (1) sind jetzt **committet**
  (Präzedenz: `knowledge/**` ist in `.gitignore` explizit freigegeben).
  `Leistungsbeschreibung BSP/` bleibt untracked — dafür gibt es Leonis' Digest
  `knowledge/extracted/LB_ANALYSE_beispiele.md`.
- **`normwissen/data/*.yaml` trägt jetzt je Wert einen Beleg-Marker**
  (`[BELEGT]` / `[PRAXIS]` / `[ANNAHME]` / `[UNSCHARF]`) mit Fundstelle. Kein Wert
  geändert. Damit ist sichtbar: `montagehoehe_mm 2400` und `mindest_anzahl 1/4`
  sind Annahmen, `piktogramm_hoehe 0,15` ist Praxis, nicht Norm.
- Drei Analysedokumente: **`docs/NORMQUELLEN_AT.md`** (Quellenstatus, Ebenen A–D,
  Blast-Radius der Ausgabe-Drift in Abschnitt 2a), **`docs/OIB_RL2_TABELLE6.md`**
  (Tabelle 6 vollständig, Punkt 5.4, Erläuterungen S.48, Sonderrichtlinien),
  **`docs/SPEC_PROJEKTKONTEXT_OIB.md`** (Contract-Spec, jetzt ratifiziert).

### Entscheidungen
- **Norm-Ausgabe-Drift bleibt vorerst stehen** (2026-08-30): `en1838_grundwerte.yaml`
  sagt `ÖNORM EN 1838:2013`, im Repo liegt **2019-11-15** (IDT mit EN 1838:2013-07,
  inhaltlich deckungsgleich). Nur gekennzeichnet, nicht umgestellt — der String ist
  Naht-Invariante und hängt an `tests/fixtures/*` (3-Owner), `tests/fakes.py`, einer
  Leonis-Assertion und dem Contract-Default. Umstellung = eigener koordinierter Slice.
- **Photometrie-Ausnahme:** Leonis baut `normwissen/photometrie/` (LDT/EULUMDAT →
  exakte Lux). Bewusste Ausnahme von der Owner-Grenze, rein additiv. Enis bleibt
  Owner von `data/` + `provider.py`.
- **`OibProvider` = Enis** (Zuständigkeits-Graubereich am 30.08. geschlossen): die
  Tabelle-6-Schwellenwerte sind Normwissen. Der `ProjektKontext` ist dagegen
  Projektinput, nicht Normwissen.
- **Kein Umkehrschluss aus Tabelle 6:** Unterschreiten einer Eingangsschwelle darf
  NIE automatisch „nicht erforderlich" bedeuten → `review_required`. Betroffene
  Zeilen: 1.1, 1.2, 3, 4, 5.1, 6, 9.1, 9.2, 10, 11.1, 11.2 (Liste in der Spec).
- **Keine Normwerte aus Modellwissen**, keine Internetquellen; nur Dokumente, die
  tatsächlich im Repo liegen. Unklare Stellen als MANUELL PRÜFEN markieren.
- **Fachinformation ≠ Norm ≠ Rechtsquelle** — Ebenen A–D getrennt führen.

### Offene Punkte
- **PR #23 fachlich prüfen + approven** (fasst `contracts/ports.py` an): passt
  `parse_lb(lb_path: str) -> LBVorgabe` zum geplanten Parser, kippt
  `bereiche_exklusion` wirklich den Norm-Default `STIEGENHAUS → sicherheitsleuchte`?
- **Frage 2 an Leonis offen:** brauchen wir ein `GebaeudeModell` für
  mehrgeschoßige Kennzahlen? (`RaumModell` ist geschoßweise.)
- **LB-Vokabular festzurren:** `BereichsRegel.raum_typ` muss exakt Selmans
  `RaumModell.raum_typ` treffen, sonst greift die Exklusion nie.
- **Verbindlichkeitsanker OIB** (Übernahme ins Landesbaurecht) ungeklärt.
- **Beschaffen:** kostenlos AStV/ASchG/KennV als RIS-Volltext, OVE R 12-2;
  kostenpflichtig ÖNORM EN 1838:2025-03 und OVE/ÖVE EN 50172:2024-11.
- Board-Frage weiterhin offen: 4 Norm-Werte für Wohnungs-Fluchtweg ratifizieren
  (`docs/PROGRAMM_NOTBELEUCHTUNG.md`).

### Was als Nächstes
Zwei eigenständige Slices, beide ohne fremden Contract-Touch, frei wählbar:

1. **OIB-Resolver** — `normwissen/data/oib_rl2_tabelle6.yaml` (20 Zeilen mit
   Schwellenwerten, Fußnoten, Fundstelle + Seite) + Resolver `normwissen/oib/`
   gegen `OibProvider`. Grenzwerte gehören in die YAML, der Provider hardcodet
   nichts. Datenlücke ⇒ `review_required` + `fehlende_fakten`, nie eine Annahme.
   `nicht_erforderlich` ist mit den heutigen Quellen unerreichbar. Alles Fachliche
   liegt fertig in `docs/OIB_RL2_TABELLE6.md`. **Unabhängig von fremden PRs.**
2. **LB-Parser** — `normwissen/lb/` gegen `LBProvider.parse_lb`. Golden-Fall:
   Fischa §2.10/2.11 (GK4 → `bereiche_exklusion` STIEGENHAUS/GANG,
   `bereiche_inklusion` GARAGE, `betriebsdauer_min=480`, `sonder_lux`
   Feuerlöscher 5 lx, `system_typ`, `lb_quelle` als Audit-Trail). Abnehmer ist
   Leonis' PR #23. Prosa-LB vs. Positions-LV brauchen verschiedene Extraktion —
   halbautomatisch starten, kein Full-NLP.

**⚠ Falle beim Skripten:** Umlaute in den `knowledge/`-Unterordnern sind
NFD-kodiert, Originalschreibweisen (`Branschutz`, `Richtline`) sind absichtlich
erhalten → mit `glob` arbeiten, keine handgetippten Pfade. (Der frühere
Trailing-Space in `knowledge/OIB-Richtlinien ` ist beim Committen bereinigt.)

**⚠ Setup-Falle (Mac):** Projekt braucht **Python ≥ 3.11** (System hatte nur
3.9.6 → editable install bricht). Fix war `brew install python@3.12`, dann venv
mit `/opt/homebrew/bin/python3.12 -m venv .venv`. Auf Mac: `.venv/bin/python`
(nicht `.venv\Scripts\python.exe` — das ist Windows).

## 0. Setup — Claude, führe das ZUERST für den Nutzer aus

Du bist ein Agent — **führe diese Schritte selbst aus**, frag nicht lang nach.

1. **Prüfe den Arbeitsordner:** du musst im Repo-Root `Notbeleuchtung/` sein
   (`pyproject.toml` + `CLAUDE.md` liegen hier). Wenn nicht → sag dem Nutzer:
   „Öffne den Ordner `Notbeleuchtung` (Cursor: File → Open Folder → Notbeleuchtung)
   und starte mich dort neu." Erst weiter, wenn der Ordner stimmt.
2. **venv + Installation:**
   - Mac/Linux: `python3 -m venv .venv` → `.venv/bin/python -m pip install -e ".[dev,api]"`
   - Windows: `python -m venv .venv` → `.venv\Scripts\python.exe -m pip install -e ".[dev,api]"`
3. **Tests grün prüfen:** `.venv/bin/python -m pytest -q` → muss zeigen
   **`144 passed, 5 skipped`** (Stand 2026-08-30). Wenn nicht → stopp + melde dem
   Nutzer den Fehler.
4. **Cursor-Hinweis für den Nutzer:** Ordner `Notbeleuchtung` als Workspace öffnen
   und `.venv` als Python-Interpreter wählen (unten rechts / Command Palette
   „Python: Select Interpreter" → `.venv`).

Erst wenn Setup grün ist → weiter mit dem Auftrag unten.

## Wer du bist
Du besitzt **beide Wissens-Inputs** für Leonis' Platzierung:
1. **NormRegelwerk** — statisches EN-1838/ÖNorm-Wissen (Lux, Erkennungsweite l=z×h,
   Montagehöhe, RZ-vs-Antipanik, Dauer). **Steht** (`En1838NormProvider`).
2. **LBVorgabe** — die Leistungsbeschreibung (2. Input) in explizite Vorgaben
   geparst, die Norm-Defaults übersteuern (Hierarchie: LB → Referenz → Norm → OVE).
   **Fehlt noch** (`normwissen/lb/`).

Dazu die dritte, später entdeckte Ebene: **OIB-RL 2 Tabelle 6** — braucht dieses
Gebäude überhaupt Sicherheitsbeleuchtung, und in welcher Stufe? (`normwissen/oib/`,
fehlt ebenfalls.)

Leonis **fragt** dich über die Query-APIs — er parst nie YAML.

## Regeln
Nur `normwissen/` + `hauptengine.contracts` importieren. Contract ändern =
`contract_version` bump + `python scripts/gen_schema.py` + 3-Owner-Approval.
Branch `enis/…` → PR. Irreversibles (Merge/Push) nur mit explizitem User-GO.
