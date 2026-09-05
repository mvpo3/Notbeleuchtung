"""legende_import — Legenden-DXF einlesen und Materialwörterbuch ADDITIV pflegen.

Jede Probe (HATCH/LINE/LWPOLYLINE/ARC-Ring) bekommt den nächstgelegenen
Legendentext als Bezeichnung. Farbige Kurztexte ('C', 'TSL', 'FLW-L') sind Teil
des Symbols, keine Bezeichnungen — nur ByLayer-/Standard-farbige Texte sind
Label-Kandidaten (Farbe als Tiebreaker, TSL-Fall). Bezeichnung → Material läuft
über Bezeichnung + Aliasnamen (fnmatch); BETON ist kein eigenes Material,
sondern Alias von STAHLBETON (Signatur identisch → Warnung).

``importiere_legende`` ergänzt materialien.yaml nur additiv (neue Aliasnamen,
Signaturvarianten, Quellen — nie überschreiben) und schreibt deterministisch
sortiert (stabile Diffs, Idempotenz).

Grenze: Bauteilart/Brandschutz kennt eine Legende nicht — unbekannte Einträge
landen mit Bauteilart UNBEKANNT im Wörterbuch und brauchen manuelle Pflege.
"""
from __future__ import annotations

import json
import logging
import math
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from notbeleuchtung.wissen import DATA_DIR

from .material_matching import signatur_aus_hatch, signatur_zu_dict

log = logging.getLogger(__name__)

XY = tuple[float, float]
_STANDARD_FARBEN = (0, 7, 256)  # ByBlock / Standard / ByLayer → Label-Kandidat
_LABEL_MAX_ABSTAND = 2.0        # Symboltext → Probe (Legendeneinheiten)

_UMLAUTE = str.maketrans({"Ä": "AE", "Ö": "OE", "Ü": "UE", "ß": "SS"})


def norm_label(text: str) -> str:
    """Legendentext → Vergleichsform: Großschrift, Umlaute transliteriert."""
    t = text.strip().upper().translate(_UMLAUTE)
    t = "".join(c if c.isalnum() else " " for c in t)
    return " ".join(t.split())


@dataclass
class _Probe:
    anker: XY
    sig: dict


@dataclass
class ImportErgebnis:
    """Was der Legendenimport getan hat — Beleg für Bericht + Tests."""

    eintraege: dict[str, str] = field(default_factory=dict)  # Label → Material
    warnungen: list[str] = field(default_factory=list)
    neue_aliasnamen: int = 0
    neue_signaturen: int = 0
    neue_materialien: int = 0
    geaendert: bool = False


# ── Proben + Texte aus dem DXF ───────────────────────────────────────────────
def _hatch_anker(h) -> XY | None:
    pts: list[XY] = []
    for path in h.paths:
        for v in getattr(path, "vertices", ()) or ():
            pts.append((float(v[0]), float(v[1])))
        for edge in getattr(path, "edges", ()) or ():
            if hasattr(edge, "start"):
                pts.append((float(edge.start[0]), float(edge.start[1])))
            elif hasattr(edge, "center"):
                pts.append((float(edge.center[0]), float(edge.center[1])))
    if not pts:
        return None
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def _true_color(e) -> list[int] | None:
    tc = e.dxf.get("true_color", None)
    if tc is None:
        return None
    from ezdxf.colors import int2rgb

    return [int(c) for c in int2rgb(tc)]


def _proben(msp) -> list[_Probe]:
    proben: list[_Probe] = []
    ring_arcs: dict[XY, list] = {}
    for e in msp:
        t = e.dxftype()
        if t == "HATCH":
            anker = _hatch_anker(e)
            if anker is None:
                continue
            proben.append(_Probe(anker, signatur_zu_dict(signatur_aus_hatch(e))))
        elif t == "LINE":
            farbe = int(e.dxf.color)
            lt = str(e.dxf.linetype).upper()
            marker = (
                farbe not in _STANDARD_FARBEN
                or int(e.dxf.lineweight) >= 13
                or lt not in ("BYLAYER", "BYBLOCK", "CONTINUOUS")
            )
            if not marker:
                continue  # Rahmenlinien der Muster-Kacheln
            s, z = e.dxf.start, e.dxf.end
            mitte = ((float(s[0]) + float(z[0])) / 2, (float(s[1]) + float(z[1])) / 2)
            sig = {"typ": "linie", "farbe": farbe}
            if (tc := _true_color(e)) is not None:
                sig["true_color"] = tc
            if int(e.dxf.lineweight) > 0:
                sig["lineweight"] = int(e.dxf.lineweight)
            if lt not in ("BYLAYER", "CONTINUOUS"):
                sig["linetype"] = str(e.dxf.linetype)
            proben.append(_Probe(mitte, sig))
        elif t == "LWPOLYLINE" and e.closed and int(e.dxf.color) not in _STANDARD_FARBEN:
            pts = [(float(p[0]), float(p[1])) for p in e.get_points("xy")]
            anker = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
            sig = {"typ": "rahmen", "farbe": int(e.dxf.color), "geschlossen": True}
            if int(e.dxf.lineweight) > 0:
                sig["lineweight"] = int(e.dxf.lineweight)
            proben.append(_Probe(anker, sig))
        elif t == "ARC":
            c = (round(float(e.dxf.center[0]), 2), round(float(e.dxf.center[1]), 2))
            ring_arcs.setdefault(c, []).append(round(float(e.dxf.radius), 3))
    # ARCs am selben Zentrum → EIN Ring-Symbol (TSL: 4 ARCs, 2 Radien).
    for center, radien in sorted(ring_arcs.items()):
        proben.append(_Probe(center, {
            "typ": "symbol", "form": "ring",
            "radien": sorted(set(radien)), "anzahl_arcs": len(radien),
        }))
    return proben


def _texte(msp) -> list[tuple[str, XY, int]]:
    out = []
    for e in msp:
        t = e.dxftype()
        if t == "MTEXT":
            txt, ins = e.plain_text(), e.dxf.insert
        elif t == "TEXT":
            txt, ins = e.dxf.text, e.dxf.insert
        else:
            continue
        if txt and txt.strip():
            out.append((txt.strip(), (float(ins[0]), float(ins[1])), int(e.dxf.color)))
    return out


def _dist(a: XY, b: XY) -> float:
    return math.dist(a, b)


# ── Wörterbuch-Merge (additiv) ───────────────────────────────────────────────
def _canon(sig: dict) -> str:
    def r(x):
        if isinstance(x, float):
            return round(x, 3)
        if isinstance(x, list):
            return [r(v) for v in x]
        if isinstance(x, dict):
            return {k: r(v) for k, v in x.items() if k != "labels"}
        return x

    return json.dumps(r(sig), sort_keys=True, ensure_ascii=False)


def _passt_laenge(norm: str, mat: dict) -> int:
    """Länge des längsten (= spezifischsten) passenden Alias, -1 = kein Treffer.

    Spezifischster gewinnt: 'GIPSKARTON*EI30*' schlägt das generische 'GIPS*' —
    sonst zieht ein Glob alle drei GK-Brandschutzklassen auf ein Material.
    """
    from fnmatch import fnmatchcase

    kandidaten = [mat["bezeichnung"], *mat.get("aliasnamen", [])]
    treffer = [k for k in kandidaten if fnmatchcase(norm, k.upper().translate(_UMLAUTE))]
    return max((len(k) for k in treffer), default=-1)


def _passt(norm: str, mat: dict) -> bool:
    return _passt_laenge(norm, mat) >= 0


def _sortiert(mats: list[dict]) -> list[dict]:
    """Deterministische Ordnung für stabile Diffs."""
    out = []
    for m in sorted(mats, key=lambda m: m["bezeichnung"]):
        d = {"bezeichnung": m["bezeichnung"], "bauteilart": m["bauteilart"],
             "brandschutz": m.get("brandschutz"), "semantik": m.get("semantik"),
             "aliasnamen": sorted(set(m.get("aliasnamen", []))),
             "signaturen": sorted(m.get("signaturen", []), key=_canon),
             "quellen": sorted(set(m.get("quellen", [])))}
        out.append(d)
    return out


def importiere_legende(
    dxf_pfad: Path | str,
    projektname: str,
    yaml_pfad: Path | str | None = None,
) -> ImportErgebnis:
    """Legenden-DXF → materialien.yaml additiv ergänzen (idempotent)."""
    import ezdxf

    yaml_pfad = Path(yaml_pfad) if yaml_pfad else DATA_DIR / "materialien.yaml"
    alt_text = yaml_pfad.read_text(encoding="utf-8") if yaml_pfad.exists() else ""
    doc = yaml.safe_load(alt_text) if alt_text else None
    doc = doc or {"materialien": []}
    mats: list[dict] = doc.setdefault("materialien", [])

    msp = ezdxf.readfile(str(dxf_pfad)).modelspace()
    proben = _proben(msp)
    texte = _texte(msp)
    labels = [(t, xy) for t, xy, farbe in texte
              if farbe in _STANDARD_FARBEN and len(norm_label(t)) > 1]
    symboltexte = [(t, xy, farbe) for t, xy, farbe in texte if farbe not in _STANDARD_FARBEN]

    erg = ImportErgebnis()
    if not labels:
        erg.warnungen.append("Legende ohne Bezeichnungstexte — nichts importiert")
        return erg

    # Farbige Kurztexte ('C', 'TSL', 'FLW-L') → nächstgelegene Symbol-Probe.
    marker = [p for p in proben if p.sig["typ"] in ("linie", "symbol", "solid")]
    for st, sxy, sfarbe in symboltexte:
        if not marker:
            break
        # Farbgleichheit vor Nähe: 'TSL' (blau) gehört zur blauen Linie, auch
        # wenn die FLW-Linie näher liegt.
        p = min(marker, key=lambda p: (p.sig.get("farbe") != sfarbe, _dist(p.anker, sxy)))
        if _dist(p.anker, sxy) <= _LABEL_MAX_ABSTAND:
            p.sig.setdefault("labels", []).append(st)
    for p in marker:
        if "labels" in p.sig:
            p.sig["labels"] = sorted(p.sig["labels"])

    # Probe → nächstgelegener Bezeichnungstext.
    eintraege: dict[str, list[dict]] = {}
    for p in proben:
        label = min(labels, key=lambda lt: _dist(lt[1], p.anker))[0]
        eintraege.setdefault(norm_label(label), []).append(p.sig)

    for label, sigs in sorted(eintraege.items()):
        mat = max(mats, key=lambda m: _passt_laenge(label, m), default=None)
        if mat is not None and not _passt(label, mat):
            mat = None
        if mat is None:
            mat = {"bezeichnung": label, "bauteilart": "UNBEKANNT", "brandschutz": None,
                   "semantik": None, "aliasnamen": [], "signaturen": [], "quellen": []}
            mats.append(mat)
            erg.neue_materialien += 1
            erg.warnungen.append(
                f"Legendeneintrag {label!r} unbekannt — als UNBEKANNT aufgenommen"
            )
            log.warning("Legendeneintrag %r ohne Wörterbuch-Material — bitte pflegen", label)
        if label.startswith("BETON") and mat["bezeichnung"] == "STAHLBETON":
            erg.warnungen.append(
                "Legende führt BETON separat — Signatur identisch, als STAHLBETON behandelt"
            )
            log.warning("Legende führt BETON separat — als STAHLBETON behandelt")
        vorhandene = {_canon(s) for s in mat["signaturen"]}
        for sig in sigs:
            if _canon(sig) not in vorhandene:
                mat["signaturen"].append(sig)
                vorhandene.add(_canon(sig))
                erg.neue_signaturen += 1
        if not _passt(label, mat):  # neuer Aliasname (nicht über Glob abgedeckt)
            mat["aliasnamen"].append(label)
            erg.neue_aliasnamen += 1
        if projektname not in mat.get("quellen", []):
            mat.setdefault("quellen", []).append(projektname)
        erg.eintraege[label] = mat["bezeichnung"]

    neu_text = yaml.safe_dump(
        {"materialien": _sortiert(mats)},
        allow_unicode=True, sort_keys=False, width=100,
    )
    if neu_text != alt_text:
        yaml_pfad.write_text(neu_text, encoding="utf-8")
        erg.geaendert = True
    return erg
