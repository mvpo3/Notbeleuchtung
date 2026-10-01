# Übergabe an Selman (@polatselman) — die „nicht-im-Merge"-Pakete

> Von: Leonis (@mvpo3, Package `platzierung/`) · Stand: 2026-09-22 · Branch `leonis/demo-l-gebaeude` @ `d593bde`
> Kontext: Nach dem 12-Pläne-Gate-Lauf + Stapel-Merge kommen S-KG, S4d (Balkontür) und die Vokabular-Typen dran.
> Meine (Leonis-)Seite ist für alle drei vorbereitet — der Bau liegt in deiner Lane (Raumerkennung). Details + Abnahme unten.

Alle Links auf Branch `leonis/demo-l-gebaeude`.

---

## 1. Paket S-KG — Kellergeschosse + Garage  (deine Lane, mein Vorlauf steht)

**Von mir fertig:** Spec, GT-Messdaten, Abnahme-Runner, mm-genaues Abgleich-Material, und der
Engine-Vorlauf **NB-R13 (UG flüchtet HINAUF)** ist gebaut
(`src/notbeleuchtung/platzierung/bausteine.py:207` `ist_untergeschoss` + `fachpraxis`).
→ Sobald du KELLERABTEIL + Garage-Zirkulation lieferst, platziert die Engine **ohne weiteren Leonis-Bau**.

**Befund (leere Pläne 1KG/2KG, live gemessen):**
- 1KG: 31 Räume, **0 KELLERABTEILE** (real ~50 Einlagerungsräume „ER"), nur 4 Zirkulations-Segmente.
- 2KG: 30 Räume, 1 GARAGE (ein Riesen-Polygon), 5 Segmente, keine Fahr-/Gehwege.
- Folge: von 29 Experten-Leuchten im 2KG verfehlt die Engine 20 komplett; alle 8 beidseitigen
  Experten-RZ unerreichbar (die Wasserscheiden-Knoten existieren im Graph nicht).

**Soll:**
1. **Einlagerungsräume/Kellerabteile erkennen** (Stempel „ER"+Nummer; 1KG/2KG-Erklärungs-DXFs
   zeigen das Muster) → Raumtyp **KELLERABTEIL**.
2. **Garage-Zirkulation**: begehbare Wege (Fahrgassen + Gehbereiche). Fachpraxis NB-R17
   (`knowledge/notbeleuchtung/regeln.md`): Motorrad-Stellflächen durchquerbar,
   Doppelparker-/PKW-Flächen + Gruben NICHT — die Stempel (MOTORRAD/DOPPELPARKER/Pflichtstellplatz)
   stehen in den Plänen.
3. **Gebäudehälften** (Mollgasse/Anastasius-Grün-Gasse): Zirkulation je Gebäudehälfte
   zusammenhängend (Trennung entlang der Gebäudewand; EG ist die Referenz). Kein neues
   Contract-Feld nötig, solange die Graph-Komponenten die Trennung abbilden — falls du eines
   brauchst: erst in COORDINATION eintragen (3-Owner).
4. STGH-Treppenläufe im KG lieferst du schon (1KG 2×4, 2KG 4/0/3 — ✓); Leonis-seitig NB-R13 gebaut.

**Abnahme (messbar):**
```
python scripts/analyse/mollgasse_gt_vergleich.py 1KG 2KG
```
Ziel-Richtung: KELLERABTEIL > 0, Zirkulations-Segmente zweistellig, „fehlt" im 2KG deutlich < 20.

**Material:**
- Spec/Details: `docs/COORDINATION.md` §S-KG (Z. 555–584)
- Runner: `scripts/analyse/mollgasse_gt_vergleich.py`
- GT-Messdaten: `tests/fixtures/mollgasse_gt/{1KG,2KG}.json`
- Abgleich (mm-genau belegt): `knowledge/notbeleuchtung/abgleich/{1KG,2KG}/abgleich_*.md` + Bericht §K

---

## 2. Paket S4d — Balkontür  (deine Lane, meine Consumer-Seite steht + ist freigegeben)

**Von mir fertig + freigegeben (13.09.):** Consumer-Seite gebaut —
- `bausteine.ist_echte_tuer` — Phantom-Tür-Filter (>1300 mm = Wandloch), `bausteine.py:73`
- BALKON/TERRASSE aus communal ausgenommen (`fachpraxis.py:81`), R2/`aussen_tuer_rz`.

**Was fehlt = dein Fix:** Balkontüren dürfen **nicht als Gebäude-Ausgänge** (`final_exit`) zählen —
das ist die Wurzel der dünnen Elektroplan-Fluchtwege und deckt meine Naht-Notiz (Müllraum-Südtür
`von==nach`) gleich mit. Deine Messung 08.09. zeigte den Effekt schon (Muthgasse `final_exit` 9→1
nach Stempel-Rückschrieb: 6 der Weggefallenen waren Balkontüren).

**Nach deinem Fix — Ping an mich:** ich re-teste dann Elektroplan v9+ und die E2E-Bänder
(`ist_echte_tuer`/R2 hängen an derselben Tür-Semantik). Kein Vorbau meinerseits möglich.

---

## 3. Vokabular-Typen KINDERZIMMER / WOHNKÜCHE  (deine Token-Seite, Norm = Enis)

Architektur-Regel: Leonis parst kein YAML → Platzierung liest Raumtypen generisch via
`norm.fuer_raum()`. Sobald der Typ verdrahtet ist, greift die Platzierung **automatisch**.

- **KINDERZIMMER**: schon Kanon (`raumtyp.py` CHILDREN_ROOM, Alias `kz`; `nutzungsklasse.py`
  WOHNUNG_PRIVAT; `lb_extraktion.yaml`; `regel_deckung.yaml`). Wenn hier noch was hakt, ist es
  ein **Erkennungs-Token**, nicht die Platzierung — deine Lane.
- **WOHNKÜCHE**: **kein Kanon-Typ** (nur in `_port`-Kommentaren). Neu anzulegen — Muster KINDERZIMMER:
  - **Selman:** `RoomType.WOHNKUECHE` + Erkennungs-Token in `raumerkennung/raumtyp.py`
    (Alias-Kandidat mit dir gegenprüfen — `wr` war schon als Fehltreffer verworfen),
    `nutzungsklasse.py` → WOHNUNG_PRIVAT.
  - **Enis:** NormAnforderung (Wohnküche = privater Wohnraum → keine Notbeleuchtung, wie
    WOHNUNG_PRIVAT-Skip), `lb_extraktion.yaml unterstuetzte_raum_typen` + `regel_deckung.yaml`.
  - Guard: `tests/contract/test_lb_raumtyp_naht.py` guardet beide Richtungen hart → gemeinsam mergen.
  - **Naht an Leonis:** Ping wenn verdrahtet — Platzierung greift automatisch, ich prüfe nur die
    Consumer-Naht (kein Bau).

---

**Reihenfolge-Empfehlung:** S-KG (größter Hebel für die GT-Quote) → S4d → WOHNKÜCHE.
Bei jedem: nach deinem Stand pingst du mich, ich fahre die Consumer-/Naht-Prüfung + GT-Re-Run.
