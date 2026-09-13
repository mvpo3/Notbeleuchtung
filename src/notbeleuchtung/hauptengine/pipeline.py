"""Pipeline — komponiert die 3 Owner-Provider zum Notbeleuchtungs-Durchstich.

    parse  -> RaumModell            (Selman)
    place  -> PlatzierungsErgebnis  (Leonis, konsumiert Raum + Norm)
    render -> Output                (Hauptengine)

Kennt nur die Ports (Protocols), nie eine konkrete Owner-Klasse. Mit `out_path`
schreibt render/ ein echtes Notbeleuchtungs-DXF (Slice 3); ohne bleibt es beim
Zähl-Summary (`rendered: False`).
"""
from __future__ import annotations

import inspect
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
from .render import blatt_vorlage_pfad, render_dxf
from .render.dxf_renderer import MassstabPasstNichtFehler
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
    # OVE E 8101 Pkt 560.9.001.AT / EN 62034: ab > 20 SICHERHEITSLEUCHTEN in einem
    # ZUSAMMENHÄNGENDEN GEBÄUDETEIL ist eine automatische Prüfeinrichtung Pflicht.
    # ⚠️ Gezählt wird hier `len(platzierung.platzierungen)` = alle Notlicht-Symbole EINES
    # GESCHOSSES (inkl. Rettungszeichen) — das ist NICHT die Bezugseinheit der Norm
    # (zusammenhängender Gebäudeteil). Der Hinweis bleibt deshalb VORLÄUFIG: er nennt die
    # gezählte Einheit + die fehlende Zuordnung, leitet WEDER Pflicht NOCH Entwarnung ab
    # und behauptet NICHT, eine Prüfeinrichtung fehle (Anlagen-Tatsache außerhalb des Plans).
    # Keine zweite Regel neben normwissen/astv (Enis-Abstimmung 2026-09-09).
    n_symbole = len(platzierung.platzierungen)
    if n_symbole > _AUTO_PRUEF_SCHWELLE:
        hinweise.append(
            f"VORLÄUFIG: {n_symbole} Notlicht-Platzierungen in diesem Geschoss (inkl. "
            f"Rettungszeichen) über der Schwelle {_AUTO_PRUEF_SCHWELLE}. OVE E 8101 "
            "560.9.001.AT / EN 62034 zählt jedoch Sicherheitsleuchten je zusammenhängendem "
            "Gebäudeteil (nicht je Geschoss) — diese Bezugseinheit ist hier nicht ermittelt; "
            "daraus folgt weder eine Pflicht noch eine Entwarnung, und es wird nicht behauptet, "
            "eine Prüfeinrichtung fehle. Für einen belastbaren Befund fehlen: (1) die fachliche "
            "Abgrenzung der zusammenhängenden Gebäudeteile (Brandschutzkonzept/Planer) und "
            "(2) die Zuordnung Leuchte→Gebäudeteil (Platzierung trägt heute weder raum_id noch "
            "gebaeudeteil_id)."
        )
        # Dieselbe Fundstelle nennt zwei weitere Aspekte (EN 62034 / EN 50172): Kreis-
        # Redundanz und Bemessungsstrom. Die Kreis-Verteilung ist aus der bereits
        # vorhandenen Zuordnung (circuit_hint) ablesbar; die Bemessungsstrom-Grenze
        # (≤ 60 % je Kreis) braucht Produkt-Stromdaten und bleibt OFFEN — kein
        # fabrizierter Beleg, rein additiver Hinweis (nicht-blockierend).
        kreise = {(p.circuit_hint or "").strip() for p in platzierung.platzierungen}
        kreise.discard("")
        if kreise:
            redundanz = (
                f"auf {len(kreise)} Stromkreise verteilt (≥ 2 = Kreis-Redundanz erkennbar)"
                if len(kreise) >= 2
                else "auf nur 1 Stromkreis — ≥ 2 alternierende Kreise (EN 50172) prüfen"
            )
            hinweise.append(
                f"Prüfeinrichtungs-Anlage: {redundanz}; Bemessungsstrom ≤ 60 % je Kreis "
                "nicht geprüft (Produkt-Stromdaten fehlen)."
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


def _parse_raum(
    bundle: ProviderBundle, dxf_path: str, floor: str, tmp: str
) -> tuple[RaumModell, str]:
    """1. Input öffnen — DWG wird vorab konvertiert. Liefert (RaumModell, DXF-Pfad):
    der Pfad wird auch vom Render gebraucht (Architektur-Unterlage), deshalb lebt
    das Konvertat im vom Aufrufer gestellten `tmp` bis nach dem Render."""
    if Path(dxf_path).suffix.lower() == ".dwg":
        konvertat = str(stelle_dxf_bereit(dxf_path, tmp))
        return bundle.raum.parse(konvertat, floor), konvertat
    return bundle.raum.parse(dxf_path, floor), dxf_path


def run(
    bundle: ProviderBundle,
    dxf_path: str,
    floor: str,
    out_path: str | Path | None = None,
    lb_path: str | None = None,
    plankopf: dict | None = None,
    projekt_kontext: ProjektKontext | None = None,
    photometrie: PhotometrieBefund | None = None,
    template_path: str | None = None,
    pdf_quelle: bool = False,
) -> Output:
    # Grundlage des Lux-Nachweises: reist mit dem Bundle, das die Registry gebaut
    # hat (typisiert, kein Zugriff auf Platzierer-Interna). Ein explizit
    # übergebener Befund gewinnt; ohne beides wird nichts behauptet.
    photometrie = photometrie or photometrie_des_bundles(bundle)
    with tempfile.TemporaryDirectory(prefix="notbel_dwg_") as _tmp:
        raum, quelle_dxf = _parse_raum(bundle, dxf_path, floor, _tmp)
        return _run_mit_quelle(
            bundle, raum, quelle_dxf, out_path=out_path, lb_path=lb_path,
            plankopf=plankopf, projekt_kontext=projekt_kontext, photometrie=photometrie,
            template_path=template_path, pdf_quelle=pdf_quelle,
        )


def _run_mit_quelle(
    bundle: ProviderBundle,
    raum: RaumModell,
    quelle_dxf: str,
    *,
    out_path,
    lb_path,
    plankopf,
    projekt_kontext,
    photometrie,
    template_path=None,
    pdf_quelle=False,
    bestand_leuchten_mm=(),
) -> Output:
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
    # R1 (Owner 2026-09-11) + Punkt 3 (2026-09-12): Bestands-Leuchten-Linie. Explizit
    # übergebene Punkte gewinnen; sonst extrahiert die Pipeline sie SELBST aus der
    # Architektur-Unterlage (bestand_leuchten.extrahiere_fuer, fail-open) — die
    # R1-/R6-Lichtlinien-Regeln liegen damit auf jedem Plan an, ohne Runner-Handarbeit.
    # Nur durchreichen, wenn der Platzierer das kwarg kennt (Fakes bleiben unberührt).
    bestand = tuple(bestand_leuchten_mm)
    if not bestand and quelle_dxf:
        from . import bestand_leuchten as _bestand_mod
        bestand = _bestand_mod.extrahiere_fuer(raum, quelle_dxf)
    _nimmt_bestand = "bestand_leuchten_mm" in inspect.signature(
        bundle.platzierer.place).parameters
    extra = {"bestand_leuchten_mm": bestand} if (bestand and _nimmt_bestand) else {}
    if oib_befund is not None:
        platzierung = bundle.platzierer.place(raum, bundle.norm, lb, oib=oib_befund, **extra)
    else:
        platzierung = bundle.platzierer.place(raum, bundle.norm, lb, **extra)
    pruef = pruefbericht(
        raum, platzierung, lb, norm=bundle.norm, oib=oib_befund,
        photometrie=photometrie, projekt_kontext=projekt_kontext,
    )
    if out_path is not None:
        # Auslieferung: das gelieferte DXF ist das Layout-Blatt (Vorlage in Layout1,
        # Viewport 1:50, in AutoCAD plot-fertig). Ohne expliziten Pfad die versionierte
        # Rivoplan-Vorlage nehmen; fehlt sie im Repo → Modelspace-Blatt (#115).
        aus_template = template_path if template_path is not None else blatt_vorlage_pfad()
        # PDF-Weg braucht eine Modelspace-Quelle (ezdxf rastert Paperspace nicht) —
        # nur erzeugen, wenn ein PDF ansteht (kein Doppel-Render für reine DXF-Lieferung).
        pdf_quelle_path = None
        if pdf_quelle and aus_template is not None:
            _op = Path(out_path)
            pdf_quelle_path = _op.with_name(_op.stem + ".modelspace.dxf")
        try:
            render_summary = render_dxf(
                platzierung, raum, out_path, lb, pruefung=pruef, plankopf=plankopf,
                photometrie=photometrie, unterlage_dxf=quelle_dxf,
                template_path=aus_template, pdf_quelle_path=pdf_quelle_path,
            )
        except MassstabPasstNichtFehler as e:
            # Liefer-Policy: passt der Plan in 1:50 nicht in den Vorlagen-Viewport (G6),
            # NICHT abbrechen — auf das Modelspace-Blatt (#115) zurückfallen (Grundriss
            # maßstabfrei ins Planfenster). Der Maßstab-Verlust wird sichtbar gemacht.
            render_summary = render_dxf(
                platzierung, raum, out_path, lb, pruefung=pruef, plankopf=plankopf,
                photometrie=photometrie, unterlage_dxf=quelle_dxf, template_path=None,
            )
            render_summary["layout_fallback"] = str(e)
        # Lux-Nachweis-Bericht je Plan (Owner 2026-09-08): eigene DIALux-artige
        # Seite neben dem DXF. Additiv — ein Fehler bricht den Plan-Lauf NIE.
        try:
            from .render.lux_nachweis_bericht import schreibe_bericht  # lazy: matplotlib
            _bericht = schreibe_bericht(
                raum, platzierung, bundle.norm,
                Path(out_path).with_suffix(".nachweis.png"),
                i_cd_fn=getattr(bundle.platzierer, "_i_cd_fn", None),
                projekt=(plankopf or {}).get("projekt"),
            )
            if _bericht is not None:
                render_summary["lux_nachweis"] = str(_bericht)
        except Exception as e:  # noqa: BLE001 — Bericht additiv, nie plan-brechend
            render_summary["lux_nachweis_fehler"] = str(e)
    else:
        render_summary = _summary(raum, platzierung)
    # Coverage-Audit + Norm-Prüfbericht an beide Pfade anhängen.
    render_summary["bestand_leuchten"] = len(bestand)   # Punkt-3-Sichtbarkeit
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
