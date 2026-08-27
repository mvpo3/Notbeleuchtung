"""Pipeline — komponiert die 3 Owner-Provider zum Notbeleuchtungs-Durchstich.

    parse  -> RaumModell            (Selman)
    place  -> PlatzierungsErgebnis  (Leonis, konsumiert Raum + Norm)
    render -> Output                (Hauptengine)

Kennt nur die Ports (Protocols), nie eine konkrete Owner-Klasse. In Slice 0 ist
`render` ein Stub (zählt/aggregiert); echtes DXF/PDF ab Slice 3 (render/).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .contracts import PlatzierungsErgebnis, ProviderBundle, RaumModell


@dataclass
class Output:
    raum: RaumModell
    platzierung: PlatzierungsErgebnis
    render_summary: dict = field(default_factory=dict)


def _render_stub(raum: RaumModell, platzierung: PlatzierungsErgebnis) -> dict:
    """Slice-0-Platzhalter für hauptengine.render (echtes DXF ab Slice 3)."""
    by_kind: dict[str, int] = {}
    for p in platzierung.platzierungen:
        by_kind[p.kind] = by_kind.get(p.kind, 0) + 1
    return {
        "floor": platzierung.floor,
        "n_symbols": len(platzierung.platzierungen),
        "by_kind": by_kind,
        "n_raeume": len(raum.raeume),
        "rendered": False,   # Slice 0: noch kein echtes DXF
    }


def run(bundle: ProviderBundle, dxf_path: str, floor: str) -> Output:
    raum = bundle.raum.parse(dxf_path, floor)
    platzierung = bundle.platzierer.place(raum, bundle.norm)
    return Output(
        raum=raum,
        platzierung=platzierung,
        render_summary=_render_stub(raum, platzierung),
    )
