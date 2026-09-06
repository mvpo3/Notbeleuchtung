"""Pipeline — komponiert die 3 Owner-Provider zum Notbeleuchtungs-Durchstich.

    parse  -> RaumModell            (Selman)
    place  -> PlatzierungsErgebnis  (Leonis, konsumiert Raum + Norm)
    render -> Output                (Hauptengine)

Kennt nur die Ports (Protocols), nie eine konkrete Owner-Klasse. Mit `out_path`
schreibt render/ ein echtes Notbeleuchtungs-DXF (Slice 3); ohne bleibt es beim
Zähl-Summary (`rendered: False`).
"""
from __future__ import annotations

import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from .contracts import (
    LBVorgabe,
    PlatzierungsErgebnis,
    ProjektKontext,
    ProviderBundle,
    RaumModell,
)
from .dwg_input import stelle_dxf_bereit
from .photometrie_befund import PhotometrieBefund, photometrie_des_bundles
from .render import render_dxf
from .validierung import pruefbericht


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


_AUTO_PRUEF_SCHWELLE = 20  # OVE E 8101 560.9.001.AT: EN-62034-Prüfeinrichtung Pflicht ab > 20 Leuchten


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
    # OVE E 8101 Pkt 560.9.001.AT: ab > 20 Sicherheitsleuchten in einem zusammenhängenden
    # Gebäudeteil ist eine automatische Prüfeinrichtung mit zentraler Erfassung (EN 62034)
    # Pflicht. Nicht-blockierender Hinweis (Anlagen-, keine Platzierungs-Anforderung).
    n_leuchten = len(platzierung.platzierungen)
    if n_leuchten > _AUTO_PRUEF_SCHWELLE:
        hinweise.append(
            f"{n_leuchten} Sicherheitsleuchten (> {_AUTO_PRUEF_SCHWELLE}) → automatische "
            "Prüfeinrichtung mit zentraler Erfassung erforderlich (OVE E 8101 560.9.001.AT / EN 62034)."
        )
    # Audit-Trail-Näherung an Sonderstellen/Flag-Räumen (Enis-Review #95): die
    # `norm_quelle` dieser Leuchten ist die Fallback-Referenzregel, nicht der echte
    # Auslöser (§4.1.2 c/h/i, §4.3.8, §4.4.1) — bis Enis' Quellen-Naht nachkommt.
    if raum.sonderstellen or any(
        r.ist_barrierefrei or r.besondere_gefaehrdung for r in raum.raeume
    ):
        hinweise.append(
            "Sonderstellen-/Flag-Leuchten: norm_quelle = Fallback-Referenzregel — echte "
            "Auslöser-Fundstellen (EN 1838 §4.1.2 c/h/i, §4.3.8, §4.4.1) folgen mit der "
            "Quellen-Naht im NormRegelwerk."
        )
    return {
        "n_raeume": len(raum.raeume),
        "n_raeume_untypisiert": n_untyped,
        "arten_platziert": sorted(arten),
        "lb_angewendet": lb is not None,
        "warnungen": warnungen,
        "hinweise": hinweise,
    }


def _parse_raum(bundle: ProviderBundle, dxf_path: str, floor: str) -> RaumModell:
    """1. Input öffnen — DWG wird vorab konvertiert (nur `parse` braucht die Datei,
    danach ist alles im RaumModell → das Konvertat darf sofort weg)."""
    if Path(dxf_path).suffix.lower() == ".dwg":
        with tempfile.TemporaryDirectory(prefix="notbel_dwg_") as tmp:
            return bundle.raum.parse(str(stelle_dxf_bereit(dxf_path, tmp)), floor)
    return bundle.raum.parse(dxf_path, floor)


def run(
    bundle: ProviderBundle,
    dxf_path: str,
    floor: str,
    out_path: str | Path | None = None,
    lb_path: str | None = None,
    plankopf: dict | None = None,
    projekt_kontext: ProjektKontext | None = None,
    photometrie: PhotometrieBefund | None = None,
) -> Output:
    # Grundlage des Lux-Nachweises: reist mit dem Bundle, das die Registry gebaut
    # hat (typisiert, kein Zugriff auf Platzierer-Interna). Ein explizit
    # übergebener Befund gewinnt; ohne beides wird nichts behauptet.
    photometrie = photometrie or photometrie_des_bundles(bundle)
    raum = _parse_raum(bundle, dxf_path, floor)
    # 2. Input (optional): LB parsen, falls ein LB-Provider verdrahtet + ein LB-Pfad da ist.
    # Fail-Closed (Enis' LB-Parser): bei blockierendem Zweifel wirft parse_lb `LbFehler`.
    # Der Plan wird trotzdem erzeugt (Norm-Default greift), aber das `lb_review`-Flag macht
    # sichtbar, dass die LB-Vorgaben NICHT angewendet wurden — sie werden nicht still verloren.
    lb = None
    lb_review: dict | None = None
    if bundle.lb is not None and lb_path is not None:
        from notbeleuchtung.normwissen.lb import LbFehler  # Provider-Ausnahme (lazy)
        try:
            lb = bundle.lb.parse_lb(lb_path)
        except LbFehler as e:
            lb_review = {"status": "review_erforderlich", "meldung": str(e)}
    # OIB-Pfad (optional 3. Input): gebäudeweiter ProjektKontext → Erforderlichkeits-
    # Befund je Gebäudeteil. Gated OVE-scope-gebundene Trigger (Antipanik-Fläche).
    # Ohne Provider oder Kontext wird `place` exakt wie bisher gerufen (bit-identisch).
    oib_befund = None
    if bundle.oib is not None and projekt_kontext is not None:
        oib_befund = bundle.oib.bewerte_oib(projekt_kontext)
    if oib_befund is not None:
        platzierung = bundle.platzierer.place(raum, bundle.norm, lb, oib=oib_befund)
    else:
        platzierung = bundle.platzierer.place(raum, bundle.norm, lb)
    pruef = pruefbericht(
        raum, platzierung, lb, norm=bundle.norm, oib=oib_befund, photometrie=photometrie
    )
    if out_path is not None:
        render_summary = render_dxf(
            platzierung, raum, out_path, lb, pruefung=pruef, plankopf=plankopf,
            photometrie=photometrie,
        )
    else:
        render_summary = _summary(raum, platzierung)
    # Coverage-Audit + Norm-Prüfbericht an beide Pfade anhängen.
    render_summary["coverage"] = _coverage(raum, platzierung, lb)
    render_summary["pruefung"] = pruef
    if photometrie is not None:
        render_summary["photometrie"] = {
            "quelle": photometrie.quelle,
            "ldt": photometrie.ldt_name,
            "rotationssymmetrisch": photometrie.rotationssymmetrisch,
            "ausrichtung_zugesichert": photometrie.ausrichtung_zugesichert,
            "vollstaendiger_nachweis": photometrie.vollstaendiger_nachweis,
            "hinweis": photometrie.hinweis,
            "einschraenkungen": list(photometrie.einschraenkungen),
        }
    if lb_review is not None:
        render_summary["lb_review"] = lb_review
    if oib_befund is not None:
        # Gate-Logik lebt beim Konsumenten (platzierung/oib_gate); lazy wie LbFehler.
        from notbeleuchtung.platzierung.oib_gate import gate_summary
        render_summary["oib"] = gate_summary(
            oib_befund, raum.floor, [r.id for r in raum.raeume]
        )
    return Output(
        raum=raum,
        platzierung=platzierung,
        render_summary=render_summary,
    )
