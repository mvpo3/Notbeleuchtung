"""sonderstellen_strategy — Pflicht-Leuchten an Sonderstellen (EN 1838 §4.1.2).

Konsumiert `RaumModell.sonderstellen` (Contract v1.1.0, Option A nach
docs/SPEC_SONDERSTELLEN_CONTRACT.md) + die Raum-Flags `ist_barrierefrei` (§4.3.8)
und `besondere_gefaehrdung` (§4.4.1). Eine generische Abstandslogik für alle
Typen: die Leuchte sitzt DIREKT an der Stelle (`xy_mm`) — damit ist die
Norm-Anforderung „nahe" (ANMERKUNG: ≤ 2 m horizontal) konstruktiv erfüllt,
ohne einen Abstands-Parameter zu raten. Für `niveauaenderung` kommt ein
Rettungszeichen nur bei expliziter LB-Vorgabe dazu (RZ-06; `richtung="gerade"` =
beidseitig, weil die Reiserichtung an einem Niveausprung nicht aus der Stelle
selbst folgt).

Norm-Parameter (Symbol, Höhe, Quelle) kommen wie beim Flächen-Trigger aus Enis'
Referenz-Regeln im Regelwerk-Snapshot — Leonis fabriziert keine Norm-Werte.
Fehlt eine Referenz-Regel, wird der Typ übersprungen (nicht geraten).

**Korrekturen 05.09.2026 (Enis, Nachzug zu #103 — bitte @mvpo3 reviewen):**

* **§4.3.8 gilt nur für Toiletten.** Wortlaut (Norm-S.11, am Original geprüft):
  „Antipanikbeleuchtung ist in **Toiletten** für Menschen mit Behinderung
  erforderlich." Auslöser ist die barrierefreie **Toilette**, nicht das Flag
  `ist_barrierefrei` allein — ein barrierefreies Zimmer löst §4.3.8 nicht aus.
* **Kein automatisches Rettungszeichen an einer Niveauänderung.** Die Einleitung
  von §4.1.2 (Norm-S.8) verlangt an den aufgezählten Stellen
  **Sicherheitsleuchten**; d) verlangt nur, dass **vorhandene** Sicherheitszeichen
  beleuchtet werden, und begründet keine neue Zeichenpflicht. Ein RZ entsteht nur
  aus einer expliziten LB-Vorgabe (`LBVorgabe.rz_stellen`) — dann trägt es
  `lb_quelle` statt `norm_quelle` (Muster: `lb_override`).

Bewusst NICHT hier: der 5-lx-vertikal-Nachweis (§4.1.2 h/i). Der Wert ist
vertikal am Gerät, `lux_raster` rechnet horizontal am Boden — ein Einsetzen wäre
der Kategorienfehler aus Enis' Befund. Die Stellen bleiben MANUELL_PRUEFEN
(Spec §3), die Leuchte wird trotzdem gesetzt (Pflichtstelle).

Ohne Sonderstellen und ohne gesetzte Flags ist dieses Modul ein No-op —
bestehende Pläne bleiben bit-identisch.
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import (
    LBVorgabe,
    NormProvider,
    Platzierung,
    RaumModell,
)

from .communal_stgh_strategy import _AGV_SV_F, _building_assigner
from .flaechen_strategy import _WC_TYPEN
from .geometry import find_center_visual

#: Raumtypen, die als „Toilette" im Sinne von §4.3.8 gelten. Bewusst dieselbe
#: WC/Sanitär-Liste wie beim Flächen-Trigger (`flaechen_strategy._WC_TYPEN`) plus
#: die ausgeschriebene Form — keine zweite Vokabular-Wahrheit. Eine engere Lesart
#: (nur WC/TOILETTE, ohne BAD/DUSCHE/NASSRAUM) ist vertretbar; sie zu wählen ist
#: eine Auslegungsentscheidung und gehört ins Review, nicht in einen stillen Fix.
_TOILETTEN_TYPEN = _WC_TYPEN | {"TOILETTE"}

#: LB-Schlüssel, der ein Rettungszeichen an Niveauänderungen anfordert
#: (`LBVorgabe.rz_stellen`, Literal `RzStelle`).
_LB_RZ_NIVEAUAENDERUNG = "niveauaenderung"


def _referenz(norm: NormProvider, klassifikation: str):
    """Erste Regelwerk-Anforderung der Klassifikation mit Symbol — oder None.

    ⚠️ FALLBACK (Enis-Review #95): die zurückgegebene `quelle` ist die der
    Referenz-Regel (§4.1/§4.2.1/§4.3.1) — NICHT der echte Auslöser der
    Pflichtstelle (§4.1.2 c/h/i bzw. §4.3.8/§4.4.1). Die Naht-Invariante
    `norm_quelle ∈ NormRegelwerk.quellen` lässt die echten Fundstellen heute
    nicht zu; Enis liefert Referenz-Anforderungen je Sonderstellen-Typ nach
    (eigener 3-Owner-PR). Bis dahin: Audit-Trail als Näherung lesen — der
    Pipeline-Summary trägt einen entsprechenden `hinweise`-Eintrag."""
    for regel in norm.regelwerk_snapshot().regeln:
        anf = regel.anforderung
        if anf.klassifikation == klassifikation and anf.symbol_katalog_keys:
            return anf
    return None


def _assigner(raum: RaumModell, extra_xs: list[float]):
    """Stromkreis-Bauteil A|B — dieselbe x-Cluster-Regel wie RZ/Flächen-Leuchten."""
    xs = [
        find_center_visual(r.polygon_mm)[0] for r in raum.raeume if r.polygon_mm
    ] + extra_xs
    return _building_assigner(xs)


def _leuchte(xy, anf, kind: str, building: str, lb_quelle: str = "") -> Platzierung:
    """Eine Pflicht-Leuchte an der Stelle.

    `lb_quelle` gesetzt = die Leuchte kommt aus einer expliziten LB-Vorgabe, nicht
    aus der Norm. Dann bleibt `norm_quelle` leer — dasselbe Muster wie in
    `lb_override`: keine Norm behaupten, wo keine ist.
    """
    return Platzierung(
        xy_mm=(xy[0], xy[1]),
        catalog_key=anf.symbol_katalog_keys[0],
        rotation_deg=0.0,
        height_mm=float(anf.montagehoehe_mm),
        kind=kind,
        richtung="gerade",
        circuit_hint=f"AGV-{building}-F{_AGV_SV_F}",
        covers_segment=[],
        norm_quelle="" if lb_quelle else anf.quelle,
        lb_quelle=lb_quelle,
    )


def _lb_fordert_rz_an_niveauaenderung(lb: LBVorgabe | None) -> str:
    """LB-Provenienz, falls die LB an Niveauänderungen ein RZ fordert — sonst "".

    Fail closed in beide Richtungen: ohne LB und ohne passenden Eintrag entsteht
    kein Rettungszeichen; mit Eintrag entsteht es mit ehrlicher LB-Quelle.
    """
    if lb is None or _LB_RZ_NIVEAUAENDERUNG not in (lb.rz_stellen or []):
        return ""
    return lb.lb_quelle or f"LB rz_stellen={_LB_RZ_NIVEAUAENDERUNG}"


def plan_sonderstellen(
    raum: RaumModell, norm: NormProvider, lb: LBVorgabe | None = None
) -> list[Platzierung]:
    """Je Sonderstelle eine Sicherheitsleuchte an der Stelle selbst (§4.1.2).

    Ein zusätzliches Rettungszeichen an einer `niveauaenderung` entsteht **nur**,
    wenn die LB es fordert (`rz_stellen` enthält `niveauaenderung`) — §4.1.2 c)
    belegt an dieser Stelle die Leuchte, nicht das Zeichen. Das RZ trägt dann
    `lb_quelle` und keine Norm-Quelle.
    """
    if not raum.sonderstellen:
        return []
    sl_ref = _referenz(norm, "sicherheitsleuchte")
    rz_ref = _referenz(norm, "rz")
    rz_lb_quelle = _lb_fordert_rz_an_niveauaenderung(lb)
    assign_building = _assigner(raum, [s.xy_mm[0] for s in raum.sonderstellen])

    out: list[Platzierung] = []
    for stelle in raum.sonderstellen:
        building = assign_building(stelle.xy_mm[0])
        if sl_ref is not None:
            out.append(_leuchte(stelle.xy_mm, sl_ref, "sicherheitsleuchte", building))
        if stelle.typ == "niveauaenderung" and rz_ref is not None and rz_lb_quelle:
            out.append(
                _leuchte(stelle.xy_mm, rz_ref, "rz", building, lb_quelle=rz_lb_quelle)
            )
    return out


def plan_flag_raeume(raum: RaumModell, norm: NormProvider) -> list[Platzierung]:
    """Raum-Flags mit Norm-Folge, je eine Leuchte am visuellen Zentrum:

    * `ist_barrierefrei` (§4.3.8) → Antipanik-Pflicht **nur in Toiletten**
      (`_TOILETTEN_TYPEN`): die Norm nennt „Toiletten für Menschen mit
      Behinderung", nicht „barrierefreie Räume". Ein barrierefreies Zimmer löst
      §4.3.8 nicht aus — was es an anderen Anforderungen braucht (Raumtyp-Regel,
      Fluchtweg, Flächen-Trigger), bleibt davon unberührt und kommt aus den
      anderen Strategien. Ist der Raum ohnehin antipanik-klassifiziert, macht
      `flaechen_strategy` die Arbeit → hier übersprungen (keine Doppelung).
    * `besondere_gefaehrdung` (§4.4.1) → Sicherheitsleuchte; der erhöhte
      Lux-Anspruch (`arbeitsplatz_lux`, 10 %/min. 15 lx) ist im Regelwerk noch
      ungefüllt → Stelle bleibt MANUELL_PRUEFEN, die Leuchte steht trotzdem.
    """
    flagged = [
        r for r in raum.raeume
        if r.polygon_mm and (r.ist_barrierefrei or r.besondere_gefaehrdung)
    ]
    if not flagged:
        return []
    ap_ref = _referenz(norm, "antipanik")
    sl_ref = _referenz(norm, "sicherheitsleuchte")
    assign_building = _assigner(raum, [])

    out: list[Platzierung] = []
    for r in flagged:
        center = find_center_visual(r.polygon_mm)
        building = assign_building(center[0])
        anf = norm.fuer_raum(r.raum_typ, r.ist_fluchtweg)
        if (
            r.ist_barrierefrei
            and r.raum_typ.upper() in _TOILETTEN_TYPEN
            and ap_ref is not None
            and anf.klassifikation != "antipanik"
        ):
            out.append(_leuchte(center, ap_ref, "antipanik", building))
        if (
            r.besondere_gefaehrdung
            and sl_ref is not None
            and anf.klassifikation != "sicherheitsleuchte"
        ):
            out.append(_leuchte(center, sl_ref, "sicherheitsleuchte", building))
    return out
