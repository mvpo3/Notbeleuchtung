# Kopplung neueste Raumerkennung (PR #161, `c3b8186`) × Platzierung — Bericht

**Branch:** `leonis/kopplung-raumerkennung-c3b8186` (von `c3b8186` = PR #161/#160, Merge
origin/main `91c5b72` in `luecken-2026-09-30`) + Merge meiner Platzierungsarbeit
(`codex/Notbeleuchtungs_Platzierungslogik`, 43 Commits vor main).
**Datum:** 2026-10-01 · **Owner-Auftrag.** Nicht nach main, nicht auf Selmans Branch.

## 1. Kopplung
- `raumerkennung/**` nach dem Merge **byte-identisch zu `c3b8186`** (Konflikte zugunsten c3b8186;
  es gab 0 Konflikte in `src/`, nur in `Projekte/_ergebnis/` Output-Artefakte → meine Seite).
- Nur meine Pakete eingebracht: `platzierung/` (13 Dateien), `symbols/` (5, shared Render),
  `hauptengine/render/dxf_renderer.py`. **`contracts/` und `normwissen/` unangetastet.**
- Deps neu installiert (`pip install -e ".[dev,api]"`).

## 2. Prüfung
- **Volle Suite:** `5 failed, 2333 passed, 2 skipped, 6 deselected, 15 xfailed` (24:48).
  Alle 5 roten in der erwarteten Menge (LUECKEN §6.1/§21.1): 2× S4c-Pins (`test_bara_raum_19/30`),
  2× `test_keine_leuchten_in_wohnung_privat[OG2/DG1]` (Board 1, meine Lane), 1×
  `test_soll_muthgasse::test_soll_plan_tuerbloecke_im_modell`.
  **Die 6. erwartete rote (`wohnung_privat[pfad0-OG1]`) ist bei mir GRÜN** — meine Platzierung
  setzt dort keine WOHNUNG_PRIVAT-Leuchte mehr (Verbesserung, kein Regress).
  **Null rot in `raumerkennung/`, null neue/unerwartete rote.**
- **Schema:** `gen_schema.py --check` → „schema in sync" (kein Contract-Touch).
- **Gate:** `pytest -m gate tests/gate` → 4 skipped, Grund: externes M17-Referenz-Paket
  (`NOTBEL_M17_REFERENZ`) nicht im Repo (Selman-Artefakt). `gate_messung.py` bricht aus demselben
  Grund ab → **lokal nicht re-messbar.** Dokumentierter Gate-Zustand „(3) DG2 `M4.einraum` 0→1,
  sonst erfüllt" gilt für diese Raumerkennung (§21.1); meine Platzierung ändert keine Gate-Messfelder
  (die sind raumerkennungsseitig).

## 3. Prüfstrecke — 13 Pläne, Vergleich Vorher/Nachher

Lauf: `scripts/plan_pruefen.py <plan>` je Plan einzeln (RAM: 16,8 GB gesamt, zur Laufzeit nur
1–4 GB frei → Muthgasse/Am-Rain-EG im Swap, einzeln statt Batch, wie vom Owner vorgesehen).
Output je Plan in `Projekte/_ergebnis/<Plan>/` (6 PNG + `bericht.md` + `raeume.json`).

**„Vorher" = LUECKEN §7 Basislauf** (Default-Platzierung `build_default_bundle` auf **derselben**
Raumerkennung `c3b8186`). **„Nachher" = meine Platzierung.** Der Vergleich isoliert damit exakt
den Effekt meiner 43 Commits; die Raumerkennung ist in beiden identisch.

| Plan | Räume | Ausgänge | rz/SL/AP **vorher** | rz/SL/AP **nachher** | Δ ges. |
|---|--:|---|---|---|--:|
| Barawitzka_EG | 49 | 1 final | 6 / 5 / 0 | 6 / 5 / 0 | 0 |
| Mollgasse_EG | 64 | 8f+1s | 24 / 27 / 0 | 24 / 25 / 0 | −2 |
| Mollgasse_1KG | 31 | 1 final | 7 / 7 / 0 | 7 / 5 / 0 | −2 |
| Mollgasse_2KG | 30 | 1 stair | 8 / 4 / 1 | 9 / 3 / 1 | 0 |
| Muthgasse_E2 | 108 | 1 stair | 86 / 53 / 0 | 69 / 24 / 0 | **−46** |
| Rennweg_EG | 24 | 2f+3s | 9 / 8 / 0 | 9 / 8 / 0 | 0 |
| Rennweg_OG3 | 17 | 3 stair | 5 / 2 / 0 | 5 / 2 / 0 | 0 |
| AmRain_UG | 82 | 2f+4s | 59 / 32 / 0 | 59 / 17 / 0 | −15 |
| AmRain_EG | 136 | 2f+1s | 27 / 13 / 0 | 27 / 13 / 0 | 0 |
| AmRain_OG1 | 134 | 4 stair | 47 / 21 / 0 | 47 / 9 / 0 | −12 |
| AmRain_OG2 | 102 | 2 stair | 52 / 23 / 0 | 52 / 18 / 0 | −5 |
| AmRain_OG3 | 59 | 3 stair | 9 / 11 / 0 | 10 / 8 / 0 | −2 |
| AmRain_OG4 | 27 | **0** (bek.) | 8 / 5 / 0 | 8 / 0 / 0 | −5 |
| **Summe** | | | **459** | **419** | **−40** |

**Muster:** `rz` bleibt nahezu konstant (nur Muthgasse −17, OG3/2KG je +1), die Reduktion ist
fast ausschließlich `SL`/Aufheller — Wirkung der Platzierungs-Logik (D1-Aufheller-Bremse,
Sichtkette-Ausdünnung, Gang-Deckungs-Drossel). Kein Plan bekommt mehr Leuchten. Wo meine
Platzierung = Default liefert (Barawitzka, Rennweg EG/OG3, AmRain EG), sind die Zahlen identisch
→ bestätigt zugleich, dass die Raumerkennung §7 **exakt** reproduziert (Räume/Ausgänge/Segmente
deckungsgleich).

**Fluchtwege/Ausgänge:** je Plan identisch zu §7 (Raumerkennung unverändert). AmRain_OG4 weiter
0 Ausgänge (bekannt, s. u.).

**Pläne, die früher abbrachen und jetzt laufen:** alle 13 laufen end-to-end (Parse + Platzierung
+ Render). Durchgelaufen ist insbesondere **Muthgasse_E2** (Peak ~11 GB, historisch OOM-Risiko auf
16-GB-Maschine; hier via Swap in ~20 min) und **alle 6 Am-Rain-Geschosse** (Familie war auf
Alt-main nicht abgenommen). Kein Plan ist abgestürzt.

## 4. Befunde

**Keine neuen Raumerkennungs-Befunde** über LUECKEN §1–21 hinaus. Die bekannten reproduzieren
exakt (nicht als neu gemeldet): AmRain_OG4 0 Ausgänge/0 Stiegenhäuser (§6.2/F-07/R-09, P0, Selman);
$INSUNITS-Maßstab-Rückfall auf 8/13 (D-04); „kein Raum"-Leuchten (N-07, z. B. Muthgasse 48,
AmRain_EG 13).

**Offene Punkte auf Platzierungsseite (meine Lane, bekannt — von den `bericht.md` selbst gemeldet):**
- **WOHNUNG_PRIVAT-Leuchten (Board 1):** Muthgasse 31, AmRain_EG 3, OG2 3, OG1 1, OG3 2,
  Mollgasse_EG 2 → Tests `test_keine_leuchten_in_wohnung_privat[OG2/DG1]` rot (erwartet). Braucht
  Board-1-Entscheid (Leuchten in privaten Wohnungen).
- **LIFT/SCHACHT bzw. Treppenlauf/Verbotszone (N-03):** Muthgasse 3, AmRain_OG3 1 „auf
  Treppenlauf/Verbotszone".
- **Muthgasse Rotation 20/21 RZ-über-Tür abweichend** — auf dem geometrisch unsaubersten Plan
  (Fremdcluster 503×276 m, 48 Leuchten ohne Raum). Zu beobachten; Mischung aus Türgeometrie
  (Raumerkennung) und RZ-Rotation (meine Lane, vgl. M3). Kein Fix in diesem Lauf.
