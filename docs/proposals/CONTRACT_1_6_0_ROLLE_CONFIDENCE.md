# Contract-Vorschlag `raum_modell` 1.6.0 — `rolle` + `confidence` durch die Naht

> Selman (@polatselman), 2026-09-12. **Status: VORSCHLAG, nicht umgesetzt.**
> Kein Feld angelegt, kein Schema angefasst, kein Version-Bump, keine Zeile
> Code. Adressiert an **@mvpo3** und **@EnisAMG**. `hauptengine/contracts/**`
> ist Konsens-Lane (Contract-Freeze, `docs/CONTRACTS.md`) — dieses Dokument
> macht den Diff reviewbar, es nimmt die Freigabe nicht vorweg.
>
> Auslöser ist Leonis' Contract-Forderung aus der Slice-3b-Review
> (`docs/COORDINATION.md` auf `origin/leonis/demo-l-gebaeude`, Eintrag
> 2026-09-10): die Naht muss **`rolle` + `confidence`** tragen (nicht nur
> `rolle`), „damit die Confidence bis zur Platzierung durchkommt und **ich bei
> niedriger Confidence auch fail-closed** gehen kann, statt auf geratener
> Geometrie zu platzieren.“

## 1. Warum das NICHT in 1.5.0 hineingeschoben wird

`raum_modell` **1.5.0** (`Raum.polygon_roh`, `Raum.bereinigung[]`) liegt mit
PR #155 beim Approval aller drei Owner. Ein Approval gilt nur für den Stand,
auf dem es erteilt wurde — **jeder nachgeschobene Commit entwertet es** (Check
`contract-freeze`, `docs/CONTRACTS.md` § Contract-Freeze). Ein zusätzliches
Feld in 1.5.0 würde also genau die Approvals wegwerfen, auf die 1.5.0 wartet,
und die fertig gemessene Raumbereinigung mit einer offenen Debatte über
Confidence-Semantik verkoppeln. Deshalb: eigene Stufe, eigener PR, **nach**
1.5.0.

Zweiter Grund, gleich wichtig: **1.6.0 hätte heute keinen Erzeuger.** Slice 3b
ist nicht gebaut, `layer_features.py` existiert nicht — gemessen: außer dem
toten `raumerkennung/_port/` (nicht importierbar, `test_port_bleibt_tot`) gibt
es in `src/notbeleuchtung/**` keine Dialekt-/Layer-Rollen-Erkennung. Ein Feld
ohne Erzeuger ist genau der Fall, den wir bei `STANDARDWERT` gerade streichen
wollen (Auflage B, `docs/OFFENE_FRAGEN.md`). Der Vorschlag ist deshalb
bewusst **Vorschlag und nicht Bauauftrag**: er legt die Naht fest, damit Slice
3b sie nicht nachträglich erfinden muss.

## 2. Der Vorschlag im Detail

Drei Ebenen, **alle additiv mit Default** — kein bestehender Erzeuger bricht,
bestehende Fixtures laden unverändert, und ein Konsument, der die Felder nicht
kennt, verhält sich wie heute.

| Ebene | Feld | Bedeutung |
|---|---|---|
| Layer (neu) | `LayerRolle.rolle` + `.confidence` | je Layer eine grobe Rolle mit Score |
| `RaumModell` | `dialekt_confidence`, `dialekt_quelle` | wie sicher ist das Plan-Profil, und woher kommt es |
| `Raum`, `Tuer` | `erkennungs_confidence` | optionaler Score je Objekt |

```python
# hauptengine/contracts/raum_modell.py — ENTWURF, NICHT umgesetzt.
# Alle Felder additiv mit Default: kein Erzeuger bricht, kein Konsument muss sie kennen.

# Grobe Layer-Rollen (Leonis' Einwand (b): grobe Klassen zuerst, `stiege` und
# andere Objekte gehoeren NICHT hierher, sondern in einen Objekt-Matcher).
LayerRollenName = Literal["wand", "oeffnung", "raumkontur", "rest"]

# Woher das Dialekt-Profil stammt. KEIN Default-Rateweg: "unbekannt" heisst
# "nicht bestimmt", nicht "egal".
DialektQuelle = Literal["unbekannt", "regel", "modell", "manuell"]


class LayerRolle(BaseModel):
    """Ein Plan-Layer mit der Rolle, die die Erkennung ihm zuschreibt.

    `confidence` ist ein Score in [0, 1] und AUSDRUECKLICH keine
    Wahrscheinlichkeit, solange 3b regelbasiert ist (s. § 4.1).
    """

    layer: str                       # Layername EXAKT wie im DXF (Audit-Trail)
    rolle: LayerRollenName
    confidence: float = Field(ge=0.0, le=1.0)
    # Warum diese Rolle: Regel-ID bzw. Modellversion. Pflicht fuer den
    # Audit-Trail -- ein Score ohne Herkunft ist nicht pruefbar.
    begruendung: str


class Raum(BaseModel):
    ...  # unveraendert
    # v1.6.0 -- None = nicht bewertet (NICHT 1.0, NICHT 0.0):
    erkennungs_confidence: float | None = Field(default=None, ge=0.0, le=1.0)


class Tuer(BaseModel):
    ...  # unveraendert
    # v1.6.0 -- None = nicht bewertet, gleiche Lesart wie breite_mm is None:
    erkennungs_confidence: float | None = Field(default=None, ge=0.0, le=1.0)


class RaumModell(BaseModel):
    ...  # unveraendert
    # v1.6.0 -- Dialekt-/Profil-Erkennung. LEER + None + "unbekannt" ist der
    # heutige Zustand: kein Erzeuger, keine Aussage.
    layer_rollen: list[LayerRolle] = Field(default_factory=list)
    dialekt_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    dialekt_quelle: DialektQuelle = "unbekannt"
```

**Was mitzuziehen wäre (nicht umgesetzt):**

1. `hauptengine/contracts/raum_modell.py` — die Typen `LayerRollenName`,
   `DialektQuelle`, `LayerRolle` und die vier Felder.
2. `raum_modell.py:18` — `CONTRACT_VERSION` `"1.5.0"` → `"1.6.0"` (Minor, rein
   additiv wie 1.1.0–1.5.0).
3. `python scripts/gen_schema.py` → `contracts/schema/raum_modell.schema.json`
   mitcommitten; bis dahin ist `tests/contract/test_schema_drift.py` rot.
4. `docs/CONTRACTS.md` § RaumModell — die drei Ebenen in Prosa, mit der
   `None`-Lesart und der ausdrücklichen Aussage, dass ein regelbasierter Score
   keine Wahrscheinlichkeit ist.
5. Approval **aller drei Owner** auf dem Head des PR (`contract-freeze`).
6. **Nicht** Teil des Contracts: die Schwellenwerte (§ 3).

## 3. Betriebsregel — und die Schwelle als Parameter, nicht als Konstante

Betrieb wie von Leonis vorgeschlagen:

| Confidence | Verhalten |
|---|---|
| **≥ 0,85** | übernehmen |
| **0,60 – 0,85** | Mensch bestätigt |
| **< 0,60** | **fail closed** — der Provider stoppt (HARD STOP), kein Modell auf geratener Geometrie |

Für Leonis kommt die Forderung dazu, dass **die Platzierung selbst**
fail-closed gehen kann. Dafür braucht sie die Schwelle als **Parameter**, nicht
als Contract-Konstante: der Contract transportiert die Messung, die
Betriebsentscheidung gehört dem Betreiber. An der Naht sieht das so aus —
`platzierung/kontext.py` hat dafür seit dem Architektur-Slice genau den
richtigen Ort (`PlatzierungsKontext`, frozen dataclass, **kein Contract-Typ**,
neue Naht = ein Feld statt N Signaturen):

```python
# platzierung/kontext.py — ENTWURF, NICHT umgesetzt
@dataclass(frozen=True)
class PlatzierungsKontext:
    lb: LBVorgabe | None = None
    oib: OibBefund | None = None
    i_cd_fn: Callable | None = None
    i_cd_fn_je_key: Mapping[str, Callable] = field(default_factory=dict)
    #: Ab welcher Erkennungs-Confidence platziert wird. None = Schwelle AUS
    #: (heutiges Verhalten, unveraendert). Der Wert ist eine Betriebs-
    #: entscheidung des Aufrufers, KEINE Norm- und keine Contract-Groesse.
    min_confidence: float | None = None
```

```python
# platzierung/platzierer.py — ENTWURF, NICHT umgesetzt
def place(self, raum, norm, lb=None, *, oib=None, min_confidence=None):
    kontext = PlatzierungsKontext(
        lb=lb, oib=oib, i_cd_fn=self._i_cd_fn,
        i_cd_fn_je_key=self._i_cd_fn_je_key,
        min_confidence=min_confidence,      # None => alles wie heute
    )
```

Damit gilt: **`None` = Schwelle aus = heutiges Verhalten** (wichtig, weil heute
kein Erzeuger die Confidence füllt — eine Default-Schwelle würde jeden
bestehenden Lauf blockieren). Wer fail-closed will, setzt sie; die
Entscheidung, was dann passiert (Platzierung auslassen und als Befund melden
vs. Lauf abbrechen), gehört in @mvpo3s Lane und ist hier nicht vorgeschlagen.

## 4. Offene Fragen — vor einer Umsetzung zu klären

### 4.1 Woraus entsteht die Confidence numerisch, solange 3b regelbasiert ist?

Das ist die wichtigste Frage, und sie ist offen. Slice 3b ist in der
vorgeschlagenen Reihenfolge **Schritt 3 und regelbasiert** (Modellkopf erst
Schritt 5, „bei ~20 Büros“). Ein regelbasierter Score ist **keine
Modellwahrscheinlichkeit** — es gibt keine kalibrierte Verteilung, keine
Likelihood, nichts, was man über Läufe hinweg vergleichen darf. „0,85“ aus
einer Regelsumme und „0,85“ aus einem GBM sind zwei verschiedene Dinge.

Das muss ehrlich im Contract stehen, sonst rechnet ein Konsument mit der Zahl,
wie man mit einer Wahrscheinlichkeit rechnet (multiplizieren, mitteln,
schwellen). Drei denkbare Wege, keiner entschieden: (a) Score **und**
Semantik-Feld (`score_art: regel | modell`) — dann muss jeder Konsument beides
lesen; (b) `confidence` erst mit dem Modellkopf einführen und bis dahin nur
`rolle` + `begruendung` tragen; (c) `confidence` als reinen Ordnungsscore
deklarieren, der **nur** gegen die drei Schwellen verglichen werden darf. Mein
Vorschlag ist (c) plus ein Satz im Contract, dass Arithmetik darauf verboten
ist. Entscheidung der 3-Owner-Runde.

### 4.2 Hat „Mensch bestätigt“ im heutigen Lauf überhaupt einen Ort?

Nein — heute gibt es **keine interaktive Stufe**. Ein Lauf ist
`scripts/plan_pruefen.py` bzw. die Pipeline, Ausgabe ist der Prüfbericht, und
die einzige menschliche Instanz ist der Owner, der ihn liest. Das mittlere Band
0,60–0,85 hat damit keinen Adressaten im Code.

Zwei Optionen, bis es eine Bestätigungsstufe gibt: (a) das mittlere Band **wie
< 0,60 behandeln** (fail closed, konservativ, blockiert aber Pläne, die heute
durchlaufen); (b) als **Warnung mit Weiterlauf** führen — Eintrag im
Prüfbericht wie die „Hinweise Kürzel-Auflösung“, Lauf geht weiter, Owner
entscheidet nachträglich. Präzedenzfall im Repo ist (b): bei `Schl.` bleibt der
Raum untypisiert und der Bericht sagt es je Lauf. **Entscheidung der
3-Owner-Runde**, nicht von mir.

### 4.3 Wer setzt `dialekt_quelle`, und welche Werte sind erlaubt?

`"regel"` und `"modell"` gehören der Erkennung (Selman-Lane). Offen ist:
**`"manuell"`** — wer darf ein Profil von Hand setzen, wo wird das hinterlegt
(Register wie `kuerzel_entscheid.py`, das je Stempelnummer eine
Owner-Entscheidung führt?), und gilt es je Plan oder je Plan-Familie? Und darf
`"manuell"` die Schwellen aus § 3 überspringen? Ohne Antwort darauf würde ich
`"manuell"` **nicht** mit anlegen — ein Enum-Wert ohne Erzeuger und ohne
Prozess ist wieder ein `STANDARDWERT`.

### 4.4 Versionsstufe und Reihenfolge gegen die zwei offenen Auflagen

Drei Contract-Änderungen konkurrieren um die nächste Stufe:

- **Auflage B** (`STANDARDWERT` streichen): eine **Einengung** des Enums
  `BreiteQuelle` und formal **nicht** additiv — die Stufe ist ungeklärt, die
  3-Owner-Runde legt sie fest.
- **Auflage A** (`lichte_quelle`): additiv, kommt aber erst **mit dem ersten
  Erzeuger** von `lichte_mm` (heute 0 von 612 Türen) — also nicht datumsgetrieben.
- **Dieser Vorschlag** (1.6.0): additiv, aber ohne Erzeuger.

Vorschlag zur Reihenfolge: **1.5.0 zuerst abschließen** (Approvals einsammeln,
nichts nachschieben), dann Auflage B, weil sie als Einengung die Stufe
bestimmt und Datenbestand 0 hat, und dieser Vorschlag danach oder gebündelt —
**gebündelt ist besser**, weil jeder einzelne Contract-PR eine neue
3-Owner-Approval-Runde auf einem neuen `head_sha` kostet. Auflage A hängt
ohnehin am Erzeuger und sollte mit ihm kommen, nicht vorher.

## 5. Status — ausdrücklich

**Nichts davon ist umgesetzt.** Kein Feld angelegt, kein Schema angefasst, kein
`CONTRACT_VERSION` verändert, keine Zeile in `platzierung/` geändert, kein
Test. Die Codeblöcke oben sind Entwürfe zum Gegenlesen, kein Diff. Was ich für
die Umsetzung brauche: eine Antwort auf § 4.1 (Semantik des Scores) und § 4.2
(mittleres Band) von der 3-Owner-Runde, und von @mvpo3 die Zusage, dass die
Schwelle als Parameter an seiner Naht liegt und nicht im Contract.
