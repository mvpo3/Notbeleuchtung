# Vokabular-Lücke v3 — Zensus, Gruppen a/b/c, Wirkung, Vorlage an Enis

Stand 2026-09-29, Selman. Nur Messung und Doku. Dieses Dokument ändert keinen Code, keinen
Contract und keinen Test. Die Entscheidung über den Slice „Vorr." (`5f17378`) liegt beim Owner
und ist **offen** (Teil 5).

## 0. Anlass, Datenbasis, Methode

**Anlass.** Owner-Auftrag 2026-09-29: Welcher Teil der magenta dargestellten Räume der
v3-Ausgabe geht auf fehlendes Vokabular zurück (Stempeltext steht im Plan, das Wörterbuch kennt
ihn nicht)? Was kann Selman selbst schließen, und was braucht ein Fachurteil von Enis?

**Datenbasis.** v3 = Commit `f91b3cc` (Branch `selman/raumerkennung-v3`, Ausgabe-Commit
`fa6a309`). `git diff aa05143 f91b3cc -- src` ist leer, der Code-Stand ist also `aa05143`.
Gemessen sind 23 Geschosse:

- Rennweg: UG, EG, OG1–OG3, DG1, DG2 (7)
- Mollgasse: 1./2. Kellergeschoß, EG, 1.–4. OG, Dachgeschoß (8)
- Muthgasse: E2–E9 (8)

Die Räume stammen aus `Projekte/_ergebnis_raumerkennung/<Projekt>_v3/<Plan>/_cache.pkl`. Die
SHA-256 der Eingangs-DXF sind gegen `kennzahlen.json` geprüft, 23 von 23 gleich [ZENSUS:3].
Insgesamt sind es 1446 Räume, davon 248 magenta mit 3971,1 m² [ZENSUS:93].

**Kategorie je Raum.** Grundlage ist `scripts/analyse/raumerkennung_darstellung._kategorie`
(magenta = unbekannt, unbestimmt oder Nische). Jeder magenta Raum bekommt genau eine Ursache;
geprüft wird in dieser Reihenfolge [ZENSUS:46-56]:

- **N**: Nische. Kommt 0-mal vor; NISCHE vergibt kein Modul in `src/` [ZENSUS:120].
- **K**: unbestimmt. Der Raum ist GANG oder VORRAUM, aber ohne Nutzungsklasse.
- **Z**: ein Text im Raum ergibt einen Typ, der Raum ist trotzdem leer.
  - Z1: ein zugeordneter Stempel typt.
  - Z2: der Stempel gehört zu einem anderen Raum.
  - Z3: ein Stempel ohne Raum (`kein_polygon` oder entfallen).
  - Z4: der Text ist gar kein Stempel.
- **V**: Stempeltext ohne Wörterbuch-Treffer.
  - V1: der Stempel ist dem Raum zugeordnet.
  - V2: der Stempeltext liegt im Polygon, ist dem Raum aber nicht zugeordnet.
- **G**: kein Text.
  - G1: Überlappung ≥ 50 % mit einem anderen Raum.
  - G2: Fläche < 2 m².
  - G3: Rest-Komponente `rest_*`.
  - G4: sonstige Fläche ohne Text.

**Typpfad (Zeilen auf `aa05143`).**

1. `provider.py:70` ruft die Kaskade auf (`kaskade.raeume_aus_kaskade`).
2. `kaskade.py:101` holt die Stempel (`stempel_anker.finde_stempel`, `stempel_anker.py:242`).
   Der Stempel-Typ ist `raumtyp_flags(name)[0]` (`stempel_anker.py:107-109`). Ein loser
   TEXT/MTEXT wird **nur dann ein Stempel**, wenn sein Name typt oder ein Kürzel-Kandidat ist
   (`stempel_anker.py:230-233`).
3. Danach folgen in der Kaskade:
   - Raum-Layer und Hatch: `kaskade.py:102/104`
   - `ordne_zu`: `kaskade.py:119-120`
   - Flutung: `kaskade.py:128-145`
   - Rückschreibung des Typs: `kaskade.py:153-162`
   - `kuerzel_entscheid`: `kaskade.py:168-175`
   - `rest_komponenten`: `kaskade.py:178`. Diese Stufe typt nur SCHACHT, STIEGENHAUS und GANG
     geometrisch und liest keine Stempel.
4. Nach der Kaskade:
   - `provider.py:83`: `typisiere_geometrisch`
   - `provider.py:164`: `liftschacht_reste`
   - `provider.py:184`: `bilde_wohnungen`. Die Klasse wird statisch vergeben
     (`wohnungen.py:190-191`), außer für GANG und VORRAUM (`wohnungsklasse.py:99`).
   - `provider.py:216`: `finde_lifte`
5. Das Wörterbuch ist `raumtyp_flags` (`raumtyp.py:157-172`). Die Reihenfolge ist
   `_EXTRA_OVERRIDE` → `classify_room` → `_EXTRA_LABELS` → `_EXTRA_DIRECT`. Alle vergleichen
   token-exakt mit dem Muster `[A-Za-zÄÖÜäöüß]+` (`raumtyp.py:89`). Es gibt keine Toleranz für
   Umlaute oder Tippfehler [ZENSUS:5-44], [KANON:54-69].

Auf `5f17378` verschieben sich die Zeilen in `raumtyp.py` ab `:67` um +5.

**Wirkung.** Grundlage sind 70 echte `ArchitekturRaumProvider().parse`-Läufe in 7 Szenarien.
Basis 0 ist `aa05143`. Szenario 0 ist auf allen 21 gelaufenen Plänen feldweise gleich den
v3-Extrakten [WIRKUNG:3-6, :132-155]. Ein Prüfer hat mit eigenem Code gegengerechnet und nur
Rundungsabweichungen ≤ 0,05 m² gefunden [WIRKUNG:8-15]. Die Zuordnung je Text, die
Magenta-Zahlen und die Flag-Listen in diesem Dokument stammen aus eigenen Auswertungen dieser
Läufe (kein neuer parse). Gegenprobe: Die Magenta-Zahl von Szenario 0 trifft den Zensus auf 21
von 21 Plänen, 0 Abweichungen [MAGENTA:1].

**Quellen** (lokaler Arbeitsordner, nicht im Repo):

| Kürzel | Datei | Inhalt |
|---|---|---|
| ZENSUS | `zensus_magenta.md` / `.json` | 248 magenta Räume mit Ursache, Stempeltexten, Typpfad |
| KANON | `kanon.md` | Kanon (24 Labels), Match-Logik, Rohtexte, Umlaut-Befund, Notlicht-Flags |
| DIREKT | `direktwirkung_slice.md` | Text- und Stempel-Ebene des Slices „Vorr." (ezdxf, kein parse) |
| WIRKUNG | `wirkung.md` / `.json` | 70 parse-Läufe, Szenarien 0, a, a+n, n, b, c, c-schleuse |
| GRUPPEN | `_vl_gruppen.py` → `_vl_gruppen.txt` | magenta je Projekt/Geschoss auf a/b/c/d/Z/G/K |
| PROTEXT | `_vl_protext.py` → `_vl_protext.txt` | Wirkung b/c je Stempeltext (über `stempel[].raum_id` des Laufs) |
| MAGENTA | `_vl_magenta.py` → `_vl_magenta.txt` | Magenta-Zahl je Szenario, validiert gegen Zensus |
| FLAGS | `_vl_flags.py` → `_vl_flags.txt` | Flag-Wechsel mit Raum-IDs je Vergleich |
| ZNACH | `_vl_zensus.py` → `_vl_zensus.txt` | Nachzählung Zensus (K-Liste, Mehrfachtexte) |

---

## 1. Teil 1 — Zensus: magenta Räume mit Stempeltext

### 1.1 Überblick je Geschoss nach Gruppe

Gruppen siehe Teil 2. a, b, c und d sind V-Räume, also Räume mit Stempeltext. Z, G und K sind
die übrigen Ursachen. Jede Zelle zeigt Anzahl / m² [GRUPPEN].

| Projekt | Geschoss | a | b | c | d | Z | G | K | Σ |
|---|---|---|---|---|---|---|---|---|---|
| Rennweg | DG1 | – | – | 1 / 15,9 | – | – | – | 1 / 12,2 | 2 / 28,1 |
| Rennweg | DG2 | – | – | – | – | – | – | 1 / 10,8 | 1 / 10,8 |
| Rennweg | EG | – | 5 / 163,7 | – | – | – | 2 / 2,6 | – | 7 / 166,3 |
| Rennweg | OG1 | – | 1 / 73,1 | – | – | – | – | – | 1 / 73,1 |
| Rennweg | OG2 | – | – | 1 / 59,5 | – | – | – | – | 1 / 59,5 |
| Rennweg | OG3 | – | – | – | – | – | 1 / 6,6 | 1 / 9,4 | 2 / 15,9 |
| Rennweg | UG | – | 6 / 22,2 | 1 / 6,1 | – | – | 4 / 64,5 | – | 11 / 92,8 |
| **Rennweg** | **Σ** | – | **12 / 258,9** | **3 / 81,5** | – | – | **7 / 73,7** | **3 / 32,4** | **25 / 446,5** |
| Mollgasse | 1.Kellergeschoß | – | 12 / 605,6 | – | – | 1 / 3,7 | 11 / 316,6 | – | 24 / 926,0 |
| Mollgasse | 2.Kellergeschoß | – | 14 / 658,0 | 1 / 5,9 | – | 2 / 52,4 | 2 / 23,1 | – | 19 / 739,4 |
| Mollgasse | Erdgeschoß | – | 6 / 218,4 | 1 / 3,2 | 3 / 75,1 | – | 1 / 13,9 | 3 / 18,9 | 14 / 329,6 |
| Mollgasse | 1.Obergeschoß | – | – | – | 7 / 138,3 | – | 1 / 2,7 | – | 8 / 141,0 |
| Mollgasse | 2.Obergeschoß | – | – | – | 6 / 121,6 | 1 / 5,4 | 2 / 6,1 | – | 9 / 133,1 |
| Mollgasse | 3.Obergeschoß | – | 2 / 15,9 | 2 / 20,6 | 5 / 178,0 | 1 / 5,4 | 1 / 2,7 | 2 / 10,0 | 13 / 232,6 |
| Mollgasse | 4.Obergeschoß | – | 2 / 142,7 | 1 / 3,0 | 2 / 83,8 | – | 1 / 2,6 | 2 / 8,7 | 8 / 240,8 |
| Mollgasse | Dachgeschoß | – | – | – | 1 / 20,6 | – | 1 / 2,0 | 3 / 19,7 | 5 / 42,3 |
| **Mollgasse** | **Σ** | – | **36 / 1640,7** | **5 / 32,7** | **24 / 617,5** | **5 / 66,9** | **20 / 369,6** | **10 / 57,2** | **100 / 2784,8** |
| Muthgasse | E2 | 3 / 26,4 | 1 / 4,9 | 5 / 17,8 | – | – | – | 2 / 20,6 | 11 / 69,7 |
| Muthgasse | E3 | 7 / 39,8 | – | 8 / 39,7 | – | – | – | 3 / 37,4 | 18 / 116,9 |
| Muthgasse | E4 | 5 / 38,0 | – | 7 / 36,0 | – | – | – | 3 / 28,5 | 15 / 102,5 |
| Muthgasse | E5 | 5 / 20,6 | – | 8 / 38,4 | – | – | – | 7 / 43,5 | 20 / 102,5 |
| Muthgasse | E6 | 7 / 31,3 | – | 8 / 38,4 | – | – | – | 7 / 42,1 | 22 / 111,8 |
| Muthgasse | E7 | 3 / 13,3 | – | 5 / 34,3 | – | – | – | 5 / 36,0 | 13 / 83,6 |
| Muthgasse | E8 | 4 / 17,3 | – | 6 / 34,3 | – | – | – | 4 / 29,8 | 14 / 81,4 |
| Muthgasse | E9 | 1 / 3,7 | – | 5 / 22,0 | – | – | 1 / 21,3 | 3 / 24,2 | 10 / 71,2 |
| **Muthgasse** | **Σ** | **35 / 190,5** | **1 / 4,9** | **52 / 261,0** | – | – | **1 / 21,3** | **34 / 262,1** | **123 / 739,8** |
| **Gesamt** | **Σ** | **35 / 190,5** | **49 / 1904,5** | **60 / 375,3** | **24 / 617,5** | **5 / 66,9** | **28 / 464,7** | **47 / 351,7** | **248 / 3971,1** |

Zusammengefasst:

- **Vokabular im engeren Sinn (a + b + c): 144 von 248 Räumen, 2470,3 von 3971,1 m² = 62 %
  der magenta Fläche.**
  - Rennweg: 15 von 25 Räumen, 340,4 von 446,5 m² (76 %).
  - Mollgasse: 41 von 100 Räumen, 1673,4 von 2784,8 m².
  - Muthgasse: 88 von 123 Räumen, 456,4 von 739,8 m².
- **d (Stempeltext, aber kein Raumname):** 24 Räume, 617,5 m², nur Mollgasse.
- **Z (Zuordnung):** 5 Räume, 66,9 m².
- **G (Geometrie, kein Text):** 28 Räume, 464,7 m².
- **K (Klassenfrage):** 47 Räume, 351,7 m².
- Der Zensus meldet für V 168 Räume und 3087,8 m²; das ist genau a + b + c + d
  [ZENSUS:93], [GRUPPEN].

### 1.2 V — Stempeltext ohne Typ (vollständig)

Diese Tabelle übernimmt die Zensus-Tabelle [ZENSUS:126-168]; m² ist die Raumfläche. Ein Raum
mit mehreren verschiedenen Texten zählt in jeder Zeile. Deshalb ergeben die Zeilen 169
Nennungen bei 168 V-Räumen: Mollgasse 2.KG `rest_6` trägt `ER 09+10`, `ER 11`, `ER 12` und
`ER-GESAMT` [ZNACH].

| Text (normalisiert) | Rohschreibweise(n) | Räume | m² | Unterfall | Pläne | Beispiel-Raum | Gruppe |
|---|---|---:|---:|---|---|---|---|
| VORR. | `Vorr.` ×35 | 35 | 190,5 | V2 ×35 | Muthgasse E2–E9 | Muthgasse E4 `raum_80` (13,1) | a |
| SR | `SR` ×24 | 24 | 104,5 | V1 ×1, V2 ×23 | Mollgasse EG, Muthgasse E2–E9 | Muthgasse E8 `raum_70` (6,1) | c |
| TOP | 20 Varianten (`TOP 8`, `TOP 2 + 3`, `TOP 22 (SONDERWUNSCH)` …) | 22 | 572,8 | V1 ×22 | Mollgasse EG, 1.–4. OG | Mollgasse 3.OG `raum_59` (76,2) | d |
| AUFZUG | `Aufzug 1` ×8, `Aufzug 2` ×8 | 16 | 47,5 | V2 ×16 | Muthgasse E2–E9 | Muthgasse E2 `raum_77` (3,0) | c |
| ER | 16 Varianten `ER nn` (`ER 09+10` …) | 14 | 221,9 | V1 ×13, V2 ×1 | Mollgasse 1.KG, 2.KG | Mollgasse 1.KG `raum_9` (54,6) | b |
| SCHL. | `Schl.` ×12 | 12 | 101,8 | V1 ×12 | Muthgasse E2–E9 | Muthgasse E3 `raum_50` (13,0) | c |
| INNENHOF | `INNENHOF` ×4 | 4 | 286,7 | V1 ×4 | Mollgasse 1.KG, 2.KG | Mollgasse 1.KG `raum_4` (266,6) | b |
| SCHRANKR. | `SCHRANKR.` ×2, `Schrankr.` ×1 | 3 | 20,8 | V1 ×2, V2 ×1 | Mollgasse 3.OG, Muthgasse E2 | Mollgasse 3.OG `raum_41` (8,7) | b |
| AUFZUG # PERS. | `AUFZUG 8 PERS.` ×2 | 2 | 14,8 | V1 ×2 | Mollgasse 3.OG, 4.OG | Mollgasse 3.OG `raum_35` (11,8) | c |
| DOPPELPARKER #I-# | `DOPPELPARKER 2072i-205` ×2 | 2 | 157,0 | V1 ×2 | Mollgasse 2.KG | `raum_16` (145,1) | b |
| ER-GESAMT | `ER-GESAMT` ×2 | 2 | 54,9 | V1 ×1, V2 ×1 | Mollgasse 2.KG | `raum_21` (32,2) | b |
| GARAGENRAMPE | `GARAGENRAMPE` ×2 | 2 | 50,2 | V1 ×2 | Mollgasse 1.KG, EG | Mollgasse EG `raum_62` (30,4) | b |
| PODEST | `PODEST` ×2 | 2 | 21,0 | V1 ×2 | Mollgasse 4.OG, EG | Mollgasse EG `raum_60` (15,2) | b |
| WR-H | `WR-H` ×2 | 2 | 7,3 | V1 ×2 | Rennweg UG | `raum_13` (5,8) | b |
| BÜRO | `BÜRO` | 1 | 8,8 | V1 | Mollgasse 3.OG | `raum_58` (8,8) | c |
| DACHGESCHOSS | `DACHGESCHOSS` | 1 | 20,6 | V1 | Mollgasse Dachgeschoß | `raum_31` (20,6) | d |
| DBA RAUM | `DBA Raum` | 1 | 6,1 | V1 | Rennweg UG | `raum_17` (6,1) | c |
| DOPPELPARKERGRUBE | `DOPPELPARKERGRUBE` | 1 | 360,0 | V1 | Mollgasse 2.KG | `raum_11` (360,0) | b |
| DUSCHE-H | `Dusche-H` | 1 | 1,5 | V1 | Rennweg UG | `raum_9` (1,5) | b |
| EIGENGARTEN TOP | `EIGENGARTEN TOP 1` | 1 | 91,8 | V1 | Mollgasse EG | `raum_8` (91,8) | b |
| ERDGESCHOSS | `ERDGESCHOSS` | 1 | 24,1 | V1 | Mollgasse EG | `raum_52` (24,1) | d |
| FLACHDACH BEGRÜNT | `FLACHDACH BEGRÜNT` | 1 | 136,9 | V1 | Mollgasse 4.OG | `raum_1` (136,9) | b |
| GARAGENEINFAHRT | `Garageneinfahrt` | 1 | 14,1 | V1 | Rennweg EG | `raum_19` (14,1) | b |
| GESCHÄFTLOKAL | `GESCHÄFTLOKAL` | 1 | 111,0 | V1 | Rennweg EG | `raum_12` (111,0) | b |
| GESCHÄFTSLOKAL | `Geschäftslokal 1` | 1 | 29,1 | V1 | Rennweg EG | `raum_10` (29,1) | b |
| GULLY FLÄCHE | `GULLY FLÄCHE` | 1 | 165,0 | V1 | Mollgasse 1.KG | `raum_15` (165,0) | b |
| KLEINKINDERSPIELPLATZ | `KLEINKINDERSPIELPLATZ` | 1 | 60,6 | V1 | Mollgasse EG | `raum_5` (60,6) | b |
| MEDIENRAUM | `MEDIENRAUM` | 1 | 5,9 | V1 | Mollgasse 2.KG | `raum_12` (5,9) | c |
| MULTIF.R. | `Multif.r.` | 1 | 10,4 | V2 | Muthgasse E7 | `raum_67` (10,4) | c |
| MÜLLPLATZ | `Müllplatz` | 1 | 4,0 | V1 | Rennweg EG | `raum_9` (4,0) | b |
| NIEDERSP. | `NIEDERSP.` | 1 | 9,8 | V1 | Mollgasse 2.KG | `raum_3` (9,8) | b |
| NIEDERSP.R. | `NIEDERSP.R.` | 1 | 11,2 | V1 | Mollgasse 1.KG | `raum_3` (11,2) | b |
| STAUDENBEET | `STAUDENBEET` | 1 | 11,4 | V1 | Mollgasse EG | `raum_1` (11,4) | b |
| TV RAUM | `TV Raum` | 1 | 15,9 | V1 | Rennweg DG1 | `raum_7` (15,9) | c |
| UMKLEIDE-D | `Umkleide-D` | 1 | 4,9 | V1 | Rennweg UG | `raum_4` (4,9) | b |
| VORPLATZ | `VORPLATZ` | 1 | 8,9 | V1 | Mollgasse EG | `raum_6` (8,9) | b |
| WOHNBEREICH | `Wohnbereich` | 1 | 59,5 | V1 | Rennweg OG2 | `raum_2` (59,5) | c |
| WOHNKCHE | `Wohnkche` | 1 | 73,1 | V1 | Rennweg OG1 | `raum_10` (73,1) | b |
| WR-D | `WR-D` | 1 | 2,8 | V1 | Rennweg UG | `raum_2` (2,8) | b |
| WR-H /UMKLEIDE | `WR-H /Umkleide` | 1 | 5,7 | V1 | Rennweg UG | `raum_8` (5,7) | b |
| ZUGANGSWEG | `Zugangsweg` | 1 | 5,5 | V1 | Rennweg EG | `raum_18` (5,5) | b |

**Warum Muthgasse V2 statt V1.** Muthgasse schreibt die Raumnamen als lose MTEXT auf
`A-AREA-IDEN`. Ein loser Name ohne Wörterbuch-Treffer wird gar kein Stempel
(`stempel_anker.py:230-233`) [ZENSUS:117]. Deshalb hängt dort kein zugeordneter Stempel am
Raum. Der Text liegt nur im Polygon.

**Weitere Auffälligkeiten** [ZENSUS:115-119]:

- Die `TOP …`-Stempel sind Wohnungs-Sammelstempel. Die Stempel-m² passt bei 0 von 22 Räumen.
- 17 von 18 `Aufzug …`-Räumen decken sich zu ≥ 50 % mit einem `lift_*`-Raum. Die
  Duplikatprüfung `lift_erkennung.py:183` vergleicht nur mit Räumen vom Typ LIFT.
- Zusätzlich gibt es 354 Stempel ohne zugeordneten Raum, 108 davon ohne Typ. Beispiel:
  Mollgasse EG 2× `GESCHÄFTSLOKAL` mit `kein_polygon`. Diese Stempel erzeugen keinen Raum und
  zählen daher in keiner magenta Zahl [ZENSUS:222, :253].

### 1.3 Z — Typtext vorhanden, Raum leer (kein Vokabularfall)

| Text | Räume | m² | Unterfall | Plan / Raum | Befund |
|---|---:|---:|---|---|---|
| `BAD` | 2 | 10,8 | Z3 | Mollgasse 2.OG `rest_4` (5,40), 3.OG `rest_2` (5,36) | Stempel 4,71 m², Flutung 0,89 m² → `kein_polygon` |
| `GANG` | 1 | 39,8 | Z3 | Mollgasse 2.KG `rest_7` | 3 GANG-Stempel, Flutung 0,00/0,02/0,00 m² |
| `BRE ABLUFT GARAGE` | 1 | 12,6 | Z3 | Mollgasse 2.KG `rest_3` | Anmerkung (Brandrauch-Entlüftung), typt nur über das Token `garage` |
| `LUFTRAUM\nGARAGE` | 1 | 3,7 | Z4 | Mollgasse 1.KG `rest_2` | Anmerkung auf 02-TXT, keine m²-Zeile |

Quelle: [ZENSUS:174-198]. Bei allen vier Z3-Räumen ist der Pfad derselbe:

1. Der Stempel findet über `ordne_zu` kein Polygon.
2. Die Flutung liefert < 1 m², also setzt `kaskade.py:133-135` `kein_polygon`.
3. An derselben Stelle entsteht später ein `rest_*`-Raum. `rest_komponenten._typisiere`
   lässt ihn leer, weil es keine Stempel liest.

Das ist eine Zuordnungs- und Geometriefrage, keine Vokabelfrage. Selman ist zuständig.

### 1.4 K — unbestimmt (Klassenfrage, kein Vokabular)

47 Räume mit 351,7 m²: GANG 6 (44,3 m²), VORRAUM 41 (307,4 m²) [ZENSUS:102-103]. Bei diesen
Räumen ist der Typ bekannt. Das zweistufige Verfahren (`wohnungen.py:190-191`,
`wohnungsklasse.py:99` `SCOPE_TYPEN`) lässt die Klasse aber auf `None`. Die Darstellung zeigt
das als „unbestimmt" (magenta). Liste [ZNACH]:

| Plan | Räume (Typ, m²) |
|---|---|
| Rennweg DG1 | `raum_4` GANG 12,19 |
| Rennweg DG2 | `raum_1` VORRAUM 10,84 |
| Rennweg OG3 | `raum_10` GANG 9,38 |
| Mollgasse 3.OG | `raum_48` GANG 4,58 · `raum_51` VORRAUM 5,41 |
| Mollgasse 4.OG | `raum_10` GANG 5,95 · `raum_12` VORRAUM 2,74 |
| Mollgasse Dachgeschoß | `raum_9` VORRAUM 9,10 · `raum_12` VORRAUM 7,18 · `raum_13` GANG 3,44 |
| Mollgasse EG | `raum_23` VORRAUM 7,91 · `raum_49` VORRAUM 2,17 · `raum_55` GANG 8,77 |
| Muthgasse E2 | `raum_51` 9,07 · `raum_54` 11,56 (VORRAUM) |
| Muthgasse E3 | `raum_67` 9,07 · `raum_76` 13,10 · `raum_80` 15,23 (VORRAUM) |
| Muthgasse E4 | `raum_47` 4,18 · `raum_50` 9,07 · `raum_76` 15,23 (VORRAUM) |
| Muthgasse E5 | `raum_6` 3,68 · `raum_45` 5,65 · `raum_54` 5,65 · `raum_65` 4,36 · `raum_72` 11,28 · `raum_79` 8,41 · `raum_108` 4,47 (VORRAUM) |
| Muthgasse E6 | `raum_42` 5,65 · `raum_53` 4,36 · `raum_60` 11,28 · `raum_65` 2,25 · `raum_67` 8,41 · `raum_109` 4,47 · `raum_110` 5,65 (VORRAUM) |
| Muthgasse E7 | `raum_8` 6,19 · `raum_23` 4,47 · `raum_33` 5,65 · `raum_44` 11,28 · `raum_51` 8,41 (VORRAUM) |
| Muthgasse E8 | `raum_27` 4,47 · `raum_37` 5,65 · `raum_50` 11,28 · `raum_57` 8,41 (VORRAUM) |
| Muthgasse E9 | `raum_13` 11,28 · `raum_18` 4,47 · `raum_23` 8,41 (VORRAUM) |

Folge für Teil 5: Jeder zusätzlich als VORRAUM typisierte Raum, dessen Klasse offen bleibt,
wandert von V nach K und **bleibt magenta**.

### 1.5 Richtigstellungen (belegt)

- **`WC-D` und `VR Personal` sind in v3 typisiert.**
  - `WC-D` ist Rennweg UG `raum_3`, WC / WOHNUNG_PRIVAT, 1,48 m².
  - `VR Personal` ist `raum_6`, VORRAUM / WOHNUNG_PRIVAT, 4,77 m².
  - `raumtyp_flags('WC-D')` = `('WC', False, False)`, `raumtyp_flags('VR Personal')` =
    `('VORRAUM', True, True)` [ZENSUS:218, :220], [KANON:141, :144].
  - Im UG untypisiert sind 7 Räume: WR-D, Umkleide-D, WR-H /Umkleide, Dusche-H, 2× WR-H und
    DBA Raum [KANON:153].
- **Der 111-m²-Stempel heißt `GESCHÄFTLOKAL`, ohne Fugen-s** (U+00C4). Das ist Rennweg EG
  `raum_12`, 111,03 m². Der 29-m²-Stempel heißt `Geschäftslokal 1` (`raum_10`)
  [ZENSUS:222 Anm. 1], [KANON:155].
- **Bei `Wohnkche` fehlt das ü schon in der DXF.**
  - Die Rohbytes lauten `Wohnkche`, ohne Byte zwischen `k` und `c`. Das gilt in BLOCK_RECORD
    `Wohnkche__10`, ATTDEF und ATTRIB.
  - Header: `$ACADVER` AC1032 (UTF-8-DXF), `$DWGCODEPAGE` ANSI_1252.
  - Dieselbe Datei trägt 2620 korrekte UTF-8-Umlaut-Sequenzen und 0 cp1252-Einzelbyte-Umlaute.
  - Es handelt sich also nicht um einen Lese- oder Encoding-Fehler [KANON:127-134].
- **Technikraum und Waschraum sind Kanon.** Auf `aa05143` gilt `technikraum` → TECHNIK
  (`raumtyp.py:101`) und `waschraum` → WASCHKÜCHE (`raumtyp.py:153`, `_EXTRA_OVERRIDE`). Auf
  `5f17378` stehen die Einträge in `:106` / `:158` [KANON:33, :36].
- **`WR` → WASCHKÜCHE wäre falsch.**
  - Die Rennweg-UG-Stempel `WR-D`, `WR-H`, `WR-H /Umkleide` gehören zum Personalbereich neben
    `WC-D`, `WC-H`, `Umkleide-D`, `Dusche-H` und `VR Personal` [KANON:138-150]. Gemeint ist
    ein Waschraum für Personal, keine Waschküche.
  - Außerdem steht `WR` im Repo auch für Wechselrichter und „Wiener Null". Der Sweep von
    2026-09-08 hat `wr` deshalb bewusst nicht aufgenommen (`docs/OFFENE_FRAGEN.md:440-441`).
- **Die richtige Schreibweise `Wohnküche` typt heute schon als KÜCHE.** Das läuft über den
  Kompositum-Kopf (`tests/raumerkennung/test_raumtyp.py:139` auf `aa05143`, `:155` auf
  `5f17378`; Befehlsausgabe auf `5f17378`: `'Wohnküche' → ('KÜCHE', False, False)`,
  `'Wohnkche' → None`). Offen ist nur der Tippfehler-Fall.

---

## 2. Teil 2 — Gruppen a / b / c / d / K

### 2.1 Regeln

- **a — Schreibweise oder Abkürzung eines Kanon-Worts.** Die Bedeutung ist im Plan eindeutig
  belegt, Typ und Klasse folgen aus dem Kanon, und es braucht kein Fachurteil. Das kann Selman
  in seiner Lane (Wörterbuch) selbst eintragen.
- **b — Das Wort ist eindeutig, offen ist die Kanon-Festlegung.** Entweder fehlt der Typ im
  Kanon: dann ist es eine Naht-Änderung (`docs/VOKABULAR.md` § 1 + § 3, LB-Stützliste mit
  `tests/contract/test_lb_raumtyp_naht.py`). Oder die Zuordnung auf einen vorhandenen Typ legt
  eine Nutzung fest. Die Klasse ist in der Regel naheliegend; wo nicht, ist das markiert.
  Gruppe b ist genau die simulierte Liste b [WIRKUNG:176-207].
- **c — Die Bedeutung ist mehrdeutig.** Kürzel ohne Auflösung oder ein Wort mit mehreren
  möglichen Nutzungen. Simuliert ist nur **eine** Lesart [WIRKUNG:208-219]. Die Entscheidung
  braucht Enis' Fachurteil.
- **d — Kein Raumname.** Wohnungs-Sammelstempel, Geschossbezeichnungen, Anmerkungen. Ein
  Wörterbuch-Eintrag wäre falsch. Das ist eine Zuordnungsfrage, Selman ist zuständig.
- **K — Typ bekannt, Klasse offen.** Das betrifft die Wohnungsklasse (Selman, S7-Regeln), nicht
  das Vokabular.

### 2.2 Zuordnung je Text

Die Spalte „Kanon?" zeigt, ob der Zieltyp der Simulation schon im Kanon steht [KANON:14-39].

| Text | Räume / m² | Gruppe | Simulierte Lesart (Typ / Klasse / Flags) | Kanon? | Begründung | Bestehender Punkt |
|---|---|---|---|---|---|---|
| `Vorr.` | 35 / 190,5 | **a** | VORRAUM / dynamisch / 11 | ja | Muthgasse-Raumstempel auf `A-AREA-IDEN`, 49 MTEXT, jeder mit m²-Nachbar ≤ 193 mm [DIREKT:93-106]. `vr` → VORRAUM steht schon im Wörterbuch. | Frage 2 (`OFFENE_FRAGEN.md:713-717`); vom Owner am 2026-09-29 übernommen, Slice `5f17378` |
| `GESCHÄFTLOKAL`, `Geschäftslokal 1`, `GESCHÄFTSLOKAL` | 2 / 140,1 (+2 Stempel ohne Raum) | b | GESCHAEFTSLOKAL / ALLGEMEIN_NEBENRAUM / 01 | nein | Wort eindeutig, Nichtwohn-Einheit. Der Contract kennt keine Nichtwohn-Klasse (`raum_modell.py:22-25`) [KANON:51-52]. | 3-Owner-Frage (`OFFENE_FRAGEN.md:443-448`) |
| `Wohnkche` | 1 / 73,1 | b | WOHNKÜCHE / WOHNUNG_PRIVAT / 00, in AUFENTHALTSRAUM | nein | Wort eindeutig (Wohnküche). Ob Aufenthaltsraum oder nicht, entscheidet die Wohnung und `raum_12` (2.3). | Board 2026-09-22 (`wohnungsklasse.py:105-106`), `COORDINATION.md` 2026-09-26 |
| `Umkleide-D`, `WR-H /Umkleide` | 2 / 10,6 | b | UMKLEIDE / ALLGEMEIN_NEBENRAUM / 01 | nein | Personalraum, keine Wohnung | – |
| `WR-H`, `WR-D` | 3 / 10,1 | b | SANITAER / WOHNUNG_PRIVAT / 00 | nein (Leonis-Synonym, `platzierung/bausteine.py:27,30`) | Personal-Waschraum. **Klasse nicht klar**: WOHNUNG_PRIVAT nimmt Notlicht, siehe 4.1 B3 | – |
| `Dusche-H` | 1 / 1,5 | b | BAD / WOHNUNG_PRIVAT / 00 | ja | Personaldusche, gleiche Klassenfrage wie WR | `dusche` bewusst nicht aufgenommen (`OFFENE_FRAGEN.md:440-441`) |
| `ER nn` (Regex) | 14 / 221,9 | b | KELLER / ALLGEMEIN_NEBENRAUM / 01 | ja | Einlagerungsraum im Keller. Zwei Kanon-Typen konkurrieren: `einlagerungsraum` → ABSTELLRAUM im Port (`_port/models/room.py:45`) [WIRKUNG:221]. | Alias `er` abgelehnt (`OFFENE_FRAGEN.md:431-433`) |
| `ER-GESAMT` | 2 / 54,9 | b | KELLER / ALLGEMEIN_NEBENRAUM / 01 | ja | Ob das überhaupt ein Raum ist, ist offen: der Sweep 2026-09-08 las `ER-GESAMT` als Summenzeile | `OFFENE_FRAGEN.md:431-432` |
| `SCHRANKR.` | 3 / 20,8 | b | ABSTELLRAUM / WOHNUNG_PRIVAT / 00 | ja | Abkürzung von Schrankraum. Formal wäre das a, aber die Frage liegt bei Enis. | Frage 2 (`OFFENE_FRAGEN.md:713-717`, Owner Enis `:730`) |
| `NIEDERSP.`, `NIEDERSP.R.` | 2 / 21,0 | b | TECHNIK / ALLGEMEIN_NEBENRAUM / 01 | ja | Niederspannungsraum | – |
| `Müllplatz` | 1 / 4,0 | b | MUELLRAUM / ALLGEMEIN_NEBENRAUM / 01 | ja | Müll**platz** (Rennweg EG, 3,98 m²). Ob das ein Raum oder eine Außenfläche ist, ist offen. | – |
| `PODEST` | 2 / 21,0 | b | STIEGENHAUS / ALLGEMEIN_ERSCHLIESSUNG / 11 | ja | Treppenpodest. Ein Mollgasse-PODEST liegt laut Raster-Umriss außen. | Alias abgelehnt (`OFFENE_FRAGEN.md:434-436`) |
| `DOPPELPARKER …`, `DOPPELPARKERGRUBE`, `GARAGENRAMPE`, `Garageneinfahrt` | 6 / 581,3 | b | GARAGE / ALLGEMEIN_NEBENRAUM / 01 | ja | Garagenflächen | S-KG (`OFFENE_FRAGEN.md:1611`) |
| `INNENHOF`, `GULLY FLÄCHE`, `FLACHDACH BEGRÜNT`, `EIGENGARTEN TOP n`, `KLEINKINDERSPIELPLATZ`, `STAUDENBEET`, `VORPLATZ`, `Zugangsweg` | 11 / 766,8 | b | FREIFLAECHE / AUSSEN / 00 | nein | Außenflächen. **Wirkt auf Ausgänge**, siehe 4.1 B5 | `vorplatz`→VORRAUM abgelehnt (`OFFENE_FRAGEN.md:423-426`); „ins Freie" (`:255`) |
| `SR` | 24 / 104,5 | c | ABSTELLRAUM / WOHNUNG_PRIVAT / 00 | ja | Kürzel ohne Auflösung | Frage 3 (`OFFENE_FRAGEN.md:718-723`) |
| `Schl.` | 12 / 101,8 | c | SCHLAFZIMMER / WOHNUNG_PRIVAT / 00 (c) · SCHLEUSE / ALLGEMEIN_ERSCHLIESSUNG / 11 (c-schleuse, nur E2) | ja (SCHLEUSE) | Das Kürzel entscheidet `kuerzel_entscheid` je Stempelnummer. **Die c-Lesart widerspricht dem Entscheid E2-VF-11a**. | `OFFENE_FRAGEN.md:892-917`, `:970-997` |
| `Aufzug 1`, `Aufzug 2` | 16 / 47,5 | c | LIFT / KEIN_RAUM / 00 | ja | Alle 16 decken sich zu ≥ 50 % mit `lift_*` [ZENSUS:131] | Frage 3; Alias `aufzug` abgelehnt (`OFFENE_FRAGEN.md:437-439`) |
| `AUFZUG 8 PERS.` | 2 / 14,8 | c | LIFT / KEIN_RAUM / 00 | ja | **Auf Mollgasse EG liegt der Stempel auf dem Stiegenhaus**, siehe 4.2 C4 | Frage 3 |
| `TV Raum`, `Wohnbereich` | 2 / 75,4 | c | WOHNZIMMER / WOHNUNG_PRIVAT / 00 | ja | Die Diagnose schlägt WOHNZIMMER als Default vor (S6b, F15), zur Bestätigung | Diagnose `34b5dd0` Z. 1196 |
| `DBA Raum` | 1 / 6,1 | c | TECHNIK / ALLGEMEIN_NEBENRAUM / 01 | ja | Druckbelüftungsanlage, Lesart | – |
| `BÜRO` | 1 / 8,8 | c | ZIMMER / WOHNUNG_PRIVAT / 00 | ja | Büro in einer Wohnung (Tür zu TOP 18+19) oder Nichtwohnen? | – |
| `MEDIENRAUM` | 1 / 5,9 | c | TECHNIK / ALLGEMEIN_NEBENRAUM / 01 | ja | Medien-Versorgung (Tür zum Stiegenhaus) oder Wohnraum? | – |
| `Multif.r.` | 1 / 10,4 | c | ZIMMER / WOHNUNG_PRIVAT / 00 | ja | Multifunktionsraum; schwächste Lesart | – |
| `TOP n` (20 Varianten) | 22 / 572,8 | d | – | – | Wohnungs-Sammelstempel. Stempel-m² passt bei 0 von 22 [ZENSUS:115]. | – |
| `DACHGESCHOSS`, `ERDGESCHOSS` | 2 / 44,7 | d | – | – | Geschossbezeichnung | – |
| `BRE ABLUFT GARAGE`, `LUFTRAUM GARAGE` (Z) | 2 / 16,3 | d | – | – | Anmerkung, kein Raumstempel [ZENSUS:195-197] | – |
| GANG/VORRAUM ohne Klasse | 47 / 351,7 | K | – | – | Wohnungsklasse, siehe 1.4 | – |

### 2.3 Umlaut-Toleranz

**Was die Rennweg-Diagnose vorschlägt.** Die Diagnose liegt als
`docs/DIAGNOSE_RENNWEG_RAUMERKENNUNG.md` in Commit `34b5dd0` vor, nur auf Branch
`selman/diagnose-rennweg` und `origin/selman/diagnose-rennweg`.

- Ursache **U15** (Z. 47, Abschnitt Z. 859-885): Stempel ohne Kanon-Treffer bleiben
  untypisiert.
- Fix-Vorschlag **S6a** `raumtyp-schreibvarianten` (Z. 865-881, Slice-Tabelle Z. 1195):
  - zuerst NFC-Normalisierung
  - dann Umlaut-Varianten (ü → ue / u / weggelassen) für Schlüssel ab 4 Buchstaben
  - Test zuerst: „Wohnkche" → KÜCHE
- **S6b** (Synonyme „Wohnbereich", „TV Raum") hängt daran (Z. 1196) [KANON:84-100].

**Umgesetzt ist davon auf `aa05143` und auf `5f17378` nichts.** Belege:

- `git grep -i -E "unicodedata|casefold|schreibvariant|varianten\("` findet in `raumtyp.py`,
  `_port/models/room.py` und `stempel_anker.py` auf `aa05143` und auf `5f17378` jeweils **0**
  Treffer.
- `git merge-base --is-ancestor 34b5dd0 5f17378` liefert Exit 1. `34b5dd0` liegt nur auf
  `selman/diagnose-rennweg` und `origin/selman/diagnose-rennweg`.
- `git log 34b5dd0..5f17378 -- raumtyp.py room.py` zeigt nur `5f17378`, also den
  „Vorr."-Eintrag.
- `raumtyp_flags('Wohnkche')` = `None` auf `5f17378` (Befehlsausgabe).
- Auf `aa05143` bestätigt [KANON:102-107] denselben Stand.

**Der einzige Datenfall gehört zu b, nicht zu a.**

- Im Korpus kommt `Wohnkche` 1-mal in 298 Stempelnamen vor. In 76 DXF trifft
  `[A-Za-zÄÖÜäöüß]{3,}(kche|kuche|kueche)` nur `Wohnkche` [KANON:90-91].
- Eine Umlaut-Toleranz hätte heute also genau einen Anwendungsfall.
- Ob dieser Raum als Aufenthaltsraum gilt, ist der offene WOHNKÜCHE-Punkt an Enis
  (`wohnungsklasse.py:105-106`: „nicht selbst einführen"). Der Kanon-Pin
  `tests/raumerkennung/test_wohnungsklasse.py:2461` und die Gate-Referenz
  `tests/gate/gate_referenz.py:24-25` erwarten `raum_10` untypisiert.

**Wirkung.** S6a (KÜCHE) und b (WOHNKÜCHE in AUFENTHALTSRAUM) wirken auf Rennweg OG1 gleich:

- `raum_12` VORRAUM 10,94 m² wird bestätigt privat, Flags **11 → 00**, Notlicht fällt weg.
- Die Wohnungen gehen 3 → 1.
- Der Gate-Abnahmewert `rest_2` fällt 4 → 2.

Belege: b-Lauf [WIRKUNG:1392-1406]; in-memory-Gegenprobe KÜCHE (`docs/GATE_TUERSTAPEL.md:1287-1290`).

**Deshalb nimmt Selman die Umlaut-Toleranz nicht als Gruppe a mit.**

---

## 3. Teil 3 — Wirkung je Gruppe

**b und c sind Simulationen mit angenommenen Lesarten, keine Entscheidungen.**

- Technik: ein Wrapper um `raumtyp_flags` greift nur, wenn `aa05143` `None` liefert, und nur
  für die gelisteten Texte.
- Neue Labels bekommen eine Klasse in `nutzungsklasse._MAP`. Für b ist WOHNKÜCHE in
  `AUFENTHALTSRAUM` aufgenommen [WIRKUNG:174].
- Die Klassen in b sind ANNAHMEN [WIRKUNG:221].
- Eine echte, token-exakte Umsetzung hätte den Kollateral aus 3.8.

### 3.1 Kopf-Tabelle (Summe je Gruppe gegen Basis 0)

Übernommen aus [WIRKUNG:116-124].

**Spalten:**

- „Räume→Typ": Räume, die von UNBEKANNT oder UNBESTIMMT zu einem Typ wechseln.
- „Flächenleuchte": das Prädikat aus `platzierung/flaechen_strategy.py:162-167`. Die
  Flächenleuchte entfällt genau bei Klasse WOHNUNG_PRIVAT und Flags 00.

| Gruppe | Pläne | Räume→Typ | m² | Flag 00→11 (n / m²) | Flag 11→00 (n / m²) | Flags sonst (n) | Wohnungen Δ (Einraum) | Typ-/Klassenwechsel | Flächenleuchte − · + (n / m²) | Geometrie neu/entf./ΔF≥0,5 | Türrollen (+neu/−weg) | Ausgänge +/− |
|---|---:|---:|---:|---:|---:|---:|---|---:|---|---|---|---|
| **a** vs 0 | 8 | 35 (davon 34 Klasse offen) | 190,49 | 47 / 274,58 | 0 / 0,00 | 0 | 218→150 (-68; 112→35) | 15 | 1 / 3,60 · 13 / 87,69 | 3/0/1 | 140 (+9/−2; Seiten 3) | +0/−0 |
| **a+n** vs 0 | 8 | 37 (davon 34 Klasse offen) | 198,93 | 46 / 295,28 | 3 / 10,40 | 0 | 218→155 (-63; 112→35) | 19 | 4 / 14,00 · 12 / 108,39 | 3/0/1 | 150 (+9/−2; Seiten 3) | +0/−0 |
| **n** vs 0 | 2 | 0 | 0,00 | 0 / 0,00 | 0 / 0,00 | 0 | 65→65 (+0; 37→37) | 0 | 0 / 0,00 · 0 / 0,00 | 0/0/0 | 0 (+0/−0; Seiten 0) | +0/−0 |
| **b** vs 0 | 11 | 51 | 1912,43 | 2 / 21,04 | 5 / 88,10 | 27 | 119→119 (+0; 62→60) | 5 | 10 / 124,16 · 0 / 0,00 | 0/0/0 | 29 (+0/−0; Seiten 0) | +7/−0 |
| **c** vs 0 | 19 | 60 | 375,29 | 0 / 0,00 | 5 / 86,14 | 2 | 364→372 (+8; 194→197) | 11 | 44 / 355,71 · 0 / 0,00 | 5/20/1 | 44 (+0/−3; Seiten 0) | +0/−0 |
| **c-schleuse** vs 0 | 1 | 5 | 17,79 | 1 / 3,73 | 0 / 0,00 | 0 | 27→29 (+2; 13→15) | 1 | 2 / 8,12 · 0 / 0,00 | 1/2/0 | 2 (+0/−0; Seiten 0) | +1/−0 |
| **a+n** vs a | 8 | 4 | 18,92 | 1 / 31,18 | 5 / 20,88 | 0 | 150→155 (+5; 35→35) | 6 | 5 / 20,88 · 1 / 31,18 | 0/0/0 | 10 (+0/−0; Seiten 0) | +0/−0 |

### 3.2 Magenta vorher / nachher je Szenario

Eigene Zählung; unbestimmt = GANG oder VORRAUM ohne Klasse. Szenario 0 = Zensus auf 21 von 21
Plänen [MAGENTA].

| Szenario | Pläne | magenta 0 (n / m²) | magenta Szenario (n / m²) | Δ |
|---|---:|---|---|---|
| a | 8 (Muthgasse E2–E9) | 123 / 739,75 | **135 / 823,82** | **+12 / +84,07** |
| a+n | 8 | 123 / 739,75 | 131 / 804,90 | +8 / +65,15 |
| b | 11 | 123 / 2983,72 | 72 / 1071,30 | −51 / −1912,42 |
| c | 19 | 237 / 3704,97 | 180 / 3343,47 | −57 / −361,50 |
| c-schleuse | 1 (Muthgasse E2) | 11 / 69,72 | 6 / 51,94 | −5 / −17,78 |

**a macht die Darstellung magenta-reicher, nicht ärmer.** Das ergibt sich so:

- 34 der 35 typisierten Vorr.-Räume bleiben VORRAUM mit offener Klasse, also K und magenta.
- 13 bisher typisierte Räume (BAD, WC, AR, ZIMMER) werden zu VORRAUM mit offener Klasse und
  damit neu magenta.
- Nur E2 `raum_70` (3,60 m²) wird bestätigt privat.
- Rechnung: −1 + 13 = +12 [WIRKUNG:273-371], [MAGENTA].

**c:** 60 Räume bekommen einen Typ, die magenta-Zahl sinkt aber nur um 57. Grund: Auf
Mollgasse EG verlieren `raum_14` (VORRAUM), `raum_39` und `raum_56` (GANG) ihre Klasse
ALLGEMEIN_ERSCHLIESSUNG [WIRKUNG:1525-1529].

### 3.3 a — „Vorr." wie gebaut (Muthgasse E2–E9)

Kennzahlen [WIRKUNG:19-29]:

- 35 Räume UNBEKANNT → VORRAUM (190,49 m²). Davon bleiben 34 mit offener Klasse, nur E2
  `raum_70` wird bestätigt privat.
- 15 bisher typisierte Räume wechseln:
  - 13× BAD / WC / AR / ZIMMER → VORRAUM
  - 1× E2 AR → VORRAUM privat
  - 1× E4 KÜCHE → ZIMMER durch geänderte Flutung
- Wohnungen 218 → 150, Einraum-Wohnungen 112 → 35.
- 140 Türrollen ändern sich. 0 Ausgänge ändern sich.
- Flächenleuchte: −1 (3,60 m²), +13 (87,69 m²).
- Flags 11 → 00: 0.

**Flags 00 → 11: 47 Räume, 274,58 m²** [FLAGS]:

| Plan | Räume (m²) |
|---|---|
| E2 | `raum_2` 4,18 · `raum_42` 6,55 · `raum_48` 11,91 · `raum_57` 13,10 · `raum_59` 10,92 · `raum_80` 4,73 |
| E3 | `raum_22` 5,06 · `raum_64` 4,18 · `raum_83` 3,93 · `raum_84` 13,10 · `raum_86` 4,73 · `raum_87` 3,62 · `raum_89` 3,86 · `raum_92` 7,06 · `raum_99` 3,60 · `raum_102` 11,55 |
| E4 | `raum_58` 12,90 · `raum_60` 4,73 · `raum_64` 5,06 · `raum_65` 3,86 · `raum_80` 13,10 · `raum_98` 7,06 · `raum_99` 3,60 · `raum_101` 3,62 · `raum_102` 11,55 |
| E5 | `raum_58` 3,80 · `raum_61` 3,98 · `raum_89` 7,00 · `raum_91` 3,65 · `raum_95` 3,56 · `raum_99` 5,63 |
| E6 | `raum_77` 3,98 · `raum_78` 3,80 · `raum_83` 5,63 · `raum_86` 3,68 · `raum_95` 3,65 · `raum_101` 7,00 · `raum_108` 3,56 |
| E7 | `raum_37` 3,98 · `raum_66` 3,80 · `raum_75` 5,63 · `raum_82` 3,68 |
| E8 | `raum_41` 3,98 · `raum_44` 3,80 · `raum_76` 5,63 · `raum_83` 3,88 |
| E9 | `raum_38` 3,72 |

Raum für Raum mit Typ, Klasse und Wohnung: [WIRKUNG:267-371].

### 3.4 a+n — „Vorr." plus Namenswahl „nächster statt oberster Text"

Gegenüber a ändern sich 10 Räume [WIRKUNG:34-38]:

- die 2 Bäder (E2 `raum_42` 6,55, E3 `raum_83` 3,93) werden wieder BAD
- E2 `raum_76` BAD 3,61 → VORRAUM privat
- E5 `raum_82` AR → WC; E5 `raum_86` GANG 1,96 → WC privat
- E6 `raum_65` Vorraum 2,25 → AR
- E7 `raum_8` Vorraum 6,19 → BAD
- E8 `raum_25` WC 31,18 m² (F00) → GANG ALLGEMEIN (F11); E8 `raum_61` BAD → AR
- E9 `raum_11` BAD → WC

Flag-Wechsel a+n gegen a [FLAGS]:

- 11 → 00: E2 `raum_42` 6,55 · E3 `raum_83` 3,93 · E5 `raum_86` 1,96 · E6 `raum_65` 2,25 ·
  E7 `raum_8` 6,19 (5 Räume, 20,88 m²)
- 00 → 11: E8 `raum_25` 31,18

Wohnungen 150 → 155. Nur n allein (E2/E3): 0 Änderungen an Räumen, Flags, Türen und Ausgängen
[WIRKUNG:39-42].

### 3.5 b — Wörterbuch je Text (ANNAHME)

**Überblick** [WIRKUNG:1190-1432], [FLAGS]:

- 51 Räume bekommen einen Typ, zusammen 1912,43 m². Davon lassen sich 48 einem Text
  zuordnen, 3 hängen indirekt am Plan-Kontext [PROTEXT].
- Flags 00 → 11: Mollgasse 4.OG `raum_15` 5,79 · EG `raum_60` 15,25 (beide PODEST →
  STIEGENHAUS).
- **Flags 11 → 00: Mollgasse EG `raum_2` 21,17 · `raum_4` 19,46 · `raum_9` 28,75 · `raum_57` 7,78;
  Rennweg OG1 `raum_12` 10,94** (5 Räume, 88,10 m²).
  - `raum_2` und `raum_4` wechseln über die Stempel EIGENGARTEN TOP 2/3, `raum_9` über
    VORPLATZ: bisher geometrischer GANG (Erschließung), neu AUSSEN.
  - `raum_57` wird VORRAUM privat; das hängt am Plan-Kontext, nicht an einem Text.
  - `raum_12` hängt an `Wohnkche`, dem einzigen geänderten Text in OG1.
- Flächenleuchte −10 (124,16 m²), jeweils Anzahl / m²:

  | Text / Raum | n / m² |
  |---|---|
  | `Wohnkche` | 1 / 73,06 |
  | `SCHRANKR.` | 3 / 20,81 |
  | `WR-H` | 2 / 7,31 |
  | `WR-D` | 1 / 2,77 |
  | `Dusche-H` | 1 / 1,49 |
  | indirekt: Rennweg OG1 `raum_12` | 10,94 |
  | indirekt: Mollgasse EG `raum_57` | 7,78 |

- **Ausgänge +7:**
  - Mollgasse EG: 6× `final_exit` über AUSSEN-Freiflächen (`tuer_70`, `durchgang_2/3/4/8/10`);
    `tuer_60` verliert dabei `hauseingang`.
  - Mollgasse 4.OG: 1× `stair_exit` über PODEST.
- **Wohnungen:**
  - Rennweg OG1: 3 → 1
  - Rennweg UG: 4 → 6 (Personalräume mit Klasse PRIVAT bilden „Wohnungen"; ein Artefakt der
    Annahme SANITAER)
  - Muthgasse E2: Einraum 13 → 12

**Je Text: Räume, die direkt den Typ bekommen** [PROTEXT]:

| Text | Räume / m² | Pläne / Räume | Flächenleuchte − |
|---|---|---|---|
| `ER nn` | 13 / 199,28 | Mollgasse 1.KG `raum_7…13`, 2.KG `raum_8/9/10/14/15/18` | 0 |
| `ER-GESAMT` | 1 / 32,23 | Mollgasse 2.KG `raum_21` | 0 |
| `DOPPELPARKER 2072i-205` | 2 / 156,98 | Mollgasse 2.KG `raum_16`, `raum_17` | 0 |
| `DOPPELPARKERGRUBE` | 1 / 359,99 | Mollgasse 2.KG `raum_11` | 0 |
| `GARAGENRAMPE` | 2 / 50,25 | Mollgasse 1.KG `raum_16`, EG `raum_62` | 0 |
| `Garageneinfahrt` | 1 / 14,06 | Rennweg EG `raum_19` | 0 |
| `GESCHÄFTLOKAL` / `Geschäftslokal 1` | 2 / 140,14 | Rennweg EG `raum_12`, `raum_10` | 0 |
| `Müllplatz` | 1 / 3,98 | Rennweg EG `raum_9` | 0 |
| `NIEDERSP.` / `NIEDERSP.R.` | 2 / 20,98 | Mollgasse 2.KG `raum_3`, 1.KG `raum_3` | 0 |
| `INNENHOF` | 4 / 286,72 | Mollgasse 1.KG `raum_2`, `raum_4`; 2.KG `raum_19`, `raum_20` | 0 |
| `GULLY FLÄCHE` | 1 / 164,99 | Mollgasse 1.KG `raum_15` | 0 |
| `FLACHDACH BEGRÜNT` | 1 / 136,91 | Mollgasse 4.OG `raum_1` | 0 |
| `EIGENGARTEN TOP n` | 1 / 91,77 (+2 Typwechsel GANG → AUSSEN 40,63) | Mollgasse EG `raum_8`; `raum_2`, `raum_4` | 0 |
| `KLEINKINDERSPIELPLATZ` | 1 / 60,62 | Mollgasse EG `raum_5` | 0 |
| `STAUDENBEET` | 1 / 11,43 | Mollgasse EG `raum_1` | 0 |
| `VORPLATZ` | 1 / 8,92 (+1 Typwechsel GANG → AUSSEN 28,75) | Mollgasse EG `raum_6`; `raum_9` | 0 |
| `Zugangsweg` | 1 / 5,50 | Rennweg EG `raum_18` | 0 |
| `PODEST` | 2 / 21,04 | Mollgasse 4.OG `raum_15`, EG `raum_60` | 0 (00 → 11) |
| `SCHRANKR.` | 3 / 20,81 | Mollgasse 3.OG `raum_41`, `raum_60`; Muthgasse E2 `raum_61` | 3 / 20,81 |
| `Wohnkche` | 1 / 73,06 | Rennweg OG1 `raum_10` | 1 / 73,06 |
| `Umkleide-D` / `WR-H /Umkleide` | 2 / 10,59 | Rennweg UG `raum_4`, `raum_8` | 0 |
| `WR-H` / `WR-D` | 3 / 10,08 | Rennweg UG `raum_13`, `raum_14`, `raum_2` | 3 / 10,08 |
| `Dusche-H` | 1 / 1,49 | Rennweg UG `raum_9` | 1 / 1,49 |

**Indirekt**, nicht einem Text zuordenbar [PROTEXT]:

- Mollgasse EG:
  - `raum_3` UNBEKANNT → FREIFLAECHE (13,93)
  - `raum_23` VORRAUM und `raum_55` GANG bekommen die Klasse ALLGEMEIN_ERSCHLIESSUNG
  - `raum_57` VORRAUM ALLGEMEIN → privat (11 → 00)
- Rennweg UG: `raum_6` VR Personal WOHNUNG_PRIVAT → ALLGEMEIN_ERSCHLIESSUNG (F11 bleibt)
- Rennweg OG1: `raum_12` 11 → 00

Nicht getroffen: Mollgasse 2.KG `rest_6` mit `ER 09+10`, `ER 11`, `ER 12`, `ER-GESAMT` (V2).
Der Rest-Raum liest keine Stempel [ZNACH], [ZENSUS:26-27].

### 3.6 c — Lesarten (je Text eine)

**Überblick** [WIRKUNG:55-67, :1434-1813], [FLAGS], [PROTEXT]:

- 60 Räume bekommen einen Typ, zusammen 375,29 m².
- **Flächenleuchte −44 (355,71 m²).**
- Flags 11 → 00:
  - **Mollgasse EG `raum_13` 31,39** (STIEGENHAUS → LIFT, auf dem Stiegenhaus liegt der Stempel
    `AUFZUG 8 PERS.`)
  - **Muthgasse E2 `raum_65` 13,04** (SCHLEUSE → SCHLAFZIMMER)
  - E2 `raum_68` GANG 24,64 → Klasse WOHNUNG_PRIVAT. In c-schleuse bleibt der Raum unverändert,
    die Ursache ist also die Schl.-Lesart.
  - Mollgasse 3.OG `raum_55` VORRAUM 12,23 und `raum_56` GANG 4,84. Im selben Lauf wurden dort
    BÜRO → ZIMMER und AUFZUG 8 PERS. → LIFT gesetzt; die Ursache ist nicht getrennt gemessen.
- Ausgänge +0. 3 Türen entfallen: Mollgasse EG `durchgang_19/20/21` an `raum_13`.
- 19 `lift_*` entfallen (Mollgasse 3, Muthgasse 16), weil der Stempelraum jetzt LIFT ist
  (`lift_erkennung.py:183`). Flags und Klasse sind gleich (KEIN_RAUM, 00). Auf E9 zerfällt
  `raum_57` LIFT 29,59 in 3 LIFT + 1 ABSTELLRAUM.

**Je Text** [PROTEXT]:

| Text | Räume→Typ / m² | Typwechsel bisher typisierter Räume | Flächenleuchte − (n / m²) |
|---|---|---|---|
| `SR` | 24 / 104,54 | **5 fremde Stempel gekippt** (oberster statt nächster Text): E2 `raum_53` BAD 5,17 → AR; E4 `raum_85` ZIMMER 17,22 → AR, `raum_87` ZIMMER 3,69 → AR; E7 `raum_73` WC 4,27 → AR, `raum_81` WC 1,96 → AR | 24 / 104,54 |
| `Schl.` | 12 / 101,83 (E2 `raum_67` 3,73; E3–E8 je 13,03–13,04 bzw. 3,73; E9 `raum_36` 4,98) | E2 `raum_65` **SCHLEUSE → SCHLAFZIMMER** | 13 / 114,87 |
| `Aufzug 1` / `Aufzug 2` | 16 / 47,52 | – (Duplikate zu `lift_*`) | 0 |
| `AUFZUG 8 PERS.` | 2 / 14,76 (Mollgasse 3.OG `raum_35`, 4.OG `raum_43`) | Mollgasse EG `raum_13` **STIEGENHAUS 28,08 → LIFT 31,39** | 0 |
| `TV Raum` | 1 / 15,91 (Rennweg DG1 `raum_7`) | – | 1 / 15,91 |
| `Wohnbereich` | 1 / 59,53 (Rennweg OG2 `raum_2`) | – | 1 / 59,53 |
| `DBA Raum` | 1 / 6,11 (Rennweg UG `raum_17`) | – | 0 |
| `BÜRO` | 1 / 8,79 (Mollgasse 3.OG `raum_58`) | – | 1 / 8,79 |
| `MEDIENRAUM` | 1 / 5,94 (Mollgasse 2.KG `raum_12`) | – | 0 |
| `Multif.r.` | 1 / 10,36 (Muthgasse E7 `raum_67`) | – | 1 / 10,36 |
| indirekt | – | Mollgasse EG `raum_14`, `raum_39`, `raum_56` verlieren die Klasse; E2 `raum_68` → privat | 3 / 41,71 (3.OG `raum_55`, `raum_56`; E2 `raum_68`) |

### 3.7 c-schleuse — `Schl.` als SCHLEUSE (nur E2)

- E2 `raum_67` (3,73 m², E2-VF-11b) → SCHLEUSE, Flags 00 → 11, `stair_exit` +1.
- `raum_65` bleibt SCHLEUSE.
- Flächenleuchte −2 (8,12 m²), nur durch SR.
- Wohnungen 27 → 29.

Quellen: [WIRKUNG:68-69, :1815-1847], [PROTEXT].

### 3.8 Kollateral einer token-exakten Umsetzung (nur Scan)

Ein echter `_EXTRA_DIRECT`-Eintrag je Token träfe zusätzlich [WIRKUNG:246-255]:

- **b:** 220 verschiedene Texte (222 Plan-Vorkommen), z. B. `FUND UK NACHBAR = … ü. WR.NULL`,
  `7x ER`, `GEFÄLLE 13% GARAGENRAMPE`. Als Stempel landen davon 11:
  - 8× `Podest n.OG/m.OG` auf Muthgasse → STIEGENHAUS (je 5,29 m²)
  - `9x ER` → KELLER (51,00 m²)
  - `FLACHDACH BEKIEST` und `FLACHDACH` → FREIFLAECHE
- **c:** 16 verschiedene Texte (46 Vorkommen). Als Stempel landen 6: auf Muthgasse E2–E6 und E9
  kippt der `Schl.`-Anker auf `WDB DBA` → TECHNIK. Das ist wieder die Regel „oberster Text".
- In Raum-Layer-Texten: 0. In Text-Layer-Texten: b 15, c 6 (nur im Fallback-Pfad).

**Folge:** b und c dürfen nicht als bloßes Token umgesetzt werden. `wr`, `er`, `podest`, `dba`
und `aufzug` treffen Anmerkungen.

### 3.9 Nicht gelaufene Pläne

Muthgasse DD, Rennweg DG2 und Rennweg OG3 sind in keinem Szenario gelaufen. Grund: Der Scan
beider Code-Stände fand dort keinen geänderten Text und keinen geänderten Stempel. DG2 und OG3
haben keinen Flächen-Anker, DD hat einen ohne Namenskandidaten [WIRKUNG:107], Prüfvermerk
[WIRKUNG:11-13].

---

## 4. Teil 4 — Vorlage für @EnisAMG

Selman entscheidet keine dieser Fragen selbst. Bestehende offene Fragen werden **referenziert,
nicht dupliziert**; neu sind nur die Zahlen aus Teil 3. Für jede Frage gilt eine vierte
Alternative: **untypisiert lassen**. Das ist der Status quo und fail-safe, weil ein Raum ohne
Klasse die Flächenleuchte behält.

Markierung **⚠** = die Lesart nimmt Notlicht oder ändert Ausgänge an einer Stelle, an der das
fachlich falsch sein kann.

### 4.1 Gruppe b — Bedeutung klar, Kanon-Festlegung offen

**B1 — GESCHÄFTSLOKAL.** Das ist die bestehende 3-Owner-Frage in `OFFENE_FRAGEN.md:443-448`.
Hier nur die Zahlen.

- Betroffen:
  - Rennweg EG `raum_12` `GESCHÄFTLOKAL` 111,03 m²
  - Rennweg EG `raum_10` `Geschäftslokal 1` 29,11 m²
  - Mollgasse EG 2 Stempel ohne Raum
- Vorschlag: Label GESCHAEFTSLOKAL, Klasse ALLGEMEIN_NEBENRAUM.
- Wirkung: Flags 00 → 01, Flächenleuchte unverändert.
- Alternative: eine eigene Nichtwohn-Klasse. Das ist eine Contract-Änderung (`raum_modell.py:22-25`,
  Approval aller 3 Owner).

**B2 — Wohnküche (`Wohnkche`, Rennweg OG1 `raum_10`, 73,06 m²).** Das ist der bestehende
Board-Punkt 2026-09-22 (`wohnungsklasse.py:105-106`), Einträge in `COORDINATION.md`
2026-09-26 und 2026-09-27.

- Frage: Gilt der Raum als Aufenthaltsraum?
- (i) als Schreibweise von Küche → KÜCHE. Das ist Diagnose S6a; die richtig geschriebene
  `Wohnküche` typt heute schon als KÜCHE.
- (ii) eigenes Label WOHNKÜCHE in `AUFENTHALTSRAUM` (simuliert).
- (i) und (ii) wirken gleich (2.3):
  - Flächenleuchte `raum_10` fällt weg.
  - **⚠ `raum_12` VORRAUM 10,94 m²: Flags 11 → 00.**
  - Wohnungen 3 → 1.
  - Gate-Abnahme `rest_2` 4 → 2 (`GATE_TUERSTAPEL.md:1287-1290`).
- Derselbe Fall auf OG2 `raum_2` `Wohnbereich` 59,53 m² steht unter C5.

**B3 — Personalbereich Rennweg UG. ⚠ Klasse.**

- Betroffen:
  - `Umkleide-D` `raum_4` 4,89, `WR-H /Umkleide` `raum_8` 5,70
  - `WR-H` `raum_13` 5,78 / `raum_14` 1,53, `WR-D` `raum_2` 2,77
  - `Dusche-H` `raum_9` 1,49
- Simuliert (ANNAHME):
  - UMKLEIDE / ALLGEMEIN_NEBENRAUM: Flags 00 → 01, Flächenleuchte bleibt.
  - SANITAER bzw. BAD / WOHNUNG_PRIVAT: **4 Flächenleuchten entfallen (11,57 m²)**
    - 3 durch SANITAER (10,08 m²)
    - 1 durch `Dusche-H` → BAD
  - Dazu 2 Schein-Wohnungen (4 → 6).
  - Mit ALLGEMEIN_NEBENRAUM für SANITAER entfielen die 3 nicht (nicht gerechnet)
    [WIRKUNG:90-94].
- Frage: Welche Nutzungsklasse haben Personal-Sanitärräume außerhalb von Wohnungen? Die Frage
  betrifft auch die **schon typisierten** `WC-D`, `WC-H`, `Beh.WC / WC-D` (WC / WOHNUNG_PRIVAT)
  und `VR Personal` (VORRAUM / WOHNUNG_PRIVAT) [KANON:138-150].
- `WR` ≠ Waschküche (1.5).

**B4 — Keller und Garage Mollgasse** (Paket S-KG, `OFFENE_FRAGEN.md:1611`).

- `ER nn` (13 Räume, 199,28 m²): KELLER oder ABSTELLRAUM? Der Port führt `einlagerungsraum` als
  ABSTELLRAUM (Klasse WOHNUNG_PRIVAT, Flächenleuchte würde entfallen). KELLER ist
  ALLGEMEIN_NEBENRAUM (Flächenleuchte bleibt).
- `ER-GESAMT` (`raum_21`, 32,23 m²): ist das ein Raum oder eine Summenzeile
  (`OFFENE_FRAGEN.md:431-432`)?
- GARAGE für `DOPPELPARKER …`, `DOPPELPARKERGRUBE`, `GARAGENRAMPE`, `Garageneinfahrt`
  (6 Räume, 581,28 m²):
  - Flags 00 → 01
  - 4 Türen werden `garagentor` (Mollgasse 2.KG `durchgang_5/13/16`, Rennweg EG `durchgang_15`)
- TECHNIK für `NIEDERSP.` / `NIEDERSP.R.` (20,98 m²).
- MUELLRAUM für `Müllplatz` (Rennweg EG, 3,98 m²): Raum oder Außenfläche?
- Wirkung auf Flächenleuchte und Ausgänge: 0.

**B5 — Freiflächen. ⚠ Ausgänge.**

- Betroffen: `INNENHOF`, `GULLY FLÄCHE`, `FLACHDACH BEGRÜNT`, `EIGENGARTEN TOP n`,
  `KLEINKINDERSPIELPLATZ`, `STAUDENBEET`, `VORPLATZ`, `Zugangsweg` (11 Räume, 766,8 m²; neues
  Label, simuliert als FREIFLAECHE / AUSSEN).
- Auf Mollgasse EG werden damit **3 bisher geometrisch erkannte GANG-Flächen AUSSEN**: `raum_2`
  21,17, `raum_4` 19,46, `raum_9` 28,75.
  - Flags 11 → 00
  - **6 neue `final_exit`**
  - `tuer_60` verliert `hauseingang`
- Frage: Label und Klasse für Freiflächen. Zählt der Übergang in eine Freifläche als Ausgang ins
  Freie? Siehe Owner-Regel „ins Freie" (`OFFENE_FRAGEN.md:255`) und „Gebäude schließt nicht"
  (`:195`).

**B6 — PODEST → STIEGENHAUS** (Alias abgelehnt, `OFFENE_FRAGEN.md:434-436`).

- Betroffen: Mollgasse 4.OG `raum_15` 5,79 und EG `raum_60` 15,25.
- Wirkung: Flags 00 → 11, +1 `stair_exit` (4.OG).
- Als Token würde es zusätzlich 8 Muthgasse-`Podest`-Stempel typisieren (3.8).
- Frage: Ist das Podest Teil des Stiegenhauses?

**B7 — `Schrankr.`** Das ist die bestehende Frage 2 (`OFFENE_FRAGEN.md:713-717`).

- Betroffen: Mollgasse 3.OG `raum_41` 8,68, `raum_60` 7,26; Muthgasse E2 `raum_61` 4,87.
- Wirkung als ABSTELLRAUM / PRIVAT: **Flächenleuchte −3 (20,81 m²)**.

### 4.2 Gruppe c — Lesart braucht Fachurteil

**C1 — `SR`** (bestehende Frage 3, `OFFENE_FRAGEN.md:718-723`).

- 24 Räume, 104,54 m², auf Mollgasse EG und Muthgasse E2–E9.
- Lesart ABSTELLRAUM / PRIVAT: **Flächenleuchte −24 (104,54 m²)**.
- **⚠ 5 fremde Stempel kippen** über die Regel „oberster Text" (3.6). Dazu kommt, dass auf E8/E9
  an der `Schl.`-Lage ein `SR` mit Parkett steht (`OFFENE_FRAGEN.md:959-960`).
- Frage: Was bedeutet SR in dieser Plan-Familie?

**C2 — `Schl.`** (entschieden nur für E2-VF-11a = SCHLEUSE, `OFFENE_FRAGEN.md:892-917`; offen für
E2-VF-11b, `:970-997`).

- **⚠ Als Token SCHLAFZIMMER überschriebe es den entschiedenen Fall**:
  - E2 `raum_65` SCHLEUSE → SCHLAFZIMMER, 11 → 00
  - GANG `raum_68` 24,64 wird privat
  - insgesamt 13 Räume, 114,87 m² ohne Flächenleuchte
- Lesart SCHLEUSE für `raum_67` (3,73 m²): 00 → 11, +1 `stair_exit`.
- Neu gezählt:
  - E3–E6 je 2 Vorkommen (≈ 13,03 und 3,73 m²)
  - E7 und E8 je 1 (13,03 m²)
  - E9 1 (4,98 m²)
- Frage: Gilt die E2-Entscheidung je Stempelnummer auch für E3–E9? `kuerzel_entscheid` löst nur
  mit Beleg **und** Register-Eintrag je Nummer.

**C3 — `Aufzug 1` / `Aufzug 2`** (Frage 3; Alias `aufzug` abgelehnt, `OFFENE_FRAGEN.md:437-439`).

- 16 Räume, 47,52 m². Alle sind Duplikate zu `lift_*`. Die Wirkung auf Notlicht ist 0.
- Vorschlag: nicht als Vokabel lösen. Die Duplikatprüfung in `lift_erkennung.py:183` ist
  Selmans Sache. Enis muss dazu nichts entscheiden, wenn LIFT als Lesart unstrittig ist.

**C4 — `AUFZUG 8 PERS.` ⚠**

- Mollgasse 3.OG `raum_35` 11,77 und 4.OG `raum_43` 2,99 werden LIFT.
- **Auf Mollgasse EG liegt der Stempel auf dem Stiegenhaus `raum_13`**: STIEGENHAUS 28,08 → LIFT
  31,39, Flags 11 → 00, 3 Durchgänge entfallen.
- Empfehlung: keine Vokabel. Es kann höchstens eine Stempelregel mit Flächenbedingung werden
  (Selman).
- Frage an Enis: Ist die Kabinenbeschriftung als Raumname je gewollt?

**C5 — `TV Raum` / `Wohnbereich`** (Diagnose S6b, Default WOHNZIMMER zur Bestätigung).

- Rennweg DG1 `raum_7` 15,91, OG2 `raum_2` 59,53.
- Lesart WOHNZIMMER: Flächenleuchte −2 (75,44 m²); OG2 Wohnungen 2 → 1.
- `raum_2` trennt die eingangslose Wohnung vom Eingang (`COORDINATION.md` 2026-09-27).
- Frage: WOHNZIMMER ja oder nein?

**C6 — `DBA Raum`** (Rennweg UG `raum_17`, 6,11).

- Lesart TECHNIK: Flags 00 → 01, Flächenleuchte bleibt.
- Als Token würde `dba` die `WDB DBA`-Texte treffen (3.8).

**C7 — `BÜRO`** (Mollgasse 3.OG `raum_58`, 8,79).

- Lesart ZIMMER: Flächenleuchte −1 (8,79).
- Im selben Lauf gehen `raum_55`/`raum_56` 11 → 00; die Ursache ist nicht getrennt.
- Frage: Ist das ein Wohnraum oder Nichtwohnen?

**C8 — `MEDIENRAUM`** (Mollgasse 2.KG `raum_12`, 5,94).

- Lesart TECHNIK: Flags 00 → 01.
- Frage: Ist das ein Versorgungsraum oder ein Aufenthaltsraum?

**C9 — `Multif.r.`** (Muthgasse E7 `raum_67`, 10,36).

- Lesart ZIMMER: Flächenleuchte −1 (10,36). Das ist die schwächste Lesart.

### 4.3 Nicht an Enis (Selman)

- **d**: `TOP n`-Sammelstempel (22 Räume, 572,8 m²), Geschossbezeichnungen (2 Räume, 44,7 m²),
  Anmerkungen in Z (2 Räume, 16,3 m²). Hier braucht es eine Zuordnungs- oder Stempelregel,
  kein Wörterbuch.
- **Z3 BAD / GANG** (3 Räume, 50,6 m²): Die Flutung bleibt unter 1 m², deshalb `kein_polygon`.
- **G** (28 Räume, 464,7 m²): Geometrie.
- **K** (47 Räume, 351,7 m²): Wohnungsklasse.
- **Namenswahl in `stempel_anker.py:218/:230-231`** (oberster statt nächster Text): Sie ist die
  Ursache der Fremd-Treffer in a, c und im Kollateral. Das ist ein eigener Slice (Teil 5,
  Option 3).

---

## 5. Teil 5 — Slice a „Vorr." (Entscheid OFFEN)

### 5.1 Commits

Branch `selman/fix-svok-schreibweise`, nicht gepusht:

| Commit | Inhalt |
|---|---|
| `bfad1ed` | `tests/raumerkennung/test_raumtyp.py` +16 Zeilen. `test_vorr_abkuerzung_ist_vorraum` mit `Vorr.` und `Vorr` → `('VORRAUM', True, True)`. `test_vorr_kein_bleed`: `Vorrat` und `Vorratsraum` bleiben `None`, `Vorraum` bleibt VORRAUM. |
| `5f17378` | `raumtyp.py` +5 Zeilen: `"vorr": RoomType.ENTRANCE_HALL` in `_EXTRA_LABELS` direkt nach `"vr"` (`:71`), mit Kommentar. |

**Rot vor dem Fix, grün danach.**

- Teilschranke des Bauers auf `bfad1ed`: 3 failed. Das sind die 2 neuen Vorr.-Tests und
  `tests/naht/test_soll_muthgasse.py::test_soll_plan_tuerbloecke_im_modell`.
- Auf `5f17378`: 1 failed (nur der Muthgasse-Türblock-Test, vorbestehend), 733 passed.
- Quelle: Logs `_tests_vorher.log` und `_tests_nachher.log`.

### 5.2 Direktwirkung (Text-Ebene, ezdxf, kein parse)

- Gescannt: 102 Pläne mit 325 762 Texten.
- Das Token `vorr` tragen **49 Texte, alle in Muthgasse**: E2 9, E3 9, E4 9, E5 6, E6 7, E7 4,
  E8 4, E9 1. Alle 49 ändern sich.
- Alle sind wörtlich `Vorr.`, MTEXT auf `A-AREA-IDEN`, jeder mit m²-Nachbar im Abstand
  ≤ 193 mm. Falschtreffer: 0.
- In den übrigen 94 Plänen kommt `vorr` 0-mal vor.

Quelle: [DIREKT:7-8, :14-21, :93-109].

### 5.3 STOPP-Befund auf Stempel-Ebene

`finde_stempel` ohne parse [DIREKT:114-158]:

- Stempel 840 → 881 (+41), VORRAUM-Stempel 35 → 87 (+52).
- 48 Stempel sind „eigene": der Vorr.-Text liegt 193–194 mm über diesem m²-Text. Das sind 39
  neue Stempel und 9 Korrekturen. Bei den Korrekturen hatte der Stempel vorher den Namen des
  Nachbarraums gegriffen (AR 3×, WC 3×, Bad 3×).
- **4 Stempel sind fremd, also Falschtreffer:**
  - 2 echte Bäder werden VORRAUM: E2 6,55 m², E3 3,93 m².
  - Am Wohnungs-Summenstempel `TÜR 8` (E2) entstehen 2 neue VORRAUM-Stempel: 54,35 m² und
    Loggia 6,47 m².

**Ursache ist die Namenswahl, nicht das Token.** `stempel_anker.py:218` sortiert die Nachbarn
nach `-y`. `:230-231` nimmt den ersten Kandidaten mit Typ, also den **obersten** Text statt des
nächsten. Erst der Eintrag `vorr` macht diese Regel hier wirksam.

**Im parse gemessen** [WIRKUNG:30-33]:

- Die 2 Bäder sind in a VORRAUM mit offener Klasse und F11.
- In a+n sind sie BAD / WOHNUNG_PRIVAT / F00, also wie in Stand 0.
- Die 2 Summentext-Stempel sind in a und in a+n `kein_polygon` und haben **0 Raumwirkung**.

### 5.4 Gate

Nachrechnung auf der vorhandenen Messung, ohne neuen parse:
`pruefe_gate(tests/gate/nullmessung_f15d03f.json, _arbeit/gate/messung_vok_5f17378.json)`
liefert **2 Verstöße**:

- `(3) M4.einraum steigt in DG2: 0 → 1`
- `(10) Barawitzka EG ABSTELLRAUM 1.98 m² ohne Verbindung: 0 Tür(en)`

Das sind dieselben zwei, die `docs/GATE_TUERSTAPEL.md:2248` für den sauberen Stand erwartet.
Weitere Messwerte:

- M17: 18 von 18 BESTANDEN.
- Referenz: 0 verneinte Verbindungen bestehen, 0 geforderte Übergänge fehlen.
- `-m gate`: 3 passed, 1 xfailed (`_gate_messung.log:776-794`, `_gate_pytest.log`).

Das ist **per Konstruktion unverändert**: Die Gate-Pläne (Rennweg 7 Geschosse + Barawitzka EG)
enthalten das Token `vorr` 0-mal [DIREKT:106-109]. Das Gate misst diesen Slice also nicht.

### 5.5 a gegen a+n

Siehe 3.3, 3.4 und die Kopf-Tabelle in 3.1. Szenario n ist die Namenswahl „nächster statt
oberster". Der Patch tauscht genau die Anweisung `stempel_anker.py:230-231`
[WIRKUNG:160-173].

- **n allein** ändert auf E2/E3 nichts.
- **Zusammen mit a** holt n die 2 Bäder zurück.
- **Zusätzlich** ändert n 7 Räume ohne Bezug zu Vorr. Darunter verlieren 3 Räume F11: E5
  `raum_86` GANG 1,96 → WC, E6 `raum_65` Vorraum 2,25 → AR, E7 `raum_8` Vorraum 6,19 → BAD.
  Die Richtigkeit dieser drei ist nur über die Regel belegt, nicht im Plan gesichtet
  [WIRKUNG:81].

### 5.6 Entscheidungsvorlage für den Owner

Nach [WIRKUNG:75-84], ergänzt um die Magenta-Zahl aus 3.2.

| Option | Was bleibt oder kommt | Preis | magenta Muthgasse E2–E9 |
|---|---|---|---|
| **1 behalten** (`5f17378`) | 35 Vorr.-Räume typisiert (34 mit offener Klasse, F11 fail-safe). 12 Räume, die bisher fremde WC-/AR-/BAD-/ZIMMER-Typen trugen, werden VORRAUM. Wohnungen 218 → 150, Einraum 112 → 35, Flächenleuchte +13. | 2 Bäder E2/E3 (10,48 m²) sind falsch VORRAUM (00 → 11, also fail-safe, keine Unterdeckung). Gate unverändert 2 Verstöße. | 123 → **135** |
| **2 revert** | Stand 0 | Alle Gewinne sind weg. 34 Vorr.-Räume bleiben UNBEKANNT, 12 Vorräume tragen weiter fremde Typen (PRIVAT F00, ohne Flächenleuchte). | 123 |
| **3 Namenswahl als eigener Slice** (a+n) | Wie Option 1; die 2 Bäder sind wieder BAD. Dazu E2 `raum_76` BAD → VORRAUM und 7 Änderungen ohne Bezug zu Vorr. | 3 Räume verlieren F11 (5.5). Braucht einen eigenen Test und einen Gate-Lauf. | 123 → 131 |

Hinweis: Option 3 lässt sich als „a behalten, n danach" schneiden, weil n allein keine Wirkung
hat [WIRKUNG:83-84].

**Magenta-Wirkung von Option 1: +12 statt weniger.** Das Label stimmt jetzt, aber die
Wohnungsklasse der Muthgasse-Vorräume bleibt offen. Siehe 1.4 und 3.2.

### 5.7 Testschranke

Volle Suite im Worktree `nb-wt/vokabular` auf `5f17378`. Parallel lief kein anderer Prozess.
Befehl: `.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider`

- Ergebnis: **`4 failed, 2101 passed, 11 skipped, 6 deselected, 14 xfailed, 3 warnings in
  1555.26s`**
- Rot sind:
  - `tests/naht/test_s7_wohnungsklasse.py::test_keine_leuchten_in_wohnung_privat`, Fälle
    `[pfad0-OG1]`, `[pfad1-OG2]`, `[pfad3-DG1]`
  - `tests/naht/test_soll_muthgasse.py::test_soll_plan_tuerbloecke_im_modell`
- Gegenprobe auf `aa05143` (Worktree `nb-wt/s5c`, sauber, nur diese Knoten): **dieselben 4
  failed** (`4 failed, 1 passed`). Alle vier waren also schon vorher rot, keiner kommt durch
  den Slice.
- Die Meldungen sind gleich:
  - OG1 2 Leuchten in `raum_8`
  - OG2 2 Leuchten in `raum_9`
  - DG1 1 Leuchte in `raum_3`
  - Muthgasse E2: „nur 30 von 72 Plan-Türblöcken"
- Einziger Unterschied: Der Muthgasse-Text nennt 119 statt 118 `tuer_*` im Modell. Das ist die
  bekannte Türwirkung von a auf E2 (3.1); der geprüfte Wert 30 ist gleich.
- Die vier sind als offene Punkte dokumentiert: `docs/GATE_TUERSTAPEL.md:2299-2300` („Rote
  Naht-Tests danach: 4, keiner S5c-eigen"). OG1 `raum_8`, OG2 `raum_9` und DG1 `raum_3` sind
  Board 1; die Muthgasse-Türblöcke sind der S5b-Rest.

### 5.8 Status

**OFFEN.** Der Owner entscheidet zwischen 1, 2 und 3. Der Slice ist nicht gepusht und nicht
gemergt.

`docs/OFFENE_FRAGEN.md:713-717` und `:730` führen `Vorr.` weiter als Frage an Enis. Das
passt die Doku erst nach dem Owner-Entscheid an; bis dahin steht der Board-Eintrag vom
2026-09-29 in `docs/COORDINATION.md`.
