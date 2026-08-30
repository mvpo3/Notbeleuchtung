"""pdf_export — Notbeleuchtungs-DXF → PDF (Liefer-Format).

Rastert/vektorisiert das gerenderte DXF über den ezdxf-matplotlib-Backend in ein PDF.
Der Nordstern liefert einen Plan „zum Weitergeben" — DXF ist der CAD-Austausch, PDF das
Sicht-/Druck-Dokument. Reine Ausgabe-Schicht; erzeugt kein neues Fach-Wissen.

matplotlib + ezdxf.addons.drawing sind optionale Abhängigkeiten (Extra `render`); der
Import passiert lazy, damit der Rest der Engine ohne sie läuft.

CAD-Hintergrund: `dunkel=True` (Default) = schwarzer Plan-Hintergrund (Layer-Farbe 7
weiß, Symbole poppen); `dunkel=False` = weißer Druckgrund.
"""
from __future__ import annotations

from pathlib import Path


def dxf_zu_pdf(
    dxf_path: str | Path,
    pdf_path: str | Path,
    *,
    dunkel: bool = True,
    dpi: int = 300,
    breite_zoll: float = 16.5,
    hoehe_zoll: float = 11.7,   # A3 quer
) -> Path:
    """Rendert `dxf_path` in ein PDF (`pdf_path`) und gibt den Pfad zurück."""
    import ezdxf
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from ezdxf.addons.drawing import Frontend, RenderContext
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend

    # Schrift mit voller Glyph-Abdeckung (Umlaute etc.) für die Legenden-Texte.
    matplotlib.rcParams["font.family"] = "DejaVu Sans"

    doc = ezdxf.readfile(str(dxf_path))
    bg = "black" if dunkel else "white"
    fig = plt.figure(figsize=(breite_zoll, hoehe_zoll), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    try:
        Frontend(RenderContext(doc), MatplotlibBackend(ax)).draw_layout(
            doc.modelspace(), finalize=True
        )
        pdf_path = Path(pdf_path)
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(str(pdf_path), facecolor=bg, bbox_inches="tight", pad_inches=0.2)
    finally:
        plt.close(fig)
    return pdf_path
