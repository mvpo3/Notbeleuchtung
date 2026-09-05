# Vorschlag — Quellen-Naht für Sonderstellen (Umsetzung von SPEC §8)

> **Status: VORSCHLAG, nicht angewendet.** Kein Code dieses Dokuments liegt im
> Branch. Er braucht die **3-Owner-Freigabe** (`hauptengine/contracts/**` =
> @mvpo3 + @EnisAMG + @polatselman) und wird erst danach umgesetzt. Dieses
> Dokument macht den Diff reviewbar, es nimmt die Freigabe nicht vorweg.
>
> Autor: @EnisAMG (normwissen), 2026-09-05. Bezug:
> `docs/SPEC_SONDERSTELLEN_CONTRACT.md` §8, Review-Befund an PR #95, PR #103.

## Problem

Eine Pflicht-Leuchte an einer Sonderstelle trägt heute die `quelle` der
**erstbesten Raumregel** derselben Leuchtenart:

| Auslöser | richtige Fundstelle | ausgewiesen |
|---|---|---|
| Feuerlöscher | §4.1.2 **i)** | §4.1 (STIEGENHAUS-Regel) |
| Erste-Hilfe-Stelle | §4.1.2 **h)** | §4.1 |
| Niveauänderung | §4.1.2 **c)** | §4.2.1 (GANG-Regel) |
| barrierefreie Toilette | §4.3.8 | §4.3.1 (SAAL-Regel) |

`platzierung/sonderstellen_strategy._referenz()` kennzeichnet das seit #106 als
Fallback (Docstring + `hinweise`-Eintrag im Summary) — der Audit-Trail bleibt
trotzdem falsch. Die Ursache ist die Naht: `NormRegelwerk.quellen` ist die
erlaubte Menge für `Platzierung.norm_quelle`, und es gibt keinen typisierten Weg,
je Auslöser eine Anforderung samt eigener Fundstelle zu erfragen.

**Was auf `main` schon steht (PR #103, `normwissen`):** die Daten und die
Query-Methoden. `NormRegelwerk.quellen` enthält bereits §4.1.2 c)/h)/i), §4.3.8
und §4.4.1 — die Naht-Invariante würde die echten Fundstellen also **zulassen**.
Was fehlt, ist ausschließlich der **vereinbarte Weg**, sie abzuholen.

**Was ausdrücklich KEIN Weg ist**

* `getattr(norm, "fuer_sonderstelle", None)` aus `platzierung` — stille Kopplung
  an eine ungeprüfte Signatur, weder vom Drift-Gate noch von einem Review
  gedeckt. Ein Methodenzugriff ersetzt keine vereinbarte Schnittstelle.
* `from notbeleuchtung.normwissen import SonderstellenAnforderung` in
  `platzierung` — verletzt die Owner-Grenze (CLAUDE.md: kein Owner-Package
  importiert ein anderes).

Deshalb müssen Typ **und** Protocol in `hauptengine/contracts` liegen.

## Teil 1 — Contract-Typen (`contracts/norm_regelwerk.py`)

Wörtlich der Typ, der heute in `normwissen/sonderstellen.py` steht und dort
erprobt ist (25+ Tests) — beim Umzug entfällt die normwissen-eigene Kopie.

```python
Bezugsflaeche = Literal["vertikal_am_geraet", "horizontal_boden", "arbeitsflaeche"]


class LuxAnforderung(BaseModel):
    """Ein Beleuchtungsstärke-Wert MIT seiner Bezugsfläche.

    EN 1838 nennt §4.1.2 h/i vertikal am Gerät, §4.3.1 horizontal auf der freien
    Bodenfläche und §4.4.1 auf der Arbeitsfläche. Die drei sind nicht ineinander
    umrechenbar; ein Wert ohne Fläche ist kein Wert.
    """

    wert: float | None = None
    bezugsflaeche: Bezugsflaeche
    quelle: str
    mindestwert: float | None = None             # §4.4.1: 15 lx
    anteil_nennbeleuchtung: float | None = None  # §4.4.1: 0.10
    vollstaendig_bestimmbar: bool = True
    offen_grund: str = ""


class SonderstellenAnforderung(BaseModel):
    """Anforderung an EINER Sonderstelle bzw. für EIN Raum-Attribut.

    Bewusst kein `NormAnforderung`: dessen `min_lux` ist ein horizontaler
    Boden-Pflichtwert. §4.1.2 nennt entweder einen vertikalen Wert (h/i) oder gar
    keinen (c). `quelle=None` heißt: keine Norm-Fundstelle → kein Norm-Default.
    """

    ausloeser: str
    klassifikation: Klassifikation
    quelle: str | None
    norm_ref: str
    symbol_katalog_keys: list[str] = Field(default_factory=list)
    montagehoehe_mm: int = 2000
    max_abstand_mm: int | None = None            # §4.1.2 ANMERKUNG 1: 2000
    lux: LuxAnforderung | None = None
    ist_norm_default: bool = True
    decision_source: str = "norm_default"
    begruendung: str = ""
    gilt_nur_fuer_raumtypen: list[str] = Field(default_factory=list)
    nachweis_offen: bool = False
    nachweis_offen_grund: str = ""
```

`CONTRACT_VERSION` **1.2.0 → 1.3.0**, `python scripts/gen_schema.py`, Schema
committen.

## Teil 2 — Ports (`contracts/ports.py`, kein Pydantic → kein Schema-Drift)

```python
 class NormProvider(Protocol):
     def fuer_raum(self, raum_typ: str, ist_fluchtweg: bool) -> NormAnforderung: ...
     def fuer_fluchtweg_abschnitt(self, segment: FluchtwegSegment) -> NormAnforderung: ...
     def erkennungsweite_m(self, piktogramm_hoehe_m: float, hinterleuchtet: bool) -> float: ...
     def regelwerk_snapshot(self) -> NormRegelwerk: ...
+
+    def fuer_sonderstelle(self, typ: str) -> list[SonderstellenAnforderung]: ...
+    def zur_pruefung(self, typ: str) -> list[SonderstellenAnforderung]: ...
+    def fuer_raum_attribut(
+        self, attribut: str, raum_typ: str | None = None
+    ) -> list[SonderstellenAnforderung]: ...
```

Semantik (heute in `normwissen` implementiert und getestet):

* `fuer_sonderstelle` — nur **norm-belegte** Anforderungen.
* `zur_pruefung` — Kandidaten **ohne** Norm-Beleg (`quelle=None`,
  `ist_norm_default=False`), z.B. das RZ an einer Niveauänderung.
* `fuer_raum_attribut` — `raum_typ` ist Teil des Auslösers (§4.3.8 gilt für
  Toiletten). Leere Liste = dieser Auslöser greift nicht; ohne nötigen `raum_typ`
  ein `ValueError` statt eines stillen Defaults.

## Teil 3 — Konsumption (`platzierung/sonderstellen_strategy.py`)

Ersetzt den Fallback `_referenz()`. Der Diff gegen den heutigen Stand:

```diff
-def _referenz(norm: NormProvider, klassifikation: str):
-    """Erste Regelwerk-Anforderung der Klassifikation mit Symbol — oder None.
-    ⚠️ FALLBACK: die zurückgegebene `quelle` ist die der Referenz-Regel …"""
-    for regel in norm.regelwerk_snapshot().regeln:
-        anf = regel.anforderung
-        if anf.klassifikation == klassifikation and anf.symbol_katalog_keys:
-            return anf
-    return None
+def _anforderungen(norm: NormProvider, ausloeser: str, raum_typ: str | None = None):
+    """Norm-belegte Anforderungen dieses Auslösers — mit seiner echten Fundstelle."""
+    if raum_typ is None:
+        return norm.fuer_sonderstelle(ausloeser)
+    return norm.fuer_raum_attribut(ausloeser, raum_typ)

 def plan_sonderstellen(raum, norm, lb=None):
     for stelle in raum.sonderstellen:
-        if sl_ref is not None:
-            out.append(_leuchte(stelle.xy_mm, sl_ref, "sicherheitsleuchte", building))
-        if stelle.typ == "niveauaenderung" and rz_ref is not None and rz_lb_quelle:
-            out.append(_leuchte(stelle.xy_mm, rz_ref, "rz", building, lb_quelle=rz_lb_quelle))
+        for anf in _anforderungen(norm, stelle.typ):
+            out.append(_leuchte(stelle.xy_mm, anf, anf.klassifikation, building))
+        # Kandidaten ohne Norm-Beleg nur mit LB-Deckung — Quelle bleibt die LB.
+        for anf in norm.zur_pruefung(stelle.typ):
+            quelle = _lb_deckung(lb, stelle.typ, anf)
+            if quelle:
+                out.append(_leuchte(stelle.xy_mm, anf, anf.klassifikation,
+                                    building, lb_quelle=quelle))
```

`_leuchte()` zieht `norm_quelle` dann aus `anf.quelle` (der **echten** Fundstelle)
und die Höhe/Symbole aus `anf` — die Signatur bleibt sonst gleich. Der
`hinweise`-Eintrag „norm_quelle = Fallback-Referenzregel" in `pipeline.py`
entfällt mit dieser Umstellung.

Für `plan_flag_raeume` analog mit `raum_typ`; der lokal bereits umgesetzte
WC-Kontext-Filter wird dann **von der Anforderung selbst** getragen
(`gilt_nur_fuer_raumtypen`) statt von einer Konstante in `platzierung`.

## Teil 4 — Prüfbericht

`SonderstellenAnforderung.nachweis_offen` + `nachweis_offen_grund` ersetzen die
heutige Typ-Liste `_SONDERSTELLEN_MIT_LUX` in `validierung.py`: die Regeln 12/12b
fragen dann die Anforderung, statt die Typen ein zweites Mal aufzuzählen. Der
Text der Befunde bleibt gleichwertig, die Bezugsfläche kommt aus
`lux.bezugsflaeche`.

## Auswirkungen (vollständig)

| Was | Warum |
|---|---|
| `norm_regelwerk`-`CONTRACT_VERSION` **1.2.0 → 1.3.0** | zwei neue Modelle im Modul |
| `scripts/gen_schema.py` + Schema committen | sonst bricht das Drift-Gate |
| `tests/fakes.py::FakeNormProvider` um drei Methoden ergänzen | `NormProvider` ist `runtime_checkable` — ohne sie erfüllt der Fake das Protocol nicht mehr |
| `tests/fixtures/norm_regelwerk_snapshot.json` (CODEOWNERS: alle drei) um §4.1.2 c)/h)/i), §4.3.8, §4.4.1 ergänzen | `tests/platzierung/test_platzierer.py` prüft `norm_quelle` gegen die **Fixture** — sonst bricht der erste reale Sonderstellen-Plan |
| `normwissen/sonderstellen.py`: lokale Typ-Kopie entfernen, Import aus `contracts` | eine Wahrheit |
| keine Signatur-Änderung an bestehenden Methoden | rein additiv |

## Was der Vorschlag NICHT leistet

* **Keinen lichttechnischen Nachweis.** Die richtige Quelle ist kein Nachweis:
  der vertikale 5-lx-Wert (§4.1.2 h/i) wird weiterhin nicht gerechnet, ebenso
  wenig der Arbeitsflächen-Wert (§4.4.1). `nachweis_offen` bleibt gesetzt, die
  Prüfregeln 12/12b bleiben nötig.
* **Keine Freischaltung.** `engine_status` der acht Matrix-Regeln bleibt
  `input_fehlt`, bis er je Regel einzeln mit Nachweis gezogen wird.
* **Nichts an `flaechen_schwellen`** — eigener Strang (Scope-Gate, PR #87-Kommentar).
