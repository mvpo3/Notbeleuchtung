"""breitenprofil — TATSÄCHLICHE Breite entlang eines Fluchtwegs (Geometrie).

Drei Breitenbegriffe, die nie zusammenfallen dürfen (Enis, RL-4-Quellenblock
in ``normwissen/data/``, Abschnitt ``breiten_begriffe``; Dateiname hier
absichtlich nicht wörtlich — siehe ``docs/ENIS_UEBERGABE_0908.md`` § 3):

1. **erforderliche Mindestbreite** — OIB-RL 4 Kapitel 2. Anforderung an den
   Entwurf, Fertigmaß. Kommt in diesem Modul NICHT vor: kein Normwert wird
   hier eingesetzt, weder als Default noch als Fallback.
2. **örtliche Engstelle** — ein einzelner Messwert. Wird getrennt geführt
   (``Breitenprofil.engstellen``) und reduziert NIE die Abschnittsbreite.
3. **tatsächliche Breite entlang des Weges** — Profil (alle 100 mm) bzw.
   abschnittsweise konstante Werte (``abschnitte``). Das ist, was dieses
   Modul misst.

Fehlt eine Messung, ist sie ``None`` MIT Grund — nie ein ersatzweise
angenommener Wert.

Kein Contract-Touch: ``Breitenprofil`` ist der Rückgabetyp dieses Moduls. Es
füllt die in ``docs/proposals/WEGBREITE_RANDSTREIFEN.md`` §2 benannte Lücke
(„belegte Wegbreite je Fluchtweg-Abschnitt"); die Contract-Ergänzung dazu ist
VORSCHLAG, nicht eingebaut.
"""
from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field
from itertools import pairwise

from shapely.geometry import LineString, MultiLineString, Point
from shapely.geometry.base import BaseGeometry

XY = tuple[float, float]

SCHRITT_MM = 100.0        # Abtastung entlang der Achse
TOLERANZ_MM = 100.0       # Breitenband eines Abschnitts konstanter Breite
MIN_ABSCHNITT_MM = 500.0  # kürzer = keine eigene Abschnittsbreite
TUER_RADIUS_MM = 400.0    # Abtastpunkt gilt als Türdurchgang
ECKE_MIN_GRAD = 20.0      # darunter Stützpunkt-Rauschen, keine echte Ecke
ECKE_FENSTER_MM = 500.0   # Fenster, über das der Knick gemessen wird


@dataclass(frozen=True)
class Messpunkt:
    """Ein Abtastpunkt: Breite SENKRECHT zur Achse. ``breite_mm=None`` = keine
    Messung, ``grund`` sagt warum."""

    laufmeter_mm: float
    xy_mm: XY
    breite_mm: float | None
    ist_tuerdurchgang: bool = False
    an_richtungswechsel: bool = False
    grund: str | None = None


@dataclass(frozen=True)
class Abschnitt:
    """Abschnitt konstanter Breite (± ``TOLERANZ_MM``)."""

    von_mm: float
    bis_mm: float
    breite_mm: float
    quelle: str = "gemessen"   # Audit-Trail; NIE ein Normwert

    @property
    def laenge_mm(self) -> float:
        return self.bis_mm - self.von_mm


@dataclass(frozen=True)
class Engstelle:
    """Lokales Minimum innerhalb eines Abschnitts — ZUSÄTZLICHE Angabe."""

    position_mm: float
    xy_mm: XY
    breite_mm: float
    laenge_mm: float


@dataclass(frozen=True)
class Breitenprofil:
    segment_id: str
    laenge_mm: float
    profil: list[Messpunkt] = field(default_factory=list)
    abschnitte: list[Abschnitt] = field(default_factory=list)
    engstellen: list[Engstelle] = field(default_factory=list)
    tuerpunkte: list[Messpunkt] = field(default_factory=list)
    breite_min_mm: float | None = None   # schmalste GEMESSENE Stelle (ohne Tür)
    messbar: bool = False
    # Grund für fehlende (messbar=False) bzw. eingeschränkte Auswertung
    # (messbar=True, aber kein Abschnitt über der Mindestlänge).
    grund: str | None = None


# ── Messung ──────────────────────────────────────────────────────────────────
def _median(werte: list[float]) -> float:
    s = sorted(werte)
    m = len(s) // 2
    return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2


def _achse(polyline_mm: list[XY]) -> LineString | None:
    pts = [(float(x), float(y)) for x, y in polyline_mm]
    entdoppelt = [p for i, p in enumerate(pts) if i == 0 or p != pts[i - 1]]
    if len(entdoppelt) < 2:
        return None
    linie = LineString(entdoppelt)
    return linie if linie.length > 0 else None


def _richtung(linie: LineString, s: float) -> XY:
    """Einheits-Tangente bei Laufmeter s, als SEHNE über ein Fenster gemessen.

    Die lokale Tangente eines Skelett-Stützpunkts kippt um bis zu 15 Grad
    (Zickzack von wenigen Millimetern); die Normale steht dann schief und misst
    systematisch zu breit (1200 mm → 1224 mm). Die Sehne mittelt das weg.
    """
    a = linie.interpolate(max(0.0, s - ECKE_FENSTER_MM / 2))
    b = linie.interpolate(min(linie.length, s + ECKE_FENSTER_MM / 2))
    dx, dy = b.x - a.x, b.y - a.y
    n = math.hypot(dx, dy)
    return (dx / n, dy / n) if n else (1.0, 0.0)


def _innere_vertex_laufmeter(linie: LineString) -> list[float]:
    """Laufmeter der ECHTEN Richtungswechsel (Knickwinkel > ``ECKE_MIN_GRAD``).

    Skelett-Polylinien (GRAPH-Segmente) haben alle paar Zentimeter einen
    Stützpunkt mit Mini-Zickzack; die sind keine Ecken und dürfen das Profil
    nicht wegfiltern.
    """
    coords = list(linie.coords)
    out: list[float] = []
    s = 0.0
    for a, b in pairwise(coords[:-1]):
        s += math.dist(a, b)
        # Knick über ein FENSTER messen, nicht zwischen Nachbar-Stützpunkten:
        # ein Zickzack von 20 mm auf 200 mm ergibt sonst 22 Grad je Stützpunkt.
        vor = linie.interpolate(max(0.0, s - ECKE_FENSTER_MM))
        nach = linie.interpolate(min(linie.length, s + ECKE_FENSTER_MM))
        v1 = (b[0] - vor.x, b[1] - vor.y)
        v2 = (nach.x - b[0], nach.y - b[1])
        n1, n2 = math.hypot(*v1), math.hypot(*v2)
        if not n1 or not n2:
            continue
        cos = max(-1.0, min(1.0, (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2)))
        if math.degrees(math.acos(cos)) > ECKE_MIN_GRAD:
            out.append(s)
    return out


def _teilflaechen(flaeche: BaseGeometry | Sequence[BaseGeometry]
                  ) -> list[BaseGeometry]:
    """Begrenzende Flächen als Liste — NICHT vereinigt.

    Räume im RaumModell überlappen einander (Halle über Gang, Wandstärke doppelt
    belegt). Eine Vereinigung würde genau die Wandkante schlucken, die den Gang
    begrenzt; deshalb bleibt jede Fläche für sich und es gilt die NÄCHSTE Kante.
    """
    if isinstance(flaeche, BaseGeometry):
        geoms = getattr(flaeche, "geoms", None)
        return [g for g in (geoms if geoms is not None else [flaeche])
                if not g.is_empty]
    return [g for g in flaeche if g is not None and not g.is_empty]


def _breite_an(teile_flaeche: list[BaseGeometry], p: Point, n: XY,
               reichweite: float) -> tuple[float | None, str | None]:
    """Distanz zwischen den begrenzenden Wandkanten: Länge des Flächen-Schnitts
    der Normalen durch p, über alle Teilflächen die ENGSTE (= nächste Kanten)."""
    treffend = [f for f in teile_flaeche if f.covers(p)]
    if not treffend:
        return None, "punkt_ausserhalb_flaeche"
    strahl = LineString([
        (p.x - n[0] * reichweite, p.y - n[1] * reichweite),
        (p.x + n[0] * reichweite, p.y + n[1] * reichweite),
    ])
    breiten: list[float] = []
    for f in treffend:
        schnitt = f.intersection(strahl)
        if schnitt.is_empty:
            continue
        teile = (list(schnitt.geoms) if isinstance(schnitt, MultiLineString)
                 else [schnitt])
        treffer = [t.length for t in teile
                   if isinstance(t, LineString) and t.distance(p) <= 1e-6]
        if treffer:
            breiten.append(max(treffer))
    if not breiten:
        return None, "wandkante_fehlt"
    breite = min(breiten)
    if breite >= 2 * reichweite - 1e-6:
        return None, "wandkante_fehlt"   # Fläche offen: keine zweite Kante
    return breite, None


def miss_breitenprofil(
    segment_id: str,
    polyline_mm: list[XY],
    flaeche: BaseGeometry | Sequence[BaseGeometry] | None,
    tueren_mm: list[XY] | None = None,
    *,
    schritt_mm: float = SCHRITT_MM,
    toleranz_mm: float = TOLERANZ_MM,
    min_abschnitt_mm: float = MIN_ABSCHNITT_MM,
) -> Breitenprofil:
    """Misst den Breitenverlauf entlang ``polyline_mm`` innerhalb ``flaeche``.

    ``flaeche`` = begrenzende lichte Fläche(n): ein Polygon oder eine Liste
    (die durchlaufenen Raumpolygone — NICHT vereinigen, s. ``_teilflaechen``).
    ``tueren_mm`` = Türpositionen; Abtastpunkte dort werden als eigener
    Punkt geführt und gehen NICHT in Abschnitte/Engstellen ein.
    """
    achse = _achse(polyline_mm)
    if achse is None:
        return Breitenprofil(segment_id, 0.0, grund="achse_nicht_ermittelbar")
    teile_flaeche = [] if flaeche is None else _teilflaechen(flaeche)
    if not teile_flaeche:
        return Breitenprofil(segment_id, achse.length, grund="flaeche_fehlt")

    xs = [c for f in teile_flaeche for c in f.bounds]
    minx, miny = min(xs[0::4]), min(xs[1::4])
    maxx, maxy = max(xs[2::4]), max(xs[3::4])
    reichweite = math.dist((minx, miny), (maxx, maxy)) + schritt_mm
    tuerpunkte_geo = [Point(x, y) for x, y in (tueren_mm or [])]

    roh: list[Messpunkt] = []
    # ponytail: ein Strahlschnitt je 100 mm, O(n·Kanten) — genügt für Gänge,
    # bei ganzen Geschossen ggf. auf ein vorbereitetes STRtree-Raster wechseln.
    anzahl = int(achse.length // schritt_mm) + 1
    for i in range(anzahl + 1):
        s = min(i * schritt_mm, achse.length)
        p = achse.interpolate(s)
        dx, dy = _richtung(achse, s)
        breite, grund = _breite_an(teile_flaeche, p, (-dy, dx), reichweite)
        roh.append(Messpunkt(round(s, 1), (round(p.x, 1), round(p.y, 1)),
                             None if breite is None else round(breite, 1),
                             grund=grund))
        if s >= achse.length:
            break

    profil = _markiere(roh, achse, tuerpunkte_geo, toleranz_mm)
    gang = [m for m in profil if m.breite_mm is not None
            and not m.ist_tuerdurchgang and not m.an_richtungswechsel]
    if not gang:
        ohne = [m for m in profil if m.breite_mm is None]
        gruende = ({m.grund for m in ohne if m.grund} if len(ohne) == len(profil)
                   else {"nur_tuer_oder_eckpunkte"})
        return Breitenprofil(segment_id, achse.length, profil=profil,
                             tuerpunkte=[m for m in profil if m.ist_tuerdurchgang],
                             grund="+".join(sorted(gruende)))

    abschnitte = _abschnitte(gang, toleranz_mm, min_abschnitt_mm)
    return Breitenprofil(
        segment_id=segment_id,
        laenge_mm=round(achse.length, 1),
        profil=profil,
        abschnitte=abschnitte,
        engstellen=_engstellen(gang, abschnitte, toleranz_mm),
        tuerpunkte=[m for m in profil if m.ist_tuerdurchgang],
        breite_min_mm=min(m.breite_mm for m in gang),
        messbar=True,
        grund=None if abschnitte else "kein_abschnitt_ueber_mindestlaenge",
    )


def _markiere(roh: list[Messpunkt], achse: LineString,
              tueren: list[Point], toleranz: float) -> list[Messpunkt]:
    """Türdurchgänge und Richtungswechsel kennzeichnen.

    * Türdurchgang: die schmalsten Punkte im ``TUER_RADIUS_MM`` um eine Tür —
      die Durchgangslichte, KEINE Gangbreite.
    * Richtungswechsel: an einer Ecke steht die Normale in den anderen
      Schenkel; der Messwert ist dort die Öffnung der Ecke, nicht die Breite
      des Gangs. Kriterium selbstskalierend: Abstand zur Ecke kleiner als die
      dort gemessene Breite.
    Beide Sorten bleiben im Profil (der Messwert ist echt), gehen aber nicht in
    Abschnitte, Engstellen oder ``breite_min_mm`` ein.

    ponytail: das Eckfenster skaliert mit der DORT gemessenen (an der Ecke also
    aufgeblähten) Breite — bei einer Ecke in einen Saal fällt viel Profil weg.
    Konservativ (verwirft, erfindet nie); wenn die Abdeckung stört, Fenster aus
    der Gangbreite der Nachbarpunkte statt aus dem Eckwert bilden.
    """
    tuer_idx: set[int] = set()
    for t in tueren:
        nah = [i for i, m in enumerate(roh)
               if m.breite_mm is not None
               and Point(m.xy_mm).distance(t) <= TUER_RADIUS_MM]
        if not nah:
            continue
        eng = min(roh[i].breite_mm for i in nah)
        tuer_idx.update(i for i in nah if roh[i].breite_mm <= eng + toleranz)

    ecken = _innere_vertex_laufmeter(achse)
    gemessen = [m.breite_mm for i, m in enumerate(roh)
                if m.breite_mm is not None and i not in tuer_idx]
    # Fenster = lokale Breite, aber GEDECKELT auf die halbe typische Breite des
    # Segments. Ohne Deckel löscht eine Ecke in einen 5,8-m-Raum ±5,8 m Profil
    # (Rennweg_EG: 61 von 68 Punkten), ohne die lokale Breite verliert man
    # umgekehrt die schmalen Punkte in weiten Segmenten.
    deckel = _median(gemessen) / 2 if gemessen else 0.0
    return [
        Messpunkt(
            m.laufmeter_mm, m.xy_mm, m.breite_mm,
            ist_tuerdurchgang=i in tuer_idx,
            an_richtungswechsel=(
                m.breite_mm is not None and i not in tuer_idx
                and any(abs(m.laufmeter_mm - e) < min(m.breite_mm, deckel)
                        for e in ecken)
            ),
            grund=m.grund,
        )
        for i, m in enumerate(roh)
    ]


# ── Abschnitte konstanter Breite ─────────────────────────────────────────────
def _abschnitte(gang: list[Messpunkt], toleranz: float,
                min_laenge: float) -> list[Abschnitt]:
    """Greedy: Lauf erweitern, solange die Spanne im Toleranzband bleibt. Zu
    kurze Läufe (Engstellen, Aufweitungen < ``min_laenge``) bekommen KEINE
    eigene Abschnittsbreite, sie werden dem Nachbarn zugeschlagen — dessen
    Breite bleibt unverändert."""
    laeufe: list[list[Messpunkt]] = []
    for m in gang:
        if laeufe:
            werte = [x.breite_mm for x in laeufe[-1]] + [m.breite_mm]
            if max(werte) - min(werte) <= toleranz:
                laeufe[-1].append(m)
                continue
        laeufe.append([m])

    breiten = [_median([x.breite_mm for x in lauf]) for lauf in laeufe]
    behalten = [i for i, lauf in enumerate(laeufe)
                if lauf[-1].laufmeter_mm - lauf[0].laufmeter_mm >= min_laenge]
    if not behalten:
        return []   # kein Lauf erreicht die Mindestlänge → keine Abschnittsbreite

    # Grenzen: jeder zu kurze Lauf fällt an den nächstgelegenen behaltenen.
    grenzen: list[tuple[float, float, float]] = []
    for i in behalten:
        von, bis, breite = (laeufe[i][0].laufmeter_mm,
                            laeufe[i][-1].laufmeter_mm, breiten[i])
        if grenzen and abs(grenzen[-1][2] - breite) <= toleranz:
            # gleiche Breite links und rechts einer kurzen Störstelle → EIN
            # Abschnitt; die Störstelle wird als Engstelle geführt.
            v0, _, b0 = grenzen[-1]
            grenzen[-1] = (v0, bis, b0)
            continue
        grenzen.append((von, bis, breite))
    out: list[Abschnitt] = []
    for k, (von, bis, breite) in enumerate(grenzen):
        v = gang[0].laufmeter_mm if k == 0 else (grenzen[k - 1][1] + von) / 2
        b = gang[-1].laufmeter_mm if k == len(grenzen) - 1 else (bis + grenzen[k + 1][0]) / 2
        out.append(Abschnitt(round(v, 1), round(b, 1), round(breite, 1)))
    return out


def _engstellen(gang: list[Messpunkt], abschnitte: list[Abschnitt],
                toleranz: float) -> list[Engstelle]:
    """Zusammenhängende Punkte, die ihren Abschnitt um mehr als die Toleranz
    unterschreiten."""
    def breite_des_abschnitts(s: float) -> float | None:
        for a in abschnitte:
            if a.von_mm <= s <= a.bis_mm:
                return a.breite_mm
        return None

    out: list[Engstelle] = []
    gruppe: list[Messpunkt] = []
    for m in [*gang, None]:
        soll = None if m is None else breite_des_abschnitts(m.laufmeter_mm)
        eng = m is not None and soll is not None and m.breite_mm < soll - toleranz
        if eng:
            gruppe.append(m)
            continue
        if len(gruppe) >= 2:      # Einzelpunkt am Rand = Rauschen, keine Engstelle
            tiefster = min(gruppe, key=lambda x: x.breite_mm)
            out.append(Engstelle(
                position_mm=tiefster.laufmeter_mm,
                xy_mm=tiefster.xy_mm,
                breite_mm=tiefster.breite_mm,
                laenge_mm=round(gruppe[-1].laufmeter_mm - gruppe[0].laufmeter_mm, 1),
            ))
        gruppe = []
    return out
