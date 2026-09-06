"""communal_stgh_strategy — Rettungszeichen entlang der Fluchtweg-Segmente.

Render-freie Adaption der generativen STGH-Logik aus elektro-planer
`backend/diagnostics/inject_communal_stgh.py` (siehe docs/PORT_LOG.md). Die
Original-Version ZEICHNET (ezdxf/insert_symbol/render_layout_pdf); diese Strategy
produziert ausschließlich Contract-B `Platzierung`-Objekte — die Hauptengine
rendert später. Import-Grenze (CLAUDE.md, hart): nur `hauptengine.contracts` +
`platzierung.geometry` + `notbeleuchtung.symbols`, KEIN Render.

Kern-Regel (generativ, KEINE Ground-Truth-Koordinaten):
  1 Rettungszeichen je Fluchtweg-Segment, gesetzt am **Ausgangs-Endpunkt** des
  Segments (`polyline_mm[-1]`). Der RaumModell-Fixture setzt diese Endpunkte an
  die realen RZ-Stellen → Positionen matchen, ohne dass hier etwas hardcodet wird.

Orientierung (`richtung`/`rotation_deg`) folgt der Segment-Laufrichtung
(`polyline_mm[-2] → [-1]`) auf die dominante Achse gerundet (Kardinal 0/90/180/270).
Die exakten Sub-Grad-Rotationen der Referenz (180.1°, 359.7° …) sind
DXF-Extraktions-Artefakte und werden bewusst NICHT reproduziert (Owner-Entscheid:
generativ statt faithful).

Bauteil-/Stromkreis-Zuordnung (AGV-<A|B>-F13) übernimmt die Cluster-Regel des
Originals: liegen die RZ über >20 m gespreizt, teilt die x-Mitte in Bauteil A
(westlich) / B (östlich); F13 = getrennter Sicherheitskreis (EN 1838).
"""
from __future__ import annotations

import math

from notbeleuchtung.hauptengine.contracts import (
    NormProvider,
    Platzierung,
    RaumModell,
)

# Slice 2.46.3 (elektro-planer): Communal-STGH hängt am Allgemeinverteiler (AGV,
# getrennt vom Wohnungszähler). SV = Sicherheitsbeleuchtung, dauergeschaltet → F13.
from .bausteine import (
    AGV_SV_F as _AGV_SV_F,
)
from .bausteine import (
    building_assigner as _building_assigner,
)
from .bausteine import (
    richtung_und_rotation as _richtung_und_rotation,
)
from .bausteine import (
    select_key as _select_key,
)


def plan_rettungszeichen(raum: RaumModell, norm: NormProvider) -> list[Platzierung]:
    """Ein RZ je Fluchtweg-Segment → Contract-B `Platzierung`-Liste (render-frei).

    Leonis fragt die Norm über `fuer_fluchtweg_abschnitt` (parst nie YAML). Position
    = Segment-Ausgangs-Endpunkt; Orientierung/Bauteil generativ (s. Modul-Docstring).
    """
    segmente = raum.zirkulation.segmente
    exits = [a.xy_mm for a in raum.ausgaenge]

    def _naechster_exit(p):
        return min(exits, key=lambda e: math.hypot(e[0] - p[0], e[1] - p[1])) if exits else None

    # Position bleibt der Segment-Endpunkt `polyline[-1]` (Provider-Vertrag: dort
    # sitzt das RZ). Owner-Fix betrifft NUR die Pfeilrichtung (s.u.): nie ins
    # blinde Gang-Ende, immer zur Tür bzw. zum nächsten Ausgang.
    endpoints: list[tuple[float, float]] = [
        (seg.polyline_mm[-1] if seg.polyline_mm else (0.0, 0.0)) for seg in segmente
    ]
    assign_building = _building_assigner([x for x, _ in endpoints])

    out: list[Platzierung] = []
    for seg, (ex, ey) in zip(segmente, endpoints):
        if not seg.polyline_mm:
            continue
        anf = norm.fuer_fluchtweg_abschnitt(seg)
        anlauf = seg.polyline_mm[-2] if len(seg.polyline_mm) >= 2 else (ex, ey)
        # Nur AUSGANGS-Türen qualifizieren (ist_notausgang oder Stiegenhaus-Anschluss) —
        # sonst zeigte der Pfeil in Nebenräume (Technik/Wohnung) statt zum Ausgang.
        typen = {r.id: (r.raum_typ or "").upper() for r in raum.raeume}
        ausgangs_tueren = [
            t for t in raum.tueren
            if t.ist_notausgang
            or "STIEGENHAUS" in (typen.get(t.von_raum or "", ""), typen.get(t.nach_raum or "", ""))
        ]
        tuer = min(
            ausgangs_tueren,
            key=lambda t: math.hypot(t.xy_mm[0] - ex, t.xy_mm[1] - ey),
            default=None,
        )
        d_tuer = (
            math.hypot(tuer.xy_mm[0] - ex, tuer.xy_mm[1] - ey) if tuer is not None else 1e12
        )
        naechster = _naechster_exit((ex, ey))
        d_exit = math.hypot(naechster[0] - ex, naechster[1] - ey) if naechster else 1e12
        if d_tuer <= 2000.0:
            # Owner-Regel: an Türen IMMER das Pfeil-unten-Zeichen, rotiert sodass der
            # Pfeil ZUR/DURCH die Tür zeigt (Anlauf-Richtung, wenn RZ auf der Tür sitzt).
            if d_tuer > 50.0:
                dx, dy = tuer.xy_mm[0] - ex, tuer.xy_mm[1] - ey
            else:
                dx, dy = ex - anlauf[0], ey - anlauf[1]
            richtung = "unten"
            catalog_key, _ = _select_key(anf.symbol_katalog_keys, "unten")
            rotation = (round((math.degrees(math.atan2(dy, dx)) + 90.0) / 90.0) * 90.0) % 360.0
            mirror_x = False
        elif naechster is not None and d_exit > 1000.0:
            # Kein Tür-Anker → Pfeil zeigt ZUM nächsten Ausgang (nie ins blinde Ende).
            richtung, fallback_rotation = _richtung_und_rotation(
                naechster[0] - ex, naechster[1] - ey
            )
            catalog_key, is_directional = _select_key(anf.symbol_katalog_keys, richtung)
            rotation = 0.0 if is_directional else fallback_rotation
            mirror_x = False if is_directional else (richtung == "rechts")
        else:
            # Auf dem Ausgang selbst (oder keine Ausgänge): Laufrichtung des Segments
            # (durch die Öffnung hinaus) — historisches 4OG-Verhalten.
            px, py = seg.polyline_mm[-2] if len(seg.polyline_mm) >= 2 else (ex, ey)
            richtung, fallback_rotation = _richtung_und_rotation(ex - px, ey - py)
            catalog_key, is_directional = _select_key(anf.symbol_katalog_keys, richtung)
            rotation = 0.0 if is_directional else fallback_rotation
            mirror_x = False if is_directional else (richtung == "rechts")
        building = assign_building(ex)
        out.append(
            Platzierung(
                xy_mm=(ex, ey),
                catalog_key=catalog_key,
                rotation_deg=rotation,
                mirror_x=mirror_x,
                height_mm=float(anf.montagehoehe_mm),
                kind=anf.klassifikation,
                richtung=richtung,
                circuit_hint=f"AGV-{building}-F{_AGV_SV_F}",
                covers_segment=[seg.segment_id],
                norm_quelle=anf.quelle,
            )
        )
    return out
