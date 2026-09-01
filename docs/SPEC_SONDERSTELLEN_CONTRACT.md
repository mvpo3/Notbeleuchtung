# Spec — Sonderstellen im `RaumModell` (Contract-Vorschlag)

> **Owner:** Enis (`normwissen`) · **Stand:** 2026-08-31
> **Status:** **VORSCHLAG.** Kein Contract geändert, kein `contract_version`-Bump,
> `hauptengine/contracts/**` unberührt. Umsetzung erst nach **3-Owner-GO**.
>
> Ausführbar: `normwissen.SonderstellenKatalog` + `data/sonderstellen.yaml`,
> 17 Tests in `tests/normwissen/test_sonderstellen.py`.

## Worum es geht

EN 1838 §4.1.2 verlangt, dass bestimmte **Stellen** hervorgehoben werden — jeder
Notausgang, Richtungsänderungen, Treppen, Kreuzungen, **Erste-Hilfe-Stellen,
Brandbekämpfungs- und Meldeeinrichtungen** — jeweils mit einer Leuchte ≤ 2 m
horizontal. Die ersten vier kann die Engine, die letzten drei nicht: das
`RaumModell` führt sie schlicht nicht.

Ergebnis: **8 von 25 Regeln** der Placement-Decision-Matrix sind blockiert, vier
davon sind **belegte Pflichtstellen**.

---

## 1. Was genau blockiert ist

| Regel-ID | benötigtes Merkmal | Input heute? | Contract-Lücke | Nutzen bei Freischaltung |
|---|---|---|---|---|
| `SL-06-FEUERLOESCHER` | Position Feuerlöscher | ⛔ | `Sonderstelle(typ=feuerloescher)` | belegte Pflichtstelle §4.1.2 |
| `SL-07-WANDHYDRANT` | Position Wandhydrant | ⛔ | `Sonderstelle(typ=hydrant)` | Pflichtstelle (Auslegung §4.1.2) |
| `SL-05-ERSTE-HILFE-STELLE` | Position Erste-Hilfe | ⛔ | `Sonderstelle(typ=erste_hilfe)` | belegte Pflichtstelle §4.1.2 |
| `SL-08-BRANDMELDER` | Position Meldeeinrichtung | ⛔ | `Sonderstelle(typ=brandmelder)` | belegte Pflichtstelle §4.1.2 |
| `RZ-06-NIVEAUAENDERUNG` | Position Niveausprung | ⛔ | `Sonderstelle(typ=niveauaenderung)` | LB-Anforderung erfüllbar |
| `SL-04-NIVEAUAENDERUNG` | Position Niveausprung | ⛔ | dieselbe Stelle | LB-Anforderung erfüllbar |
| `SL-10-BARRIEREFREIES-WC` | Raum ist barrierefrei | 🟡 `raum_typ == WC`, aber nicht „barrierefrei" | `Raum.ist_barrierefrei` | belegte Pflicht §4.3.8 |
| `SL-11-BESONDERE-GEFAEHRDUNG` | Raum/Fläche gefährdet | ⛔ | `Raum.besondere_gefaehrdung` | belegte Pflicht §4.4.1, höchster Lux-Anspruch |

Maschinell nachprüfbar: `PlatzierungsRegelwerk().blockiert_durch_contract()` ==
`SonderstellenKatalog().wuerde_freischalten()` — ein Test hält das fest.

---

## 2. Vorgeschlagenes Modell — minimal und additiv

**Ein** generisches Punkt-Modell für die punktförmigen Stellen, **zwei** Flags für
die Raum-Eigenschaften. Kein Feld je Normregel.

```python
# hauptengine/contracts/raum_modell.py  (nach 3-Owner-GO)

SonderstellenTyp = Literal[
    "feuerloescher", "hydrant", "erste_hilfe", "brandmelder", "niveauaenderung",
]

class Sonderstelle(BaseModel):
    """Hervorzuhebende Stelle nach EN 1838 §4.1.2 — punktförmig."""
    id: str
    typ: SonderstellenTyp
    xy_mm: XY
    raum_id: str | None = None
    quelle: str = ""              # Audit-Trail: woher die Angabe stammt

class Raum(BaseModel):
    ...
    ist_barrierefrei: bool = False        # §4.3.8
    besondere_gefaehrdung: bool = False   # §4.4.1

class RaumModell(BaseModel):
    ...
    sonderstellen: list[Sonderstelle] = Field(default_factory=list)
```

**Warum Punkt und nicht Raum-Flag:** die 2-m-Regel aus §4.1.2 ist ein *Abstand zum
Gerät*. Ein Raum-Flag kann sie nicht ausdrücken. **Warum umgekehrt Raum-Flags für
§4.3.8/§4.4.1:** dort gilt die Anforderung dem Raum bzw. der Aufgabenfläche, nicht
einem Punkt.

**Warum die Typ-Namen nicht erfunden sind:** der professionelle Plan
`DIN-Notbeleuchtungspläne(Beispiele)/din_support_ReMi_Barawitzkagasse_28.04.2026.dxf`
führt genau diese Stellen als Blöcke — `din_Feuerloescher_F001`, `din_Hydrant_F002`,
`din_ErsteHilfe_E003` (Registriernummern nach ISO 7010). Die Fachpraxis benennt sie
bereits so.

Alle Felder haben Defaults → **rein additiv**, bestehende Fixtures und Golden-Daten
bleiben gültig.

---

## 3. Was jeder Typ auslöst

| Typ | Regel | Leuchtenart | Abstand | Norm-Lux | LB-Lux | Beleg |
|---|---|---|---|---|---|---|
| `feuerloescher` | `SL-06` | sicherheitsleuchte | ≤ 2000 mm | **keiner** → `MANUELL_PRUEFEN` | 5,0 lx | BELEGT (§4.1.2) |
| `hydrant` | `SL-07` | sicherheitsleuchte | ≤ 2000 mm | **keiner** → `MANUELL_PRUEFEN` | 5,0 lx | AUSLEGUNG (§4.1.2) |
| `erste_hilfe` | `SL-05` | sicherheitsleuchte | ≤ 2000 mm | **keiner** → `MANUELL_PRUEFEN` | — | BELEGT (§4.1.2) |
| `brandmelder` | `SL-08` | sicherheitsleuchte | ≤ 2000 mm | **keiner** → `MANUELL_PRUEFEN` | — | BELEGT (§4.1.2) |
| `niveauaenderung` | `RZ-06` + `SL-04` | rz + sicherheitsleuchte | ≤ 2000 mm | — | — | BELEGT (§4.1.2 c); Lux offen |

### Der Punkt, an dem nicht geschummelt wird

> **Korrigiert am 01.09.2026.** Dieser Abschnitt behauptete bis dahin, §4.1.2 nenne
> für diese Stellen kein Beleuchtungsniveau. Das ist am Volltext widerlegt: §4.1.2
> **h)** und **i)** fordern „so dass **5 lx vertikale Beleuchtungsstärke** … erreicht
> werden" — am Erste-Hilfe-Kasten bzw. an Melde- und Brandbekämpfungseinrichtungen
> und den Anzeigen der Brandmeldeanlage. Belege: `docs/NORMQUELLEN_AT.md` 2c.

**§4.1.2 begründet die Leuchte — und beziffert vier der fünf Stellen.** Für
Feuerlöscher, Wandhydrant, Erste-Hilfe-Stelle und Meldeeinrichtung ist der Wert
normativ; die reale Elektro-LB (§5.1.23) wiederholt ihn nur. Weicht eine LB ab,
übersteuert sie ihn (LB-explizit > Norm-Default).

**Der Wert ist vertikal am Gerät, nicht horizontal am Boden.** Der Lux-Nachweis der
Engine (`lux_raster`) rechnet horizontal — ein vertikaler Norm-Wert darf dort nicht
als `min_lux` eingesetzt werden. Die Query-API trägt die Bezugsfläche deshalb im
Namen: `norm_lux_vertikal(typ)` liefert 5.0, `norm_lux_horizontal(typ)` bewusst
`None`. Zwei Tests nageln beides fest.

**Ohne eigenen Lux-Wert bleibt `niveauaenderung`** (§4.1.2 c) nennt nur „nahe",
ANMERKUNG 1: ≤ 2 m horizontal). Dort gilt weiter `MANUELL_PRUEFEN`. Der *Auslöser*
ist aber auch dort belegt — §4.1.2 führt b) Treppen und c) jede andere
Niveauänderung als getrennte Punkte.

**Feuerlöscher und Wandhydrant bleiben fachlich getrennt**, auch wenn die LB beide in
einem Satz nennt: zwei Geräte, zwei Orte, zwei 2-m-Umgebungen. Der Katalog trägt
dafür ein explizites `nicht_zusammenfassen_mit`.

---

## 4. Woher die Daten kommen sollen

| Quelle | heute nutzbar? | Befund |
|---|---|---|
| **Architekturplan (heute geparst)** | ❌ | An Mollgasse EG + 1KG geprüft: **keine** Feuerlöscher-, Hydranten-, Erste-Hilfe- oder Melder-Symbole. Nur Fließtext-Anmerkungen ohne Position. **Keine Quelle.** |
| **Elektro-LB (2. Input)** | ⚠️ teilweise | Liefert die **Anforderung**, nicht den **Ort**: `SonderLux` trägt `ort` + `min_lux`, keine Koordinate. Kann den Lux-Wert setzen, aber **keine Sonderstelle erzeugen**. |
| **GU-Dokument** | ❌ | Verweist auf die Elektro-LB; trägt selbst keine Notbeleuchtungs-Vorgaben (fail-closed am realen GU-Dokument belegt). |
| **Bestückter Elektro-/Notbeleuchtungsplan** | ❌ (künftig) | Fachlich naheliegendste Quelle. Im Repo liegt nur die Symbol-**Bibliothek** (0 platzierte INSERTs), kein bestückter Plan → **kein Parser, kein Beleg**. |
| **Manuelle Angabe** | ✅ | Die einzige heute tragfähige Quelle. |

**Konsequenz für den Zuschnitt:** der Vorschlag ist so geschnitten, dass er **ohne
Parser** nutzbar ist. `SonderstellenKatalog.typ_ist_heute_automatisch_erkennbar()`
gibt für jeden Typ `False` zurück — ein Test verhindert, dass hier je etwas als
automatisch erkennbar behauptet wird, wofür es keinen erprobten Parser gibt.

---

## 5. Fail-closed-Verhalten

| Eingabe | Verhalten |
|---|---|
| unbekannter `typ` | **Review.** Eine still verworfene Sonderstelle ist eine verlorene Pflichtstelle. |
| Sonderstelle ohne `xy_mm` | **Review.** Ohne Koordinate ist die 2-m-Regel nicht prüfbar. |
| Typ mit ungeklärtem Lux-Niveau | **Review** — die Leuchte wird trotzdem gefordert. |
| Hard Stops (`HS-01`…`HS-04`) | bleiben übergeordnet, der Vorschlag rührt sie nicht an. |

---

## 6. Entscheidung — drei Optionen

### Option A — generisches `sonderstellen[]` (**Empfehlung**)

Ein Modell, ein Listenfeld, zwei Raum-Flags.

- **Vorteile:** ein Contract-Bump für alle 8 Regeln · neue Typen später ohne
  Schema-Änderung (nur Literal + Katalog-Eintrag) · Track A schreibt **eine**
  Abstandslogik statt fünf · Typ-Vokabular deckt sich mit ISO-7010-Symbolik
- **Nachteile:** ein `Literal` muss gepflegt werden · sagt nichts über *Erkennung*
  (die bleibt offen)
- **Engine-Aufwand:** gering — eine generische Regel „Leuchte ≤ 2 m um jede
  Sonderstelle", getrieben aus dem Katalog
- **Skalierbarkeit:** hoch
- **Risiko:** gering — rein additiv, alle Felder mit Default

### Option B — einzelne Felder je Stellenart

`feuerloescher: list[XY]`, `hydranten: list[XY]`, `erste_hilfe: list[XY]`, …

- **Vorteile:** maximal explizit, jedes Feld eigenständig typisierbar
- **Nachteile:** jede neue Stellenart = **neuer Contract-Bump + 3-Owner-Runde** ·
  fünf fast identische Felder · Track A schreibt fünf fast gleiche Codepfade ·
  die gemeinsame 2-m-Semantik wird unsichtbar
- **Engine-Aufwand:** höher, wächst linear mit den Typen
- **Skalierbarkeit:** niedrig
- **Risiko:** mittel — Contract-Fläche wächst dauerhaft

### Option C — kein Contract-Ausbau, Sonderstellen manuell außerhalb

- **Vorteile:** kein Contract-Risiko, keine Abstimmung
- **Nachteile:** die 8 Regeln bleiben **dauerhaft** blockiert, darunter vier belegte
  Pflichtstellen · jeder erzeugte Plan bleibt in diesem Punkt unvollständig, ohne
  dass es der Ausgabe anzusehen wäre · widerspricht dem Nordstern (Plan rein →
  fertiger Plan raus)
- **Engine-Aufwand:** null jetzt, unbegrenzt später
- **Skalierbarkeit:** —
- **Risiko:** **hoch** — eine fehlende Pflichtleuchte ist ein Sicherheitsmangel, den
  heute nichts sichtbar macht

### Empfehlung

**Option A.** Sie schließt die Lücke exakt (ein Test prüft: nicht weniger, nicht
mehr), kostet eine 3-Owner-Runde statt fünf, und ist rein additiv. Option C ist
vertretbar, wenn Track A gerade keine Kapazität hat — dann aber bitte mit einem
sichtbaren Review-Befund im Plan, nicht stillschweigend.

---

## 7. Handoff — was nach dem GO zu tun ist

### @mvpo3 (Leonis) — `hauptengine/contracts/` + `platzierung/`

1. `raum_modell.py`: `Sonderstelle` + `SonderstellenTyp` ergänzen,
   `RaumModell.sonderstellen`, `Raum.ist_barrierefrei`, `Raum.besondere_gefaehrdung`
2. `CONTRACT_VERSION` bumpen → `python scripts/gen_schema.py` → Schema committen
   (sonst bricht das Drift-Gate)
3. `platzierung/`: eine generische Strategie „Sicherheitsleuchte ≤ 2 m um jede
   Sonderstelle", Typ-Parameter aus `SonderstellenKatalog`.
   `niveauaenderung` löst zusätzlich ein Rettungszeichen aus (`RZ-06`).
4. `normwissen/data/platzierung_regeln.yaml`: `engine_status` der 8 Regeln von
   `input_fehlt` auf `unterstuetzt` ziehen — **das mache ich**, sag mir Bescheid.

### @polatselman (Selman) — `raumerkennung/`

Zunächst **nichts**: keine der Quellen ist heute automatisch erkennbar, das Modell
funktioniert mit manueller Eingabe. Später relevant:

- `ist_barrierefrei` aus Raumstempeln („WC barrierefrei", „BF-WC")
- `niveauaenderung` aus Geometrie (Stufen, Rampen)
- ein bestückter Elektroplan als zusätzlicher Input — dafür bräuchten wir erst ein
  echtes Beispiel im Repo

### Bleibt `MANUELL_PRUEFEN`

1. **Lux-Niveau an Betonungsstellen** — §4.1.2 nennt keines; die 5 lx sind LB.
2. **Niveauänderung normativ** — steht in der LB, nicht in der §4.1.2-Extraktion.
3. **Teilflächen-Gefährdung** — ein Raum-Flag kann eine gefährdete *Teilfläche*
   nicht abbilden.
4. **`brandmelder` ohne CAD-Beleg** — im Repo liegt kein Symbol dafür.
5. **Notrufsprechstelle** (`din_Notrufstelle_E004`) — im Profi-Plan vorhanden,
   plausibel eine „Meldeeinrichtung", aber **keine Regel braucht sie**. Bewusst
   nicht aufgenommen; Aufnahme erst, wenn eine Regel sie fordert.
