"""Raumerkennungs-Darstellung — nur Räume, ein großes Bild je Plan, Ordner für Ordner.

Owner-Auftrag (Selman, 2026-09-13): den reinen Raumerkennungs-Output über die
leeren Architektenpläne in ``Projekte_Leere Architektpläne (Input)/`` sehen —
keine Fluchtwege, keine Ausgänge, keine Türtypen, keine Platzierung. Nur
messen und darstellen, nichts an der Erkennung reparieren.

Ehrlichkeit vor Schönheit:
  * untypisiert bleibt magenta mit ``?``;
  * ein Stempel, der NICHT im zugeordneten Raum liegt (mehr als 0,3 m daneben
    oder im Inneren eines anderen Raums), wird nicht verschoben, sondern als
    Linie vom Stempelpunkt (○) zum zugeordneten Raum (●) gezeichnet;
  * weicht die berechnete Fläche > 10 % vom Stempel-m² ab, steht die Zahl rot;
  * ein Raum, dessen Beschriftung keinen Platz findet, bekommt ein □ und wird
    in Legende und Index gezählt — kein Label verschwindet lautlos;
  * Nicht-Grundrisse (Dateiname), Pläne ohne erkannte Räume und Abstürze
    stehen mit Grund im Index; jede DXF läuft nur einmal (SHA-256 des Inhalts).

Die Stempel→Raum-Zuordnung ist die ECHTE der Erkennung
(``KaskadeErgebnis.zuordnungen`` — nach Flutung und Bereinigung), abgegriffen
über einen Wrapper um ``provider.raeume_aus_kaskade``, der das Ergebnis nur
durchreicht. Punkt-in-Polygon (wie in ``gesamtdarstellung``) wird hier NICHT
benutzt — es zeigte Stempel an Räumen, denen die Erkennung sie nie zugeordnet hat.

Zwei Stufen je Plan: Stufe 1 = Erkennung + graue Plan-Kulisse →
``_cache.pkl``/``_hintergrund_<n>.png``; Stufe 2 = Overlays + Legende →
``uebersicht.png`` (+ ``uebersicht_<n>.png`` je weiterem Ausschnitt).
``--nur-zeichnen`` wiederholt Stufe 2 aus dem Cache.

Aufruf:
    python scripts/analyse/raumerkennung_darstellung.py                # alle Ordner
    python scripts/analyse/raumerkennung_darstellung.py --neu          # alles neu rechnen
    python scripts/analyse/raumerkennung_darstellung.py --dxf <pfad>   # ein Plan → _einzel/
    python scripts/analyse/raumerkennung_darstellung.py --nur-zeichnen # Bilder aus Cache
    python scripts/analyse/raumerkennung_darstellung.py --nur-index    # nur HTML
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import multiprocessing as mp
import pickle
import re
import subprocess
import sys
import time
import traceback
import zipfile
from collections import Counter
from datetime import datetime
from html import escape
from pathlib import Path
from urllib.parse import quote

REPO = Path(__file__).resolve().parents[2]
for _p in (REPO / "src", REPO / "scripts", REPO / "scripts" / "analyse"):
    sys.path.insert(0, str(_p))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import uebersicht_karte as uk
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.transforms import Bbox
from PIL import Image
from shapely import wkb
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

import plan_pruefen as pp

EINGANG = REPO / "Projekte_Leere Architektpläne (Input)"
AUSGABE = REPO / "Projekte" / "_ergebnis_raumerkennung"
MIN_BREITE_PX = 2500          # Owner-Vorgabe: mindestens 2500 px breit
#: Obergrenze der adaptiven Bildbreite. ponytail: dichte Pläne (Herrenholzgasse
#: EG, 483 Räume) bekommen so trotzdem nicht jedes Label — die übrigen zählt □.
MAX_BREITE_PX = 8000
#: Platzbedarf eines Raumlabels im Endbild. Die Bildbreite wird so gewählt, dass
#: ein Raum mit der Median-Seitenlänge des Plans etwa so breit ist.
LABEL_PX = 130
LEGENDE_PX = 640
TITEL_PX = 60
DPI = 144                     # 1 pt = 2 px im Endbild
WORKER = 4
#: Summe der DXF-Größen, die gleichzeitig laufen dürfen. Gemessen im ersten
#: Vollauf: 4 Worker mit 76–100-MB-Plänen → 13× MemoryError bei 32 GB RAM.
BYTE_BUDGET = 130e6
TIMEOUT_MIN = 60.0
ABWEICHUNG_PROZENT = 10.0
#: ArchiCAD-Zonen setzen den Einfügepunkt AUF die Raumkante (stempel_anker.py).
#: Bis zu diesem Abstand gilt ein Stempel als "am Raum" — außer er liegt im
#: Inneren eines anderen Raums, dann ist es immer eine Linie.
STEMPEL_TOLERANZ_MM = 300.0
MAX_AUSSCHNITTE = 4

# ── Farbtabelle: die Owner-Vorgabe ──────────────────────────────────────────
# key → (Legendentext, Füllung, Kontur, Schraffur)
_KAT: dict[str, tuple[str, str, str, str | None]] = {
    "wohnen":    ("Zimmer / Wohnräume", "#4caf50", "#1b5e20", None),
    "kueche":    ("Küche", "#8e24aa", "#4a0072", None),
    "nass":      ("Bad / WC / Nassraum", "#e53935", "#8e0000", None),
    "abstell":   ("Abstellraum / Vorraum", "#dedede", "#6f6f6f", None),
    "gang":      ("Gang allgemein", "#ffeb3b", "#9a7400", None),
    "gang_whg":  ("Gang innerhalb einer Wohnung", "#ffeb3b", "#9a7400", "///"),
    "stiege":    ("Stiegenhaus / Schleuse", "#fb8c00", "#994400", None),
    "lift":      ("Lift", "#ffffff", "#d50000", None),
    "schacht":   ("Schacht (mit Kreuz)", "#ffffff", "#d50000", None),
    # Die Erkennung kennt drei weitere communale Nebenräume; sie stehen hier
    # ausdrücklich im Text, statt still unter "Keller/Technik/Lager/Garage".
    "neben":     ("Keller / Technik / Lager / Garage\n(auch Müllraum, Waschküche, Kinderwagenraum)",
                  "#9e9e9e", "#424242", None),
    "frei":      ("Balkon / Loggia / Terrasse", "#a5d6a7", "#2e7d4f", None),
    "sonstig":   ("sonstiger Typ (nicht in der Farbtabelle)", "#d7ccc8", "#5d4037", None),
    "unbekannt": ("UNBEKANNT — nicht typisiert", "#ff00ff", "#8b0060", None),
}
#: raum_typ → Kategorie. Ein Typ, der hier fehlt, wird "sonstig" — NICHT
#: "unbekannt" (unbekannt = gar kein Typ) und NICHT stillschweigend grau.
_TYP_KAT = {
    "ZIMMER": "wohnen", "WOHNZIMMER": "wohnen", "SCHLAFZIMMER": "wohnen",
    "KINDERZIMMER": "wohnen", "WOHNEN": "wohnen",
    "KÜCHE": "kueche", "KUECHE": "kueche", "WOHNKÜCHE": "kueche", "WOHNKUECHE": "kueche",
    "BAD": "nass", "WC": "nass", "DUSCHE": "nass", "BAD_WC": "nass", "NASSRAUM": "nass",
    "ABSTELLRAUM": "abstell", "VORRAUM": "abstell",
    "GANG": "gang", "FLUR": "gang", "KORRIDOR": "gang", "AUFZUGSVORPLATZ": "gang",
    "STIEGENHAUS": "stiege", "TREPPENHAUS": "stiege", "SCHLEUSE": "stiege",
    "LIFT": "lift", "AUFZUG": "lift",
    "SCHACHT": "schacht",
    "KELLER": "neben", "KELLERABTEIL": "neben", "TECHNIK": "neben", "LAGER": "neben",
    "GARAGE": "neben", "MUELLRAUM": "neben", "MÜLLRAUM": "neben",
    "WASCHKÜCHE": "neben", "WASCHKUECHE": "neben", "KINDERWAGENRAUM": "neben",
    "BALKON": "frei", "LOGGIA": "frei", "TERRASSE": "frei",
}
_AUSSEN_FC, _AUSSEN_EC = "#42a5f5", "#0d47a1"
_WOHNUNG_FARBE = "#3b1fa8"
_STEMPEL_LINIE = "#b71c1c"
_ROT = "#d50000"
#: Farben, die die 256-Farben-Palette EXAKT behalten muss. Gemessen: eine reine
#: Median-Cut-Palette zog Magenta #ff00ff auf #fb63ff und Rot #d50000 auf #d3141c.
_SIGNAL = ("#000000", "#ffffff", _ROT, "#ff00ff", "#8b0060", _STEMPEL_LINIE,
           _WOHNUNG_FARBE, "#9a7400")

#: Nicht-Grundrisse am Dateinamen: Schnitte, Ansichten, Lagepläne,
#: Dachdraufsichten (DD), Legenden, Symbolbibliotheken, Vorlagen.
_KEIN_GRUNDRISS_RX = re.compile(
    r"schnitt|(?<![a-z])schn(?![a-z])|ansicht|lageplan|draufsicht"
    r"|(?<![a-z0-9])dd(?![a-z0-9])|legende|symbol|vorlage|fassade|detail|stromkreis",
    re.IGNORECASE)


class _NichtErkannt(Exception):
    """Kein Gebäudeumriss mit Räumen — kein Absturz, sondern ein Befund."""

    def __init__(self, grund: str, plan=None):
        super().__init__(grund)
        self.plan = plan


# ── Kleinkram ───────────────────────────────────────────────────────────────

def _sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def _rel(p: Path) -> str:
    try:
        return p.resolve().relative_to(REPO).as_posix()
    except ValueError:
        return p.as_posix()


def _commit() -> str:
    """Kurz-SHA von HEAD; ``-dirty``, wenn ``src/`` oder ``scripts/`` ungesichert
    geändert sind — dann ist der SHA nicht der Code, der gerechnet hat."""
    def git(*a):
        return subprocess.run(["git", *a], capture_output=True, text=True, check=False,
                              cwd=REPO).stdout.strip()
    sha = git("rev-parse", "--short", "HEAD") or "?"
    return f"{sha}-dirty" if git("status", "--porcelain", "--", "src", "scripts") else sha


def _kategorie(typ: str | None, nutzungsklasse: str | None) -> str:
    t = (typ or "").upper()
    if not t:
        return "unbekannt"
    k = _TYP_KAT.get(t)
    if k is None:
        return "sonstig"
    if k == "gang" and nutzungsklasse == "WOHNUNG_PRIVAT":
        return "gang_whg"
    return k


def _kein_grundriss_grund(name: str) -> str | None:
    m = _KEIN_GRUNDRISS_RX.search(name)
    return f"Dateiname enthält „{m.group(0)}“" if m else None


def _schreibe(ziel: Path, daten: dict) -> None:
    ziel.mkdir(parents=True, exist_ok=True)
    (ziel / "kennzahlen.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")


def _lies(ziel: Path) -> dict | None:
    kz = ziel / "kennzahlen.json"
    return json.loads(kz.read_text(encoding="utf-8")) if kz.exists() else None


def _polygon(pts) -> Polygon | None:
    if len(pts) < 3:
        return None
    g = Polygon(pts).buffer(0)
    return None if g.is_empty else g


# ── Eingang: ZIPs entpacken, Pläne sammeln ──────────────────────────────────

def _entpacken(eingang: Path) -> int:
    """ZIP → Unterordner gleichen Namens (nur *.dxf; cp437-Namen → UTF-8).
    Vorhandene Dateien gleicher Größe bleiben liegen."""
    n = 0
    for z in sorted(eingang.glob("*.zip")):
        ziel = eingang / z.stem
        ziel.mkdir(exist_ok=True)
        with zipfile.ZipFile(z) as zf:
            for i in zf.infolist():
                if i.is_dir():
                    continue
                name = i.filename
                if not i.flag_bits & 0x800:
                    try:
                        name = name.encode("cp437").decode("utf-8")
                    except UnicodeError:
                        pass
                if not name.lower().endswith(".dxf"):
                    continue
                out = ziel / Path(name).name
                if out.exists() and out.stat().st_size == i.file_size:
                    continue
                with zf.open(i) as src, open(out, "wb") as dst:
                    while chunk := src.read(1 << 20):
                        dst.write(chunk)
                n += 1
    return n


def _plaene(eingang: Path) -> list[tuple[str, Path]]:
    """(Projekt, DXF) je Unterordner — Ordner für Ordner, darin alphabetisch."""
    return [(d.name, dxf)
            for d in sorted(p for p in eingang.iterdir() if p.is_dir())
            for dxf in sorted(d.rglob("*.dxf"))]


def _ausgabename(dxf: Path, belegt: dict[str, Path]) -> str:
    """Ordnername je Plan; bei Namenskollision hängt der Elternordner an, bei
    erneuter Kollision eine Nummer (Lehre aus gesamtdarstellung: Baulegende.dxf
    lag zweimal, ein Plan verschwand lautlos)."""
    name, n = dxf.stem, 1
    while belegt.get(name, dxf) != dxf:
        n += 1
        name = f"{dxf.stem} ({dxf.parent.name})" + (f" {n - 1}" if n > 2 else "")
    belegt[name] = dxf
    return name


# ── Stufe 1: Erkennung + Kulisse ────────────────────────────────────────────

def _ausschnitte(polys: list[Polygon], f: float, rand: float = 0.06,
                 abstand_mm: float = 5000.0) -> tuple[list[tuple[tuple, list]], int]:
    """Bild-Ausschnitte (Plan-Koordinaten) samt der Räume darin.

    Ein Modelspace kann mehrere Grundrisse weit auseinander tragen (Rennweg EG:
    zweite Zeichnung 740 m entfernt, Barawitzka: Planvarianten nebeneinander) —
    ein Gesamtausschnitt zeigte nur Briefmarken, ein Cluster-Zoom ließ die
    Hälfte der Räume stumm verschwinden. Räume werden über 5 m gruppiert; wäre
    der Gesamtausschnitt höchstens 2,5× so groß wie der der größten Gruppe
    (zwei Trakte, Innenhof), bleibt es EIN Bild — sonst ein Bild je Gruppe,
    größte zuerst, höchstens ``MAX_AUSSCHNITTE``. Der Rest wird gezählt."""
    def _bounds(geoms):
        bs = [g.bounds for g in geoms]
        x0, y0 = min(b[0] for b in bs), min(b[1] for b in bs)
        x1, y1 = max(b[2] for b in bs), max(b[3] for b in bs)
        m = rand * max(x1 - x0, y1 - y0, 1.0)
        return ((x0 - m) / f, (x1 + m) / f, (y0 - m) / f, (y1 + m) / f)

    huelle = unary_union([g.buffer(abstand_mm) for g in polys])
    teile = list(getattr(huelle, "geoms", [huelle]))
    gruppen = [[g for g in polys if t.contains(g.representative_point())] for t in teile]
    gruppen = sorted((gr for gr in gruppen if gr), key=lambda gr: -sum(g.area for g in gr))
    if len(gruppen) <= 1:
        return [(_bounds(polys), polys)], 0
    gx0, gx1, gy0, gy1 = _bounds(polys)
    bx0, bx1, by0, by1 = _bounds(gruppen[0])
    if max((gx1 - gx0) / max(bx1 - bx0, 1e-9), (gy1 - gy0) / max(by1 - by0, 1e-9)) <= 2.5:
        return [(_bounds(polys), polys)], 0
    return ([(_bounds(gr), gr) for gr in gruppen[:MAX_AUSSCHNITTE]],
            sum(len(gr) for gr in gruppen[MAX_AUSSCHNITTE:]))


def _breite_px(bounds: tuple, geoms: list[Polygon], f: float, rot: int) -> int:
    """Bildbreite so, dass ein Raum mit Median-Seitenlänge ~LABEL_PX breit ist —
    in den Grenzen MIN_BREITE_PX..MAX_BREITE_PX."""
    seite_m = float(np.median([math.sqrt(g.area) for g in geoms])) / 1000.0
    x0, x1, y0, y1 = bounds
    quer_m = ((y1 - y0) if rot else (x1 - x0)) * f / 1000.0
    return int(min(MAX_BREITE_PX, max(MIN_BREITE_PX, quer_m * LABEL_PX / max(seite_m, 1.0))))


def _hintergrund(plan, ziele: list[tuple[tuple, int]], rot: int, ziel: Path) -> list[dict]:
    """Plan EINMAL als graue Kulisse aufbauen (der teure ezdxf-Durchlauf), dann
    je Ausschnitt Grenzen setzen und speichern. Der Extent wird NACH dem
    Speichern gelesen — mit ``adjustable='datalim'`` passt matplotlib die
    Grenzen beim Zeichnen an den Maßstab an, und genau diese Grenzen deckt das
    PNG ab."""
    fig, ax = pp._figur(plan, None)
    uk._hintergrund_ausgrauen(ax)
    ax.set_aspect("equal", adjustable="datalim")
    out = []
    for i, ((x0, x1, y0, y1), breite) in enumerate(ziele, start=1):
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)
        w, h = max(x1 - x0, 1e-9), max(y1 - y0, 1e-9)
        lang = 12.0
        fig.set_size_inches(lang if w >= h else lang * w / h,
                            lang if h > w else lang * h / w)
        breite_in = fig.get_size_inches()[1 if rot else 0]
        # 1000 dpi × 12 in = 12 000 px längste Seite — Speicherdeckel.
        dpi = min(1000, math.ceil(breite * 1.02 / breite_in))
        png = ziel / f"_hintergrund_{i}.png"
        fig.savefig(str(png), dpi=dpi, facecolor="white")
        ex0, ex1 = ax.get_xlim()
        ey0, ey1 = ax.get_ylim()
        with Image.open(png) as im:
            w_px, h_px = im.size
        out.append({"extent": (float(ex0), float(ex1), float(ey0), float(ey1)),
                    "png": png.name, "px": (w_px, h_px), "breite_soll": breite})
    plt.close(fig)
    return out


def _roh_bild(plan, ziel: Path) -> bool:
    """Für nicht erkannte Pläne: der nackte Plan, damit man sieht, was da war."""
    if plan is None:
        return False
    try:
        fig, _ax = pp._figur(plan, None)
        fig.savefig(str(ziel / "plan_roh.png"), dpi=140, facecolor="white")
        plt.close(fig)
        return True
    except Exception:  # noqa: BLE001 — nur ein Hilfsbild, darf nichts kippen
        plt.close("all")
        return False


def _erkennen(dxf: Path, ziel: Path) -> dict:
    """Erkennung laufen lassen, echte Stempel-Zuordnung und Plan abgreifen,
    Kulisse rendern, alles als Cache ablegen."""
    import notbeleuchtung.raumerkennung.provider as pm
    from notbeleuchtung.raumerkennung.stempel_anker import finde_stempel, ordne_zu

    gefangen: dict = {}
    orig_lade, orig_kask = pm.lade_dxf, pm.raeume_aus_kaskade

    def lade(pfad):
        gefangen["plan"] = orig_lade(pfad)
        return gefangen["plan"]

    def kask(plan, *a, **kw):
        gefangen["k"] = orig_kask(plan, *a, **kw)
        return gefangen["k"]

    t0 = time.time()
    pm.lade_dxf, pm.raeume_aus_kaskade = lade, kask
    try:
        provider = pm.ArchitekturRaumProvider()
        try:
            modell = provider.parse(str(dxf), "")
        except ValueError as e:
            if "Wand-Entities" in str(e):
                raise _NichtErkannt(f"keine Wand-Entities — das Wand-Layer-Muster greift nicht ({e})",
                                    gefangen.get("plan")) from e
            raise
    finally:
        pm.lade_dxf, pm.raeume_aus_kaskade = orig_lade, orig_kask
    plan = gefangen["plan"]
    k = gefangen.get("k")

    raeume = [{"id": r.id, "typ": r.raum_typ or "",
               "polygon_mm": [(float(x), float(y)) for x, y in r.polygon_mm],
               "flaeche_m2": float(r.flaeche_m2), "nutzungsklasse": r.nutzungsklasse,
               "wohnung_id": r.wohnung_id}
              for r in modell.raeume]
    polys = [g for r in raeume if (g := _polygon(r["polygon_mm"])) is not None]
    if not polys:
        raise _NichtErkannt(f"{len(raeume)} Räume, keiner mit Polygon — kein geschlossener "
                            "Gebäudeumriss mit Räumen", plan)

    ids = {r.id for r in modell.raeume}
    if k is not None:
        zuord = list(k.zuordnungen)
        zuordnung_quelle = f"Erkennung (KaskadeErgebnis.zuordnungen, {len(zuord)} Stempel)"
    else:   # Kaskade lief nicht (kein Wand-Layer, aber Wandkörper)
        zuord = ordne_zu(finde_stempel(plan), modell.raeume)
        zuordnung_quelle = "nachgerechnet (ordne_zu auf Endmodell — Kaskade lief nicht)"
    stempel = []
    for z in zuord:
        s = z.stempel
        rid = z.raum.id if z.raum is not None else None
        stempel.append({"name": str(s.name or "").strip(), "typ": s.typ,
                        "flaeche_m2": s.flaeche_m2,
                        "xy": (float(s.position_mm[0]), float(s.position_mm[1])),
                        "raum_id": rid if rid in ids else None,
                        "raum_fehlt": rid is not None and rid not in ids,
                        "flag": z.flag, "abweichung_prozent": z.abweichung_prozent})

    ab = getattr(provider, "letzte_aussenbereiche", None)
    befund = getattr(provider, "geschoss_befund", None)
    f = plan.factor
    rot, vermerk = pp._rotation(plan)
    aus, nicht_gezeigt = _ausschnitte(polys, f)
    bilder = _hintergrund(plan, [(b, _breite_px(b, g, f, rot)) for b, g in aus], rot, ziel)

    cache = {
        "raeume": raeume,
        "stempel": stempel,
        "zuordnung_quelle": zuordnung_quelle,
        "aussen_offen": [g.wkb for g in (ab.offen if ab is not None else [])],
        "aussen_geschlossen": [g.wkb for g in (ab.geschlossen if ab is not None else [])],
        "kein_umriss": ab is None or not ab.komponenten,
        "geschoss": modell.floor,
        "geschoss_quelle": getattr(befund, "quelle", None),
        "rotation": rot, "rotation_vermerk": vermerk,
        "factor": f, "ausschnitte": bilder, "raeume_nicht_gezeigt": nicht_gezeigt,
        "erkennung_s": round(time.time() - t0, 1),
    }
    (ziel / "_cache.pkl").write_bytes(pickle.dumps(cache))
    return cache


# ── Auswertung (gemeinsam für Bild und Kennzahlen) ──────────────────────────

def _auswertung(cache: dict) -> tuple[dict, dict, dict]:
    """(Polygon je Raum-ID, Stempel je Raum-ID, Flächenabweichung % je Raum-ID).
    Setzt an jedem Stempel ``ohne_raum`` und ``ausserhalb``."""
    polys = {r["id"]: g for r in cache["raeume"] if (g := _polygon(r["polygon_mm"])) is not None}
    je_raum: dict[str, list[dict]] = {}
    for s in cache["stempel"]:
        pt = Point(s["xy"])
        g = polys.get(s["raum_id"]) if s["raum_id"] else None
        s["ohne_raum"] = g is None
        if g is None:
            s["ausserhalb"] = False
            continue
        in_anderem = not g.covers(pt) and any(
            p.contains(pt) for rid, p in polys.items() if rid != s["raum_id"])
        s["ausserhalb"] = bool(g.distance(pt) > STEMPEL_TOLERANZ_MM or in_anderem)
        je_raum.setdefault(s["raum_id"], []).append(s)
    abw: dict[str, float] = {}
    for rid, st in je_raum.items():
        mit_m2 = next((s for s in st if s["flaeche_m2"]), None)
        r = next(r for r in cache["raeume"] if r["id"] == rid)
        if mit_m2 is not None:
            abw[rid] = abs(r["flaeche_m2"] - mit_m2["flaeche_m2"]) / mit_m2["flaeche_m2"] * 100.0
    return polys, je_raum, abw


def _kennzahlen(cache: dict, bilder: list[dict]) -> dict:
    """Owner-Kennzahlen auf oberster Ebene — genau die verlangten. Alles andere
    steht unter ``kontext`` und erklärt nur das Bild."""
    polys, je_raum, abw = _auswertung(cache)
    raeume, st = cache["raeume"], cache["stempel"]
    typen = Counter((r["typ"] or "UNBEKANNT") for r in raeume)
    whg = Counter(r["wohnung_id"] for r in raeume if r["wohnung_id"])
    return {
        "raeume_gesamt": len(raeume),
        "raeume_je_typ": dict(typen.most_common()),
        "raeume_unbekannt": typen.get("UNBEKANNT", 0),
        "raeume_mit_stempel": len(je_raum),
        "stempel_abweichung_gt10": sum(1 for v in abw.values() if v > ABWEICHUNG_PROZENT),
        "wohnungen": len(whg),
        "raeume_je_wohnung": dict(sorted(whg.items())),
        "kontext": {
            "raeume_ohne_polygon": len(raeume) - len(polys),
            "raeume_ohne_label": sum(b["ohne_label"] for b in bilder),
            "raeume_nicht_gezeigt": cache["raeume_nicht_gezeigt"],
            "stempel_gesamt": len(st),
            "stempel_ohne_raum": sum(1 for s in st if s["ohne_raum"]),
            "stempel_nicht_im_zugeordneten_raum": sum(1 for s in st if s["ausserhalb"]),
            "stempel_raum_nicht_im_endmodell": sum(1 for s in st if s["raum_fehlt"]),
            "stempel_flags": dict(Counter(s["flag"] for s in st)),
            "raeume_mit_mehreren_stempeln": sum(1 for v in je_raum.values() if len(v) > 1),
            "zuordnung_quelle": cache["zuordnung_quelle"],
            "geschoss": cache["geschoss"], "geschoss_quelle": cache["geschoss_quelle"],
            "kein_gebaeudeumriss": cache["kein_umriss"],
            "aussen_offen": len(cache["aussen_offen"]),
            "aussen_geschlossen": len(cache["aussen_geschlossen"]),
            "rotation": cache["rotation_vermerk"],
        },
        "bilder": bilder,
    }


# ── Stufe 2: Zeichnen ───────────────────────────────────────────────────────

def _platziere(ax, renderer, x, y, zeilen, fs, belegt: list) -> bool:
    """Mehrzeiliges Label mittig im Raum, jede Zeile mit eigener Farbe (rote
    m²-Zahl). Überlappt es ein gesetztes Label (echte Pixel-Box), ein zweiter
    Versuch mit 75 % Schrift; passt auch der nicht, kein Label (→ □)."""
    for groesse in (fs, max(5.0, fs * 0.75)):
        n = len(zeilen)
        texte = [ax.annotate(text, (x, y), xytext=(0, ((n - 1) / 2 - i) * groesse * 1.3),
                             textcoords="offset points", ha="center", va="center",
                             fontsize=groesse, color=farbe, zorder=8,
                             fontweight="bold" if fett else "normal",
                             bbox={"fc": "white", "alpha": 0.78, "ec": "none", "pad": 1.0})
                 for i, (text, farbe, fett) in enumerate(zeilen)]
        box = Bbox.union([t.get_window_extent(renderer) for t in texte])
        if not any(box.overlaps(b) for b in belegt):
            belegt.append(box)
            return True
        for t in texte:
            t.remove()
    return False


def _umbruch(text: str, breite: int) -> str:
    worte, zeilen, akt = text.split(), [], ""
    for w in worte:
        if len(akt) + len(w) + 1 > breite and akt:
            zeilen.append(akt)
            akt = w
        else:
            akt = f"{akt} {w}".strip()
    zeilen.append(akt)
    return "\n".join(zeilen)


def _legende(ax, zaehl: Counter, hinweise: list[str]) -> None:
    hand: list = []
    for key, (text, fc, ec, hatch) in _KAT.items():
        voll = key in ("lift", "schacht")
        hand.append(Patch(facecolor=fc, edgecolor=ec, hatch=hatch, lw=1.6,
                          alpha=1.0 if voll else 0.6, label=f"{text} ({zaehl.get(key, 0)})"))
    hand.append(Patch(facecolor=_AUSSEN_FC, edgecolor=_AUSSEN_EC, hatch="//", alpha=0.4,
                      label=f"Außenbereich  // offen ({zaehl.get('aussen_offen', 0)})"
                            f"  xx Innenhof ({zaehl.get('aussen_geschlossen', 0)})"))
    hand.append(Line2D([], [], color=_WOHNUNG_FARBE, lw=3.4,
                       label=f"Wohnung — dicker Umriss + ID ({zaehl.get('wohnungen', 0)})"))
    hand.append(Line2D([], [], color="none", label=""))
    hand.append(Line2D([], [], color="none",
                       label="Beschriftung je Raum:  Typ · Fläche berechnet ·\n"
                             "(Stempeltext  Stempel-m²)"))
    k = zaehl.get("abw_ohne_label", 0)
    hand.append(Line2D([], [], color=_ROT, marker="s", ls="none", ms=9,
                       label=f"rote Zahl = Fläche weicht > {ABWEICHUNG_PROZENT:.0f} % vom Stempel"
                             f" ab ({zaehl.get('abweichung_gt10', 0)}"
                             + (f", davon {k} ohne Label" if k else "") + ")"))
    hand.append(Line2D([], [], color=_STEMPEL_LINIE, lw=2.2, marker="o", mfc="none", mew=2,
                       label="Stempel liegt nicht im zugeordneten Raum\n"
                             f"(> {STEMPEL_TOLERANZ_MM / 1000:.1f} m daneben oder in anderem Raum):\n"
                             f"○ Stempel → ● Raum ({zaehl.get('stempel_ausserhalb', 0)})"))
    hand.append(Line2D([], [], color="#ff00ff", marker="x", ls="none", mew=2.2, ms=9,
                       label="Stempel ohne zugeordneten Raum"
                             f" ({zaehl.get('stempel_ohne_raum', 0)})"))
    hand.append(Line2D([], [], color="#444444", marker="s", mfc="none", ls="none", mew=1.6,
                       ms=7, label="Raum ohne Platz für Beschriftung"
                                   f" ({zaehl.get('ohne_label', 0)})"))
    hand.append(Line2D([], [], color="none", label=""))
    for h in hinweise:
        hand.append(Line2D([], [], color="none", label=_umbruch(h, 56)))
    ax.legend(handles=hand, loc="upper left", bbox_to_anchor=(0.03, 0.99),
              fontsize=8.5, framealpha=1.0, borderpad=0.8, labelspacing=0.55,
              handlelength=1.8, handletextpad=0.6,
              title="Legende — nur Raumerkennung (Anzahl in diesem Bild)",
              title_fontproperties={"weight": "bold", "size": 10})


def _speichere(fig, ziel: Path) -> tuple[int, int]:
    """256-Farben-PNG (Datei ~4× kleiner), Signalfarben exakt in der Palette."""
    tmp = ziel.with_name("_voll.png")
    fig.savefig(str(tmp), dpi=DPI, facecolor="white")
    with Image.open(tmp) as im:
        rgb = im.convert("RGB")
    frei = 256 - len(_SIGNAL)
    pal = rgb.quantize(colors=frei, dither=Image.Dither.NONE).getpalette()[: frei * 3]
    pal += [0] * (frei * 3 - len(pal))
    for c in _SIGNAL:
        pal += [int(c[i:i + 2], 16) for i in (1, 3, 5)]
    palbild = Image.new("P", (1, 1))
    palbild.putpalette(pal)
    rgb.quantize(palette=palbild, dither=Image.Dither.NONE).save(ziel, optimize=True)
    tmp.unlink()
    return rgb.size


def _zeichne_ausschnitt(cache: dict, ziel: Path, i: int, titel: str,
                        polys: dict, je_raum: dict, abw: dict) -> dict:
    aus = cache["ausschnitte"][i - 1]
    n_aus = len(cache["ausschnitte"])
    datei = "uebersicht.png" if i == 1 else f"uebersicht_{i}.png"
    with Image.open(ziel / aus["png"]) as im:
        img = np.asarray(im.convert("RGB"))      # uint8 — float32 kostete 4× Speicher
    x0, x1, y0, y1 = aus["extent"]
    f = cache["factor"]
    rot = cache["rotation"]
    assert rot in (0, 1), rot
    if rot:                       # np.rot90 = 90° gegen den Uhrzeigersinn
        img = np.rot90(img, 1)
        def R(x, y):
            return (-y, x)
        ex = (-y1, -y0, x0, x1)
    else:
        def R(x, y):
            return (x, y)
        ex = (x0, x1, y0, y1)

    def P(pts):                   # mm → gedrehte Plan-Koordinaten
        return [R(x / f, y / f) for x, y in pts]

    def sichtbar(x, y):
        return ex[0] <= x <= ex[1] and ex[2] <= y <= ex[3]

    h_px, w_px = img.shape[:2]
    plan_px = max(w_px, MIN_BREITE_PX)
    hoehe_px = h_px * plan_px / w_px
    ges_w, ges_h = plan_px + LEGENDE_PX, hoehe_px + TITEL_PX
    fig = plt.figure(figsize=(ges_w / DPI, ges_h / DPI), dpi=DPI)
    fig.patch.set_facecolor("white")
    links, unten = LEGENDE_PX / ges_w, TITEL_PX / ges_h
    ax = fig.add_axes([links, unten, 1 - links, 1 - unten])
    ax.set_axis_off()
    ax.imshow(img, extent=list(ex), interpolation="none", aspect="auto", zorder=0)
    ax.set_xlim(ex[0], ex[1])
    ax.set_ylim(ex[2], ex[3])
    span_m = (ex[1] - ex[0]) * f / 1000.0
    fs = max(6.5, min(10.0, plan_px / max(span_m, 1.0) / 9.0))
    renderer = fig.canvas.get_renderer()
    belegt: list = []
    zaehl: Counter = Counter()

    # ── Außenbereiche: blau schraffiert (offen //, Innenhof xx) ────────────
    for key, geoms, hatch in (("aussen_offen", cache["aussen_offen"], "//"),
                              ("aussen_geschlossen", cache["aussen_geschlossen"], "xx")):
        for w in geoms:
            g = wkb.loads(w)
            rp = g.representative_point()
            zaehl[key] += sichtbar(*R(rp.x / f, rp.y / f))
            for gg in getattr(g, "geoms", [g]):
                xs, ys = zip(*P(gg.exterior.coords))
                ax.fill(xs, ys, facecolor=_AUSSEN_FC, alpha=0.18, edgecolor=_AUSSEN_EC,
                        lw=1.4, zorder=1)
                ax.fill(xs, ys, facecolor="none", edgecolor=_AUSSEN_EC, lw=0.6,
                        hatch=hatch, alpha=0.55, zorder=1)

    # ── Räume: Flächen (groß zuerst, klein oben), Labels gesammelt ─────────
    jobs = []
    for r in sorted(cache["raeume"], key=lambda r: -r["flaeche_m2"]):
        g = polys.get(r["id"])
        if g is None:
            continue
        k = _kategorie(r["typ"], r["nutzungsklasse"])
        _t, fc, ec, hatch = _KAT[k]
        voll = k in ("lift", "schacht")
        for gg in getattr(g, "geoms", [g]):
            xs, ys = zip(*P(gg.exterior.coords))
            ax.fill(xs, ys, facecolor=fc, edgecolor=ec, alpha=0.95 if voll else 0.5,
                    lw=2.2 if voll else 1.4, zorder=2)
            if hatch:
                ax.fill(xs, ys, facecolor="none", edgecolor=ec, lw=0.8, hatch=hatch, zorder=3)
            mrr = gg.minimum_rotated_rectangle
            if k == "schacht" and mrr.geom_type == "Polygon":
                # Kreuz über die Diagonalen des gedrehten Rechtecks, auf den
                # Schacht beschnitten — über die Achsen-Bounds lief es bei
                # schrägen Schächten aus dem Polygon.
                e = list(mrr.exterior.coords)
                for a, b in ((e[0], e[2]), (e[1], e[3])):
                    teil = LineString([a, b]).intersection(gg)
                    for s in getattr(teil, "geoms", [teil]):
                        if s.geom_type == "LineString" and not s.is_empty:
                            xs, ys = zip(*P(s.coords))
                            ax.plot(xs, ys, color=ec, lw=1.8, zorder=4)
        rp = g.representative_point()
        cx, cy = R(rp.x / f, rp.y / f)
        if not sichtbar(cx, cy):
            continue
        zaehl[k] += 1
        unbek = not r["typ"]
        rot_zahl = abw.get(r["id"], 0.0) > ABWEICHUNG_PROZENT
        zaehl["abweichung_gt10"] += rot_zahl
        zeilen = [("? UNBEKANNT" if unbek else r["typ"],
                   _KAT["unbekannt"][2] if unbek else "black", unbek),
                  (f"{r['flaeche_m2']:.1f} m²", _ROT if rot_zahl else "black", rot_zahl)]
        stmp = je_raum.get(r["id"], [])
        if stmp:
            zeilen.append(("(" + " | ".join(
                (s["name"] or "—") + (f" {s['flaeche_m2']:.1f} m²" if s["flaeche_m2"] else "")
                for s in stmp) + ")", "#333333", False))
        jobs.append((0 if unbek or rot_zahl else 1, cx, cy, zeilen, rot_zahl, ec))

    # ── Wohnungen: dicker Umriss + ID über der Oberkante ───────────────────
    je_w: dict[str, list] = {}
    for r in cache["raeume"]:
        if r["wohnung_id"] and r["id"] in polys:
            je_w.setdefault(r["wohnung_id"], []).append(polys[r["id"]])
    for wid, ps in sorted(je_w.items()):
        u = unary_union(ps).buffer(200).buffer(-200)
        if u.is_empty:
            u = unary_union(ps)
        oben = None
        for gg in getattr(u, "geoms", [u]):
            pts = P(gg.exterior.coords)
            xs, ys = zip(*pts)
            ax.plot(xs, ys, color=_WOHNUNG_FARBE, lw=3.4, zorder=6)
            kand = max(pts, key=lambda p: p[1])
            oben = kand if oben is None or kand[1] > oben[1] else oben
        t = ax.annotate(wid, oben, xytext=(0, fs * 1.3), textcoords="offset points",
                        ha="center", va="center", fontsize=fs + 3, fontweight="bold",
                        color="white", zorder=9,
                        bbox={"fc": _WOHNUNG_FARBE, "alpha": 0.9, "ec": "none", "pad": 2.5})
        if sichtbar(*oben):
            zaehl["wohnungen"] += 1
            belegt.append(t.get_window_extent(renderer))

    # ── Raumlabels: Auffälliges (UNBEKANNT, rote Zahl) zuerst ──────────────
    for _prio, cx, cy, zeilen, rot_zahl, ec in sorted(jobs, key=lambda j: j[0]):
        if not _platziere(ax, renderer, cx, cy, zeilen, fs, belegt):
            zaehl["ohne_label"] += 1
            zaehl["abw_ohne_label"] += rot_zahl
            ax.plot(cx, cy, "s", ms=7, mfc="none", mec=ec, mew=1.6, zorder=8)

    # ── Stempel: nicht im zugeordneten Raum → Linie; ohne Raum → x ─────────
    for s in cache["stempel"]:
        sx, sy = R(s["xy"][0] / f, s["xy"][1] / f)
        m2 = f" {s['flaeche_m2']:.1f} m²" if s["flaeche_m2"] else ""
        if s["ohne_raum"]:
            if not sichtbar(sx, sy):
                continue
            zaehl["stempel_ohne_raum"] += 1
            ax.plot(sx, sy, "x", ms=9, mew=2.2, color="#ff00ff", zorder=10)
            ax.annotate(f"{s['name']}{m2} (kein Raum)", (sx, sy), xytext=(5, -4),
                        textcoords="offset points", fontsize=max(fs - 1, 6),
                        color=_KAT["unbekannt"][2], ha="left", va="top", style="italic",
                        zorder=10)
        elif s["ausserhalb"]:
            rp = polys[s["raum_id"]].representative_point()
            tx, ty = R(rp.x / f, rp.y / f)
            if not (sichtbar(sx, sy) or sichtbar(tx, ty)):
                continue
            zaehl["stempel_ausserhalb"] += 1
            ax.plot([sx, tx], [sy, ty], color=_STEMPEL_LINIE, lw=2.0, zorder=10)
            ax.plot(sx, sy, "o", ms=8, mfc="none", mec=_STEMPEL_LINIE, mew=2.2, zorder=11)
            ax.plot(tx, ty, "o", ms=5, color=_STEMPEL_LINIE, zorder=11)
            ax.annotate(f"{s['name']}{m2}", (sx, sy), xytext=(5, -4), textcoords="offset points",
                        fontsize=max(fs - 1, 6), color=_STEMPEL_LINIE, ha="left", va="top",
                        fontweight="bold", zorder=11)

    im_bild = sum(zaehl.get(key, 0) for key in _KAT)
    hinweise = []
    if n_aus > 1:
        hinweise.append(f"Ausschnitt {i} von {n_aus}: {im_bild} von {len(polys)} Räumen in "
                        "diesem Bild — die Räume liegen im Modelspace weit auseinander.")
    if cache["raeume_nicht_gezeigt"]:
        hinweise.append(f"{cache['raeume_nicht_gezeigt']} Räume in KEINEM Bild "
                        f"(mehr als {MAX_AUSSCHNITTE} Raumgruppen).")
    hinweise.append(cache["rotation_vermerk"])
    axl = fig.add_axes([0, 0, links, 1])
    axl.set_axis_off()
    _legende(axl, zaehl, hinweise)
    fig.text(links + (1 - links) / 2, unten * 0.45,
             titel + (f" · Ausschnitt {i}/{n_aus}" if n_aus > 1 else ""),
             ha="center", va="center", fontsize=11, fontweight="bold")
    w, h = _speichere(fig, ziel / datei)
    plt.close(fig)
    return {"datei": datei, "px": [w, h], "raeume": im_bild, "ohne_label": zaehl["ohne_label"]}


def _zeichnen(cache: dict, ziel: Path, titel: str) -> list[dict]:
    polys, je_raum, abw = _auswertung(cache)
    return [_zeichne_ausschnitt(cache, ziel, i, titel, polys, je_raum, abw)
            for i in range(1, len(cache["ausschnitte"]) + 1)]


def _titel(projekt: str, name: str, cache: dict, commit: str) -> str:
    return (f"{projekt} / {name} — Raumerkennung, nur Räume · Geschoss "
            f"{cache['geschoss'] or 'UNBEKANNT'} ({cache['geschoss_quelle']}) · Commit {commit}")


# ── Worker (eigener Prozess je Plan) ────────────────────────────────────────

def _worker(dxf_s: str, ziel_s: str, projekt: str, name: str, commit: str, sha: str) -> None:
    dxf, ziel = Path(dxf_s), Path(ziel_s)
    ziel.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    basis = {"plan": name, "projekt": projekt, "dxf": _rel(dxf), "sha256": sha,
             "bytes": dxf.stat().st_size, "commit": commit}
    phase = "Erkennung"
    try:
        cache = _erkennen(dxf, ziel)
        phase = "Zeichnen"
        t1 = time.time()
        bilder = _zeichnen(cache, ziel, _titel(projekt, name, cache, commit))
        d = {**basis, "status": "ok", **_kennzahlen(cache, bilder),
             "laufzeit_s": {"erkennung": cache["erkennung_s"],
                            "zeichnen": round(time.time() - t1, 1),
                            "gesamt": round(time.time() - t0, 1)}}
    except _NichtErkannt as e:
        d = {**basis, "status": "nicht_erkannt", "grund": str(e),
             "roh_bild": _roh_bild(e.plan, ziel), "laufzeit_s": round(time.time() - t0, 1)}
    except Exception:  # noqa: BLE001 — Fehlergrund in den Index, nicht abstürzen
        d = {**basis, "status": "fehler",
             "grund": f"Abbruch in Phase {phase}:\n{traceback.format_exc()}",
             "laufzeit_s": round(time.time() - t0, 1)}
    plt.close("all")
    _schreibe(ziel, d)


_GESTARTET = "Prozess gestartet, aber kein Ergebnis geschrieben"


def _fehler_eintrag(a: dict, grund: str, t0: float) -> dict:
    return {"plan": a["name"], "projekt": a["projekt"], "dxf": _rel(a["dxf"]),
            "sha256": a["sha"], "bytes": a["bytes"], "commit": a["commit"],
            "status": "fehler", "grund": grund, "laufzeit_s": round(time.time() - t0, 1)}


def _lauf(auftraege: list[dict], out: Path, worker: int, timeout_min: float) -> None:
    """Große Pläne zuerst, höchstens ``worker`` parallel UND höchstens
    ``BYTE_BUDGET`` DXF-Bytes gleichzeitig (ein einzelner Plan darf immer
    starten). Vor dem Start steht ein Platzhalter-Fehlereintrag im Zielordner —
    stirbt der Prozess hart, bleibt der sichtbar statt eines alten Ergebnisses."""
    warte = sorted(auftraege, key=lambda a: -a["bytes"])
    offen_je_projekt = Counter(a["projekt"] for a in warte)
    n, fertig = len(warte), 0
    aktiv: list[tuple[mp.Process, dict, float]] = []

    def passt(a):
        return len(aktiv) < worker and (
            not aktiv or sum(x[1]["bytes"] for x in aktiv) + a["bytes"] <= BYTE_BUDGET)

    while warte or aktiv:
        while (j := next((k for k, a in enumerate(warte) if passt(a)), None)) is not None:
            a = warte.pop(j)
            t0 = time.time()
            _schreibe(a["ziel"], _fehler_eintrag(a, _GESTARTET, t0))
            p = mp.Process(target=_worker, args=(str(a["dxf"]), str(a["ziel"]), a["projekt"],
                                                 a["name"], a["commit"], a["sha"]))
            p.start()
            aktiv.append((p, a, t0))
            print(f"  start   {a['projekt']} / {a['name']} ({a['bytes'] / 1e6:.0f} MB)", flush=True)
        time.sleep(2)
        for eintrag in list(aktiv):
            p, a, t0 = eintrag
            if p.is_alive():
                if time.time() - t0 <= timeout_min * 60:
                    continue
                p.terminate()
                p.join(15)
                _schreibe(a["ziel"], _fehler_eintrag(
                    a, f"Timeout nach {timeout_min:.0f} min — Prozess abgebrochen", t0))
            aktiv.remove(eintrag)
            fertig += 1
            d = _lies(a["ziel"]) or {}
            if d.get("grund") == _GESTARTET:
                d = _fehler_eintrag(a, f"{_GESTARTET} — Exitcode {p.exitcode} "
                                       "(harter Absturz, z. B. Speicher)", t0)
                _schreibe(a["ziel"], d)
            lz = d.get("laufzeit_s")
            lz = lz.get("gesamt") if isinstance(lz, dict) else lz
            print(f"  [{fertig}/{n}] {a['projekt']} / {a['name']}: {d.get('status')}"
                  f" — {d.get('raeume_gesamt', '')} Räume, {lz} s", flush=True)
            offen_je_projekt[a["projekt"]] -= 1
            if offen_je_projekt[a["projekt"]] == 0:
                print(f"  Index: {_index_projekt(out, a['projekt'])}", flush=True)


# ── Index ───────────────────────────────────────────────────────────────────

_CSS = """
:root{color-scheme:light dark;--bg:#f7f7f8;--fg:#1a1a1a;--kart:#fff;
--rand:#d8d8dc;--muted:#666;--warn:#b00020;--ok:#1b7f3b}
@media (prefers-color-scheme:dark){:root{--bg:#16161a;--fg:#e8e8ea;
--kart:#1f1f24;--rand:#33333a;--muted:#a0a0a8}}
*{box-sizing:border-box}
body{margin:0;padding:16px;background:var(--bg);color:var(--fg);
font:14px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
h1{font-size:22px;margin:0 0 4px}
h2.abschnitt{font-size:17px;margin-top:28px}
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
.tab{overflow-x:auto}
table{border-collapse:collapse;margin:12px 0;font-size:13px}
td,th{border:1px solid var(--rand);padding:4px 9px;text-align:left;
vertical-align:top}
th{background:rgba(127,127,127,.12);font-weight:600}
.num{text-align:right;font-variant-numeric:tabular-nums}
.fehler{background:rgba(176,0,32,.1);border-left:4px solid var(--warn);
padding:10px 12px;border-radius:4px}
.fehler pre{white-space:pre-wrap;font-size:11px;margin:6px 0 0;max-height:16em;
overflow:auto}
.skip{background:rgba(127,127,127,.12);border-left:4px solid var(--muted);
padding:10px 12px;border-radius:4px}
.warn{color:var(--warn);font-weight:600}
.hinweis{color:var(--muted);font-size:12px;margin-top:6px}
"""

_STATUS_TEXT = {"ok": "ausgewertet", "kein_grundriss": "kein Grundriss (Dateiname, übersprungen)",
                "nicht_erkannt": "kein Grundriss erkannt — kein Gebäudeumriss mit Räumen",
                "dublette": "Dublette (übersprungen)", "fehler": "FEHLER"}


def _kopf(titel: str) -> str:
    return ("<!doctype html><html lang='de'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{escape(titel)}</title><style>{_CSS}</style></head><body>")


def _lz(kz: dict) -> float:
    lz = kz.get("laufzeit_s") or 0.0
    return lz["gesamt"] if isinstance(lz, dict) else lz


def _tabelle(d: dict) -> str:
    def z(label, wert, klasse="num"):
        return f"<tr><th>{label}</th><td class='{klasse}'>{wert}</td></tr>"

    def warn(n):
        return f"<span class='warn'>{n}</span>" if n else "0"

    typen = ", ".join(
        (f"<span class='warn'>{escape(k)} {v}</span>" if k == "UNBEKANNT" else f"{escape(k)} {v}")
        for k, v in d["raeume_je_typ"].items())
    je_w = ", ".join(f"{escape(k)} {v}" for k, v in d["raeume_je_wohnung"].items()) or "—"
    lz = d["laufzeit_s"]
    rows = [
        z("Räume gesamt", d["raeume_gesamt"]),
        z("je Typ", typen or "—", ""),
        z("davon UNBEKANNT", warn(d["raeume_unbekannt"])),
        z("Räume mit Stempel", d["raeume_mit_stempel"]),
        z("davon Flächenabweichung &gt; 10 %", warn(d["stempel_abweichung_gt10"])),
        z("Wohnungen", d["wohnungen"]),
        z("Räume je Wohnung", je_w, ""),
        z("Laufzeit", f"{lz['gesamt']} s (Erkennung {lz['erkennung']} s, Bild {lz['zeichnen']} s)"),
    ]
    # Unter der Tabelle nur, was das Bild erklärt — keine weiteren Kennzahlen.
    k, hinweise = d.get("kontext", {}), []
    bilder = d.get("bilder", [])
    if len(bilder) > 1:
        hinweise.append(f"<span class='warn'>{len(bilder)} Ausschnitte</span> — Räume liegen im "
                        "Modelspace weit auseinander")
    if k.get("raeume_nicht_gezeigt"):
        hinweise.append(f"<span class='warn'>{k['raeume_nicht_gezeigt']} Räume in keinem Bild</span>")
    if k.get("raeume_ohne_label"):
        hinweise.append(f"<span class='warn'>{k['raeume_ohne_label']} Räume ohne Platz für die "
                        "Beschriftung</span> (im Bild □)")
    if k.get("raeume_ohne_polygon"):
        hinweise.append(f"<span class='warn'>{k['raeume_ohne_polygon']} Räume ohne Polygon</span> "
                        "(nicht gezeichnet)")
    if not k.get("zuordnung_quelle", "Erkennung").startswith("Erkennung"):
        hinweise.append(f"<span class='warn'>Stempel-Zuordnung {escape(k['zuordnung_quelle'])}</span>")
    tab = "<div class='tab'><table>" + "".join(rows) + "</table></div>"
    return tab + (f"<div class='hinweis'>{' · '.join(hinweise)}</div>" if hinweise else "")


def _eintraege(ordner: Path) -> list[tuple[Path, dict]]:
    if not ordner.is_dir():
        return []
    return [(d, kz) for d in sorted(ordner.iterdir())
            if d.is_dir() and (kz := _lies(d)) is not None]


def _index_projekt(out: Path, projekt: str) -> Path:
    ordner = out / projekt
    plaene = _eintraege(ordner)
    stat = Counter(kz["status"] for _, kz in plaene)
    aktuell = _commit()
    teile = [_kopf(f"Raumerkennung — {projekt}"),
             f"<h1>{escape(projekt)} — Raumerkennung, nur Räume</h1>",
             (f"<div class='sub'><a href='../index.html'>← Gesamtübersicht</a> · "
              f"{len(plaene)} Pläne · " + " · ".join(
                  f"{_STATUS_TEXT[s]} {n}" for s, n in stat.items()) + "</div>"),
             "<div class='nav'>"]
    for d, kz in plaene:
        mark = {"ok": "", "fehler": " ⚠", "nicht_erkannt": " ∅"}.get(kz["status"], " –")
        teile.append(f"<a href='#{quote(d.name)}'>{escape(d.name)}{mark}</a>")
    teile.append("</div>")
    for d, kz in plaene:
        s = kz["status"]
        c = kz.get("commit", "?")
        c_html = (f"<code>{escape(c)}</code>" if c == aktuell
                  else f"<span class='warn'>Commit {escape(c)} ≠ aktuell {escape(aktuell)}</span>")
        teile.append(f"<div class='plan' id='{quote(d.name)}'><h2>{escape(d.name)}</h2>"
                     f"<div class='pfad'>{escape(kz.get('dxf', ''))} · SHA-256 "
                     f"<code>{kz.get('sha256', '')[:12]}</code> · gerechnet auf {c_html}</div>")
        if s == "ok":
            for i, b in enumerate(kz.get("bilder", []), start=1):
                href = f"{quote(d.name)}/{b['datei']}"
                if len(kz["bilder"]) > 1:
                    teile.append(f"<div class='hinweis'>Ausschnitt {i} von {len(kz['bilder'])} — "
                                 f"{b['raeume']} Räume</div>")
                teile.append(f"<a href='{href}'><img src='{href}' alt='{escape(d.name)}' "
                             "loading='lazy'></a>")
            teile.append(_tabelle(kz))
        elif s == "fehler":
            teile.append(f"<div class='fehler'><b>{_STATUS_TEXT[s]}</b> nach {_lz(kz)} s"
                         f"<pre>{escape(kz['grund'])}</pre></div>")
        else:
            teile.append(f"<div class='skip'><b>{_STATUS_TEXT[s]}</b> — {escape(kz['grund'])}</div>")
            if kz.get("roh_bild"):
                href = f"{quote(d.name)}/plan_roh.png"
                teile.append(f"<details><summary>Plan roh (ohne Erkennung)</summary><a href='{href}'>"
                             f"<img src='{href}' alt='roh' loading='lazy'></a></details>")
        teile.append("</div>")
    teile.append("</body></html>")
    ziel = ordner / "index.html"
    ziel.write_text("".join(teile), encoding="utf-8")
    return ziel


_SPALTEN = ("plaene", "ok", "kein_grundriss", "nicht_erkannt", "dublette", "fehler",
            "raeume", "unbekannt", "mit_stempel", "abw", "wohnungen", "laufzeit")
_WARN_SPALTEN = ("fehler", "nicht_erkannt", "unbekannt", "abw")


def _index_gesamt(out: Path) -> Path:
    projekte = sorted(p for p in out.iterdir() if p.is_dir() and not p.name.startswith("_"))
    aktuell = _commit()
    zeilen, summe, fremd = [], Counter(), 0
    for pr in projekte:
        plaene = _eintraege(pr)
        ok = [kz for _, kz in plaene if kz["status"] == "ok"]
        z = Counter(Counter(kz["status"] for _, kz in plaene))
        z["plaene"] = len(plaene)
        z["raeume"] = sum(k["raeume_gesamt"] for k in ok)
        z["unbekannt"] = sum(k["raeume_unbekannt"] for k in ok)
        z["mit_stempel"] = sum(k["raeume_mit_stempel"] for k in ok)
        z["abw"] = sum(k["stempel_abweichung_gt10"] for k in ok)
        z["wohnungen"] = sum(k["wohnungen"] for k in ok)
        z["laufzeit"] = round(sum(_lz(kz) for _, kz in plaene))
        fremd += sum(1 for _, kz in plaene if kz.get("commit") != aktuell)
        summe.update(z)
        zeilen.append((pr.name, z))

    def zeile(name, z, link=True):
        n = (f"<a href='{quote(name)}/index.html'>{escape(name)}</a>" if link
             else f"<b>{escape(name)}</b>")
        zellen = "".join(
            "<td class='num'>" + (f"<span class='warn'>{z[k]}</span>"
                                   if z[k] and k in _WARN_SPALTEN else f"{z[k]}") + "</td>"
            for k in _SPALTEN)
        return f"<tr><td>{n}</td>{zellen}</tr>"

    stand = f"Stand <code>{escape(aktuell)}</code>"
    if fremd:
        stand += f" · <span class='warn'>{fremd} Pläne auf anderem Commit gerechnet</span>"
    teile = [_kopf("Raumerkennung — Gesamtübersicht"),
             "<h1>Raumerkennung, nur Räume — Gesamtübersicht</h1>",
             (f"<div class='sub'>{stand} · {datetime.now().astimezone():%Y-%m-%d %H:%M} · "
              f"Eingang <code>{escape(_rel(EINGANG))}</code> · "
              f"{summe['plaene']} Pläne in {len(projekte)} Ordnern · "
              "Bericht: <a href='BERICHT.md'>BERICHT.md</a><br>"
              "Ehrlichkeit vor Schönheit: untypisiert magenta, Stempel außerhalb des "
              "zugeordneten Raums als Linie, Flächenabweichung &gt; 10 % rot, Räume ohne "
              "Platz für ein Label □.</div>"),
             ("<div class='tab'><table><tr><th>Ordner</th><th>Pläne</th><th>ausgewertet</th>"
              "<th>kein Grundriss (Name)</th><th>kein Grundriss erkannt</th><th>Dubletten</th>"
              "<th>Fehler</th><th>Räume</th><th>UNBEKANNT</th><th>mit Stempel</th>"
              "<th>Abw. &gt; 10 %</th><th>Wohnungen</th><th>Laufzeit s</th></tr>")]
    teile += [zeile(n, z) for n, z in zeilen]
    teile.append(zeile("gesamt", summe, link=False))
    teile.append("</table></div>")
    besonderes = [(pr.name, d.name, kz) for pr in projekte for d, kz in _eintraege(pr)
                  if kz["status"] != "ok"]
    if besonderes:
        teile.append("<h2 class='abschnitt'>Übersprungen / kein Grundriss erkannt / Fehler</h2>"
                     "<div class='tab'><table><tr><th>Ordner</th><th>Plan</th><th>Status</th>"
                     "<th>Grund</th></tr>")
        for pn, name, kz in besonderes:
            grund = kz["grund"].strip().splitlines()[-1] if kz["status"] == "fehler" else kz["grund"]
            teile.append(f"<tr><td>{escape(pn)}</td><td><a href='{quote(pn)}/index.html#"
                         f"{quote(name)}'>{escape(name)}</a></td><td>{_STATUS_TEXT[kz['status']]}"
                         f"</td><td>{escape(grund)}</td></tr>")
        teile.append("</table></div>")
    einzel = _eintraege(out / "_einzel")
    if einzel:
        teile.append("<h2 class='abschnitt'>Einzelläufe außerhalb des Eingangs</h2>"
                     "<div class='tab'><table><tr><th>Plan</th><th>DXF</th><th>Status</th></tr>")
        for d, kz in einzel:
            teile.append(f"<tr><td><a href='_einzel/index.html#{quote(d.name)}'>{escape(d.name)}"
                         f"</a></td><td>{escape(kz.get('dxf', ''))}</td>"
                         f"<td>{_STATUS_TEXT[kz['status']]}</td></tr>")
        teile.append("</table></div>")
    teile.append("</body></html>")
    ziel = out / "index.html"
    ziel.write_text("".join(teile), encoding="utf-8")
    return ziel


# ── main ────────────────────────────────────────────────────────────────────

def _nachzeichnen(out: Path, worker: int) -> None:
    """Stufe 2 für alle Pläne mit Cache neu — ohne neue Erkennung."""
    jobs = [str(d) for d in out.rglob("_cache.pkl")]
    print(f"{len(jobs)} Pläne aus Cache neu zeichnen", flush=True)
    with mp.Pool(worker) as pool:
        for text in pool.imap_unordered(_nachzeichnen_einer, jobs):
            print(f"  {text}", flush=True)


def _nachzeichnen_einer(cache_s: str) -> str:
    ziel = Path(cache_s).parent
    d = _lies(ziel) or {}
    commit = _commit()
    try:
        cache = pickle.loads(Path(cache_s).read_bytes())
        t1 = time.time()
        bilder = _zeichnen(cache, ziel, _titel(d.get("projekt", "?"), d.get("plan", ziel.name),
                                               cache, commit))
        erkennung = (d.get("laufzeit_s") or {}).get("erkennung", cache["erkennung_s"]) \
            if isinstance(d.get("laufzeit_s"), dict) else cache["erkennung_s"]
        zeichnen = round(time.time() - t1, 1)
        d.pop("grund", None)
        d.update({"status": "ok", **_kennzahlen(cache, bilder), "commit": commit,
                  "laufzeit_s": {"erkennung": erkennung, "zeichnen": zeichnen,
                                 "gesamt": round(erkennung + zeichnen, 1)}})
        ergebnis = "ok"
    except Exception:  # noqa: BLE001 — ein defekter Cache darf die anderen nicht kippen
        d.update({"status": "fehler", "commit": commit,
                  "grund": f"Abbruch beim Nachzeichnen:\n{traceback.format_exc()}"})
        ergebnis = "FEHLER"
    plt.close("all")
    _schreibe(ziel, d)
    return f"{ergebnis}: {d.get('projekt')} / {d.get('plan')}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--eingang", default=str(EINGANG))
    ap.add_argument("--out", default=str(AUSGABE))
    ap.add_argument("--dxf", help="nur diesen einen Plan (Ausgabe unter <out>/_einzel/)")
    ap.add_argument("--ordner", action="append",
                    help="nur diesen Unterordner des Eingangs (mehrfach möglich), z. B. Rennweg")
    ap.add_argument("--nur-index", action="store_true")
    ap.add_argument("--nur-zeichnen", action="store_true")
    ap.add_argument("--neu", action="store_true", help="auch fertige Pläne neu rechnen")
    ap.add_argument("--worker", type=int, default=WORKER)
    ap.add_argument("--timeout-min", type=float, default=TIMEOUT_MIN)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    commit = _commit()

    def alle_indizes():
        for pr in sorted(p for p in out.iterdir() if p.is_dir() and not p.name.startswith("_")):
            _index_projekt(out, pr.name)
        if (out / "_einzel").is_dir():
            _index_projekt(out, "_einzel")
        return _index_gesamt(out)

    if a.nur_zeichnen:
        _nachzeichnen(out, a.worker)
    if a.nur_index or a.nur_zeichnen:
        print(f"Index: {alle_indizes()}")
        return 0

    if a.dxf:
        dxf = Path(a.dxf)
        ziel = out / "_einzel" / dxf.stem
        _worker(str(dxf), str(ziel), "_einzel", dxf.stem, commit, _sha256(dxf))
        d = _lies(ziel) or {}
        print(json.dumps({k: v for k, v in d.items() if k != "grund"}, ensure_ascii=False, indent=1))
        if d.get("grund"):
            print(d["grund"])
        print(f"Index: {alle_indizes()}")
        return 0

    eingang = Path(a.eingang)
    print(f"Eingang: {eingang} · Commit {commit}", flush=True)
    print(f"entpackt: {_entpacken(eingang)} DXF", flush=True)
    alle = [(p, d) for p, d in _plaene(eingang) if not a.ordner or p in a.ordner]
    if not alle:
        print(f"Kein DXF im Eingang für Ordner {a.ordner}", file=sys.stderr)
        return 2
    print(f"{len(alle)} DXF in {len({p for p, _ in alle})} Ordnern", flush=True)

    gesehen: dict[str, tuple[str, Path]] = {}
    belegt: dict[str, dict[str, Path]] = {}
    auftraege: list[dict] = []
    stat: Counter = Counter()
    for projekt, dxf in alle:
        name = _ausgabename(dxf, belegt.setdefault(projekt, {}))
        ziel = out / projekt / name
        sha = _sha256(dxf)
        basis = {"plan": name, "projekt": projekt, "dxf": _rel(dxf), "sha256": sha,
                 "bytes": dxf.stat().st_size, "commit": commit, "laufzeit_s": 0.0}
        if sha in gesehen:
            p0, d0 = gesehen[sha]
            _schreibe(ziel, {**basis, "status": "dublette",
                             "grund": f"inhaltsgleich mit {p0} / {d0.name} ({_rel(d0)})"})
            stat["dublette"] += 1
            continue
        gesehen[sha] = (projekt, dxf)
        if (g := _kein_grundriss_grund(dxf.stem)) is not None:
            _schreibe(ziel, {**basis, "status": "kein_grundriss", "grund": g})
            stat["kein_grundriss"] += 1
            continue
        alt = _lies(ziel)
        if (not a.neu and alt is not None and alt.get("sha256") == sha
                and alt.get("status") in ("ok", "nicht_erkannt")):
            stat["uebernommen"] += 1
            continue
        auftraege.append({**basis, "dxf": dxf, "sha": sha, "ziel": ziel, "name": name})
        stat["rechnen"] += 1
    print(f"{stat['rechnen']} rechnen · {stat['uebernommen']} schon fertig · "
          f"{stat['dublette']} Dubletten · {stat['kein_grundriss']} kein Grundriss "
          f"(Dateiname) · {a.worker} Worker · Budget {BYTE_BUDGET / 1e6:.0f} MB · "
          f"Timeout {a.timeout_min:.0f} min", flush=True)

    t0 = time.time()
    _lauf(auftraege, out, a.worker, a.timeout_min)
    print(f"\nLaufzeit {(time.time() - t0) / 60:.1f} min\nIndex: {alle_indizes()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
