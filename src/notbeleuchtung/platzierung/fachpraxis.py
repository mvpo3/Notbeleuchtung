"""fachpraxis — Praxis-Regeln des Owners (weder Norm- noch LB-Wissen).

Slice 2.3 (MEGA-Prompt 2026-09-07). Werte sind bewusst KEIN YAML in
`normwissen/` — sie stammen aus der Planungspraxis des Owners, nicht aus
EN 1838/ÖNorm. Stellt sich später heraus, dass ein Wert in einer LB stehen
kann, wandert er in den LB-explizit-Pfad (Entscheidungs-Hierarchie).

Mess-Protokoll (docs/analyse/mollgasse_ug_notbeleuchtung.md, Abschlussreport):
- Regel A („Tür-RZ-unten → Pfeil links") wurde nach Messung VERWORFEN
  (Gate G3, Owner-Entscheid in-Session): Mollgasse-GU 5/41 links, die
  Owner-korrigierte wohnbau_v7-Datei bestätigt #111 (Pfeil rotiert ZUR Tür).
- Regel B (Aufheller 500 mm) in Lesart **B1** gebaut (Gate G4, Owner-Entscheid
  in-Session auf Owner-Wort): die GU-Pläne kennen keinen Aufheller-Typ, die
  Messung konnte B1/B2 nicht entscheiden — Quelle ist die Owner-Ansage
  („Aufheller 500 mm neben dem RZ"), nicht die Empirie.
  Owner-Nachtrag 2026-09-09: das **Tür-RZ** der Pflichträume (TECHNIK/MUELL/
  KINDERWAGEN) ist vom Aufheller **ausgenommen** — es sitzt an der Tür, das
  Rauminnere trägt die mittige Zusatzleuchte; ein Aufheller dahinter wäre doppelt.

Audit-Trail: `norm_quelle = "fachpraxis: aufheller-500mm"` (die Naht-Invariante
prüft Quellen nur auf der Golden-Fixture; ein eigenes `decision_source`-Feld
wäre ein 3-Owner-Contract-Slice → handoff(contracts) im Report).
"""
from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass

from notbeleuchtung.hauptengine.contracts import (
    FluchtwegSegment,
    NormProvider,
    Platzierung,
    RaumModell,
)

from .bausteine import AGV_SV_F as _AGV_SV_F
from .bausteine import KORRIDOR_TYPEN as _KORRIDOR_TYPEN
from .bausteine import RZ_INS_RAUM_MM as _RZ_INS_RAUM_MM
from .bausteine import building_assigner as _building_assigner
from .bausteine import ist_echte_tuer as _ist_echte_tuer
from .bausteine import rotation_piktogramm_in_raum as _rotation_piktogramm_in_raum
from .bausteine import rotation_zur_tuer as _rotation_zur_tuer
from .bausteine import select_key as _select_key
from .geometry import (
    _bbox,
    _bbox_area,
    _relocate_outside_exclusions,
    find_center_visual,
    point_in_polygon,
)
from .lux import lux_punkte, wartungsfaktor_aus_norm

AUFHELLER_KEY = "sicherheitsleuchte_aufheller"
QUELLE_AUFHELLER = "fachpraxis: aufheller-500mm"
# Owner-Korrektur 2026-09-10 (AutoCAD-Diff L-Demo): das Tür-RZ eines Nebenraums (Technik/
# Müll) sitzt nicht exakt auf der Schwelle, sondern leicht IM bedienten Raum (Richtung
# Raum-Inneres, weg vom Gang) — dort ist es klar dem Raum zugeordnet, nicht dem Gang.

#: Regel 2026-09-07: diese Raumtypen bekommen IMMER eine Sicherheitsleuchte an
#: der Tür — fensterlose Innen-/Nebenräume, bei Netzausfall muss die Tür
#: auffindbar bleiben. TECHNIK/MUELLRAUM sind kanonische Vokabular-Typen
#: (docs/VOKABULAR.md); KINDERWAGENRAUM ist der GEMEINSAME Kinderwagenraum im
#: Wohnbau (Owner-Wahl, Referenz-Praxis), NICHT der private Wohnungs-Abstellraum.
#: ⚠️ Naht Selman: raumerkennung/raumtyp.py ebnet `kinderwagen`→ABSTELLRAUM ein
#: (STORAGE), d.h. auf ECHTEN Plänen trägt ein Kinderwagenraum heute
#: `ABSTELLRAUM`, nicht `KINDERWAGENRAUM` — bis die Erkennung den Typ erhält,
#: greift diese Regel nur, wo der Plan den Literal `KINDERWAGENRAUM` führt
#: (docs/COORDINATION.md 2026-09-07).
#: Owner-Korrektur 2026-09-11 (AutoCAD-Diff Elektroplan DE, zwei Runden): erst
#: „Hier hast du es Vergessen" am Fahrradraum (communal ABSTELLRAUM), dann „Im
#: Spielraum gehört auch eine Notleuchte" (communal ZIMMER) → GENERALISIERT:
#: JEDER communal Nebenraum bekommt das Tür-RZ — außer Erschließungs-/Außen-/
#: Schacht-Flächen (`_TUERLEUCHTE_KEIN_COMMUNAL`). Private Räume (ist_communal=
#: False) bleiben draußen (Owner-Entscheid 2026-09-07 unverändert). VORRAUM ist
#: ausgenommen, weil die Erkennung private Wohnungs-Vorräume real mit
#: communal=True flaggt (Elektroplan DE raum_2/raum_5) — sonst „RZ in der Wohnung".
_TUERLEUCHTE_RAUMTYPEN = {"TECHNIK", "MUELLRAUM", "KINDERWAGENRAUM"}
_TUERLEUCHTE_KEIN_COMMUNAL = (
    _KORRIDOR_TYPEN
    | {"STIEGENHAUS", "VORRAUM", "AUFZUGSVORPLATZ", "LIFT", "SCHACHT", "BALKON", "TERRASSE"}
)
#: Symbol = din-AP3-Antipanikleuchte, die in der SICHERHEITSLEUCHTEN-Rolle als
#: Universal-Leuchte verwendet wird (Rolle ≠ Produkt) — die knowledge-gestützte
#: Darstellung der Raum-Sicherheitsbeleuchtung. KEIN Aufheller (Zusatz-/Fülllicht).
TUERLEUCHTE_KEY = "antipanik_leuchte"
#: Referenz-Praxis (Owner-Wahl „immer"): dokumentierte Regel SL-13 in
#: normwissen/data/platzierung_regeln.yaml (leuchtenart sicherheitsleuchte) +
#: INOTEC HB2026 (Technikräume 5 lx) + EN 1838:2025 §5.4 + reale Elektro-LB §5.1.23.
QUELLE_TUERLEUCHTE = (
    "Referenz-Praxis: Technik-/Nebenraum-SL an der Tür "
    "(INOTEC HB2026 · EN 1838:2025 §5.4 · Elektro-LB §5.1.23)"
)
#: Montagehöhe der mittigen Zusatzleuchte (über Boden; ≥ EN-1838-Mindesthöhe 2 m).
TUERLEUCHTE_HOEHE_MM = 2400.0
#: Erschließungs-Raumtypen — eine Tür DORTHIN ist die „Ausgangs"-Tür des Raums.
_ERSCHLIESSUNG = _KORRIDOR_TYPEN | {"STIEGENHAUS"}
#: Ab dieser Raumfläche ist die mittige Zusatzleuchte eine Antipanikleuchte (0,5 lx,
#: EN 1838 §4.3 Flächenbezug) statt eines Aufhellers (Füll-/Zusatzlicht). Owner 2026-09-08.
_ANTIPANIK_AB_M2 = 60.0
#: Fallback-Reichweite eines Tür-RZ, wenn die Norm keine Erkennungsweite (l=z·h) liefert.
_RZ_REICHWEITE_FALLBACK_MM = 15000.0
#: Konvexitäts-Schwelle (Polygon-Fläche / Bbox-Fläche). Darunter = L-Form mit potenziell
#: von der Tür aus VERDECKTER Ecke → mittige Zusatzleuchte auch unterhalb der Reichweite.
_KONVEX_MIN = 0.85


def _polygon_flaeche_m2(polygon: list[tuple[float, float]]) -> float:
    """Polygon-Fläche (Gauß/Shoelace) in m² — Fallback, wenn `Raum.flaeche_m2` fehlt."""
    if len(polygon) < 3:
        return 0.0
    s = sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(polygon, polygon[1:] + polygon[:1]))
    return abs(s) / 2.0 / 1_000_000.0


@dataclass(frozen=True)
class FachpraxisRegeln:
    """Konstanten der Owner-Praxis. Quelle: Leonis 07.09.2026 (G3/G4-Entscheide),
    Demo-Projekte + Mollgasse-UG-Referenz (Slice 4.1) als Mess-Kontext."""

    aufheller_abstand_mm: float = 500.0
    #: reserviert — Regel A (tuer_rz_richtung) nach Messung verworfen (G3).
    tuer_naehe_mm: float = 300.0


def _effektive_richtung_deg(p: Platzierung) -> float | None:
    """Weltwinkel des RZ-Pfeils (Basis→Spiegel→Rotation) — None ohne Richtungs-Block."""
    # Lazy-Import: hält den Modul-Import ezdxf-frei und zyklenfrei (bausteine
    # importiert symbols.orientation bereits — gleiche Grenze).
    from notbeleuchtung.symbols import load_symbol_mapping
    from notbeleuchtung.symbols.orientation import basis_deg

    entry = load_symbol_mapping().get(p.catalog_key) or {}
    basis = basis_deg(str(entry.get("block_name", "")))
    if basis is None:
        return None
    eff = (180.0 - basis) % 360.0 if p.mirror_x else basis
    return (eff + p.rotation_deg) % 360.0


def _in_einem_raum(raum: RaumModell, xy: tuple[float, float]) -> bool:
    return any(
        len(r.polygon_mm) >= 3 and point_in_polygon(xy, r.polygon_mm)
        for r in raum.raeume
    )


def _punkt_unterversorgt(xy, quellen, raum, norm, i_cd_fn) -> bool:
    """Liegt die Beleuchtungsstärke am Punkt `xy` UNTER der Norm-Schwelle?

    Rechnet die Beleuchtungsstärke aus den bereits platzierten Sicherheits-/
    Antipanikleuchten (Corridor-/Rundoptik über `i_cd_fn`) am Kandidatenpunkt —
    physik-identisch zu `deckung`/`lux`, inkl. Wartungsfaktor. Fehlt jede
    Lichtquelle, gilt der Punkt als unterversorgt (Aufheller nötig). Ohne
    passenden Raum-Kontext konservativ True (setzen).
    """
    r = next(
        (rr for rr in raum.raeume if len(rr.polygon_mm) >= 3 and point_in_polygon(xy, rr.polygon_mm)),
        None,
    )
    if r is None:
        return True
    if not quellen:
        return True
    anf = norm.fuer_raum(r.raum_typ, r.ist_fluchtweg)
    wf = wartungsfaktor_aus_norm(anf)
    res = lux_punkte(
        quellen, [xy], montagehoehe_m=anf.montagehoehe_mm / 1000.0, i_cd_fn=i_cd_fn,
        ziel_lux=anf.min_lux or 1.0, wartungsfaktor=wf,
    )
    return not res.erfuellt_min


def aufheller_je_rz(
    platzierungen: list[Platzierung],
    raum: RaumModell,
    norm: NormProvider | None = None,
    *,
    i_cd_fn: Callable[..., float] | None = None,
    regeln: FachpraxisRegeln | None = None,
) -> list[Platzierung]:
    """Regel B1 (lux-bedingt): je RZ ein Aufheller `aufheller_abstand_mm` hinter dem RZ —
    ABER nur, wenn die Stelle nicht schon von vorhandenen Sicherheitsleuchten
    ausgeleuchtet ist.

    „Hinter" = entgegen der effektiven Pfeilrichtung (weg vom Ausgang, Richtung
    Rauminneres — der Flüchtende kommt von dort und braucht das Licht VOR dem
    Zeichen). RZ ohne definierte Richtung (Doppelpfeil `gerade`, rotations-
    neutrale Symbole) bekommen keinen Aufheller. Liegt die Zielposition in
    keinem Raumpolygon, wird der Aufheller NICHT gesetzt (nie still außerhalb) —
    **fail-closed**: fehlen dem RaumModell die Polygone ganz (fragmentierte
    CAD-Familien liefern real leere `raeume`), ist die Kontur unbekannt und es
    wird KEIN Aufheller gesetzt, statt ihn ungeprüft ins Nichts zu platzieren.

    **Lux-Gate (Owner 2026-09-08):** mit `norm` UND echter Hersteller-Photometrie
    (`i_cd_fn`) wird der Kandidatenpunkt gegen die Norm-Beleuchtungsstärke
    (`anf.min_lux`) aus den schon platzierten Sicherheits-/Antipanikleuchten geprüft —
    deckt das vorhandene Licht ihn ab, entfällt der Aufheller (keine Überproduktion).
    Ohne `i_cd_fn` (keine LDT) bleibt es beim bedingungslosen Setzen — die konstante
    Lichtstärke-Annahme überschätzt die Deckung, ein stilles Weglassen wäre unsicher.
    """
    regeln = regeln or FachpraxisRegeln()
    quellen = [
        (q.xy_mm[0], q.xy_mm[1], q.rotation_deg)
        for q in platzierungen
        if q.kind in ("sicherheitsleuchte", "antipanik")
    ]
    out: list[Platzierung] = []
    for p in platzierungen:
        if p.kind != "rz":
            continue
        # Owner-Entscheid 2026-09-09: das Tür-RZ der TECHNIK/MUELL/KINDERWAGEN-Regel
        # (`tuerleuchte_pflichtraeume`) bekommt KEINEN Aufheller — es sitzt direkt an der
        # Tür, und das Rauminnere deckt die mittige Zusatzleuchte (Regel-Teil 2) ab. Ein
        # 500-mm-Aufheller dicht dahinter wäre redundant (sonst vom abstand_nachpass
        # ohnehin weggeräumt). Fluchtweg-RZ bleiben unberührt.
        if p.norm_quelle == QUELLE_TUERLEUCHTE:
            continue
        eff = _effektive_richtung_deg(p)
        if eff is None:
            continue
        winkel = math.radians(eff + 180.0)
        xy = (
            p.xy_mm[0] + regeln.aufheller_abstand_mm * math.cos(winkel),
            p.xy_mm[1] + regeln.aufheller_abstand_mm * math.sin(winkel),
        )
        # Fail-closed: ohne belegte Kontur (leere raeume ODER Position außerhalb
        # aller Polygone) kein Aufheller — Review-Befund 2026-09-07.
        if not _in_einem_raum(raum, xy):
            continue
        # Lux-Gate — NUR mit echter Hersteller-Photometrie (i_cd_fn): deckt das
        # vorhandene Licht den Punkt schon ab, entfällt der Aufheller. Ohne LDT
        # ist die konstante Lichtstärke-Annahme zu optimistisch (überschätzt die
        # Deckung) → dann konservativ bedingungslos setzen (kein stilles Weglassen).
        if norm is not None and i_cd_fn is not None and not _punkt_unterversorgt(
            xy, quellen, raum, norm, i_cd_fn
        ):
            continue
        out.append(
            Platzierung(
                xy_mm=xy,
                catalog_key=AUFHELLER_KEY,
                rotation_deg=0.0,
                mirror_x=False,
                height_mm=p.height_mm,
                kind="sicherheitsleuchte",
                richtung="gerade",
                circuit_hint=p.circuit_hint,
                covers_segment=[],
                norm_quelle=QUELLE_AUFHELLER,
            )
        )
    return out


# Tür-Echtheit: EINE Quelle in bausteine (ist_echte_tuer) — Elektroplan-DE-Befund
# „6064-mm-durchgang_12 = Wand mit Erkennungsloch" (Owner 2026-09-12).


def _tuer_des_raums(raum: RaumModell, r):
    """Die (Haupt-)Tür eines Raums oder None.

    Reihenfolge: bevorzugt eine Tür, die in einen Erschließungsraum (GANG/Flur/
    Stiegenhaus) führt — das ist die „Ausgangs"-Tür; sonst die erste referenzierte
    Tür; sonst geometrisch die dem Raum-Zentrum nächste Tür, die im Raumpolygon
    liegt. Fehlt jede Tür-Information, None (der Aufrufer platziert dann nichts —
    fail-closed, keine Leuchte an geratener Stelle). Phantom-Öffnungen
    (`_ist_echte_tuer`) sind von vornherein raus.
    """
    typen = {x.id: (x.raum_typ or "").upper() for x in raum.raeume}
    referenziert = [t for t in raum.tueren
                    if r.id in (t.von_raum, t.nach_raum) and _ist_echte_tuer(t)]
    if referenziert:
        def _zielraum(t):
            return t.nach_raum if t.von_raum == r.id else t.von_raum
        erschliessung = [
            t for t in referenziert
            if typen.get(_zielraum(t) or "", "") in _ERSCHLIESSUNG
        ]
        return (erschliessung or referenziert)[0]
    if len(r.polygon_mm) >= 3:
        drin = [t for t in raum.tueren
                if _ist_echte_tuer(t) and point_in_polygon(t.xy_mm, r.polygon_mm)]
        if drin:
            cx, cy = find_center_visual(r.polygon_mm)
            return min(drin, key=lambda t: (t.xy_mm[0] - cx) ** 2 + (t.xy_mm[1] - cy) ** 2)
    return None


def tuerleuchte_pflichtraeume(raum: RaumModell, norm: NormProvider) -> list[Platzierung]:
    """Referenz-Praxis (Owner 2026-09-08): TECHNIK/MUELLRAUM/KINDERWAGENRAUM bekommen
    IMMER ein **Rettungszeichen an der Tür** — der „Pfeil nach unten"-Block, rotiert
    sodass der Pfeil physisch ZUR Tür zeigt (bei Netzausfall muss die Tür auffindbar
    bleiben; diese fensterlosen Neben-/Innenräume liegen meist nicht auf dem erkannten
    Fluchtweg, deshalb setzt die Regel das RZ explizit).

    Reicht ein Tür-RZ nicht — geht jemand tief in den Raum oder in eine von der Tür
    aus verdeckte Ecke, ist bei Netzausfall dort kein Notlicht sichtbar (Panikgefahr) —
    kommt zusätzlich MITTIG eine Zusatzleuchte. „Reicht nicht" =: der weiteste Raumpunkt
    liegt weiter als die RZ-Erkennungsweite (l=z·h) von der Tür, ODER der Raum ist
    nicht-konvex (L-Form, Fläche/Bbox < `_KONVEX_MIN` → mögliche verdeckte Ecke). Die
    Zusatzleuchte ist ein Aufheller (< `_ANTIPANIK_AB_M2`) bzw. eine Antipanikleuchte
    (≥ `_ANTIPANIK_AB_M2`, 0,5-lx-Fläche EN 1838 §4.3) — je nach Raumgröße.

    Trägt der Raum keine bestimmbare Tür, wird nichts gesetzt (fail-closed — keine
    Leuchte an geratener Stelle). RZ-Symbol/-Höhe kommen aus der Norm
    (`fuer_fluchtweg_abschnitt`); die Provenienz `QUELLE_TUERLEUCHTE` markiert, dass die
    PLATZIERUNG Referenz-Praxis ist (die Norm mandatiert sie in diesen Räumen nicht).
    """
    pflicht = [
        r for r in raum.raeume
        if (r.raum_typ or "").upper() in _TUERLEUCHTE_RAUMTYPEN
        or (r.ist_communal and (r.raum_typ or "").upper() not in _TUERLEUCHTE_KEIN_COMMUNAL)
    ]
    if not pflicht:
        return []
    assign_building = _building_assigner(
        [find_center_visual(r.polygon_mm)[0] for r in raum.raeume if len(r.polygon_mm) >= 3]
    )
    out: list[Platzierung] = []
    for r in pflicht:
        tuer = _tuer_des_raums(raum, r)
        if tuer is None:
            continue
        tx, ty = tuer.xy_mm
        kreis = f"AGV-{assign_building(tx)}-F{_AGV_SV_F}"
        hat_polygon = len(r.polygon_mm) >= 3
        zentrum = find_center_visual(r.polygon_mm) if hat_polygon else (tx, ty - 1.0)

        # 1) RZ an der Tür — Pfeil-unten-Block, Piktogramm blickt INS Rauminnere
        #    (R-B, Owner-Fachdoku v2 — ersetzt Pfeil-zur-Tür an Tür-RZ).
        anf = norm.fuer_fluchtweg_abschnitt(
            FluchtwegSegment(segment_id=f"tuerleuchte_{r.id}", polyline_mm=[(tx, ty)], reason="exit")
        )
        rz_key, _ = _select_key(anf.symbol_katalog_keys, "unten")
        dx, dy = tx - zentrum[0], ty - zentrum[1]
        if math.hypot(dx, dy) < 50.0:
            dx, dy = 0.0, -1.0
        rot = _rotation_piktogramm_in_raum(dx, dy)
        # Owner-Korrektur: RZ ~150 mm ins Raum-Innere versetzen (Richtung Zentrum = weg
        # vom Gang). (dx, dy) zeigt vom Zentrum zur Tür (raus) → −Einheitsvektor = rein.
        _n = math.hypot(dx, dy) or 1.0
        rz_xy = (tx - dx / _n * _RZ_INS_RAUM_MM, ty - dy / _n * _RZ_INS_RAUM_MM)
        out.append(
            Platzierung(
                xy_mm=rz_xy,
                catalog_key=rz_key,
                rotation_deg=rot,
                mirror_x=False,
                height_mm=float(anf.montagehoehe_mm),
                kind="rz",
                richtung="unten",
                circuit_hint=kreis,
                covers_segment=[],
                norm_quelle=QUELLE_TUERLEUCHTE,
            )
        )

        # 2) Mittige Zusatzleuchte, wenn 1 Tür-RZ den Raum nicht abdeckt.
        if not hat_polygon:
            continue
        reichweite = (anf.erkennungsweite_m or 0.0) * 1000.0 or _RZ_REICHWEITE_FALLBACK_MM
        weitester = max(math.hypot(px - tx, py - ty) for (px, py) in r.polygon_mm)
        flaeche = r.flaeche_m2 or _polygon_flaeche_m2(r.polygon_mm)
        bbox_m2 = _bbox_area(_bbox(r.polygon_mm)) / 1_000_000.0
        nicht_konvex = bbox_m2 > 0 and (flaeche / bbox_m2) < _KONVEX_MIN
        if weitester <= reichweite and not nicht_konvex:
            continue
        antipanik = flaeche >= _ANTIPANIK_AB_M2
        out.append(
            Platzierung(
                xy_mm=zentrum,
                catalog_key=TUERLEUCHTE_KEY if antipanik else AUFHELLER_KEY,
                rotation_deg=0.0,
                mirror_x=False,
                height_mm=TUERLEUCHTE_HOEHE_MM,
                kind="antipanik" if antipanik else "sicherheitsleuchte",
                richtung="gerade",
                circuit_hint=kreis,
                covers_segment=[],
                norm_quelle=QUELLE_TUERLEUCHTE,
            )
        )
    return out


#: R2 (Owner-Korrektur 2026-09-11, AutoCAD-Diff Elektroplan DE): max. Abstand, in dem ein
#: bereits modellierter Ausgang die AUSSEN-Tür „abdeckt" (dann setzt der Anker-Pfad das
#: Exit-RZ, keine Dublette hier).
_AUSSEN_TUER_AUSGANG_MM = 2000.0


def aussen_tuer_rz(raum: RaumModell, norm: NormProvider) -> list[Platzierung]:
    """R2 (Owner-Korrektur 2026-09-11, „Hier ist der Ausgang vom Müllraum"): eine Tür
    von einem COMMUNAL Raum nach AUSSEN ist ein Notausgang und trägt ein Rettungszeichen
    (EN 1838 §4.1.2 g) — Pfeil DURCH die Tür nach draußen, ~150 mm im Raum-Inneren
    (gleiches Muster wie das Tür-RZ der Pflichträume).

    Bewusst NUR communal (Müll-/Fahrrad-/Technikraum-Außentüren): Balkon-/Terrassentüren
    privater Räume sind KEINE Notausgänge. Türen mit `tuer_detail="hauseingang"` und
    Türen, die ein modellierter Ausgang schon abdeckt, überspringt die Regel (der
    Anker-Pfad setzt dort das Exit-RZ)."""
    kandidaten = []
    for t in raum.tueren:
        seiten = {t.von_raum, t.nach_raum}
        if "AUSSEN" not in seiten or getattr(t, "tuer_detail", None) == "hauseingang":
            continue
        innen_id = next((s for s in (t.von_raum, t.nach_raum) if s != "AUSSEN"), None)
        r = next((x for x in raum.raeume if x.id == innen_id), None)
        if r is None or not r.ist_communal or len(r.polygon_mm) < 3:
            continue
        if any(
            math.hypot(a.xy_mm[0] - t.xy_mm[0], a.xy_mm[1] - t.xy_mm[1]) <= _AUSSEN_TUER_AUSGANG_MM
            for a in raum.ausgaenge
        ):
            continue
        kandidaten.append((t, r))
    if not kandidaten:
        return []
    assign_building = _building_assigner(
        [find_center_visual(r.polygon_mm)[0] for r in raum.raeume if len(r.polygon_mm) >= 3]
    )
    out: list[Platzierung] = []
    for t, r in kandidaten:
        tx, ty = t.xy_mm
        zentrum = find_center_visual(r.polygon_mm)
        dx, dy = tx - zentrum[0], ty - zentrum[1]     # Raum-Inneres → Tür = Fluchtrichtung raus
        if math.hypot(dx, dy) < 50.0:
            continue                                   # fail-closed: Richtung unbestimmbar
        anf = norm.fuer_fluchtweg_abschnitt(
            FluchtwegSegment(segment_id=f"aussen_tuer_{t.id}", polyline_mm=[(tx, ty)], reason="exit")
        )
        rz_key, _ = _select_key(anf.symbol_katalog_keys, "unten")
        _n = math.hypot(dx, dy)
        out.append(
            Platzierung(
                xy_mm=(tx - dx / _n * _RZ_INS_RAUM_MM, ty - dy / _n * _RZ_INS_RAUM_MM),
                catalog_key=rz_key,
                rotation_deg=_rotation_piktogramm_in_raum(dx, dy),
                mirror_x=False,
                height_mm=float(anf.montagehoehe_mm),
                kind="rz",
                richtung="unten",
                circuit_hint=f"AGV-{assign_building(tx)}-F{_AGV_SV_F}",
                covers_segment=[],
                norm_quelle=anf.quelle,
            )
        )
    return out


#: R4 (Owner-Korrektur 2026-09-11): Suchradien des Hauseingang-Pfeil-Nachpasses.
_HAUSEINGANG_RZ_MM = 1500.0     # RZ gilt als „an der Tür", wenn näher als das
_HAUSEINGANG_EXIT_MM = 3500.0   # nächster modellierter Ausgang = Fluchtziel-Referenz


def pfeil_durch_hauseingang(
    platzierungen: list[Platzierung], raum: RaumModell
) -> list[Platzierung]:
    """R4 (Owner-Korrektur 2026-09-11, „Pfeil zeigt Richtung Ausgang, nicht wohin die
    Tür aufgeht"): das RZ an einer Tür mit `tuer_detail="hauseingang"` zeigt in
    FLUCHTRICHTUNG durch die Tür nach draußen — nie in die Aufschlagrichtung.

    Rotations-Nachpass: Fluchtrichtung = Vektor zum nächsten modellierten Ausgang
    (primär), sonst Tür-Position minus RZ-Position (durch die Tür). Nur Pfeil-unten-
    Basis-RZ (Rotation trägt die Richtung); Tür-RZ der Pflichträume bleiben unberührt."""
    eingaenge = [t for t in raum.tueren if getattr(t, "tuer_detail", None) == "hauseingang"]
    if not eingaenge:
        return platzierungen
    out: list[Platzierung] = []
    for p in platzierungen:
        if p.kind != "rz" or p.richtung != "unten" or p.norm_quelle == QUELLE_TUERLEUCHTE:
            out.append(p)
            continue
        tuer = min(
            eingaenge,
            key=lambda t: math.hypot(t.xy_mm[0] - p.xy_mm[0], t.xy_mm[1] - p.xy_mm[1]),
        )
        if math.hypot(tuer.xy_mm[0] - p.xy_mm[0], tuer.xy_mm[1] - p.xy_mm[1]) > _HAUSEINGANG_RZ_MM:
            out.append(p)
            continue
        exits = [
            a for a in raum.ausgaenge
            if math.hypot(a.xy_mm[0] - tuer.xy_mm[0], a.xy_mm[1] - tuer.xy_mm[1])
            <= _HAUSEINGANG_EXIT_MM
        ]
        if exits:
            ziel = min(
                exits,
                key=lambda a: math.hypot(a.xy_mm[0] - tuer.xy_mm[0], a.xy_mm[1] - tuer.xy_mm[1]),
            )
            dx, dy = ziel.xy_mm[0] - p.xy_mm[0], ziel.xy_mm[1] - p.xy_mm[1]
        else:
            dx, dy = tuer.xy_mm[0] - p.xy_mm[0], tuer.xy_mm[1] - p.xy_mm[1]
        if math.hypot(dx, dy) < 50.0:
            out.append(p)
            continue
        out.append(p.model_copy(update={"rotation_deg": _rotation_piktogramm_in_raum(dx, dy)}))
    return out


#: R7 (Owner-Korrektur 2026-09-11, „RZ NICHT in der Wohnung"): Wohnungs-Vorraum-Heuristik.
_WOHNUNGS_VORRAUM_MAX_M2 = 6.0
_WOHNUNGS_VORRAUM_TYPEN = {"GANG", "VORRAUM"}


def entferne_wohnungs_vorraum_rz(
    platzierungen: list[Platzierung], raum: RaumModell
) -> list[Platzierung]:
    """R7 (Owner-Korrektur 2026-09-11, „RZ NICHT in der Wohnung"): die Erkennung flaggt
    kleine Wohnungs-Vorräume an der Stiege real als Fluchtweg-GANG (Stempel „GANG 2.75m2"
    IN der Wohnung) — dort landete ein Segment-RZ. Heuristik „privater Stiegen-Vorraum":
    kleiner GANG/VORRAUM (< 6 m²), der ans STIEGENHAUS grenzt und dessen übrige Türen
    ausschließlich zu PRIVATEN Räumen führen → alle RZ darin entfernen (außer Tür-RZ der
    Pflichträume und Räume mit Hauseingang/Ausgang — die sind echte Fluchtweg-Knoten)."""
    typen = {r.id: (r.raum_typ or "").upper() for r in raum.raeume}
    communal = {r.id: r.ist_communal for r in raum.raeume}

    def _ist_wohnungs_vorraum(r) -> bool:
        if (r.raum_typ or "").upper() not in _WOHNUNGS_VORRAUM_TYPEN or len(r.polygon_mm) < 3:
            return False
        if (r.flaeche_m2 or 0.0) >= _WOHNUNGS_VORRAUM_MAX_M2:
            return False
        if any(point_in_polygon(a.xy_mm, r.polygon_mm) for a in raum.ausgaenge):
            return False                                   # echter Ausgangs-Knoten
        stgh_tuer = False
        for t in raum.tueren:
            if r.id not in (t.von_raum, t.nach_raum):
                continue
            if getattr(t, "tuer_detail", None) == "hauseingang":
                return False                               # Hauseingang = Fluchtweg-Knoten
            andere = t.nach_raum if t.von_raum == r.id else t.von_raum
            if typen.get(andere or "") == "STIEGENHAUS":
                stgh_tuer = True
            elif communal.get(andere):
                return False                               # an communal Fläche angebunden
        return stgh_tuer

    vorraeume = [r for r in raum.raeume if _ist_wohnungs_vorraum(r)]
    if not vorraeume:
        return platzierungen
    return [
        p for p in platzierungen
        if p.kind != "rz"
        or p.norm_quelle == QUELLE_TUERLEUCHTE
        or not any(point_in_polygon(p.xy_mm, r.polygon_mm) for r in vorraeume)
    ]


#: R8 (Owner-Korrektur 2026-09-11): Radien des Stiegenhaus-RZ-Nachpasses.
_STGH_RZ_SUCHRADIUS_MM = 1500.0   # RZ gilt als „am Stiegen-Zugang"
_STGH_EXIT_RADIUS_MM = 2500.0     # stair_exit gehört zu diesem Stiegenhaus


def stiegenhaus_rz_nachpass(
    platzierungen: list[Platzierung], raum: RaumModell
) -> list[Platzierung]:
    """R8 (Owner-Korrektur 2026-09-11, „RZ im Stiegenhaus meistens an den Wänden, zeigt
    in die Richtung wie man in den Erdgeschoß kommt"): das RZ am Stiegen-Zugang gehört
    IN das Stiegenhaus, Pfeil in Abstiegs-Richtung — nicht davor in den Gang.

    Approximation (ohne Stiegenlauf-Geometrie im Contract): Position auf der Strecke
    stair_exit → Stiegenhaus-Zentrum (erster Probepunkt im Polygon), Rotation = Pfeil in
    diese Richtung. Nur Pfeil-unten-Basis-RZ nahe einem stair_exit; No-op ohne
    STIEGENHAUS-Raum oder stair_exit."""
    stghs = [
        r for r in raum.raeume
        if (r.raum_typ or "").upper() == "STIEGENHAUS" and len(r.polygon_mm) >= 3
    ]
    stair_exits = [a for a in raum.ausgaenge if a.typ == "stair_exit"]
    if not stghs or not stair_exits:
        return platzierungen
    out: list[Platzierung] = []
    for p in platzierungen:
        if p.kind != "rz" or p.richtung != "unten" or p.norm_quelle == QUELLE_TUERLEUCHTE:
            out.append(p)
            continue
        ex = min(
            stair_exits,
            key=lambda a: math.hypot(a.xy_mm[0] - p.xy_mm[0], a.xy_mm[1] - p.xy_mm[1]),
        )
        if math.hypot(ex.xy_mm[0] - p.xy_mm[0], ex.xy_mm[1] - p.xy_mm[1]) > _STGH_RZ_SUCHRADIUS_MM:
            out.append(p)
            continue
        stgh = min(
            stghs,
            key=lambda r: (find_center_visual(r.polygon_mm)[0] - ex.xy_mm[0]) ** 2
            + (find_center_visual(r.polygon_mm)[1] - ex.xy_mm[1]) ** 2,
        )
        cx, cy = find_center_visual(stgh.polygon_mm)
        if math.hypot(cx - ex.xy_mm[0], cy - ex.xy_mm[1]) > _STGH_EXIT_RADIUS_MM * 2:
            out.append(p)
            continue
        dx, dy = cx - ex.xy_mm[0], cy - ex.xy_mm[1]
        # Punkt 4: liefert die Erkennung Treppenläufe, ersetzt die ECHTE
        # Flucht-Gehrichtung (R-H) die Zentrum-Näherung.
        from .stgh_strategy import fluchtvektor as _fluchtvektor
        sh = next((s_ for s_ in raum.stiegenhaeuser if s_.raum_id == stgh.id), None)
        if sh is not None:
            fv = _fluchtvektor(sh)
            if fv is not None:
                dx, dy = fv[0] * 1000.0, fv[1] * 1000.0   # Einheitsvektor → mm-Skala
        if math.hypot(dx, dy) < 50.0:
            out.append(p)
            continue
        # erster Probepunkt Richtung Zentrum, der IM Stiegenhaus liegt (Wand-Nähe).
        ziel = None
        for t in (0.35, 0.5, 0.65, 0.8):
            probe = (ex.xy_mm[0] + dx * t, ex.xy_mm[1] + dy * t)
            if point_in_polygon(probe, stgh.polygon_mm):
                ziel = probe
                break
        if ziel is None:
            out.append(p)
            continue
        out.append(p.model_copy(update={
            "xy_mm": ziel,
            "rotation_deg": _rotation_zur_tuer(dx, dy),
        }))
    return out


#: D2 (BVH Fischamend 2026-09-13): Aufzugs-/Schacht-Polygone sind kein Montageort —
#: die Kabinen-Notbeleuchtung regelt die Aufzugsnorm (EN 81-20), nicht dieser Plan.
#: Real landete dort die STIEGENHAUS-Zentrum-SL (§4.1): der Liftschacht liegt im
#: Kern des Stiegenhaus-Polygons, `find_center_visual` fällt hinein (BT2 EG lift_1).
_SCHACHT_TYPEN = {"LIFT", "SCHACHT"}


def entferne_schacht_leuchten(
    platzierungen: list[Platzierung], raum: RaumModell
) -> list[Platzierung]:
    """D2-Guard: keine Platzierung im LIFT-/SCHACHT-Polygon.

    Liegt der Punkt zugleich in einem umgebenden Wirts-Raum (Lift im Stiegenhaus-
    Kern), wird er mit `_relocate_outside_exclusions` an den nächsten montierbaren
    Punkt DIESES Raums geschoben — die Leuchte gehört dem Wirts-Raum, sie darf
    nicht still verschwinden. Bei mehreren Wirten zählt der engste (kleinste
    Fläche). Liegt der Punkt NUR im Schacht, fällt die Platzierung (dort ist
    nichts montierbar). No-op ohne LIFT-/SCHACHT-Räume.
    """
    schaechte = [
        r for r in raum.raeume
        if (r.raum_typ or "").upper() in _SCHACHT_TYPEN and len(r.polygon_mm) >= 3
    ]
    if not schaechte:
        return platzierungen
    wirte = [
        r for r in raum.raeume
        if (r.raum_typ or "").upper() not in _SCHACHT_TYPEN and len(r.polygon_mm) >= 3
    ]
    out: list[Platzierung] = []
    for p in platzierungen:
        treffer = [s for s in schaechte if point_in_polygon(p.xy_mm, s.polygon_mm)]
        if not treffer:
            out.append(p)
            continue
        wirt = min(
            (r for r in wirte if point_in_polygon(p.xy_mm, r.polygon_mm)),
            key=lambda r: r.flaeche_m2 or _bbox_area(_bbox(r.polygon_mm)),
            default=None,
        )
        if wirt is None:
            continue                                   # nur im Schacht → entfällt
        andere = [q.xy_mm for q in platzierungen if q is not p]
        neu_xy = _relocate_outside_exclusions(
            p.xy_mm, wirt.polygon_mm, [s.polygon_mm for s in treffer], existing=andere
        )
        out.append(p if neu_xy == p.xy_mm else p.model_copy(update={"xy_mm": neu_xy}))
    return out
