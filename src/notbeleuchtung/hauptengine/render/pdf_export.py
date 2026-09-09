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

#: Fester Liefer-Maßstab (Owner 2026-09-09, Referenz MOL_GR-…_1-50): das PDF ist ein
#: ECHTES Vektor-Blatt, dessen Seite = Zeichnungs-Ausschnitt / Maßstab misst — so lässt es
#: sich wie ein CAD-Plan stufenlos zoomen (statt eines kleinen tight-gecroppten Rasters).
#: 1 Zeichnungs-mm → 1/50 Seiten-mm. Nur wirksam mit `ausschnitt`; None = altes A3-Verhalten.
_LIEFER_MASSSTAB = 50
#: Kanten-Deckel gegen Phantom-Extents (korrupte DXF) — nie größer als 5 m Blatt.
_MAX_BLATT_MM = 5000.0
#: Layer des Blatt-Rahmens (Rivoplan-Vorlage) — sein Extent ist der Liefer-Ausschnitt.
_TITLEBLOCK_LAYER = "din_SIBEL_99_titleblock"


def _auto_ausschnitt(doc):
    """Extent des Blatt-Rahmens im Modelspace → Liefer-Ausschnitt (1:50-Blatt).

    Damit JEDER PDF-Weg der Hauptengine (API, Batch, _merge_pdf, CLI) automatisch das
    große Vektor-Blatt bekommt, ohne dass der Aufrufer den Ausschnitt kennen muss.
    Kein Rahmen (kein Blatt-/Template-Modus) → None (A3-Fallback)."""
    import ezdxf.bbox as _ezbbox

    tb = [e for e in doc.modelspace() if e.dxf.layer == _TITLEBLOCK_LAYER]
    if not tb:
        return None
    ext = _ezbbox.extents(tb, fast=True)
    if not ext.has_data:
        return None
    return (ext.extmin.x, ext.extmin.y, ext.extmax.x, ext.extmax.y)


def dxf_zu_pdf(
    dxf_path: str | Path,
    pdf_path: str | Path,
    *,
    dunkel: bool = False,
    dpi: int = 300,
    breite_zoll: float = 16.5,
    hoehe_zoll: float = 11.7,   # A3 quer (Fallback ohne Ausschnitt)
    layout: str | None = None,  # z.B. "Notbeleuchtungsplan" = Owner-Blatt-Vorlage
    ausschnitt: tuple | None = None,  # (x0, y0, x1, y1) — nur diesen Bereich rendern
    massstab: int | None = _LIEFER_MASSSTAB,  # Seite = Ausschnitt/Maßstab (Vektor, zoombar)
) -> Path:
    """Rendert `dxf_path` in ein PDF (`pdf_path`) und gibt den Pfad zurück.

    `layout=None` rendert den Modelspace (bisheriges Verhalten); ein Layout-Name
    rendert das Paperspace-Blatt (Planrahmen + Viewport, Owner-Vorlage).

    `massstab` (mit `ausschnitt`): die Seite wird auf `Ausschnitt/Maßstab` mm dimensioniert
    (1:50-Vektor-Blatt) und OHNE tight-Crop geschrieben — man kann wie in einem CAD-Plan
    beliebig hineinzoomen. `massstab=None` fällt auf das alte A3-tight-Verhalten zurück."""
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
    # „Immer so" (Owner 2026-09-09): ohne expliziten Ausschnitt automatisch den
    # Blatt-Rahmen als 1:50-Liefer-Ausschnitt nehmen — gilt für JEDES PDF der Engine
    # (API/Batch/CLI), nicht nur die Skripte. Nur bei PDF-Ausgabe (PNG bleibt wie bisher).
    if ausschnitt is None and massstab and str(pdf_path).lower().endswith(".pdf"):
        ausschnitt = _auto_ausschnitt(doc)
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
        skaliertes_blatt = False
        if ausschnitt is not None:
            # finalize=True setzt aspect=equal mit adjustable='datalim' — dabei
            # überstimmt matplotlib feste xlim/ylim („Ignoring fixed x limits").
            # 'box' hält die Limits fest und passt stattdessen die Achsen-Box an.
            ax.set_aspect("equal", adjustable="box")
            x0, y0, x1, y1 = ausschnitt
            pad_x, pad_y = (x1 - x0) * 0.01, (y1 - y0) * 0.01
            ax.set_xlim(x0 - pad_x, x1 + pad_x)
            ax.set_ylim(y0 - pad_y, y1 + pad_y)
            if massstab and x1 > x0 and y1 > y0:
                # Echtes Vektor-Blatt: Seite = Ausschnitt/Maßstab (in mm), Achse [0,0,1,1]
                # füllt sie (Seiten-Aspekt == Daten-Aspekt → kein Letterbox). Kein
                # tight-Crop → die Seite bleibt physisch groß und stufenlos zoombar.
                page_w = (x1 - x0 + 2 * pad_x) / massstab
                page_h = (y1 - y0 + 2 * pad_y) / massstab
                k = max(page_w, page_h)
                if k > _MAX_BLATT_MM:                      # Phantom-Extents deckeln
                    page_w *= _MAX_BLATT_MM / k
                    page_h *= _MAX_BLATT_MM / k
                fig.set_size_inches(page_w / 25.4, page_h / 25.4)
                skaliertes_blatt = True
        pdf_path = Path(pdf_path)
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        if skaliertes_blatt:
            fig.savefig(str(pdf_path), facecolor=bg)          # Seite == figsize, Vektor
        else:
            fig.savefig(str(pdf_path), facecolor=bg, bbox_inches="tight", pad_inches=0.2)
    finally:
        plt.close(fig)
    return pdf_path
