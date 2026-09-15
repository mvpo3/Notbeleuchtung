"""aussenbereich — AUSSEN-Flächen erkennen (Hof, Garten, Wege ins Freie).

Bezug ist der FLÄCHENGRUNDRISS bis zur Grundstücksgrenze (``grundstuecksgrenze``)
— der umfasst auch Garten, Innenhof und Vorplatz. Fehlt ein Grenz-Layer, bleibt
die konvexe Hülle der Fallback (gemessen: Mollgasse-Hülle 1804.5 m² ist größer
als das Grundstück 1510.2 m² und ragt auf öffentlichen Grund).

AUSSEN = freie Fläche im Bezugspolygon, die
(a) Außenanlagen enthält (GRÜN-/Platten-/Kies-Schraffuren, Baum-Blöcke,
    Grundstücksgrenze-Layer — Layer-Hinweise, keine Normwerte) ODER
(b) den Bezugsrand berührt.
Sie ist ``offen`` nur, wenn sie die STRASSENKANTE erreicht: „ins Freie" heißt
aus dem Flächengrundriss HERAUS auf öffentlichen Grund.

Ein Hof OHNE Weg ins Freie ist ``AUSSEN_GESCHLOSSEN``: dort entsteht kein
final_exit (offene Frage an Enis, docs/OFFENE_FRAGEN.md) — seine Fläche zählt
für die Türzuordnung weiter als "gedeckt" (Türen dorthin werden nicht AUSSEN).

Die Außenkontur wird JE GEBÄUDE-KOMPONENTE gerechnet (Barawitzka = 2 Trakte
mit einem Hof dazwischen — eine einzige Kontur verschluckt den Südtrakt).
Barawitzka gemessen: dieser Hof (190.2 m²) verbindet zwar beide Stiegenhäuser,
liegt aber 2.55 m von der 20.6 m langen Straßenkante entfernt → geschlossen;
offen ist nur die Vorplatz-Fläche (12.5 m², Abstand 0.10 m).

Decken-Heuristik (Slab-Polygone) ist hier bewusst KEIN Ausschluss: auf Rennweg
EG enthält die Slab-Union den Türschließer-Eingang (Beleg docs/OFFENE_FRAGEN.md)
— Slabs taugen nur als Positiv-Hinweis, wo sie verlässlich sind.
"""
from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass, field
from itertools import combinations

from shapely.geometry import LineString, MultiPolygon, Point, Polygon
from shapely.ops import polygonize, unary_union

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum

from .dxf_load import DxfPlan
from .raumlayer import _hatch_pfad_mm
from .stempel_anker import Zuordnung
from .wandkoerper import Wandkoerper, finde_wandkoerper

XY = tuple[float, float]

# Layer-Hinweise auf Außenanlagen (tolerant gegen cp-dekodierte Umlaute:
# 'GRÜN' → 'GR.N'). BELAG bewusst NICHT: Belagsflächen gibt es auch innen.
_AUSSEN_LAYER = re.compile(
    r"GR.N|KIES|GARTEN|RASEN|PLATTE|BAUM|B.UME|GRUNDST|GRENZE", re.IGNORECASE)
# Baum-/Bepflanzungs-Blöcke.
_BAUM_BLOCK = re.compile(r"BAUM|TREE|STRAUCH", re.IGNORECASE)

# Morphologisches Schließen der Wand-Union. BEWUSST größer als aussenkontur
# (600): auch Doppelflügel-Hauseingänge (~1.9 m) müssen versiegelt werden,
# sonst „leckt" der Erschließungsgang durch die Eingangsöffnung in den
# Außenraum und würde als AUSSEN klassifiziert. Tore > 2.4 m (Garagen-/
# Hof-Durchfahrten) bleiben offen — gewollt: dort ist ein Weg ins Freie.
_SCHLIESS_MM = 1200.0
_MIN_HOF_M2 = 5.0        # kleinere freie Flächen sind Nischen, keine Höfe
_RAND_EPS_MM = 250.0     # "berührt den Bezugsrand" -Toleranz
# Halbe Mindest-Durchgangsbreite: eine Fläche, die nach Erosion um diesen
# Wert verschwindet, ist ein Zeichnungs-Splitter (Haarriss zwischen Grenz-
# und Wandgeometrie), kein begehbarer Weg. Barawitzka gemessen: der
# 0.13-m-Splitter entlang der Nordfassade fällt weg, der 190.2-m²-Hof bleibt.
_HALS_MM = 400.0

# Grundstücksgrenze: Layer-Muster (tolerant gegen cp-dekodierte Umlaute).
_GRENZ_LAYER = re.compile(
    r"GRUNDST.CKSGRENZE|GRUNDSTUECKSGRENZE|KATASTER|PROP-?LINE", re.IGNORECASE)
# Typ-Filter PFLICHT: Rennweg_OG3 trägt auf 'New_GRUNDSTÜCKSGRENZE' 103
# DIMENSION und KEINE Liniengeometrie — ohne Filter ein Falschpositiv.
_GRENZ_TYPEN = ("LINE", "LWPOLYLINE", "POLYLINE")
# Barawitzka: die 16 Grenzlinien sind an 7 Grenzpunkt-Kreisen (r=100 mm)
# zurückgeschnitten — ohne Brückung liefert polygonize 0 Ringe, mit 1 Ring.
_BRUECKE_MM = 400.0

# Straßen-Indiz für die Straßenkante. 'STRA.ENVERKEHR' bewusst NICHT: der
# Layer 'Straßenverkehr_Situationslinie.verm' läuft bei Barawitzka auch an der
# SÜDgrenze (Kontakt bis y = -34.01 m) und würde den Hof wieder öffnen.
_STRASSE_LAYER = re.compile(
    r"GEHSTEIG|GEHWEG|RANDSTEIN|BORDSTEIN", re.IGNORECASE)
_STRASSE_MM = 3000.0

# ── Innen-Zonen (Diagnose Rennweg U8, Slice S2) ──────────────────────────────
# Fachregel S-C: ein Raum liegt nie im Außenbereich. Owner-Entscheid F6
# Option 4 (Selman, 2026-09-15): innen ist ein Raum OHNE Ausschluss mit
# mindestens einem Grund. Vokabular und Regexe sind die der Diagnose-Metrik M2
# — aus ArchiCAD-Blocknamen EINER Familie abgeleitet, also familienabhängig.
_INNEN_TYPEN = frozenset({"WOHNZIMMER", "ZIMMER", "SCHLAFZIMMER", "KINDERZIMMER",
                          "BAD", "WC", "ABSTELLRAUM", "VORRAUM", "STIEGENHAUS"})
# Freiflächen sind nie Innen-Zone (S-C, F6). Sie werden nur NICHT geometrisch
# ausgeschnitten — die Nutzungsklasse AUSSEN von BALKON/TERRASSE bleibt, wie
# sie ist (F6-Zusatz unentschieden, kein Contract-Bump).
_FREI_TYPEN = frozenset({"TERRASSE", "BALKON", "LOGGIA"})
# Außen-Vokabular im Raumstempel schlägt jeden Grund: Möbel auf einer
# Freifläche (Rennweg EG „HOF/Terrasse" mit runden Tischen) dürfen sie nicht
# innen machen. Nur aus Rennweg abgeleitet — Mollgasse EIGENGARTEN/VORPLATZ
# hängen an genau dieser Liste.
_AUSSEN_STEMPEL = re.compile(
    r"HOF|ZUGANG|EINFAHRT|M(Ü|UE)LLPLATZ|GARTEN|VORPLATZ", re.IGNORECASE)
# ArchiCAD-Zonenstempel („Bad__4") sind Beschriftung, kein Einrichtungsobjekt.
_STEMPELBLOCK = re.compile(r"__\d+$")
_SANITAER = re.compile(
    r"(?<![a-z])WC(?![a-z])|WASCH(BECKEN|TISCH)|DUSCH|SHOWER|WANNE|BATHTUB|URINAL|SP(Ü|UE)LE"
    r"|(?<![a-z])SINK(?![a-z])|BIDET|TOILET", re.IGNORECASE)
_MOEBEL = re.compile(
    r"CHAIR|ST(U|Ü|UE)HL|TISCH|TABLE|SOFA|COUCH|BETT|(?<![a-z])BED(?![a-z])|SCHRANK|WARDROBE"
    r"|REGAL|K(Ü|UE)CHE|KITCHEN|KOCHFELD|PANEL TV|HOME-TRAINER|HANTELBANK|LAUFBAND"
    r"|R(Ü|UE)CKENTRAINER", re.IGNORECASE)
_BLOCK_TIEFE = 4         # Rekursionstiefe über virtual_entities (wie M2)
# Gebäudemaske für den Zuschnitt der Innen-Zonen: Komponenten der Wand-Union,
# geschlossen mit diesem Radius. ponytail: Knopf, an Rennweg gemessen (Diagnose
# B.2 — der DG2-Dachstreifen bis 1,27 m vor der Fassade bleibt draußen, alle
# echten Innen-Zonen liegen drin). Nachmessen, wenn eine Innen-Zone offen
# bleibt (Maske zu klein) oder ein Hof/Vorplatz gedeckt wird (zu groß), und
# vor dem Merge auf Barawitzka/Mollgasse/Muthgasse.
_MASKE_MM = 5000.0


@dataclass
class AussenBereiche:
    """Ergebnis der Außen-Analyse (Vektor-Geometrie in mm)."""

    komponenten: list[Polygon] = field(default_factory=list)   # Kontur je Trakt
    offen: list[Polygon] = field(default_factory=list)         # AUSSEN
    geschlossen: list[Polygon] = field(default_factory=list)   # AUSSEN_GESCHLOSSEN
    # Innen-Zonen (S2), auf die Gebäudemaske zugeschnitten.
    innen: list[Polygon] = field(default_factory=list)

    def gedeckt(self):
        """Fläche, die für die Türzuordnung als „nicht AUSSEN" gilt:
        alle Komponenten-Konturen minus der offenen Außenflächen, plus
        geschlossene Höfe (dort kein final_exit) und die Innen-Zonen — eine
        Zone außerhalb der Komponenten-Kontur bliebe sonst ungedeckt (S2)."""
        u = unary_union([*self.komponenten, *self.geschlossen, *self.innen])
        if self.offen:
            u = u.difference(unary_union(self.offen))
        return u


def aussen_indizien(plan: DxfPlan) -> list[XY]:
    """Punkte mit Außenanlagen-Indiz: Schwerpunkte von Hatches/Linien auf
    Außen-Layern + Baum-Block-Positionen (mm)."""
    out: list[XY] = []
    for e in plan.entities():
        t = e.dxftype()
        layer = str(e.dxf.layer)
        if t == "INSERT" and _BAUM_BLOCK.search(str(e.dxf.name)):
            out.append(plan._scale(e.dxf.insert))
        elif _AUSSEN_LAYER.search(layer):
            if t == "HATCH":
                try:
                    seeds = list(e.seeds) or None
                except Exception:  # noqa: BLE001 — kaputter Hatch liefert keinen Seed
                    seeds = None
                if seeds:
                    out.append(plan._scale(seeds[0]))
                else:
                    pts = plan.entity_points(e)
                    if pts:
                        out.append(pts[0])
            else:
                pts = plan.entity_points(e)
                if pts:
                    out.extend(pts[:2])
    return out


def _wand_geschlossen(koerper: list[Wandkoerper], d_mm: float):
    """Wand-Union, morphologisch geschlossen (Löcher bleiben Löcher).

    Vor dem Puffern vereinfacht + eckige Puffer (join_style mitre, quad_segs 2)
    — auf Muthgasse (836 Körper mit Kurven-Hatches) war der runde
    Doppel-Puffer sonst der Zeitfresser.
    """
    u = unary_union([Polygon(k.polygon_mm).buffer(0)
                     for k in koerper]).simplify(20.0)
    return u.buffer(d_mm, quad_segs=2).buffer(-d_mm, quad_segs=2)


def aussenkontur_komponenten(koerper: list[Wandkoerper],
                             d_mm: float = _SCHLIESS_MM) -> list[Polygon]:
    """Außenkontur JE zusammenhängender Gebäude-Komponente (Löcher gefüllt).

    Union der Wandkörper, morphologisch geschlossen (überbrückt Tür-/Fenster-
    öffnungen ≤ 2·d) — jede verbleibende Komponente ist ein Trakt.
    """
    if not koerper:
        return []
    return _komponenten_aus(_wand_geschlossen(koerper, d_mm))


def _komponenten_aus(wand_zu) -> list[Polygon]:
    geoms = (list(wand_zu.geoms) if isinstance(wand_zu, MultiPolygon)
             else [wand_zu])
    return [Polygon(g.exterior) for g in geoms
            if g.geom_type == "Polygon" and g.area >= 1e6]  # ≥1 m²


def grundstuecksgrenze(plan: DxfPlan, wand_zu=None) -> Polygon | None:
    """Grundstücksgrenze als Ring (mm) — der FLÄCHENGRUNDRISS des Projekts.

    Umfasst auch Garten, Innenhof und Vorplatz, nicht nur die bebaute Fläche.
    Layer-Muster UND Liniengeometrie sind beide Pflicht; offene Grenzzüge
    werden über Endpunkt-Paare < 400 mm gebrückt und polygonisiert.
    Plausibel nur, wenn der Ring ≥ 90 % der Wandfläche deckt — sonst None.

    Gemessen: Barawitzka 616.8 m², Mollgasse 1510.2 m²; Rennweg EG/OG3 und
    Muthgasse E2 → None.
    """
    ringe: list[Polygon] = []
    segmente: list[LineString] = []
    for e in plan.entities():
        if e.dxftype() not in _GRENZ_TYPEN:
            continue
        if not _GRENZ_LAYER.search(str(e.dxf.layer)):
            continue
        pts = plan.entity_points(e)
        if len(pts) < 2:
            continue
        zu = bool(getattr(e, "closed", False) or getattr(e, "is_closed", False))
        if zu and len(pts) >= 3:
            p = Polygon(pts).buffer(0)
            if not p.is_empty:
                ringe.append(p)
        else:
            segmente += [LineString(pts[i:i + 2]) for i in range(len(pts) - 1)]
    if segmente:
        enden = [p for s in segmente for p in (s.coords[0], s.coords[-1])]
        # ponytail: O(n²) über die Endpunkte — Grenzzüge haben Dutzende, nicht Tausende.
        bruecken = [LineString([a, b]) for a, b in combinations(enden, 2)
                    if 0 < Point(a).distance(Point(b)) < _BRUECKE_MM]
        ringe += list(polygonize(unary_union(segmente + bruecken)))
    if not ringe:
        return None
    ring = max(ringe, key=lambda p: p.area)
    if wand_zu is None:
        koerper = finde_wandkoerper(plan)
        if not koerper:
            return None
        wand_zu = _wand_geschlossen(koerper, _SCHLIESS_MM)
    if wand_zu.is_empty or ring.intersection(wand_zu).area < 0.9 * wand_zu.area:
        return None      # Ring deckt das Gebäude nicht → kein Grundstücksring
    return ring


def _strassenkante(plan: DxfPlan, rand):
    """Teile des Grenz-Randes ≤ 3 m von Geometrie auf einem Straßen-Layer.

    ``None`` = kein Straßen-Indiz im Plan (dann gilt der ganze Rand als
    Straßenkante); eine leere Geometrie = Indiz vorhanden, aber kein Kontakt.
    """
    geo = []
    for e in plan.entities():
        if not _STRASSE_LAYER.search(str(e.dxf.layer)):
            continue
        pts = plan.entity_points(e)
        if len(pts) >= 2:
            geo.append(LineString(pts))
        elif pts:
            geo.append(Point(pts[0]))
    if not geo:
        return None
    return rand.intersection(unary_union(geo).buffer(_STRASSE_MM))


def _teilflaechen(g) -> list[Polygon]:
    """Nicht-leere Polygon-Teile einer Geometrie (Union-/Differenz-Ergebnis)."""
    geoms = list(g.geoms) if hasattr(g, "geoms") else [g]
    return [p for p in geoms if p.geom_type == "Polygon" and not p.is_empty]


def _beleg_punkte(plan: DxfPlan) -> list[XY]:
    """Einfügepunkte (mm, WCS) aller Sanitär-/Möbel-Blöcke — rekursiv über
    ``virtual_entities`` bis ``_BLOCK_TIEFE``, EINMAL je Plan.

    Der Einfügepunkt liegt gemessen 391-836 mm neben der Block-Mitte; für die
    Raumzugehörigkeit reicht das. Zonenstempel-Blöcke zählen nicht.
    """
    out: list[XY] = []

    def _walk(entities, tiefe: int) -> None:
        for e in entities:
            if e.dxftype() != "INSERT":
                continue
            name = str(e.dxf.name)
            if not _STEMPELBLOCK.search(name) and (_SANITAER.search(name)
                                                   or _MOEBEL.search(name)):
                try:
                    p = e.ocs().to_wcs(e.dxf.insert)
                except Exception:  # noqa: BLE001 — kaputte OCS-Matrix: Rohpunkt
                    p = e.dxf.insert
                out.append(plan._scale(p))
            if tiefe < _BLOCK_TIEFE:
                try:
                    sub = list(e.virtual_entities())
                except Exception:  # noqa: BLE001, S112 — kaputter Block killt den Walk nicht
                    continue
                _walk(sub, tiefe + 1)

    _walk(plan.space, 0)
    return out


def waehle_innen_zonen(plan: DxfPlan, raeume: list[Raum],
                       zuordnungen: Sequence[Zuordnung] = ()) -> list[Polygon]:
    """Raumpolygone, die nie Außenbereich sein dürfen (Fachregel S-C).

    Owner-Entscheid F6 Option 4 (Selman, 2026-09-15): innen ist ein Raum ohne
    Ausschluss — Freiflächen-Typ oder Außen-Vokabular in einem zugeordneten
    Stempel — mit mindestens einem Grund: Typ aus ``_INNEN_TYPEN``,
    zugeordneter Raumstempel (auch untypisiert, „TV Raum") oder ein Sanitär-/
    Möbel-Block im Polygon.
    """
    stempel_je_raum: dict[str, list[str]] = {}
    for z in zuordnungen:
        if z.raum is not None:
            stempel_je_raum.setdefault(z.raum.id, []).append(z.stempel.name or "")
    zonen: list[Polygon] = []
    ohne_grund: list[Polygon] = []     # nur noch ein Block-Beleg kann sie tragen
    for r in raeume:
        if len(r.polygon_mm) < 3:
            continue
        typ = r.raum_typ or ""
        stempel = stempel_je_raum.get(r.id, [])
        if typ in _FREI_TYPEN or any(_AUSSEN_STEMPEL.search(n) for n in stempel):
            continue                   # Ausschluss hat Vorrang
        g = Polygon(r.polygon_mm).buffer(0)
        if g.is_empty:
            continue
        (zonen if (typ in _INNEN_TYPEN or stempel) else ohne_grund).append(g)
    if ohne_grund:
        punkte = _beleg_punkte(plan)
        zonen += [g for g in ohne_grund if any(g.covers(Point(p)) for p in punkte)]
    return zonen


def erkenne_aussenbereiche(plan: DxfPlan,
                           koerper: list[Wandkoerper],
                           innen_zonen: list[Polygon] | None = None) -> AussenBereiche:
    """Außen-Analyse: Komponenten-Konturen + offene/geschlossene Außenflächen.

    ``innen_zonen`` (aus ``waehle_innen_zonen``): Raumpolygone, die nie AUSSEN
    sein dürfen (S2) — sie fallen aus jedem freien Teil heraus und zählen als
    gedeckt. Ohne das Argument bleibt das Verhalten unverändert.
    """
    if not koerper:
        return AussenBereiche()
    # Geschlossene Wand-Union MIT Löchern — Höfe/Innenräume bleiben Löcher;
    # die Komponenten-Konturen sind ihre gefüllten Exterior-Ringe.
    wand_zu = _wand_geschlossen(koerper, _SCHLIESS_MM)
    komponenten = _komponenten_aus(wand_zu)
    if not komponenten:
        return AussenBereiche()
    # Diagnose Rennweg U8, Slice S2: Innen-Zonen auf die Gebäudemaske
    # zuschneiden — eine Zone, die über die Fassade hinausragt (Rennweg DG2:
    # Dachstreifen bis 1,27 m, U9/F5), darf den Außenraum nicht mit abdecken.
    innen = None
    if innen_zonen:
        maske = _komponenten_aus(_wand_geschlossen(koerper, _MASKE_MM))
        if maske:
            innen = unary_union(list(innen_zonen)).intersection(unary_union(maske))
            innen = None if innen.is_empty else innen
    # Bezug ist der Flächengrundriss bis zur Grundstücksgrenze; ohne Grenz-
    # Layer bleibt die konvexe Hülle der Fallback (Verhalten unverändert).
    grund = grundstuecksgrenze(plan, wand_zu)
    bezug = grund if grund is not None else unary_union(komponenten).convex_hull
    # Freie Fläche = Bezug minus Wand-Geometrie (MIT Löchern): enthält den
    # Raum zwischen den Trakten, Höfe (Löcher) UND Innenräume — letztere
    # filtert die Indiz-/Rand-Pflicht unten heraus.
    frei = bezug.difference(wand_zu)
    teile = _teilflaechen(frei)

    indizien = aussen_indizien(plan)
    rand = bezug.exterior
    kante = _strassenkante(plan, rand)
    if kante is None:
        kante = rand           # kein Straßen-Indiz → ganzer Rand zählt
    # Gefüllte Komponenten (+1 mm Rundung) für den Loch-Test unten.
    komp_u = unary_union(komponenten).buffer(1.0)
    offen: list[Polygon] = []
    geschlossen: list[Polygon] = []
    for t in teile:
        if t.area < _MIN_HOF_M2 * 1e6:
            continue
        hat_indiz = any(t.covers(Point(p)) for p in indizien)
        # Owner-Entscheid F7 (Selman, 2026-09-15): ein Loch der Komponenten
        # berührt den Rand nie, egal wie nah (Rennweg DG1/OG3: Innenraum-
        # Loch 193 mm vor der Hülle) — ohne Außen-Indiz ist es nie AUSSEN.
        ist_loch = t.within(komp_u)
        beruehrt_rand = not ist_loch and t.distance(rand) < _RAND_EPS_MM
        if not (hat_indiz or beruehrt_rand):
            continue                      # Loch/Innenraum ohne Außen-Indiz
        # Weg ins Freie ⇔ die Fläche reicht bis an die STRASSENKANTE, also aus
        # dem Flächengrundriss heraus auf öffentlichen Grund. Ein ringsum
        # ummauerter Innenhof erreicht sie nicht → AUSSEN_GESCHLOSSEN.
        # Der Engstellen-Test filtert Zeichnungs-Splitter (Haarrisse zwischen
        # Grenz- und Wandgeometrie), die den Rand sonst zufällig berühren.
        hals = t.buffer(-_HALS_MM).buffer(_HALS_MM + 20.0)
        weg_ins_freie = (not hals.is_empty and not kante.is_empty
                         and hals.distance(kante) < _RAND_EPS_MM)
        ziel = offen if weg_ins_freie else geschlossen
        # S2: Die Innen-Zonen fallen aus dem Teil heraus; die Reste erben
        # seinen Status — ein Rest wird nie neu „offen". Ein Rest unter der
        # Hof-Mindestfläche ist wie jede freie Fläche darunter keine
        # Außenfläche, sondern eine Nische: Raumpolygone enden an den
        # Wandflächen, die Türöffnung dazwischen gehört zu keinem Raum —
        # ohne den Deckel bleiben dort Splitter als AUSSEN stehen (Rennweg
        # OG3 gemessen: 1,99 m² in 8 Wandöffnungen).
        reste = _teilflaechen(t.difference(innen)) if innen is not None else [t]
        ziel.extend(r for r in reste if r.area >= _MIN_HOF_M2 * 1e6)
    return AussenBereiche(komponenten=komponenten, offen=offen,
                          geschlossen=geschlossen,
                          innen=_teilflaechen(innen) if innen is not None else [])


# ------------------------------------------------------------ Überdachungen

# Namensbasierte Vordach-Erkennung ist TOT: kein Plan trägt einen Layer/Block/
# Text VORDACH|ÜBERDACHUNG|AUSKRAGUNG|LAUBENGANG|ARKADE|PERGOLA|CANOPY.
# Einziges Signal ist ein NICHT flächendeckender Decken-Layer. Barawitzka
# nachgemessen: Decken-Union über diesem Regex 601.1 m² gegen 426.0 m²
# Gebäudefläche (Anteil 0.865); vom Layer '210 Decke' liegen 320.5 m²
# ausserhalb der Wand-Union. Der Schnitt mit den OFFENEN Außenflächen — das
# eigentliche Vordach-Signal — ist dort 0.752 m², größtes Stück 0.707 m² in
# 2.22 m Abstand zu final_exit exit_tuer_27.
_DECKE_LAYER = re.compile(r"DECKE|SLAB|CLNG|DACH", re.IGNORECASE)
# Ein flächendeckender Decken-Layer beschreibt die Geschossdecke, kein Vordach.
# Barawitzka liegt mit 0.865 knapp unter der Schwelle — die Regel steht dort auf
# 3.5 Prozentpunkten, das ist bewusst als Schwäche vermerkt (OFFENE_FRAGEN.md).
_DECKE_MAX_ANTEIL = 0.9
# 0.5 statt 1.0 m²: das einzige real gemessene Vordach (Barawitzka, über dem
# Eingangsvorbereich) misst 0.707 m² — bei 1.0 m² fiele genau der Fall weg,
# für den die Erkennung gebaut ist. ponytail: an EINEM Plan kalibriert.
_MIN_UEBERDACHUNG_M2 = 0.5


def ueberdachungen(plan: DxfPlan, gebaeude, aussen_offen) -> list[Polygon]:
    """Überdachte Teile der OFFENEN Außenflächen (Vordach vor dem Eingang).

    Reiner Prüfstrecken-Output (Bericht), KEIN Contract-Feld: Deckenflächen
    (Layer DECKE|SLAB|CLNG|DACH, geschlossene LW/POLYLINE + HATCH) geschnitten
    mit ``aussen_offen``, Teilflächen ≥ 0.5 m². Deckt der Layer ≥ 90 % der
    Gebäudefläche, ist er flächendeckend und trägt kein Vordach-Signal → [].
    """
    if gebaeude is None or gebaeude.is_empty or not aussen_offen:
        return []
    flaechen: list[Polygon] = []
    for e in plan.entities():
        t = e.dxftype()
        if not _DECKE_LAYER.search(str(e.dxf.layer)):
            continue
        if t == "HATCH":
            pts = _hatch_pfad_mm(plan, e)
        elif t in ("LWPOLYLINE", "POLYLINE") and (
                getattr(e, "closed", False) or getattr(e, "is_closed", False)):
            pts = plan.entity_points(e)
        else:
            continue
        if len(pts) >= 3:
            p = Polygon(pts).buffer(0)
            if not p.is_empty:
                flaechen.append(p)
    if not flaechen:
        return []
    decke = unary_union(flaechen)
    if decke.intersection(gebaeude).area >= _DECKE_MAX_ANTEIL * gebaeude.area:
        return []
    treffer = decke.intersection(unary_union(aussen_offen))
    teile = (list(treffer.geoms) if hasattr(treffer, "geoms")
             else ([treffer] if not treffer.is_empty else []))
    return [p for p in teile if p.geom_type == "Polygon"
            and p.area >= _MIN_UEBERDACHUNG_M2 * 1e6]
