"""stgh_strategy — das din-2-RZ-Modul im Stiegenhaus (Punkt 4 der Owner-Reihe).

Referenz Am Rain (AM_RAIN_NOTBELEUCHTUNG_ANALYSE.md §3.2/§6 Kandidat 2, OG1–OG3 in
beiden Cores deckungsgleich gestapelt) + Owner-Fachdoku R-G/R-H (S.10–12): am
Übergang in das Stiegenhaus wirken ZWEI Zeichen zusammen — das Pfeil-unten-RZ an
der Zugangstür („hier durch", allgemeine Türregel R-B/R-C, setzt der Anker-/
Segment-Pfad) und ein **Richtungs-RZ im Stiegenhaus** („weiter in diese
Richtung"), dessen Pfeil der tatsächlichen FLUCHT-Gehrichtung folgt — und die
ergibt sich aus der **Laufrichtung der Stiege** (R-H), nicht aus einer Näherung.

Dieses Modul konsumiert die bislang ungenutzten v1.2.0-Contract-Felder
`StiegenhausModell.laeufe` (Treppenlauf: antritt/austritt/richtung) und
`podeste` (ist_hauptpodest): Position = Hauptpodest-Zentrum (Fallback größtes
Podest, sonst Austrittspunkt des Flucht-Laufs), Pfeil = Fluchtvektor abwärts.
Fail-open: ohne Läufe (heutige Erkennung am 02-TWA-Dialekt, Selman-Naht (c))
passiert hier NICHTS — die R8-Approximation in `fachpraxis` bleibt zuständig.
Im EG-Stiegenhaus mit eigenem `final_exit` leitet das Exit-RZ; kein Podest-RZ.
"""
from __future__ import annotations

import math

from notbeleuchtung.hauptengine.contracts import (
    FluchtwegSegment,
    NormProvider,
    Platzierung,
    RaumModell,
)

from .bausteine import AGV_SV_F as _AGV_SV_F
from .bausteine import building_assigner as _building_assigner
from .bausteine import key_und_rotation as _key_und_rotation
from .bausteine import richtung_und_rotation as _richtung_und_rotation
from .geometry import point_in_polygon


def fluchtvektor(sh) -> tuple[float, float] | None:
    """Flucht-Gehrichtung (abwärts) im Geschoss aus den Treppenläufen — oder None.

    `Treppenlauf.richtung` = Gehrichtung Antritt→Austritt: bei "ab" IST das die
    Fluchtrichtung, bei "auf" ist Flucht die Gegenrichtung (Austritt→Antritt).
    "unbekannt" trägt nichts bei; ohne verwertbaren Lauf None (fail-open)."""
    summe = [0.0, 0.0]
    n = 0
    for lauf in sh.laeufe:
        ax, ay = lauf.antritt_mm
        ex, ey = lauf.austritt_mm
        if lauf.richtung == "ab":
            dx, dy = ex - ax, ey - ay
        elif lauf.richtung == "auf":
            dx, dy = ax - ex, ay - ey
        else:
            continue
        laenge = math.hypot(dx, dy)
        if laenge <= 0.0:
            continue
        summe[0] += dx / laenge
        summe[1] += dy / laenge
        n += 1
    if n == 0 or math.hypot(*summe) < 1e-6:
        return None
    return (summe[0], summe[1])


def _podest_position(sh, flucht: tuple[float, float]) -> tuple[float, float] | None:
    """Hauptpodest-Zentrum; Fallback größtes Podest; sonst Austritt des Flucht-Laufs."""
    def _zentrum(poly):
        xs = [p[0] for p in poly]
        ys = [p[1] for p in poly]
        return ((min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0)

    haupt = [p for p in sh.podeste if p.ist_hauptpodest and len(p.polygon_mm) >= 3]
    if haupt:
        return _zentrum(haupt[0].polygon_mm)
    andere = [p for p in sh.podeste if len(p.polygon_mm) >= 3]
    if andere:
        def _flaeche(p):
            poly = p.polygon_mm
            return abs(sum(x1 * y2 - x2 * y1
                           for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1])))
        return _zentrum(max(andere, key=_flaeche).polygon_mm)
    ablauefe = [x for x in sh.laeufe if x.richtung == "ab"]
    if ablauefe:
        return tuple(ablauefe[0].austritt_mm)
    auflauefe = [x for x in sh.laeufe if x.richtung == "auf"]
    if auflauefe:
        return tuple(auflauefe[0].antritt_mm)
    return None


def plan_stiegenhaus_rz(raum: RaumModell, norm: NormProvider) -> list[Platzierung]:
    """Je Stiegenhaus mit Läufen EIN Richtungs-RZ am Hauptpodest (din-Paar-Teil 2)."""
    if not raum.stiegenhaeuser:
        return []
    stgh_polys = {r.id: r.polygon_mm for r in raum.raeume
                  if (r.raum_typ or "").upper() == "STIEGENHAUS" and len(r.polygon_mm) >= 3}
    out: list[Platzierung] = []
    assign_building = _building_assigner([a.xy_mm[0] for a in raum.ausgaenge] or [0.0])
    for sh in raum.stiegenhaeuser:
        flucht = fluchtvektor(sh)
        if flucht is None:
            continue                                   # Selman-Naht (c): keine Läufe
        poly = stgh_polys.get(sh.raum_id)
        if poly and any(a.typ == "final_exit" and point_in_polygon(a.xy_mm, poly)
                        for a in raum.ausgaenge):
            continue                                   # EG: das Exit-RZ leitet
        pos = _podest_position(sh, flucht)
        if pos is None:
            continue
        richtung, _ = _richtung_und_rotation(flucht[0], flucht[1])
        seg = FluchtwegSegment(segment_id=f"stgh_{sh.raum_id}", polyline_mm=[pos],
                               reason="direction_change")
        anf = norm.fuer_fluchtweg_abschnitt(seg)
        key, rot, mirror = _key_und_rotation(anf.symbol_katalog_keys, richtung)
        out.append(Platzierung(
            xy_mm=pos, catalog_key=key, rotation_deg=rot, mirror_x=mirror,
            height_mm=float(anf.montagehoehe_mm), kind="rz", richtung=richtung,
            circuit_hint=f"AGV-{assign_building(pos[0])}-F{_AGV_SV_F}",
            covers_segment=[], norm_quelle=anf.quelle,
        ))
    return out
