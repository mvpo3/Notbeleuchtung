"""Gesamtdarstellung der Raumerkennung — ein großes Bild je Plan + Index.

Owner-Auftrag (Selman, 2026-09-13): den Ist-Stand der Raumerkennung visuell
beurteilen können, BEVOR weitergebaut wird. Deshalb gilt hier durchgehend
**Ehrlichkeit vor Schönheit**: untypisierte Räume magenta mit ``?``, unbekannte
Türen ``?``, unbelastbare Ausgänge gestrichelt. Nichts wird geglättet, nichts
weggefiltert — auch Schnitte, Legenden und Symbolbibliotheken laufen mit und
erscheinen mit ihrem Fehlergrund im Index.

Wiederverwendung statt Neubau: Rotation/Zoom/Cluster/Beschriftung kommen aus
``uebersicht_karte``, Türbögen/Ausgangskreise/Segmentfarben aus
``plan_pruefen`` (dort Bild ``05_fluchtweg``). Dieses Skript legt beides
übereinander und ergänzt die vom Owner vorgegebene Farbtabelle.

ZWEI BEWUSSTE ABWEICHUNGEN vom Bestand, beide auf Owner-Vorgabe:
  * Segmentfarben: Owner will LINIE grün, GRAPH blau. ``plan_pruefen._SEG_FARBE``
    hat es andersherum (LINIE blau, GRAPH grün). Hier gilt die Owner-Vorgabe,
    das Bestandsbild 05 bleibt unverändert.
  * Türkürzel: der Owner listet ``NA`` als eigenes Kürzel. ``ist_notausgang``
    ist aber ein FLAG neben ``tuer_detail``, keine Alternative dazu — eine
    Haustür kann zugleich Notausgang sein. Darum bleibt die Kombination
    ``HE/NA`` erhalten; die Legende erklärt sie.

Aufruf:
    python scripts/analyse/gesamtdarstellung.py            # alle DXF im Repo
    python scripts/analyse/gesamtdarstellung.py <dxf>      # ein Plan
    python scripts/analyse/gesamtdarstellung.py --nur-index  # nur index.html
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
import traceback
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "scripts" / "analyse"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import uebersicht_karte as uk
from matplotlib.lines import Line2D
from matplotlib.patches import Arc, Patch
from shapely.geometry import Point, Polygon

import plan_pruefen as pp

AUSGABE = REPO / "Projekte" / "_ergebnis"
#: Mindestbreite laut Owner-Auftrag. Das Bild wird darauf hochskaliert.
MIN_BREITE_PX = 2000

# ── Farbtabelle: WÖRTLICH die Owner-Vorgabe ─────────────────────────────────
# Schlüssel = interne Kategorie, Wert = (Legendentext, Füllfarbe, Kontur,
# Schraffur oder None). Die Kategorie entsteht in `_kategorie` aus raum_typ UND
# nutzungsklasse — der Gang braucht beides, weil "allgemein" und "privat"
# denselben raum_typ tragen.
_KAT: dict[str, tuple[str, str, str, str | None]] = {
    "wohnen":     ("Zimmer / Wohnräume", "#4caf50", "#1b5e20", None),
    "nass":       ("Bad / WC / Nassräume", "#e53935", "#8e0000", None),
    "kueche":     ("Küche / Wohnküche", "#8e24aa", "#4a0072", None),
    "stiege":     ("Stiegenhaus / Schleuse / Vorraum", "#fb8c00", "#994400", None),
    "gang_allg":  ("Gang allgemein (Erschließung)", "#ffeb3b", "#9a7400", None),
    "gang_priv":  ("Gang privat (in Wohnung)", "#ffeb3b", "#9a7400", "///"),
    "neben":      ("Abstellraum / Technik / Keller / Lager", "#9e9e9e", "#424242", None),
    "schacht":    ("Lift / Schacht", "#ffffff", "#d50000", None),
    "freiflaeche": ("Balkon / Loggia / Terrasse", "#a5d6a7", "#2e7d4f", None),
    "aussen":     ("AUSSEN (Weg ins Freie)", "#42a5f5", "#0d47a1", "//"),
    "aussen_zu":  ("AUSSEN_GESCHLOSSEN (kein Weg ins Freie)", "#42a5f5",
                   "#0d47a1", "xx"),
    "unbekannt":  ("UNBEKANNT — nicht typisiert", "#ff00ff", "#8b0060", None),
}

#: raum_typ → Kategorie. Typen, die es im Korpus gibt (18 gemessen) plus die
#: im Contract/Code vorkommenden Synonyme. Was hier fehlt, landet in "neben" —
#: NICHT in "unbekannt": unbekannt heißt "gar kein raum_typ".
_TYP_KAT = {
    "ZIMMER": "wohnen", "WOHNZIMMER": "wohnen", "SCHLAFZIMMER": "wohnen",
    "KINDERZIMMER": "wohnen", "WOHNEN": "wohnen",
    "BAD": "nass", "WC": "nass", "DUSCHE": "nass", "BAD_WC": "nass",
    "KÜCHE": "kueche", "KUECHE": "kueche", "WOHNKÜCHE": "kueche",
    "WOHNKUECHE": "kueche",
    "STIEGENHAUS": "stiege", "SCHLEUSE": "stiege", "VORRAUM": "stiege",
    "AUFZUGSVORPLATZ": "stiege", "TREPPENHAUS": "stiege",
    "GANG": "gang_allg", "FLUR": "gang_allg", "KORRIDOR": "gang_allg",
    "ABSTELLRAUM": "neben", "TECHNIK": "neben", "KELLER": "neben",
    "LAGER": "neben", "KINDERWAGENRAUM": "neben", "MUELLRAUM": "neben",
    "MÜLLRAUM": "neben", "WASCHKÜCHE": "neben", "WASCHKUECHE": "neben",
    "GARAGE": "neben", "KELLERABTEIL": "neben",
    "LIFT": "schacht", "SCHACHT": "schacht", "AUFZUG": "schacht",
    "BALKON": "freiflaeche", "LOGGIA": "freiflaeche", "TERRASSE": "freiflaeche",
}

#: Türkürzel — Bestand aus plan_pruefen, hier nur gespiegelt, damit das Bild
#: und die Legende garantiert dieselbe Tabelle benutzen.
_TUER_KUERZEL = dict(pp._TUER_KUERZEL)
#: Owner-Vorgabe: LINIE grün, GRAPH blau, FALLBACK grau (siehe Modul-Docstring).
_SEG_FARBE = {"LINIE": "#00a040", "GRAPH": "#0055cc", "FALLBACK": "#888888"}
_EXIT_FARBE = {"final_exit": "#dd0000", "stair_exit": "#ff8800", "door": "#777777"}
_WOHNUNG_FARBE = "#7b68ee"
_BOGEN_FARBE = "#994400"


def _ausgabename(dxf: Path, belegt: dict[str, Path]) -> str:
    """Eindeutiger Ordnername je Plan — der Dateiname allein reicht NICHT.

    ``Baulegende.dxf`` liegt zweimal im Repo (``Projekte/Rennweg/Legende/`` und
    ``Vorlagen-Legende/``). Beide schrieben in denselben Ordner, der zweite
    überschrieb den ersten: 83 Läufe, aber nur 82 Einträge im Index. Ein Plan
    verschwand lautlos — genau das Gegenteil von "Pläne, die scheitern, nicht
    überspringen". Bei Kollision hängt der übergeordnete Ordner an.
    """
    name = dxf.stem
    vorher = belegt.get(name)
    if vorher is None or vorher == dxf.resolve():
        belegt.setdefault(name, dxf.resolve())
        return name
    eindeutig = f"{name} ({dxf.parent.name})"
    belegt[eindeutig] = dxf.resolve()
    return eindeutig


def _rel(pfad: Path) -> str:
    """Pfad relativ zum Repo — auch wenn er relativ übergeben wurde.

    ``Path.relative_to`` wirft bei einem relativen CLI-Argument; das hat beim
    ersten Lauf sowohl den Normal- als auch den FEHLERpfad gekippt, sodass der
    Fehler-Eintrag gar nicht mehr geschrieben werden konnte. Der Fehlerpfad
    muss selbst robust sein — sonst verschwindet genau der Plan aus dem Index,
    den man sehen will.
    """
    try:
        return pfad.resolve().relative_to(REPO).as_posix()
    except ValueError:
        return pfad.as_posix()


def _kategorie(raum) -> str:
    """Kategorie aus raum_typ UND nutzungsklasse.

    Der Gang ist der einzige Fall, in dem der Typ allein nicht reicht: GANG
    trägt allgemein wie privat denselben ``raum_typ``, der Unterschied steht in
    ``nutzungsklasse``. Der Owner will genau diesen Unterschied sofort sehen.
    """
    typ = (raum.raum_typ or "").upper()
    if not typ:
        return "unbekannt"
    kat = _TYP_KAT.get(typ)
    if kat is None:
        # Kein Eintrag ≠ untypisiert: der Plan hat einen Typ geliefert, wir
        # kennen ihn nur nicht einsortiert. Als Nebenraum zeigen, nicht als
        # UNBEKANNT — sonst behauptet das Bild eine Lücke, die keine ist.
        return "neben"
    if kat == "gang_allg" and (raum.nutzungsklasse or "") == "WOHNUNG_PRIVAT":
        return "gang_priv"
    if kat == "freiflaeche" and (raum.nutzungsklasse or "") == "AUSSEN":
        return "freiflaeche"
    return kat


def _unbelastbar(ausgang, tuer_ids: set[str]) -> str | None:
    """Warum ist dieser Ausgang nicht belastbar? None = belastbar.

    Zwei Fälle, beide vom Owner benannt: kein Türbezug (die ``exit_<id>``
    zeigt auf keine Tür des Modells) und unentscheidbar (die Tür trägt kein
    ``tuer_detail``, ist also nicht typisiert).
    """
    ref = ausgang.id.removeprefix("exit_")
    if ref not in tuer_ids:
        return "ohne Türbezug"
    return None


def _stempel_je_raum(stempel, raeume) -> dict[str, object]:
    """Stempel → Raum über Punkt-in-Polygon. Der Contract führt weder Name noch
    Stempel-m²; beides existiert nur hier."""
    geo = [(r, Polygon(r.polygon_mm).buffer(0)) for r in raeume
           if len(r.polygon_mm) >= 3]
    out: dict[str, object] = {}
    for s in stempel:
        p = Point(s.position_mm)
        for r, g in geo:
            if not g.is_empty and g.contains(p):
                out.setdefault(r.id, s)
                break
    return out


def _raum_label(raum, stmp) -> str:
    """Owner-Vorgabe: Name, Typ, Fläche berechnet, Stempel-m² in Klammern.

    Name und Typ werden NICHT beide gedruckt, wenn sie dasselbe sagen — sonst
    steht "KÜCHE KÜCHE" im Bild (Sichtbefund EG_Grundriss_DE_NEU). Verglichen
    wird ohne Groß-/Kleinschreibung und ohne Trennzeichen, weil der Stempel
    "BAD/WC" und der Typ "BAD" derselbe Raum sind.
    """
    zeilen: list[str] = []
    typ = raum.raum_typ or "?"
    name = str(stmp.name).strip() if stmp is not None and stmp.name else ""

    def _kern(s: str) -> str:
        return "".join(c for c in s.upper() if c.isalnum())

    if name and _kern(name) != _kern(typ):
        zeilen.append(name)
    zeilen.append(typ)
    flaeche = f"{raum.flaeche_m2:.1f} m²"
    if stmp is not None and stmp.flaeche_m2:
        flaeche += f" ({stmp.flaeche_m2:.1f})"
    zeilen.append(flaeche)
    return "\n".join(zeilen)


def _legende(fig, ax, zaehl: Counter) -> None:
    """Legende im Bild — der Owner will sie IM Bild, nicht daneben."""
    hand: list = []
    for key, (text, fc, ec, hatch) in _KAT.items():
        n = zaehl.get(key, 0)
        hand.append(Patch(facecolor=fc, edgecolor=ec, hatch=hatch, alpha=0.55,
                          label=f"{text} ({n})"))
    hand.append(Line2D([], [], color="none", label=""))
    for typ, farbe in _EXIT_FARBE.items():
        if typ == "door":
            continue
        hand.append(Line2D([], [], marker="o", mfc="none", mec=farbe, mew=2.5,
                           ms=11, ls="none",
                           label=f"{typ} ({zaehl.get(typ, 0)})"))
    hand.append(Line2D([], [], marker="o", mfc="none", mec="#dd0000", mew=2.0,
                       ms=11, ls="none", label="unbelastbar (gestrichelt)"))
    hand.append(Line2D([], [], color="none", label=""))
    for q, farbe in _SEG_FARBE.items():
        hand.append(Line2D([], [], color=farbe, lw=2.0,
                           label=f"Fluchtweg {q} ({zaehl.get('seg_' + q, 0)})"))
    hand.append(Line2D([], [], color=_WOHNUNG_FARBE, lw=2.5,
                       label=f"Wohnung ({zaehl.get('wohnungen', 0)})"))
    hand.append(Line2D([], [], color="none", label=""))
    # Die Kürzel MÜSSEN umbrechen: als eine Zeile (~120 Zeichen) zog dieses
    # eine Label die Legendenbox über den Streifen hinaus in den Plan
    # (Sichtbefund EG_Grundriss_DE_NEU) — verdeckter Plan ist das Gegenteil
    # des Auftrags "ich will die Lücken sehen".
    hand.append(Line2D([], [], color=_BOGEN_FARBE, lw=1.5,
                       label="Türbogen — Kürzel:"))
    paare = [*_TUER_KUERZEL.items(), ("unbekannt", "?")]
    for i in range(0, len(paare), 2):
        text = " · ".join(f"{v} {k}" for k, v in paare[i:i + 2])
        hand.append(Line2D([], [], color="none", label="    " + text))
    hand.append(Line2D([], [], color="none", label="    /NA = Notausgang"))
    hand.append(Line2D([], [], color="none", label="    * = ohne Türblatt"))
    ax.legend(handles=hand, loc="upper left", bbox_to_anchor=(0.02, 0.995),
              fontsize=7.5, framealpha=1.0, borderpad=0.7, labelspacing=0.4,
              handlelength=1.6, handletextpad=0.6,
              title="Legende — Ehrlichkeit vor Schönheit",
              title_fontproperties={"weight": "bold", "size": 9})


def _zeichne(plan, zoom, rot, modell, hoefe, wpolys, stmp_je_raum,
             ziel: Path, titel: str) -> tuple[int, int]:
    """Ein Render, alle Overlays drauf, dann Rotation + Legende + Titel."""
    f = plan.factor
    fig, ax = pp._figur(plan, zoom)
    fig.set_dpi(uk._dpi_fuer(plan, ax))
    uk._hintergrund_ausgrauen(ax)
    ax.autoscale(False)
    ztop = pp._ztop(ax)
    labels_xy: list = []
    zaehl: Counter[str] = Counter()
    fs = uk._schriftgroesse(ax, plan)

    # ── Räume: groß zuerst, klein liegt oben ───────────────────────────────
    for r in sorted(modell.raeume, key=lambda r: -r.flaeche_m2):
        if len(r.polygon_mm) < 3:
            continue
        k = _kategorie(r)
        zaehl[k] += 1
        _txt, fc, ec, hatch = _KAT[k]
        xs = [p[0] / f for p in r.polygon_mm]
        ys = [p[1] / f for p in r.polygon_mm]
        ax.fill(xs, ys, color=fc, alpha=0.5, ec=ec, lw=1.6, zorder=ztop)
        if hatch:
            ax.fill(xs, ys, facecolor="none", ec=ec, lw=1.2, hatch=hatch,
                    zorder=ztop + 1)
        if r.flaeche_m2 >= 1.5:
            g = Polygon(r.polygon_mm).buffer(0)
            if not g.is_empty:
                rp = g.representative_point()
                lbl = _raum_label(r, stmp_je_raum.get(r.id))
                if k == "unbekannt":
                    lbl = "?\n" + lbl
                uk._text(ax, rp.x / f, rp.y / f, lbl, fs, ztop + 3, labels_xy,
                         ax, farbe=ec if k == "unbekannt" else "black",
                         fett=k == "unbekannt")

    # ── Innenhöfe: der Contract kennt kein AUSSEN_GESCHLOSSEN, die geschlossenen
    # Höfe kommen nur über provider.letzte_aussenbereiche.geschlossen. ───────
    for g in hoefe:
        zaehl["aussen_zu"] += 1
        for gg in getattr(g, "geoms", [g]):
            xs, ys = zip(*[(x / f, y / f) for x, y in gg.exterior.coords])
            ax.fill(xs, ys, facecolor=_KAT["aussen_zu"][1], alpha=0.4,
                    ec=_KAT["aussen_zu"][2], lw=2.0, hatch="xx", zorder=ztop + 1)

    # ── Wohnungen: Umriss + ID ─────────────────────────────────────────────
    for wid, geom in sorted(wpolys.items()):
        zaehl["wohnungen"] += 1
        for g in getattr(geom, "geoms", [geom]):
            xs, ys = zip(*[(x / f, y / f) for x, y in g.exterior.coords])
            ax.plot(xs, ys, color=_WOHNUNG_FARBE, lw=2.6, zorder=ztop + 5)
        rp = geom.representative_point()
        uk._text(ax, rp.x / f, rp.y / f, wid, fs + 1, ztop + 6, labels_xy, ax,
                 fc=_WOHNUNG_FARBE, fett=True)

    # ── Fluchtwege: Farbe nach Quelle, Pfeil Richtung Ausgang ──────────────
    for s in modell.zirkulation.segmente:
        if len(s.polyline_mm) < 2:
            continue
        q = s.quelle or "FALLBACK"
        zaehl["seg_" + q] += 1
        farbe = _SEG_FARBE.get(q, "#888888")
        pts = [(x / f, y / f) for x, y in s.polyline_mm]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=farbe, lw=1.8,
                ls="--" if s.richtung_unbekannt else "-", alpha=0.95,
                zorder=ztop + 7)
        if not s.richtung_unbekannt:
            pp._pfeil(ax, pts[-2], pts[-1], farbe, ztop + 8)

    # ── Türen: Bogen + Typkürzel ───────────────────────────────────────────
    for t in modell.tueren:
        w = pp._wandwinkel_bei(plan, t.xy_mm) or 0.0
        d = min(max(t.breite_mm or 0.0, pp._BOGEN_ZEICHEN_MIN_MM),
                pp._BOGEN_ZEICHEN_MAX_MM) / f
        ax.add_patch(Arc((t.xy_mm[0] / f, t.xy_mm[1] / f), d, d, angle=w,
                         theta1=0.0, theta2=180.0, color=_BOGEN_FARBE, lw=1.5,
                         zorder=ztop + 9))
        k = pp._tuer_kuerzel(t)
        zaehl["tuer_" + (t.tuer_detail or "unbekannt")] += 1
        ax.text(t.xy_mm[0] / f, t.xy_mm[1] / f, k, ha="center", va="bottom",
                fontsize=max(5.0, fs - 2), color=_BOGEN_FARBE,
                fontweight="bold" if k.startswith("?") else "normal",
                zorder=ztop + 10)

    # ── Ausgänge: unbelastbare gestrichelt ─────────────────────────────────
    tuer_ids = {t.id for t in modell.tueren}
    for a in modell.ausgaenge:
        zaehl[a.typ] += 1
        grund = _unbelastbar(a, tuer_ids)
        x, y = a.xy_mm[0] / f, a.xy_mm[1] / f
        farbe = _EXIT_FARBE.get(a.typ, "#777777")
        ax.plot(x, y, "o", ms=13, mfc="none", mec=farbe, mew=2.6,
                ls="--" if grund else "-", zorder=ztop + 11)
        if grund:
            zaehl["unbelastbar"] += 1
            ax.add_patch(plt.Circle((x, y), 900.0 / f, fill=False, ec=farbe,
                                    ls="--", lw=1.8, zorder=ztop + 11))
            ax.text(x, y, f"  {grund}", ha="left", va="top", fontsize=6,
                    color=farbe, zorder=ztop + 12)

    # ── Ein Render, dann rotieren, dann Legende obendrauf ──────────────────
    tmp = ziel / "_roh.png"
    fig.savefig(str(tmp), facecolor="white", dpi=fig.dpi)
    plt.close(fig)
    img = plt.imread(str(tmp))
    if rot:
        img = np.rot90(img, rot)
    tmp.unlink()

    # Owner-Vorgabe: mindestens 2000 px breit. Die Legende bekommt einen
    # EIGENEN Streifen links — im Bild lag sie über einem ganzen Gebäudeteil
    # (Sichtbefund EG_Grundriss_DE_NEU), und verdeckter Plan ist das Gegenteil
    # von "ich will die Lücken sehen".
    dpi = 100
    plan_px = max(img.shape[1], MIN_BREITE_PX)
    skala = plan_px / img.shape[1]
    hoehe_px = img.shape[0] * skala
    leg_px = 470.0                      # fester Streifen, unabhängig vom Zoom
    titel_px = 46.0
    ges_px = plan_px + leg_px
    fig2 = plt.figure(figsize=(ges_px / dpi, (hoehe_px + titel_px) / dpi),
                      dpi=dpi)
    fig2.patch.set_facecolor("white")
    links = leg_px / ges_px
    unten = titel_px / (hoehe_px + titel_px)
    ax2 = fig2.add_axes([links, unten, 1 - links, 1 - unten])
    ax2.set_axis_off()
    ax2.imshow(img, interpolation="none")
    axl = fig2.add_axes([0, 0, links, 1])
    axl.set_axis_off()
    _legende(fig2, axl, zaehl)
    fig2.text(links + (1 - links) / 2, 0.004, titel, ha="center", va="bottom",
              fontsize=14, fontweight="bold",
              bbox={"fc": "white", "alpha": 0.95, "ec": "#444444", "pad": 5})
    fig2.savefig(str(ziel / "uebersicht_gesamt.png"), facecolor="white")
    plt.close(fig2)
    return int(ges_px), int(hoehe_px + titel_px)


def _kennzahlen(name: str, dxf: Path, modell, provider, wpolys, hoefe,
                px, dauer: float) -> dict:
    """Die vom Owner verlangte Tabelle — je Typ, je Quelle, mit Geschoss-Beleg."""
    befund = getattr(provider, "geschoss_befund", None)
    kat = Counter(_kategorie(r) for r in modell.raeume)
    tuer_ids = {t.id for t in modell.tueren}
    unbelastbar = [{"id": a.id, "typ": a.typ, "grund": g}
                   for a in modell.ausgaenge
                   if (g := _unbelastbar(a, tuer_ids))]
    return {
        "plan": name,
        "dxf": _rel(dxf),
        "sha256": hashlib.sha256(dxf.read_bytes()).hexdigest(),
        "bytes": dxf.stat().st_size,
        "bild_px": list(px),
        "laufzeit_s": round(dauer, 1),
        "geschoss": modell.floor,
        "geschoss_quelle": getattr(befund, "quelle", None),
        "geschoss_beleg": getattr(befund, "beleg", None),
        "ausgangs_warnungen": [str(w) for w in
                               getattr(provider, "ausgangs_warnungen", []) or []],
        "raeume_gesamt": len(modell.raeume),
        "raeume_unbekannt": kat.get("unbekannt", 0),
        "raum_typen": dict(Counter(r.raum_typ for r in modell.raeume
                                   if r.raum_typ)),
        "kategorien": dict(kat),
        "tueren_gesamt": len(modell.tueren),
        "tueren_typisiert": sum(1 for t in modell.tueren if t.tuer_detail),
        "tuer_typen": dict(Counter(t.tuer_detail or "UNBEKANNT"
                                   for t in modell.tueren)),
        "tueren_notausgang": sum(1 for t in modell.tueren if t.ist_notausgang),
        "ausgaenge": dict(Counter(a.typ for a in modell.ausgaenge)),
        "ausgaenge_unbelastbar": unbelastbar,
        "segmente_gesamt": len(modell.zirkulation.segmente),
        "segmente_je_quelle": dict(Counter(s.quelle or "FALLBACK"
                                           for s in modell.zirkulation.segmente)),
        "segmente_richtung_unbekannt": sum(
            1 for s in modell.zirkulation.segmente if s.richtung_unbekannt),
        "wohnungen": len(wpolys),
        "innenhoefe_geschlossen": len(hoefe),
        "stiegenhaeuser": len(modell.stiegenhaeuser),
        "contract_version": modell.contract_version,
    }


def plan_bauen(dxf: Path, out: Path, floor: str | None = None,
               name: str | None = None) -> dict:
    from notbeleuchtung.raumerkennung import ArchitekturRaumProvider

    t0 = time.time()
    name = name or dxf.stem
    ziel = out / name
    ziel.mkdir(parents=True, exist_ok=True)

    # Kein Standardwert EG (Owner-Entscheidung): leer lassen, der Provider
    # entscheidet mehrstufig und meldet bei UNBEKANNT fail closed.
    provider = ArchitekturRaumProvider()
    modell = provider.parse(str(dxf), floor or "")
    ab = getattr(provider, "letzte_aussenbereiche", None)
    hoefe = list(ab.geschlossen) if ab is not None and ab.geschlossen else []

    plan = pp.lade_dxf(dxf)
    stempel = pp.finde_stempel(plan)
    prefix = pp._varianten_prefix(stempel)
    zoom = pp._varianten_bounds(plan, prefix, stempel)
    rot, _vermerk = pp._rotation(plan)
    inhalt = uk._inhalts_bounds(plan, modell, hoefe)
    if inhalt is not None:
        zoom = inhalt
    haupt, _ausserhalb = uk._haupt_cluster(modell, plan)
    if haupt is not None:
        zoom = haupt

    wpolys = pp._wohnungs_umrisse(modell)
    stmp_je_raum = _stempel_je_raum(stempel, modell.raeume)

    befund = getattr(provider, "geschoss_befund", None)
    gq = getattr(befund, "quelle", "?")
    titel = (f"{name} — Raumerkennung · Geschoss "
             f"{modell.floor or 'UNBEKANNT'} (Quelle {gq})")
    px = _zeichne(plan, zoom, rot, modell, hoefe, wpolys, stmp_je_raum, ziel,
                  titel)

    daten = _kennzahlen(name, dxf, modell, provider, wpolys, hoefe, px,
                        time.time() - t0)
    (ziel / "kennzahlen.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")
    return daten


# ── Index ───────────────────────────────────────────────────────────────────

_EINZELBILDER = [("01_render.png", "01 Render"), ("02_raeume.png", "02 Räume"),
                 ("03_rest.png", "03 Rest"), ("04_material.png", "04 Material"),
                 ("05_fluchtweg.png", "05 Fluchtweg"),
                 ("06_platzierung.png", "06 Platzierung"),
                 ("07_referenzvergleich.png", "07 Referenzvergleich")]

_CSS = """
:root{color-scheme:light dark;--bg:#f7f7f8;--fg:#1a1a1a;--kart:#fff;
--rand:#d8d8dc;--muted:#666;--warn:#b00020}
@media (prefers-color-scheme:dark){:root{--bg:#16161a;--fg:#e8e8ea;
--kart:#1f1f24;--rand:#33333a;--muted:#a0a0a8}}
*{box-sizing:border-box}
body{margin:0;padding:16px;background:var(--bg);color:var(--fg);
font:14px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
h1{font-size:22px;margin:0 0 4px}
.sub{color:var(--muted);margin-bottom:20px}
.nav{position:sticky;top:0;background:var(--bg);padding:10px 0;
border-bottom:1px solid var(--rand);margin-bottom:18px;z-index:5}
.nav a{display:inline-block;margin:2px 8px 2px 0;font-size:12px}
.plan{background:var(--kart);border:1px solid var(--rand);border-radius:10px;
padding:16px;margin-bottom:26px}
.plan h2{margin:0 0 2px;font-size:18px}
.pfad{color:var(--muted);font-size:12px;word-break:break-all;margin-bottom:12px}
img{max-width:100%;height:auto;border:1px solid var(--rand);border-radius:6px;
background:#fff}
table{border-collapse:collapse;margin:12px 0;font-size:13px}
td,th{border:1px solid var(--rand);padding:4px 9px;text-align:left;
vertical-align:top}
th{background:rgba(127,127,127,.12);font-weight:600}
.num{text-align:right;font-variant-numeric:tabular-nums}
.fehler{background:rgba(176,0,32,.1);border-left:4px solid var(--warn);
padding:10px 12px;border-radius:4px}
.fehler pre{white-space:pre-wrap;font-size:11px;margin:6px 0 0;max-height:16em;
overflow:auto}
.warn{color:var(--warn);font-weight:600}
details{margin-top:12px}
summary{cursor:pointer;font-weight:600;padding:4px 0}
.gal{display:flex;flex-wrap:wrap;gap:12px;margin-top:10px}
.gal figure{margin:0;flex:1 1 380px;min-width:280px}
.gal figcaption{font-size:12px;color:var(--muted);margin-bottom:4px}
"""


def _tabelle(d: dict) -> str:
    def z(label, wert, klasse="num"):
        return f"<tr><th>{label}</th><td class='{klasse}'>{wert}</td></tr>"

    typen = ", ".join(f"{k} {v}" for k, v in
                      sorted(d["raum_typen"].items(), key=lambda x: -x[1]))
    ttypen = ", ".join(f"{k} {v}" for k, v in
                       sorted(d["tuer_typen"].items(), key=lambda x: -x[1]))
    ausg = ", ".join(f"{k} {v}" for k, v in d["ausgaenge"].items()) or "—"
    segq = ", ".join(f"{k} {v}" for k, v in d["segmente_je_quelle"].items()) or "—"
    unb = d["ausgaenge_unbelastbar"]
    unb_s = (f"<span class='warn'>{len(unb)}</span> — "
             + ", ".join(f"{u['id']} ({u['grund']})" for u in unb)) if unb else "0"
    unbek = d["raeume_unbekannt"]
    unbek_s = f"<span class='warn'>{unbek}</span>" if unbek else "0"
    warn = d.get("ausgangs_warnungen") or []
    rows = [
        z("Geschoss", f"<b>{d['geschoss'] or 'UNBEKANNT'}</b> "
          f"(Quelle {d['geschoss_quelle']})", ""),
        z("Beleg", f"<code>{(d['geschoss_beleg'] or '—')[:120]}</code>", ""),
        z("Räume gesamt", d["raeume_gesamt"]),
        z("davon UNBEKANNT", unbek_s),
        z("Raumtypen", typen or "—", ""),
        z("Türen gesamt", d["tueren_gesamt"]),
        z("davon typisiert", d["tueren_typisiert"]),
        z("Türtypen", ttypen or "—", ""),
        z("Notausgang-Flag", d["tueren_notausgang"]),
        z("Ausgänge", ausg, ""),
        z("davon unbelastbar", unb_s, ""),
        z("Fluchtwegsegmente", d["segmente_gesamt"]),
        z("je Quelle", segq, ""),
        z("Richtung unbekannt", d["segmente_richtung_unbekannt"]),
        z("Wohnungen", d["wohnungen"]),
        z("Innenhöfe geschlossen", d["innenhoefe_geschlossen"]),
        z("Stiegenhäuser", d["stiegenhaeuser"]),
        z("Laufzeit", f"{d['laufzeit_s']} s"),
    ]
    if warn:
        rows.append(z("Warnungen", "<span class='warn'>"
                      + "<br>".join(warn) + "</span>", ""))
    return "<table>" + "".join(rows) + "</table>"


def index_bauen(out: Path) -> Path:
    plaene = []
    for d in sorted(out.iterdir()):
        if not d.is_dir():
            continue
        kz = d / "kennzahlen.json"
        if kz.exists():
            plaene.append((d, json.loads(kz.read_text(encoding="utf-8"))))
    # check=False: ohne git-Repo (ausgepackter Ordner) soll der Index trotzdem
    # entstehen — dann steht dort "?" statt eines Commits.
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True, check=False,
                            cwd=REPO).stdout.strip() or "?"
    ok = [p for p in plaene if not p[1].get("fehler")]
    fehler = [p for p in plaene if p[1].get("fehler")]

    kopf = (
        "<!doctype html><html lang='de'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>Raumerkennung — Gesamtdarstellung</title>"
        f"<style>{_CSS}</style></head><body>"
    )
    unter = (
        f"<div class='sub'>Stand <code>{commit}</code> · {len(plaene)} Pläne"
        f" · {len(ok)} ausgewertet · {len(fehler)} nicht auswertbar<br>"
        "Ehrlichkeit vor Schönheit: untypisierte Räume magenta,"
        " unbekannte Türen <code>?</code>,"
        " unbelastbare Ausgänge gestrichelt.</div>"
    )
    teile = [kopf,
             "<h1>Raumerkennung — Gesamtdarstellung aller Pläne</h1>",
             unter,
             "<div class='nav'>"]
    for d, kz in plaene:
        mark = "" if not kz.get("fehler") else " ⚠"
        teile.append(f"<a href='#{d.name}'>{d.name}{mark}</a>")
    teile.append("</div>")

    for d, kz in plaene:
        teile.append(f"<div class='plan' id='{d.name}'>")
        teile.append(f"<h2>{d.name}</h2>")
        teile.append(f"<div class='pfad'>{kz.get('dxf', '')}</div>")
        if kz.get("fehler"):
            teile.append("<div class='fehler'><b>nicht auswertbar</b>"
                         f"<pre>{kz['fehler']}</pre></div>")
        else:
            bild = d / "uebersicht_gesamt.png"
            if bild.exists():
                teile.append(f"<a href='{d.name}/uebersicht_gesamt.png'>"
                             f"<img src='{d.name}/uebersicht_gesamt.png' "
                             f"alt='Übersicht {d.name}' loading='lazy'></a>")
            teile.append(_tabelle(kz))
            vorhanden = [(f, t) for f, t in _EINZELBILDER if (d / f).exists()]
            if vorhanden:
                teile.append("<details><summary>Einzelbilder der Prüfstrecke "
                             f"({len(vorhanden)})</summary><div class='gal'>")
                for f, t in vorhanden:
                    teile.append(f"<figure><figcaption>{t}</figcaption>"
                                 f"<a href='{d.name}/{f}'>"
                                 f"<img src='{d.name}/{f}' alt='{t}' "
                                 f"loading='lazy'></a></figure>")
                teile.append("</div></details>")
        teile.append("</div>")

    teile.append("</body></html>")
    ziel = out / "index.html"
    ziel.write_text("".join(teile), encoding="utf-8")
    return ziel


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dxf", nargs="?", help="ein Plan; ohne = alle DXF im Repo")
    ap.add_argument("--out", default=str(AUSGABE))
    ap.add_argument("--floor", default=None)
    ap.add_argument("--nur-index", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    if a.nur_index:
        print(f"Index: {index_bauen(out)}")
        return 0

    if a.dxf:
        plaene = [Path(a.dxf)]
    else:
        plaene = sorted(p for p in REPO.rglob("*.dxf")
                        if ".git" not in p.parts)
    print(f"{len(plaene)} Pläne", flush=True)

    fehler = 0
    belegt: dict[str, Path] = {}
    for i, p in enumerate(plaene, 1):
        name = _ausgabename(p, belegt)
        print(f"[{i}/{len(plaene)}] {name} …", flush=True)
        ziel = out / name
        try:
            d = plan_bauen(p, out, a.floor, name)
            print(f"   ok — {d['raeume_gesamt']} Räume "
                  f"({d['raeume_unbekannt']} unbekannt), "
                  f"{d['tueren_gesamt']} Türen, Geschoss "
                  f"{d['geschoss'] or 'UNBEKANNT'}/{d['geschoss_quelle']}, "
                  f"{d['bild_px'][0]}×{d['bild_px'][1]} px, "
                  f"{d['laufzeit_s']} s", flush=True)
        except Exception as e:  # noqa: BLE001 — ein Plan darf den Lauf nicht kippen
            fehler += 1
            ziel.mkdir(parents=True, exist_ok=True)
            (ziel / "kennzahlen.json").write_text(
                json.dumps({"plan": name,
                            "dxf": _rel(p),
                            "fehler": traceback.format_exc()},
                           ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"   FEHLER: {e!r} — weiter", file=sys.stderr, flush=True)
            plt.close("all")

    ziel = index_bauen(out)
    print(f"\n{len(plaene) - fehler} ok · {fehler} Fehler\nIndex: {ziel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
