"""platzierer — Leonis' echte Platzierungs-Logik (erfüllt das `Platzierer`-Port).

`NotlichtPlatzierer.place(raum, norm)` konsumiert Selmans `RaumModell` + Enis'
`NormProvider` und produziert das Contract-B `PlatzierungsErgebnis`. Er zeichnet
nichts (Render = Hauptengine) und importiert kein anderes Owner-Package.

Orchestriert den Fahrplan **Anker → Linie → Fläche → Deckung**:
* **RZ:** `anker_strategy` (graph-basiert, an Kreuzungen+Ausgängen) wenn der
  Zirkulationsgraph Kreuzungen hat (echter Graph); sonst Fallback auf die
  Segment-Strategie `communal_stgh_strategy` (dünnes 4OG-Fixture).
* **Sicherheitsleuchten + Antipanik:** raum-bezogen (`flaechen_strategy`).
* **Deckung:** Lux-getriebene Verdichtung der Korridore (`deckung`).
Alle Strategien sind norm-getrieben und render-frei.

**Photometrie (F2→F1-Naht):** `NotlichtPlatzierer(i_cd_fn=…)` nimmt optional ein
Lichtstärke-Callable `i_cd_fn(γ_grad) -> cd` — die richtungsabhängige Hersteller-
Photometrie (EULUMDAT/LDT). Die Hauptengine (`registry`) baut es aus
`normwissen.photometrie.Photometrie.intensitaet` und injiziert es beim Konstruieren;
`platzierung` bleibt so frei von `normwissen`-Imports (Owner-Grenze). Fehlt es, rechnet
die Deckung mit der konstanten isotropen Lichtstärke.
"""
from __future__ import annotations

from collections.abc import Callable
from itertools import pairwise

from notbeleuchtung.hauptengine.contracts import (
    FluchtwegSegment,
    LBVorgabe,
    NormProvider,
    OibBefund,
    Platzierung,
    PlatzierungsErgebnis,
    RaumModell,
)

from . import (
    abstand_nachpass,
    circuit_zuordnung,
    deckungs_zuordnung,
    fachpraxis,
    lb_override,
    mittellinie_snap,
    sichtkette,
    verbotszonen_nachpass,
)
from .anker_strategy import plan_rettungszeichen_anker
from .aussen_strategy import plan_aussenleuchten
from .bausteine import KORRIDOR_TYPEN as _KORRIDOR_TYPEN
from .communal_stgh_strategy import plan_rettungszeichen
from .deckung import garantiere_redundanz, verdichte_fluchtweg
from .flaechen_strategy import plan_antipanik, plan_sicherheitsleuchten
from .gang_strategy import plan_rettungszeichen_gang
from .geometry import point_in_polygon
from .graph import build_circulation_graph, kreuzungs_anker
from .kontext import PlatzierungsKontext
from .sonderstellen_strategy import plan_flag_raeume, plan_sonderstellen

# Ein Gang-Raum gilt erst ab dieser Länge (Bounding-Box-Längsseite) als eigener
# begehbarer Arm, der ein eigenes RZ braucht. Fragmentierte Erkennung (Mollgasse: 62
# spikey Teil-Polygone eines Gangs) erzeugt viele Klein-Fragmente — die würden sonst
# je einzeln aufgefüllt (Überproduktion). Ein echter Flur-Arm ist deutlich länger.
_MIN_KORRIDOR_ARM_MM = 6000.0
# Owner-Korrektur 2026-09-10 (12-m-Praxis-Sichtlinie), ERSETZT durch R-F (Fachdoku v2,
# S.7: „nicht nach festem Abstand … lückenlose Sichtkette"): die Lücken-Schwelle ist die
# Norm-Erkennungsweite l=z·h; dieser Wert ist nur noch der FALLBACK, wenn der Provider
# keine Erkennungsweite liefert.
_MAX_RZ_ARM_GAP_FALLBACK_MM = 12000.0


def _arm_gap_mm(norm: NormProvider) -> float:
    """Zwischen-RZ-Schwelle je Arm = Erkennungsweite l=z·h (R-F); Fallback 12 m."""
    try:
        weite = float(norm.erkennungsweite_m(0.15, True)) * 1000.0
    except Exception:
        return _MAX_RZ_ARM_GAP_FALLBACK_MM
    return weite if weite > 0.0 else _MAX_RZ_ARM_GAP_FALLBACK_MM


def _flucht_ziele(raum: RaumModell) -> list:
    """Richtungs-Ziele für Zwischen-RZ: Ausgänge, sonst Stiegenhaus-Zentren (1OG ohne
    eigenen Ausgang flieht über die Stiege)."""
    ziele = [a.xy_mm for a in raum.ausgaenge]
    if not ziele:
        from .geometry import find_center_visual
        ziele = [find_center_visual(r.polygon_mm) for r in raum.raeume
                 if (r.raum_typ or "").upper() == "STIEGENHAUS" and len(r.polygon_mm) >= 3]
    return ziele


def _mittel_arm_rz(rz: list, korridore: list, raum: RaumModell, norm: NormProvider) -> list:
    """Zwischen-RZ in langen Gang-Armen, deren End-RZ eine Lücke > Erkennungsweite
    lassen (R-F: Kette reißt erst jenseits l=z·h). Pfeil zeigt zum nächsten Fluchtziel."""
    import math

    from .bausteine import AGV_SV_F as _AGV_SV_F
    from .bausteine import key_und_rotation as _kr
    from .bausteine import richtung_und_rotation as _rr
    from .geometry import _bbox
    ziele = _flucht_ziele(raum)
    gap_mm = _arm_gap_mm(norm)
    zusatz: list = []
    for r in korridore:
        x0, y0, x1, y1 = _bbox(r.polygon_mm)
        laengs = 0 if (x1 - x0) >= (y1 - y0) else 1     # 0=x-Arm, 1=y-Arm
        lo, hi = (x0, x1) if laengs == 0 else (y0, y1)
        quer = (y0 + y1) / 2.0 if laengs == 0 else (x0 + x1) / 2.0
        if hi - lo < gap_mm:
            continue
        pos = sorted(p.xy_mm[laengs] for p in (rz + zusatz)
                     if point_in_polygon(p.xy_mm, r.polygon_mm))
        grenzen = [lo, *pos, hi]
        for a, b in pairwise(grenzen):
            if b - a <= gap_mm:
                continue
            mid = (a + b) / 2.0
            pt = (mid, quer) if laengs == 0 else (quer, mid)
            ziel = min(ziele, key=lambda z: math.hypot(z[0] - pt[0], z[1] - pt[1]), default=None)
            richtung, _ = _rr(ziel[0] - pt[0], ziel[1] - pt[1]) if ziel else ("unten", 0.0)
            seg = FluchtwegSegment(segment_id=f"sicht_{r.id}_{int(mid)}",
                                   polyline_mm=[pt], reason="long_run")
            anf = norm.fuer_fluchtweg_abschnitt(seg)
            key, rot, mirror = _kr(anf.symbol_katalog_keys, richtung)
            zusatz.append(Platzierung(
                xy_mm=pt, catalog_key=key, rotation_deg=rot, mirror_x=mirror,
                height_mm=float(anf.montagehoehe_mm), kind="rz", richtung=richtung,
                # vorläufiger F13-SV-Kreis; circuit_zuordnung vergibt final (F06-fest).
                circuit_hint=f"AGV-A-F{_AGV_SV_F}", covers_segment=[], norm_quelle=anf.quelle))
    return zusatz


def _sichtlinien_garantie(rz: list, raum: RaumModell, norm: NormProvider) -> list:
    """Owner-Regel 2026-09-09: aus jeder Wohnungstür muss beim Blick in den Gang ein
    Rettungszeichen sichtbar sein. Anker- und Segment-Pfad setzen RZ nur an Ausgängen/
    Kreuzungen — ein langer Gang-Arm ohne eigenen Entscheidungspunkt bleibt sonst
    RZ-los (nur Aufheller). Jeder **substanzielle** GANG-Raum (Längsseite ≥
    `_MIN_KORRIDOR_ARM_MM`), der KEIN RZ in seinem Polygon trägt, wird per
    GANG-Mittellinie aufgefüllt (Pfeil zum Fluchtziel, `plan_rettungszeichen_gang`).
    Gänge mit RZ und Klein-Fragmente (fragmentierte Erkennung) bleiben unberührt —
    keine Überproduktion."""
    def _arm_lang_genug(r) -> bool:
        xs = [p[0] for p in r.polygon_mm]
        ys = [p[1] for p in r.polygon_mm]
        return max(max(xs) - min(xs), max(ys) - min(ys)) >= _MIN_KORRIDOR_ARM_MM

    korridore = [
        r for r in raum.raeume
        if (r.raum_typ or "").upper() in _KORRIDOR_TYPEN
        and len(r.polygon_mm) >= 3 and _arm_lang_genug(r)
    ]
    unbedeckt = [
        r for r in korridore
        if not any(p.kind == "rz" and point_in_polygon(p.xy_mm, r.polygon_mm) for p in rz)
    ]
    if unbedeckt:
        unbedeckt_ids = {r.id for r in unbedeckt}
        gefuellt = list(rz) + [
            p for p in plan_rettungszeichen_gang(raum, norm)
            if any(r.id in unbedeckt_ids and point_in_polygon(p.xy_mm, r.polygon_mm)
                   for r in unbedeckt)
        ]
    else:
        gefuellt = list(rz)
    # R-F: Lücken > Erkennungsweite bekommen ein Zwischen-RZ …
    voll = gefuellt + _mittel_arm_rz(gefuellt, korridore, raum, norm)
    # … und die fertige Kette wird auf die lückenlose SICHTKETTE ausgedünnt
    # (Fachdoku v2: „Ist das nächste Zeichen bereits sichtbar, wird kein
    # weiteres gesetzt" — Ground truth EG: Gang-RZ 4→1).
    return sichtkette.kette_ausduennen(voll, raum, norm)


def _plan_rettungszeichen(raum: RaumModell, norm: NormProvider):
    """RZ-Strategie nach Verfügbarkeit des Fluchtweg-Wissens:

    1. **Anker** (Graph-Kreuzungen degree>=3) — echter Zirkulationsgraph (Selman).
    2. **Segment** — 1 RZ je Fluchtweg-Segment (dünnes 4OG-Fixture, faithful 5 RZ).
    3. **GANG-Fallback** — weder Kreuzung noch Segment (fremde CAD-Familie ohne
       erkannten Fluchtweg-Layer): RZ entlang der GANG-Mittelachsen, damit die
       Engine auch ohne Fluchtweg-Layer RZ setzt (fischamender-Bug B2).

    Danach die **Sichtlinien-Garantie**: RZ-lose Gang-Räume auffüllen (Owner-Regel,
    aus jeder Wohnungstür ein RZ sichtbar)."""
    if kreuzungs_anker(build_circulation_graph(raum)):
        primaer = plan_rettungszeichen_anker(raum, norm)
    else:
        segment_rz = plan_rettungszeichen(raum, norm)
        primaer = segment_rz if segment_rz else plan_rettungszeichen_gang(raum, norm)
    return _sichtlinien_garantie(primaer, raum, norm)


class NotlichtPlatzierer:
    """Erfüllt `hauptengine.contracts.ports.Platzierer`."""

    def __init__(
        self,
        i_cd_fn: Callable[[float], float] | None = None,
        i_cd_fn_je_key: dict[str, Callable[[float], float]] | None = None,
    ) -> None:
        # Richtungsabhängige Hersteller-Lichtstärke (aus F2-Photometrie); None = konstant.
        # `i_cd_fn` = Fluchtweg-Deckungs-Leuchte (Corridor-Optik); `i_cd_fn_je_key` =
        # catalog_key → Callable für Nachweise anderer Familien (Antipanik-Rundlinse).
        self._i_cd_fn = i_cd_fn
        self._i_cd_fn_je_key = i_cd_fn_je_key or {}

    def place(
        self,
        raum: RaumModell,
        norm: NormProvider,
        lb: LBVorgabe | None = None,
        *,
        oib: OibBefund | None = None,
        bestand_leuchten_mm: tuple[tuple[float, float], ...] = (),
    ) -> PlatzierungsErgebnis:
        # Querschneidende Eingaben EINMAL bündeln — künftige Nähte sind ein
        # Kontext-Feld statt neuer Parameter-Fädelei durch alle Signaturen.
        kontext = PlatzierungsKontext(
            lb=lb, oib=oib,
            i_cd_fn=self._i_cd_fn, i_cd_fn_je_key=self._i_cd_fn_je_key,
            bestand_leuchten_mm=tuple(bestand_leuchten_mm),
        )
        platzierungen = [
            *_plan_rettungszeichen(raum, norm),          # Anker
            # Owner-Praxisregel (fachpraxis, 2026-09-07): TECHNIK/MUELLRAUM tragen
            # IMMER eine Sicherheitsleuchte an der Tür (fensterlose Nebenräume, oft
            # nicht auf dem Fluchtweg → keine Norm-Strategie greift dort). BEWUSST
            # zuerst unter den Sicherheitsleuchten: der abstand_nachpass-Dubletten-
            # Merge behält bei Gleichstand die früher gelistete → die Pflicht-Leuchte
            # bleibt AN der Tür, eine zufällig <2 m benachbarte SL weicht (netto-neutral).
            *fachpraxis.tuerleuchte_pflichtraeume(raum, norm),
            # R2 (Owner-Korrektur 2026-09-11): AUSSEN-Tür eines COMMUNAL Raums =
            # Notausgang → RZ, Pfeil durch die Tür (EN 1838 §4.1.2 g). Balkontüren
            # privater Räume bleiben außen vor (nicht communal).
            *fachpraxis.aussen_tuer_rz(raum, norm),
            *plan_sicherheitsleuchten(raum, norm),       # Betonungspunkte (Aufheller)
            *plan_antipanik(raum, norm, kontext=kontext),  # Fläche (Trigger OIB-gegated)
            *plan_sonderstellen(raum, norm, kontext=kontext),  # Pflichtstellen §4.1.2
            *plan_flag_raeume(raum, norm),               # barrierefrei/Gefährdung (Flags)
            *plan_aussenleuchten(raum, norm),            # außerhalb Schlussausgang (§4.1.2 b)
            *verdichte_fluchtweg(raum, norm, kontext=kontext),  # Linie + Deckung (Lux)
        ]
        # Owner-Praxisregel B1 (fachpraxis, G4-Entscheid 2026-09-07): je RZ ein
        # Aufheller 500 mm hinter dem Zeichen (Rauminneres). Vor lb_override
        # (LB-Exklusionen greifen auch auf Fachpraxis-SL) und vor dem
        # abstand_nachpass (der Naht-Kollisionen entzerrt/merged).
        platzierungen += fachpraxis.aufheller_je_rz(
            platzierungen, raum, norm, i_cd_fn=kontext.i_cd_fn
        )
        # 2. Input: explizite LB-Vorgaben übersteuern die norm-getriebene Platzierung.
        platzierungen = lb_override.anwenden(platzierungen, raum, lb)
        # Symbole aus Stiegenhaus-Verbotszonen (Laufflächen/Öffnungen) an den nächsten
        # montierbaren Punkt holen (Selman-BEFUND) — vor dem abstand_nachpass, damit
        # dieser eventuelle Verschiebungs-Kollisionen entzerrt.
        platzierungen = verbotszonen_nachpass.entferne_aus_verbotszonen(platzierungen, raum)
        # Owner-Korrektur 2026-09-10: RZ/Aufheller im Gang auf die Korridor-Mittelachse
        # snappen (Querachse zentrieren, Längsachse erhalten). VOR dem Entzerren, damit ein
        # Aufheller, der dabei auf sein RZ fällt, vom abstand_nachpass aufgelöst wird.
        # Tür-RZ ausgenommen.
        platzierungen = mittellinie_snap.snappe_auf_mittellinie(
            platzierungen, raum, bestand_leuchten_mm=kontext.bestand_leuchten_mm
        )
        # R4 (Owner-Korrektur 2026-09-11): RZ am Hauseingang zeigt in FLUCHTRICHTUNG
        # durch die Tür — nie in die Aufschlagrichtung. Rotations-Nachpass, No-op ohne
        # `tuer_detail="hauseingang"`. Nach dem Snap (Positionen final für die Richtung).
        platzierungen = fachpraxis.pfeil_durch_hauseingang(platzierungen, raum)
        # R8 (Owner 2026-09-11): das RZ am Stiegen-Zugang gehört INS Stiegenhaus (Wand),
        # Pfeil in Abstiegs-Richtung — nicht davor in den Gang. No-op ohne stair_exit.
        platzierungen = fachpraxis.stiegenhaus_rz_nachpass(platzierungen, raum)
        # R7 (Owner 2026-09-11, „RZ NICHT in der Wohnung"): Segment-RZ in privaten
        # Stiegen-Vorräumen (Erkennungs-Artefakt: Wohnungs-„GANG"-Stempel) entfernen.
        platzierungen = fachpraxis.entferne_wohnungs_vorraum_rz(platzierungen, raum)
        # Kollisionen an der Strategie-Naht auflösen (Dubletten mergen, verschieden-artige
        # entzerren) — nach lb_override (das SL hinzufügt), vor der Deckungs-Zuordnung,
        # damit diese die finalen Positionen sieht.
        platzierungen = abstand_nachpass.entzerre(platzierungen, raum)
        # Fluchtweg-Deckung nachträglich geometrisch zuordnen (füllt covers_segment,
        # das die RZ-Strategien selbst nicht setzen) → Deckungs-Prüfung wird aussagekräftig.
        platzierungen = deckungs_zuordnung.zuordnen(platzierungen, raum, norm)
        # ≥2-Leuchten-Redundanz je Fluchtweg-Abschnitt garantieren (EN 50172 §5.1.8, F07):
        # unterversorgte Abschnitte bekommen die fehlende SL. VOR der Stromkreis-Zuordnung,
        # damit die Zusatz-Leuchten ihren getrennten SV-Kreis (F13) erhalten — sonst
        # triggert der getrennte-Kreis-Hard-Stop (F06). No-op auf schon konformen Plänen.
        platzierungen = garantiere_redundanz(platzierungen, raum, norm)
        # Stromkreise final vergeben: Dauer-/Bereitschaftslicht trennen + je Kreis deckeln
        # (statt alles grob auf AGV-{Gebäude}-F13 zu mischen). Läuft zuletzt, nach lb_override.
        platzierungen = circuit_zuordnung.zuordnen(platzierungen)
        return PlatzierungsErgebnis(floor=raum.floor, platzierungen=platzierungen)
