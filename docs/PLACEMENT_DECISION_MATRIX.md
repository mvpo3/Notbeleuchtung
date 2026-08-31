# Placement-Decision-Matrix — Notbeleuchtung

> **Owner:** Enis (`normwissen`) · **Stand:** 2026-08-31 · **Für:** Track A (Leonis)
>
> **Single Source ist die YAML**, nicht dieses Dokument:
> `src/notbeleuchtung/normwissen/data/platzierung_regeln.yaml`.
> Abgefragt wird sie über `normwissen.PlatzierungsRegelwerk` — Track A parst kein YAML.
> Dieses Dokument erklärt die Matrix, den Gap-Stand und die Übergabe.

## Warum es sie gibt

Die Engine wusste bisher zwei Dinge:

| Datei | Antwortet auf |
|---|---|
| `data/en1838_grundwerte.yaml` | *Welche Zahlen gelten?* (Lux, Höhe, Dauer, z-Faktoren) |
| `data/raumtyp_regeln.yaml` | *Welche Anforderung hat ein Raumtyp?* |

Sie wusste **nicht**, welche **Situation** eine Leuchte auslöst und wohin sie gehört —
„jeder Notausgang", „jede Kreuzung", „nahe Treppen", „Erste-Hilfe-Stellen". Genau das
ist die Kernaussage von EN 1838 §4.1.2, und genau das fehlte maschinenlesbar.
`platzierung_regeln.yaml` schließt diese Lücke: **25 Regeln + 4 Hard Stops**.

Keine zweite Regelwelt: die Matrix trägt keine eigenen Zahlen, sie referenziert die
bestehenden über `*_ref`.

---

## 1. Gap-Report (Bestandsaufnahme vor diesem Slice)

| Regelfall | bereits vorhanden | Quelle | Engine-Support | fehlte |
|---|---|---|---|---|
| Lux Rettungsweg / Antipanik | ✅ | `en1838_grundwerte.yaml` | ✅ `deckung`, `flaechen_strategy` | — |
| Montagehöhe ≥ 2 m, Dauer ≥ 60 min | ✅ | `en1838_grundwerte.yaml` | ✅ | als **Hard Stop** markiert |
| Erkennungsweite l = z·h | ✅ | `en1838_grundwerte.yaml` + `_port_source/rz_coverage` | ✅ `deckung` | — |
| Raumtyp → Klassifikation | ✅ | `raumtyp_regeln.yaml` | ✅ | — |
| OIB-RL 2 Tabelle 6 | ✅ | `data/oib_rl2_tabelle6.yaml`, `normwissen/oib/` | ⛔ `ProviderBundle.oib` nicht verdrahtet | Naht zum Platzierer |
| LB-Vorgaben (Bereiche, Skalare, Sonder-Lux) | ✅ | `normwissen/lb/` + `lb_extraktion.yaml` | ✅ `lb_override` | — |
| **§4.1.2 hervorzuhebende Stellen** | 🟡 nur als Rohtext in `_port_source` | EN 1838 §4.1.2 | 🟡 nur Ausgang/Kreuzung | **maschinenlesbare Auslöser-Regeln** |
| **Feuerlöscher / Hydrant / Erste-Hilfe / Melder** | ⛔ | EN 1838 §4.1.2 | ⛔ | **Merkmal im `RaumModell`** |
| **Niveauänderung** | ⛔ | reale LB | ⛔ | Merkmal + Normbeleg |
| **Barrierefreies WC** (§4.3.8) | ⛔ | EN 1838 §4.3.8 | ⛔ | Merkmal „barrierefrei" |
| **Arbeitsplatz besonderer Gefährdung** (§4.4.1) | ⛔ | EN 1838 §4.4.1 | ⛔ | Gefährdungs-Merkmal |
| **Konflikt-/Prioritätslogik** | ⛔ | — | ⛔ | **Hierarchie maschinenlesbar** |
| **Review statt stiller Entscheidung** | 🟡 im LB-Parser | — | 🟡 | für Platzierung |
| Ground Truth Mollgasse | ⛔ | — | — | **existiert nicht** (s. Abschnitt 3) |

---

## 2. Die Matrix

Vollständige Felder je Regel in der YAML. Kompaktübersicht, sortiert nach Priorität
(0 schlägt alles):

| Regel-ID | Auslöser | Leuchte | Prio | Beleg | Decision-Source | Review | Engine |
|---|---|---|---|---|---|---|---|
| `RZ-11-FLUCHTWEG-UNKLAR` | Fluchtwegführung nicht bestimmbar | keine | 0 | AUSLEGUNG | hard_stop | ja | 🟡 |
| `SL-14-WIDERSPRUCH` | zwei Regeln fordern Unvereinbares | keine | 0 | AUSLEGUNG | hard_stop | ja | 🟡 |
| `RZ-01-NOTAUSGANG` | Tür ist Notausgang | rz | 1 | BELEGT | norm_default | — | ✅ |
| `RZ-02-AUSGANG-INS-FREIE` | `Ausgang.typ == final_exit` | rz | 1 | BELEGT | norm_default | — | ✅ |
| `RZ-07-AUSGANG-STIEGENHAUS` | `Ausgang.typ == stair_exit` | rz | 1 | AUSLEGUNG | referenz_praxis | — | 🟡 |
| `SL-01-FLUCHTWEG-MITTELLINIE` | Fluchtweg-Segment vorhanden | sicherheitsleuchte | 1 | BELEGT | norm_default | — | ✅ |
| `SL-02-TREPPE` | Treppe / STIEGENHAUS | sicherheitsleuchte | 1 | BELEGT | norm_default | — | ✅ |
| `RZ-03-RICHTUNGSAENDERUNG` | `reason ∈ {direction_change, corner}` | rz | 2 | BELEGT | norm_default | — | ✅ |
| `RZ-04-KREUZUNG` | Graph-Knoten Grad ≥ 3 | rz | 2 | BELEGT | norm_default | — | ✅ |
| `RZ-05-TREPPE` | Fluchtweg über Treppe | rz | 2 | BELEGT | norm_default | — | 🟡 |
| `SL-03-KREUZUNG` | Gang-Kreuzung | sicherheitsleuchte | 2 | BELEGT | norm_default | — | 🟡 |
| `SL-05-ERSTE-HILFE-STELLE` | Erste-Hilfe-Stelle | sicherheitsleuchte | 2 | BELEGT | norm_default | ja | ⛔ |
| `SL-06-FEUERLOESCHER` | Feuerlöscher-Standort | sicherheitsleuchte | 2 | BELEGT | norm_default | ja | ⛔ |
| `SL-07-WANDHYDRANT` | Wandhydrant | sicherheitsleuchte | 2 | AUSLEGUNG | norm_default | ja | ⛔ |
| `SL-08-BRANDMELDER` | Melde-/Brandbekämpfungseinrichtung | sicherheitsleuchte | 2 | BELEGT | norm_default | ja | ⛔ |
| `SL-09-ANTIPANIK-FLAECHE` | Raum mit Klassifikation `antipanik` | antipanik | 2 | BELEGT | norm_default | — | ✅ |
| `SL-10-BARRIEREFREIES-WC` | Toilette für Menschen mit Behinderung | antipanik | 2 | BELEGT | norm_default | ja | ⛔ |
| `SL-11-BESONDERE-GEFAEHRDUNG` | Arbeitsplatz besonderer Gefährdung | sicherheitsleuchte | 2 | BELEGT | norm_default | ja | ⛔ |
| `SL-12-GARAGE` | Raumtyp GARAGE | sicherheitsleuchte | 2 | LB | lb_explizit | — | ✅ |
| `RZ-06-NIVEAUAENDERUNG` | Niveausprung ohne Treppe | rz | 3 | LB | lb_explizit | ja | ⛔ |
| `SL-04-NIVEAUAENDERUNG` | Niveausprung | sicherheitsleuchte | 3 | LB | lb_explizit | ja | ⛔ |
| `SL-13-TECHNIK-LAGER-KELLER` | TECHNIK / LAGER / MUELLRAUM / KELLER | sicherheitsleuchte | 3 | LB | lb_explizit | — | ✅ |
| `RZ-09-SICHTACHSE-AUFFUELLEN` | Abstand > Erkennungsweite l = z·h | rz | 4 | BELEGT | norm_default | — | ✅ |
| `RZ-10-BEIDSEITIGE-RICHTUNG` | Wasserscheide zwischen zwei Ausgängen | rz | 4 | PRAXIS | referenz_praxis | — | ✅ |
| `RZ-08-TUER-AM-FLUCHTWEG` | Tür am Fluchtweg, kein Notausgang | **keine** | 9 | AUSLEGUNG | norm_default | — | ✅ |

✅ umsetzbar (17) · 🟡 teilweise (5) · ⛔ Contract-Lücke (8)

### Hard Stops — unübersteuerbar, schlagen auch LB-explizit

| ID | Regel |
|---|---|
| `HS-01-MONTAGEHOEHE` | ≥ 2000 mm über Boden (§4.1.1). Darunter ist **Fehler**, nicht Warnung. |
| `HS-02-BETRIEBSDAUER` | ≥ 60 min (§4.2.5/§4.3.5/§5.4.5). Eine LB darunter → Review, nicht übernehmen. |
| `HS-03-LB-EXKLUSION-GEGEN-PFLICHT` | LB schließt aus, was der OIB-Befund fordert → **Konflikt → Review**. Ein *fehlender* OIB-Befund ist kein Freibrief. |
| `HS-04-KEINE-GERATENE-RICHTUNG` | RZ ohne bestimmbare Fluchtrichtung wird nicht gesetzt. Ein falsch weisender Pfeil ist schlechter als kein Pfeil. |

### Prioritätslogik

```
hard_stop (9)  >  lb_explizit (4)  >  referenz_praxis (3)  >  norm_default (2)
```

Bei gleicher Decision-Source entscheidet `prioritaet` (kleiner gewinnt). Bleibt es
gleichauf, liefert `PlatzierungsRegelwerk.gewinner()` bewusst **`None`** — das heißt
Review, nicht „irgendeine nehmen".

### Zwei Regeln erzeugen absichtlich nichts

`RZ-08` (Tür am Fluchtweg) und `RZ-11`/`SL-14` (unklar/widersprüchlich) sind
Abgrenzungsregeln. Ohne `RZ-08` würde eine Engine plausibel, aber falsch **jede**
Wohnungstür bestücken — die Coverage-Reihenfolge nennt ausdrücklich Türen ins Freie
und Stiegenhaustüren, nicht alle Türen.

---

## 3. Ground Truth Mollgasse — Befund zuerst

**Es gibt keinen professionell gezeichneten Mollgasse-Notbeleuchtungsplan im Repo.**

- `Projekte/Mollgasse/*.dxf` = leere Architekturpläne, **0 Notbeleuchtungs-Layer**
- `Projekte/Mollgasse Notbeleuchtung/` = ein 5,8-kB-Bildschirmausschnitt ohne
  verwertbare Symbolik
- `DIN-Notbeleuchtungspläne(Beispiele)/din_support_ReMi_Barawitzkagasse…dxf` (PR #66)
  enthält Notruf**sprech**stellen, **keine** Notbeleuchtung

„Welche Leuchten wurden tatsächlich gesetzt, in welcher Orientierung" ist aus dem
Repo damit **nicht beantwortbar**. Das wird hier nicht erfunden.

Belegbar ist die **Auslöser-Lage** des echten Gebäudes — welche Regeln auf einem
realen Grundriss überhaupt feuern. Gemessen am Erdgeschoss:

| Messwert | EG |
|---|---|
| Räume / davon typisiert | 192 / 7 |
| Ausgänge `final_exit` | 4 |
| Ausgänge `stair_exit` | **0** |
| Notausgangstüren | 6 |
| Kreuzungen (Grad ≥ 3) | 12 |
| Segmente Richtungswechsel | 81 |
| STIEGENHAUS-Räume | 2 |

7 Fälle in `tests/normwissen/ground_truth/mollgasse_eg.yaml`, vier greifen
(`RZ-01`…`RZ-04`), drei halten eine Lücke fest:

- **GT-MOLL-EG-05** — 2 Stiegenhäuser, aber **0 `stair_exit` und 0 `stair`-Knoten**.
  `RZ-05`/`RZ-07` sind auf echten Plänen unerreichbar, obwohl der Platzierer den
  Code-Pfad hat. → Befund an **@polatselman**.
- **GT-MOLL-EG-06** — vier belegte Pflichtstellen aus §4.1.2 sind nicht planbar, weil
  das `RaumModell` die Merkmale nicht führt. → **Contract-Lücke, 3-Owner**.
- **GT-MOLL-EG-07** — 1OG typisiert 2/254 Räume, 1KG 6/64, beide 0 Segmente. Deckt
  sich mit `DOD_GEBAEUDE_MOLLGASSE.md` (6 von 8 Geschossen faktisch leer).

Die Tests prüfen **Untergrenzen**: verbessert sich die Raumerkennung, steigen die
Zahlen, ohne den Test zu brechen. Ground Truth übersteuert keine Norm.

---

## 4. Übergabe an Track A

### Fertige Regeldateien

| Datei | Inhalt |
|---|---|
| `normwissen/data/platzierung_regeln.yaml` | die Matrix (Single Source) |
| `normwissen/platzierungsregeln.py` | Query-API `PlatzierungsRegelwerk` |
| `tests/normwissen/test_platzierungsregeln.py` | 27 Domain-Tests |
| `tests/normwissen/ground_truth/mollgasse_eg.yaml` | 7 Ground-Truth-Fälle |

### Was die Engine konsumieren soll

```python
from notbeleuchtung.normwissen import PlatzierungsRegelwerk

w = PlatzierungsRegelwerk()
w.umsetzbar()                 # 17 Regeln, die das heutige RaumModell trägt
w.fuer_leuchtenart("rz")      # nach Priorität sortiert
w.gewinner(a, b)              # Konfliktauflösung; None == Review
w.hard_stops()                # unübersteuerbare Grenzen
w.blockiert_durch_contract()  # 8 Regeln, die auf Contract 1 warten
```

Felder je Regel: `id` · `ausloeser` · `leuchtenart` · `positionierungsziel` ·
`orientierung` · `abstand` · `prioritaet` · `ausnahmen` · `konfliktregel` ·
`review_erforderlich` · `decision_source` · `engine_input` · `engine_status` ·
`quelle` · `norm_ref` · `beleg`.

`quelle` + `norm_ref` gehören in den Audit-Trail der erzeugten Platzierung — dieselbe
Rolle wie `norm_quelle` heute.

### Review-Fälle (10) — nie still entscheiden

`RZ-06`, `RZ-11`, `SL-04`…`SL-08`, `SL-10`, `SL-11`, `SL-14`. Sie liefern **keinen
Default**. Erwartetes Verhalten analog zum LB-Parser: Befund mit Fundstelle
erzeugen, nicht raten.

### Contract-Vorschlag (3-Owner, blockiert 8 Regeln)

`RaumModell` braucht die hervorzuhebenden Stellen aus EN 1838 §4.1.2. Vorschlag,
rein additiv, Contract 1:

```python
class Sonderstelle(BaseModel):
    id: str
    xy_mm: XY
    typ: Literal["feuerloescher", "hydrant", "erste_hilfe",
                 "brandmelder", "niveauaenderung"]
    raum_id: str | None = None

class RaumModell(BaseModel):
    ...
    sonderstellen: list[Sonderstelle] = Field(default_factory=list)
```

Zusätzlich auf `Raum`: `ist_barrierefrei: bool = False` (§4.3.8) und
`besondere_gefaehrdung: bool = False` (§4.4.1).

Danach ist `PlatzierungsRegel` selbst der zweite Contract-Kandidat
(`hauptengine/contracts/platzierung_regel.py` + Aufnahme in `ports.NormProvider`).
Bis dahin liegt das Modell bewusst in `normwissen/` und Track A fragt die API.

### Offene Domain-Fragen

1. **Lux-Niveau an Betonungsstellen.** §4.1.2 fordert die Leuchte ≤ 2 m, nennt aber
   keinen Lux-Wert für Feuerlöscher/Hydrant/Erste-Hilfe. Die 5 lx stammen aus der
   realen Elektro-LB. → Normquelle beschaffen oder als LB-abhängig belassen.
2. **Niveauänderung.** Steht in der realen LB, nicht in der vorliegenden
   §4.1.2-Extraktion (die nennt Treppen). → Originalwortlaut gegenlesen.
3. **`vorschriftenkurzuebersicht-at.pdf`** (PR #66) ist AES-verschlüsselt; `pypdf`
   öffnet es ohne `cryptography` nicht. Nicht ausgewertet.
4. **OVE R 12-2, OVE E 8350, TRVB E 102** liegen nur als Quellen-*Nennung* in
   `_port_source` vor, nicht als Volltext. Die RZ-Pflicht ab GK3 stützt sich darauf.
5. **Wegbreite > 2 m / Randstreifen** (§4.2.1, §4.3.1 Anhang B) ist nicht modelliert.
6. **`stair_exit` wird nie erzeugt** — Raumerkennungs-Befund, blockiert 2 Regeln.

### Empfohlener nächster Track-A-Slice

**`SL-03-KREUZUNG` + `RZ-05`/`RZ-07` ehrlich machen.** Beide sind 🟡, beide brauchen
keinen neuen Contract:

1. `SL-03` — an jeder Kreuzung zusätzlich zur RZ eine Sicherheitsleuchte ≤ 2 m
   setzen. Heute sitzt dort nur das Zeichen; §4.1.2 verlangt die Beleuchtung des
   Knotens. Reine `platzierung`-Arbeit, Eingabe ist da (12 Kreuzungen allein im
   Mollgasse-EG).
2. `RZ-11`/`HS-04` verdrahten — wenn keine Fluchtrichtung bestimmbar ist, einen
   Review-Befund erzeugen statt einer Platzierung. Die Naht dafür existiert seit
   `lb_review` in `render_summary`.

Erst danach der Contract-Slice für die Sonderstellen — er kostet 3-Owner-Abstimmung
und schaltet dann 8 Regeln auf einmal frei.
