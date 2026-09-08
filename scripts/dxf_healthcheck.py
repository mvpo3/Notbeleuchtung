"""dxf_healthcheck — Eingabe-DXF auf Koordinaten-Korruption prüfen.

Schritt 0 der Skill `plan-verify`: fängt korrupte Quell-DXF ab, BEVOR ein teurer
Parse/Render (Minuten, ggf. Out-of-Memory) verbrannt wird.

Diagnostizierter Fall (Baufeld-4OG, 2026-09-08): ein Basispunkt-/Koordinaten-Versatz
schiebt einen Teil der Geometrie auf y ≈ 1e11…1e14 mm. Die dadurch riesige Extents-
Spanne lässt raster-basierte Engine-Schritte (`raumerkennung.stempel_flutung`,
`platzierung.lux`) GB/TB-große Arrays allozieren → OOM oder >50-min-Hänger. Ein 250-mm-
Raster über 347.535 km sind ~1,9 Mrd. Punkte.

Rein `ezdxf` (keine `notbeleuchtung`-Importe) → schnell, unabhängig vom Engine-Stand,
auch auf Rohplänen nutzbar. Betrachtet die häufigen Entity-Typen (deckt den groben
Versatz zuverlässig ab); exotische Typen (HATCH/DIMENSION) werden für die
Gesundheits-Entscheidung nicht gebraucht.

CLI:  python scripts/dxf_healthcheck.py "<plan1.dxf>" ["<plan2.dxf>" …]
Exit-Code 0 = alle gesund, 1 = mindestens ein Plan auffällig (für Skript-Gates).
"""
from __future__ import annotations

import contextlib
import math
import sys
from collections import Counter
from dataclasses import dataclass, field

import ezdxf

#: Ab dieser |Koordinate| (mm) gilt eine Entity als Ausreißer (~1000 km — jenseits
#: jedes realen Gebäudes, aber unter typischen Geodäsie-Nordwerten irrelevant, da
#: Pläne in lokalen mm liegen).
AUSREISSER_MM = 1_000_000_000.0
#: Extents-Spanne (m), ab der ein Render riskant wird (echte Geschosse ~50–300 m).
SPAN_WARN_M = 2_000.0
#: NO-GO-Handlungshinweis (ASCII, damit auch cp1252-Konsolen ihn drucken).
_HINWEIS_NOGO = (
    "  -> Quelle in AutoCAD bereinigen (MOVE/PURGE) oder Extents in der "
    "Erkennung ausreisser-robust machen (raumerkennung-Lane)."
)


def _repr_point(e):
    """Ein repräsentativer (x, y) der Entity oder None (unbekannter Typ)."""
    dt = e.dxftype()
    try:
        v = None
        if dt == "LINE":
            v = e.dxf.start
        elif dt in ("CIRCLE", "ARC"):
            v = e.dxf.center
        elif dt in ("TEXT", "MTEXT", "INSERT"):
            v = e.dxf.insert
        elif dt == "POINT":
            v = e.dxf.location
        elif dt == "LWPOLYLINE":
            pts = e.get_points()
            return (float(pts[0][0]), float(pts[0][1])) if pts else None
        elif dt == "POLYLINE":
            vs = list(e.vertices)
            v = vs[0].dxf.location if vs else None
        if v is None:
            return None
        return (float(v[0]), float(v[1]))
    except Exception:  # noqa: BLE001 — defekte Entity zählt als „nicht verortbar"
        return None


@dataclass
class Befund:
    pfad: str
    entities: int = 0
    verortet: int = 0                       # Entities mit auswertbarem Punkt
    ausreisser: int = 0                     # davon jenseits AUSREISSER_MM
    span_x_m: float = 0.0
    span_y_m: float = 0.0
    cluster: dict = field(default_factory=dict)   # Größenordnungs-Bucket → Anzahl
    top_layer_fern: list = field(default_factory=list)  # Layer der Ausreißer
    fehler: str | None = None

    @property
    def ausreisser_pct(self) -> float:
        return 100.0 * self.ausreisser / self.verortet if self.verortet else 0.0

    @property
    def gesund(self) -> bool:
        if self.fehler is not None:
            return False
        return (
            self.ausreisser == 0
            and self.span_x_m <= SPAN_WARN_M
            and self.span_y_m <= SPAN_WARN_M
        )


def _bucket(v: float) -> str:
    if abs(v) < 1000.0:
        return "~0 (<1 m)"
    p = int(math.log10(abs(v)))
    return f"{'+' if v >= 0 else '-'}1e{p} mm (~{10 ** p / 1e6:.3g} km)"


def pruefe(pfad: str) -> Befund:
    """DXF laden und Koordinaten-Gesundheit bestimmen."""
    b = Befund(pfad=pfad)
    try:
        doc = ezdxf.readfile(pfad)
    except Exception as ex:  # noqa: BLE001 — unlesbar = auffällig, nicht crashen
        b.fehler = f"{type(ex).__name__}: {str(ex)[:80]}"
        return b
    xs: list[float] = []
    ys: list[float] = []
    cluster: Counter = Counter()
    fern_layer: Counter = Counter()
    for e in doc.modelspace():
        b.entities += 1
        p = _repr_point(e)
        if p is None:
            continue
        x, y = float(p[0]), float(p[1])
        b.verortet += 1
        xs.append(x)
        ys.append(y)
        cluster[_bucket(y)] += 1
        if abs(x) > AUSREISSER_MM or abs(y) > AUSREISSER_MM:
            b.ausreisser += 1
            fern_layer[e.dxf.layer] += 1
    if xs:
        b.span_x_m = (max(xs) - min(xs)) / 1000.0
        b.span_y_m = (max(ys) - min(ys)) / 1000.0
    b.cluster = dict(cluster.most_common())
    b.top_layer_fern = fern_layer.most_common(8)
    return b


def report(b: Befund) -> str:
    if b.fehler:
        return f"{b.pfad}\n  NICHT LESBAR: {b.fehler}  → NO-GO"
    zeilen = [
        b.pfad,
        (f"  entities={b.entities} verortet={b.verortet} "
         f"ausreisser={b.ausreisser} ({b.ausreisser_pct:.1f}%)"),
        f"  spanne x={b.span_x_m:.1f} m  y={b.span_y_m:.1f} m",
    ]
    if len(b.cluster) > 1:
        zeilen.append("  y-cluster: " + " · ".join(f"{k}={v}" for k, v in b.cluster.items()))
    if b.top_layer_fern:
        zeilen.append("  ausreisser-layer: " + ", ".join(f"{lay}({n})" for lay, n in b.top_layer_fern))
    if b.gesund:
        zeilen.append("  VERDIKT: GO (Koordinaten plausibel)")
    else:
        grund = []
        if b.ausreisser:
            grund.append(f"{b.ausreisser} Ausreißer >1000 km (Basispunkt-Versatz)")
        if b.span_x_m > SPAN_WARN_M or b.span_y_m > SPAN_WARN_M:
            grund.append(f"Extents-Spanne > {SPAN_WARN_M:.0f} m (Raster-OOM-Risiko)")
        zeilen.append("  VERDIKT: NO-GO - " + "; ".join(grund))
        zeilen.append(_HINWEIS_NOGO)
    return "\n".join(zeilen)


def main(argv: list[str]) -> int:
    # Umlaute/Sonderzeichen auch auf cp1252-Konsolen sicher ausgeben.
    with contextlib.suppress(Exception):
        sys.stdout.reconfigure(encoding="utf-8")
    if not argv:
        print("usage: python scripts/dxf_healthcheck.py <plan.dxf> [<plan.dxf> …]")
        return 2
    alle_gesund = True
    for pfad in argv:
        b = pruefe(pfad)
        print(report(b), flush=True)
        alle_gesund = alle_gesund and b.gesund
    return 0 if alle_gesund else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
