"""kuerzel_beleg — ein Raumkürzel im Raumpolygon ist Typbeleg, auch ohne Flächenzeile.

Owner-Entscheid 1 (2026-10-01, ``docs/AUFTRAG_2026-10-01.md`` § 1): „Ein Raumkürzel
gilt als Beleg für den Typ, auch ohne Flächenzeile. Bedingung: Der Text liegt
innerhalb des Raumpolygons, nicht in Legende, Plankopf oder an Schnitt-/Achsmarken."

Bisher zählte ein loser Text nur als Stempel, wenn eine m²-Zeile im Umkreis stand
(``stempel_anker._stempel_aus_texten``); „STGH" ohne Flächenzeile blieb unsichtbar
(Am Rain OG4 ``rest_2``, LUECKEN.md § 20.4). Hier läuft NACH der Rest-Stufe und der
Bereinigung ein eigener Durchgang über alle noch untypisierten Räume der Kaskade
(L/H/F ohne Stempel, R). Kein Stempel-Objekt, keine Flutung, keine Zuordnung — ein
loser Text ohne Polygon bleibt ohne Wirkung (kein neuer Raum aus einem Legendenwort).

**Ausschlussregel (Entscheid 1, hier festgelegt):**

- Der Einfügepunkt liegt in einem Raumpolygon; alles außerhalb zählt nicht.
  Legende und Plankopf liegen im Papierbereich oder außerhalb der Gebäude-Kontur
  (die R-Stufe baut nur in der größten Wandkörper-Komponente), also in keinem
  Polygon — zusätzlich zählt kein Text auf einem Legenden-/Plankopf-Layer
  (``_ZONEN_LAYER``).
- Kürzel-FORM (``_KUERZEL``): ein Wort aus Buchstaben (mit ``.``, ``/``, ``-``),
  optional eine ein-/zweistellige Zählnummer („ZI 2", „TREPPENHAUS 1"); jedes
  Buchstaben-Token mindestens zwei Zeichen. Damit fallen Achs-/Schnittmarken
  („A", „1", „A-A"), Stufen-Beschriftung („17 STG 17/29" — Token ``stg`` steht im
  Wörterbuch!), Höhenkoten („STUK = 225 ü. FOK STGH = -0.70"), Summenblöcke
  („Wohnfläche (inkl.Loggia)") und Fließtext („Luftraum Garage", „Gully Müll") weg.
  Bei ``/``-Verbund müssen ALLE Teile im Wörterbuch stehen („BAD/WC" ja,
  „Terrasse/Balkon/Garten" nein).
- Ein Raum mit zugeordnetem Stempel wird nie umtypisiert — auch wenn der Stempel
  keinen Typ trägt („GESCHÄFTLOKAL", „TV Raum", „Kochnische": Vokabular-Fälle,
  Enis). Sein Stempel ist sein Name; ein loses Wort darin („Garderobe" als
  Möbelbeschriftung im Geschäftslokal, Rennweg EG) ist kein Gegenbeleg. Die
  Texte in seinem Polygon werden trotzdem ihm zugerechnet, nicht einem
  größeren untypisierten Nachbarn.
- Der Typ kommt aus dem bestehenden Wörterbuch (``raumtyp.raumtyp_flags``); hier
  wird kein Typ erfunden. Mehrdeutige Kürzel (``kuerzel_entscheid.MEHRDEUTIG``:
  SR, TR, KA) und Kandidaten-Kürzel („Schl.", ``KANDIDATEN``) typisieren nie —
  der Raum bleibt UNBESTIMMT mit Notlicht, Grund im Bericht. Sie zählen nur als
  eigenes Wort; „Zul.KA" (Zuluft Kellerabteil) ist kein Kürzel.
- Ein Raum wird nur typisiert, wenn alle Kürzel in seinem Polygon denselben Typ
  ergeben. Zwei verschiedene Typen in einem Polygon (R-Stufe fasst Räume
  zusammen, deren Stempel kein Polygon bekamen): es gilt der **dominante
  Stempel** — der Stempel ohne Polygon (``stempel_anker``, Flag
  ``kein_polygon``) mit der größten Flächenzeile, wenn sie mindestens die
  Hälfte der Polygonfläche deckt (``_DOMINANT``). Am Rain OG4 ``rest_2``
  40,2 m²: „STGH 32.44 m²" (81 %) gegen „VR 8.52" und „VR 6.87" → STIEGENHAUS.
  Ohne dominanten Stempel (Bad + Gang ohne Flächen) → untypisiert mit Grund.
- Ein Wort mit Trennstrich am Ende („Schacht-" / „entlüftung") ist ein
  Fragment einer Fließtext-Zeile, kein Kürzel.
- Erscheinungsbild schlägt Kürzel: hat der Raum ≥ 2 Sanitärobjekte
  (``sanitaer.sanitaerobjekte``), wird er nicht per Kürzel AR/ZIMMER-Familie —
  Warnung, Typ offen (die K3-Sanitärregel im Provider kann ihn BAD/WC machen).

Grundsatz (a) bleibt: ein Raum ohne eindeutigen Beleg behält sein Notlicht.
"""
from __future__ import annotations

import re
from collections.abc import Callable

from shapely.geometry import Point, Polygon
from shapely.strtree import STRtree

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum

from .dxf_load import XY, DxfPlan
from .kuerzel_entscheid import KANDIDATEN, MEHRDEUTIG
from .raumtyp import _WORT, raumtyp_flags
from .stempel_anker import Stempel

#: Kürzel-Form: Buchstabenwort (., /, - erlaubt), optional Zählnummer 1–2 Stellen.
_KUERZEL = re.compile(r"^[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß./-]{0,23}(?:\s?\d{1,2})?$")
#: Legenden-/Plankopf-Layer: dort steht ein Kürzel als Erklärung, nicht als Raumname.
_ZONEN_LAYER = re.compile(r"LEGEND|PLANKOPF|SCHRIFTFELD|TITEL|TITLE", re.IGNORECASE)
#: Typen, die ein Sanitärbefund (≥ 2 Objekte) überstimmt — Owner: „AR mit WC und
#: Waschbecken" ist kein Abstellraum; dasselbe für die Zimmer-Familie.
_TROCKEN = frozenset({"ABSTELLRAUM", "ZIMMER", "SCHLAFZIMMER", "KINDERZIMMER", "WOHNZIMMER"})
_SANITAER_MIN = 2
#: Dominanter Stempel: Flächenzeile deckt mindestens die Hälfte des Polygons.
_DOMINANT = 0.5
#: Flächenabweichung Polygon ↔ Stempel, ab der der Hinweis sie nennt (wie ``stempel_anker``).
_ABWEICHUNG_PROZENT = 10.0
#: Ein Text ist mehrdeutig/Kandidat → nie typisieren, nur melden.
MEHRDEUTIG_MARKE = "mehrdeutig"

Text = tuple[str, XY, str]            # (Text, xy_mm, Layer)


def ist_kuerzel_text(text: str) -> bool:
    """Form-Regel: ein Kürzel-Wort, keine Marke, keine Stufe, kein Fließtext."""
    t = " ".join((text or "").split())
    if t.endswith("-") or not _KUERZEL.match(t):
        return False
    return all(len(w) >= 2 for w in _WORT.findall(t))


def kuerzel_typ(text: str) -> tuple[str, bool, bool] | str | None:
    """Kürzel → ``(raum_typ, ist_fluchtweg, ist_communal)``, ``"mehrdeutig"`` oder None.

    None heißt: kein Kürzel (Form) oder kein Wörterbuch-Treffer — kein Beleg.
    """
    if not ist_kuerzel_text(text):
        return None
    t = " ".join(text.split())
    tokens = {w.lower() for w in _WORT.findall(t)}
    # Mehrdeutig nur als EIGENES Wort („SR", „KA 10", „Schl."); im Verbund („Zul.KA"
    # = Zuluft Kellerabteil, Am Rain UG) ist es Lüftungs-Beschriftung, kein Kürzel.
    if len(tokens) == 1 and tokens & (set(MEHRDEUTIG) | set(KANDIDATEN)):
        return MEHRDEUTIG_MARKE
    teile = [p for p in t.split("/") if _WORT.search(p)]
    if len(teile) > 1 and any(raumtyp_flags(p) is None for p in teile):
        return None
    return raumtyp_flags(t)


def kuerzel_texte(plan: DxfPlan) -> list[Text]:
    """(Text, xy_mm, Layer) aller TEXT/MTEXT des Modellraums, die der Form nach
    Kürzel sind — die Punkt-in-Polygon-Probe macht ``typisiere_kuerzel``."""
    out: list[Text] = []
    for e in plan.space:
        t = e.dxftype()
        if t not in ("MTEXT", "TEXT"):
            continue
        txt = e.plain_text() if t == "MTEXT" else e.dxf.text
        if txt and ist_kuerzel_text(str(txt)):
            out.append((" ".join(str(txt).split()), plan._scale(e.dxf.insert),
                        str(e.dxf.layer)))
    return out


def _grund(text: str) -> str:
    tokens = {w.lower() for w in _WORT.findall(text)}
    k = next((k for k in MEHRDEUTIG if k in tokens), None)
    if k is not None:
        return MEHRDEUTIG[k]
    k = next((k for k in KANDIDATEN if k in tokens), None)
    return (f"Kandidaten-Kürzel {KANDIDATEN[k]} — nur mit Flächenzeile, Beleg und "
            f"Owner-Entscheidung (kuerzel_entscheid)") if k else "mehrdeutig"


def _dominant(poly: Polygon, stempel: list[Stempel]) -> Stempel | None:
    """Stempel ohne Polygon mit der größten Flächenzeile im Polygon, wenn sie
    mindestens ``_DOMINANT`` der Polygonfläche deckt — sonst None."""
    drin = [s for s in stempel if s.typ and s.flaeche_m2
            and poly.covers(Point(s.position_mm))]
    if not drin:
        return None
    best = max(drin, key=lambda s: s.flaeche_m2 or 0.0)
    return best if (best.flaeche_m2 or 0.0) >= _DOMINANT * poly.area / 1e6 else None


def typisiere_kuerzel(texte: list[Text], raeume: list[Raum],
                      sanitaer_quelle: Callable[[], list[tuple[str, XY]]],
                      *, hinweise: list[str], warnungen: list[str],
                      stempel: list[Stempel] = (),
                      gestempelt: frozenset[str] | set[str] = frozenset()) -> None:
    """Untypisierte Räume aus Kürzeln in ihrem Polygon typisieren — in place.

    ``sanitaer_quelle`` wird höchstens einmal gerufen, und nur wenn ein Kürzel
    der Trocken-Familie ansteht. ``stempel`` = Raumstempel OHNE eigenes Polygon
    (``kein_polygon``) für die Dominanz-Regel bei widersprechenden Kürzeln.
    ``gestempelt`` = IDs der Räume mit zugeordnetem Stempel: sie nehmen Texte
    auf, werden aber nie typisiert.
    ``hinweise`` bekommt je typisiertem Raum eine Zeile (bericht.md „Hinweise
    Kürzel-Auflösung"), ``warnungen`` je offenem Raum den Grund (bericht.md
    „Warnungen", Präfix ``kuerzel:``).
    """
    offen = [(r, Polygon(r.polygon_mm).buffer(0)) for r in raeume
             if not (r.raum_typ or "").strip() and len(r.polygon_mm) >= 3]
    offen = [(r, p) for r, p in offen if not p.is_empty]
    if not offen or not texte:
        return
    baum = STRtree([p for _, p in offen])
    je_raum: dict[str, list[Text]] = {}
    for txt, xy, layer in texte:
        if _ZONEN_LAYER.search(layer):
            continue
        pt = Point(xy)
        idx = [int(i) for i in baum.query(pt) if offen[int(i)][1].covers(pt)]
        if not idx:
            continue
        r = offen[min(idx, key=lambda i: offen[i][1].area)][0]   # kleinster deckender Raum
        je_raum.setdefault(r.id, []).append((txt, xy, layer))
    sanitaer: list[tuple[str, XY]] | None = None
    for r, poly in offen:
        funde = je_raum.get(r.id)
        if not funde or r.id in gestempelt:
            continue
        typen: dict[str, tuple[str, bool, bool]] = {}
        unklar: list[str] = []
        belegt: list[Text] = []            # nur Texte, die ein Kürzel sind
        for txt, xy, layer in funde:
            tf = kuerzel_typ(txt)
            if tf is None:
                continue
            belegt.append((txt, xy, layer))
            if tf == MEHRDEUTIG_MARKE:
                unklar.append(txt)
            else:
                typen[tf[0]] = tf
        texte_s = ", ".join(f"»{t}«" for t, _, _ in belegt)
        if not typen and not unklar:
            continue
        if unklar and not typen:
            warnungen.append(
                f"kuerzel: {r.id} bleibt UNBESTIMMT (Notlicht): Kürzel mehrdeutig — "
                + ", ".join(f"»{u}« = {_grund(u)}" for u in unklar)
                + "; zweite Meinung (Abschnitt 3) entscheidet")
            continue
        beleg = "im Polygon (Typbeleg ohne eigene Zuordnung)"
        dominant = False
        if len(typen) > 1 or unklar:
            dom = _dominant(poly, list(stempel))
            if dom is None or raumtyp_flags(dom.name or "") is None:
                warnungen.append(
                    f"kuerzel: {r.id} bleibt UNBESTIMMT (Notlicht): nicht eindeutig — "
                    f"{texte_s} → {', '.join(sorted(typen))}"
                    + (f"; mehrdeutig: {', '.join(unklar)}" if unklar else "")
                    + "; kein dominanter Stempel")
                continue
            typen = {dom.typ: raumtyp_flags(dom.name or "")}
            dominant = True
            beleg = (f"im Polygon → nicht eindeutig, es gilt der dominante Stempel "
                     f"»{dom.name} {dom.flaeche_m2:.2f} m²« "
                     f"({100 * dom.flaeche_m2 / (poly.area / 1e6):.0f} % der Polygonfläche)")
        (label, flucht, communal), = typen.values()
        # Flächenzeile eines polygonlosen Stempels gleichen Typs im Polygon: weicht
        # das Polygon > 10 % ab (R-Stufe fasst Räume zusammen), steht das im Hinweis
        # — wie das Flag ``zu_gross``/``zu_klein`` der Stempel-Zuordnung.
        gleich = [s for s in stempel if s.typ == label and s.flaeche_m2
                  and poly.covers(Point(s.position_mm))]
        if gleich and not dominant:
            s0 = max(gleich, key=lambda s: s.flaeche_m2 or 0.0)
            abw = (poly.area / 1e6 - s0.flaeche_m2) / s0.flaeche_m2 * 100
            if abs(abw) > _ABWEICHUNG_PROZENT:
                beleg += (f"; Polygon {poly.area / 1e6:.2f} m² gegen Stempel "
                          f"»{s0.name} {s0.flaeche_m2:.2f} m²« ({abw:+.0f} %, Polygon "
                          f"fasst mehr als den Stempelraum)" if abw > 0 else
                          f"; Polygon {poly.area / 1e6:.2f} m² gegen Stempel "
                          f"»{s0.name} {s0.flaeche_m2:.2f} m²« ({abw:+.0f} %)")
        if label in _TROCKEN:
            if sanitaer is None:
                sanitaer = list(sanitaer_quelle())
            drin = [art for art, xy in sanitaer if poly.covers(Point(xy))]
            if len(drin) >= _SANITAER_MIN:
                warnungen.append(
                    f"kuerzel: {r.id} Kürzel {texte_s} → {label} widerspricht dem "
                    f"Erscheinungsbild ({len(drin)} Sanitärobjekte: "
                    f"{', '.join(sorted(drin))}) — Typ offen, Erscheinungsbild gilt")
                continue
        r.raum_typ = label
        r.ist_fluchtweg = r.ist_fluchtweg or flucht
        r.ist_communal = r.ist_communal or communal
        layer_s = sorted({layer for _, _, layer in belegt})
        hinweise.append(f"{r.id}: Kürzel {texte_s} {beleg} "
                        f"(Layer {', '.join(layer_s)}) -> {label} (Entscheid 1, "
                        f"Owner 2026-10-01)")
