"""lux_nachweis_bericht — EN-1838-Lux-Nachweis-Bericht je Plan (Rivoplan-Layout).

Erzeugt aus dem **fertigen** `PlatzierungsErgebnis` + `RaumModell` eine Bericht-Seite
im Stil geprüfter Profi-Berechnungen (DIALux/din, Relux/Schrack): Falschfarben-Lux-
Feld über die Fluchtwege + beschriftete Isolux-Konturen (1 lx grün = Norm), Bemaßung/
Maßstab, Ergebnistabelle (Em/Emin/Emax/g1/g2), din-Nachweis-Tabelle (Mittellinie ≥1 lx
+ Mittelfläche ≥0,5 lx + Ud ≥1:40), polare LVK + Leuchten-Stückliste — gebrandet mit
dem Rivoplan-Logo. **Re-Konsum**: platziert NICHTS neu, rechnet das Feld aus den
schon gesetzten Sicherheits-/Antipanikleuchten (wie `platzierung.lux_nachweis`).

Wird von `pipeline._run_mit_quelle` je Plan aufgerufen (lazy, matplotlib nur beim
Render). Rendert nichts (`None`), wenn es keine Korridore oder keine Leuchten gibt.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.patches import Polygon as MplPoly
from matplotlib.patches import Rectangle
from matplotlib.path import Path as MPath

from notbeleuchtung.hauptengine.contracts import NormProvider, PlatzierungsErgebnis, RaumModell
from notbeleuchtung.platzierung.geometry import _bbox, point_in_polygon
from notbeleuchtung.platzierung.lux import lux_punkte
from notbeleuchtung.platzierung.mittellinie import mittellinie

_ROOT = Path(__file__).resolve().parents[4]
_LOGO = _ROOT / "Vorlagen-Legende" / "rivoplan_logo.png"
_LDT = _ROOT / "CAD_Symbole" / "photometrie" / "sl_nlkbu433_3h_corridor.ldt"
_NAVY, _GREEN, _INK = "#1f3b57", "#127a3a", "#222222"
_KORR = {"GANG", "FLUR", "KORRIDOR"}
_LICHT = {"sicherheitsleuchte", "antipanik"}
MF, HM, _ICD = 0.80, 2.4, 45.0                     # Wartungsfaktor · Montagehöhe · generische cd
_VMIN, _VMAX = 0.5, 6.0
_ISO = [0.5, 1.0, 2.0, 3.0, 4.0, 5.0]
_CMAP = "RdYlGn_r"


def _generisch(gamma, c=0.0):
    return _ICD


def _lade_photo():
    """Beste-Fall Hersteller-LVK (Schrack Corridor-SL); None wenn nicht vorhanden."""
    try:
        from notbeleuchtung.normwissen.photometrie import lade_ldt
        return lade_ldt(_LDT) if _LDT.exists() else None
    except Exception:  # noqa: BLE001 — Asset optional; ohne LDT generisch rechnen
        return None


def _lux_feld(gx, gy, sl, i_cd_fn):
    h = HM * 1000.0
    e = np.zeros_like(gx)
    ivec = np.vectorize(i_cd_fn)
    for lx, ly, az in sl:
        d_h = np.hypot(gx - lx, gy - ly)
        cos_t = h / np.hypot(d_h, h)
        gamma = np.degrees(np.arctan2(d_h, h))
        c = (np.degrees(np.arctan2(gy - ly, gx - lx)) - az) % 360.0
        e += ivec(gamma, c) * cos_t**3 / (HM**2)
    return e * MF


def _band(linie, breite_mm):
    if len(linie) < 2:
        return []
    off = breite_mm / 4.0
    band = []
    for i, (x, y) in enumerate(linie):
        x2, y2 = linie[min(i + 1, len(linie) - 1)]
        x1, y1 = linie[max(i - 1, 0)]
        tx, ty = x2 - x1, y2 - y1
        n = (tx * tx + ty * ty) ** 0.5
        if n < 1e-9:
            continue
        nx, ny = -ty / n, tx / n
        band += [(x + nx * off, y + ny * off), (x - nx * off, y - ny * off)]
    return band


def _rw_stats(r, norm, sl, i_cd_fn):
    anf = norm.fuer_raum(r.raum_typ, r.ist_fluchtweg)
    h, wf = anf.montagehoehe_mm / 1000.0, (getattr(anf, "wartungsfaktor", None) or 1.0)
    drin = [(x, y, az) for (x, y, az) in sl if point_in_polygon((x, y), r.polygon_mm)]
    bb = _bbox(r.polygon_mm)
    breite = min(bb[2] - bb[0], bb[3] - bb[1])
    ml = mittellinie(r.polygon_mm, 250.0)
    band = _band(ml, breite)
    rml = lux_punkte(drin, ml, montagehoehe_m=h, i_cd_fn=i_cd_fn, ziel_lux=1.0, wartungsfaktor=wf)
    rmf = (lux_punkte(drin, ml + band, montagehoehe_m=h, i_cd_fn=i_cd_fn, ziel_lux=0.5, wartungsfaktor=wf)
           if band else rml)
    return {"emin_mf": rmf.min_lux, "emax_mf": rmf.max_lux, "emin_ml": rml.min_lux,
            "emax_ml": rml.max_lux, "ud": rmf.ud, "ok_mf": rmf.min_lux >= 0.5,
            "ok_ml": rml.min_lux >= 1.0, "ok_ud": rmf.ud >= 0.025}


def _leuchte_symbol(ax, x_m, y_m, az_deg, length_m=0.62, width_m=0.28):
    a = np.radians(az_deg)
    ca, sa = np.cos(a), np.sin(a)
    hx, hy = length_m / 2, width_m / 2
    corners = [(-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)]
    world = [(x_m + px * ca - py * sa, y_m + px * sa + py * ca) for px, py in corners]
    ax.add_patch(MplPoly(world, closed=True, fc=_GREEN, ec="white", lw=1.0, zorder=7))


def _scalebar(ax, x0, y0, length_m, label):
    ax.add_patch(Rectangle((x0, y0), length_m, 0.12, fc="k", ec="k", zorder=9))
    ax.plot([x0, x0], [y0 - 0.12, y0 + 0.24], "k", lw=1, zorder=9)
    ax.plot([x0 + length_m, x0 + length_m], [y0 - 0.12, y0 + 0.24], "k", lw=1, zorder=9)
    ax.text(x0 + length_m / 2, y0 + 0.38, label, ha="center", va="bottom", fontsize=7.5)


def schreibe_bericht(
    raum: RaumModell,
    platzierung: PlatzierungsErgebnis,
    norm: NormProvider,
    out: str | Path,
    *,
    i_cd_fn=None,
    projekt: str | None = None,
    seite: int = 1,
) -> Path | None:
    """Bericht-Seite als PNG neben `out` schreiben; `None` ohne Korridor/Leuchte.

    `i_cd_fn` = Hersteller-Photometrie (aus dem Bundle/Platzierer); ohne sie wird die
    Standard-Corridor-LDT geladen, sonst generisch gerechnet. Rechnet NICHT neu —
    das Feld kommt aus den bereits platzierten Sicherheits-/Antipanikleuchten.
    """
    korr = [r for r in raum.raeume if r.raum_typ.upper() in _KORR and len(r.polygon_mm) >= 3]
    # Finished PlatzierungsErgebnis ist bereits entzerrt (abstand_nachpass) — keine
    # erneute Dublettenzusammenfassung; alle platzierten Leuchten zählen.
    sl3 = [
        (p.xy_mm[0], p.xy_mm[1], p.rotation_deg)
        for p in platzierung.platzierungen if p.kind in _LICHT
    ]
    if not korr or not sl3:
        return None

    out = Path(out)
    photo = _lade_photo()
    icd = i_cd_fn if i_cd_fn is not None else (photo.intensitaet if photo else _generisch)
    projekt = projekt or "—"

    mnx, mny = raum.bounds_mm.min_xy
    mxx, mxy = raum.bounds_mm.max_xy
    if mxx <= mnx or mxy <= mny:
        return None
    nx = 420
    ny = max(60, int(nx * (mxy - mny) / (mxx - mnx)))
    xs, ys = np.linspace(mnx, mxx, nx), np.linspace(mny, mxy, ny)
    gx, gy = np.meshgrid(xs, ys)
    e = _lux_feld(gx, gy, sl3, icd)
    grid_pts = np.column_stack([gx.ravel(), gy.ravel()])
    korr_mask, inside = {}, np.zeros(gx.size, bool)
    for r in korr:
        m = MPath(np.array(r.polygon_mm)).contains_points(grid_pts)
        korr_mask[r.id] = m
        inside |= m
    ef = np.where(inside.reshape(gx.shape), e, np.nan)

    def stats(rid):
        v = e.ravel()[korr_mask[rid]]
        if not len(v):
            return (0, 0, 0, 0, 0)
        em, emn, emx = float(v.mean()), float(v.min()), float(v.max())
        return (em, emn, emx, emn / em if em else 0, emn / emx if emx else 0)

    fig = plt.figure(figsize=(8.27, 11.69), dpi=170)
    fig.patch.set_facecolor("white")

    if _LOGO.exists():
        axl = fig.add_axes([0.82, 0.925, 0.11, 0.06]); axl.axis("off")
        axl.imshow(mpimg.imread(str(_LOGO)))
    fig.text(0.07, 0.963, "Rivoplan", fontsize=16, fontweight="bold", color="black")
    fig.text(0.07, 0.945, "Notbeleuchtung · Sicherheits- und Fluchtwegbeleuchtung", fontsize=8.5, color="#555")
    fig.text(0.60, 0.965, f"Projekt   {projekt}", fontsize=8.5, color=_INK)
    fig.text(0.60, 0.951, f"Geschoss  {raum.floor}", fontsize=8.5, color=_INK)
    fig.text(0.60, 0.937, "Norm      ÖNORM EN 1838", fontsize=8.5, color=_INK)
    fig.add_artist(plt.Line2D([0.07, 0.93], [0.923, 0.923], color=_NAVY, lw=1.6))
    fig.text(0.07, 0.905, "Lux-Nachweis — Fluchtweg-Beleuchtungsstärke (Notbetrieb)",
             fontsize=12.5, fontweight="bold", color=_INK)

    ax = fig.add_axes([0.08, 0.505, 0.84, 0.375])
    cmap = plt.get_cmap(_CMAP).copy(); cmap.set_bad(alpha=0)
    nrm = Normalize(_VMIN, _VMAX)
    ax.pcolormesh(gx / 1000, gy / 1000, ef, cmap=cmap, norm=nrm, shading="gouraud", zorder=1)
    for r in raum.raeume:
        xy = np.array(r.polygon_mm) / 1000.0
        if len(xy) < 3:
            continue
        is_k = r.raum_typ.upper() in _KORR
        ax.add_patch(MplPoly(xy, closed=True, fill=False, ec=("#333" if is_k else "#9aa4ad"),
                             lw=(1.3 if is_k else 0.9), zorder=3))
        area = abs(np.dot(xy[:, 0], np.roll(xy[:, 1], -1)) - np.dot(xy[:, 1], np.roll(xy[:, 0], -1))) / 2
        if not is_k and area >= 3.0 and len(raum.raeume) <= 14:  # komplexe Pläne nicht zukleistern
            ax.text(*xy.mean(0), r.raum_typ, fontsize=6.2, color="#9aa4ad", ha="center", va="center", zorder=3)
    eg = np.nan_to_num(ef)
    _halo = [pe.withStroke(linewidth=2.4, foreground="white")]
    cs = ax.contour(gx / 1000, gy / 1000, eg, levels=_ISO, colors="#222222", linewidths=0.6, zorder=4)
    lbls = ax.clabel(cs, levels=[1.0, 2.0, 3.0, 5.0], fmt="%g", fontsize=7,
                     colors="#111111", inline=True, inline_spacing=6)
    c1 = ax.contour(gx / 1000, gy / 1000, eg, levels=[1.0], colors=_GREEN, linewidths=1.8, zorder=5)
    lbls1 = ax.clabel(c1, fmt="%.0f lx", fontsize=7, colors=_GREEN, inline=True, inline_spacing=6)
    for t in list(lbls) + list(lbls1):
        t.set_path_effects(_halo)
    for r in korr:
        ml = np.array(mittellinie(r.polygon_mm, 250.0)) / 1000
        if len(ml) > 1:
            ax.plot(ml[:, 0], ml[:, 1], ls=(0, (4, 3)), color="#222", lw=0.7, alpha=0.6, zorder=5)
    for x, y, az in sl3:
        _leuchte_symbol(ax, x / 1000, y / 1000, az)
    ax.set_aspect("equal")
    ax.set_xlim(mnx / 1000 - 0.4, mxx / 1000 + 0.4)
    ax.set_ylim(mny / 1000 - 0.6, mxy / 1000 + 0.4)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(labelsize=7, length=3, color="#888")
    ax.set_xlabel("m", fontsize=7); ax.set_ylabel("m", fontsize=7)
    _scalebar(ax, mnx / 1000, mny / 1000 - 0.45, 2.0, "2 m")
    ax.text(mxx / 1000 + 0.4, mxy / 1000 + 0.25, "▪ Sicherheitsleuchte   — 1 lx (Norm)   · Zahlen = Isolux [lx]",
            fontsize=6.4, color="#444", ha="right")

    axp = fig.add_axes([0.115, 0.792, 0.115, 0.082], projection="polar")
    gg = np.linspace(-90, 90, 91)
    th = np.radians(gg)
    axp.set_theta_zero_location("S"); axp.set_theta_direction(-1)
    axp.set_thetamin(-90); axp.set_thetamax(90)
    axp.plot(th, [icd(abs(g), 0.0) for g in gg], color="#c0392b", lw=1.1)
    axp.plot(th, [icd(abs(g), 90.0) for g in gg], color="#2c6fbb", lw=1.1)
    axp.set_xticks([]); axp.set_yticks([])
    axp.grid(alpha=0.25, lw=0.4)
    axp.set_title("Polare LVK  (C0 rot · C90 blau)", fontsize=6, color="#444", pad=2)

    axb = fig.add_axes([0.08, 0.462, 0.45, 0.015])
    grad = np.linspace(_VMIN, _VMAX, 256).reshape(1, -1)
    axb.imshow(grad, aspect="auto", cmap=_CMAP, norm=nrm, extent=[_VMIN, _VMAX, 0, 1], origin="lower")
    axb.set_yticks([]); axb.set_xticks([0.5, 1, 2, 3, 4, 5, 6])
    axb.set_xticklabels(["0,5", "1", "2", "3", "4", "5", "6"], fontsize=6.3)
    axb.tick_params(length=2)
    axb.text(_VMAX + 0.25, 0.5, "E [lx]", va="center", fontsize=7, transform=axb.transData)

    def _area(r):
        p = np.array(r.polygon_mm) / 1000.0
        return abs(np.dot(p[:, 0], np.roll(p[:, 1], -1)) - np.dot(p[:, 1], np.roll(p[:, 0], -1))) / 2

    # Nutzebene kompakt als Aggregat-Zeile (robust bei vielen Fluchtwegen).
    ty = 0.442
    _emins = [stats(r.id)[1] for r in korr]
    _emaxs = [stats(r.id)[2] for r in korr]
    fig.text(0.08, ty, "Berechnungsergebnis · Nutzebene (Höhe 0,020 m · Randzone 0,500 m): "
             f"{len(korr)} Fluchtwege · Σ {sum(_area(r) for r in korr):.0f} m² · "
             f"Emin {min(_emins):.2f} lx · Emax {max(_emaxs):.1f} lx",
             fontsize=8.5, color=_INK)

    # EN-1838-Nachweis je Rettungsweg — offene zuerst, gedeckelt (Rest als Summe).
    rw_all = [(r, _rw_stats(r, norm, sl3, icd)) for r in korr]

    def _ok(s):
        return s["ok_mf"] and s["ok_ml"] and s["ok_ud"]

    n_ok = sum(1 for _, s in rw_all if _ok(s))
    alle = n_ok == len(rw_all)
    rw_all.sort(key=lambda rs: (_ok(rs[1]), rs[0].id))
    ny2 = 0.412
    fig.text(0.08, ny2, "Nachweis nach EN 1838 §4.2.1 · Rettungswege", fontsize=9.5,
             fontweight="bold", color=_INK)
    fig.text(0.92, ny2, "NACHWEIS ERFÜLLT" if alle else f"{n_ok}/{len(rw_all)} ERFÜLLT",
             fontsize=9, fontweight="bold", ha="right", color=(_GREEN if alle else "#b02020"))
    heads = [("Rettungsweg", 0.08, "l", ""), ("Emin\nMittelfläche", 0.36, "r", "(≥ 0,50 lx)"),
             ("Emax\nMittelfläche", 0.47, "r", ""), ("Emin\nMittellinie", 0.61, "r", "(≥ 1,00 lx)"),
             ("Emax\nMittellinie", 0.72, "r", ""), ("Ud", 0.815, "r", "(≥ 0,025)"),
             ("Index", 0.885, "c", "")]
    hy = ny2 - 0.022
    for name, x, al, soll in heads:
        fig.text(x, hy, name, fontsize=7.2, fontweight="bold", color=_NAVY, va="top",
                 ha=("right" if al == "r" else "center" if al == "c" else "left"))
        if soll:
            fig.text(x, hy - 0.028, soll, fontsize=6.2, color="#888", va="top",
                     ha=("right" if al == "r" else "left"))
    fig.add_artist(plt.Line2D([0.08, 0.92], [hy - 0.038, hy - 0.038], color="#ccc", lw=0.8))
    _maxn = 5
    for k, (r, s) in enumerate(rw_all[:_maxn]):
        yy = hy - 0.050 - k * 0.033
        fig.text(0.08, yy, r.id, fontsize=8, color=_INK)
        fig.text(0.08, yy - 0.011, "Höhe 0,000 m", fontsize=6.0, color="#888")

        def cell(x, val, ok=None, yy=yy):
            fig.text(x, yy, val, fontsize=8, color=_INK, ha="right")
            if ok is not None:
                fig.text(x, yy - 0.011, "✓" if ok else "✗", fontsize=7.5, ha="right",
                         color=(_GREEN if ok else "#b02020"))

        cell(0.36, f"{s['emin_mf']:.2f} lx", s["ok_mf"])
        cell(0.47, f"{s['emax_mf']:.1f} lx")
        cell(0.61, f"{s['emin_ml']:.2f} lx", s["ok_ml"])
        cell(0.72, f"{s['emax_ml']:.1f} lx")
        cell(0.815, f"{s['ud']:.3f}", s["ok_ud"])
        fig.text(0.885, yy, f"ER{k + 1}", fontsize=7.5, color=_NAVY, ha="center", va="center",
                 bbox={"boxstyle": "square,pad=0.3", "fc": "none", "ec": _NAVY, "lw": 0.8})
    if len(rw_all) > _maxn:
        rest = rw_all[_maxn:]
        offen = sum(1 for _, s in rest if not _ok(s))
        fig.text(0.08, hy - 0.050 - _maxn * 0.033,
                 f"… +{len(rest)} weitere Rettungswege ({offen} offen) — vollständige Liste im Prüfbericht",
                 fontsize=7, color="#777")

    sy = 0.115
    fig.text(0.08, sy, "Leuchten-Stückliste", fontsize=9, fontweight="bold", color=_INK)
    for name, x in [("Stück", 0.08), ("Bezeichnung", 0.20), ("Φ Notbetrieb", 0.62),
                    ("Rolle", 0.70), ("Montagehöhe", 0.90)]:
        fig.text(x, sy - 0.02, name, fontsize=7.6, fontweight="bold", color=_NAVY,
                 ha=("right" if x in (0.62, 0.90) else "left"))
    fig.add_artist(plt.Line2D([0.08, 0.90], [sy - 0.026, sy - 0.026], color="#ccc", lw=0.8))
    bez = f"Schrack {photo.name} · Corridor-Optik" if photo else "Sicherheitsleuchte Fluchtweg (generisch)"
    phi = f"{photo.lampen_lumen:.0f} lm" if photo else "—"
    fig.text(0.08, sy - 0.045, str(len(sl3)), fontsize=8, color=_INK)
    fig.text(0.20, sy - 0.045, bez, fontsize=8, color=_INK)
    fig.text(0.62, sy - 0.045, phi, fontsize=8, color=_INK, ha="right")
    fig.text(0.70, sy - 0.045, "SL", fontsize=8, color=_INK)
    fig.text(0.90, sy - 0.045, f"{HM:.1f} m", fontsize=8, color=_INK, ha="right")

    fig.add_artist(plt.Line2D([0.07, 0.93], [0.05, 0.05], color=_NAVY, lw=1.2))
    quelle = "echte Hersteller-Photometrie (EULUMDAT/LDT)" if (i_cd_fn or photo) else "generische Lichtstärke-Annahme"
    fig.text(0.07, 0.038, f"Berechnung: Punktmethode E = I(γ,C)·cos³θ/h² · Wartungsfaktor 0,80 · ohne Reflexion · {quelle}.",
             fontsize=6.6, color="#777")
    fig.text(0.07, 0.024, "Erstellt mit Notbeleuchtung-Engine", fontsize=7, color=_NAVY)
    fig.text(0.93, 0.024, f"Rivoplan · www.rivoplan.com    Seite {seite}", fontsize=7, color=_NAVY, ha="right")

    fig.savefig(out, facecolor="white")
    plt.close(fig)
    return out
