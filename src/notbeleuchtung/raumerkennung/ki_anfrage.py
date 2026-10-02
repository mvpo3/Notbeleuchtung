"""ki_anfrage — Anfrage-Aufbau der zweiten Meinung aus dem Plan (Abschnitt 3 Teil B).

Die Engine misst, die KI liest (Entscheid 3, ``docs/AUFTRAG_2026-10-01.md`` § 3). Hier
entsteht je Geschoss EINE Frage (``GeschossAnfrage``), große Pläne in vier Quadranten wie
beim Vision-Audit (längste Seite der Raum-Hülle über ``QUADRANT_AB_MM``, 1 m Überlappung,
NW/NO/SW/SO): das gerenderte Geschoss mit Raum-IDs als PNG und je Raum die Merkmale, die
die Engine kennt — Typ und Beleg (``belege_je_raum``: stempel | kuerzel | erscheinungsbild |
geometrie | leer), Texte im Polygon, Fläche, Möbel-/Sanitärblöcke (``sanitaer.moebelobjekte``),
Fenster (``fenster_signatur``), Treppenläufe (``objekt_stiege``), Lift-Texte/-Blöcke, Türen mit
korrigierter Rolle und Blatt, Wohnung, Lage zur Wohnungseingangstür, Nutzungsklasse,
Nachbarräume (≤ ``wohnungsumriss.NACHBAR_MM``). Der Kanon und die Ausgangs-Definition stehen
im Prompt (``ki_zweitmeinung.baue_prompt``).

Bild: derselbe Weg wie ``scripts/plan_pruefen._figur`` (ezdxf-Zeichen-Addon auf eine
matplotlib-Achse, weißer Grund, ``min_dash_length`` gegen Punkt-Linientypen) — einmal
gezeichnet, je Quadrant ein Ausschnitt; Räume halbtransparent (untypisiert magenta), Label
= Raum-ID (+ Engine-Typ). ``stempel_abdecken`` (Eichung, Phase B) lässt alle TEXT/MTEXT/
ATTRIB weg — auch in Blöcken — und streicht ``texte`` aus den Merkmalen. matplotlib ist
eine optionale Abhängigkeit (``render``/``dev``) und wird erst beim Rendern importiert:
ohne KI wird nichts gerendert.

``zweite_meinung`` ist der eine Einstieg für ``provider.parse``: Belege → ohne KI nur die
Herkunft „Engine" je Raum; mit KI Anfragen → Cache → Bild nur für Fragen ohne Cache-Treffer
→ Backend → ``zweitmeinung_anwenden`` (Freigabeliste, K3-Sanitärregel als bestätigende
Regel, Lift-/Schacht-Evidenz) → ``KiErgebnis`` (Herkunft je Raum, ``ki:``-Warnungen,
Anzahl Anfragen und Cache-Treffer). Fehler sind Warnungen, nie Abbruch.
"""
from __future__ import annotations

import re
import tempfile
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass, field, replace
from pathlib import Path

from shapely.geometry import Point, Polygon
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union
from shapely.strtree import STRtree

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer

from . import raumtyp
from .dxf_load import XY, DxfPlan
from .ki_zweitmeinung import (
    GeschossAnfrage,
    Herkunft,
    KiKonfig,
    RaumAnfrage,
    Zweitmeinung,
    zweitmeinung_anwenden,
)
from .lift_erkennung import _LIFT_BLOCK, _lift_texte
from .raumtyp import raumtyp_flags
from .rest_komponenten import _schacht_text_punkte
from .sanitaer import moebelobjekte, sanitaer_typ, sanitaerobjekte
from .stempel_anker import Zuordnung, _block_texte, flaeche_aus_text
from .tuer_zuordnung import AUSSEN, KEIN_RAUM
from .wohnungsklasse import korrigierte_rollen
from .wohnungsumriss import NACHBAR_MM

#: Ab dieser längsten Seite der Raum-Hülle wird das Geschoss in vier Quadranten gefragt
#: (Vision-Audit: Stempel und Möbel bleiben lesbar).
QUADRANT_AB_MM = 40_000.0
_UEBERLAPPUNG_HALB_MM = 500.0        # 1 m Überlappung wie beim Vision-Audit
_RAND_MM = 1000.0                    # Bildrand um den Ausschnitt
BILD_LANG_PX = 1600                  # längste Seite des Bilds
_MIN_STRICH_MM = 50.0                # wie plan_pruefen._MIN_STRICH_MM (RAM, Punkt 2f)
_FENSTER_NAH_MM = 400.0              # Fenstermitte liegt in der Wand, bis dahin zählt es zum Raum
_TEXTE_MAX = 16                      # Texte je Raum im Prompt

_KUERZEL_HINWEIS = re.compile(r"^(\S+): (?:Kürzel|Stempel »)")
_FREI_ENTSCHEID2 = re.compile(r"neuer Raum (\S+) \S+,.*Entscheid 2")
_SANITAER_BEFUND = re.compile(r"^(\S+): (?:BAD|WC) aus Sanitärbeleg")


# --- Belege -------------------------------------------------------------------------------

def belege_je_raum(raeume: Sequence[Raum], zuordnungen: Sequence[Zuordnung],
                   hinweise: Sequence[str], sanitaer_befund: Sequence[str],
                   freiflaeche_befund: Sequence[str], plan: DxfPlan | None = None,
                   ) -> dict[str, str]:
    """Woher der Engine-Typ kommt: stempel (zugeordneter Raumstempel der Kaskade, auch ohne
    Kanon-Typ; ohne Kaskade der Stempel von ``raumtyp.beschrifte_raeume`` im Polygon),
    kuerzel (Entscheid 1 in der Kaskade, Entscheid 2 an ``frei_*``), erscheinungsbild
    (K3-Sanitärbeleg), geometrie (alle anderen Typen: Treppen-/Schacht-/Gang-Regeln),
    leer = ohne Typ und ohne Stempel (UNBEKANNT/UNBESTIMMT)."""
    gestempelt = {z.raum.id for z in zuordnungen if z.raum is not None}
    kuerzel = ({m.group(1) for h in hinweise if (m := _KUERZEL_HINWEIS.match(h))}
               | {m.group(1) for b in freiflaeche_befund if (m := _FREI_ENTSCHEID2.search(b))})
    sanit = {m.group(1) for b in sanitaer_befund if (m := _SANITAER_BEFUND.match(b))}
    stempel_texte: list[tuple[str, XY]] | None = None
    out: dict[str, str] = {}
    for r in raeume:
        if r.id in gestempelt:
            out[r.id] = "stempel"
        elif r.raum_typ and r.id in kuerzel:
            out[r.id] = "kuerzel"
        elif r.raum_typ and r.id in sanit:
            out[r.id] = "erscheinungsbild"
        elif r.raum_typ:
            out[r.id] = "geometrie"
            if plan is not None and len(r.polygon_mm) >= 3:
                if stempel_texte is None:   # Wandzyklen-Pfad: Stempel von beschrifte_raeume
                    stempel_texte = [(t, xy) for t, xy in raumtyp._stempel(plan)
                                     if raumtyp_flags(t) is not None]
                g = Polygon(r.polygon_mm).buffer(0)
                if any(raumtyp_flags(t)[0] == r.raum_typ and g.covers(Point(xy))
                       for t, xy in stempel_texte):
                    out[r.id] = "stempel"
        else:
            out[r.id] = ""
    return out


# --- Merkmale -----------------------------------------------------------------------------

def _polygone(raeume: Sequence[Raum]) -> list[tuple[Raum, Polygon]]:
    out = []
    for r in raeume:
        if len(r.polygon_mm) < 3:
            continue
        p = Polygon(r.polygon_mm).buffer(0)
        if not p.is_empty:
            out.append((r, p))
    return out


def _je_raum(polys: list[tuple[Raum, Polygon]], punkte: Sequence[tuple[str, XY]],
             nah_mm: float = 0.0) -> dict[str, list[str]]:
    """Punkt → kleinster deckender Raum (bis ``nah_mm`` außerhalb); ``{raum_id: [wert]}``."""
    out: dict[str, list[str]] = {}
    if not polys or not punkte:
        return out
    baum = STRtree([p for _, p in polys])
    for wert, xy in punkte:
        pt = Point(xy)
        kand = [int(i) for i in baum.query(pt.buffer(nah_mm) if nah_mm else pt)
                if polys[int(i)][1].distance(pt) <= nah_mm]
        if kand:
            r = polys[min(kand, key=lambda i: polys[i][1].area)][0]
            out.setdefault(r.id, []).append(wert)
    return out


def _texte(plan: DxfPlan) -> list[tuple[str, XY]]:
    """Alle Texte des Plans (mm): TEXT/MTEXT, dazu ATTRIBs und Blocktexte der INSERTs —
    Rennweg-Stempel sind Blöcke mit Attributen (``stempel_anker._stempel_aus_insert``)."""
    out: list[tuple[str, XY]] = []
    for e in plan.space:
        t = e.dxftype()
        if t in ("MTEXT", "TEXT"):
            txt = e.plain_text() if t == "MTEXT" else e.dxf.text
            if (s := " ".join(str(txt or "").split())):
                out.append((s, plan._scale(e.dxf.insert)))
        elif t == "INSERT":
            px, py = float(e.dxf.insert[0]), float(e.dxf.insert[1])
            for a in e.attribs or []:
                if (s := " ".join(str(a.dxf.text or "").split())):
                    out.append((s, plan._scale((px, py))))
            out += [(" ".join(txt.split()), plan._scale(xy))
                    for txt, xy in _block_texte(plan.doc, e.dxf.name, px, py)]
    return out


def _stempel_zuerst(t: str) -> tuple[int, str]:
    """Stempel-artige Texte (Wörterbuch-Treffer, Flächenzeile) vor dem Rest — die Liste je
    Raum ist auf ``_TEXTE_MAX`` gekappt."""
    return (0 if raumtyp_flags(t) is not None or flaeche_aus_text(t) is not None else 1, t)


def _fenster(plan: DxfPlan, wandflaeche: BaseGeometry | None) -> list[tuple[str, XY]]:
    from .fenster_signatur import finde_rahmenfenster, wandsegmente
    return [("fenster", f.mitte_mm) for f in finde_rahmenfenster(wandsegmente(plan), wandflaeche)]


def _stiegen(plan: DxfPlan) -> list[Polygon]:
    from .objekt_stiege import finde_stiegen
    return [Polygon(s.polygon_mm) for s in finde_stiegen(plan) if len(s.polygon_mm) >= 3]


def lift_punkte(plan: DxfPlan) -> list[XY]:
    """Lift-Texte und -Blöcke (mm) — Merkmal ``lift`` je Raum."""
    return list(_lift_texte(plan)) + [
        plan._scale(e.dxf.insert) for e in plan.space
        if e.dxftype() == "INSERT" and _LIFT_BLOCK.search(str(e.dxf.name))]


def lift_schacht_punkte(plan: DxfPlan) -> list[XY]:
    """Lift-Punkte plus Schacht-Beschriftungen (SCHACHT, DDB/BDB; ``rest_komponenten``) —
    Evidenz für die KEIN_RAUM-Typen LIFT und SCHACHT."""
    return lift_punkte(plan) + list(_schacht_text_punkte(plan))


def _tueren_je_raum(tueren: Sequence[Tuer], raeume: Sequence[Raum]) -> dict[str, list[dict]]:
    rollen = korrigierte_rollen(list(raeume), list(tueren)) if tueren else {}
    out: dict[str, list[dict]] = {}
    for t in tueren:
        for seite, andere in ((t.von_raum, t.nach_raum), (t.nach_raum, t.von_raum)):
            if seite in (None, AUSSEN, KEIN_RAUM):
                continue
            out.setdefault(seite, []).append({
                "id": t.id, "rolle": rollen.get(t.id, t.tuer_detail),
                "blatt": not t.ohne_tuerblatt,
                "zu": None if andere in (None, KEIN_RAUM) else andere})
    return out


def _nachbarn(polys: list[tuple[Raum, Polygon]]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    if not polys:
        return out
    baum = STRtree([p for _, p in polys])
    for r, p in polys:
        nah = [polys[int(i)][0] for i in baum.query(p.buffer(NACHBAR_MM))
               if polys[int(i)][0].id != r.id and polys[int(i)][1].distance(p) <= NACHBAR_MM]
        out[r.id] = [f"{n.id} {n.raum_typ or '—'}" for n in sorted(nah, key=lambda n: n.id)]
    return out


def quadranten(polys: Sequence[Polygon]) -> list[tuple[str, tuple[float, float, float, float]]]:
    """``[(name, (x0, y0, x1, y1))]`` in mm: ein Ausschnitt ``""`` (ganz) oder vier Quadranten
    mit 1 m Überlappung, sobald die längste Seite der Raum-Hülle ``QUADRANT_AB_MM``
    übersteigt (wie ``audit_render`` des Vision-Audits)."""
    if not polys:
        return []
    x0, y0, x1, y1 = unary_union(list(polys)).bounds
    if max(x1 - x0, y1 - y0) <= QUADRANT_AB_MM:
        return [("", (x0, y0, x1, y1))]
    xm, ym, h = (x0 + x1) / 2, (y0 + y1) / 2, _UEBERLAPPUNG_HALB_MM
    return [("NW", (x0, ym - h, xm + h, y1)), ("NO", (xm - h, ym - h, x1, y1)),
            ("SW", (x0, y0, xm + h, ym + h)), ("SO", (xm - h, y0, x1, ym + h))]


def _quadrant_von(p: Polygon, quadr: list[tuple[str, tuple[float, float, float, float]]]) -> str:
    if len(quadr) == 1:
        return quadr[0][0]
    x0, y0 = quadr[0][1][0], quadr[2][1][1]
    x1, y1 = quadr[1][1][2], quadr[0][1][3]
    xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
    c = p.representative_point()
    return ("N" if c.y >= ym else "S") + ("W" if c.x < xm else "O")


def baue_anfragen(plan: DxfPlan, dxf_path: str | Path, geschoss: str, raeume: Sequence[Raum],
                  tueren: Sequence[Tuer], belege: dict[str, str], *,
                  stempel_abdecken: bool = False, bilder: dict[str, Path] | None = None,
                  wandflaeche: BaseGeometry | None = None,
                  quadr: list[tuple[str, tuple[float, float, float, float]]] | None = None,
                  ) -> list[GeschossAnfrage]:
    """Je Quadrant mit Räumen eine ``GeschossAnfrage`` mit den Merkmalen je Raum.

    ``bilder`` = ``{quadrant: PNG}`` (leer → Anfragen ohne Bild, z. B. vor dem Cache-Blick);
    ``wandflaeche`` = Union der Wandkörper für die Fenster-Öffnungsprobe (None = Rohbefund).
    """
    polys = _polygone(raeume)
    if not polys:
        return []
    quadr = quadr or quadranten([p for _, p in polys])
    texte = {} if stempel_abdecken else _je_raum(polys, _texte(plan))
    objekte = _je_raum(polys, moebelobjekte(plan))
    fenster = _je_raum(polys, _fenster(plan, wandflaeche), _FENSTER_NAH_MM)
    lifte = _je_raum(polys, [("lift", xy) for xy in lift_punkte(plan)])
    stiegen = _stiegen(plan)
    tueren_je = _tueren_je_raum(tueren, raeume)
    nachbarn = _nachbarn(polys)
    je_quadrant: dict[str, list[RaumAnfrage]] = {}
    for r, p in polys:
        m: dict[str, object] = {"flaeche_m2": round(r.flaeche_m2, 1)}
        if not stempel_abdecken:
            m["texte"] = sorted(texte.get(r.id, []), key=_stempel_zuerst)[:_TEXTE_MAX]
        tj = tueren_je.get(r.id, [])
        m |= {
            "objekte": dict(sorted(Counter(objekte.get(r.id, [])).items())),
            "fenster": len(fenster.get(r.id, [])),
            "stiegen": sum(1 for s in stiegen if s.intersects(p)),
            "lift": bool(lifte.get(r.id)),
            "tueren": tj,
            "wohnung": r.wohnung_id,
            "wohnungseingang_am_raum": any(t["rolle"] == "wohnungseingang" for t in tj),
            "klasse": r.nutzungsklasse,
            "nachbarn": nachbarn.get(r.id, []),
        }
        je_quadrant.setdefault(_quadrant_von(p, quadr), []).append(
            RaumAnfrage(r.id, r.raum_typ or "", belege.get(r.id, ""), m))
    bilder = bilder or {}
    return [GeschossAnfrage(plan_datei=Path(dxf_path), geschoss=geschoss, quadrant=q,
                            raeume=tuple(je_quadrant[q]),
                            bilder=(bilder[q],) if q in bilder else ())
            for q, _ in quadr if q in je_quadrant]


# --- Bild ---------------------------------------------------------------------------------

def rendere_bilder(plan: DxfPlan, raeume: Sequence[Raum], ordner: Path,
                   quadr: list[tuple[str, tuple[float, float, float, float]]], *,
                   stempel_abdecken: bool = False, lang_px: int = BILD_LANG_PX) -> dict[str, Path]:
    """Geschoss einmal zeichnen (wie ``plan_pruefen._figur``), Räume mit Raum-ID
    überlagern, je Quadrant einen Ausschnitt speichern → ``{quadrant: PNG}``."""
    from ezdxf.addons.drawing import Frontend, RenderContext
    from ezdxf.addons.drawing.config import Configuration
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    from ezdxf.addons.drawing.properties import LayoutProperties
    from matplotlib.figure import Figure

    class _OhneText(Frontend):
        """Eichung: kein TEXT/MTEXT/ATTRIB im Bild — auch nicht aus Blöcken."""

        def draw_text_entity(self, entity, properties) -> None:
            return None

        def draw_mtext_entity(self, entity, properties) -> None:
            return None

    doc = plan.doc
    if "Standard" in doc.styles:   # SHX-'txt' hat Glyph-Lücken im mpl-Backend
        doc.styles.get("Standard").dxf.font = "DejaVuSans.ttf"
    f = plan.factor
    lang = lang_px / 100.0
    fig = Figure(figsize=(lang, lang), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    lp = LayoutProperties.from_layout(doc.modelspace())
    lp.set_colors("#FFFFFF")
    cfg = Configuration(min_dash_length=_MIN_STRICH_MM / f)
    frontend = (_OhneText if stempel_abdecken else Frontend)(
        RenderContext(doc), MatplotlibBackend(ax), config=cfg)
    frontend.draw_layout(plan.space, finalize=True, layout_properties=lp)
    ax.set_aspect("equal", adjustable="box")   # Ausschnitt bestimmt die Grenzen, nicht umgekehrt
    ztop = max((c.get_zorder() for c in ax.get_children()), default=0.0) + 1.0
    for r, p in _polygone(raeume):
        xs, ys = zip(*[(x / f, y / f) for x, y in r.polygon_mm], strict=True)
        farbe = "#4a90d9" if r.raum_typ else "#ff00ff"
        ax.fill(xs, ys, color=farbe, alpha=0.18 if r.raum_typ else 0.28, ec=farbe, lw=1.2,
                zorder=ztop)
        c = p.representative_point()
        ax.text(c.x / f, c.y / f, r.id + (f"\n{r.raum_typ}" if r.raum_typ else "\n?"),
                ha="center", va="center", fontsize=7, color="black", zorder=ztop + 1,
                bbox={"fc": "white", "alpha": 0.7, "ec": "none", "pad": 1})
    ordner = Path(ordner)
    ordner.mkdir(parents=True, exist_ok=True)
    out: dict[str, Path] = {}
    for name, (x0, y0, x1, y1) in quadr:
        ax.set_xlim((x0 - _RAND_MM) / f, (x1 + _RAND_MM) / f)
        ax.set_ylim((y0 - _RAND_MM) / f, (y1 + _RAND_MM) / f)
        w, h = max(x1 - x0 + 2 * _RAND_MM, 1.0), max(y1 - y0 + 2 * _RAND_MM, 1.0)
        fig.set_size_inches(lang if w >= h else lang * w / h, lang if h > w else lang * h / w)
        pfad = ordner / f"geschoss_{name or 'ganz'}.png"
        fig.savefig(str(pfad), facecolor="white")
        out[name] = pfad
    return out


# --- Einstieg für den Provider ------------------------------------------------------------

@dataclass
class KiErgebnis:
    """Prüfstrecken-Ausgabe der zweiten Meinung (Provider-Attribut, kein Contract-Feld)."""

    an: bool = False
    backend: str = ""
    modell: str = ""
    herkunft: list[Herkunft] = field(default_factory=list)
    warnungen: list[str] = field(default_factory=list)   # ``ki: …`` → bericht.md „Warnungen"
    fragen: int = 0        # gestellte Fragen (Geschoss bzw. Quadranten)
    anfragen: int = 0      # echte Backend-Aufrufe
    treffer: int = 0       # Cache-Treffer


def _sanitaer_regel(plan: DxfPlan):
    """Bestehende Regel K3 als Bestätigung eines Notlicht-Verlust-Typs: die Sanitärobjekte im
    Polygon ergeben nach ``sanitaer_typ`` genau diesen Typ (BAD/WC)."""
    objekte: list[tuple[str, XY]] | None = None

    def regel(raum: Raum, typ: str) -> bool:
        nonlocal objekte
        if objekte is None:
            objekte = sanitaerobjekte(plan)
        g = Polygon(raum.polygon_mm).buffer(0)
        return sanitaer_typ(Counter(a for a, xy in objekte if g.contains(Point(xy)))) == typ
    return regel


def _kein_raum_evidenz(plan: DxfPlan):
    punkte: list[XY] | None = None

    def evidenz(raum: Raum, typ: str) -> str:
        nonlocal punkte
        if punkte is None:
            punkte = lift_schacht_punkte(plan)
        g = Polygon(raum.polygon_mm).buffer(0)
        if any(g.covers(Point(p)) for p in punkte):
            return ""
        return "kein Lift-/Schacht-Text oder -Block im Polygon"
    return evidenz


def zweite_meinung(plan: DxfPlan, dxf_path: str | Path, geschoss: str, raeume: list[Raum],
                   tueren: Sequence[Tuer], *, zuordnungen: Sequence[Zuordnung],
                   hinweise: Sequence[str], sanitaer_befund: Sequence[str],
                   freiflaeche_befund: Sequence[str], wandflaeche: BaseGeometry | None = None,
                   konfig: KiKonfig | None = None, backend=None) -> KiErgebnis:
    """Belege → (ohne KI: Herkunft „Engine") → Anfragen → Cache/Bild/Backend → anwenden.

    Wirft nie; jeder Fehler wird eine ``ki:``-Warnung, das Engine-Ergebnis bleibt.
    """
    konfig = konfig or KiKonfig.aus_umgebung()
    belege = belege_je_raum(raeume, zuordnungen, hinweise, sanitaer_befund, freiflaeche_befund,
                            plan)
    erg = KiErgebnis(an=konfig.an, backend=konfig.backend if konfig.an else "",
                     modell=konfig.modell if konfig.an else "")
    if not konfig.an:
        erg.herkunft = [Herkunft(r.id, "Engine", r.raum_typ or "", belege.get(r.id, ""),
                                 grund="KI aus") for r in raeume]
        return erg
    gesehen: set[str] = set()
    try:
        zm = Zweitmeinung(konfig, backend=backend)
        polys = _polygone(raeume)
        quadr = quadranten([p for _, p in polys])
        anfragen = baue_anfragen(plan, dxf_path, geschoss, raeume, tueren, belege,
                                 stempel_abdecken=konfig.stempel_abdecken, wandflaeche=wandflaeche,
                                 quadr=quadr)
        erg.fragen = len(anfragen)
        offen = {a.quadrant for a in anfragen if not zm.im_cache(a)}
        regel, evidenz = _sanitaer_regel(plan), _kein_raum_evidenz(plan)
        with tempfile.TemporaryDirectory(prefix="nb_ki_bild_") as td:
            if offen:
                bilder = rendere_bilder(plan, raeume, Path(td), [q for q in quadr if q[0] in offen],
                                        stempel_abdecken=konfig.stempel_abdecken)
                anfragen = [replace(a, bilder=(bilder[a.quadrant],)) if a.quadrant in bilder else a
                            for a in anfragen]
            for a in anfragen:
                antwort = zm.frage(a)
                erg.herkunft += zweitmeinung_anwenden(
                    raeume, a, antwort, freigabe=konfig.freigabe, regel_bestaetigt=regel,
                    evidenz=evidenz)
                gesehen |= a.raum_ids
        erg.warnungen, erg.anfragen, erg.treffer = list(zm.warnungen), zm.anfragen, zm.treffer
    except Exception as exc:  # noqa: BLE001 — zweite Meinung darf den Parse nie killen (Auftrag § 3)
        erg.warnungen.append(f"ki: sonstig — {type(exc).__name__}: {exc}; Engine-Ergebnis bleibt "
                             "unverändert, Räume ohne Typ bleiben UNBESTIMMT mit Notlicht")
    erg.herkunft += [Herkunft(r.id, "Engine", r.raum_typ or "", belege.get(r.id, ""),
                              grund="ohne KI-Anfrage" + (" (Fehler, s. Warnungen)"
                                                         if erg.warnungen else ""))
                     for r in raeume if r.id not in gesehen
                     and r.id not in {h.raum_id for h in erg.herkunft}]
    return erg
