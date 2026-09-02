"""projekt — Mehr-Geschoss-Orchestrierung: mehrere Floors → ein Projekt-Plan-Set.

Ein reales Projekt hat N Geschosse (je eine Architektur-DXF). Diese Schicht fährt die
Pipeline je Geschoss und bündelt die Ergebnisse: pro Floor ein Notbeleuchtungs-DXF und
— auf Wunsch — ein **zusammengefügtes PDF** (ein Blatt je Geschoss) als Liefer-Dokument.

Reine Orchestrierung über `pipeline.run` (kein neues Fach-Wissen). Der PDF-Merge (pypdf)
+ der DXF→PDF-Export (matplotlib) sind optionale Abhängigkeiten (Extra `render`); der
Import passiert lazy, damit der Rest der Engine ohne sie läuft.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .contracts import ProjektKontext, ProviderBundle
from .pipeline import Output, run


@dataclass
class ProjektPlan:
    """Ein Geschoss-Eingang: Architektur-DXF + Geschoss-Kennung."""

    dxf_path: str
    floor: str


@dataclass
class ProjektErgebnis:
    outputs: list[Output] = field(default_factory=list)
    combined_pdf: str | None = None
    summary: dict = field(default_factory=dict)


def run_projekt(
    bundle: ProviderBundle,
    plaene: list[ProjektPlan],
    *,
    out_dir: str | Path | None = None,
    lb_path: str | None = None,
    plankopf: dict | None = None,
    pdf: bool = False,
    projekt_kontext: ProjektKontext | None = None,
) -> ProjektErgebnis:
    """Fährt die Pipeline je Geschoss; optional Sammel-PDF (ein Blatt je Geschoss).

    `projekt_kontext` (optional) ist gebäudeweit — er gilt wie die LB für das ganze
    Projekt und wird 1:1 an jede Geschoss-Pipeline gereicht (OIB-Pfad)."""
    out_dir = Path(out_dir) if out_dir is not None else None
    outputs: list[Output] = []
    dxf_paths: list[Path] = []

    for plan in plaene:
        op = out_dir / f"{plan.floor}_notbeleuchtung.dxf" if out_dir is not None else None
        out = run(bundle, dxf_path=plan.dxf_path, floor=plan.floor,
                  out_path=op, lb_path=lb_path, plankopf=plankopf,
                  projekt_kontext=projekt_kontext)
        outputs.append(out)
        if op is not None:
            dxf_paths.append(op)

    combined_pdf: str | None = None
    if pdf and out_dir is not None and dxf_paths:
        combined_pdf = str(_merge_pdf(dxf_paths, out_dir / "projekt_notbeleuchtung.pdf"))

    summary = {
        "n_geschosse": len(plaene),
        "geschosse": [
            {
                "floor": o.render_summary.get("floor"),
                "n_symbols": o.render_summary.get("n_symbols"),
                "pruefung": (o.render_summary.get("pruefung") or {}).get("status"),
            }
            for o in outputs
        ],
        "combined_pdf": combined_pdf,
    }
    # Die LB gilt für das ganze Projekt (ein `lb_path` für alle Geschosse), der
    # Review-Bedarf ist also nicht geschoss-spezifisch — er gehört auf die oberste
    # Ebene. Ohne ihn wäre ein rein norm-getriebener Plan-Satz von einem
    # LB-konformen nicht unterscheidbar (dieselbe Lücke wie in `POST /plan`).
    review = next((o.render_summary["lb_review"] for o in outputs
                   if "lb_review" in o.render_summary), None)
    if review is not None:
        summary["lb_review"] = review
    return ProjektErgebnis(outputs=outputs, combined_pdf=combined_pdf, summary=summary)


def _merge_pdf(dxf_paths: list[Path], ziel: Path) -> Path:
    """Jedes Geschoss-DXF → PDF-Seite; alle in ein PDF (Reihenfolge = Eingabe)."""
    from pypdf import PdfWriter

    from .render import dxf_zu_pdf

    writer = PdfWriter()
    for dxf in dxf_paths:
        seite = dxf.with_suffix(".pdf")
        dxf_zu_pdf(dxf, seite)
        writer.append(str(seite))
    ziel.parent.mkdir(parents=True, exist_ok=True)
    with open(ziel, "wb") as fh:
        writer.write(fh)
    return ziel
