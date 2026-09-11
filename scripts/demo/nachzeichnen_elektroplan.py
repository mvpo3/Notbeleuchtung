"""nachzeichnen_elektroplan — Elektroplan DE (EG+1OG) bestmöglich nachgezeichnet + ROHE Engine.

Owner-Auftrag 2026-09-11: „Zeichne dieses Projekt bestmöglich nach, und lass die rohe
Hauptengine drauf die Notbeleuchtung und die Lichtberechnung ausführen."

NACHZEICHNEN heißt hier: Primärweg = Selmans Erkennung (`pipeline._parse_raum`) — sie
typt die Wohnungen korrekt. Die LÜCKEN der Erkennung werden mit den REALEN Fakten des
Quellplans gefüllt (jede Ergänzung trägt ihren Plan-Beleg als Kommentar):

  EG:  · EINGANG-Windfang (Stempel EINGANG @2875.69/1737.36) → GANG, Fluchtweg
       · NIEDERSP. (Stempel @2875.66/1731.72) → TECHNIK
       · STGH (Stempel @2890.86/1736.77, Treppen/Lift-Block x 2889.87..2891.63)
         → STIEGENHAUS + StiegenhausModell
       · Hauseingang = Fassadentür (WET-Block @2876.07/1737.06, Dreieck-Marker,
         Wandöffnung x 2875.53..2876.68) → Ausgang `final_exit` + tuer_detail
  1OG: · STGH (Stempel @2890.94/1736.79) → STIEGENHAUS + StiegenhausModell
       · Hausbetreuung (Stempel @2875.66/1731.72) → ABSTELLRAUM (communal)
       · Spielraum (Stempel @2883.79/1732.88) → ZIMMER (communal)
       · Flucht über die Stiege → Ausgang `stair_exit` am Stiegen-Zugang
         (Durchgang Gang→STGH @2890.57/1735.70)

Anders als `run_projekt_neu.py` (Gang-Enden-Exits = Konstrukt) sind die Ausgänge hier
die ECHTEN des Gebäudes. Danach läuft die Engine ROH: `pipeline._run_mit_quelle`
(Platzierung + Prüfung + Render mit Original-Unterlage + Lux-Nachweis) — nichts von Hand.

Ausgabe (P4/nachgezeichnet_out/): {floor}_notbeleuchtung.dxf · {floor}_plan.pdf (A0 1:50)
· {floor}_lichtberechnung.pdf · {floor}.pdf (gemergt) · {floor}.raummodell.json ·
{floor}.pruefung.json · run_summary.json
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import ezdxf
from ezdxf import bbox as ezbbox

from notbeleuchtung.hauptengine import pipeline
from notbeleuchtung.hauptengine.contracts import (
    Ausgang,
    FluchtwegSegment,
    RaumModell,
    StiegenhausModell,
)
from notbeleuchtung.hauptengine.registry import build_default_bundle
from notbeleuchtung.hauptengine.render.lux_nachweis_bericht import schreibe_bericht
from notbeleuchtung.hauptengine.render.pdf_export import dxf_zu_pdf

P4 = Path(r"C:\Users\mvpst\Documents\KI-Projekt\Notbeleuchtung\Projektbeispiele-demo-Platzierungslogik")
OUT = P4 / "nachgezeichnet_out" / "v4"

#: R1 (Owner-Korrektur 2026-09-11): Block-Namen der Allgemeinbeleuchtung im Quellplan —
#: deren Reihe ist die Montagelinie der Gang-Notleuchten.
_BESTAND_BLOCKS = {"spots", "deckenauslass"}


def _bestand_leuchten(quelle_dxf: str, faktor: float = 1000.0):
    """Positionen der Bestands-Allgemeinbeleuchtung (Quellplan in Metern → mm)."""
    doc = ezdxf.readfile(quelle_dxf)
    return tuple(
        (e.dxf.insert[0] * faktor, e.dxf.insert[1] * faktor)
        for e in doc.modelspace().query("INSERT")
        if e.dxf.name.lower().strip() in _BESTAND_BLOCKS
    )


def _enthaelt(poly, xy) -> bool:
    """Punkt-in-Polygon (Ray-Cast) — Stempel-Position → Raum, robust gegen Raum-IDs."""
    x, y = xy
    innen = False
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i][0], poly[i][1]
        x1, y1 = poly[(i + 1) % n][0], poly[(i + 1) % n][1]
        if (y0 > y) != (y1 > y) and x < x0 + (x1 - x0) * (y - y0) / (y1 - y0):
            innen = not innen
    return innen


def _raum_bei(raum: RaumModell, xy_mm):
    """Kleinster Raum, der den Punkt enthält (Stempel liegen ggf. in überlappenden Bboxen)."""
    treffer = [r for r in raum.raeume if len(r.polygon_mm) >= 3 and _enthaelt(r.polygon_mm, xy_mm)]
    return min(treffer, key=lambda r: r.flaeche_m2) if treffer else None


def _type_raum(raum: RaumModell, xy_mm, typ, *, fluchtweg=None, communal=None, beleg=""):
    """Untypisierten Raum am Stempel-Punkt typisieren — Erkennungs-Typen NIE überschreiben."""
    r = _raum_bei(raum, xy_mm)
    if r is None:
        print(f"    ! kein Raum am Stempel {xy_mm} ({typ}) — übersprungen [{beleg}]")
        return raum, None
    if (r.raum_typ or "").strip():
        print(f"    = {r.id} schon typisiert ({r.raum_typ}) — belasse [{beleg}]")
        return raum, r.id
    upd = {"raum_typ": typ}
    if fluchtweg is not None:
        upd["ist_fluchtweg"] = fluchtweg
    if communal is not None:
        upd["ist_communal"] = communal
    neu = [r.model_copy(update=upd) if x.id == r.id else x for x in raum.raeume]
    print(f"    + {r.id} -> {typ} [{beleg}]")
    return raum.model_copy(update={"raeume": neu}), r.id


def _mark_communal(raum: RaumModell, xy_mm, beleg=""):
    """Communal-Flag am Raum unterm Stempel setzen (Typ bleibt unangetastet)."""
    r = _raum_bei(raum, xy_mm)
    if r is None or r.ist_communal:
        return raum
    neu = [x.model_copy(update={"ist_communal": True}) if x.id == r.id else x
           for x in raum.raeume]
    print(f"    + {r.id} -> ist_communal [{beleg}]")
    return raum.model_copy(update={"raeume": neu})


def _tuer_detail(raum: RaumModell, xy_mm, detail, toleranz_mm=400.0):
    """tuer_detail an der Tür nächst xy setzen (nur wenn leer)."""
    best = min(raum.tueren, key=lambda t: (t.xy_mm[0] - xy_mm[0]) ** 2 + (t.xy_mm[1] - xy_mm[1]) ** 2,
               default=None)
    if best is None:
        return raum
    d2 = (best.xy_mm[0] - xy_mm[0]) ** 2 + (best.xy_mm[1] - xy_mm[1]) ** 2
    if d2 > toleranz_mm**2 or getattr(best, "tuer_detail", None):
        return raum
    neu = [t.model_copy(update={"tuer_detail": detail, "ist_notausgang": True})
           if t.id == best.id else t for t in raum.tueren]
    print(f"    + Tuer {best.id} -> tuer_detail={detail}")
    return raum.model_copy(update={"tueren": neu})


def nachzeichnen(raum: RaumModell, floor: str) -> RaumModell:
    """Erkennungs-Lücken mit den realen Plan-Fakten füllen (Belege im Modul-Docstring)."""
    if floor == "EG":
        # EINGANG-Windfang (Stempel EINGANG @2875.69/1737.36) — Teil des Fluchtwegs.
        raum, _ = _type_raum(raum, (2875690, 1737260), "GANG", fluchtweg=True, communal=True,
                             beleg="Stempel EINGANG")
        # NIEDERSP. = Niederspannungsraum (Stempel @2875.66/1731.72).
        raum, _ = _type_raum(raum, (2875660, 1731720), "TECHNIK", communal=True,
                             beleg="Stempel NIEDERSP.")
        # STGH (Stempel @2890.86/1736.77; Treppen/Lift x 2889.87..2891.63). Punkt = exakte
        # Stempel-Position — das Raumpolygon hat eine Stiegen-Aussparung, Mittelpunkte liegen im Void.
        raum, stgh_id = _type_raum(raum, (2890860, 1736770), "STIEGENHAUS", communal=True,
                                   beleg="Stempel STGH + Treppen/Lift-Block")
        # Fahrradraum ist GEMEINSCHAFTLICH (Stempel „Fahrradraum" @2879.06/1731.72;
        # Owner-Korrektur „Hier hast du es Vergessen") — Erkennung typt ABSTELLRAUM
        # ohne communal-Flag → Türleuchten-Regel schlief.
        raum = _mark_communal(raum, (2879060, 1731720), beleg="Stempel Fahrradraum")
        # Hauseingang: Fassadentür (WET @2876.07/1737.06; Öffnung x 2875.53..2876.68).
        raum = _tuer_detail(raum, (2876070, 1737057), "hauseingang")
        ausgaenge = [*raum.ausgaenge,
                     Ausgang(id="EXIT-EINGANG", xy_mm=(2876100.0, 1737300.0), typ="final_exit")]
        # Reales Flucht-Stück Gang-Achse → Hauseingang (der erkannte Korridor-Abschnitt
        # endet an der Gangkante; die letzte Wegstrecke durch den Windfang fehlt sonst).
        stub = FluchtwegSegment(
            segment_id="eingang-stub",
            polyline_mm=[[2876100.0, 1735530.0], [2876100.0, 1737300.0]],
            laenge_mm=1770.0, reason="exit", quelle="FALLBACK", ziel_ausgang="EXIT-EINGANG")
        raum = raum.model_copy(update={"zirkulation": raum.zirkulation.model_copy(
            update={"segmente": [*raum.zirkulation.segmente, stub]})})
    else:
        # STGH (Stempel @2890.94/1736.79) — Flucht führt über die Stiege nach unten.
        raum, stgh_id = _type_raum(raum, (2890940, 1736790), "STIEGENHAUS", communal=True,
                                   beleg="Stempel STGH + Treppen/Lift-Block")
        # Hausbetreuung (Stempel @2875.66/1731.72) — communaler Nebenraum.
        raum, _ = _type_raum(raum, (2875660, 1731720), "ABSTELLRAUM", communal=True,
                             beleg="Stempel Hausbetreuung")
        # Spielraum (Stempel @2883.79/1732.88) — communaler Aufenthaltsraum.
        raum, _ = _type_raum(raum, (2883790, 1732880), "ZIMMER", communal=True,
                             beleg="Stempel Spielraum")
        # Stiegen-Zugang vom Gang (Durchgang @2890.57/1735.70) = Fluchtziel des Geschosses.
        ausgaenge = [*raum.ausgaenge,
                     Ausgang(id="EXIT-STGH", xy_mm=(2890600.0, 1735700.0), typ="stair_exit")]
    stiegen = list(raum.stiegenhaeuser)
    if stgh_id and all(s.raum_id != stgh_id for s in stiegen):
        stiegen.append(StiegenhausModell(raum_id=stgh_id, verbotszonen_mm=[]))
    return raum.model_copy(update={"ausgaenge": ausgaenge, "stiegenhaeuser": stiegen})


def _clip_unterlage(quelle_dxf: str, fenster_m, ziel: str) -> str:
    """Unterlage aufs Gebäudefenster clippen (Quellplan trägt Plankopf/Ansichten km-weit
    draußen → Extents 3,4 km sprengen den Blatt-Fit; gleiche Klasse wie `_geschoss_extents`).
    Entities, deren Bbox das Fenster nicht schneidet, fliegen raus."""
    x0, y0, x1, y1 = fenster_m

    def _anker(e):
        """Repräsentativer Punkt je Entity (bbox-fast liefert bei INSERTs oft nichts)."""
        t = e.dxftype()
        try:
            if t == "LINE":
                s, en = e.dxf.start, e.dxf.end
                return ((s[0] + en[0]) / 2, (s[1] + en[1]) / 2)
            if t == "LWPOLYLINE":
                pts = e.get_points()
                return (pts[0][0], pts[0][1]) if pts else None
            if t in ("INSERT", "TEXT", "MTEXT"):
                p = e.dxf.insert
                return (p[0], p[1])
            if t in ("CIRCLE", "ARC"):
                c = e.dxf.center
                return (c[0], c[1])
            b = ezbbox.extents([e], fast=True)
            if b.has_data:
                return ((b.extmin.x + b.extmax.x) / 2, (b.extmin.y + b.extmax.y) / 2)
        except Exception:  # noqa: BLE001 — unbestimmbar → behalten (fail-open)
            return None
        return None

    doc = ezdxf.readfile(quelle_dxf)
    msp = doc.modelspace()
    weg = []
    for e in msp:
        p = _anker(e)
        if p is not None and not (x0 <= p[0] <= x1 and y0 <= p[1] <= y1):
            weg.append(e)
    for e in weg:
        msp.delete_entity(e)
    doc.saveas(ziel)
    print(f"    Unterlage geclippt: {len(weg)} Entities außerhalb Fenster entfernt")
    return ziel


def _merge(seiten, ziel):
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter()
    for s in seiten:
        for pg in PdfReader(str(s)).pages:
            w.add_page(pg)
    with open(ziel, "wb") as fh:
        w.write(fh)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    bundle = build_default_bundle()
    i_cd_fn = getattr(bundle.platzierer, "_i_cd_fn", None)
    zus = []
    for floor in ("EG", "1OG"):
        dxf_in = P4 / f"{floor}_Elektroplan_DE_NEU.dxf"
        print(f"== {floor}: parse + nachzeichnen")
        with tempfile.TemporaryDirectory(prefix="nachzeichnen_") as tmp:
            raum, quelle_dxf = pipeline._parse_raum(bundle, str(dxf_in), floor, tmp)
            raum = nachzeichnen(raum, floor)
            # Unterlage clippen: Gebäude-Bounds (mm) → Quell-Einheit Meter, +10 m Rand.
            bx0, by0 = raum.bounds_mm.min_xy
            bx1, by1 = raum.bounds_mm.max_xy
            quelle_dxf = _clip_unterlage(
                quelle_dxf,
                (bx0 / 1000 - 10, by0 / 1000 - 10, bx1 / 1000 + 10, by1 / 1000 + 10),
                str(Path(tmp) / f"{floor}_unterlage_clip.dxf"))
            (OUT / f"{floor}.raummodell.json").write_text(
                raum.model_dump_json(indent=1), encoding="utf-8")
            out_dxf = OUT / f"{floor}_notbeleuchtung.dxf"
            res = pipeline._run_mit_quelle(
                bundle, raum, quelle_dxf, out_path=str(out_dxf), lb_path=None,
                plankopf={"projekt": f"Elektroplan DE (nachgezeichnet) · {floor}"},
                projekt_kontext=None, photometrie=None, pdf_quelle=True,
                bestand_leuchten_mm=_bestand_leuchten(quelle_dxf))
            plan_pdf = OUT / f"{floor}_plan.pdf"
            # PDF aus dem Modelspace-Sibling (Modus 1): ezdxf rastert Paperspace-Viewports
            # nicht — das Sibling trägt den Blatt-Rahmen, dxf_zu_pdf liefert A0 1:50
            # (gleicher Weg wie projekt._merge_pdf).
            ms_dxf = out_dxf.with_name(out_dxf.stem + ".modelspace.dxf")
            dxf_zu_pdf(str(ms_dxf if ms_dxf.exists() else out_dxf), str(plan_pdf))
            lb_pdf = OUT / f"{floor}_lichtberechnung.pdf"
            bericht = schreibe_bericht(res.raum, res.platzierung, bundle.norm, str(lb_pdf),
                                       i_cd_fn=i_cd_fn,
                                       projekt=f"Elektroplan DE (nachgezeichnet) · {floor}")
            _merge([plan_pdf, lb_pdf] if bericht else [plan_pdf], OUT / f"{floor}.pdf")
        pruef = res.render_summary.get("pruefung", {})
        (OUT / f"{floor}.pruefung.json").write_text(
            json.dumps(pruef, ensure_ascii=False, indent=1), encoding="utf-8")
        bk: dict = {}
        for p in res.platzierung.platzierungen:
            bk[p.kind] = bk.get(p.kind, 0) + 1
        zeile = {"floor": floor, "raeume": len(res.raum.raeume),
                 "ausgaenge": [a.id for a in res.raum.ausgaenge],
                 "platzierungen": bk, "status": pruef.get("status")}
        zus.append(zeile)
        print(f"   {zeile}")
    (OUT / "run_summary.json").write_text(
        json.dumps(zus, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
