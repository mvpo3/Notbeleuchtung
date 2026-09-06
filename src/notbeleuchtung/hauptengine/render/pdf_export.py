"""pdf_export — Notbeleuchtungs-DXF → PDF (Liefer-Format).

Rastert/vektorisiert das gerenderte DXF über den ezdxf-matplotlib-Backend in ein PDF.
Der Nordstern liefert einen Plan „zum Weitergeben" — DXF ist der CAD-Austausch, PDF das
Sicht-/Druck-Dokument. Reine Ausgabe-Schicht; erzeugt kein neues Fach-Wissen.

matplotlib + ezdxf.addons.drawing sind optionale Abhängigkeiten (Extra `render`); der
Import passiert lazy, damit der Rest der Engine ohne sie läuft.

CAD-Hintergrund: `dunkel=False` (Default, Owner-Regel 2026-09-06: das Liefer-PDF
ist WEISS) = weißer Druckgrund; `dunkel=True` = schwarzer CAD-Look auf Wunsch.
"""
from __future__ import annotations

from pathlib import Path


def dxf_zu_pdf(
    dxf_path: str | Path,
    pdf_path: str | Path,
    *,
    dunkel: bool = False,
    dpi: int = 300,
    breite_zoll: float = 16.5,
    hoehe_zoll: float = 11.7,   # A3 quer
    layout: str | None = None,  # z.B. "Notbeleuchtungsplan" = Owner-Blatt-Vorlage
    ausschnitt: tuple | None = None,  # (x0, y0, x1, y1) — nur diesen Bereich rendern
) -> Path:
    """Rendert `dxf_path` in ein PDF (`pdf_path`) und gibt den Pfad zurück.

    `layout=None` rendert den Modelspace (bisheriges Verhalten); ein Layout-Name
    rendert das Paperspace-Blatt (Planrahmen + Viewport, Owner-Vorlage)."""
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
        ziel_layout = (doc.layout(layout) if layout and layout in doc.layout_names()
                       else doc.modelspace())
        lp = LayoutProperties.from_layout(ziel_layout)
        lp.set_colors("#000000" if dunkel else "#FFFFFF")
        Frontend(RenderContext(doc), MatplotlibBackend(ax)).draw_layout(
            ziel_layout, finalize=True, layout_properties=lp
        )
        # ezdxf's draw_image erzeugt AxesImage ohne extent (Transform mappt
        # Pixel→Daten) — savefig(bbox_inches="tight") crasht dann in
        # get_window_extent ("cannot unpack non-iterable NoneType"). Extent =
        # Pixelmaße nachrüsten; der Transform macht daraus die richtige Screen-Box.
        # Zusätzlich spiegelt der Backend IMAGEs vertikal (empirisch geprüft an der
        # Blatt-Vorlage: AutoCAD richtig, matplotlib kopfüber — doppelter Flip aus
        # np.flip(axis=0) + Pixel-Transform) → Daten einmal zurückspiegeln.
        import numpy as np
        for im in ax.images:
            arr = im.get_array()
            if getattr(im, "_extent", None) is None:
                im._extent = (0.0, float(arr.shape[1]), 0.0, float(arr.shape[0]))
            im.set_data(np.flip(arr, axis=0))
        if ausschnitt is not None:
            # finalize=True setzt aspect=equal mit adjustable='datalim' — dabei
            # überstimmt matplotlib feste xlim/ylim („Ignoring fixed x limits").
            # 'box' hält die Limits fest und passt stattdessen die Achsen-Box an.
            ax.set_aspect("equal", adjustable="box")
            x0, y0, x1, y1 = ausschnitt
            pad_x, pad_y = (x1 - x0) * 0.01, (y1 - y0) * 0.01
            ax.set_xlim(x0 - pad_x, x1 + pad_x)
            ax.set_ylim(y0 - pad_y, y1 + pad_y)
        pdf_path = Path(pdf_path)
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(str(pdf_path), facecolor=bg, bbox_inches="tight", pad_inches=0.2)
    finally:
        plt.close(fig)
    return pdf_path
