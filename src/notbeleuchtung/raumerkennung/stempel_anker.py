"""stempel_anker — Raumstempel (Name + m² + Belag) als verlässlicher Metadaten-Anker.

Prinzip: Der Raumstempel (Raumname + Fläche, optional Belag) ist die einzige
verlässliche Metadaten-Quelle im Plan — Layer- und Blocknamen sind nur Hinweise.
Drei Stempel-Formen werden layerunabhängig erkannt:

    Rennweg      INSERT je Raum (Blockname ``Bad__6``), ATTRIBs ROOM_NAME/floor_f,
                 m²-MTEXT im Block (ArchiCAD-Zone).
    Barawitzka   lose, vertikal gestapelte MTEXT-Zeilen → Umkreis-Gruppierung.
    Mollgasse    INSERT ``01-SQM`` mit ATTRIBs NR/ROOM/AREA/FLOOR (AREA/FLOOR
                 teils vertauscht — beide werden aufs m²-Muster geprüft).

Zuordnung Stempel→Polygon läuft flächen-first (±10 %), weil ArchiCAD-Zonen ihren
Einfügepunkt AUF die Raumgrenze legen — Punkt-in-Polygon allein kippt dort.

Grenze: Block-Texte werden nur translatiert (kein Rotations-/Skalier-Transform);
alle beobachteten Stempel-Blöcke haben scale 1 / rot 0.
"""
from __future__ import annotations

import math
import re
from collections.abc import Sequence
from dataclasses import dataclass

from shapely.geometry import Point, Polygon

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum

from .dxf_load import XY, DxfPlan
from .raumtyp import raumtyp_flags

# Fläche: '38,35 m2', '1.84m2', '100.95 m²', '25,67^  m2^' (Stacking-Reste), '12 qm'.
_FLAECHE = re.compile(r"(\d+(?:[.,]\d+)?)\s*(?:m\s*[²2]|qm)(?!\w)", re.IGNORECASE)
# Belag-Vokabular (kurze Materialzeile, keine Zahlen).
_BELAG = re.compile(
    r"parkett|fliesen|estrich|estr\.|gu[ßs]s?asphalt|asphalt|platten|rasen|beton"
    r"|teppich|laminat|linoleum|kies|feinsteinzeug|fstz",
    re.IGNORECASE,
)
_BLOCK_SUFFIX = re.compile(r"__\d+$")
_BUCHSTABEN = re.compile(r"[A-Za-zÄÖÜäöüß]")
_MAX_M2 = 10_000.0


@dataclass
class Stempel:
    """Ein erkannter Raumstempel — Position in mm, Fläche in m²."""

    name: str
    typ: str | None                # raum_typ-Label aus dem Wörterbuch, None bei UNKNOWN
    flaeche_m2: float | None
    belag: str | None
    position_mm: XY
    quelle: str                    # 'TEXT' | 'MTEXT' | 'INSERT-Block' | 'Attribut'
    layer: str


@dataclass
class Zuordnung:
    """Stempel→Polygon-Ergebnis inkl. Flächen-Plausibilität."""

    stempel: Stempel
    polygon_index: int | None
    raum: Raum | None
    abweichung_prozent: float | None   # (Polygon − Stempel) / Stempel · 100
    flag: str                          # 'ok' | 'zu_gross' | 'zu_klein' | 'kein_polygon'


def flaeche_aus_text(text: str) -> float | None:
    """m²-Wert aus Freitext; Komma UND Punkt als Dezimaltrenner, '^'-Stacking-Reste."""
    m = _FLAECHE.search(text.replace("^", " "))
    if not m:
        return None
    wert = float(m.group(1).replace(",", "."))
    return wert if 0.0 < wert <= _MAX_M2 else None


def ist_belag(text: str) -> bool:
    """Kurze Materialzeile ('Gußasphalt Bfl', 'Estr. vers.') — keine Fläche, keine Zahl."""
    t = text.strip()
    return (
        len(t) <= 40
        and flaeche_aus_text(t) is None
        and not any(c.isdigit() for c in t)
        and bool(_BELAG.search(t))
    )


def belag_hinweis(belag: str | None) -> str | None:
    """Belag → Raumtyp-HINWEIS (überstimmt den Namens-Typ nie)."""
    if not belag:
        return None
    b = belag.lower()
    if "fliese" in b:
        return "NASSRAUM/VORRAUM"
    if "fstz" in b or "feinsteinzeug" in b:
        return "NASSRAUM/GANG"      # Feinsteinzeug (Rennweg-Kürzel FSTZ.)
    if "parkett" in b:
        return "WOHNRAUM"
    if "estr" in b or "asphalt" in b or "beton" in b:
        return "KELLER/TECHNIK"
    return None


def _typ(name: str) -> str | None:
    tf = raumtyp_flags(name)
    return tf[0] if tf else None


def _blockname_als_name(blockname: str) -> str | None:
    """'Hobbyraum_Fitness__2' → 'Hobbyraum/Fitness'; Technik-Blöcke ('01-SQM') → None."""
    if blockname.startswith(("*", "_")):
        return None
    n = _BLOCK_SUFFIX.sub("", blockname).replace("_", "/").strip("/ ")
    if any(c.isdigit() for c in n) or len(_BUCHSTABEN.findall(n)) < 2:
        return None
    return n


def _block_texte(doc, blockname: str, dx: float, dy: float, tiefe: int = 0):
    """(text, xy_roh) aller TEXT/MTEXT im Block, rekursiv, nur translatiert.

    Grenze: Rotation/Skalierung der INSERTs wird ignoriert (Stempel-Blöcke: 1/0).
    """
    if tiefe > 3:
        return
    blk = doc.blocks.get(blockname)
    if blk is None:
        return
    bx, by = float(blk.base_point[0]), float(blk.base_point[1])
    for e in blk:
        t = e.dxftype()
        if t in ("MTEXT", "TEXT"):
            txt = e.plain_text() if t == "MTEXT" else e.dxf.text
            if txt and txt.strip():
                p = e.dxf.insert
                yield txt.strip(), (float(p[0]) - bx + dx, float(p[1]) - by + dy)
        elif t == "INSERT":
            p = e.dxf.insert
            yield from _block_texte(doc, e.dxf.name,
                                    dx + float(p[0]) - bx, dy + float(p[1]) - by,
                                    tiefe + 1)


def _stempel_aus_insert(plan: DxfPlan, ins) -> Stempel | None:
    """INSERT → Stempel: ATTRIBs (ROOM*/AREA/FLOOR*), Blockname, MTEXT im Block."""
    attribs = [(a.dxf.tag.upper(), a.dxf.text.strip())
               for a in (ins.attribs or []) if a.dxf.text and a.dxf.text.strip()]
    name, quelle = None, ""
    for tag, val in attribs:
        if "ROOM" in tag and flaeche_aus_text(val) is None:
            name, quelle = val, "Attribut"
            break
    if name is None:
        name = _blockname_als_name(ins.dxf.name)
        quelle = "INSERT-Block"
    if name is None:
        return None

    # Fläche: erst ATTRIB-Werte (AREA/FLOOR — vertauschte Paare heilen), dann Block-MTEXT.
    flaeche = next((f for _, v in attribs if (f := flaeche_aus_text(v)) is not None), None)
    # Belag: FLOOR/AREA/BELAG-Wert ohne Ziffern (heilt 'AREA=Plattenbelag'-Vertauschung).
    belag = next((v for tag, v in attribs
                  if ("FLOOR" in tag or "AREA" in tag or "BELAG" in tag)
                  and v and not any(c.isdigit() for c in v)), None)

    px, py = float(ins.dxf.insert[0]), float(ins.dxf.insert[1])
    pos_roh: XY = (px, py)
    # Position bevorzugt vom m²-MTEXT im Block: der liegt IM Raum, der
    # Einfügepunkt (ArchiCAD-Zonen-Referenz) oft AUF der Raumgrenze.
    for txt, xy in _block_texte(plan.doc, ins.dxf.name, px, py):
        f = flaeche_aus_text(txt)
        if f is not None:
            if flaeche is None:
                flaeche = f
            pos_roh = xy
            break
        if belag is None and ist_belag(txt):
            belag = txt
    # Blockname-Stempel ohne Raumtyp UND ohne m² sind Möbel-/Detail-Blöcke
    # ('BodenWandaufbau', 'Spüle', 'schnittführung') — keine Raumstempel.
    if quelle == "INSERT-Block" and _typ(name) is None and flaeche is None:
        return None
    return Stempel(
        name=name, typ=_typ(name), flaeche_m2=flaeche, belag=belag,
        position_mm=(pos_roh[0] * plan.factor, pos_roh[1] * plan.factor),
        quelle=quelle, layer=ins.dxf.layer,
    )


def _stempel_aus_texten(
    fragmente: list[tuple[str, XY, str, str]], radius_mm: float
) -> list[Stempel]:
    """Lose TEXT/MTEXT gruppieren → Stempel, wenn Name UND m² im Umkreis stehen.

    Anker-basiert (je m²-Text ein Kandidat) statt Ketten-Clustering — Single-
    Linkage würde in dichten Plänen alle Stempel zu EINEM Cluster verschmelzen.
    """
    out: list[Stempel] = []
    r2 = radius_mm * radius_mm
    for txt_a, xy_a, _layer_a, _q_a in fragmente:
        flaeche = flaeche_aus_text(txt_a)
        if flaeche is None:
            continue
        # ponytail: O(n·Anker)-Nachbarsuche — Grid-Hash erst, wenn Pläne >10k Texte haben.
        nachbarn = [
            f for f in fragmente
            if (f[1][0] - xy_a[0]) ** 2 + (f[1][1] - xy_a[1]) ** 2 <= r2
            and flaeche_aus_text(f[0]) is None
        ]
        nachbarn.sort(key=lambda f: -f[1][1])  # oberste Zeile zuerst (Stapel-Reihenfolge)
        belag = next((f[0] for f in nachbarn if ist_belag(f[0])), None)
        kandidaten = [f for f in nachbarn if not ist_belag(f[0])
                      and len(_BUCHSTABEN.findall(f[0])) >= 2]
        # NUR Wörterbuch-Treffer: lose m²-Texte ohne erkannten Raumtyp sind
        # Maßketten/Detail-/Möbel-Beschriftung ('WP BD 0,63…'), keine Stempel.
        # INSERT-Stempel (ATTRIB/Blockname) laufen separat und bleiben ungefiltert.
        name_frag = next((f for f in kandidaten if _typ(f[0])), None)
        if name_frag is None:
            continue
        txt, _xy, layer, quelle = name_frag
        out.append(Stempel(
            name=txt, typ=_typ(txt), flaeche_m2=flaeche, belag=belag,
            position_mm=xy_a, quelle=quelle, layer=layer,
        ))
    return out


def finde_stempel(plan: DxfPlan, radius_mm: float = 1500.0) -> list[Stempel]:
    """Alle Raumstempel des Plans — layerunabhängig, drei Formen (s. Modul-Doc)."""
    stempel: list[Stempel] = []
    lose: list[tuple[str, XY, str, str]] = []
    for e in plan.space:
        t = e.dxftype()
        if t in ("MTEXT", "TEXT"):
            txt = e.plain_text() if t == "MTEXT" else e.dxf.text
            if txt and txt.strip():
                lose.append((txt.strip(), plan._scale(e.dxf.insert), e.dxf.layer, t))
        elif t == "INSERT":
            st = _stempel_aus_insert(plan, e)
            if st is not None:
                stempel.append(st)
    stempel.extend(_stempel_aus_texten(lose, radius_mm))
    return stempel


# ---------------------------------------------------------------- Zuordnung

_TOLERANZ_PROZENT = 10.0


def _als_polygone(polygone: Sequence) -> list[tuple[int, Raum | None, Polygon]]:
    out = []
    for i, p in enumerate(polygone):
        pts = p.polygon_mm if isinstance(p, Raum) else p
        if len(pts) >= 3:
            out.append((i, p if isinstance(p, Raum) else None, Polygon(pts)))
    return out


def ordne_zu(stempel: list[Stempel], polygone: Sequence) -> list[Zuordnung]:
    """Stempel→Polygon: (a) Flächen-Match ±10 % (Mehrdeutigkeit → nächstliegend),
    (b) Punkt-in-Polygon, (c) nächster Abstand. NIE nur Punkt-in-Polygon —
    ArchiCAD-Zonen setzen den Einfügepunkt auf die Raumgrenze."""
    polys = _als_polygone(polygone)
    out: list[Zuordnung] = []
    for st in stempel:
        if not polys:
            out.append(Zuordnung(st, None, None, None, "kein_polygon"))
            continue
        pt = Point(st.position_mm)
        treffer = None
        if st.flaeche_m2:
            kandidaten = [
                (i, r, poly) for i, r, poly in polys
                if abs(poly.area / 1e6 - st.flaeche_m2) / st.flaeche_m2 * 100
                <= _TOLERANZ_PROZENT
            ]
            if kandidaten:
                treffer = min(kandidaten, key=lambda k: k[2].centroid.distance(pt))
        if treffer is None:
            treffer = next(((i, r, poly) for i, r, poly in polys if poly.covers(pt)), None)
        if treffer is None:
            treffer = min(polys, key=lambda k: k[2].distance(pt))
        i, raum, poly = treffer
        if st.flaeche_m2:
            abw = (poly.area / 1e6 - st.flaeche_m2) / st.flaeche_m2 * 100
            flag = ("zu_gross" if abw > _TOLERANZ_PROZENT
                    else "zu_klein" if abw < -_TOLERANZ_PROZENT else "ok")
        else:
            abw, flag = None, "ok"
        out.append(Zuordnung(st, i, raum, abw, flag))
    return out


def restflaechen(polygone: Sequence, zuordnungen: list[Zuordnung]) -> list:
    """Polygone ohne Stempel — Kandidaten für Stiegenhaus/Gang/Schacht/Vorraum."""
    belegt = {z.polygon_index for z in zuordnungen if z.polygon_index is not None}
    return [p for i, p in enumerate(polygone) if i not in belegt]


def zentrum(polygon) -> XY:
    """Zentroid (mm) eines Raum-/Punktlisten-Polygons — für Report/Restflächen."""
    pts = polygon.polygon_mm if isinstance(polygon, Raum) else polygon
    c = Polygon(pts).centroid
    return (c.x, c.y) if not math.isnan(c.x) else (0.0, 0.0)
