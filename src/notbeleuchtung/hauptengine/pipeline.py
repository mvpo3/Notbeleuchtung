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

from .contracts import LBVorgabe, PlatzierungsErgebnis, ProviderBundle, RaumModell
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


def _coverage(
    raum: RaumModell, platzierung: PlatzierungsErgebnis, lb: LBVorgabe | None = None
) -> dict:
    """Audit der Planungs-Vollständigkeit — macht ein stummes RZ-only-Ergebnis LAUT.

    Die Leuchten-Arten (Sicherheitsleuchte/Antipanik) sind norm-getrieben über
    `raum_typ` (Enis). Liefert Selmans Raumerkennung untypisierte Räume (`raum_typ`
    leer), fällt die Norm auf den Rettungsweg-Default → der Plan kommt RZ-only heraus,
    ohne Fehler. Diese Warnungen surfacen das (auch im API-Response-Header), statt es
    zu verschlucken — kein Provider wird „korrekt" nur weil er nichts typisiert hat.

    **LB-aware:** hat die LB die Sicherheitsbeleuchtung explizit ausgeschlossen
    (`bereiche_exklusion`, z.B. Fischa GK4), ist ein RZ-only-Ergebnis GEWOLLT — dann
    ist die „nur RZ"-Warnung ein Fehlalarm und wird zum neutralen Hinweis.
    """
    n_untyped = sum(1 for r in raum.raeume if not (r.raum_typ or "").strip())
    arten = {p.kind for p in platzierung.platzierungen}
    lb_schliesst_sl_aus = bool(
        lb is not None and any(not b.sicherheitsbeleuchtung for b in lb.bereiche_exklusion)
    )
    warnungen: list[str] = []
    if raum.raeume and n_untyped == len(raum.raeume):
        warnungen.append(
            f"Kein Raum typisiert ({n_untyped}/{len(raum.raeume)}) → Raumerkennung liefert "
            "keine Raumtypen; Leuchten-Arten (Sicherheits-/Antipanik) nicht ableitbar."
        )
    elif n_untyped:
        warnungen.append(
            f"{n_untyped}/{len(raum.raeume)} Räume ohne Raumtyp → Leuchten-Arten evtl. unvollständig."
        )
    if raum.raeume and arten and arten <= {"rz"} and not lb_schliesst_sl_aus:
        warnungen.append(
            "Nur Rettungszeichen platziert — keine Sicherheits-/Antipanik-Leuchten "
            "(Raumtypen der Raumerkennung prüfen)."
        )
    hinweise: list[str] = []
    if lb_schliesst_sl_aus and arten <= {"rz"}:
        hinweise.append("Sicherheitsbeleuchtung per LB ausgeschlossen (bereiche_exklusion) — RZ-only ist gewollt.")
    return {
        "n_raeume": len(raum.raeume),
        "n_raeume_untypisiert": n_untyped,
        "arten_platziert": sorted(arten),
        "lb_angewendet": lb is not None,
        "warnungen": warnungen,
        "hinweise": hinweise,
    }


def run(
    bundle: ProviderBundle,
    dxf_path: str,
    floor: str,
    out_path: str | Path | None = None,
    lb_path: str | None = None,
) -> Output:
    raum = bundle.raum.parse(dxf_path, floor)
    # 2. Input (optional): LB parsen, falls ein LB-Provider verdrahtet + ein LB-Pfad da ist.
    lb = bundle.lb.parse_lb(lb_path) if (bundle.lb is not None and lb_path is not None) else None
    platzierung = bundle.platzierer.place(raum, bundle.norm, lb)
    if out_path is not None:
        render_summary = render_dxf(platzierung, raum, out_path)
    else:
        render_summary = _summary(raum, platzierung)
    # Coverage-Audit an beide Pfade anhängen (Warnungen fließen so auch in den API-Header).
    render_summary["coverage"] = _coverage(raum, platzierung, lb)
    return Output(
        raum=raum,
        platzierung=platzierung,
        render_summary=render_summary,
    )
