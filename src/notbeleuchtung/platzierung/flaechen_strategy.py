"""flaechen_strategy — raum-bezogene Notbeleuchtung: Sicherheitsleuchten + Antipanik.

Ergänzt die RZ-Strategie (`communal_stgh_strategy`, Fluchtweg-Segmente) um die
flächigen Leuchten-Arten: Sicherheitsleuchten (Aufheller an Betonungspunkten,
EN 1838 §4.1) und Antipanik-Beleuchtung (offene Flächen, EN 1838 §4.3). Render-frei
— produziert ausschließlich Contract-B `Platzierung`.

Norm-getrieben (CLAUDE.md-Regel): OB ein Raum eine Leuchten-Art braucht, entscheidet
die Norm über `norm.fuer_raum(raum_typ, ist_fluchtweg)` (Fläche/Schwelle liegt in
Enis' Norm-Daten, nicht hier hartcodiert). Leonis entscheidet nur die GEOMETRIE:
1 Leuchte je qualifiziertem Raum am visuellen Zentrum (`find_center_visual` — bleibt
bei L-förmigen Räumen innen). Stromkreis A|B via derselben x-Cluster-Regel wie die RZ.
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import (
    NormProvider,
    OibBefund,
    Platzierung,
    RaumModell,
)

from .bausteine import AGV_SV_F as _AGV_SV_F
from .bausteine import building_assigner as _building_assigner
from .geometry import _bbox, find_center_visual, grid_points
from .kontext import LEER, PlatzierungsKontext
from .lux import lux_raster, ud_min_aus_norm
from .oib_gate import sanitaer_scope, verkehr_scope

# Sicherung gegen Überproduktion, falls der Lux-Nachweis nie hält (defekte Geometrie).
_ANTIPANIK_MAX_LEUCHTEN = 25
_ANTIPANIK_MAX_RUNDEN = 6

# WC/Sanitär-Raumtypen für den flächenbasierten Antipanik-Trigger (EN 1838 §4.3).
from .bausteine import WC_TYPEN as _WC_TYPEN


def _antipanik_referenz(norm: NormProvider):
    """Repräsentative Antipanik-Anforderung aus dem Norm-Regelwerk (0,5 lx, Symbol, Quelle).

    Wird gebraucht, wenn ein Raum NICHT über seinen Typ, sondern über die Fläche
    antipanik-pflichtig wird: die Antipanik-Parameter kommen dann aus Enis' eigener
    Antipanik-Regel (Leonis fabriziert keine Norm-Werte). `None`, falls das Regelwerk
    keine Antipanik-Regel kennt → dann wird nicht flächen-getriggert.
    """
    for regel in norm.regelwerk_snapshot().regeln:
        if regel.anforderung.klassifikation == "antipanik" and regel.anforderung.symbol_katalog_keys:
            return regel.anforderung
    return None


def _ist_sanitaer_schwelle(raum_typ: str, flaeche_m2: float, schwellen) -> bool:
    """OVE 718.560.9.001.AT **Punkt 1**: Sanitärbereich ab der 8-m²-Schwelle.

    (Der zweite Halbsatz von Punkt 1 — barrierefreie WC-Anlagen **ohne**
    Flächenmaß — ist keine Schwelle und gehört nicht hierher; er wird über
    `sonderstellen_strategy.plan_flag_raeume` / EN 1838 §4.3.8 bedient.)
    """
    wc = schwellen.wc_sanitaer_min_m2
    return wc is not None and raum_typ.upper() in _WC_TYPEN and flaeche_m2 >= wc


def _ist_verkehr_schwelle(flaeche_m2: float, schwellen) -> bool:
    """OVE 718.560.9.001.AT **Punkt 3**: 60-m²-Schwelle in Verkehrseinrichtungen.

    Die Flächenzahl allein reicht nicht — Punkt 3 nennt zusätzlich Raumkategorien
    (Wartezone, Abfertigungshalle, Geschäftsfläche, betriebsnotwendiger
    Arbeitsraum), die das RaumModell nicht führt. Solange `verkehr_scope` nie
    `anwendbar` liefert, ist das ohne Wirkung — die Prüfung steht hier, damit die
    beiden Schwellen sichtbar getrennt sind.
    """
    ap = schwellen.antipanik_min_m2
    return ap is not None and flaeche_m2 >= ap


def _flaechen_trigger_greift(
    raum_typ: str, flaeche_m2: float, schwellen, oib, floor: str, raum_id: str
) -> bool:
    """Löst einer der beiden OVE-Flächen-Trigger für DIESEN Raum aus?

    Jede Schwelle wird mit **ihrem eigenen** Geltungsbereich geprüft. `ungeklaert`
    platziert nicht — der Fall wird im Prüfbericht sichtbar gemacht (Regel 13),
    nicht still als erfüllt oder als nicht erforderlich behandelt.
    """
    if (
        sanitaer_scope(oib, floor, raum_id) == "anwendbar"
        and _ist_sanitaer_schwelle(raum_typ, flaeche_m2, schwellen)
    ):
        return True
    return (
        verkehr_scope(oib, floor, raum_id) == "anwendbar"
        and _ist_verkehr_schwelle(flaeche_m2, schwellen)
    )


def _antipanik_punkte(polygon: list, anf, i_cd_fn=None) -> list:
    """Antipanik-Raster, verdichtet bis der EN-1838-Nachweis (`anf.min_lux`, i.d.R.
    0,5 lx / Ud≥1:40) erfüllt ist — nicht nur `mindest_anzahl` blind gesetzt.

    Startet beim Norm-Raster (`mindest_anzahl`) und erhöht die Punktzahl, solange der
    Nachweis fehlt. Ist die Fläche kleiner als das EN-Nachweisfenster (Randstreifen),
    gibt es kein Raster → dann bleibt es beim Norm-Raster (nicht beweisbar, nicht raten).
    """
    n = max(1, anf.mindest_anzahl)
    bounds = _bbox(polygon)
    h_m = anf.montagehoehe_mm / 1000.0
    ud_min = ud_min_aus_norm(anf.gleichmaessigkeit_max)
    pts = grid_points(polygon, n)
    for _ in range(_ANTIPANIK_MAX_RUNDEN):
        res = lux_raster(
            pts, bounds, montagehoehe_m=h_m, i_cd_fn=i_cd_fn,
            ziel_lux=anf.min_lux, ud_min=ud_min,
        )
        if res.max_lux == 0.0:                       # kein Nachweisfenster (Fläche < Rand)
            return grid_points(polygon, max(1, anf.mindest_anzahl))
        if res.erfuellt_min and res.erfuellt_ud:
            break
        if len(pts) >= _ANTIPANIK_MAX_LEUCHTEN:
            break
        n = max(n + 1, int(n * 1.6))
        pts = grid_points(polygon, n)
    return pts


def _plan_raumleuchten(
    raum: RaumModell,
    norm: NormProvider,
    klassifikation: str,
    oib: OibBefund | None = None,
    i_cd_fn_je_key: dict | None = None,
) -> list[Platzierung]:
    """Je Raum mit passender Norm-Klassifikation Leuchten, geometrisch über die Fläche
    verteilt (`grid_points`): Sicherheitsleuchte → `mindest_anzahl` (Aufheller-Betonung);
    Antipanik → verdichtet bis zum EN-1838-Lux-Nachweis (`_antipanik_punkte`, §4.3).
    `kind` == `klassifikation` (Literale deckungsgleich: rz/sicherheitsleuchte/antipanik).
    Alle Leuchten eines Raums teilen dessen Stromkreis-Bauteil (A|B aus Zentroid-x)."""
    centroids = {
        r.id: find_center_visual(r.polygon_mm) for r in raum.raeume if r.polygon_mm
    }
    assign_building = _building_assigner([cx for cx, _ in centroids.values()])

    # Flächen-Trigger nur im Antipanik-Durchlauf. Die Schwellen sind
    # OVE-scope-gebunden (OVE E 8101:2019/2025 718.560.9.001.AT) und werden
    # **je Raum und je Schwelle getrennt** ausgewertet — Punkt 1 (8 m² Sanitär)
    # gilt für jede Nutzung mit erhöhten Anforderungen, Punkt 3 (60 m²) nur für
    # verkehrstechnische Einrichtungen. Ein bestätigter Verkaufsteil gibt Punkt 3
    # deshalb NICHT frei. Nur `anwendbar` platziert (fail closed).
    schwellen = norm.regelwerk_snapshot().flaechen_schwellen
    ap_referenz = _antipanik_referenz(norm) if klassifikation == "antipanik" else None

    out: list[Platzierung] = []
    for r in raum.raeume:
        if r.id not in centroids:
            continue
        anf = norm.fuer_raum(r.raum_typ, r.ist_fluchtweg)
        eff = anf
        getriggert = False
        if anf.klassifikation != klassifikation:
            # Zusatz-Trigger: darf nur ADDIEREN (Antipanik über Fläche), nie überschreiben.
            if ap_referenz is not None and _flaechen_trigger_greift(
                r.raum_typ, r.flaeche_m2, schwellen, oib, raum.floor, r.id
            ):
                eff = ap_referenz
                getriggert = True
            else:
                continue
        # Flächen-getriggerte Leuchten tragen die Schwellen-Quelle (OVE) im Audit-Trail,
        # sobald Enis sie liefert; bis dahin Fallback auf die Antipanik-Regel-Quelle
        # (hält die Naht-Invariante norm_quelle ∈ NormRegelwerk.quellen).
        quelle = (schwellen.quelle or eff.quelle) if getriggert else eff.quelle
        building = assign_building(centroids[r.id][0])
        # Nachweis mit der Photometrie der eingesetzten LEUCHTENFAMILIE (Katalog:
        # antipanik_leuchte = Rundlinse) statt pauschal isotrop/Corridor. Ohne
        # Zuordnung bleibt es bei der isotropen Annahme (wie bisher).
        familie_fn = (i_cd_fn_je_key or {}).get(eff.symbol_katalog_keys[0])
        punkte = (
            _antipanik_punkte(r.polygon_mm, eff, i_cd_fn=familie_fn)
            if klassifikation == "antipanik"
            else grid_points(r.polygon_mm, max(1, eff.mindest_anzahl))
        )
        for px, py in punkte:
            out.append(
                Platzierung(
                    xy_mm=(px, py),
                    catalog_key=eff.symbol_katalog_keys[0],
                    rotation_deg=0.0,
                    height_mm=float(eff.montagehoehe_mm),
                    kind=klassifikation,
                    richtung="gerade",
                    circuit_hint=f"AGV-{building}-F{_AGV_SV_F}",
                    covers_segment=[],
                    norm_quelle=quelle,
                )
            )
    return out


def plan_sicherheitsleuchten(raum: RaumModell, norm: NormProvider) -> list[Platzierung]:
    """Aufheller-Sicherheitsleuchten je Raum mit Norm-Klassifikation 'sicherheitsleuchte'."""
    return _plan_raumleuchten(raum, norm, "sicherheitsleuchte")


def plan_antipanik(
    raum: RaumModell,
    norm: NormProvider,
    oib: OibBefund | None = None,
    i_cd_fn_je_key: dict | None = None,
    *,
    kontext: PlatzierungsKontext | None = None,
) -> list[Platzierung]:
    """Antipanik-Leuchten je Raum mit Norm-Klassifikation 'antipanik' (offene Fläche).

    `oib` schaltet den zusätzlichen Flächen-Trigger frei (OVE-scope-gebunden, siehe
    `oib_gate`); ohne Befund bleibt es bei der reinen Typ-Klassifikation.
    `i_cd_fn_je_key` (catalog_key → Lichtstärke-Callable) lässt den 0,5-lx-Nachweis
    mit der Photometrie der tatsächlichen Leuchtenfamilie rechnen.
    """
    k = kontext or LEER
    return _plan_raumleuchten(
        raum, norm, "antipanik",
        oib=oib if oib is not None else k.oib,
        i_cd_fn_je_key=i_cd_fn_je_key if i_cd_fn_je_key is not None else dict(k.i_cd_fn_je_key),
    )
