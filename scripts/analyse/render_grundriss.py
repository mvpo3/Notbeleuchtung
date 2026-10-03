"""render_grundriss — hochqualitativer Grundriss-Render eines Output-DXF.

Rendert das Engine-Output-DXF (reale Architektur `ARCH_Unterlage` + platzierte
Notbeleuchtungs-Symbole auf `din_SIBEL_*`) als Vektor-PDF (+ optional PNG), weißer
Hintergrund (Owner-Regel: Pläne IMMER weiß). Zum Sichten des Plan-Outputs; der
norm-geprüfte Prüfbericht läuft über `pipeline.run` / `scripts/plan_pruefen.py`.

Aufruf:  python scripts/analyse/render_grundriss.py <output.dxf> <out.pdf> [<out.png>] [<titel>]
"""
from __future__ import annotations

import sys

import ezdxf
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import Frontend, RenderContext
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend


def render(dxf_path: str, out_pdf: str, out_png: str | None = None,
           titel: str | None = None) -> None:
    doc = ezdxf.readfile(dxf_path)
    fig = plt.figure(figsize=(23.4, 16.5))          # A2 quer
    ax = fig.add_axes([0.0, 0.0 if not titel else 0.03, 1.0, 1.0 if not titel else 0.94])
    ax.set_axis_off()
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    Frontend(RenderContext(doc), MatplotlibBackend(ax)).draw_layout(
        doc.modelspace(), finalize=True)
    if titel:
        fig.suptitle(titel, fontsize=14, y=0.985)
    fig.savefig(out_pdf, facecolor="white")
    if out_png:
        fig.savefig(out_png, dpi=200, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2],
           sys.argv[3] if len(sys.argv) > 3 else None,
           sys.argv[4] if len(sys.argv) > 4 else None)
