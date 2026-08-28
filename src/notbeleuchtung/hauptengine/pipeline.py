"""Pipeline — komponiert die 3 Owner-Provider zum Notbeleuchtungs-Durchstich.

    parse  -> RaumModell            (Selman)
    place  -> PlatzierungsErgebnis  (Leonis, konsumiert Raum + Norm)
    render -> Output                (Hauptengine)

Kennt nur die Ports (Protocols), nie eine konkrete Owner-Klasse. Mit `out_path`
schreibt render/ ein echtes Notbeleuchtungs-DXF (Slice 3); ohne bleibt es beim
Zähl-Summary (`rendered: False`).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .contracts import PlatzierungsErgebnis, ProviderBundle, RaumModell
from .render import render_dxf


@dataclass
class Output:
    raum: RaumModell
    platzierung: PlatzierungsErgebnis
    render_summary: dict = field(default_factory=dict)


def _summary(raum: RaumModell, platzierung: PlatzierungsErgebnis) -> dict:
    """Zähl-Summary ohne DXF-Output (kein out_path angefragt)."""
    by_kind: dict[str, int] = {}
    for p in platzierung.platzierungen:
        by_kind[p.kind] = by_kind.get(p.kind, 0) + 1
    return {
        "floor": platzierung.floor,
        "n_symbols": len(platzierung.platzierungen),
        "by_kind": by_kind,
        "n_raeume": len(raum.raeume),
        "rendered": False,
    }


def run(
    bundle: ProviderBundle,
    dxf_path: str,
    floor: str,
    out_path: str | Path | None = None,
) -> Output:
    raum = bundle.raum.parse(dxf_path, floor)
    platzierung = bundle.platzierer.place(raum, bundle.norm)
    if out_path is not None:
        render_summary = render_dxf(platzierung, raum, out_path)
    else:
        render_summary = _summary(raum, platzierung)
    return Output(
        raum=raum,
        platzierung=platzierung,
        render_summary=render_summary,
    )
