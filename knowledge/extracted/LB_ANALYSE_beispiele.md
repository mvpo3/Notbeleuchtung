# LB-Analyse — reale Leistungsbeschreibungen → `LBVorgabe`-Contract-Groundwork

**Zweck:** Der 2. Engine-Input (Leistungsbeschreibung) trägt die **expliziten,
projektspezifischen** Auftraggeber-Vorgaben, die Norm-Defaults **übersteuern**
(CLAUDE.md-Hierarchie: `LB-explizit → Referenz-Praxis → EN-1838/ÖNorm → OVE-Verbote`).
Dieser Digest wertet 4 reale LBs aus und leitet daraus die vorgeschlagenen Felder des
noch fehlenden `LBVorgabe`-Contracts ab — Groundwork zur Ratifizierung mit Enis
(LB-Parsing = Enis' Lane; `LBVorgabe`-Contract = hauptengine/Leonis, 3-Owner, wie OIB).

**Quellen** (liegen unter `Leistungsbeschreibungen BSP/`, PDFs sind **gitignored** —
nur dieser Digest ist eingecheckt; Seiten-Refs für Audit):
| Datei | Typ | Notbeleuchtungs-Kern |
|-------|-----|----------------------|
| `mo-leistungsbeschreibung_Elektro_240718.pdf` | Prosa-LB (Elektro) | §5.1.23 Fluchtwegorientierungsbeleuchtung (S.37–39) |
| `20241209_E LV Fischa 46.pdf` | **Prosa-LB (Elektro)** — *nicht* LV mit Positionen | §2.10/2.11 LED-Sicherheitsbeleuchtung (S.37–38) |
| `250116_GU Leistungsbeschreibung.pdf` | GU-Rahmen | **keine technische Vorgabe** — nur Wartungs-Labels (S.15, S.115) + Verweis auf die Fischa-Elektro-LB (S.122) |
| `mo-Bau-_und_Ausstattungsbeschreibung…pdf` | Bau/Ausstattung | Fluchtweg-Türen; Bildlegende „Fluchtwegsleuchten im Stiegenhaus" (S.15, ohne Marke); „Batterie" = Sanitär (irrelevant) |

> **Korrektur 2026-08-30 (Enis, Gegenprüfung am Original).** Drei Punkte dieses
> Digests waren falsch und sind unten berichtigt:
> 1. **Fischa ist kein Positions-LV**, sondern Prosa mit Abschnittsnummern — wie
>    `mo-Elektro`. Beide brauchen dieselbe Parser-Klasse, nicht zwei.
> 2. **Fischa enthält KEINE Skalare.** `lux`/`lx` = 0 Treffer im ganzen Dokument,
>    ebenso „Umschaltzeit", „Betriebsdauer", „Feuerlöscher" und „7010". Die Werte
>    8 Std / < 0,5 s / 1 lx / 5 lx / EN ISO 7010 stammen **ausschließlich** aus
>    `mo-Elektro`. „lt. Vorschrift" in den Fischa-Spalten suggerierte eine Vorgabe,
>    die es nicht gibt — korrekt ist `None`, damit der Norm-Default greift.
> 3. **Die vier Dateien sind zwei Projekte à zwei Dokumente:** `250116_GU` +
>    `Fischa` (Schwadorf) und `mo-Bau` + `mo-Elektro` (Parkside). Die
>    Notbeleuchtungs-Vorgaben stehen immer im **Elektro**-Dokument.
>
> **Merksatz für den Parser:** *Fischa = Bereichslogik. mo-Elektro = Skalare.*

---

## Kernbefund — LB übersteuert Norm (der ganze Grund für Input 2)

**Gegensätzlicher SL-Umfang bei gleicher Bauaufgabe (Wohnbau):**

- **`mo-Elektro` §5.1.23:** Sicherheitsleuchten in **Stiegenhäusern, Gängen UND Garage**
  + Technik-/Lager-/Müllräume, Feuerlöscher/Hydrant (≥5 lx), Niveauänderungen,
  Außen-Notausgänge.
- **`Fischa` §2.10 (wörtlich):** „Für die Stiegenhäuser und die an die Stiegenhäuser
  anschließenden Gänge ist **KEINE** LED-Sicherheitsbeleuchtung herzustellen **(GK4)**."
  §2.11: SL **nur in der Garage**.

→ Eine reine Norm-Engine (Enis-Default: `STIEGENHAUS → sicherheitsleuchte`) würde für
**Fischa GK4 zu viel** platzieren. Nur die LB weiß, dass hier Stiegenhaus/Gänge
ausgenommen sind (Gebäudeklasse + Brandschutzkonzept). **Ohne LB-Input ist der Plan
für Fischa fachlich falsch.** Das ist der kanonische „LB-explizit übersteuert"-Fall.

**Cross-Link:** Fischa ist derselbe Gebäude-Stamm wie der Plan im
[[fischamender-durchstich-f2-bugs]]-Durchstich. Der RZ-only-Plan (Coverage-Audit,
PR #19) liegt für GK4 zufällig näher an der LB-Wahrheit als für ein GK5-Gebäude —
belegt aber genauso, dass die Leuchten-Art-Entscheidung NICHT aus Geometrie allein
fällt, sondern aus LB + Norm + Gebäudeklasse.

---

## Extrahierte LB-explizite Felder (was die LBs tatsächlich vorschreiben)

| Feld | `mo-Elektro` | `Fischa` | übersteuert Norm-Default |
|------|--------------|---------------|--------------------------|
| **System-Typ** | Gruppenbatterie | **WIDERSPRUCH**: §2.3/§2.11 Gruppenbatterie vs. §2.21 Fabrikatsliste „(Versorgt über Zentralbatterie)" (S.43) → Review, kein Wert | — (Norm sagt nur „getrennter SV-Kreis") |
| **Batterie-Standort** | UG Zählerraum, brandbeständige Einhausung | Technikraum | — |
| **Betriebsdauer** | **8 Std** (Akkus) | **kommt nicht vor** → `None` | EN 1838 `dauer_min` (60) → **480** |
| **Umschaltzeit** | **< 0,5 s** | **kommt nicht vor** → `None` | EN 1838 (≤ 0,5 s Rettungsweg-Vollwert / 5 s) |
| **Mindest-Lux Fluchtweg** | **1 lx**, 2,00 cm ü. FBOK | **kommt nicht vor** (`lux`/`lx` = 0 Treffer) → `None` | EN 1838 §4.2.1 (1 lx) — bestätigt |
| **Sonder-Lux** | Feuerlöscher/Hydrant **≥ 5 lx** | **kommt nicht vor** (`Feuerlöscher` = 0 Treffer) | EN 1838 §4.1 (5 lx an Sicherheitseinrichtungen) |
| **SL-Bereiche (inkl.)** | Stiegenhaus, Gänge, Garage, Technik, Lager/Müll, Niveauänderungen, Außen-Notausgang | **nur Garage** | Norm-Default Raumtyp-Regel |
| **SL-Bereiche (AUSGESCHLOSSEN)** | — | **Stiegenhaus + Gänge (GK4)** | **kippt** `STIEGENHAUS→SL`-Default |
| **RZ-Stellen** | Fluchttüren, Kreuzungen, Richtungsänderungen; 1-/2-seitig; Wand/Decke/Einbau | (Konzept) | deckt Enis-RZ-Regel + [[rz-tuer-regel]] |
| **Überwachung** | Einzelleuchtenüberwachung (Strommessung) + Adressschalter | Einzelleuchte + WEB-Prüfung (LAN) | — (Norm fordert nur Prüfbarkeit) |
| **Prüfeinrichtung** | automatisch, Ladung < 5 min, tägl. Umschalt-Test | WEB-basiert (Controller/LAN) | — |
| **Piktogramm-Norm** | ÖNORM EN ISO 7010 | **kommt nicht vor** (`7010` = 0 Treffer); genannt ist **ÖNORM Z 1000** | — (fixiert Symbol-Familie) |
| **Batterie-Bauart** | OGi-Blei, Gel, 10 J, ÖVE-EN IEC 62485-2 | — (das LiFePO4 aus §2.16 ist der **PV-Speicher**, nicht die SV-Anlage) | — |
| **Norm-Bezug** | ÖVE E8101, R12-2, EN 1838, EN IEC 62485-2, DIN 4102, EN ISO 7010 | ÖVE8101, R12-2, EN 1838, ÖNORM Z1000 | — |
| **Fabrikat** | **für SL/RZ nicht genannt** (Molto Luce ist die Allgemeinbeleuchtung) | **DIN-Sicherheitstechnik Concept-LED, IP65** (§2.21, S.42) | — |
| **Funktionserhalt** | E30 / 30 min (ÖNORM DIN 4102-12) | E30 (ÖNORM DIN 4102-12) | **kein Contract-Feld** — nur im `LbBericht` |

---

## Vorschlag `LBVorgabe`-Contract (zur Ratifizierung mit Enis)

Analog zum OIB-Slice: Pydantic in `hauptengine/contracts/lb_vorgabe.py`, `contract`/
`contract_version`, `None` = „in LB nicht spezifiziert" (dann greift Norm-Default).
**Kern:** jede Vorgabe trägt ihre Herkunft (`lb_quelle` = Datei + Seite/§) als
Audit-Trail — spiegelbildlich zu `norm_quelle`.

```
LBVorgabe:
  contract: Literal["LBVorgabe"]; contract_version: "1.0.0"
  projekt: str | None
  system_typ: Literal["einzelbatterie","gruppenbatterie","zentralbatterie"] | None
  betriebsdauer_min: int | None            # 8 Std → 480; übersteuert EN-1838-Default
  umschaltzeit_max_s: float | None
  mindest_lux_fluchtweg: float | None
  ueberwachung: Literal["einzelleuchte","zentral"] | None
  pruefung: Literal["automatisch","web","manuell"] | None
  piktogramm_norm: str | None              # "EN ISO 7010"
  fabrikat_rz: str | None; fabrikat_sl: str | None
  bereiche_inklusion: list[BereichsRegel]  # explizit MIT Sicherheitsbeleuchtung
  bereiche_exklusion: list[BereichsRegel]  # explizit OHNE (Fischa: Stiegenhaus/Gänge!)
  rz_stellen: list[str]                    # "fluchttuer","kreuzung","richtungsaenderung"
  sonder_lux: list[SonderLux]              # z.B. {ort:"feuerloescher", lux:5.0}
  norm_bezug: list[str]
  lb_quelle: str                           # Datei + §/Seite (Audit)

BereichsRegel:  raum_typ: str; sicherheitsbeleuchtung: bool; begruendung: str | None
SonderLux:      ort: str; min_lux: float
```

**Konsum bei Leonis (Platzierer):** vor der norm-getriebenen Leuchten-Art-Entscheidung
prüft der Platzierer `LBVorgabe.bereiche_exklusion` (Hard-Override: kein SL trotz
Norm-Default) bzw. `_inklusion`; `betriebsdauer_min`/`fabrikat` wandern in Katalog-Key
+ Audit. Fehlt die LB (kein 2. Input) → alles `None` → reines Norm-Verhalten (heute).

---

## Offene Fragen für Enis (LB-Parser) + Naht

1. **Bereichs-Vokabular:** `BereichsRegel.raum_typ` muss auf Selmans `raum_typ`-Enum
   mappen (STIEGENHAUS/GANG/GARAGE …) — sonst greift die Exklusion nicht (vgl.
   [[fischamender-durchstich-f2-bugs]] B3: untypisierte Räume).
2. **Gebäudeklasse-Begründung** (Fischa: „GK4") überschneidet sich mit dem
   OIB-`ProjektKontext.gebaeudeklasse` — LB-Exklusion vs OIB-Ableitung sauber trennen.
3. **Betriebsdauer-Einheit:** LB nennt „8 Std" → Contract in Minuten (480) normieren.
4. **LB-Parser-Reife:** Prosa-LB (`mo`) vs Positions-LV (`Fischa`) brauchen verschiedene
   Extraktion; Start: strukturierte Felder manuell/halbautomatisch, kein Full-NLP.
