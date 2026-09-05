"""material_matching — HATCH-Signatur + Kontext → Material aus dem Wörterbuch.

Prinzip: das Erscheinungsbild ist die Wahrheit. Musternamen sind unzuverlässig
(FP_822 trägt drei Materialien, nur die Füllfarbe unterscheidet; Rennweg nutzt
ganz andere Namen ohne Füllfarbe) — gematcht wird gewichtet über
Musterlinien-Geometrie (50 %), Füllfarbe (25 %), Aliasname (15 %) und
Layer-Hinweis (10 %). Ein EXAKTER Alias-Treffer (Name steht wörtlich im
Wörterbuch, kein Glob) setzt einen Score-Boden: der Name ist dann selbst
Wörterbuch-Wissen und schlägt eine abweichende Geometrie (Rennweg-INSULATION).

Abstände werden RELATIV bewertet (zueinander), nie absolut — Mollgasse zeichnet
in Metern (Skalen 0.005–0.05), Rennweg in mm.

Grenze: matcht nur hatch-/solid-Signaturen. Linien-/Symbol-Signaturen
(Brandabschnitt, FLW, TSL, Schacht-Rahmen) erkennt eine eigene Marker-Spur.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field, replace
from fnmatch import fnmatchcase
from functools import lru_cache

from notbeleuchtung.wissen import Material, lade_materialien

RGB = tuple[int, int, int]

#: Unter diesem Score wird kein Material behauptet → 'UNBEKANNT'.
SCHWELLE = 0.45
#: Score-Boden bei exaktem (glob-freiem) Alias-Treffer.
_ALIAS_BODEN = 0.70
_WINKEL_TOL = 3.0
_ABSTAND_TOL = 0.15


@dataclass(frozen=True)
class MusterLinie:
    """Eine Definitionslinie eines Hatch-Musters (Winkel °, Offset-Betrag)."""

    winkel: float
    abstand: float
    dashes: tuple[float, ...] = ()

    @property
    def ist_solid(self) -> bool:
        # [100, 0] (Dash ohne Lücke) ist faktisch durchgezogen.
        return not any(d < 0 for d in self.dashes)


@dataclass(frozen=True)
class HatchSignatur:
    """Erscheinungsbild eines HATCH — alles, was fürs Matching zählt."""

    pattern_name: str = ""
    bgcolor: RGB | None = None
    farbe: int | None = None
    true_color: RGB | None = None
    linien: tuple[MusterLinie, ...] = ()
    skala: float = 1.0


@dataclass(frozen=True)
class Treffer:
    """Match-Ergebnis: Material-Bezeichnung (oder 'UNBEKANNT') + Beleg."""

    material: str
    score: float
    begruendung: str
    signatur: HatchSignatur
    layer: str = ""


def signatur_aus_hatch(hatch, skala: float = 1.0) -> HatchSignatur:
    """ezdxf-HATCH → HatchSignatur (auch für Hatches in Blockdefinitionen).

    ``skala``: Insert-/Kontext-Skala; Abstände bleiben roh, die Skala steht
    daneben — verglichen wird ohnehin relativ.
    """
    from ezdxf.colors import int2rgb

    tc = hatch.dxf.get("true_color", None)
    bg = hatch.bgcolor
    linien = tuple(
        MusterLinie(
            winkel=round(float(ln.angle), 3),
            abstand=round(math.hypot(float(ln.offset[0]), float(ln.offset[1])), 3),
            dashes=tuple(round(float(d), 3) for d in ln.dash_length_items),
        )
        for ln in (hatch.pattern.lines if hatch.pattern else [])
    )
    return HatchSignatur(
        pattern_name=str(hatch.dxf.pattern_name),
        bgcolor=tuple(int(c) for c in bg) if bg is not None else None,
        farbe=int(hatch.dxf.color),
        true_color=tuple(int2rgb(tc)) if tc is not None else None,
        linien=linien,
        skala=float(hatch.dxf.pattern_scale) * skala,
    )


def signatur_aus_dict(d: dict) -> HatchSignatur:
    """YAML-Signatur-Dict (typ hatch/solid) → HatchSignatur."""
    return HatchSignatur(
        pattern_name=str(d.get("pattern_name", "")),
        bgcolor=tuple(d["bgcolor"]) if d.get("bgcolor") else None,
        farbe=d.get("farbe"),
        true_color=tuple(d["true_color"]) if d.get("true_color") else None,
        linien=tuple(
            MusterLinie(
                winkel=float(ln["winkel"]),
                abstand=float(ln["abstand"]),
                dashes=tuple(float(x) for x in ln.get("dashes", ())),
            )
            for ln in d.get("linien", ())
        ),
        skala=float(d.get("skala", 1.0)),
    )


def signatur_zu_dict(sig: HatchSignatur, typ: str = "hatch") -> dict:
    """HatchSignatur → YAML-taugliches Dict (deterministische Feldordnung)."""
    d: dict = {"typ": "solid" if not sig.linien and sig.pattern_name.upper() == "SOLID" else typ}
    if sig.pattern_name:
        d["pattern_name"] = sig.pattern_name
    if sig.farbe is not None and sig.farbe != 256:
        d["farbe"] = sig.farbe
    if sig.true_color is not None:
        d["true_color"] = list(sig.true_color)
    if sig.bgcolor is not None:
        d["bgcolor"] = list(sig.bgcolor)
    if sig.linien:
        d["linien"] = [
            {"winkel": ln.winkel, "abstand": ln.abstand, "dashes": list(ln.dashes)}
            for ln in sig.linien
        ]
    return d


# ── Geometrie ────────────────────────────────────────────────────────────────
def _winkel_mod180(w: float) -> float:
    return round(w % 180.0, 1)


def struktur_klasse(sig: HatchSignatur) -> str:
    """Strukturklasse: solid | einfach | kreuz | paar_sd | welle."""
    if not sig.linien:
        return "solid"
    winkel = {_winkel_mod180(ln.winkel) for ln in sig.linien}
    solid = [ln for ln in sig.linien if ln.ist_solid]
    dashed = [ln for ln in sig.linien if not ln.ist_solid]
    if len(sig.linien) >= 6 and dashed:
        return "welle"  # viele gestrichelte Def-Lines (FP_824-Welle, EPS)
    if len(winkel) >= 2:
        return "kreuz"
    if solid and dashed:
        return "paar_sd"  # solid+dashed-Paar in einer Richtung (FP_825-Familie)
    return "einfach"


def _winkel_score(a: HatchSignatur, b: HatchSignatur) -> float:
    wa = {_winkel_mod180(ln.winkel) for ln in a.linien}
    wb = {_winkel_mod180(ln.winkel) for ln in b.linien}
    if not wa or not wb:
        return 0.0
    treffer = sum(1 for w in wa if any(abs(w - v) <= _WINKEL_TOL for v in wb))
    return treffer / max(len(wa), len(wb))


def _abstand_score(a: HatchSignatur, b: HatchSignatur) -> float:
    """Abstände RELATIV zueinander (skalenfrei): Verhältnis-Vektoren vergleichen."""
    da = sorted(ln.abstand for ln in a.linien if ln.abstand > 0)
    db = sorted(ln.abstand for ln in b.linien if ln.abstand > 0)
    if not da or not db:
        return 0.0
    ra = [x / da[0] for x in da]
    rb = [x / db[0] for x in db]
    if len({round(r, 2) for r in ra}) == 1 and len({round(r, 2) for r in rb}) == 1:
        return 1.0  # beidseitig äquidistant — skalenfrei identisch
    if len(ra) != len(rb):
        return 0.1
    ok = all(abs(x - y) <= _ABSTAND_TOL * max(x, y) for x, y in zip(ra, rb))
    return 1.0 if ok else 0.2


def _geo_score(a: HatchSignatur, b: HatchSignatur) -> float:
    ka, kb = struktur_klasse(a), struktur_klasse(b)
    if ka == "solid" or kb == "solid":
        return 0.4 if ka == kb else 0.0
    struktur = 1.0 if ka == kb else 0.4
    return struktur * (0.4 + 0.3 * _winkel_score(a, b) + 0.3 * _abstand_score(a, b))


# ── Farbe ────────────────────────────────────────────────────────────────────
def _rgb_dist(a: RGB, b: RGB) -> float:
    return math.dist(a, b)


def _farbe_score(sig: HatchSignatur, msigs: list[HatchSignatur]) -> tuple[float, str]:
    """(Score, Modus). Modus 'fehlt' = beidseitig keine Füllfarbe → Gewicht umlegen."""
    if not sig.linien:  # SOLID: die Flächenfarbe IST die Signatur
        eff = sig.true_color or sig.farbe
        beste = 0.0
        for m in msigs:
            if m.linien:
                continue
            meff = m.true_color or m.farbe
            if isinstance(eff, tuple) and isinstance(meff, tuple):
                beste = max(beste, max(0.0, 1.0 - _rgb_dist(eff, meff) / 150.0))
            elif eff is not None and eff == meff:
                beste = 1.0
        return beste, "echt"
    m_bgs = [m.bgcolor for m in msigs if m.bgcolor is not None]
    if sig.bgcolor is None and not m_bgs:
        return 0.0, "fehlt"
    if sig.bgcolor is None or not m_bgs:
        return 0.5, "neutral"
    beste = max(max(0.0, 1.0 - _rgb_dist(sig.bgcolor, bg) / 150.0) for bg in m_bgs)
    return beste, "echt"


# ── Alias + Layer ────────────────────────────────────────────────────────────
def _alias_score(name: str, mat: Material) -> tuple[float, bool, str]:
    """(Score, exakt?, getroffener Alias). fnmatch case-insensitiv."""
    n = name.upper()
    if not n:
        return 0.0, False, ""
    for alias in (mat.bezeichnung, *mat.aliasnamen):
        a = alias.upper()
        if not any(c in a for c in "*?[") and a == n:
            return 1.0, True, alias
    for alias in (mat.bezeichnung, *mat.aliasnamen):
        if fnmatchcase(n, alias.upper()):
            return 1.0, False, alias
    return 0.0, False, ""


_LAYER_HINWEISE: tuple[tuple[re.Pattern, str], ...] = (
    (re.compile(r"\bSTB\b|STAHLBETON|WAND[ _-]?AUSSEN|AUSSENWAND|TRAGEND", re.IGNORECASE),
     "STAHLBETON"),
    (re.compile(r"\bGK\b|GIPS", re.IGNORECASE), "GIPSKARTON"),
    (re.compile(r"SCHACHT", re.IGNORECASE), "SCHACHT"),
    (re.compile(r"D[ÄA]MM|DAEMM|ISOL", re.IGNORECASE), "WAERMEDAEMMUNG"),
    (re.compile(r"ZIEGEL", re.IGNORECASE), "ZIEGELMAUERWERK"),
)


def _layer_score(layer: str, mat: Material) -> float:
    for rx, ziel in _LAYER_HINWEISE:
        if rx.search(layer) and mat.bezeichnung.startswith(ziel):
            return 1.0
    return 0.0


# ── Matching ─────────────────────────────────────────────────────────────────
@lru_cache(maxsize=1)
def _default_materialien() -> tuple[Material, ...]:
    return tuple(lade_materialien())


def bestimme_material(
    hatch_signatur: HatchSignatur,
    layer: str = "",
    kontext_skala: float = 1.0,
    materialien: tuple[Material, ...] | None = None,
) -> Treffer:
    """Signatur + Layer-Kontext → bester Wörterbuch-Treffer oder 'UNBEKANNT'."""
    sig = replace(hatch_signatur, skala=hatch_signatur.skala * kontext_skala)
    mats = materialien if materialien is not None else _default_materialien()
    bester: Treffer | None = None
    for mat in mats:
        msigs = [
            signatur_aus_dict(s)
            for s in mat.signaturen
            if s.get("typ") in ("hatch", "solid")
        ]
        geo = max((_geo_score(sig, m) for m in msigs), default=0.0)
        farbe, modus = _farbe_score(sig, msigs) if msigs else (0.0, "fehlt")
        alias, exakt, alias_name = _alias_score(sig.pattern_name, mat)
        lay = _layer_score(layer, mat)
        if modus == "fehlt":
            score = 0.60 * geo + 0.30 * alias + 0.10 * lay
        else:
            score = 0.50 * geo + 0.25 * farbe + 0.15 * alias + 0.10 * lay
        if exakt:
            score = max(score, _ALIAS_BODEN)
        teile = [f"Geometrie {geo:.2f}", f"Farbe {modus if modus != 'echt' else f'{farbe:.2f}'}"]
        if alias:
            teile.append(f"Alias '{alias_name}'" + (" exakt" if exakt else ""))
        if lay:
            teile.append(f"Layer-Hinweis '{layer}'")
        t = Treffer(mat.bezeichnung, round(score, 4), ", ".join(teile), sig, layer)
        if bester is None or t.score > bester.score:
            bester = t
    if bester is None or bester.score < SCHWELLE:
        sc = bester.score if bester else 0.0
        return Treffer(
            "UNBEKANNT", sc,
            f"kein Material über Schwelle {SCHWELLE} (bester Kandidat: "
            f"{bester.material if bester else '—'} {sc:.2f})",
            sig, layer,
        )
    return bester


@dataclass
class MatchSammlung:
    """Sammelt Treffer eines Plan-Durchlaufs; ``unbekannte()`` für den Kachel-Export."""

    materialien: tuple[Material, ...] | None = None
    treffer: list[Treffer] = field(default_factory=list)

    def bestimme(
        self, sig: HatchSignatur, layer: str = "", kontext_skala: float = 1.0
    ) -> Treffer:
        t = bestimme_material(sig, layer, kontext_skala, self.materialien)
        self.treffer.append(t)
        return t

    def unbekannte(self) -> list[Treffer]:
        return [t for t in self.treffer if t.material == "UNBEKANNT"]
