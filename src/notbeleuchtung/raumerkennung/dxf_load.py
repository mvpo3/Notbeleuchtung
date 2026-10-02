"""dxf_load — DXF öffnen, Einheiten normalisieren, Layer/Geometrie-Zugriff.

Kapselt ezdxf: liefert einen ``DxfPlan`` (Dokument + der Layout-Raum, der die
Architektur trägt + Skalierungsfaktor auf mm). Der Rest des Packages arbeitet
nur mit mm — die Faktor-Multiplikation passiert genau hier.

Zwei Layouts (auto-erkannt):
- **Direct-Mode**: Wände liegen direkt im Modelspace (Mollgasse).
- **Wrapper-Mode**: Modelspace enthält einen INSERT, dessen Block die Wände
  trägt — dann wird der Block-Raum genommen (best-effort, ohne Transform).
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path

import ezdxf

from notbeleuchtung.hauptengine.contracts.raum_modell import BBox

# Wand-Layer über Projekt-Familien erkennen (Muster statt fixem Prefix):
#   Mollgasse:    02-TWA/02-ZWA/02-WDA-… (floor-agnostisch)
#   Fischamender: A_Waende / A_Wand…
#   ArchiCAD-num: „110/120/130 Wand …" (auch mit Präfix ``PP_2_110 Wand``,
#                 Suffix ``_Stift_Nr__N``)
#   ArchiCAD-New: ``New_015 Innenwände`` (Rennweg; Umlaut ggf. cp-dekodiert
#                 → tolerant ``w.nde``)
#   AIA/US-Stil:  ``A-WALL`` / ``I-WALL`` (+ ``A-WALL-PATT`` etc., Muthgasse);
#                 Lookbehind hält z.B. ``EA-WALL``-Fremdpräfixe draußen.
WALL_PATTERN = re.compile(
    r"02-(?:TWA|ZWA|WDA)|A_Wa?ende|A_Wand|(?<!\d)1[123]0 Wand"
    r"|New_0?\d{2} (?:innen|au\S{0,2}en)?w.nde"
    r"|(?<![A-Z])[AI]-WALL",
    re.IGNORECASE)

# Rückwärts-kompatibel (Mollgasse-Tests/Direktnutzung).
WALL_PREFIXES: tuple[str, ...] = ("02-TWA", "02-ZWA", "02-WDA")

# $INSUNITS-Code → Faktor auf mm. 4=mm, 5=cm, 6=m; Rest → 1.0 (mm-Annahme).
_INSUNITS_TO_MM: dict[int, float] = {4: 1.0, 5: 10.0, 6: 1000.0}

XY = tuple[float, float]


# Plausible Ausdehnung eines Geschosses in mm (~15 m … ~500 m). Die 15-m-Untergrenze
# schließt die falsche Klein-Dekade aus (z.B. 8 m statt 80 m bei Meter-Plänen).
_SPAN_MIN_MM = 15_000.0
_SPAN_MAX_MM = 500_000.0


def _wall_layers(space) -> frozenset[str]:
    """Wand-Layer-Namen im Raum, per WALL_PATTERN erkannt (projekt-familien-agnostisch)."""
    return frozenset(
        e.dxf.layer for e in space if WALL_PATTERN.search(e.dxf.layer)
    )


# Perzentil-Fenster für die Wandspannweite: Plankopf-, Rahmen- und
# Phantom-Geometrie liegt oft hunderte Meter neben dem Grundriss (Rennweg-
# Phantomraum #126, Baufeld-4OG bei y≈3.5e11). Blindes min/max nimmt sie mit
# und verdirbt die Dekaden-Wahl in `_calibrate_factor`.
_SPAN_PERZENTIL = 0.02


def _wand_punkte(space, wall_layers: frozenset[str],
                 tiefe: int = 0) -> tuple[list[float], list[float]]:
    """Stützpunkte der Wand-Layer, AUCH innerhalb von Blöcken.

    Ohne den Block-Abstieg sieht die Kalibrierung bei Plänen, deren Wände nur
    in Blockdefinitionen stecken, gar nichts (Baufeld 1OG/2OG/4OG: 0 Punkte)
    und fällt auf ``$INSUNITS`` zurück — das dort 6 (Meter) meldet, obwohl die
    Zeichnung in mm vorliegt. Ergebnis war Faktor 1000 statt 1.
    """
    xs: list[float] = []
    ys: list[float] = []
    for e in space:
        t = e.dxftype()
        if t == "INSERT" and tiefe < 3:
            try:
                bx, by = _wand_punkte(e.virtual_entities(), wall_layers, tiefe + 1)
            except Exception:  # noqa: BLE001, S112 — kaputte Block-Referenz überspringen
                continue
            xs += bx
            ys += by
            continue
        if e.dxf.layer not in wall_layers:
            continue
        if t == "LINE":
            xs += [e.dxf.start[0], e.dxf.end[0]]
            ys += [e.dxf.start[1], e.dxf.end[1]]
        elif t == "LWPOLYLINE":
            for p in e.get_points("xy"):
                xs.append(p[0]); ys.append(p[1])
        elif t == "POLYLINE":
            for v in e.vertices:
                xs.append(v.dxf.location[0]); ys.append(v.dxf.location[1])
    return xs, ys


def _perzentil(werte: list[float], q: float) -> float:
    s = sorted(werte)
    i = min(len(s) - 1, max(0, round(q * (len(s) - 1))))
    return s[i]


def _raw_wall_span(space, wall_layers: frozenset[str]) -> float:
    """Wand-Ausdehnung (dx/dy) in Quell-Einheiten, ausreißer-robust.

    Statt min/max das 2–98-%-Fenster: eine Handvoll Plankopf-/Phantom-Punkte
    kippt die Dekaden-Wahl sonst um Faktor 10–1000 (Baufeld, s. `_wand_punkte`).
    """
    xs, ys = _wand_punkte(space, wall_layers)
    if not xs:
        return 0.0
    lo, hi = _SPAN_PERZENTIL, 1.0 - _SPAN_PERZENTIL
    return max(_perzentil(xs, hi) - _perzentil(xs, lo),
               _perzentil(ys, hi) - _perzentil(ys, lo))


_DOOR_MM = 900.0         # Tür-Blattbreite ≈ Schwenkbogen-Radius (Kalibrier-Anker)
_DOOR_MIN_MM, _DOOR_MAX_MM = 600.0, 1300.0


def _door_arc_factor(space) -> float | None:
    """mm-Faktor aus Tür-Schwenkbögen: wähle die Zehnerpotenz, die die MEISTEN
    ARC-Radien in den Tür-Blattbreiten-Bereich (600–1300 mm) legt.

    Robuster als die Geschoss-Ausdehnung (die ist zwischen 8 m und 80 m
    mehrdeutig); eine Tür ist immer ~0.9 m breit.
    """
    # Tür-Bögen stecken oft NUR in Tür-Blöcken (Muthgasse: A-DOOR-INSERTs;
    # die Modelspace-ARCs dort sind Kurvenwände mit 600–1300 Quell-Einheiten —
    # als Türen gelesen kalibrierten sie den Faktor eine Dekade zu klein).
    # Block-Bögen sind definitiv Türen → wenn vorhanden, zählen NUR sie.
    door_block_radii: list[float] = []
    for ins in space:
        if ins.dxftype() != "INSERT":
            continue
        kennung = f"{ins.dxf.name or ''} {ins.dxf.layer or ''}".upper()
        if "DOOR" not in kennung and "TUER" not in kennung and "TÜR" not in kennung:
            continue
        try:
            door_block_radii += [
                v.dxf.radius for v in ins.virtual_entities()
                if v.dxftype() == "ARC" and v.dxf.radius > 0
            ]
        except Exception:  # noqa: BLE001, S112 — korrupte Block-Referenzen überspringen
            continue
    radii = door_block_radii or [
        e.dxf.radius for e in space if e.dxftype() == "ARC" and e.dxf.radius > 0
    ]
    if not radii:
        return None
    best, best_count = None, 0
    for factor in (1.0, 10.0, 100.0, 1000.0):
        count = sum(1 for r in radii if _DOOR_MIN_MM <= r * factor <= _DOOR_MAX_MM)
        if count > best_count:
            best, best_count = factor, count
    return best if best_count >= 3 else None


def _calibrate_factor(raw_span: float, space,
                      doc: ezdxf.document.Drawing) -> tuple[float, str]:
    """mm-Faktor aus der Geometrie ableiten, NICHT aus $INSUNITS (das lügt oft:
    leere Pläne in Metern, fertige in mm — beide mit gleichem Code).

    Die Geschoss-Ausdehnung (15–500 m) gibt die Kandidaten-Dekaden vor. Bleibt
    genau eine → nimm sie. Bleiben mehrere → Tür-Schwenkbogen-Radius (~0.9 m)
    als Tiebreak, sonst die kleinste (konservativ).

    Liefert ``(Faktor, Quelle)``. Die Quelle beginnt mit ``$INSUNITS``, wenn
    keine Wand-Spanne messbar war (2g, D-04): dann steht die Türprobe als Beleg
    dabei — sie entscheidet hier nichts (S-MST, Owner-Frage), sie wird nur
    ausgewiesen.
    """
    candidates = [
        f for f in (1.0, 10.0, 100.0, 1000.0, 10000.0)
        if raw_span > 0 and _SPAN_MIN_MM <= raw_span * f <= _SPAN_MAX_MM
    ]
    if len(candidates) == 1:
        return candidates[0], "spanne"
    if candidates:
        by_door = _door_arc_factor(space)
        if by_door in candidates:
            return by_door, "spanne+tuerbogen"
        return candidates[0], "spanne"
    code = int(doc.header.get("$INSUNITS", 0) or 0)
    factor = _INSUNITS_TO_MM.get(code, 1.0)
    by_door = _door_arc_factor(space)
    probe = ("keine" if by_door is None else f"{by_door:g}"
             + ("" if by_door == factor else " — widerspricht"))
    return factor, (f"$INSUNITS={code} (keine Wand-Spanne 15–500 m messbar), "
                    f"Türprobe: {probe}")


# Entscheid 4 (Owner 2026-10-01, R1-01): eine Koordinate, die nicht endlich ist
# oder jenseits von 1e9 mm liegt, ist kein Planinhalt. Die Entity fliegt beim
# Laden raus — sonst rastert `footprint.gebaeude_umriss` die ungefilterten
# Bounds ins Unendliche (OverflowError/ValueError, Review 1 § 15).
_KOORD_MAX_MM = 1e9


def _koordinaten(e) -> list[float]:
    """x/y-Werte (und Radius) einer Entity in Quell-Einheiten; unbekannter Typ → leer."""
    t = e.dxftype()
    if t == "LINE":
        return [e.dxf.start[0], e.dxf.start[1], e.dxf.end[0], e.dxf.end[1]]
    if t == "LWPOLYLINE":
        return [c for p in e.get_points("xy") for c in p]
    if t == "POLYLINE":
        return [c for v in e.vertices for c in (v.dxf.location[0], v.dxf.location[1])]
    if t in ("INSERT", "TEXT", "MTEXT"):
        return [e.dxf.insert[0], e.dxf.insert[1]]
    if t in ("ARC", "CIRCLE"):
        return [e.dxf.center[0], e.dxf.center[1], e.dxf.radius]
    if t == "HATCH":
        return [c for p in e.paths for v in getattr(p, "vertices", ()) for c in (v[0], v[1])]
    return []


def _verwerfe_defekte(space, grenze: float) -> list[str]:
    """Entities mit nicht-endlicher oder |Koordinate| > ``grenze`` (Quell-Einheiten)
    aus ``space`` löschen; je Entity eine Warnung mit Typ, Handle, Layer, Wert."""
    warnungen: list[str] = []
    for e in list(space):
        try:
            schlecht = next((c for c in _koordinaten(e)
                             if not math.isfinite(c) or abs(c) > grenze), None)
        except Exception:  # noqa: BLE001, S112 — unlesbare Entity bleibt, wie bisher
            continue
        if schlecht is None:
            continue
        warnungen.append(f"entity_verworfen: {e.dxftype()} Handle {e.dxf.handle} "
                         f"Layer {e.dxf.layer} — Koordinate {float(schlecht):g}")
        space.delete_entity(e)
    return warnungen


def _has_walls(space, min_count: int = 10) -> bool:
    n = 0
    for e in space:
        if WALL_PATTERN.search(e.dxf.layer):
            n += 1
            if n >= min_count:
                return True
    return False


@dataclass
class DxfPlan:
    """Geöffneter Plan — Zugriff auf Entities in mm."""

    doc: ezdxf.document.Drawing
    space: object          # Modelspace oder Block-Layout, das die Architektur trägt
    factor: float          # Multiplikator Quell-Einheit → mm
    wall_layers: frozenset[str] = frozenset()  # erkannte Wand-Layer
    faktor_quelle: str = ""  # woher `factor` stammt (`_calibrate_factor`)
    warnungen: list[str] = field(default_factory=list)  # Lade-Warnungen (`entity_verworfen`)

    def entities(self, prefixes: tuple[str, ...] | None = None):
        """Alle Entities des Architektur-Raums, optional nach Layer-Prefix gefiltert."""
        for e in self.space:
            if prefixes is None or e.dxf.layer.startswith(prefixes):
                yield e

    def wall_entities(self):
        """Entities auf den erkannten Wand-Layern (familien-agnostisch)."""
        for e in self.space:
            if e.dxf.layer in self.wall_layers:
                yield e

    def _scale(self, p) -> XY:
        return (float(p[0]) * self.factor, float(p[1]) * self.factor)

    def entity_points(self, e) -> list[XY]:
        """Stützpunkte einer Entity in mm (LINE→2, LW/POLYLINE→n, INSERT→Position)."""
        t = e.dxftype()
        if t == "LINE":
            return [self._scale(e.dxf.start), self._scale(e.dxf.end)]
        if t == "LWPOLYLINE":
            return [self._scale(p) for p in e.get_points("xy")]
        if t == "POLYLINE":
            return [self._scale(v.dxf.location) for v in e.vertices]
        if t == "INSERT":
            return [self._scale(e.dxf.insert)]
        return []


class DxfNichtLesbar(ValueError):
    """Datei fehlt, ist kein DXF oder strukturell defekt (ezdxf-Fehler) — der
    einzige gewollte Abbruch im Lade-Pfad (Owner-Auftrag 2026-09-30, 2a): ohne
    gelesenes Dokument gibt es nichts, woran eine Warnung hängen könnte."""


def lade_dxf(pfad: str | Path) -> DxfPlan:
    """Öffne die DXF, wähle den Architektur-Raum, kalibriere den mm-Faktor."""
    try:
        doc = ezdxf.readfile(str(pfad))
    except (OSError, ezdxf.DXFError) as exc:
        raise DxfNichtLesbar(f"DXF nicht lesbar: {pfad} — {exc}") from exc
    msp = doc.modelspace()
    space = msp
    if not _has_walls(msp):
        # Wrapper-Mode: ersten INSERT suchen, dessen Block Wände trägt.
        for ins in (e for e in msp if e.dxftype() == "INSERT"):
            blk = doc.blocks.get(ins.dxf.name)
            if blk is not None and _has_walls(blk):
                space = blk
                break
    # nan/inf vor der Kalibrierung (sonst kippt das Perzentil-Fenster), die
    # 1e9-mm-Grenze danach in Quell-Einheiten (Entscheid 4).
    warnungen = _verwerfe_defekte(space, math.inf)
    wall_layers = _wall_layers(space)
    factor, quelle = _calibrate_factor(_raw_wall_span(space, wall_layers), space, doc)
    warnungen += _verwerfe_defekte(space, _KOORD_MAX_MM / factor)
    return DxfPlan(doc=doc, space=space, factor=factor, wall_layers=wall_layers,
                   faktor_quelle=quelle, warnungen=warnungen)


def bounds_mm(plan: DxfPlan) -> BBox:
    """Bounding-Box (mm) über alle Wand-Entities."""
    xs: list[float] = []
    ys: list[float] = []
    for e in plan.wall_entities():
        for x, y in plan.entity_points(e):
            xs.append(x)
            ys.append(y)
    if not xs:
        raise ValueError("Keine Wand-Entities gefunden — Layer-Muster prüfen.")
    return BBox(min_xy=(min(xs), min(ys)), max_xy=(max(xs), max(ys)))
