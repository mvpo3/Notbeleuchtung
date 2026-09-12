# Handoff — Selman (Raumerkennung)

> Claude: Du bist die Session von **Selman**. Owner-Package:
> `src/notbeleuchtung/raumerkennung/`. GitHub `@polatselman`. Task: **Issue #3**.
> Lies zuerst `CLAUDE.md`, `docs/CONTRACTS.md`, `docs/ONBOARDING.md` (Abschnitt Selman).

## 0. Setup — Claude, führe das ZUERST für den Nutzer aus

Du bist ein Agent — **führe diese Schritte selbst aus**, frag nicht lang nach.

1. **Prüfe den Arbeitsordner:** du musst im Repo-Root `Notbeleuchtung/` sein
   (`pyproject.toml` + `CLAUDE.md` liegen hier). Wenn nicht → sag dem Nutzer:
   „Öffne den Ordner `Notbeleuchtung` (Cursor: File → Open Folder → Notbeleuchtung)
   und starte mich dort neu." Erst weiter, wenn der Ordner stimmt.
2. **venv + Installation:**
   - Windows: `python -m venv .venv` → `.venv\Scripts\python.exe -m pip install -e ".[dev,api]"`
   - Mac/Linux: `python3 -m venv .venv` → `.venv/bin/python -m pip install -e ".[dev,api]"`
3. **Tests grün prüfen:** `.venv\Scripts\python.exe -m pytest -q` → muss zeigen
   **`13 passed, 1 skipped`**. Wenn nicht → stopp + melde dem Nutzer den Fehler.
4. **Cursor-Hinweis für den Nutzer:** Ordner `Notbeleuchtung` als Workspace öffnen
   und `.venv` als Python-Interpreter wählen (unten rechts / Command Palette
   „Python: Select Interpreter" → `.venv`).

Erst wenn Setup grün ist → weiter mit dem Auftrag unten.

## Wer du bist
Du machst den **1. Input**: leerer Architekturplan (DXF/DWG) → **RaumModell**
(Räume/Türen/Ausgänge/Fluchtweg-Zirkulation). Reine Geometrie/Topologie — KEIN
Norm-Urteil (das macht Enis/Leonis). Dein Contract: `RaumModell`
(`hauptengine/contracts/raum_modell.py`), dein Protocol: `RaumProvider`.

## Dein Auftrag — Slice 4 (größter Port, deshalb solide angehen)
Das Port-Material liegt schon im Repo (Leonis hat es gestaged, du hast keinen
elektro-planer-Zugriff): **`raumerkennung/_port/`** (~14,4k LOC — `parsers/`,
`engine_walls/`, `models/`). Es ist ROH und läuft noch nicht (alte Imports). Deine
Aufgabe (Details: `raumerkennung/_port/README.md`):

1. **Imports umbiegen** auf die neue Struktur (`engine.walls` → `._port.engine_walls`,
   `parsers.x` → `._port.parsers.x`).
2. **`config.py`-Kopplung brechen:** harte Mollgasse-Pfade (`CANONICAL_BLANK_DIR`,
   Referenz-DXF) optional/`.env`; nur `RULES_DIR`/`resolve_rule_path` behalten.
3. **Zirkular-Import** `keller_geometry` ↔ `architecture_dxf` sauber trennen.
4. **`ArchitekturRaumProvider.parse(dxf, floor)`** (`raumerkennung/provider.py`)
   erfüllt `RaumProvider` → liefert ein `RaumModell`, schema-gleich zu
   `tests/fixtures/raum_modell_4og.json`. Test-Pläne: `Projekte/`.
5. **Fake ersetzen:** `tests/fakes.py` `FakeRaumProvider` → echt; E2E mit echter
   4OG-DXF grün.

**Tipp:** nicht alles auf einmal. Erst `architecture_dxf` + `keller_geometry`
importierbar machen → Räume/Türen extrahieren → dann Fluchtweg-Zirkulation
(`segmente`) füllen. Zwischendrin `pytest -q` grün halten.

**DoD:** echtes RaumModell aus 4OG-DXF, schema-identisch zur Fixture;
`tests/contract/test_raum_modell_contract.py` grün.

## Regeln
Nur `raumerkennung/` + `hauptengine.contracts` importieren (der `_port`-Code darf
intern untereinander importieren). Contract ändern = version bump + gen_schema +
3-Owner-Approval. Branch `selman/…` → PR.

## STAND (append-only, neueste oben) — für nahtloses Weitermachen

---

## ═══ SELMAN: HIER WEITER (Stand 2026-09-12, Bereinigung + SCHLEUSE) ═══

**Branch:** `selman/extents-ausreisser`, **gepusht**, **neuer PR als Nachfolger
von #152** (das war am 2026-09-10 23:31 UTC von @EnisAMG gemerged, ein Push
aktualisiert es nicht mehr), **kein Merge**. Commits dieser Runde: `731a7d5`
(WIP-Sicherung der Übersichtskarten vor dem Sync) · `804e6af` (Merge
`origin/main`) · `64527f0` (BRANCH_PROTECTION § 7) · `7d41907` (Enis' Auflagen
A/B) · `96dcef6` (SCHLEUSE + Kürzel-Auflösung) · `6ebf676` (**Bereinigung +
Contract `raum_modell` 1.5.0**) + Abschluss-Commit.

**⚠️ CONTRACT-TOUCH:** `raum_modell` 1.4.0 → **1.5.0**, additiv
(`Raum.polygon_roh`, `Raum.bereinigung[]`), Schema regeneriert. Der Check
`contract-freeze` verlangt das Approval **aller drei** Owner auf dem aktuellen
`head_sha` — **jeder nachgeschobene Commit entwertet ein erteiltes Approval.**
Also: erst alles fertig, dann Approvals einsammeln.

**Suite:** `1264 passed, 10 skipped, 2 deselected, 12 xfailed, 2 warnings in 1181.23s (0:19:41)`, exit 0, keine XPASS-Zeile · Prüfstrecke über alle fünf Pläne **ohne Parallellast**,
exit 0, 251,0 / 286,2 / 1813,0 / 56,8 / 51,7 s = 2459 s · `test_soll_muthgasse`
9 passed / 4 xfailed / **0 XPASS** · Riegel + Bereinigung + Kürzel 49 passed ·
`ruff` clean · `gen_schema --check` in sync.

**Leitregel unverändert:** *der Code erfindet keine Maße und keine Typen.* Neu
dazu: **er löscht auch keine Flächen unbelegt** — jeder Abzug der Bereinigung
ist mit Regel und Gegenspieler gebucht, die Bilanz geht exakt auf
(0,000000 mm² unbucht).

**Was diese Runde erledigt hat (Details: `docs/ENIS_UEBERGABE_0908.md`
§§ 19 + 20 + 21):**

1. **Bereinigung der Raumüberlappungen umgesetzt** (§ 14.6/§ 14.6.1, neues
   Modul `raumerkennung/bereinigung.py`, 430 Zeilen, 24 eigene Tests):
   **62 von 62 Überlappern gelöst**, doppelt belegte Fläche **262,342 m² →
   0,39 mm²**, kein Restpaar > 1 mm². Regel für Regel: Regel 1 löst 1,
   +Regel 2 → 16, +Regel 3 → **62**, Regel 4 nur Mikroflächen, **Regel 5 greift
   in null Fällen**. 5 Räume entfallen (Restkörper < 1 m², Σ 1,7494 m²),
   14,829 m² Zerfall-Nebenkomponenten — beides gebucht und namentlich im
   Bericht. Riegel-Bänder auf (0, 0.0) nachgezogen, **plus neue löschungsfeste
   Untergrenze `BAND_RAEUME` 47/62/101/21/14**.
2. **Muthgasse gesondert:** der einzige verschluckte LIFT ist weg (`raum_88` ⊃
   `raum_79`, 97,6 % → kein Fall). Die **Ursache** bleibt sichtbar, nicht
   behoben: 11 der 12 geänderten Muthgasse-Räume sind F-Flutungen
   („Wohnküche"), `raum_88` behält 3,82 m² gegen 39,70 m² Stempel.
3. **SCHLEUSE entschieden umgesetzt, nur für `E2-VF-11a`**: Kanon-Typ +
   Nutzungsklasse `ALLGEMEIN_ERSCHLIESSUNG`, `regel_deckung.yaml` `offen`
   (Owner Enis). `Schl.` typisiert **nur** mit Zusatzbeleg UND eingetragener
   Owner-Entscheidung; `raum_67` bleibt untypisiert mit Hinweis im Prüfbericht.
   Gemessen und wichtig: die In-Plan-Belege trennen die beiden Räume **nicht**
   (die alten „0 mm / 8,2 m"-Angaben sind korrigiert) — der Unterscheider ist
   das Vergleichsgeschoss (E8 627 mm, E9 10 mm von `raum_65`).
4. **Enis' CODEOWNERS-Patch übernommen und unabhängig nachgeprüft**
   (Kommentar in #152, Zahlen dort), **BRANCH_PROTECTION § 7** trennt die zwei
   offenen Punkte (Workflow-Umstellung vs. Required Status Check).
5. **Enis' zwei Auflagen dokumentiert** (`docs/OFFENE_FRAGEN.md`): A mit
   Erzeuger-Codestelle und lauffähiger Test-Skizze (2 passed / 2 strict-xfail),
   B mit der gemessenen Null (`STANDARDWERT` 0 von 612 Türen) und dem
   Streich-Vorschlag. **PR #154 geprüft, kein Approval** — vier belegte Mängel
   bei „fehlende Messung = None", die anderen drei Punkte passen.

**NÄCHSTER PUNKT: die vier offenen Owner-Entscheidungen, nicht neuer Code.**

- **Regel-Reihenfolge (d):** § 14.6.1 ordnet die Restflächen-Regel an Position 2,
  umgesetzt ist sie zuletzt — sonst unterläuft sie „LIFT und SCHACHT werden
  IMMER ausgestanzt" (4 der 5 LIFT/SCHACHT-Räume kommen aus dem R-Zweig, zwei
  davon nur 0,15 m² über der Entfall-Schwelle). Im Docstring deklariert,
  Wirkungsunterschied gemessen.
- **Regel 2 vor Regel 3:** kostet genau einen Fall — `raum_29` (L mit Stempel)
  fällt auf −15,6 %, weil `raum_91` (F) zu 99,97 % darin liegt. Ein-Zeilen-
  Alternative gerechnet, nicht umgesetzt.
- **Muthgasse-Türband:** Türen 291 → 270, **ausschließlich** Kontaktzonen-
  Durchgänge (`durchgang_*` 169 → 148, `tuer_*` unverändert 121). Band **nicht**
  abgesenkt, sondern als eigener strict-xfail `test_soll_tuerzahl_band` mit
  Beleg; Räume/Segmente/Stiegenhäuser bleiben scharf. Entscheidung: Band
  fachlich auf „Türen ohne Kontaktzonen-Durchgänge" umstellen oder bei ≥ 280
  als Zielbild führen?
- **Ursache im F-Zweig** (`flute_stempel` bekommt `belegte` nicht übergeben,
  Punkt 2 der Skizze § 14.6): weiterhin offen. Die Bereinigung ist die
  nachgelagerte Auflösung.

**Offen an @EnisAMG:** `E2-VF-11b` (`raum_67`) — Entscheidungsvorlage liegt ·
Notbeleuchtungsanforderung SCHLEUSE (`regel_deckung.yaml`) · Auflage A beim
ersten `lichte_mm`-Erzeuger · Auflage B (`STANDARDWERT` streichen?) ·
**Approval für `raum_modell` 1.5.0** und das weiterhin ausstehende für 1.4.0 ·
die vier Mängel in #154 · die drei älteren Vokabular-Fragen und die
Mollgasse-„Laubengang"-Frage.
**Offen an @mvpo3:** **Branch Protection auf `main`** (heute nachgemessen:
`protection` 404, `rulesets` 403, Token `admin:false`) · **Bbox-Mitte sieht ein
Schlitz-Loch nicht** (`platzierung/geometry.py:226`; betroffen heute genau
`Mollgasse raum_51`) · **Modell-Restüberlappung** Muthgasse 12 / 38,279 m²,
Barawitzka 4 / 7,131 m² aus `stiegenhaus_*`/`lift_*` · **`SCHACHT`-Lücke** in
`lift_erkennung.py:171` (`Barawitzka lift_2` ⊃ `rest_3` zu 100 %) · die
Flächenschwellen rechnen ab jetzt mit der **bereinigten** Fläche ·
**Approval für `raum_modell` 1.5.0**.

**Mess- und Prüfskripte dieser Runde** (Session-Scratchpad
`C:/Users/selma/AppData/Local/Temp/claude/D--KI-Projekt/15c400f4-f6ff-4226-8584-4bd9ac336bc7/scratchpad`,
alle nur lesend): `_nachmessung.py` (Riegel-Basis, `BAND_RAEUME`, Muthgasse-
Verschluck, >5 %-Bilanz, Entfall-Liste) · `_gp_leck.py` (Flächenbilanz) ·
`_gp_pruef.py`, `_gp_reihenfolge.py` (Determinismus, Regelreihenfolge) ·
`_schl_*.py` (Schl.-Inventar inkl. Vergleichsgeschosse) · `_tuer_ist.py` +
`_tuer_zaehlen.py` (612 Türen, Breiten-Herkünfte) · `_gegenprobe`-Aufbau für die
14 CI-Tests am alten Skript. Rohlogs: `_pruefstrecke.log`, `_suite_vorher.log`,
`_suite_nachher.log`, `_suite_final.log`, `_nachlauf_muthgasse.log`.
Im Repo dauerhaft: `scripts/analyse/ueberlappung_regeln.py` (kumulative
Regel-Messung, Akzeptanzkriterien (a)–(d) prüft es selbst).

---

## ═══ SELMAN: HIER WEITER (Stand 2026-09-11, Übersichtskarten-Sweep) ═══

**Branch:** `selman/extents-ausreisser`, **PR #152 offen, kein Merge, kein Push.**
**Kein Code in `src/` geändert**, `hauptengine/contracts/**` unberührt, keine
Contract-Änderung. Neu ist genau ein dauerhaftes Skript + Ausgabe-Artefakte.

**Was diese Runde gebaut hat:**

1. **`scripts/analyse/uebersicht_karte.py`** (neu) — eine Übersichtskarte je Plan:
   `uebersicht.png` (Räume nach Kategorie eingefärbt: Wohnräume / Sanitär / sonstige
   typisierte / Außenflächen / Gänge / Stiegenhäuser / Schächte+Lifte / **untypisiert
   magenta schraffiert**, dazu Innenhöfe, Wohnungen farbcodiert, Ausgänge nach
   `Ausgang.typ`, Fluchtweg-Segmente, verschluckte Räume), `uebersicht.json`
   (maschinenlesbar) und `uebersicht.md` (Kennzahlen + Abschnitt „nicht erkannt“).
   **Wiederverwendet `scripts/plan_pruefen.py`** (`import plan_pruefen as pp`) für
   Ladepfad, Rotation, Maßstab, Farbwahl und die matplotlib-Konventionen — dort war das
   schon gelöst, nichts davon wurde neu erfunden. Argument `--name <Ausgabename>` gibt dem
   Ausgabeordner einen lesbaren Namen; `dxf:` in JSON/MD führt weiter den echten
   Originalpfad. ruff sauber.

2. **Sweep über alle Pläne:** 63 gerechnet, **62 ok, 1 nicht auswertbar**. Rund **133 min**
   Wanduhr (111,2 min bei 2 parallel + 22,2 min zwei serielle Nachläufe), 219,9 min CPU.
   Ausgabe `Projekte/_uebersicht/<plan>/`; die **17 fertigen Elektro-/Notbeleuchtungspläne**
   (Ergebnisbeispiele, enthalten bereits Leuchten — **keine** leeren Architekturpläne)
   getrennt unter `Projekte/_uebersicht/_elektro_beispiele/<plan>/`.

3. **`Projekte/_uebersicht/INDEX.md`** — eine Zeile je Plan (Projekt / Geschoss / Pfad /
   Räume / untypisiert / Wohnungen / Stiegenhäuser / Gänge / Innenhöfe / Schächte+Lifte /
   final_exit / stair_exit / Fluchtwegsegmente), nach Projekt gruppiert, Summenzeile je
   Projekt und über alles, Elektro-Gruppe in eigenem, als solchem gekennzeichnetem
   Abschnitt. Dazu die Abschnitte **„Was die Karte NICHT zeigt“** und **„Auffälligkeiten“**.

**Zahlen (Σ, aus den 62 `uebersicht.json`):** Architektur (45 Karten) 3507 Räume · 666
untypisiert · 348 Wohnungen · 127 Stiegenhäuser · 403 Gänge · 53 Innenhöfe · 140
Schächte+Lifte · 77 `final_exit` · 75 `stair_exit` · 2422 Fluchtweg-Segmente. Elektro-
Beispiele (17 Karten) 2681 / 404 / 151 / 91 / 463 / 33 / 38 / 30 / 120 / 2425.

**Die harten Befunde (Details in INDEX.md, Abschnitt „Auffälligkeiten“):**
- **7 Pläne mit 0 erkannten Ausgängen:** `Barawitzka_2DG`, `Barawitzka_FDM`,
  `Barawitzka_KG`, `Herrenholz_OG1`, `Herrenholz_OG2`, `Herrenholz_UG`, `Rennweg_OG2`.
  Härtester Fall `Herrenholz_OG1`: 300 Räume, 640 Türen, 55 Segmente, **kein** Ausgang.
- **Untypisierung häuft sich in UG/KG:** `BaufeldE2_NB_UG` 237/266 · `Mollgasse_KG1` 24/31 ·
  `Fischamend_E_UG` 30/43 · `Barawitzka_KG` 28/41 · `Mollgasse_KG2` 19/30 ·
  `Fischamend_BT1_UG` 21/44 · `Rennweg_UG` 10/23. Absolut größter: `Herrenholz_EG` mit 244.
- **Verschluckte Räume (>90 % in einem anderen Raum):** `Herrenholz_EG` 257 Paare /
  127 Räume · `BaufeldE2_NB_UG` 201 / 201 · `Barawitzka_KG` 54 Paare bei 41 Räumen.
  Verschluckte **LIFT/SCHACHT**-Polygone: alle acht Muthgasse-Pläne (2–3 je Plan), die
  Fischamend-Obergeschosse (1–2), Barawitzka 1DG/EG (2).
- **Dublette hart bestätigt:** `Herrenholz_UG` und `Herrenholz_OG2` liefern Zeile für Zeile
  identische Werte, 28.284.638 vs. 28.284.639 Byte. Derselbe Plan zweimal. **Welcher das
  echte Geschoss ist, entscheidet der Owner.**
- **`floor`-Feld unbrauchbar:** 43 von 62 Plänen melden `floor == "EG"`. Die Geschoss-Spalte
  im INDEX kommt deshalb aus dem Dateinamen, nicht aus dem Modell. Nicht korrigiert — die
  Erkennung soll nichts erfinden.
- **Renderlast reproduziert (Leonis' Befund):** `BaufeldE2_NB_OG1` / `_OG3` sind bei
  2 parallel mit `MemoryError` in `LineCollection.set_segments` gestorben, seriell dann ok
  (512,5 s / 819,4 s); ein Prozess stand bei 22,3 GB.

**Was NICHT geht / offen ist:**
- **`Aichholzgasse`** (`26_0507_AICH.dxf`, 146 MB, 10 Grundrisse in einem Modelspace) ist
  **nicht auswertbar**: `ValueError: Keine Wand-Entities gefunden — Layer-Muster prüfen.`
  (`dxf_load.py:258`, aus `provider.parse`), Abbruch nach 84,9 s vor dem Render. Die
  Layer-Benennung dieses Büros passt nicht auf die Wand-Muster. Traceback:
  `Projekte/_uebersicht/Aichholzgasse/uebersicht.md`.
- **Die 8 Muthgasse-Karten sind so nicht vorzeigbar.** Zahlen stimmen, PNG nicht: der
  Modelspace enthält mehrere abgesetzte Zeichnungen, der Auto-Zoom umfasst alles, der
  Grundriss sitzt als briefmarkengroßer Fleck oben links, die Legende liegt darüber.
  `pp._varianten_bounds` kennt nur den Barawitzka-Stempel-Prefix → **nächster Schritt:
  eigene Bounds-Heuristik für Muthgasse.**
- **`Baufeld_E2.zip`** (zweite Fassung, gleiche Dateinamen, andere MD5, minimal kleiner)
  ist **nicht** geprüft. Gerechnet wurde `Baufeld_E2_Notbeleuchtungsplaene.zip`.
- **`Barawitzka_FDM`** ist ein Fundamentplan (Ebene −2, 8 Räume, 0 Türen) — als Draufsicht
  mitgerechnet, inhaltlich wahrscheinlich kein Grundriss. Owner-Entscheidung.
- **Sichtgeprüft sind nur 3 PNGs** (`Rennweg_UG`, `Herrenholz_EG`, `Muthgasse_E2`). Die
  übrigen ~59 wurden **nicht** einzeln angesehen — das wird hier nicht behauptet.
- Board-Eintrag mit den Lane-Auswirkungen (@mvpo3 Ausgänge, @EnisAMG Vokabular) steht in
  `docs/COORDINATION.md` unter „## Log“.

---

## ═══ SELMAN: HIER WEITER (Stand 2026-09-10, Abschluss zweiter Block) ═══

**Branch:** `selman/extents-ausreisser`, **PR #152 offen, kein Merge.** Commits
dieser Runde: `f7fb165` (Contract-Freeze-Gate) · `79fc0bb` (Überlappungs-Riegel +
Enis-Frage + Bereinigungsregeln) + Abschluss-Commit. **Kein Code in `src/`
geändert**, `hauptengine/contracts/**` unberührt, keine Contract-Änderung.

**Belege dieser Runde (echte Läufe):**
- Prüfstrecke über alle fünf Pläne **nacheinander, ohne Parallellast**, exit 0 —
  Barawitzka 258,6 s · Mollgasse 290,6 s · Muthgasse 1840,5 s · Rennweg_EG 56,1 s
  · Rennweg_OG3 51,1 s. **Keine Kennzahl bewegt sich** gegen den Lauf `47df2d9`,
  alle fünf `raeume.json` sind **byte-identisch** (`git diff` leer); geändert haben
  sich nur die Laufzeit-Zeile in `bericht.md` und die Render-PNGs. Das ist das
  **erwartete** Ergebnis, weil seit `47df2d9` kein `src/`-Code geändert wurde —
  nicht wegerklärt, sondern gemessen.
- Volle Suite: **`1211 passed, 10 skipped, 2 deselected, 11 xfailed, 2 warnings in
  1153.08s (0:19:13)`**, exit 0, **keine XPASS-Zeile**. Die +11 gegen die 1200 des
  Vorlaufs sind exakt die neuen Riegel-Tests.
- **Kein xfail gedreht, kein Zielband geändert.** Die 11 XFAIL sind unverändert
  dieselben: Barawitzka 3 (FLW-Linien fehlen im Plan / ≥90 % Türen / final_exit
  deckt Endpunkte), Mollgasse 3 (final_exit-Deckung / ≥90 % Türen / final_exit =
  Endpunktzahl), Muthgasse 3 (≥9 stair_exit / ≥1 stair_exit an echter Blocktür /
  ≥90 % Türen), Referenzvergleich 1 (≥80 % Trefferquote), Rennweg 1 (≥90 % Türen).
- `tests/naht/test_ueberlappung_riegel.py` + `tests/contract/test_keine_erfundenen_masse.py`
  einzeln: **`14 passed in 1.32s`**.

**Leitregel unverändert:** *der Code erfindet keine Maße und keine Typen.* Der
AST-Riegel `tests/contract/test_keine_erfundenen_masse.py` setzt die Maß-Hälfte
durch, er wurde nicht umgangen.

**Was diese Runde gebaut hat:**

1. **Contract-Freeze-Gate — Check `contract-freeze`**
   (`.github/workflows/contract-freeze.yml` + `.github/scripts/contract_freeze_check.py`).
   Anlass ist der #149-Vorfall (0 Reviews, 55 nachgeschobene Commits, alter Titel,
   Contract-Bump 1.4.0 auf `main`). Der Check läuft auf `pull_request`
   **inkl. `synchronize`** — das ist der Riegel gegen genau diese Lücke — und auf
   `pull_request_review`. Owner-Logins kommen aus `.github/CODEOWNERS`, kein
   zweiter Pflegeort. Ein Approval zählt nur bei `review.commit_id == head_sha`
   (nicht `submitted_at`); pro Login zählt das jüngste wertende Review. Berührt ein
   PR keine Contracts → **grün**, nicht geskippt, damit er als Required Status
   Check taugt. Gegen echte Daten: **#149 exit 1, #152 exit 0.**
   **ACHTUNG: das Gate allein verhindert nichts.** Auf `main` gibt es **keine
   Branch Protection** (`GET .../branches/main/protection` → **404**), und unser
   Token hat `admin:false`. **@mvpo3 muss sie setzen** — fertige Anleitung inkl.
   `PUT`-Aufruf und den drei Check-Namen `test` / `contracts` / `contract-freeze`
   in **`docs/BRANCH_PROTECTION.md`**.
2. **Überlappungs-Riegel** `tests/naht/test_ueberlappung_riegel.py` (11 Tests,
   0,24 s): Obergrenzen 9/42,3 · 16/45,8 · 37/174,2 · 0 · 0, Summe **62 / 262,3 m²**.
   Steigt eine Zahl → rot; sinkt sie → Band im selben Commit nachziehen. Datenquelle
   sind die eingecheckten `raeume.json` (die DXF sind nicht getrackt).
3. **SCHLEUSE-Frage an @EnisAMG** in `docs/OFFENE_FRAGEN.md` — vollständig belegt,
   **nicht geraten**: `Schl.` = Schleuse (Kanon-Typ + Nutzungsklasse nötig) oder
   Schlafzimmer (`schl → ZIMMER`)? Wirkung gemessen, Falschtrefferrisiko 0.
4. **§§ 17 + 18 in `docs/ENIS_UEBERGABE_0908.md` — beides NUR gemessen, nichts
   umgesetzt.** § 17 Douglas-Peucker 20 mm: 14 149 → 5 740 Punkte (−59,4 %), 0
   ungültige Polygone, 0 MultiPolygon-Zerfälle, Flächenfehler 0,058 % — **aber 17
   von 245 Räumen reißen die 0,5-%-Grenze** (max 1,47 %, ausschließlich kleine
   Räume, 15 davon auf Mollgasse), und als Bereinigung taugt es **nicht**: 62
   bleibt 62 mit identischen IDs, 262,342 → 262,043 m². § 18 Muthgasse: **eine
   Ursache, kein Bündel** — der F-Zweig bekommt `belegte` nicht übergeben; 31 von
   32 relevanten Paaren F↔L, 100 % der Doppelfläche mit F-Beteiligung.
   **Widerlegt**: Rasterauflösung (überall exakt 50 mm), HATCH-Zahl (Barawitzka 6×
   mehr, 2× weniger Doppelbelegung), Layerstruktur (Muthgasse hat die
   zweitwenigsten Layer), Blockverschachtelung (Rennweg tiefer). Zweiter,
   unabhängiger und für die Überlappung folgenloser Mangel: Blattausdehnung
   503,8 × 275,9 m gegen 46,8 × 47,9 m echtes Geschoss → 57,45 Mio Rasterzellen
   Laufzeit und 7 Phantom-Fragmente (27 m²), aber **null Überlapper**.
5. **`Projekte/_ergebnis/VERLAUF.md`** führt die Überlappungszahlen jetzt
   dauerhaft mit (je Plan Überlapper >5 %, doppelbelegte Fläche absolut und in
   Prozent, verschluckte LIFT/SCHACHT, plus Summenzeile).

**NÄCHSTER PUNKT: unverändert die Bereinigung (§ 14.6 / § 14.6.1) — weiterhin
NICHT freigegeben.** Die fünf Owner-Fragen sind offen; die Regelkaskade ist
gerechnet (löst 62 von 62 Fällen, 0 ungelöst, Regel (d) greift im heutigen
Bestand null Mal), aber (e) wäre **contract-berührend** (`polygon_roh`,
`bereinigung`) und der Contract ist eingefroren.

**Offen an @EnisAMG:** die SCHLEUSE-Frage (`Schl.`), die drei älteren
Vokabular-Fragen (`Vorr.`/`Schrankr.`, `SR`/`Aufzug`), die Mollgasse-
„Laubengang"-Frage — und das **weiterhin ausstehende Approval für `raum_modell`
1.4.0**, das mit PR #149 ohne sein Approval auf `main` gelandet ist.
**Offen an @mvpo3:** die **Branch Protection auf `main` setzen**
(`docs/BRANCH_PROTECTION.md`) — ohne sie ist der neue Check nur Dekoration; und
die Überlappungszahlen: `raum_79` (LIFT) liegt zu 97,6 % in `raum_88`
(STIEGENHAUS), 13 Räume liegen zu >90 % ihrer eigenen Fläche in einem anderen,
Leuchten können rechnerisch in verschluckten Polygonen landen.

**Vorbestehend rot, nicht von uns und nicht repariert:** `ruff check .` → 4 ×
`ISC004` in `scripts/plan_pruefen.py:1135,1143,1145,1147`. Die Datei ist in
unseren Commits unverändert; der CI-Job `test` bleibt aus demselben Grund rot wie
bei #149.

**Mess- und Prüfskripte dieser Runde** (Session-Scratchpad
`C:/Users/selma/AppData/Local/Temp/claude/D--KI-Projekt/8fc32369-9bee-42cd-9e07-20d9eeb9eff5/scratchpad`,
alle nur lesend): `_freeze_probe.sh`, `_freeze_stale_probe.py`,
`_s2_regel_umfang.py`, `_p4b_simplify.py`, `_p4b_liste17.py`, `_p4b_delta.py`,
`_m5_struktur.py`, `_m5_zweige.py`, `_m5_cluster.py`, `_m5_fzweig.py`,
`_m5_verteilung.py`, `_s3b_verlauf_overlap.py`; Rohlogs `_s3b_pruefstrecke.log`,
`_s3b_pytest.log`.

---

## ═══ SELMAN: HIER WEITER (Stand 2026-09-10, Abschluss-Runde 3) ═══

**Branch:** `selman/extents-ausreisser`, **nicht gepusht, kein PR, kein Merge** —
der Owner gibt das GO separat. Commits dieser Runde: `fff9f65` +
Abschluss-Commit. **Kein Code in `src/` geändert** (`git diff --stat
47df2d9..HEAD -- src/` ist leer), `hauptengine/contracts/**` unberührt.
**Suite: 1200 passed, 10 skipped, 2 deselected, 11 xfailed, 0 XPASS, 0 failed
(19:29 min), exit 0.**
**Prüfstrecke bewusst NICHT gelaufen** und kein Lauf erfunden: ohne
`src/`-Änderung liefert sie per Konstruktion die Zahlen des Laufs
`2026-09-10 13:35 · 47df2d9`; `Projekte/_ergebnis/VERLAUF.md` bleibt deshalb
unverändert.

**Leitregel unverändert:** *der Code erfindet keine Maße und keine Typen.* Ist
ein `raum_typ` nicht belegbar, bleibt der Raum untypisiert — ein geratener Typ
ist schlimmer als keiner. Der AST-Riegel
`tests/contract/test_keine_erfundenen_masse.py` setzt die Maß-Hälfte durch.

**Was diese Runde geklärt hat (Details: `docs/ENIS_UEBERGABE_0908.md`
§§ 13 + 14 + 15):**

1. **`raum_65` (Muthgasse E2): nicht umgesetzt, xfail bleibt, Band unverändert.**
   Der Raum trägt einen vollständigen `A-AREA-IDEN`-Stempel (`E2-VF-11a` /
   `Schl.` / `13,04 m²` / `Ker.Bel.`), aber `raumtyp_flags('Schl.')` und
   `classify_room('Schl.')` liefern `None` / `UNKNOWN`, deshalb bricht
   `stempel_anker.py:219-221` ab und es entsteht gar kein `Stempel`.
   **Vokabular-Lücke, kein Code-Fehler** — `SCHLEUSE` gibt es im Kanon nicht,
   und Kanon-Typ + Nutzungsklasse sind Enis' Lane. Nebenbefund: der xfail wäre
   ohnehin nicht gefallen, weil `tuer_50` **keine Blocktür** ist (780,5 mm zum
   nächsten `A-DOOR`-INSERT) — Korrektur an § 11.5 / § 12.5 #8 steht in § 13.7.
   Untypisiert über alle fünf Pläne: **50 von 278 Räumen = 18,0 %**.
2. **Überlappende Raumpolygone vermessen — nur berichtet, auf Owner-Wunsch
   NICHTS umgesetzt (§ 14).** **62 von 245 Räumen (25,3 %)** überlappen einen
   anderen um >5 % ihrer eigenen Fläche (Muthgasse 37/101 = 37 %, Rennweg beide
   0); **262,3 m² von 3329,4 m² (7,9 %)** Grundfläche gehören mehr als einem
   Raum. **Ursache ist der F-Zweig (Stempel-Flutung), nicht
   `rest_komponenten.py`:** 96 % der relevanten Paare haben einen F-Raum auf
   mindestens einer Seite, aus dem R-Zweig stammt **kein einziger** Überlapper.
   `flute_stempel` bekommt die belegten Raumpolygone gar nicht übergeben
   (`stempel_flutung.py:227-233`), der F-Zweig hängt ungeprüft an
   (`kaskade.py:110-126`), die H-Dedup misst IoU statt Anteil am kleineren
   Polygon (`kaskade.py:90`). Der R-Zweig blockiert `belegte` im Raster
   (`rest_komponenten.py:147-151`) und hat 0 von 9 Überlappern — das ist der
   Gegenbeweis, dass die Rasterisierung nicht das Problem ist.

**NÄCHSTER PUNKT: die REST-/Überlappungs-Bereinigung (§ 14.6).** Sie ist als
**Vorschlag** ausgearbeitet und **noch nicht freigegeben**. Reihenfolge, wenn
das GO kommt: (1) Riegel zuerst — ein Test, der 62 Überlapper / 262,3 m² als
*Obergrenze* einfriert, plus ein `xfail`-Zielbild mit Sollwert 0 (heute gibt es
**keinen** solchen Test); (2) `flute_stempel` bekommt die belegten Polygone und
blockiert sie im Raster, exakt nach dem Muster aus `rest_komponenten.py:147-151`
— adressiert 94 % der Doppelfläche; (3) Metrik in `kaskade.py:90` um „Anteil am
kleineren Polygon > 0,5" ergänzen (Restposten 2 Paare / 13,9 m²); (4) nachmessen
und Restfälle namentlich belegen.

**Vor Schritt (2) müssen fünf Owner-Fragen beantwortet sein** (§ 14.6, Kurzform):
Ursache oder Nachbereinigung? Was passiert mit einem F-Raum, der nach dem Abzug
unter 1 m² fällt oder in Bruchstücke zerfällt? Darf „Flag ok" sinken, wenn dafür
die Überlappung verschwindet? Ist die Rangfolge **L > H > F** richtig? Soll
„Überlappende Räume / doppelt belegte m²" dauerhaft in `VERLAUF.md` und die
Prüfstrecke? **Ohne diese Antworten nicht anfangen** — Schritt (2) kann Räume
verschwinden lassen (1-m²-Kriterium `kaskade.py:114`) oder in
Zusammenhangskomponenten zerlegen.

**Offen an @EnisAMG:** drei Vokabular-Fragen in `docs/OFFENE_FRAGEN.md`
(`Schl.`, `Vorr.`/`Schrankr.`, `SR`/`Aufzug`); die Mollgasse-„Laubengang"-Frage
aus `47df2d9`; und das **weiterhin ausstehende Approval für `raum_modell`
1.4.0**, das mit PR #149 ohne sein Approval auf `main` gelandet ist.
**Offen an @mvpo3:** `raum_79` (LIFT) liegt zu 98 % in `raum_88` (STIEGENHAUS) —
Leuchten können rechnerisch in verschluckten LIFT/SCHACHT-Polygonen landen;
13 Räume liegen zu >90 % ihrer eigenen Fläche in einem anderen.

**Messskripte dieser Runde** (Session-Scratchpad
`C:/Users/selma/AppData/Local/Temp/claude/D--KI-Projekt/8fc32369-9bee-42cd-9e07-20d9eeb9eff5/scratchpad`,
alle nur lesend, wiederverwendbar): `_r65_umfeld.py`, `_r65_vokabular.py`,
`_r65_vf.py`, `_r65_tuer50.py`, `_r65_falschtreffer.py`, `_untyp_tabelle.py`,
`_p4_overlap.py`, `_p4_detail.py`, `_p4_herkunft.py`, `_p4_top3.py`,
`_p4_f_rate.py`.

---

## ═══ SELMAN: HIER WEITER (Stand 2026-09-10, Abschluss-Runde 2) ═══

**Branch:** `selman/extents-ausreisser`, **nicht gepusht, kein PR, kein Merge** —
der Owner gibt das GO separat. Commits dieser Runde: `c3cd3e7` · `47df2d9` +
Abschluss-Commit. **Kein Code in `src/` geändert, `hauptengine/contracts/**`
unberührt.**
**Suite: 1200 passed, 10 skipped, 2 deselected, 11 xfailed, 0 XPASS, 0 failed (19:08 min).**
**Prüfstrecke über alle fünf Pläne gelaufen, diesmal OHNE Parallellast**
(`scripts/plan_pruefen.py`, exit 0, Lauf `2026-09-10 13:35 · 47df2d9`).

**Leitregel unverändert:** *der Code erfindet keine Maße.* Fehlende Messung ist
`None` mit Quelle `UNBEKANNT` und einem Grund — nie ein Default, nie ein
Normwert, nie ein Mittelwert. Der AST-Riegel
`tests/contract/test_keine_erfundenen_masse.py` setzt das durch.

**Was diese Runde geklärt hat (Details: `docs/ENIS_UEBERGABE_0908.md` §§ 11 + 12):**
1. **Der Befund „3 echte Türen haben ihre Typisierung verloren" ist widerlegt.**
   Zwei tatsächlich gelaufene Provider-Parses derselben DXF (`0d7c5db` gegen
   HEAD, Worktree `D:/nbwt_vorher` steht noch) zeigen: die 3 war eine
   **Saldo-Zahl** (15 − 5 Fahnen − 7), keine Mengendifferenz. Lagebezogen:
   11 Ausgänge weg, 1 geblieben, 4 neu; davon 5 Beschriftungs-Fahnen und
   6 Kontaktzonen-Artefakte. **Keine echte Tür ist verloren gegangen.**
2. **Band `>= 9` in `test_soll_stair_exits` NICHT abgesenkt.** Der einzige
   gemessen gedeckte Ersatzwert wäre der Ist-Stand (5) selbst — verboten.
   Geändert wurde nur der `reason` (er behauptete die widerlegte Ursache) plus
   Docstring. Der fachliche Ersatz steht als eigener strict-xfail daneben:
   `test_soll_stair_exit_aus_echter_blocktuer`, Soll ≥ 1 `stair_exit` an einer
   echten `A-DOOR`/`A-GLAZ`-Blocktür, **Ist 0 von 5** — Zielwert aus `tuer_50`
   (334453/106403, `von_raum=stiegenhaus_1`), nicht aus dem Ist.
3. **Mollgasse-„Laubengänge" sind keine Laubengänge** — alle 12 `flaeche_fehlt`-
   Segmente liegen auf dem Außenanlagen-Layer `09-WEG_G00-LEG-M0` (Zaun,
   Mauersockel, Pflanztrog h=40 cm, Rigol, Gehsteig, Restmüll). Bewusste Grenze
   statt Pseudo-Fix, ausführlich in `docs/OFFENE_FRAGEN.md`: eine „nächste
   durchgehende Linie"-Regel griffe bei **107 von 107** korrekt gemessenen
   Segmenten auf das Achsraster `02-AXO` zu und ersetzte jede richtige Messung
   durch eine erfundene.

**Ist der Prüfstrecke (Lauf `2026-09-10 13:35 · 47df2d9`), Türen typisiert:**
Barawitzka_EG 55/106 · Mollgasse_EG 70/147 · Muthgasse_E2 206/291 ·
Rennweg_EG 24/41 · Rennweg_OG3 15/27 — **gegen `e9837b0` bewegt sich keine
einzige Kennzahl**, auf keinem Plan (erwartet, es wurde kein `src/`-Code
angefasst).

**Laufzeit endlich sauber gemessen (keine pytest-Suite parallel):**
Barawitzka 263,6 s · Mollgasse 288,2 s · **Muthgasse 1852,4 s** · Rennweg_EG
58,3 s · Rennweg_OG3 51,6 s. Muthgasse gegen den lastfreien Vorbefund 1838 s =
**+14,4 s / +0,8 %** — die 2116,4 s des Laufs `e9837b0` waren Lastkontext, keine
Verschlechterung.

**XFAIL-Bilanz: 11 strict-xfails, 0 XPASS.** Alle elf mit je einem Satz
Begründung in § 12.5. **In dieser Runde wurde kein xfail zu XPASS gedreht und
kein Zielband geändert.** Neu ist genau einer: `test_soll_stair_exit_aus_echter_blocktuer`
(zusätzlich sichtbar gemachter Befund, kein gefallenes Zielbild).

**DIE NÄCHSTEN DREI SACHEN IN MEINER LANE, alle belegt:**
1. **Manhattan-Dedupe `provider.py:148-157`** entkoppelt die `stair_exit`-Kennzahl
   von den Türen — zwei der untersuchten Türen fallen dort weg. Solange das so
   ist, misst `test_soll_stair_exits` nicht das, was sein Name behauptet.
2. **`tuer_typisierung.py:152-156` feuert auch bei `von_raum == nach_raum`.** Bei
   **4 der 5** widerlegten Fahnen war genau das der Fall (raum_88 → raum_88). Eine
   Tür von einem Raum in denselben Raum darf keine `stiegenhaustuer` sein.
3. **Die 9 STIEGENHAUS-Polygone auf Muthgasse sind höchstens 4 Kerne**
   (`stiegenhaus_1 ≡ _5`, `_2 ≡ _3 ≡ _4`, `_6`, `_7`, plus `_8` = 0,2 m² = 100 %
   `lift_5`). Vorher wie nachher gleich defekt.

**Was bewusst NICHT angefasst wurde:** `hauptengine/contracts/**` (Bump
`raum_modell` 1.4.0 wartet auf @EnisAMG-Approval — bis dahin eingefroren) ·
Enis' YAML + `test_quellenblock_e07_rl4.py:301` · `dxf_renderer.py` (@mvpo3) ·
`lux_nachweis_bericht.py:329/:333` (nur gemeldet) · Nennerfrage Muthgasse
`A-DETL` · die 12 Mollgasse-Segmente (Entscheidung dokumentiert, kein Code).

**Vorbestehend, nicht von mir:** `tests/raumerkennung/test_tueren.py::test_mollgasse_tueren`
**skippt** (DXF `Projekte/Mollgasse Notbeleuchtung/WHA_MOL_EG.dxf` fehlt im
Arbeitsbaum). `ruff check .`: 4 vorbestehende ISC004 in `scripts/plan_pruefen.py`.

**Weiter offen wie gehabt:** GESCHÄFTSLOKAL (blockiert, seit 2026-09-08) ·
Render-Speicher `_figur` 8×/Plan (Leonis) · Spikey-Polygone Mollgasse raum_41/55
(meine Lane) · Referenz-Frames UG/OG1 nicht verdrahtet · 4 Tür-Quoten-xfails ·
Baufeld E2 ohne Zielbild · `lichte_mm` ohne Erzeuger (darf nie aus `breite_mm`
abgeleitet werden).

---

## ═══ SELMAN: Stand 2026-09-10, Abschluss Schritte 1–6 ═══

**Branch:** `selman/extents-ausreisser`, **nicht gepusht, kein PR, kein Merge** —
der Owner gibt das GO separat. Commits dieser Runde: `8b35e53` · `58cd3a0` ·
`1ddb752` · `9141a3c` · `e9837b0` + Abschluss-Commit.
**Suite: 1199 passed, 10 skipped, 2 deselected, 10 xfailed, 0 XPASS, 0 failed (27:28 min).**
**Prüfstrecke über alle fünf Pläne gelaufen** (`scripts/plan_pruefen.py`, exit 0).

**Leitregel dieser Runde, die stehen bleiben muss:** *der Code erfindet keine
Maße.* Fehlende Messung ist `None` mit Quelle `UNBEKANNT` und einem Grund — nie
ein Default, nie ein Normwert, nie ein Mittelwert.

**Was umgesetzt ist (Details + alle Zahlen: `docs/ENIS_UEBERGABE_0908.md` § 10,
Tabelle § 7.2; Vorher-Stand unverändert in § 7.1):**
1. **Beschriftungsfahnen sind keine Türen** — `_DOOR_EXCLUDE` um `BESCHRIFT`,
   Muthgasse **308 → 291 Türen**, 83 Phantom-`TuerOeffnung`en weg, Zähler
   `_verworfene_bloecke` statt stiller Ausschluss. Andere vier Pläne: 0.
2. **Contract `raum_modell` 1.3.0 → 1.4.0** — `Tuer.breite_mm: float | None`
   (vorher `0.0`), `breite_quelle`, `breite_grund`, `lichte_mm` (**bleibt None**,
   kein Erzeuger). Alle neun Schreibpfade setzen die Quelle, alle Konsumenten
   None-fest, Schema regeneriert, Drift-Gate grün. **3-Owner-Approval offen.**
3. **Riegel gegen erfundene Maße** — `tests/contract/test_keine_erfundenen_masse.py`,
   AST über `src/**`, Messfeldliste aus den Contracts selbst. `dxf_renderer.py`
   `900.0` → `_ZEICHEN_ERSATZBREITE_MM` (gleicher Wert, gleiches Bild).
4. **Fluchtweg-Breitenmessung 209/307 (68,1 %) → 287/307 (93,5 %)** —
   `begrenzende_flaechen` + `SNAP_MM = 200` verschieben den **Messort**, nicht das
   Polygon; zweiter Deckel `ECKE_FENSTER_MM` gegen Eckfenster.
5. **Fenstererkennung nach Erscheinungsbild** — `raumerkennung/fenster_signatur.py`,
   24 Barawitzka-Öffnungen, **0 Falschtreffer** auf den vier Vergleichsplänen.
   `belichtung_vollstaendigkeit` Barawitzka UNGEPRUEFT → TEILWEISE.

**Ist der Prüfstrecke (Lauf 2026-09-10 04:48 · `e9837b0`), Türen typisiert:**
Barawitzka_EG 55/106 · Mollgasse_EG 70/147 · **Muthgasse_E2 206/291** ·
Rennweg_EG 24/41 · Rennweg_OG3 15/27. Gegen `ab0ad51` bewegt sich **nur
Muthgasse** (vorher 219/308).

**DIE NÄCHSTEN DREI SACHEN IN MEINER LANE, alle belegt:**
1. **`stair_exit` Muthgasse 12 → 5 — 3 echte Türen haben ihre Typisierung
   verloren.** 5 der 7 Verschwundenen waren Fahnen (erfundene Ausgänge, richtig
   so), die restlichen 3 nicht. Ursache liegt in der **Tür-Typisierung**, nicht im
   Fahnen-Ausschluss, und ist **nicht aufgeklärt**. Band bewusst **nicht**
   abgesenkt, sondern als strict-xfail `test_soll_stair_exits` sichtbar.
2. **12 Mollgasse-Segmente `flaeche_fehlt`** (`seg_4/7/8/9/10/27/34/41/92/93/94/95`) —
   dort existiert **kein lichtes Raumpolygon** (Laubengang/Hofwege, Kaskade `R:0`,
   Ursache `aussenkontur` in `rest_komponenten.py`). `SNAP_MM` NICHT auf 300 heben:
   `seg_92-95` laufen 6 m **an** einem KINDERWAGENRAUM entlang, nicht durch ihn —
   das würde die Zahl heben und die Messung kaputtmachen.
3. **`lichte_mm` hat keinen Erzeuger.** Das Feld steht im Contract und bleibt
   `None`. Der Slice dazu ist offen — und er darf die Lichte **nie** aus
   `breite_mm` ableiten.

**Was bewusst NICHT angefasst wurde:** Enis' YAML + `test_quellenblock_e07_rl4.py:301`
(Vorschlag `== 3` → `== 4` steht in § 6.4) · `dxf_renderer.py` über die Konstante
hinaus · `lux_nachweis_bericht.py:329/:333` (nur gemeldet) · die Nennerfrage
Muthgasse `A-DETL` · Raumzuordnung der 24 Fensteröffnungen.

**Vorbestehend, nicht von mir:** `tests/raumerkennung/test_tueren.py::test_mollgasse_tueren`
**skippt**, weil `Projekte/Mollgasse Notbeleuchtung/WHA_MOL_EG.dxf` im Arbeitsbaum
fehlt (Prüfstrecken-DXF liegt unter `Projekte/_eingang/Mollgasse_EG.dxf`).
`ruff check .`: 4 Fehler, die vorbestehenden ISC004 in `scripts/plan_pruefen.py`.

**Weiter offen wie gehabt:** GESCHÄFTSLOKAL (blockiert, seit 2026-09-08) ·
Render-Speicher `_figur` 8×/Plan (Leonis) · Spikey-Polygone Mollgasse raum_41/55
(meine Lane) · Referenz-Frames UG/OG1 nicht verdrahtet · 4 Tür-Quoten-xfails ·
Baufeld E2 ohne Zielbild.

---
## ═══ SELMAN: HIER WEITER (Stand 2026-09-10) ═══

**Branch:** `selman/extents-ausreisser`, **nicht gepusht**. Contracts unberührt.
**Suite: 1177 passed, 10 skipped, 9 xfailed, 0 failed (19:31 min).**

**Enis' Normwissen-Übergabe 0908-v2 verarbeitet** — Bericht
`docs/ENIS_UEBERGABE_0908.md` (655 Z.), Board-Antwort an @EnisAMG/@mvpo3 vom
2026-09-10 in `docs/COORDINATION.md`. Commits `a9ab1b6` (WIP-Sicherung) →
`1a78966` (Bericht + Breitenprofil) → `3d3215d` (Wächter-Fix) → `288efc8` /
`38a4387` (Bericht nachgezogen). Archiv-SHA nicht prüfbar (Paket lag entpackt),
`SHA256SUMS.txt` alle 12 OK.

**Umgesetzt (Punkt 2 von dreien):** `raumerkennung/breitenprofil.py` misst den
tatsächlichen Breitenverlauf — Mittelachse, 100-mm-Abtastung, Abschnitte
konstanter Breite (Tol. 100 mm, min. 500 mm), Engstellen getrennt, Türpunkte
eigen, fehlende Messung `None` **mit Grund**, **nie ein Normwert als Fallback**.
Drei Messfehler behoben (u. a. schiefe Normale: 1200 mm wurden als 1223,8 mm
gemessen, jetzt 1200,8 mm). Ist: **209 von 307 Segmenten messbar (68,1 %)**.

**Punkt 1 (natürliche Belichtung) und Punkt 3 (`Tuer.breite_mm`): nur Vorschlag,
kein Code** — beide brauchen Contract-Felder (1.3.0 → 1.4.0, additiv, Default
`None`) und damit die 3-Owner-Runde.

**Die drei nächsten Sachen in meiner Lane, alle belegt:**
1. **61 Fluchtwegsegmente ohne schneidendes Raumpolygon** (`flaeche_fehlt`) —
   Erkennungslücke, größter Einzelposten der 98 nicht messbaren Segmente.
2. **83 Muthgasse-Beschriftungsfahnen zählen als Türen** → `RaumModell.tueren`
   308 statt ~225 (+27 %). Eigenständiger Erkennungs-Bug.
3. **`dxf_renderer.py:524` erfindet still 900 mm Türbreite** (`breite_mm or 900.0`).

**Fensterlage vorab gemessen** (für Punkt 1, falls er GO bekommt): Muthgasse
Layer `A-GLAZ*` 579 Punkte (`A-GLAZ-IDEN` = Beschriftung, ausschließen) · Mollgasse
nur Blockname, 17 INSERTs · Rennweg EG/OG3 in den `Wall_*`-Blöcken, **Einfügepunkt
ist ein Dummy**, echte Lage nur über Blockgeometrie · **Barawitzka: null
Fensterobjekte**. Oberlichter: 0 im ganzen Repo.

**Weiter offen wie gehabt:** GESCHÄFTSLOKAL (blockiert, seit 2026-09-08) ·
Render-Speicher `_figur` 8×/Plan (Leonis) · Spikey-Polygone Mollgasse raum_41/55
(meine Lane) · Referenz-Frames UG/OG1 nicht verdrahtet · 4 Tür-Quoten-xfails ·
Baufeld E2 ohne Zielbild · `Projekte/BVH Fischamenderstrasse/fertige
Elektromontagepläne/` unausgewertet.

---
## ═══ SELMAN: Stand 2026-09-09 ═══

**Branch:** `selman/extents-ausreisser`, **gepusht**, PR offen. `origin/main` gemergt
(Leonis: 1:50-Vektor-PDF auf ISO-A-Blatt, DIN-Farbtrennung, Richtungspfeile,
Sichtlinien-Garantie, `mittellinie._raster`-Kappung). Contracts unverändert.
**Suite nach dem Merge: 1096 passed, 10 skipped, 9 xfailed, 0 failed (19:55 min).**

**Prüfstreckenlauf über alle fünf Pläne abgeschlossen** (Commit `cef2210`), gemessen:
Barawitzka 38 Stempel/47 Räume, Türen 55/106, **Referenzvergleich 18 %** (2 Treffer /
9 fehlend / 5 überzählig), 263 s · Mollgasse 83/62, Türen 70/147, RZ 30 SL 35, 292 s ·
Muthgasse E2 99/102, **Türen 219/308**, RZ 64 SL 28, 1838 s · Rennweg EG 19/21,
Türen 24/41, 56 s · Rennweg OG3 10/14, Türen 15/27, 52 s.

**Bestandsaufnahme (10 Themen, belegt) — die zwei echten Baustellen:**
1. **`RaumModell.anker` hat NULL Konsumenten** in `platzierung/` und `hauptengine/`
   (`grep '\.anker'` dort leer). Stiegenhaus-/Ganganker inkl. `winkel_grad` und
   `fluchtrichtung_grad` werden erzeugt, geprüft — und nie gelesen. Das ist die
   plausibelste Einzelursache für die 18 % Referenz-Trefferquote.
2. **WOHNUNG_PRIVAT-Filter greift nur in `flaechen_strategy.py:155-167`** — sechs
   weitere Platzierungspfade laufen ungefiltert. Realbefund: Mollgasse 11,
   Muthgasse 29 Leuchten in Wohnungen. Leonis' Lane, im Board gemeldet.

**Weiter offen:** GESCHÄFTSLOKAL (3-Owner-Frage, blockiert) · Render-Speicher
`_figur` 8×/Plan (Leonis) · Spikey-Polygone Mollgasse raum_41/55 (**meine Lane**,
von Leonis übergeben) · Referenz-Frames UG/OG1 nicht verdrahtet (`_REFERENZ_FRAME`
kennt nur Barawitzka_EG → 35 der 46 Referenzleuchten ungenutzt) · 4 Tür-Quoten-xfails
(Ist 48–71 %, Ziel 90 %) · Baufeld E2 ohne Zielbild (nur ZIP) · unausgewertetes
Referenzmaterial, größter Posten: `Projekte/BVH Fischamenderstrasse/fertige
Elektromontagepläne/` (10+ fertige Elektropläne, in keiner Datei je erwähnt).

---
## ═══ SELMAN: HIER WEITER (Stand 2026-09-08 abends) ═══

**Branch:** `selman/extents-ausreisser` — **35 Commits vor `origin/main`, 0 dahinter**
(Merge `956e827` gemacht). Suite nach dem Merge **1089 passed, 0 failed**.
**NICHT gepusht** — Push/PR braucht Owner-GO.

**Was diese Session gemacht hat (alles gemessen, nicht geschätzt):**
1. `stempel_flutung._fuelle` auf Pillow-Scanline — `skimage.draw.polygon` kostete
   O(BBox-Pixel × Stützpunkte), ein Ring der Baufeld-Wand-Union 166 s. **Baufeld E2
   entsperrt: Kaskade 41 s statt >13 min, 0,47 GB, 237 Räume.**
2. `kaskade`: Stempel-Typ auf L-/H-Räume zurückschreiben, **nach** der Flutung
   (davor bleibt der Typ an verworfenen Polygonen hängen). Muthgasse Türen
   27/311 → 219/307; xfail-Zielbild erreicht.
3. `tuer_typisierung`: Türtext-Fallback darf `ist_notausgang=False` von
   Balkontür/Garagentor nicht zurückdrehen (Geschosskürzel „E2" matchte das
   Notausgang-Muster).
4. `plan_pruefen._material_report` folgt dem Ausgabeziel — der Sammellauf hatte
   `docs/MATERIAL_REPORT.md` überschrieben (zurückgeholt aus 45d60c7).
5. **KINDERWAGENRAUM** als eigener Kanon-Typ + Token `kiwa` in `_EXTRA_OVERRIDE`
   (reale Stempel schreiben „KIWA", nie „Kinderwagen"; als OVERRIDE, weil sonst
   das generische `fahrrad`-Token den Mischraum „FAHRRADRAUM / KIWA" gewinnt).
   Wirkung: Mollgasse RZ 26 → 28, Barawitzka RZ 2 → 3.

**Offen / als Nächstes:**
- **Push + PR** (Owner-GO nötig). Danach Board-Antworten abwarten.
- **`GESCHÄFTSLOKAL`** — echte Kanon-Lücke, 3-Owner-Frage steht im Board.
- **Render-Speicherfresser** `plan_pruefen._figur` (8× `draw_layout` je Plan,
  ~13 GB) — Leonis' Lane, im Board gemeldet.
- **Sammellauf wiederholen**, sobald der Render entlastet ist: der letzte lief nur
  über 62 der 72 Ordner, und die Zwillinge (Barawitzka_EG/415_1_3,
  Muthgasse_E2/M109B E2, Rennweg_EG/OG3) müssen vor jeder Statistik dedupliziert
  werden.
- **Vokabular:** Trefferquote 87 %; sechs Alias-Kandidaten sind mit Beleg
  VERWORFEN (`docs/OFFENE_FRAGEN.md`) — nicht erneut vorschlagen ohne neuen Beleg.

---
## ═══ SELMAN: HIER MORGEN WEITER (Zusammenfassung 2026-08-29) ═══

**Branch:** `selman/raumerkennung-dxf` (gepusht). Setup: siehe oben §0. Test: `pytest -q`
→ **95 passed**. Ruff sauber. Plan-Datei: `.claude/plans/du-bist-fenster-delightful-wozniak.md`.

**Was steht — `ArchitekturRaumProvider.parse(dxf, floor) -> RaumModell`** liest 5 CAD-
Familien (Mollgasse / Fischamender / Barawitzka / Herrenholz / Baufeld). Module in
`src/notbeleuchtung/raumerkennung/`:
- `dxf_load.py` — öffnen, **Wand-Layer per Muster** (`WALL_PATTERN`), **Skala aus Geometrie**
  (Span-Gate 15–500 m + Tür-ARC-Radius; `$INSUNITS` ignoriert — lügt).
- `waende.py` — Wand-Segmente → `extract_room_faces` (Port). Fallback-Raumquelle.
- `raumlayer.py` — **echte Raum-Polygone aus Raum-Layern** (`81\d Raum`/`Raumbegrenzung`/
  `A_Raeume`) + Name (`ROOM_NAME`-ATTRIB / MTEXT) → `classify_room`. Provider bevorzugt das.
- `raumtyp.py` — Stempel→`raum_typ`+Flags (`raumtyp_flags` Helper).
- `tueren.py` — Türen: benannte Blöcke `TÜR…`/`ÖFFNUNG…` + **ARC-Schwenkbogen-Fallback**
  (ArchiCAD). Alle Familien liefern Türen (F1-Naht).
- `zirkulation.py` — 09-WEG → Segmente + networkx-Graph.
- `footprint.py` — **Raster-Flood-Fill Gebäude-Umriss**; Hauptausgang = Doppeltür (2 ARCs)
  am Rand.
- `provider.py` — verdrahtet alles.

**Zahlen heute (EG je Projekt):** Räume — Fischamender 68 · Herrenholz 473 · Baufeld 220 ·
Mollgasse 184 (Fallback, kein Raum-Layer) · Barawitzka 2 (schwach). Türen — Mollgasse 44 ·
Fischamender 120 · Barawitzka 116 · Herrenholz 140 · Baufeld 191. Hauptausgänge — Mollgasse 4.

**OFFENE PUNKTE (Priorität) — inkl. F1-Bugmeldungen (Board `docs/COORDINATION.md` §Bugs):**
1. **B2 (F1, wichtig): `zirkulation` + Ausgänge nur Mollgasse-Layer.** `zirkulation_aus_dxf`
   sucht `09-WEG`; Fischamender-Fluchtweg liegt auf **`A_Fluchtweg`** → 0 Segmente/0 Ausgänge,
   F1-RZ-Routing unmöglich. FIX: **Fluchtweg-Layer per Muster** (wie `WALL_PATTERN`) +
   Ausgang-Erkennung pro Familie. F1-Hinweis: Stiegenhaus BT1 aus `S-STRS`-Layer, Cluster
   bei mm (20928, 85023).
2. **B1 (F1): Tür-Doppelzählung.** Fischamender: jede Tür als 2 ARC-Schwenkbögen → ~42
   Quasi-Duplikate <20 cm (102 statt ~60). FIX: Dedup-Cluster <300 mm je Tür-Position
   (betrifft `_arc_tueren` UND ggf. Doppeltür-Paare in `footprint`).
3. **Hauptausgang generalisieren** — Doppeltür-2-ARC nur Mollgasse (4). Fischamender/Baufeld 0.
   Ggf. F1-seitig via `richtung_durch_tuer` an echten `tueren` — mit F1 abklären.
4. **Baufeld Wände sind INSERT-Blöcke** (`Wand_*`) → Footprint sieht nur 126 Linien (99%
   außen, kaputt). **Wand-Block-Descent** (INSERT-Transform) — hilft Footprint/Hauptausgang.
5. **Barawitzka Räume (nur 2)** — Polygone auf `Icon`-Layern/LINE-Loops, nicht geschl. LWPOLY.
6. **Mollgasse-Räume** (kein Raum-Layer) → Face-Clustering (Union-Find, NICHT DBSCAN —
   auditierbarer, keine neue Dep). Nebenbefund F1: 20/59 Räume Fragmente (Gap-Healing-Grenze).
7. **Fake-Swap E2E** offen (4OG-Golden ≠ echter DXF; mit F1 neue Golden abstimmen).

**⚠️ GIT-TANGLE (Board-Log):** F1-Platzier-Commit `e87a745` liegt versehentlich auf diesem
Branch `selman/raumerkennung-dxf`. Vor PR entwirren (F2-Raumerkennung von F1-Platzierung
trennen) — mit F1 abstimmen.

**Naht-Regeln:** nur `raumerkennung/` + `hauptengine.contracts`. Contract NICHT ändern.
Renders (Beleg) via scratchpad-Skripte; Beispiel-Outputs lagen in `output/` (untracked).

---

### 2026-08-29 — Türen über ALLE Familien (F1-Naht: `richtung_durch_tuer`)
F1-Hinweis: `richtung_durch_tuer` greift automatisch, sobald echte `RaumModell.tueren`
an den realen Öffnungen stehen. → F2-Job: `tueren` pro Familie vollständig.
Vorher nur Mollgasse(44)+Fischamender(114); Barawitzka/Herrenholz/Baufeld = **0**.

`tueren.py` erweitert (3 Darstellungen):
1. Benannte Blöcke: `TÜR…` + jetzt auch `ÖFFNUNG` (Baufeld-Marker) + Außentür-Namen.
2. **ARC-Fallback** (ArchiCAD ohne Türblöcke): je Schwenkbogen (r 600–1300mm) eine Tür
   am Drehpunkt, Breite = Radius. Greift nur, wenn (1) leer.
3. Breite: cm-Konvention (`TÜR-80`→800) ODER mm direkt (`_0800x2000`→800).

**Ergebnis:** Mollgasse 44 · Fischamender 120 · Barawitzka **116** · Herrenholz **140** ·
Baufeld **191** — alle Familien liefern echte Tür-Positionen → F1 entblockt. Suite 95.
Caveat: ARC-Türen evtl. Doppelzählung (Doppeltür=2 ARCs); Baufeld-Öffnungen ggf. inkl.
Fenster; Positionen aber real.

### 2026-08-29 — Raum-Layer-Reader: echte Raum-Polygone (löst Schlitz-Problem)
Auf Basis des „Schritt-6"-Vorschlags (Face-Clustering), aber die auditierbarere/
billigere Variante: **3 von 4 Input-Familien haben fertige Raum-Polygone auf eigenen
Layern** → direkt lesen statt clustern. `raumlayer.py::raeume_aus_layer(plan)`:
- Raum-Poly-Layer per Muster (`81\d Raum` · `Raumbegrenzung` · `A_Raeume`, ohne Icon),
  geschlossene LWPOLYLINE → Polygon + Fläche.
- Name aus `ROOM_NAME`-ATTRIB (Herrenholz/Baufeld) ODER MTEXT im Polygon
  (Barawitzka/Fischamender) → `raumtyp_flags` (neuer Public-Helper in `raumtyp.py`).
- Provider: `raeume_aus_layer` bevorzugt, sonst Wand-Polygonize-Fallback (Mollgasse).

**Output-Wandel (echte Räume + Typen statt Schlitze):**
Fischamender **68** (45 typisiert: ZIMMER/GANG/BAD/WC/KÜCHE) · Herrenholz **473** ·
Baufeld **220** · Mollgasse Fallback 184 (kein Raum-Layer) · Barawitzka nur **2**
(Polygone liegen wohl auf Icon/LINE — Nacharbeit). Viz:
`output/RaumModell_Fischamender_EG_HQ.png` (Gänge sauber als Erschließung erkannt).
Suite **93**, ruff sauber.

Offen: Barawitzka-Raum-Polygone (Icon-Layer/LINE-Loops); Mollgasse-Räume brauchen
weiterhin Face-Clustering (Union-Find, nicht DBSCAN) da kein Raum-Layer.

### 2026-08-29 — Cross-Projekt-Fundament: Wand-Layer + Skala über alle 5 Familien
Ziel (Owner): Muster über alle Projekte, Haupteingänge in JEDEM Projekt erkennen.

**Generalisiert (getestet, Suite 91):**
- **Wand-Layer per Muster** statt fixem Prefix (`dxf_load.WALL_PATTERN`):
  `02-TWA/ZWA/WDA` (Mollgasse) · `A_Waende` (Fischamender) · `1[123]0 Wand` (ArchiCAD:
  Barawitzka/Herrenholz/Baufeld, auch mit `_Stift_Nr__N`). `DxfPlan.wall_entities()`.
- **Skala robust** (`_calibrate_factor`): Span-Gate 15–500 m (killt falsche Klein-Dekade),
  Tür-Schwenkbogen-Radius (~0.9 m) als Tiebreak. Ergebnis korrekt für ALLE:
  Mollgasse leer 54.6×48.4m (×1000) · fertig (×1) · Fischamender 53×95m · Barawitzka
  80×36m (vorher fälschlich 8m!) · Herrenholz 215×64m.
- Synth auf 20×12 m vergrößert (Span-Gate braucht ≥15 m); Tests angepasst.

**Hauptausgang-Status je Familie:**
- Mollgasse: **4** (Doppeltür am Rand) ✓.
- Barawitzka: 116 Tür-ARCs (800/900/1000mm ✓), 59 Doppeltür-Paare erkannt, aber alle
  INNEN → 0 am Rand. Braucht eigene Kalibrierung (Paar-Kriterium enger; andere
  Eingangs-Darstellung). Umriss OK (37% außen).
- Fischamender: nur 7 Tür-ARCs top-level — Rest **nested in `A_Tueren`-Blöcken** →
  `_schwenkboegen` muss in Tür-Blöcke absteigen (INSERT-Transform anwenden).
- Herrenholz/Baufeld: analog ArchiCAD, noch offen.

**Nächster Schritt:** (a) `_schwenkboegen` in Blöcke absteigen (Fischamender);
(b) Doppeltür-Paar-Kriterium schärfen (gleiche Wand, gegenläufige Flügel) gegen die 59
Barawitzka-Falschpaare; (c) je Familie an einem Geschoss validieren. Raum-Polygone aus
Raum-Layern (`_815`/`810`/`A_Raeume`) bleibt ebenfalls offen.

### 2026-08-29 — FIX-3 Hauptausgang = DOPPELTÜR am Rand (Fachmuster vom Owner)
Owner-Regel: **Gebäude-Haupteingang wird als Doppeltür gezeichnet** (2 Flügel), 1–2 je
Gebäude/Stiegenhaus; Muster über alle Projekte lernen. Perimeter-Tür allein war zu grob
(18 inkl. Fassaden-Wohnungstüren).

**Signatur Doppeltür (Mollgasse):** zwei Schwenkbögen (ARC, r≈600–1300mm = Tür-Blattbreite)
gleicher Größe, Drehpunkte 1.4–2.6m auseinander (= Öffnungsbreite). ARC-Paar **an der
Gebäude-Außenkante** (Raster-Umriss-Rand) = Hauptausgang. `türachse&qualität` (33×) =
vollständige Tür-Positionsquelle (nicht Noise!) — für spätere Verfeinerung.

`footprint.py::hauptausgaenge(plan, bounds)`: Raster-Umriss (mit Padding > Schließ-
Dilatation!) → Rand-Band → Doppeltür-ARC-Paare am Rand. Mollgasse EG (leer + fertig):
**4 Hauptausgänge** (1 links Hof + 3 rechts), deckt beide Stiegenhäuser/Blöcke. Provider:
`ausgaenge = hauptausgaenge(plan, bounds)`. Alte Perimeter-/Namensheuristik entfernt.
Suite **87**, ruff sauber. Viz: `output/hauptausgaenge_final_EG.png`.

Offen: Rechter Block 3 (evtl. 1 Loggia-Doppeltür zu viel) — Rim-Toleranz feinjustieren.
**Cross-Projekt:** Doppeltür-als-2-ARCs ist Mollgasse-Muster; Fischamender (`A_Tueren`
benannte Blöcke `…Wohnungstür…`) + ArchiCAD (keine Türblöcke, nur ARC-Schwenk) brauchen
je eigenes Doppeltür-Erkennungs-Profil. Muster-Lernen über Profile = nächster Schritt.

### 2026-08-29 — FIX-2 Hauptausgänge via Raster-Umriss (`footprint.py`)
User: „du erkennst die Hauptausgänge nicht" + 4 Beispielbilder (Mollgasse EG).
Definition bestätigt: **Hauptausgang = Tür in der Außenwand, die nach außen führt**
(Vorplatz/Hof), im fertigen Plan mit grünem RZ + Richtungspfeil.

Erprobt + verworfen (alle scheitern am lückigen, nicht-konvexen Wandwerk):
Wand-Polygonize→Schlitze · Wand-Buffer-Union→239m²-Fragment · konvexe Hülle→Türen
1.8–14m daneben · WET_AUSSEN-Namensheuristik→geraten · Fluchtrichtungspfeil-Block→im
Plan 0 (Pfeil steckt im RZ). RZ sitzen an `türachse&qualität`-Markern (jede Tür), nicht
nur an Hauptausgängen.

**Lösung `footprint.py` (nur scikit-image):** Wände rastern (200mm) → `disk(5)` dilatieren
(Türlücken schließen) → `label(~closed)`, Ecke=außen fluten → Gebäude-Innen/Außen.
**Hauptausgang = Perimeter-Tür** (Türzelle ∈ dilatierter Außen-Maske). Mollgasse EG:
**6 Perimeter-Türen, alle am Vorplatz/Hof — Owner bestätigt „im Wesentlichen richtig".**
Provider: `ausgaenge = ausgaenge_aus_umriss(plan, tueren, bounds)`. Suite **88**, ruff sauber.
Viz: `output/hauptausgaenge_perimeter_EG.png`.

Offen: rechter Gebäudeblock hat 0 Kandidaten (eigener Eingang? prüfen); ggf. 6→4
verschärfen (Türbreite). `footprint`-Umriss ist auch Basis für Raum-Extraktion (Innen-Blob).

### 2026-08-29 — FIX-1 Ausgänge + Skala (nach Analyse ALLER 6 Projekte)
User-Feedback: „Ausgänge falsch". Ursache: Heuristik „09-WEG-Endknoten nahe Bounding-Box"
→ 88 fragmentierte 2-Punkt-Segmente, deren Enden am **Planrahmen** liegen (die 09-WEG-
Annotation ist kein begehbarer Weg). Ergab 11 Müll-Ausgänge.

**Projekt-Analyse (4 Agenten, alle Ordner):**
- 3 Layer-Konventionen: Mollgasse (`02-TWA/09-WEG/TÜR-80`), Fischamender (`A_Waende/
  A_Tueren/A_Raeume/A_Fluchtweg`), ArchiCAD-numerisch (`110/120/130 Wand`, `810/815 Raum`
  + `ROOM_NAME`-ATTRIB) für Barawitzka/Herrenholz/Baufeld.
- **`$INSUNITS` lügt überall**: leere Pläne in METERN, fertige in mm, beide oft Code 4/6.
- **Kein Plan hat ein explizites Ausgang-Symbol.** Fertige Pläne: RZ/Sicherheitsleuchten
  auf `E_Sicherheitsbeleuchtung` (ATTRIB `ANLAGE='Eak'`) bzw. `dp_GE_SIBEL` = OUTPUT.
- **3 leere Inputs haben fertige Raum-Polygone** auf `_815`/`810 Raum`/`A_Raeume` → der
  Schlitz-Problem-Killer (nächster Slice: Raum aus Layer statt Wand-Polygonisierung).
- Ich hatte gegen die FALSCHE Datei getestet: `WHA_MOL_EG.dxf` = fertig (Output). Echter
  Input = `Projekte/Mollgasse/Erdgeschoß.dxf` (Meter).

**Gefixt (Owner-Wahl: Außentüren + Skala-Fix):**
- `dxf_load._calibrate_factor`: mm-Faktor per Dekaden-Snap aus Wand-Ausdehnung (Input
  Meter→×1000). `$INSUNITS` nur noch Fallback.
- `tueren.ausgaenge_aus_dxf`: Ausgang = Außen-/Eingangstür (`WET_AUSSEN`/`WET`/`SCHIEBETÜR`/
  `Fenstertür`), `typ=final_exit`; Außentüren tragen `ist_notausgang=True`.
- `zirkulation`: Ausgang-Erzeugung entfernt (nur noch Segmente+Graph), `reason` ohne Rand.
- Provider zieht Ausgänge aus Türen. Mollgasse: 11 Müll → **6 echte Außentüren**. Suite **86**.

**Nächster Schritt (empfohlen):** Raum-Polygone aus den Raum-Layern (`_815`/`810`/
`A_Raeume`) statt Wand-Polygonisierung — löst die 184-Schlitze für 3 Projekte. Danach
Parser-Profile (Mollgasse / A_* / ArchiCAD-numerisch) trennen.

### 2026-08-29 — S3–S6 fertig: parse() steht, Teil-READY (Owner-Weg B)
Owner-Entscheidung: **B** — erst die Teile bauen, die auf echten Plänen JETZT gehen.

**Fertig & echt grün auf Mollgasse-EG** (`ArchitekturRaumProvider.parse`):
- `tueren.py` (S4): 40 Türen, Nennbreite aus Blockname (cm→mm, erste Zahl 60–130),
  Achsmarker/Türöffner ausgeschlossen.
- `zirkulation.py` (S5): 09-WEG LINE/LWPOLYLINE → 103 `FluchtwegSegment` + networkx-Graph
  (gesnappte Knoten) + 11 `Ausgang` (grad-1 an Außenkante).
- `raumtyp.py` (S3): MTEXT-Stempel → `classify_room` → `raum_typ`+Flags per Point-in-Polygon
  (synth deterministisch; auf echt limitiert durch fehlende Raum-Polygone).
- `provider.py` (S6): verdrahtet alles, `RaumModell.model_validate`-Roundtrip grün.
  Volle Suite **80 passed**, ruff sauber.

**Weiter offen — das harte Teil:** echte **Raum-Polygone** (184 Wand-Schlitze statt
Räumen). Nächster Slice-Kandidat: Tür-Öffnungs-Virtualwände + Fragment-Bridge aus
`_port/parsers/architecture_dxf.py` (`_build_virtual_walls_from_doors`,
`_build_fragment_bridges`) selektiv portieren, ODER room-partition via Anker/`assign_room`.
Erst DANN E2E-Fake-Swap (mit kuratierter neuer 4OG-Golden + F1-Konsens).

Branch `selman/raumerkennung-dxf` — bereit für PR (User-GO nötig, nicht gepusht).

### 2026-08-29 — S1+S2 fertig, HARTES PROBLEM gefunden (Raum-Polygone)
**S1** `dxf_load.py`: ezdxf öffnen, `$INSUNITS`→mm (Mollgasse=mm, factor 1.0),
Direct-Mode (797 Wand-Ents direkt im msp; Wrapper-Fallback vorhanden), `bounds_mm`.
Tests grün gegen echte Mollgasse-EG.

**S2** `waende.py`: Wand-Segmente (LINE + LWPOLYLINE explodiert) → Port-Helfer
`extract_room_faces`. **Synth (Einzellinien-Wände) = exakt 2 Räume, 25+15 m² ✓.**
ABER echte Mollgasse: 1005 Segmente → 184 „Räume" mit median 0.2 m² = **Wand-Schlitze**
zwischen den Doppellinien (10er/20er-Wand), NICHT echte Räume. Zweiter Versuch
shapely-Buffer-Difference (Wände puffern → aus Grundfläche subtrahieren): 1 Riesen-Blob
2400 m² weil Türlücken alles verbunden lassen. → **Naive Geometrie reicht für echte
Pläne NICHT.** Das ist genau das Problem, für das die `_port`-Maschinerie (virtuelle
Wände an Tür-/Fensteröffnungen `_build_virtual_walls_from_doors`, `_build_fragment_bridges`,
room-partition via `assign_room`, room-hatch-ranking) existiert. FIL-Hatches (LILA/ORANGE)
sind Belag-Muster, KEINE Raum-Polygone.

**ENTSCHEIDUNG offen (User gefragt):** (A) Port-Maschinerie reanimieren, (B) erst
Türen/Fluchtweg/Bounds liefern (funktionieren auf echt) + Raum-Polygone nur clean-DXF,
(C) mittlere Heuristik. `waende.raeume_aus_waenden` bleibt als clean-DXF-Pfad + Fallback.


### 2026-08-29 — S0 fertig (Branch `selman/raumerkennung-dxf`)
**Ansatz (entschieden):** NICHT die 14.4k-LOC `_port/` reanimieren, sondern schlanker
Neubau in `raumerkennung/`, der die *sauberen* Port-Helfer wiederverwendet:
- `._port.parsers.room_faces.extract_room_faces` — Wand-Segmente → Raum-Polygone (pure).
- `._port.models.room.classify_room` + `GERMAN_ROOM_TYPE_MAP` — Stempel→RoomType (pure).
Plan-Datei: `.claude/plans/du-bist-fenster-delightful-wozniak.md`.

**Gebaut:** `provider.py` (`ArchitekturRaumProvider.parse` Stub, erfüllt Protocol),
`__init__.py` export, `tests/raumerkennung/{conftest,test_scaffold}.py`. Suite grün
(69 passed). Baseline-Info: volle Suite ist heute **69** (nicht mehr 13/1 aus Handoff).

**Datenlage (DXF-Inspektion):** Mollgasse `Projekte/Mollgasse Notbeleuchtung/WHA_MOL_*.dxf`
= mm ($INSUNITS=4, Koords ~65k). Layer: Wände `02-TWA*/02-ZWA*/02-WDA*`, Text
`01-/03-/05-TXT*` (MTEXT), Türen `TÜR-80_*` (INSERT auf `05-SYM*`), Fluchtweg `09-WEG*`.
Baufeld E2 = Meter + andere Taxonomie (110/120/130-Blöcke) → deferred.

**Nächster Schritt:** S1 `dxf_load.py` — ezdxf öffnen, Modelspace/Wrapper-INSERT,
$INSUNITS→mm-Faktor, Layer-Prefix-Filter, `bounds_mm`. Test gegen `WHA_MOL_EG.dxf` (skipif).

**Naht-Warnung:** E2E NICHT auf echten Provider umstellen — 4OG-Golden (neg. Koords,
7 Symbole) matcht keinen echten DXF. Fake-Swap erst mit kuratierter neuer Golden + F1.
