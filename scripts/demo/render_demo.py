"""render_demo — ansehbarer Grundriss: reiche DEMO-Architektur + roher Notbeleuchtungs-Output.

Die generierte DEMO_{f}.dxf trägt die REICHE Geometrie (aus Q extrahierte Wohnungen +
Stiege, echte Wände); das Engine-Ergebnis DEMO_{f}_notbeleuchtung.dxf trägt die platzierten
Symbole + die grüne Fluchtweg-Linie. Beide liegen im selben Koordinatensystem → hier werden
sie in EIN Bild komponiert (Architektur grau/schwarz, Notbeleuchtung darüber), auf die
Gebäude-Extents zugeschnitten. Ausgabe: P4/demo/out/DEMO_{f}_plan.png.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import ezdxf
import matplotlib.pyplot as plt
from ezdxf import bbox
from ezdxf.addons.drawing import Frontend, RenderContext
from ezdxf.addons.drawing.config import BackgroundPolicy, Configuration
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend

P4 = Path(r"C:\Users\mvpst\Documents\KI-Projekt\Notbeleuchtung\Projektbeispiele-demo-Platzierungslogik")
DEMO = P4 / "demo"
OUT = DEMO / "out"
# Weiß-auf-weiß vermeiden: Farbe 7 wird schwarz gerendert.
CFG = Configuration(background_policy=BackgroundPolicy.WHITE)


def _draw(ax, dxf_path):
    doc = ezdxf.readfile(str(dxf_path))
    msp = doc.modelspace()
    Frontend(RenderContext(doc), MatplotlibBackend(ax), config=CFG).draw_layout(msp, finalize=False)
    return msp


def render(floor):
    fig = plt.figure(figsize=(16, 14))
    ax = fig.add_axes([0.01, 0.01, 0.98, 0.98])
    ax.set_axis_off()
    ax.set_aspect("equal", adjustable="box")   # sonst ignoriert matplotlib die set_xlim (Memory-Falle)
    arch = _draw(ax, DEMO / f"DEMO_{floor}.dxf")            # reiche Architektur (Q-Geometrie)
    _draw(ax, OUT / f"DEMO_{floor}_notbeleuchtung.dxf")     # roher Engine-Output darüber
    # Auf die Architektur-Extents zuschneiden (Blatt/Legende des Engine-DXF ausblenden).
    ext = bbox.extents(arch, fast=True)
    pad = 1500.0
    ax.set_xlim(ext.extmin.x - pad, ext.extmax.x + pad)
    ax.set_ylim(ext.extmin.y - pad, ext.extmax.y + pad)
    out = OUT / f"DEMO_{floor}_plan.png"
    fig.savefig(str(out), dpi=120, facecolor="white")
    plt.close(fig)
    print("geschrieben", out)


def main():
    for f in ("EG", "1OG"):
        render(f)


if __name__ == "__main__":
    main()
