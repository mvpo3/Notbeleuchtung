"""abgleich_kennungen.py — ordnet DXF-Kennungs-Texte (A), (B), … den nächsten
Leuchten zu (je Projekt/Geschoss) und reichert das Seitenprotokoll mit
dxf_abgleich-Handles an.

Läuft NACH den Analyse-Batches:
1. je evidenz/<P>/<Datei>.json: kennungen (Regex ^\\(?[A-Z]\\)?$ u.ä.) → nächste
   Leuchte (euklidisch, Cap 3 m) → kennung_map.
2. seitenprotokoll.jsonl: Records mit geschoss + elemente.leuchten[].kennung
   bekommen dxf_abgleich.handles aus der Map (befund bleibt Agenten-/Skript-Sache).

Aufruf: python abgleich_kennungen.py [Projekt …]
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

HIER = Path(__file__).resolve()
BASIS = HIER.parents[1]

_KENNUNG_RE = re.compile(r"^\(?([A-Z]{1,2}\d?)\)?$")
_MAX_DIST_MM = 3000.0


def kennung_map(evidenz: dict) -> dict[str, dict]:
    """Kennungs-Text → {handle, block, dist_mm} der nächsten Leuchte."""
    out: dict[str, dict] = {}
    leuchten = [l for l in evidenz.get("leuchten", []) if l.get("xy_mm")]
    for k in evidenz.get("kennungen", []):
        m = _KENNUNG_RE.match(k.get("text", "").strip())
        if not m or not k.get("xy_mm"):
            continue
        key = m.group(1)
        best, bd = None, _MAX_DIST_MM
        for l in leuchten:
            d = math.dist(k["xy_mm"], l["xy_mm"])
            if d < bd:
                best, bd = l, d
        if best is None:
            continue
        eintrag = {"handle": best["handle"], "block": best["block"],
                   "dist_mm": round(bd, 0), "kennung_handle": k["handle"]}
        # bei Mehrfach-Kennung (gleicher Buchstabe mehrfach je Geschoss) Liste führen
        out.setdefault(key, []).append(eintrag) if isinstance(out.get(key), list) else None
        if key not in out:
            out[key] = [eintrag]
        elif eintrag not in out[key]:
            out[key].append(eintrag)
    return out


def main(argv: list[str]) -> int:
    projekte = argv or [p.name for p in (BASIS / "evidenz").iterdir() if p.is_dir()]
    for projekt in projekte:
        ev_dir = BASIS / "evidenz" / projekt
        maps: dict[str, dict] = {}          # geschoss → kennung_map
        for j in sorted(ev_dir.glob("*.json")):
            if j.name in ("inventur.json",):
                continue
            daten = json.loads(j.read_text(encoding="utf-8"))
            if "geschoss" not in daten:
                continue
            maps[daten["geschoss"]] = kennung_map(daten)
        (ev_dir / "kennung_map.json").write_text(
            json.dumps(maps, ensure_ascii=False, indent=1), encoding="utf-8")

        jl = ev_dir / "seitenprotokoll.jsonl"
        if not jl.exists():
            print(f"[{projekt}] kennung_map ({sum(len(m) for m in maps.values())} Kennungen), "
                  f"kein Protokoll — nur Map geschrieben")
            continue
        records = [json.loads(z) for z in jl.read_text(encoding="utf-8").splitlines() if z.strip()]
        n_angereichert = 0
        for r in records:
            g = r.get("geschoss")
            if not g or g not in maps:
                continue
            handles: list[str] = []
            for le in (r.get("elemente") or {}).get("leuchten", []) or []:
                m = _KENNUNG_RE.match(str(le.get("kennung", "")).strip("() "))
                if m and m.group(1) in maps[g]:
                    for e in maps[g][m.group(1)]:
                        if e["handle"] not in handles:
                            handles.append(e["handle"])
            if handles:
                ab = r.setdefault("dxf_abgleich", {})
                ab.setdefault("datei", "")
                ab["handles"] = handles
                n_angereichert += 1
        jl.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records),
                      encoding="utf-8")
        print(f"[{projekt}] {len(records)} Records, {n_angereichert} mit Handles angereichert")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
