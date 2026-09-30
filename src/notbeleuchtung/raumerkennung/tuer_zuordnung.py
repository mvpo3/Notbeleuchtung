"""tuer_zuordnung — Türen an Räume anschließen (füllt ``Tuer.von_raum/nach_raum``).

Je Tür wird beidseits der Türsehne in Stufen (100/200/300/500 mm) senkrecht
geprobt, welcher Raum den Probepunkt deckt: die erste getroffene FREMDE
Raumfläche je Seite zählt. Übersprungen werden Stufen im Wandkörper und Stufen
im „eigenen" Raum — dem Raum, der den Türpunkt selbst deckt, weil gestempelte
Raumpolygone durch die Türöffnung ragen. Findet eine Seite keinen fremden Raum,
fällt sie auf den eigenen zurück (höchstens eine Seite, sonst stünde beidseits
derselbe Raum). Die Sehne kommt aus dem ``winkel_grad`` der nächsten Türöffnung
(INSERT-Rotation bzw. ARC-Startwinkel), sonst aus der nächsten Raumkante.
Seiten ohne Raum: ``AUSSEN`` (außerhalb der Gebäude-Außenkontur) oder
``KEIN_RAUM`` — letzteres wird als ``seite_fehlt`` gemeldet statt still
hingenommen. Nachschritt ``andere_bogenrichtung`` (S4c Fassung A): bleibt an
einer Bogentür eine Seite ``KEIN_RAUM``, wird die Sehne aus dem ENDwinkel
probiert — übernommen nur, wenn dadurch ein sonst verbindungsloser Raum
angeschlossen wird.

Zusätzlich: Wandöffnungen ab 800 mm Nennmaß (gemessen ≥ 797 mm, s. Schwelle)
zwischen zwei Räumen ohne Bogen/Block (``durchgaenge_ohne_tuerblatt``) werden
als ``Tuer(ohne_tuerblatt=True)`` ergänzt — die Kontaktzone zweier Raumpolygone
minus Wandflächen ist die Öffnung. Gewertet wird nur ein freier Streifen, der
BEIDE Raumpolygone berührt (Querungskriterium, Slice S5b); die Breite ist die
Länge der gemeinsamen Grenze, nicht die Rechtecklänge des Streifens. Ein
Streifen, der die Sehne einer Block-Tür desselben Raumpaars überlappt, ist die
Öffnung DIESER Tür und entfällt (Dublette).
"""
from __future__ import annotations

import math
from itertools import pairwise

from shapely.geometry import LineString, Point, Polygon
from shapely.prepared import prep

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer

from .tueren import TuerOeffnung

XY = tuple[float, float]

AUSSEN = "AUSSEN"
KEIN_RAUM = "KEIN_RAUM"

# Probeabstände senkrecht zur Türsehne. Eine feste Probe traf bei Sehnen auf
# der Wandflanke (ArchiCAD) je nach Wanddicke die Wand statt des Nachbarraums;
# die Stufen laufen von der Flanke bis hinter eine 500-mm-Wand.
_PROBE_STUFEN_MM = (100.0, 200.0, 300.0, 500.0)
_OEFFNUNG_SUCH_MM = 1500.0  # Türöffnung muss so nah an der Tür liegen
_DURCHGANG_MIN_MM = 800.0
_KONTAKT_MM = 250.0        # halbe Wanddicke für die Kontaktzone zweier Räume
_TUER_NAH_MM = 600.0       # bestehende Tür „deckt" eine Öffnung in diesem Radius
_KONTAKT_TOL_MM = 1.0      # „berührt den Raum" (Quellpräzision der Polygone)
# Dünner als das quert ein Streifen nicht. Unterer Anker ist synthetisch: das
# 2-mm-Band von ``test_splitter_quert_nicht``; die realen 2-mm-Bänder der
# Diagnose U13 haben einen Wandkörper und scheitern schon am Kontaktkriterium.
# 50,0 → 25,0 härtet nur die Reserve des geforderten Übergangs Rennweg OG1
# O01/O02 (50,0-mm-Band, 60 000 mm² frei, 1198,06 mm breit): 0,16 % → 100,3 %;
# über 11 gemessene Pläne dreht die Absenkung KEINE Entscheidung. Preis: die
# Regel wirkt als Abstandsdeckel d ≤ 500 − _SPLITTER_MM, der von 450 auf 475 mm
# wandert — fehlt zwischen zwei Räumen 451…475 mm der Wandkörper, entsteht
# jetzt ein raumlanger Durchgang (synthetisch: 460 mm → mit 50,0 keiner, mit
# 25,0 einer über 3998 mm; 476 mm → keiner); bei d ≤ 450 galt das schon immer.
# ponytail: feste Kontaktzone der Dicke 2 · _KONTAKT_MM − d; Öffnungen in Wänden
# dicker als 475 mm queren NIE. Ausbaupfad: Zone abstandsabhängig puffern.
_SPLITTER_MM = 25.0
_UEBERLAPPUNG_TOL_MM2 = 1.0  # darunter ist „Überlappung" Berührungsrauschen


def _raum_polys(raeume: list[Raum]) -> list[tuple[Raum, Polygon, object]]:
    out = []
    for r in raeume:
        if len(r.polygon_mm) >= 3:
            p = Polygon(r.polygon_mm).buffer(0)
            if not p.is_empty:
                out.append((r, p, prep(p)))
    return out


def _kanten_richtung(xy: XY, polys) -> float:
    """Richtung (rad) der nächsten Raumkante — Sehnen-Fallback ohne Öffnung."""
    best_d, best_w = math.inf, 0.0
    pt = Point(xy)
    for _, p, _pp in polys:
        ring = list(p.exterior.coords)
        for a, b in pairwise(ring):
            seg_len = math.dist(a, b)
            if seg_len < 1.0:
                continue
            # Punkt-Segment-Abstand
            t = max(0.0, min(1.0, ((xy[0] - a[0]) * (b[0] - a[0])
                                   + (xy[1] - a[1]) * (b[1] - a[1])) / seg_len**2))
            proj = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
            d = pt.distance(Point(proj))
            if d < best_d:
                best_d = d
                best_w = math.atan2(b[1] - a[1], b[0] - a[0])
    return best_w


def _naechste_oeffnung(tuer: Tuer, oeffnungen: list[TuerOeffnung]):
    """Nächste Türöffnung MIT Sehnenwinkel, höchstens ``_OEFFNUNG_SUCH_MM`` weit."""
    best, best_d = None, _OEFFNUNG_SUCH_MM
    for o in oeffnungen:
        if o.winkel_grad is None:
            continue
        d = math.dist(o.xy_mm, tuer.xy_mm)
        if d < best_d:
            best, best_d = o, d
    return best


def _sehnen_richtung(tuer: Tuer, oeffnungen: list[TuerOeffnung], polys) -> float:
    best = _naechste_oeffnung(tuer, oeffnungen)
    if best is not None:
        return math.radians(best.winkel_grad)
    return _kanten_richtung(tuer.xy_mm, polys)


def _raum_an(xy: XY, polys) -> Raum | None:
    for r, _p, pp in polys:
        if pp.covers(Point(xy)):
            return r
    return None


def _seite(xy: XY, normale: XY, sgn: float, polys, kontur, wand,
           eigen: Raum | None) -> tuple[str, bool]:
    """Eine Seite der Tür proben → (Ergebnis, „eigener Raum berührt").

    Je Stufe: liegt der Punkt in einem Wandkörper, zählt er nicht (die Wand ist
    weder Raum noch Freiland). Ebenso wenig zählt ``eigen`` — der Raum, der den
    TÜRPUNKT deckt: gestempelte Raumpolygone ragen durch die Türöffnung, und
    gemessen an Barawitzka/Mollgasse/Muthgasse traf die 100/200-mm-Stufe dann
    beidseits denselben Raum. Erst ein FREMDER Raum entscheidet die Seite.

    Liegt der Punkt außerhalb der gedeckten Kontur, wird AUSSEN gemerkt — aber
    NICHT sofort entschieden: gemessen am Rennweg OG1 liegt der 100-mm-Punkt
    einer Zimmertür 20 mm außerhalb der Kontur und 20 mm neben dem Raum, der
    ihn bei 200 mm deckt. Ein Raum schlägt AUSSEN also über alle Stufen; AUSSEN
    bleibt, wenn keine Stufe einen fremden Raum findet.
    """
    draussen = eigen_beruehrt = False
    for stufe in _PROBE_STUFEN_MM:
        p = Point(xy[0] + sgn * stufe * normale[0], xy[1] + sgn * stufe * normale[1])
        if wand is not None and wand.covers(p):
            continue
        r = _raum_an((p.x, p.y), polys)
        if r is not None and r is eigen:
            eigen_beruehrt = True
            continue
        if r is not None:
            return r.id, eigen_beruehrt
        if kontur is not None and not kontur.covers(p):
            draussen = True
    return (AUSSEN if draussen else KEIN_RAUM), eigen_beruehrt


def _prep(geom):
    return prep(geom) if geom is not None and not geom.is_empty else None


def _proben(t: Tuer, w: float, polys, kontur, wand) -> list[str]:
    """Beide Seiten der Tür quer zur Sehnenrichtung ``w`` (rad) → [von, nach].

    Rückfall auf den eigenen Raum: eine Seite, die bis zur letzten Stufe
    keinen fremden Raum findet, gehört dem Raum, der den Türpunkt deckt.
    HÖCHSTENS eine Seite — sonst stünde beidseits derselbe Raum. Vorrang hat
    die Seite, deren Probe den eigenen Raum wirklich berührt hat; AUSSEN ist
    ein Befund und fällt nicht zurück.
    """
    normale = (-math.sin(w), math.cos(w))   # Normale zur Sehne
    eigen = _raum_an(t.xy_mm, polys)
    proben = [_seite(t.xy_mm, normale, sgn, polys, kontur, wand, eigen)
              for sgn in (1.0, -1.0)]
    seiten = [p[0] for p in proben]
    if eigen is not None:
        for i in ((0, 1) if proben[0][1] else (1, 0)):
            if seiten[i] == KEIN_RAUM and seiten[1 - i] != eigen.id:
                seiten[i] = eigen.id
    return seiten


def ordne_tueren(tueren: list[Tuer], oeffnungen: list[TuerOeffnung],
                 raeume: list[Raum], aussenkontur, wand_union_geom=None,
                 fehlende_seiten: list | None = None) -> list[Tuer]:
    """Füllt ``von_raum``/``nach_raum`` jeder Tür in-place (Rückgabe = Eingabe).

    ``aussenkontur`` = „gedeckte" Fläche (Polygon/MultiPolygon): was sie NICHT
    deckt, ist AUSSEN — seit der Außen-Analyse auch offene Höfe zwischen den
    Gebäude-Komponenten. ``wand_union_geom`` (optional) lässt Probepunkte IM
    Wandkörper überspringen; ohne sie gelten dieselben Stufen ohne Übersprung.
    Bereits gesetzte Zuordnungen bleiben unverändert.

    ``fehlende_seiten`` sammelt (Tür, „+"/„-", letzte Stufe) für jede Seite, die
    bis zur letzten Stufe weder Raum noch AUSSEN fand — der Aufrufer macht
    daraus seinen Klartext (der Contract ``Tuer`` führt kein ``seite_fehlt``).
    """
    polys = _raum_polys(raeume)
    kontur, wand = _prep(aussenkontur), _prep(wand_union_geom)
    for t in tueren:
        if t.von_raum is not None and t.nach_raum is not None:
            continue
        seiten = _proben(t, _sehnen_richtung(t, oeffnungen, polys), polys,
                         kontur, wand)
        if fehlende_seiten is not None:
            fehlende_seiten += [
                (t, zeichen, _PROBE_STUFEN_MM[-1])
                for zeichen, seite in zip(("+", "-"), seiten, strict=True)
                if seite == KEIN_RAUM]
        t.von_raum, t.nach_raum = seiten[0], seiten[1]
    return tueren


def andere_bogenrichtung(tueren: list[Tuer], oeffnungen: list[TuerOeffnung],
                         raeume: list[Raum], aussenkontur,
                         wand_union_geom=None) -> list[Tuer]:
    """Nachschritt: die andere Bogenrichtung nur für verbindungslose Räume.

    S4c Fassung A (Owner 2026-09-30, docs/GATE_TUERSTAPEL.md § 10c ``xsehne3``).
    Die Sehne aus dem ARC-STARTwinkel zeigt bei manchen Bogentüren auf das
    offene Blatt; die Normale läuft dann entlang der Wand und eine Seite bleibt
    ``KEIN_RAUM`` (Barawitzka EG ``tuer_17`` vor dem ABSTELLRAUM 1,98, Gate
    (10)). Für eine Tür mit GENAU einer zugeordneten Seite wird die Sehne aus
    dem ENDwinkel (``blatt_enden[1]`` der nächsten Öffnung) geprobt und nur
    übernommen, wenn die zugeordnete Seite bleibt und die neue Seite ein Raum
    ist, der im ganzen Modell OHNE jede Verbindung wäre (keine Tür, kein
    Durchgang, keine Außenöffnung). Nicht begehbare Räume (SCHACHT/LIFT,
    Klasse KEIN_RAUM) und untypisierte ``rest``-Flächen sind keine Zielseite.
    Läuft darum NACH den Durchgängen. Rückgabe: die umgehängten Türen.

    ponytail: füllt nur Lücken, korrigiert die Sehne nicht allgemein — Türen
    mit beiden Seiten ``KEIN_RAUM`` oder falschem Raumpaar bleiben (§ 10c
    Grenzen), und bekommt der Zielraum anderswo eine Verbindung, gilt wieder
    der Startwinkel. Ausbaupfad: Sehne aus dem geschlossenen Blatt (eigener
    Slice mit Vorraum-Fehlklasse).
    """
    from .nutzungsklasse import nutzungsklasse_fuer
    verbunden = {s for t in tueren for s in (t.von_raum, t.nach_raum)}
    frei = {r.id for r in raeume if r.id not in verbunden
            and nutzungsklasse_fuer(r.raum_typ) != KEIN_RAUM
            and not (r.id.startswith("rest_") and not r.raum_typ)}
    if not frei:
        return []
    polys = _raum_polys(raeume)
    kontur, wand = _prep(aussenkontur), _prep(wand_union_geom)
    out: list[Tuer] = []
    for t in tueren:
        alt = [s for s in (t.von_raum, t.nach_raum) if s != KEIN_RAUM]
        if len(alt) != 1:
            continue
        o = _naechste_oeffnung(t, oeffnungen)
        if o is None or o.blatt_enden is None:
            continue
        e = o.blatt_enden[1]
        w = math.atan2(e[1] - o.xy_mm[1], e[0] - o.xy_mm[0])
        seiten = _proben(t, w, polys, kontur, wand)
        neu = [s for s in seiten if s != alt[0]]
        if alt[0] in seiten and len(neu) == 1 and neu[0] in frei:
            t.von_raum, t.nach_raum = seiten[0], seiten[1]
            out.append(t)
    return out


def _sehnen_zonen(tueren: list[Tuer], oeffnungen: list[TuerOeffnung]):
    """(gepufferte Sehne, Raumpaar) je Block-Tür mit Breite — Dubletten-Probe.

    Die Sehne ist ``xy_mm`` ± halbe Breite entlang ``winkel_grad`` der nächsten
    Öffnung, gepuffert um die halbe Wanddicke (``_KONTAKT_MM``), weil die Sehne
    auf einer Wandflanke liegen kann. Der Puffer ist FLACH (``cap_style="flat"``,
    nur quer zur Sehne): rund verlängert er die Zone um 250 mm über jedes
    Sehnenende hinaus und verschluckt eine echte Öffnung neben der Tür, sobald
    der Pfeiler dazwischen dünner als 250 mm ist (synthetisch belegt, 180 mm).

    Ohne gemessenen Sehnenwinkel gibt es KEINE Zone — der Kanten-Fallback von
    ``_sehnen_richtung`` wäre hier geraten, und eine geratene Sehne darf keinen
    Durchgang löschen. Türen ohne messbare Breite (Schiebetür) bleiben
    ebenfalls draußen: für sie gilt weiter allein die 600-mm-Regel.
    """
    zonen = []
    for t in tueren:
        if t.quelle != "block" or not t.breite_mm:
            continue
        o = _naechste_oeffnung(t, oeffnungen)
        if o is None:
            continue
        w = math.radians(o.winkel_grad)
        halb = t.breite_mm / 2.0
        sehne = LineString([
            (t.xy_mm[0] - halb * math.cos(w), t.xy_mm[1] - halb * math.sin(w)),
            (t.xy_mm[0] + halb * math.cos(w), t.xy_mm[1] + halb * math.sin(w))])
        zonen.append((sehne.buffer(_KONTAKT_MM, cap_style="flat"),
                      {t.von_raum, t.nach_raum}))
    return zonen


def _kontakt_grenze(abstand: float) -> float:
    """Wie nah ein freier Teil an BEIDEN Raumpolygonen liegen muss.

    Die Kontaktzone reicht je ``_KONTAKT_MM`` weit; bei Wänden bis 250 mm
    überlappt sie beide Räume, ein querender Teil berührt sie also (1 mm
    Quellpräzision). Bei dickeren Wänden bleibt die Zone ein Band MITTEN in der
    Wand — dort heißt „quert", dass der Teil das Band ganz durchspannt, also bis
    auf ``abstand − _KONTAKT_MM`` an beide Räume heranreicht. Ein fester 1-mm-
    Wert wäre dort nie erfüllbar und löschte auch echte Öffnungen (Rennweg OG1:
    Vorraum 10,94 ↔ Wohnküche 73,06 über 450 mm, Referenz O01/O02).
    """
    return max(0.0, abstand - _KONTAKT_MM) + _KONTAKT_TOL_MM


def _grenz_breite(g, pa, pb, abstand: float, wand_puffer) -> float:
    """Breite der Öffnung ENTLANG der gemeinsamen Grenze (max beider Seiten).

    Gemessen wird der Rand des einen Raums, der vor dem freien Teil liegt und
    NICHT am Wandkörper: das ist die offene Stelle der Wand. Die Rechtecklänge
    des Teils taugt nicht — an einer dünnen Wand läuft der freie Teil die ganze
    Wand entlang und maß deren Länge statt der Öffnung (Diagnose U13:
    100/200/240-mm-Wand ohne jede Lücke → 4490/4458/4438 mm).

    Abgezogen wird der um ``_KONTAKT_TOL_MM`` GEPUFFERTE Wandverbund, und der
    Puffer ist die eigentliche Arbeit: ``difference`` entfernt den Raumrand nur,
    wo er exakt auf der geschlossenen Wandfläche liegt. In echten Plänen liegt
    er daneben — ungepuffert bleibt er stehen und die Funktion misst wieder die
    Wandlänge (Rennweg OG1, eigener Lauf: O05 948 → 1774 mm, OG2 GANG 6,06 ↔
    VORRAUM 4,92 1548 → 4055 mm; am UG werden zwei lückenlose 100-mm-Wände zu
    Durchgängen von 1810 und 1552 mm).

    Der 1-mm-Puffer deckt aber nur, was NÄHER als 1 mm liegt; eine gemessene
    Obergrenze der Quellpräzision hat er nicht. Gemessene Decke (eigener
    OG3-Lauf): beim Paar WC 1,51 ↔ ZIMMER 45,36 liegen 1667 der 1794 gezählten
    mm 1–3 mm NEBEN dem Wandkörper und gelten weiter als Öffnungsbreite; mit
    2-mm-Puffer blieben dort 278 mm und dieser (phantome) 1794-mm-Durchgang
    entfiele. Der Puffer ist also kein Beweis, dass gezählte Breite = Öffnung.

    Preis: wo die Öffnung an einer Wandflanke endet, fehlt je Ende 1 mm. Das
    ist systematisch und wird an der Schwelle in ``durchgaenge_ohne_tuerblatt``
    herausgerechnet, nicht hier — sonst fällt der Rauschschutz.
    """
    schatten = g.buffer(_kontakt_grenze(abstand))
    return max(p.boundary.intersection(schatten).difference(wand_puffer).length
               for p in (pa, pb))


def durchgaenge_ohne_tuerblatt(
        raeume: list[Raum], tueren: list[Tuer], wand_union_geom,
        oeffnungen: list[TuerOeffnung] | None = None) -> list[Tuer]:
    """Öffnungen ab 800 mm Nennmaß (gemessen ≥ 797 mm) ohne Bogen/Block.

    Kontaktzone = Schnitt der um ``_KONTAKT_MM`` gepufferten Raumpolygone; was
    davon NICHT von Wandkörpern gedeckt ist, ist ein freier Streifen. Ein
    Streifen QUERT nur dann (Diagnose U13, Slice S5b), wenn er BEIDE Räume
    erreicht (``_kontakt_grenze``); ein Streifen, der an genau einem Raum
    anliegt und zur Gegenseite die Wanddicke entfernt bleibt, ist kein
    Durchgang. Ebenso queren Splitter (Fläche < Breite · ``_SPLITTER_MM``) und
    überlappende Raumpolygone nicht — überlappend heißt ECHT überlappend
    (``_UEBERLAPPUNG_TOL_MM2``, Quellpräzision wie im Gate): gemessen auf vier
    Plänen verloren 23 Raumpaare mit Überlappung > 0 ihren Durchgang, 22 davon
    mit Slivern unter 0,2 mm² (21 unter 0,06 mm², größter 0,197 mm²) — das ist
    Berührungsrauschen gestempelter Nachbarräume auf der Wandmitte, und 16 der
    22 sind laut senkrechter Wandsonde Wandlücken ≥ 700 mm. Nur das 23. Paar
    überlappt echt (Muthgasse E2: KÜCHE 2,55 m² liegt ganz in KÜCHE). Zurück
    kehren über 11 gemessene Pläne 17 Durchgänge (alle Raumabstand 0,
    Überlappung ≤ 0,197 mm²) — das ist der Stand VOR S5b; ob jeder davon eine
    echte Innenöffnung ist, entscheidet die vorgelagerte Raumerkennung, nicht
    diese Regel. Die Breite ist die Länge der gemeinsamen Grenze
    (``_grenz_breite``), nicht die Rechtecklänge des Streifens. Erst ein
    querender Streifen ergibt eine ``Tuer`` mit ``ohne_tuerblatt=True``.

    Zwei Regeln halten bekannte Türen frei. (a) Die alte: eine Tür < 600 mm vom
    Streifen-Schwerpunkt. (b) Die Dublette: überlappt der Streifen die Sehne
    einer Block-Tür, die DASSELBE Raumpaar verbindet, ist er deren eigene
    Öffnung. Gemessen am Rennweg OG1: der Streifen läuft die ganze dünne Wand
    entlang (5711 mm), sein Schwerpunkt liegt 1766 mm von der Tür — (a) greift
    dort nicht, (b) schon (Überlappung 70,7 % der Sehnenzone). Das Raumpaar
    gehört zur Bedingung: ein Streifen eines ANDEREN Paares streift dieselbe
    Sehnenzone am Rennweg OG1 zu 1,3 % und ist keine Dublette, sondern ein
    eigener Durchgang (dort der Gang).
    """
    if wand_union_geom is None or wand_union_geom.is_empty:
        return []
    from .nutzungsklasse import nutzungsklasse_fuer
    # Diagnose Rennweg U13, Slice S5a: SCHACHT/LIFT (KEIN_RAUM) sind nicht
    # begehbar — Paare mit so einer Seite geben keinen Durchgang. Statische Map,
    # weil Raum.nutzungsklasse hier noch None ist (lift_* entstehen erst später).
    polys = [x for x in _raum_polys(raeume)
             if nutzungsklasse_fuer(x[0].raum_typ) != KEIN_RAUM]
    tuer_punkte = [t.xy_mm for t in tueren]
    zonen = _sehnen_zonen(tueren, oeffnungen or [])
    # ponytail: fester 1-mm-Wandpuffer. Raumrand, der weiter als 1 mm neben der
    # Wandflanke liegt, zählt weiter als Öffnungsbreite (synthetisch gemessen:
    # ab 1,1 mm Versatz wird eine 300-mm-Nische zum 3998-mm-Durchgang, s.
    # test_raumkante_weiter_als_der_wandpuffer; real: OG3 WC ↔ ZIMMER, s.
    # _grenz_breite). Upgrade-Pfad: Puffer aus der gemessenen Quellpräzision des
    # Plans statt fest — pauschal größer nimmt echten Öffnungen Breite.
    wand_puffer = wand_union_geom.buffer(_KONTAKT_TOL_MM)
    out: list[Tuer] = []
    for i, (ra, pa, _) in enumerate(polys):
        for rb, pb, _ in polys[i + 1:]:
            abstand = pa.distance(pb)
            if abstand > 2 * _KONTAKT_MM:
                continue
            if pa.intersection(pb).area > _UEBERLAPPUNG_TOL_MM2:
                continue      # Überlappung ist keine Öffnung (Muthgasse E2, 2,55 m²)
            zone = pa.buffer(_KONTAKT_MM).intersection(pb.buffer(_KONTAKT_MM))
            frei = zone.difference(wand_union_geom)
            if frei.is_empty:
                continue
            nah = _kontakt_grenze(abstand)
            teile = list(frei.geoms) if hasattr(frei, "geoms") else [frei]
            for g in teile:
                if pa.distance(g) > nah or pb.distance(g) > nah:
                    continue
                breite = _grenz_breite(g, pa, pb, abstand, wand_puffer)
                # −3 mm: der gepufferte Wandabzug kostet jede an Wandflanken
                # endende Öffnung systematisch 2 · _KONTAKT_TOL_MM, dazu 1 mm
                # Quellpräzision. Ohne das fiel Barawitzka EG KÜCHE 20,47 ↔
                # VORRAUM 3,87 (echte 800-mm-Lücke ohne Türbogen, keine Tür am
                # Paar, gemessen 798,0) aus der Wertung — über 11 gemessene
                # Pläne der EINZIGE neue Durchgang der Absenkung. Folge: eine
                # echte 800-mm-TÜRlücke hält die Breite nicht mehr auf, sie
                # hängt allein an Regel (a)/(b) unten (gemessen: ohne Block-Tür
                # MIT Breite bleibt sie als Dublette stehen —
                # test_800er_tuerluecke_haengt_an_regel_a_b). Am Rennweg OG1
                # hängt VORRAUM 2,59 ↔ BAD 4,66 (798,06 mm, die 800er-Türlücke
                # einer Block-Tür OHNE Breite) jetzt allein an Regel (a), mit
                # 284 mm Schwerpunktabstand.
                if breite < _DURCHGANG_MIN_MM - 3 * _KONTAKT_TOL_MM:
                    continue
                if g.area < breite * _SPLITTER_MM:
                    continue
                c = g.centroid
                xy = (float(c.x), float(c.y))
                if any(math.dist(xy, p) < _TUER_NAH_MM for p in tuer_punkte):
                    continue
                if any(paar == {ra.id, rb.id} and g.intersects(sehnen_zone)
                       for sehnen_zone, paar in zonen):
                    continue
                out.append(Tuer(
                    id=f"durchgang_{len(out) + 1}", xy_mm=xy,
                    breite_mm=float(round(breite)),
                    breite_quelle="GEOMETRIE_OEFFNUNG", von_raum=ra.id,
                    nach_raum=rb.id, ohne_tuerblatt=True, quelle="durchgang"))
                tuer_punkte.append(xy)
    return out


# ── Öffnungen in der AUSSENWAND (ohne Türblatt) ──────────────────────────────
_AUSSEN_KONTAKT_MM = 400.0   # Außenwände sind dicker als Innenwände (≤ 800)
_AUSSEN_DURCHGANG_MAX_MM = 2600.0  # breiter = Fassaden-Artefakt, keine Tür
# S5c, Owner-Entscheid F5: so viel des freien Teils muss außerhalb der gedeckten
# Kontur liegen. Gemessen trennt 0,10 die echten Öffnungen (Rennweg UG
# `aussenoeffnung_1` 0,149, Mollgasse EG Garagentor 0,591) von den Innenstreifen,
# die die Kontur nur berühren (Mollgasse EG `_10` 0,000, `raum_51` 0,002).
_AUSSEN_ANTEIL_MIN = 0.10


def aussen_durchgaenge(raeume: list[Raum], tueren: list[Tuer],
                       wand_union_geom, kontur) -> list[Tuer]:
    """Öffnungen > 800 mm in der Außenwand eines ALLGEMEIN-Raums ohne
    Bogen/Block → ``Tuer(ohne_tuerblatt=True, nach_raum=AUSSEN)``.

    Analog zu ``durchgaenge_ohne_tuerblatt``, aber gegen die AUSSEN-Fläche:
    Kontaktzone = Raum-Puffer ∩ Außenring (2 m um die gedeckte Kontur),
    minus Wandkörper. Nur ALLGEMEIN-Räume (Rennweg-EG-Muster: Rampenkorridor
    mit 1340-mm-Lücke) — Wohnungs-Fensteröffnungen bleiben draußen.

    Querung (Slice S5c, Owner-Entscheid F5 2026-09-27, P_A2 wie § 8a): ein
    freier Teil ist nur dann eine Öffnung, wenn er am Raum anliegt, die Kante
    der gedeckten Kontur erreicht (beide ≤ ``_KONTAKT_TOL_MM``) UND zu
    mindestens ``_AUSSEN_ANTEIL_MIN`` außerhalb der Kontur liegt.
    Außenstreifen vor einer geschlossenen Wand (erreichen den Raum nicht),
    Innenstreifen dahinter (erreichen das Freie nicht) und Zwischenstücke
    zwischen Wandkörpern queren nicht (Rennweg OG3-Stiegenhauslücke F8, EG
    B009). Geprüft IN der Schleife: ein verworfener Teil deckt keinen
    Folge-Teil über ``tuer_punkte``.

    ponytail: die Zone reicht ``_AUSSEN_KONTAKT_MM`` ab dem Raum. In einer
    Außenwand dicker als 400 mm erreicht der freie Teil einer echten Lücke den
    Raum nicht und fällt (auf den 12 Plänen: geschlossene Wand an den Streifen
    150–330 mm). Ausbaupfad: die Zone aus der gemessenen Wanddicke puffern.
    """
    if (wand_union_geom is None or wand_union_geom.is_empty
            or kontur is None or kontur.is_empty):
        return []
    from .nutzungsklasse import nutzungsklasse_fuer
    # Ring + Kontakt-Puffer EINMAL rechnen (die Kontur ist auf großen Plänen
    # komplex — je Raum gepuffert war das der Zeitfresser auf Muthgasse).
    aussen_ring = (kontur.buffer(2000.0).difference(kontur)
                   .buffer(_AUSSEN_KONTAKT_MM))
    kante = kontur.boundary
    tuer_punkte = [t.xy_mm for t in tueren]
    out: list[Tuer] = []
    for r in raeume:
        klasse = r.nutzungsklasse or nutzungsklasse_fuer(r.raum_typ)
        if not (klasse or "").startswith("ALLGEMEIN") or len(r.polygon_mm) < 3:
            continue
        poly = Polygon(r.polygon_mm).buffer(0)
        if poly.is_empty:
            continue
        zone = poly.buffer(_AUSSEN_KONTAKT_MM).intersection(aussen_ring)
        frei = zone.difference(wand_union_geom)
        teile = list(frei.geoms) if hasattr(frei, "geoms") else [frei]
        for g in teile:
            if g.is_empty:
                continue
            mrr = g.minimum_rotated_rectangle
            coords = list(getattr(mrr, "exterior", g).coords)[:4]
            if len(coords) < 3:
                continue
            # Langseite ≈ Öffnungsbreite (die Wand klippt die Zone seitlich).
            # Der Deckel filtert Fassaden-Artefakte (fehlende Wandkörper an
            # einer ganzen Raumkante ergäben raumlange Pseudo-Öffnungen).
            breite = max(math.dist(coords[0], coords[1]),
                         math.dist(coords[1], coords[2]))
            if not (_DURCHGANG_MIN_MM < breite <= _AUSSEN_DURCHGANG_MAX_MM):
                continue
            if (poly.distance(g) > _KONTAKT_TOL_MM
                    or g.distance(kante) > _KONTAKT_TOL_MM
                    or g.difference(kontur).area < _AUSSEN_ANTEIL_MIN * g.area):
                continue
            c = g.centroid
            xy = (float(c.x), float(c.y))
            if any(math.dist(xy, p) < 2 * _TUER_NAH_MM for p in tuer_punkte):
                continue
            out.append(Tuer(
                id=f"aussenoeffnung_{len(out) + 1}", xy_mm=xy,
                breite_mm=float(round(breite)),
                breite_quelle="GEOMETRIE_OEFFNUNG", von_raum=r.id,
                nach_raum=AUSSEN, ohne_tuerblatt=True,
                quelle="oeffnung_aussenwand"))
            tuer_punkte.append(xy)
    return out
