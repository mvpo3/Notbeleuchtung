"""freiflaeche — freie Flächen im Wohnungsumriss bekommen einen Raum (Punkt 2d).

Owner 2026-09-30: „Innerhalb eines Wohnungsumrisses gibt es keine freie Fläche
ohne Raum." Messfall Rennweg DG1: das stempellose Sofa-Feld (16,9 m²) links
neben Bad/WC, offen zum Wohnzimmer — die Rest-Stufe sieht es nicht, weil sie
nur in der größten Wandkörper-Komponente sucht (``rest_komponenten``,
``aussenkontur(d=1000)``).

**Freie Fläche** = gedeckte Kontur (``kontur`` des Providers — dieselbe Fläche,
die die Türzuordnung als „nicht AUSSEN" liest) minus alle Räume minus
Wandkörper, morphologisch geöffnet (``_OEFFNEN_MM``: Raster-Splitter zwischen
Raum und Wand fallen weg), je Zusammenhangskomponente > ``MIN_M2``. Die
Deckenplatte (Rennweg ``New_035 Decken``) gibt es nur in einer Planfamilie;
die gedeckte Kontur gibt es auf jedem Plan mit Wandkörpern.

**Im Wohnungsumriss** heißt (``wohnungsumriss``): alle Nachbarräume bis
Wanddicke gehören zu einer Wohnung (``umschliessende_wohnung`` — auch für
Kerben an der Fassade, die das Schließen um ±250 mm nicht füllt, wie das
Sofa-Feld) oder die Fläche liegt zu ≥ ``VOLL`` im ±250-mm-Umriss genau einer
Wohnung. Außerhalb eines Wohnungsumrisses bleibt alles, wie es ist.

**Regel** (Owner 2026-09-30): eine Öffnung zum Nachbarraum ohne Türblatt ist
kein Trenner — die Fläche geht in diesen Raum (bei mehreren entscheidet die
breiteste; nicht eindeutig → eigener Raum). Eine Tür mit Blatt ist ein
Trenner → eigener Raum UNBEKANNT (``raum_typ`` leer = untypisiert, magenta in
den Darstellungen). Öffnung = Grenzabschnitt am Nachbarraum ohne Wandkörper,
mindestens so breit wie ein Durchgang ohne Türblatt (``_DURCHGANG_MIN_MM``).
Steht an der Grenze zu einem Raum eine Tür mit Blatt, ist die ganze Grenze
Trenner — die Wandlücken daneben sind nicht erkannte Wand (Am Rain).

Grundsatz (b): die Fläche erbt die Wohnung nur über den aufnehmenden Raum;
``wohnung_id`` wird nie gesetzt, am aufnehmenden Raum ändern sich weder Klasse,
Typ noch Flags. Türen bleiben unverändert.

**Stempel vor UNBEKANNT** (Owner-Entscheid 2, 2026-10-01, Abschnitt 2): bevor
ein neuer Raum ``frei_n`` UNBEKANNT wird, werden Kürzel/Stempel in seinem
Polygon gelesen und nach Abschnitt 1 typisiert (``kuerzel_beleg.
typisiere_kuerzel`` — dieselbe Regel wie in der Kaskade: Kürzel-Form,
Wörterbuch, mehrdeutig → nie, Doppelstempel → dominanter Stempel ≥ 50 % der
Polygonfläche, sonst UNBESTIMMT mit Grund; Sanitär schlägt AR/Zimmer). Ein so
typisierter Raum bekommt die statische Klasse seines Typs
(``nutzungsklasse_fuer``); ``wohnung_id`` bleibt leer — die kommt nur aus rohen
Türen (Grundsatz (b)), und die Türen an diesen Räumen tragen KEIN_RAUM-Seiten.
Am Rain: in 6 der 12 ``frei_*`` liegt ein Raumstempel, dessen Stempel kein
Polygon bekam (LUECKEN.md § 22); ohne diese Stufe blieben echte VR/AR/Balkone
UNBEKANNT.
"""
from __future__ import annotations

from collections.abc import Callable, Sequence

from shapely import BufferJoinStyle
from shapely.geometry import Point, Polygon
from shapely.ops import linemerge, unary_union

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer

from .bereinigung import _groesste, _ring, _schlitz
from .kuerzel_beleg import Text, typisiere_kuerzel
from .nutzungsklasse import nutzungsklasse_fuer
from .stempel_anker import Stempel
from .tuer_zuordnung import _DURCHGANG_MIN_MM, _KONTAKT_TOL_MM, _TUER_NAH_MM
from .wohnungsumriss import VOLL, umschliessende_wohnung, wohnungsumrisse

#: Owner-Schwelle: freie Flächen bis 2 m² bleiben frei.
MIN_M2 = 2.0
#: Öffnen um ±150 mm: Streifen unter 300 mm sind Raster-Splitter (Räume der
#: F-/R-Stufe liegen auf 50 mm, ``rest_komponenten._BELEGT_PUFFER_MM`` = 100).
_OEFFNEN_MM = 150.0
#: Ein Grenzabschnitt liegt „am Raum" bis zu zwei Rasterzellen (2 × 50 mm).
_KANTE_MM = 100.0
#: Zwei Öffnungen zu verschiedenen Räumen sind gleich breit, wenn sie weniger
#: als zwei Rasterzellen (je Ende eine) auseinander liegen → nicht eindeutig.
_EINDEUTIG_MM = 100.0
#: Türlücke: der Türpunkt liegt in der Wandachse, die Lücke reicht bis zur
#: halben Wanddicke (Wandkörper bis 600 mm, ``wandkoerper._BREITE_MAX_MM``);
#: ohne gemessene Breite eine 1-m-Tür.
_WAND_HALB_MM = 300.0
_TUER_BREITE_MM = 1000.0
_MITRE = BufferJoinStyle.mitre


def _polys(geom) -> list[Polygon]:
    return [g for g in getattr(geom, "geoms", [geom])
            if g.geom_type == "Polygon" and not g.is_empty]


def freie_flaechen(raeume: list[Raum], kontur, wu) -> list[Polygon]:
    """Zusammenhangskomponenten > ``MIN_M2`` von Kontur − Räume − Wandkörper."""
    if kontur is None or kontur.is_empty:
        return []
    belegt = unary_union([Polygon(r.polygon_mm).buffer(0) for r in raeume
                          if len(r.polygon_mm) >= 3])
    roh = kontur.difference(belegt)
    if wu is not None and not wu.is_empty:
        roh = roh.difference(wu)
    offen = roh.buffer(-_OEFFNEN_MM, join_style=_MITRE).buffer(
        _OEFFNEN_MM, join_style=_MITRE).intersection(roh)
    # Zähne der 50-mm-Raumränder zurück: freie Fläche bis _KANTE_MM an der
    # Komponente — ohne das, was eine frühere Komponente schon bekommen hat
    # (zwei Flächen an einem Hals < 2 × _KANTE_MM, Am Rain OG1).
    out: list[Polygon] = []
    for p in _polys(offen):
        if p.area > MIN_M2 * 1e6:
            zahn = p.buffer(_KANTE_MM, join_style=_MITRE).intersection(roh)
            out.append(_groesste(zahn.difference(unary_union(out))) or p)
    return out


def _wohnung(f: Polygon, raeume: list[Raum], tueren: list[Tuer],
             umrisse: dict) -> tuple[str | None, str]:
    probe = Raum(id="__freiflaeche", raum_typ="", polygon_mm=_ring(f))
    wid, grund = umschliessende_wohnung(probe, raeume, tueren)
    if wid:
        return wid, f"Nachbarn nur {wid}"
    drin = [w for w, u in umrisse.items() if f.intersection(u).area >= VOLL * f.area]
    if len(drin) == 1:
        return drin[0], f"±250-mm-Umriss {drin[0]}"
    return None, grund


def _grenzen(f: Polygon, raeume: list[Raum], an: list[Tuer], wu) -> list[tuple]:
    """``(breite_mm, raum, türen)`` je Grenzabschnitt ohne Wandkörper an einem
    Nachbarraum (Rand der Fläche bis ``_KANTE_MM`` am Raum). ``türen`` = die
    Türen mit Blatt aus ``an`` an der Grenze zu diesem Raum: der Türpunkt liegt
    in der Wandachse, die Lücke reicht halbe Türbreite + ``_WAND_HALB_MM``."""
    wand = wu.buffer(_KONTAKT_TOL_MM) if wu is not None and not wu.is_empty else None
    out = []
    for r in raeume:
        if len(r.polygon_mm) < 3:
            continue
        p = Polygon(r.polygon_mm).buffer(0)
        if p.distance(f) > _KANTE_MM:
            continue
        grenze = f.boundary.intersection(p.buffer(_KANTE_MM))
        if grenze.is_empty:
            continue
        tuer = [t.id for t in an if Point(t.xy_mm).distance(grenze)
                <= (t.breite_mm or _TUER_BREITE_MM) / 2 + _WAND_HALB_MM]
        linie = grenze.difference(wand) if wand is not None else grenze
        if linie.is_empty:
            continue
        m = linemerge(linie) if linie.geom_type == "MultiLineString" else linie
        out += [(teil.length, r, tuer) for teil in getattr(m, "geoms", [m]) if teil.length > 0]
    return out


def _entscheid(grenzen: list[tuple], an: list[Tuer], wid: str) -> tuple[Raum | None, str]:
    """``(aufnehmender Raum | None, Grund)`` nach der Owner-Regel; ``an`` =
    Türen mit Blatt in ``_TUER_NAH_MM`` der Fläche (auch ohne Raum dahinter).
    Eine Tür mit Blatt an der Grenze zu einem Raum macht die ganze Grenze zum
    Trenner — die Wandlücken daneben sind dann nicht erkannte Wand, keine
    Öffnung (im Zweifel eigener Raum statt Zuschlag)."""
    oeffnungen = sorted(((b, r) for b, r, tuer in grenzen if not tuer
                         and b >= _DURCHGANG_MIN_MM - 3 * _KONTAKT_TOL_MM),
                        key=lambda x: -x[0])
    if not oeffnungen:
        if an:
            tuer = ", ".join(f"{t.id} {t.von_raum or '—'}|{t.nach_raum or '—'}" for t in an)
            return None, f"Tür mit Blatt trennt ({tuer}), keine Öffnung ohne Türblatt"
        return None, (f"keine Öffnung ≥ {_DURCHGANG_MIN_MM / 1000:.2f} m ohne Türblatt "
                      "und keine Tür")
    b1, r1 = oeffnungen[0]
    zweite = next(((b, r) for b, r in oeffnungen if r.id != r1.id), None)
    if zweite and b1 - zweite[0] < _EINDEUTIG_MM:
        return None, (f"nicht eindeutig: Öffnung {b1 / 1000:.2f} m zu {r1.id} "
                      f"{r1.raum_typ or '—'} und {zweite[0] / 1000:.2f} m zu "
                      f"{zweite[1].id} {zweite[1].raum_typ or '—'}")
    if r1.wohnung_id != wid:   # Balkon, Schacht, Erschließung, fremde Wohnung
        return None, (f"breiteste Öffnung {b1 / 1000:.2f} m führt zu {r1.id} "
                      f"{r1.raum_typ or '—'} ({r1.nutzungsklasse}, "
                      f"{r1.wohnung_id or 'ohne Wohnung'})")
    return r1, f"Öffnung ohne Türblatt {b1 / 1000:.2f} m"


def _vereinige(a: Polygon, b: Polygon):
    """Union zweier Flächen mit gemeinsamer Kante — um die Quellpräzision
    geschlossen, sonst bleiben zwei Teile an einer Gleitkomma-Fuge."""
    e = _KONTAKT_TOL_MM
    return unary_union([a.buffer(e, join_style=_MITRE),
                        b.buffer(e, join_style=_MITRE)]).buffer(-e, join_style=_MITRE)


def fuelle_freie_flaechen(raeume: list[Raum], tueren: list[Tuer], kontur, wu, *,
                          texte: Sequence[Text] = (), stempel: Sequence[Stempel] = (),
                          sanitaer_quelle: Callable[[], list] = list) -> list[str]:
    """Freie Flächen im Wohnungsumriss zuschlagen oder als eigenen Raum
    anlegen — in place auf ``raeume``. Liefert je Fläche eine Befund-Zeile
    (Prüfstrecken-Ausgabe, kein Contract-Feld), dazu je offen gebliebenem
    Kürzel-Fall eine ``kuerzel:``-Warnung.

    ``texte`` = Kürzel-Texte des Plans (``kuerzel_beleg.kuerzel_texte``),
    ``stempel`` = Raumstempel ohne eigenes Polygon (Dominanz-Regel),
    ``sanitaer_quelle`` = Sanitärobjekte für „Erscheinungsbild schlägt Kürzel"
    — Entscheid 2: Stempel vor UNBEKANNT für jeden neuen Raum ``frei_n``.
    """
    flaechen = freie_flaechen(raeume, kontur, wu)
    if not flaechen:
        return []
    umrisse = wohnungsumrisse(raeume)
    plan: list[tuple[Polygon, Raum | None, str]] = []
    for f in flaechen:
        wid, wo = _wohnung(f, raeume, tueren, umrisse)
        if wid is None:
            continue
        an = [t for t in tueren if not t.ohne_tuerblatt
              and Point(t.xy_mm).distance(f) <= _TUER_NAH_MM]
        ziel, grund = _entscheid(_grenzen(f, raeume, an, wu), an, wid)
        plan.append((f, ziel, f"im Umriss {wid} ({wo}); {grund}"))
    zeilen: list[str | tuple[str, Raum, str]] = []
    neue: list[Raum] = []
    for f, ziel, grund in plan:
        c = f.representative_point()
        kopf = (f"freiflaeche: {f.area / 1e6:.2f} m² bei ({c.x / 1000:.1f}, "
                f"{c.y / 1000:.1f}) m")
        if ziel is not None:
            vorher = Polygon(ziel.polygon_mm).buffer(0)
            u = _vereinige(vorher, f)
            neu, _, ok = _schlitz(u) if u.geom_type == "Polygon" else (u, 0.0, False)
            if ok:
                if len(ziel.polygon_roh) >= 3:   # Bilanz roh − mm bleibt (Contract v1.5.0)
                    ziel.polygon_roh = _ring(_groesste(_vereinige(
                        Polygon(ziel.polygon_roh).buffer(0), f)))
                ziel.polygon_mm = _ring(neu)
                ziel.flaeche_m2 = neu.area / 1e6
                zeilen.append(f"{kopf} → {ziel.id} {ziel.raum_typ or '—'} "
                              f"{vorher.area / 1e6:.2f} → {ziel.flaeche_m2:.2f} m², {grund}")
                continue
            grund += "; Zuschlag nicht zusammenhängend"
        p, _, _ = _schlitz(f)
        raum = Raum(id=f"frei_{len(neue) + 1}", raum_typ="", polygon_mm=_ring(p),
                    flaeche_m2=p.area / 1e6)
        raeume.append(raum)
        neue.append(raum)
        zeilen.append((kopf, raum, grund))
    # Entscheid 2: Stempel/Kürzel im Polygon lesen, bevor der Raum UNBEKANNT wird.
    # Nur die neuen Räume stehen zur Wahl; Klasse statisch nach Typ, keine Wohnung.
    hinweise: list[str] = []
    warnungen: list[str] = []
    if neue and texte:
        typisiere_kuerzel(list(texte), neue, sanitaer_quelle,
                          hinweise=hinweise, warnungen=warnungen, stempel=list(stempel))
        for r in neue:
            if r.raum_typ:
                r.nutzungsklasse = nutzungsklasse_fuer(r.raum_typ)
    beleg = {h.split(":", 1)[0]: h.split(":", 1)[1].strip() for h in hinweise}
    befund: list[str] = []
    for z in zeilen:
        if isinstance(z, str):
            befund.append(z)
            continue
        kopf, raum, grund = z
        befund.append(f"{kopf} → neuer Raum {raum.id} {raum.raum_typ or 'UNBEKANNT'}, {grund}"
                      + (f"; {beleg[raum.id]} (Entscheid 2: Stempel vor UNBEKANNT)"
                         if raum.id in beleg else ""))
    return befund + warnungen
