"""deckung — Lux-getriebene Verdichtung der Fluchtweg-Beleuchtung (Schicht „Deckung").

Schließt den Fahrplan Anker → Linie → Fläche → **Deckung**: Fluchtweg-SL entlang der
Mittelachse (`mittellinie.leuchten_auf_linie`), Abstand **photometrisch hergeleitet**
(`lux.max_leuchtenabstand_mm` aus der Hersteller-LDT) und gegen den **norm-korrekten
Nachweis** verifiziert: EN 1838 §4.2.1 fordert ≥ 1 lx auf der MITTELLINIE des
Rettungswegs + ≥ 0,5 lx im halben Mittenband (± Breite/4) + Ud ≥ 1:40 — NICHT
flächig bis in jede Raum-Ecke. Der frühere bbox-Raster-Nachweis war strenger als
die Norm und erzwang ~5-m-Abstände (Faktor 2–3 Überproduktion gegenüber
Herstellerangaben: Schrack IL-Flur > 24 m, din SL5 ~16–21 m — siehe
knowledge/extracted/PRODUKTE_SCHRACK_DIN.md). Erfüllt der photometrische
Start-Abstand den Nachweis nicht, wird verdichtet (÷1.3) bis er hält oder der
Mindestabstand erreicht ist.

Norm-getrieben: OB ein Raum Fluchtweg-Beleuchtung braucht + Montagehöhe/Katalog-Key
kommen aus `norm.fuer_raum`. Feuert nur auf Korridor-Räumen (GANG/FLUR/KORRIDOR) mit
Polygon — Stiegenhäuser/Wohnräume bleiben unberührt. Render-frei, kein Contract berührt.
"""
from __future__ import annotations

from collections.abc import Callable
from itertools import pairwise

from notbeleuchtung.hauptengine.contracts import NormProvider, Platzierung, RaumModell

from .bausteine import AGV_SV_F as _AGV_SV_F
from .bausteine import KORRIDOR_TYPEN as _KORRIDOR_TYPEN
from .bausteine import building_assigner as _building_assigner
from .geometry import _bbox
from .kontext import PlatzierungsKontext
from .lux import (
    LuxErgebnis,
    lux_punkte,
    lux_raster,
    max_leuchtenabstand_mm,
    ud_min_aus_norm,
    wartungsfaktor_aus_norm,
)
from .mittellinie import leuchten_auf_linie_mit_richtung, mittellinie

_SL_KEY = "sicherheitsleuchte_aufheller"   # bis die Norm einen Fluchtweg-SL-Key liefert
_MAX_VERDICHTUNGEN = 6
_VERDICHTUNGS_FAKTOR = 1.3
_MIN_ABSTAND_MM = 4000.0   # Fluchtweg-SL realistisch ≥ 4 m Abstand (nicht 1,5 m)
_MAX_ABSTAND_MM = 30000.0  # Sanity-Cap (Hersteller-Maximum Hochdecken-Optik ~35 m)
_NACHWEIS_RASTER_MM = 250.0
_REDUNDANZ_MIN = 2         # EN 50172 §5.1.8: je Fluchtweg-Abschnitt ≥ 2 Leuchten (= validierung._REDUNDANZ_MIN)
_REDUNDANZ_RADIUS_FALLBACK_MM = 30000.0  # z=200·h=0,15=30 m, nur falls Provider keine Erkennungsweite liefert
# Drossel (S4, Owner 2026-09-13): ein RZ zählt als Gang-Stützpunkt, wenn es IM Gang oder
# höchstens so weit vom Gangrand entfernt ist — deckt die Nebenraum-Tür-RZ ab, die in den
# Gang münden (gemessen EG: Tür-RZ 115–168 mm, Gang-RZ 0). Ein Lücken-Aufheller kommt nur,
# wo zwei aufeinanderfolgende Stützpunkte weiter als _DROSSEL_LUECKE_MM auseinander liegen.
_DROSSEL_RANDNAH_MM = 2000.0
_DROSSEL_LUECKE_MM = 2.0 * _MIN_ABSTAND_MM   # 8 m — konservativer als max_leuchtenabstand (norm-sicher)


def _dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def _dist_punkt_polyline(p, poly) -> float:
    """Minimaler Abstand p→Polylinie (geklemmte Segment-Projektion). Lokal gehalten wie
    in `validierung` — die Deckungs-Schicht bleibt dependency-leicht, identische Metrik."""
    if not poly:
        return float("inf")
    if len(poly) == 1:
        return _dist(p, poly[0])
    best = float("inf")
    for a, b in pairwise(poly):
        dx, dy = b[0] - a[0], b[1] - a[1]
        lq = dx * dx + dy * dy
        if lq == 0.0:
            d = _dist(p, a)
        else:
            t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / lq))
            d = _dist(p, (a[0] + t * dx, a[1] + t * dy))
        best = min(best, d)
    return best


def _redundanz_radius_mm(norm: NormProvider) -> float:
    """Redundanz-Reichweite = Erkennungsweite l=z·h aus der Norm (hinterleuchtet, 0,15 m) —
    DIESELBE Metrik wie `validierung._redundanz_radius_mm` (F04), damit die Platzierungs-
    Garantie und der Prüf-Hard-Fail denselben Radius sehen. Fallback nur, wenn die Norm
    keine (positive) Erkennungsweite liefert."""
    w = norm.erkennungsweite_m(0.15, hinterleuchtet=True) * 1000.0
    return w if w and w > 0 else _REDUNDANZ_RADIUS_FALLBACK_MM


def _resample_polyline(poly: list[tuple[float, float]], k: int) -> list[tuple[float, float]]:
    """k gleich-(bogen-)verteilte Punkte auf der Polylinie (inkl. beider Enden)."""
    if k <= 1 or len(poly) < 2:
        mid = poly[len(poly) // 2] if poly else (0.0, 0.0)
        return [mid]
    seg_len = [_dist(a, b) for a, b in pairwise(poly)]
    total = sum(seg_len)
    if total <= 0.0:
        return [poly[0]]
    paare = list(pairwise(poly))
    out: list[tuple[float, float]] = []
    for j in range(k):
        ziel = total * j / (k - 1)
        acc = 0.0
        for idx, ((a, b), ln) in enumerate(zip(paare, seg_len)):
            if acc + ln >= ziel or idx == len(paare) - 1:
                t = 0.0 if ln == 0.0 else (ziel - acc) / ln
                out.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
                break
            acc += ln
    return out


def garantiere_redundanz(
    platzierungen: list[Platzierung], raum: RaumModell, norm: NormProvider
) -> list[Platzierung]:
    """F07 / W19 — EN 50172 §5.1.8 [AT-verbindlich über ÖNORM EN 1838]: jeder Fluchtweg-
    Abschnitt braucht ≥ 2 Leuchten (RZ/SL) in Erkennungsweite, damit ein Leuchten-Ausfall
    den Abschnitt nicht verdunkelt. Abschnitte mit < 2 Leuchten in Reichweite bekommen die
    fehlende(n) Sicherheitsleuchte(n) bogen-verteilt auf der Segment-Polylinie, möglichst
    weit weg von den schon vorhandenen. **Minimal/segment-genau**: Abschnitte mit ≥ 2
    Leuchten sind ein No-op → kein Golden-Shift auf schon konformen Plänen. Läuft VOR der
    Stromkreis-Zuordnung, damit die Zusatz-Leuchten ihren getrennten SV-Kreis (F13) erhalten.
    Radius = `norm.erkennungsweite_m` (identisch zur Prüfung)."""
    segmente = raum.zirkulation.segmente if raum.zirkulation else []
    if not segmente:
        return platzierungen
    radius = _redundanz_radius_mm(norm)
    vorhandene = [p for p in platzierungen if p.kind in ("rz", "sicherheitsleuchte")]
    zusatz: list[Platzierung] = []
    for s in segmente:
        poly = [tuple(pt) for pt in s.polyline_mm]
        if not poly:
            continue
        nah = [p.xy_mm for p in (vorhandene + zusatz)
               if _dist_punkt_polyline(p.xy_mm, poly) <= radius]
        fehlen = _REDUNDANZ_MIN - len(nah)
        if fehlen <= 0:
            continue
        anf = norm.fuer_fluchtweg_abschnitt(s)
        # Kandidaten weit von schon vorhandenen Leuchten: größtmöglicher Ausfall-Abstand.
        kandidaten = _resample_polyline(poly, max(2 * fehlen + 1, 3))
        kandidaten.sort(key=lambda c: min((_dist(c, q) for q in nah), default=0.0), reverse=True)
        for (x, y) in kandidaten[:fehlen]:
            zusatz.append(Platzierung(
                xy_mm=(x, y), catalog_key=_SL_KEY, rotation_deg=0.0,
                height_mm=float(anf.montagehoehe_mm), kind="sicherheitsleuchte",
                # Vorläufiger getrennter SV-Kreis (F13); `circuit_zuordnung` vergibt final.
                # MUSS F13 tragen, sonst schlägt der getrennte-Kreis-Hard-Stop (F06) zu.
                richtung="gerade", circuit_hint=f"AGV-A-F{_AGV_SV_F}",
                covers_segment=[s.segment_id], norm_quelle=anf.quelle,
            ))
    return platzierungen + zusatz


def _nachweis_punkte(linie: list, breite_mm: float) -> tuple[list, list]:
    """(Mittellinien-Punkte, Mittenband-Punkte ± Breite/4) für den §4.2.1-Nachweis.

    Band-Offsets folgen der lokalen Tangente (Nachbarpunkte) — deckt auch L-förmige
    Korridore. §4.2.1: Mittellinie ≥ 1 lx, halbes Mittenband ≥ 0,5 lx.
    """
    if len(linie) < 2:
        return linie, []
    off = breite_mm / 4.0
    band = []
    for i, (x, y) in enumerate(linie):
        x2, y2 = linie[min(i + 1, len(linie) - 1)]
        x1, y1 = linie[max(i - 1, 0)]
        tx, ty = x2 - x1, y2 - y1
        n = (tx * tx + ty * ty) ** 0.5
        if n < 1e-9:
            continue
        nx, ny = -ty / n, tx / n
        band.append((x + nx * off, y + ny * off))
        band.append((x - nx * off, y - ny * off))
    return linie, band


def _rz_stuetz_positionen(bestehende_rz, r) -> tuple[list, int]:
    """RZ-Positionen, die den Korridor `r` stützen — projiziert auf seine Längsachse
    (`laengs`: 0=x, 1=y) und sortiert. Ein RZ zählt, wenn es IM Gang-Polygon liegt oder
    höchstens `_DROSSEL_RANDNAH_MM` vom Rand entfernt ist (Nebenraum-Tür-RZ am Gang).
    Konvention identisch zu `platzierer._mittel_arm_rz` (Positions-Projektion via bbox)."""
    from .geometry import point_in_polygon
    x0, y0, x1, y1 = _bbox(r.polygon_mm)
    laengs = 0 if (x1 - x0) >= (y1 - y0) else 1
    poly = [tuple(c) for c in r.polygon_mm]
    pos = [
        p.xy_mm[laengs] for p in bestehende_rz
        if p.kind == "rz" and (point_in_polygon(p.xy_mm, r.polygon_mm)
                               or _dist_punkt_polyline(p.xy_mm, poly) <= _DROSSEL_RANDNAH_MM)
    ]
    return sorted(pos), laengs


def _drossel_fueller(r, stuetz_pos: list, laengs: int) -> list:
    """Statt der verdichteten SL-Reihe: EIN Aufheller in der Mitte jeder Längslücke
    zwischen aufeinanderfolgenden Stützpunkten (RZ + Gang-Enden), die > `_DROSSEL_LUECKE_MM`
    ist. Kurze Gänge / dicht gestützte Abschnitte bleiben leer (RZ decken sie)."""
    x0, y0, x1, y1 = _bbox(r.polygon_mm)
    lo, hi = (x0, x1) if laengs == 0 else (y0, y1)
    quer = (y0 + y1) / 2.0 if laengs == 0 else (x0 + x1) / 2.0
    az = 0.0 if laengs == 0 else 90.0
    out = []
    for a, b in pairwise([lo, *stuetz_pos, hi]):
        if b - a <= _DROSSEL_LUECKE_MM:
            continue
        mid = (a + b) / 2.0
        pt = (mid, quer) if laengs == 0 else (quer, mid)
        out.append((pt[0], pt[1], az))
    return out


def verdichte_fluchtweg(
    raum: RaumModell, norm: NormProvider, *,
    i_cd: float = 200.0,
    i_cd_fn: Callable[[float], float] | None = None,
    kontext: PlatzierungsKontext | None = None,
    bestehende_rz: list[Platzierung] | tuple = (),
) -> list[Platzierung]:
    """Sicherheitsleuchten entlang jeder Korridor-Mittellinie, verdichtet bis 1 lx / Ud≥1:40.

    `i_cd` = konstante Lichtstärke-Annahme; `i_cd_fn(γ)` = richtungsabhängige Hersteller-
    Photometrie (EULUMDAT/LDT, überschreibt `i_cd`), von der Hauptengine injiziert.
    `kontext` bündelt die querschneidenden Eingaben; ein explizites `i_cd_fn` gewinnt.

    **Deckungs-Drossel (S4, Owner-Muster 2026-09-13):** stützt mindestens ein RZ den
    Korridor (IM Gang oder als Nebenraum-Tür-RZ am Gangrand, `bestehende_rz`), wird die
    verdichtete SL-Reihe NICHT aufgespannt — stattdessen füllt EIN Aufheller jede Längslücke
    zwischen aufeinanderfolgenden RZ/Gang-Enden, die weiter als `_DROSSEL_LUECKE_MM` ist
    (Ground-truth EG: RZ an den Gang-Enden + 1 Aufheller mittig statt 4 SL). Korridore ohne
    stützendes RZ behalten die volle Lux-Verdichtung (kein Golden-Shift dort)."""
    if i_cd_fn is None and kontext is not None:
        i_cd_fn = kontext.i_cd_fn
    korridore = [
        r for r in raum.raeume if r.raum_typ.upper() in _KORRIDOR_TYPEN and len(r.polygon_mm) >= 3
    ]
    if not korridore:
        return []
    assign_building = _building_assigner(
        [(_bbox(r.polygon_mm)[0] + _bbox(r.polygon_mm)[2]) / 2 for r in korridore]
    )

    out: list[Platzierung] = []
    for r in korridore:
        anf = norm.fuer_raum(r.raum_typ, r.ist_fluchtweg)
        bounds = _bbox(r.polygon_mm)
        h_m = anf.montagehoehe_mm / 1000.0
        ud_min = ud_min_aus_norm(anf.gleichmaessigkeit_max)
        ziel = anf.min_lux or 1.0
        # Wartungsfaktor aus der Norm (Alterung/Verschmutzung; Profi-Praxis 0,80 innen /
        # 0,57 außen — s. knowledge/extracted/LICHTBERECHNUNG_REFERENZ.md). Defensiv
        # gelesen: liefert die (noch) MF-freie NormAnforderung kein Feld, bleibt es bei
        # 1,0 → Platzierung bit-identisch (Track-B-Muster). Enis füllt das Feld später.
        wf = wartungsfaktor_aus_norm(anf)
        breite = min(bounds[2] - bounds[0], bounds[3] - bounds[1])
        linie, band = _nachweis_punkte(
            mittellinie(r.polygon_mm, raster_mm=_NACHWEIS_RASTER_MM), breite
        )
        # Start-Abstand photometrisch aus der Leuchte selbst (aufweiten UND verdichten
        # möglich — der alte Fix-Start bei 8 m konnte nur verdichten). Die Optik wird
        # längs der Korridor-Achse montiert (Azimut je Kandidat, s.u.) — der Reihen-
        # Startwert darf deshalb die C0-Keule ansetzen.
        abstand = max_leuchtenabstand_mm(
            montagehoehe_m=h_m, i_cd=i_cd, i_cd_fn=i_cd_fn, ziel_lux=ziel,
            min_mm=_MIN_ABSTAND_MM, max_mm=_MAX_ABSTAND_MM, optik_entlang_reihe=True,
            wartungsfaktor=wf,
        )
        stuetz_pos, laengs = _rz_stuetz_positionen(bestehende_rz, r)
        if stuetz_pos:
            # Drossel: RZ decken den Gang → Reihe durch Lücken-Aufheller ersetzen.
            kandidaten = _drossel_fueller(r, stuetz_pos, laengs)
        else:
            kandidaten = leuchten_auf_linie_mit_richtung(r.polygon_mm, abstand)
            for _ in range(_MAX_VERDICHTUNGEN):
                if not linie:   # degeneriertes Polygon → alter Flächen-Nachweis als Fallback
                    res = lux_raster(
                        kandidaten, bounds, montagehoehe_m=h_m, i_cd=i_cd, i_cd_fn=i_cd_fn,
                        ziel_lux=ziel, ud_min=ud_min, wartungsfaktor=wf,
                    )
                    erfuellt = res.erfuellt_min and res.erfuellt_ud
                else:
                    mitte = lux_punkte(
                        kandidaten, linie, montagehoehe_m=h_m, i_cd=i_cd, i_cd_fn=i_cd_fn,
                        ziel_lux=ziel, ud_min=ud_min, wartungsfaktor=wf,
                    )
                    halbband = lux_punkte(
                        kandidaten, band, montagehoehe_m=h_m, i_cd=i_cd, i_cd_fn=i_cd_fn,
                        ziel_lux=ziel / 2.0, ud_min=0.0, wartungsfaktor=wf,
                    ) if band else None
                    erfuellt = (
                        mitte.erfuellt_min and mitte.erfuellt_ud
                        and (halbband is None or halbband.erfuellt_min)
                    )
                if erfuellt or abstand <= _MIN_ABSTAND_MM:
                    break
                abstand = max(_MIN_ABSTAND_MM, abstand / _VERDICHTUNGS_FAKTOR)
                kandidaten = leuchten_auf_linie_mit_richtung(r.polygon_mm, abstand)
        cx = (bounds[0] + bounds[2]) / 2
        building = assign_building(cx)
        for px, py, az in kandidaten:
            out.append(
                Platzierung(
                    xy_mm=(px, py),
                    catalog_key=_SL_KEY,
                    # Montage-Rotation = Korridor-Achse: die Optik-C0 zeigt längs
                    # des Gangs — exakt der Azimut, mit dem der Lux-Nachweis oben
                    # gerechnet hat (Azimut-Tripel). Symbol dreht mit.
                    rotation_deg=az,
                    height_mm=float(anf.montagehoehe_mm),
                    kind="sicherheitsleuchte",
                    richtung="gerade",
                    circuit_hint=f"AGV-{building}-F{_AGV_SV_F}",
                    covers_segment=[],
                    norm_quelle=anf.quelle,
                )
            )
    return out


def lux_bericht(
    raum: RaumModell, ergebnis, *,
    i_cd: float = 200.0,
    i_cd_fn: Callable[[float], float] | None = None,
) -> dict[str, LuxErgebnis]:
    """Je Korridor-Raum: Lux-Bewertung der darin liegenden Sicherheitsleuchten.

    Reporting/Audit — verändert nichts. Schlüssel = Raum-ID. `i_cd_fn` wie in
    `verdichte_fluchtweg` (Hersteller-Photometrie statt konstant `i_cd`).
    """
    from .geometry import point_in_polygon

    bericht: dict[str, LuxErgebnis] = {}
    sl = [p for p in ergebnis.platzierungen if p.kind == "sicherheitsleuchte"]
    for r in raum.raeume:
        if r.raum_typ.upper() not in _KORRIDOR_TYPEN or len(r.polygon_mm) < 3:
            continue
        drin = [p.xy_mm for p in sl if point_in_polygon(p.xy_mm, r.polygon_mm)]
        bericht[r.id] = lux_raster(
            drin, _bbox(r.polygon_mm), i_cd=i_cd, i_cd_fn=i_cd_fn, ziel_lux=1.0
        )
    return bericht
