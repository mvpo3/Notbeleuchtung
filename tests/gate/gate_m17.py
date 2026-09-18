"""Messfunktion für die 18 Erwartungen aus Beispiel 17 (Rennweg OG1, Mauern).

Nenner ist fest: JEDE Erwartung der Referenz bekommt genau einen Eintrag —
``BESTANDEN``, ``NICHT_BESTANDEN`` oder ``NICHT_MESSBAR`` mit Grund. Nichts fällt
still heraus, nichts wird geraten: ist eine Erwartung mehrdeutig oder eine
Zuordnung nicht eindeutig, ist das Ergebnis ``NICHT_MESSBAR`` und nie ein PASS.

Gemessen wird auf der Quellpräzision im Speicher (Raumpolygone, Wandkörper,
Türpunkte der Erkennung), nie auf exportierten/gerundeten Werten. Toleranzen:
``KONTAKT_TOL_MM`` für Abstände, ``UEBERLAPPUNG_TOL_MM2`` für Flächen.

„Physische Wand" heißt hier IMMER Einzel-Wandkörper (``Wandkoerper.polygon_mm``).
Die technische ``wand_union`` (Fugenschluss mit 25-mm-Puffer) ist kein Urteil,
sie läuft nur als Messwert ``in_wand_union_technisch`` mit.

Zwei Stellen sind bewusst STRENGER bzw. enger als die Referenz:

* ``physical_wall_covers_probe`` mit ``expected=true`` verlangt hier IMMER
  zusätzlich „kein Raumpolygon deckt die Sonde". Die Referenz fordert das nur
  bei zwei Fällen ausdrücklich; das Gate zieht die Bedingung auf alle Fälle
  hoch, weil eine Sonde, die zugleich in Wand und Raum liegt, kein Beleg für
  eine erkannte physische Wand ist.
* ``direct_portal_in_probe_segment`` fragt geometrisch (Tür im clip und nah an
  der markierten Wand), nicht über ``von_raum``/``nach_raum`` — eine Öffnung
  verschwindet sonst allein dadurch, dass eine Tür anders beschriftet wird.

Die Referenz selbst liegt AUSSERHALB des Repos (Übergabepaket) und wird zur
Laufzeit gelesen (``referenz_pfad``). Rangfolge der Suche:

1. ``NOTBEL_M17_REFERENZ``. Ist die Variable gesetzt, zeigt aber auf keine
   Datei, wird NICHT still auf die Suche zurückgefallen — ``referenz_pfad``
   wirft ``FileNotFoundError``. Ein Tippfehler im Pfad darf nicht als
   „Referenz fehlt eben" durchgehen.
2. sonst Suche in bis zu 3 Elternordnern des Repos (Übergabepaket daneben).

Ohne Variable und ohne Fund gibt es keine Messung (``None``).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from shapely.geometry import LineString, MultiPolygon, Point, Polygon
from shapely.ops import unary_union

from notbeleuchtung.raumerkennung.wandkoerper import wand_union

STATUS = ("BESTANDEN", "NICHT_BESTANDEN", "NICHT_MESSBAR")
KONTAKT_TOL_MM = 1.0
UEBERLAPPUNG_TOL_MM2 = 1.0
# Abstand Tür -> markierte Wand, ab dem eine Tür als Öffnung DIESER Wand zählt.
# Derselbe Wert wie ``tuer_zuordnung._KONTAKT_MM`` (halbe Wanddicke, 250 mm): die
# Erkennung ordnet eine Tür genau in diesem Radius einer Wand zu, also misst das
# Gate mit demselben Radius zurück.
PORTAL_WAND_MM = 250.0

_REPO = Path(__file__).resolve().parents[2]
_REF_RELPFAD = Path(
    "_uebergabe_enis_M17", "Uebergabe_Selman_M17_Rennweg_OG1", "01_Referenzpaket",
    "01_Fachreferenzen", "Raumerkennung_Enis_17_Rennweg_Mauern_Prueffaelle.json")

# Erwartungswerte, für die diese Gate-Semantik definiert ist. Ein anderer
# `expected` wäre eine Lesart, die hier nicht entschieden ist → NICHT_MESSBAR.
_ERWARTET_FEST = {
    "same_room": True,
    "direct_portal_in_probe_segment": False,
    "wall_contact_preserved": True,
    "distinct_rooms_connected_by_door": True,
}


def referenz_pfad() -> Path | None:
    """Pfad zur Referenz-JSON des Übergabepakets — oder None, wenn sie fehlt.

    Gesetztes ``NOTBEL_M17_REFERENZ`` ohne Datei dahinter ist ein Fehler
    (``FileNotFoundError``), kein stiller Rückfall auf die Elternordner-Suche.
    """
    aus_umgebung = os.environ.get("NOTBEL_M17_REFERENZ")
    if aus_umgebung:
        p = Path(aus_umgebung)
        if not p.is_file():
            raise FileNotFoundError(
                "NOTBEL_M17_REFERENZ ist gesetzt, dort liegt aber keine Datei "
                f"({p}) — kein Rückfall auf die Suche in den Elternordnern.")
        return p
    for eltern in list(_REPO.parents)[:3]:
        p = eltern / _REF_RELPFAD
        if p.is_file():
            return p
    return None


def lade_referenz(pfad: Path) -> dict:
    return json.loads(Path(pfad).read_text(encoding="utf-8"))


# ------------------------------------------------------------------ Geometrie

def _sig(wert: float) -> float:
    """Drei signifikante Stellen — ein Abstand von 3e-08 mm darf nicht auf 0.0 runden."""
    return float(f"{wert:.3g}")


def _polygon(punkte) -> Polygon | MultiPolygon | None:
    """Polygon aus Punktliste; repariert Selbstschnitte, None wenn unbrauchbar."""
    if punkte is None or len(punkte) < 3:
        return None
    p = Polygon([(float(x), float(y)) for x, y in punkte])
    if not p.is_valid:
        p = p.buffer(0)
    return None if p.is_empty else p


class _Messer:
    """Hält die vorbereitete Geometrie eines Laufs und misst einen check."""

    def __init__(self, ref: dict, raeume, tueren, wandkoerper, faktor: float) -> None:
        self.ref = ref
        self.faktor = float(faktor)
        self.tueren = list(tueren)
        self.wandkoerper = list(wandkoerper)
        self.raeume = [(r.id, g) for r in raeume if (g := _polygon(r.polygon_mm)) is not None]
        self.raum_obj = {r.id: r for r in raeume}
        self.koerper = [g for k in wandkoerper if (g := _polygon(k.polygon_mm)) is not None]
        self._union = None

    # -- Grundgrößen -------------------------------------------------------
    def pkt(self, xy) -> Point:
        return Point(float(xy[0]) * self.faktor, float(xy[1]) * self.faktor)

    def poly(self, punkte):
        return _polygon([(float(x) * self.faktor, float(y) * self.faktor) for x, y in punkte])

    def linie(self, punkte) -> LineString:
        return LineString([(float(x) * self.faktor, float(y) * self.faktor) for x, y in punkte])

    def raeume_an(self, p: Point) -> list[str]:
        return [rid for rid, g in self.raeume if g.covers(p)]

    def koerper_an(self, p: Point) -> list[int]:
        return [i for i, g in enumerate(self.koerper) if g.covers(p)]

    def in_union(self, p: Point) -> bool:
        if self._union is None:
            self._union = wand_union(self.wandkoerper)
        return bool(self._union.covers(p))

    def raum_geom(self, rid: str):
        return next(g for r, g in self.raeume if r == rid)

    # -- Auflösung ---------------------------------------------------------
    def sonde(self, fall: dict, name: str) -> Point | None:
        xy = (fall.get("probes_wcs_source_units") or {}).get(name)
        return None if xy is None else self.pkt(xy)

    def raum_von(self, fall: dict, name: str) -> tuple[str | None, str | None, str]:
        """(raum_id, status_bei_misserfolg, grund) für die Sonde ``name``."""
        p = self.sonde(fall, name)
        if p is None:
            return None, "NICHT_MESSBAR", f"Sonde {name} fehlt in der Referenz"
        ids = self.raeume_an(p)
        if not ids:
            return None, "NICHT_BESTANDEN", f"Sonde {name} liegt in keinem Raumpolygon"
        if len(ids) > 1:
            return None, "NICHT_MESSBAR", (
                f"Sonde {name} liegt in mehreren Räumen {ids} — Zuordnung mehrdeutig")
        return ids[0], None, ""

    # -- Messung -----------------------------------------------------------
    def check(self, fall: dict, check: dict) -> dict:
        kind = check.get("kind", "")
        erwartet = check.get("expected")
        kopf = {"id": check.get("id", ""), "fall": fall.get("id", ""),
                "kind": kind, "expected": erwartet}
        fest = _ERWARTET_FEST.get(kind)
        if fest is not None and erwartet is not fest:
            return {**kopf, "status": "NICHT_MESSBAR", "messwerte": {},
                    "grund": f"Gate-Semantik für {kind} ist nur für expected={fest} definiert"}
        fn = getattr(self, f"_k_{kind}", None)
        if fn is None:
            return {**kopf, "status": "NICHT_MESSBAR", "messwerte": {},
                    "grund": f"Unbekannte Prüfart '{kind}' — keine Gate-Semantik definiert"}
        status, grund, messwerte = fn(fall, check)
        return {**kopf, "status": status, "grund": grund, "messwerte": messwerte}

    # -- die sieben Prüfarten ---------------------------------------------
    def _k_physical_wall_covers_probe(self, fall, check):
        name = check["objects"][0]
        p = self.sonde(fall, name)
        if p is None:
            return "NICHT_MESSBAR", f"Sonde {name} fehlt in der Referenz", {}
        koerper, raeume = self.koerper_an(p), self.raeume_an(p)
        mw = {"sonde": name, "koerper": koerper, "raeume": raeume,
              "in_wand_union_technisch": self.in_union(p)}
        if check["expected"]:
            ok = bool(koerper) and not raeume
            grund = ("Wandkörper deckt die Sonde, kein Raumpolygon" if ok else
                     f"Wandkörper {koerper or 'keiner'}, Raumpolygone {raeume or 'keine'} — "
                     "erwartet: Wandkörper ja, Raum nein")
        else:
            ok = not koerper
            grund = ("kein Wandkörper an der Sonde" if ok else
                     f"Wandkörper {koerper} deckt die Sonde, erwartet war keiner")
        return ("BESTANDEN" if ok else "NICHT_BESTANDEN"), grund, mw

    def _k_same_room(self, fall, check):
        a, b = check["objects"][:2]
        ra, sa, ga = self.raum_von(fall, a)
        rb, sb, gb = self.raum_von(fall, b)
        if ra is None or rb is None:
            return (sa or sb), (ga or gb), {"raum_a": ra, "raum_b": rb}
        mw = {"raum_a": ra, "raum_b": rb}
        route = fall.get("route_wcs_source_units")
        if route:
            treffer = [(i, round(le, 2)) for i, g in enumerate(self.koerper)
                       if (le := self.linie(route).intersection(g).length) > KONTAKT_TOL_MM]
            mw["route_schnitt"] = treffer
            if treffer:
                return "NICHT_BESTANDEN", (
                    f"Route schneidet Wandkörper {treffer} (Index, Länge mm)"), mw
        if ra != rb:
            return "NICHT_BESTANDEN", f"{a} in {ra}, {b} in {rb} — verschiedene Räume", mw
        return "BESTANDEN", f"{a} und {b} liegen beide in {ra}", mw

    def _k_room_covers_probe(self, fall, check):
        name = check["objects"][0]
        p = self.sonde(fall, name)
        if p is None:
            return "NICHT_MESSBAR", f"Sonde {name} fehlt in der Referenz", {}
        ids = self.raeume_an(p)
        if check["expected"]:
            mw = {"sonde": name, "raeume": ids}
            # Mehrdeutig vs. gar nicht — gleiche Lesart wie ``raum_von``/``same_room``:
            # mehrere Räume sind keine Messung, kein Raum ist ein echter Fehlschlag.
            if len(ids) > 1:
                return "NICHT_MESSBAR", (
                    f"Sonde {name} liegt in mehreren Räumen {ids} — Zuordnung mehrdeutig"), mw
            if not ids:
                return "NICHT_BESTANDEN", f"Sonde {name} liegt in keinem Raumpolygon", mw
            r = self.raum_obj[ids[0]]
            return "BESTANDEN", f"Sonde {name} liegt genau in {ids[0]}", {
                **mw, "raum_typ": r.raum_typ, "flaeche_m2": round(float(r.flaeche_m2), 2)}
        ziel, grund = self._zielraum(fall)
        if ziel is None:
            return "NICHT_MESSBAR", grund, {"sonde": name, "raeume": ids}
        drin = ziel in ids
        return ("NICHT_BESTANDEN" if drin else "BESTANDEN"), (
            f"Zielraum {ziel} deckt Sonde {name}" if drin
            else f"Zielraum {ziel} deckt Sonde {name} nicht (dort: {ids or 'kein Raum'})"
        ), {"sonde": name, "raeume": ids, "zielraum": ziel}

    def _zielraum(self, fall) -> tuple[str | None, str]:
        """Der Raum, den die positive room_covers_probe-Sonde des Falls deckt."""
        positiv = [c for c in fall.get("checks", [])
                   if c.get("kind") == "room_covers_probe" and c.get("expected")]
        if len(positiv) != 1:
            return None, ("Zielraum nicht auflösbar: der Fall hat "
                          f"{len(positiv)} positive room_covers_probe-Erwartungen")
        name = positiv[0]["objects"][0]
        rid, _status, grund = self.raum_von(fall, name)
        return rid, (grund or f"Zielraum über Sonde {name} nicht eindeutig")

    def _k_direct_portal_in_probe_segment(self, fall, check):
        a, b = check["objects"][:2]
        ra, sa, ga = self.raum_von(fall, a)
        rb, sb, gb = self.raum_von(fall, b)
        if ra is None or rb is None:
            return (sa or sb), (ga or gb), {"raum_a": ra, "raum_b": rb}
        if ra == rb:
            return "NICHT_BESTANDEN", (
                f"{a} und {b} liegen im selben Raum {ra} — die Trennung fehlt schon vor "
                "der Portalfrage"), {"raum_a": ra, "raum_b": rb}
        clip = self.poly(fall["clip_polygon_wcs_source_units"])
        wand = self._wand_quelle(fall)
        if clip is None or wand is None:
            return "NICHT_MESSBAR", (
                "markiertes Stück nicht auflösbar: clip_polygon "
                f"{'fehlt' if clip is None else 'ok'}, Quellpolygone der Wand "
                f"{'fehlen' if wand is None else 'ok'}"), {"raum_a": ra, "raum_b": rb}
        portale = []
        for t in self.tueren:
            punkt = self.pkt_mm(t.xy_mm)
            if not clip.covers(punkt):
                continue
            abstand = wand.distance(punkt)
            if abstand <= PORTAL_WAND_MM:
                portale.append({**self._tuer_info(t), "von_raum": t.von_raum,
                                "nach_raum": t.nach_raum,
                                "abstand_wand_mm": round(abstand, 1)})
        mw = {"raum_a": ra, "raum_b": rb,
              "direkte_tueren_gesamt": len(self._tueren_zwischen(ra, rb)),
              "portale": portale}
        if portale:
            return "NICHT_BESTANDEN", (
                f"{len(portale)} Öffnung(en) an der markierten Wand im markierten Stück "
                f"(≤ {PORTAL_WAND_MM:g} mm), obwohl {a} in {ra} und {b} in {rb} liegt"), mw
        return "BESTANDEN", (
            f"keine Öffnung an der markierten Wand im markierten Stück; {a} in {ra}, "
            f"{b} in {rb}"), mw

    def _k_distinct_rooms_connected_by_door(self, fall, check):
        objekte = check["objects"]
        if len(objekte) < 3:
            return "NICHT_MESSBAR", (
                "Referenz nennt keine Sonde für die Öffnung (objects[2] fehlt)"), {}
        a, b, oname = objekte[:3]
        ra, sa, ga = self.raum_von(fall, a)
        rb, sb, gb = self.raum_von(fall, b)
        if ra is None or rb is None:
            return (sa or sb), (ga or gb), {"raum_a": ra, "raum_b": rb}
        if ra == rb:
            return "NICHT_BESTANDEN", (
                f"{a} und {b} liegen im selben Raum {ra} — keine getrennten Räume"
            ), {"raum_a": ra, "raum_b": rb}
        o = self.sonde(fall, oname)
        if o is None:
            return "NICHT_MESSBAR", (
                f"Sonde {oname} fehlt in der Referenz"), {"raum_a": ra, "raum_b": rb}
        clip = self.poly(fall["clip_polygon_wcs_source_units"])
        verb = []
        for t in self._tueren_zwischen(ra, rb):
            punkt = self.pkt_mm(t.xy_mm)
            if clip is None or not clip.covers(punkt):
                continue
            abstand = o.distance(punkt)
            # "an O": die Sonde markiert die Öffnung, also muss sie im Türblatt liegen.
            if t.breite_mm is not None and abstand > float(t.breite_mm) / 2:
                continue
            verb.append({**self._tuer_info(t), "abstand_zu_O_mm": round(abstand)})
        mw = {"raum_a": ra, "raum_b": rb, "sonde": oname, "verbindungen": verb}
        if len(verb) != 1:
            return "NICHT_BESTANDEN", (
                f"{len(verb)} Verbindung(en) zwischen {ra} und {rb} an Sonde {oname} im "
                "markierten Stück, erwartet: genau eine"), mw
        eine = verb[0]
        if eine["ohne_tuerblatt"]:
            return "NICHT_MESSBAR", (
                "Referenz mehrdeutig (Frage an Enis in docs/OFFENE_FRAGEN.md): einzige "
                f"Verbindung {eine['id']} ist ein Durchgang ohne Türblatt "
                f"({eine['breite_mm']} mm, tuer_detail {eine['tuer_detail']}, "
                f"{eine['abstand_zu_O_mm']} mm von {oname}); zählt das als "
                "'Türverbindung'?"), mw
        return "BESTANDEN", (
            f"genau eine Türverbindung {eine['id']} zwischen {ra} und {rb} an Sonde "
            f"{oname}"), mw

    def _k_physical_wall_intersects_route(self, fall, check):
        route = fall.get("route_wcs_source_units")
        if not route:
            return "NICHT_MESSBAR", "Fall führt keine Route (route_wcs_source_units)", {}
        linie = self.linie(route)
        laengen = [(i, round(le, 2)) for i, g in enumerate(self.koerper)
                   if (le := linie.intersection(g).length) > KONTAKT_TOL_MM]
        schneidet = bool(laengen)
        mw = {"schnitte": laengen, "route_laenge_mm": round(linie.length, 1)}
        if schneidet == bool(check["expected"]):
            return "BESTANDEN", (
                f"Route schneidet Wandkörper {laengen}" if schneidet
                else "Route schneidet keinen Wandkörper (> 1 mm)"), mw
        return "NICHT_BESTANDEN", (
            f"Route schneidet Wandkörper {laengen}, erwartet war kein Schnitt" if schneidet
            else "Route schneidet keinen Wandkörper, erwartet war ein Schnitt"), mw

    def _k_wall_contact_preserved(self, fall, check):
        h1, h2, jname = check["objects"][:3]
        j = self.sonde(fall, jname)
        if j is None:
            return "NICHT_MESSBAR", f"Sonde {jname} fehlt in der Referenz", {}
        mw: dict[str, Any] = {}
        gefunden = []
        for h in (h1, h2):
            idx, deckung = self._koerper_zu_handle(h)
            mw[f"koerper_{h}"] = idx
            mw[f"deckung_{h}"] = None if deckung is None else round(deckung, 3)
            if idx is None or deckung is None or deckung < 0.5:
                return "NICHT_BESTANDEN", (
                    f"Quellwand {h} nicht als Wandkörper erkannt "
                    f"(beste Deckung {0.0 if deckung is None else round(deckung, 3)})"), mw
            gefunden.append(self.koerper[idx])
        g1, g2 = gefunden
        abstand = g1.distance(g2)
        dj1, dj2 = j.distance(g1), j.distance(g2)
        ueberlappung = g1.intersection(g2).area
        mw |= {"abstand_mm": _sig(abstand), "j_abstand_1_mm": _sig(dj1),
               "j_abstand_2_mm": _sig(dj2), "ueberlappung_mm2": _sig(ueberlappung),
               "intersects": bool(g1.intersects(g2)), "touches": bool(g1.touches(g2))}
        if ueberlappung > UEBERLAPPUNG_TOL_MM2:
            mw["hinweis"] = "Durchdringung — die Körper überlappen mehr als die Toleranz"
        kontakt = (abstand <= KONTAKT_TOL_MM and dj1 <= KONTAKT_TOL_MM and dj2 <= KONTAKT_TOL_MM)
        ra, _sa, ga = self.raum_von(fall, "A")
        rb, _sb, gb = self.raum_von(fall, "B")
        mw |= {"raum_a": ra, "raum_b": rb}
        if ra is None or rb is None:
            return "NICHT_MESSBAR", (
                f"Flutungsleck nicht prüfbar — {ga or gb}"), mw
        leck, teile = self._flutungsleck(fall, ra, rb)
        mw |= {"freie_teile": teile, "leck": leck}
        if not kontakt:
            return "NICHT_BESTANDEN", (
                f"kein Kontakt bei {jname}: Abstand {abstand:.3g} mm > Toleranz "
                f"{KONTAKT_TOL_MM:g} mm, J-Abstände {dj1:.3g}/{dj2:.3g} mm "
                "(Quellpräzision im Speicher)"), mw
        if leck:
            return "NICHT_BESTANDEN", (
                f"Kontakt besteht, aber eine freie Fläche im markierten Stück verbindet "
                f"{ra} und {rb} an der Wand vorbei"), mw
        return "BESTANDEN", (
            f"Körper berühren sich bei {jname} (Abstand {abstand:.3g} mm ≤ Toleranz "
            f"{KONTAKT_TOL_MM:g} mm, Quellpräzision im Speicher) und im markierten Stück "
            f"gibt es keine freie Verbindung zwischen {ra} und {rb}"), mw

    # -- Werkzeuge ---------------------------------------------------------
    def pkt_mm(self, xy) -> Point:
        """Punkt, der bereits in Modell-mm vorliegt (Türen der Erkennung)."""
        return Point(float(xy[0]), float(xy[1]))

    def _wand_quelle(self, fall):
        """Vereinigung der Quellpolygone der markierten Wand (``fall['wall']``)."""
        quellen = self.ref.get("source_entities") or {}
        teile = []
        for handle in fall.get("wall") or []:
            g = self.poly((quellen.get(handle) or {}).get("points_wcs_source_units") or [])
            if g is not None:
                teile.append(g)
        return unary_union(teile) if teile else None

    def _tueren_zwischen(self, ra: str, rb: str) -> list:
        return [t for t in self.tueren if {t.von_raum, t.nach_raum} == {ra, rb}]

    def _tuer_info(self, t) -> dict:
        return {"id": t.id, "breite_mm": t.breite_mm, "ohne_tuerblatt": bool(t.ohne_tuerblatt),
                "quelle": t.quelle, "tuer_detail": t.tuer_detail}

    def _koerper_zu_handle(self, handle: str) -> tuple[int | None, float | None]:
        """Einzelwandkörper mit der größten Schnittfläche zum Quellpolygon."""
        eintrag = (self.ref.get("source_entities") or {}).get(handle) or {}
        quelle = self.poly(eintrag.get("points_wcs_source_units") or [])
        if quelle is None or quelle.area <= 0:
            return None, None
        best, bestflaeche = None, 0.0
        for i, g in enumerate(self.koerper):
            f = g.intersection(quelle).area
            if f > bestflaeche:
                best, bestflaeche = i, f
        return best, bestflaeche / quelle.area

    def _flutungsleck(self, fall, ra: str, rb: str) -> tuple[bool, int]:
        """Freie Fläche im clip, die beide Räume an der Wand vorbei verbindet."""
        clip = self.poly(fall["clip_polygon_wcs_source_units"])
        if clip is None:
            return False, 0
        gepuffert = [g.buffer(KONTAKT_TOL_MM / 2) for g in self.koerper]
        frei = clip.difference(unary_union(gepuffert)) if gepuffert else clip
        teile = list(getattr(frei, "geoms", [frei])) if not frei.is_empty else []
        ga, gb = self.raum_geom(ra), self.raum_geom(rb)
        leck = any(t.intersection(ga).area > UEBERLAPPUNG_TOL_MM2
                   and t.intersection(gb).area > UEBERLAPPUNG_TOL_MM2 for t in teile)
        return leck, len(teile)


def messe(ref: dict, raeume, tueren, wandkoerper, faktor: float = 1.0) -> list[dict]:
    """Genau ein Ergebnis je Erwartung der Referenz, in deren Reihenfolge."""
    messer = _Messer(ref, raeume, tueren, wandkoerper, faktor)
    return [messer.check(fall, check)
            for fall in ref.get("cases", [])
            for check in fall.get("checks", [])]
