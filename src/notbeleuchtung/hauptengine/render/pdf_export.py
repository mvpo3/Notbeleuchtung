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
    from ezdxf.addons.drawing.properties import LayoutProperties

    doc = ezdxf.readfile(str(dxf_path))
    # Der DXF-Standard-Textstil nutzt die SHX-Schrift „txt" — deren Glyph-Abdeckung im
    # matplotlib-Backend ist lückenhaft (Großbuchstaben-O/Umlaute → Kästchen). Für die
    # PDF-/Bild-Ausgabe auf eine TTF mit voller Abdeckung umstellen (DXF selbst bleibt
    # unangetastet — CAD rendert weiter mit seiner Standard-Schrift).
    if "Standard" in doc.styles:
        doc.styles.get("Standard").dxf.font = "DejaVuSans.ttf"
    bg = "black" if dunkel else "white"
    fig = plt.figure(figsize=(breite_zoll, hoehe_zoll), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    try:
        # Hintergrund über explizite LayoutProperties an draw_layout übergeben, damit
        # ACI-Farbe 7 (weiß/schwarz) korrekt invertiert: auf weißem Druckgrund sonst
        # weiß-auf-weiß → Legende/Plankopf/Stückliste/Prüfbericht (alle Layer-Farbe 7)
        # unsichtbar. set_colors(bg) leitet die Vordergrundfarbe aus der bg-Helligkeit
        # ab (schwarz auf hell / weiß auf dunkel). Ohne explizites layout_properties
        # re-derived draw_layout die Farben aus dem Layout und überschrieb die Inversion.
        lp = LayoutProperties.from_layout(doc.modelspace())
        lp.set_colors("#000000" if dunkel else "#FFFFFF")
        Frontend(RenderContext(doc), MatplotlibBackend(ax)).draw_layout(
            doc.modelspace(), finalize=True, layout_properties=lp
        )
        pdf_path = Path(pdf_path)
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(str(pdf_path), facecolor=bg, bbox_inches="tight", pad_inches=0.2)
    finally:
        plt.close(fig)
    return pdf_path
