"""Am-Rain-Extraktion: je DXF ein JSON-Dump der Notbeleuchtungs-Substanz."""
import json
import sys
from collections import Counter
from pathlib import Path

import ezdxf

SRC = Path("DIN-Notbeleuchtungspläne(Beispiele)/Am Rain Notbeleuchtungspläne")
OUT = Path("scratchpad/am_rain")
OUT.mkdir(parents=True, exist_ok=True)

NOTLICHT_HINT = ("sibel", "notbel", "notlicht", "flucht", "rettung", "emergency", "sicherheits")


def extrahiere(pfad: Path) -> dict:
    doc = ezdxf.readfile(pfad)
    ms = doc.modelspace()
    layer_alle = sorted(la.dxf.name for la in doc.layers)
    layer_not = [n for n in layer_alle if any(h in n.lower() for h in NOTLICHT_HINT)]

    inserts, texte_not, texte_rot = [], [], []
    block_counter = Counter()
    for e in ms:
        try:
            typ = e.dxftype()
            layer = e.dxf.layer or ""
            ist_not = any(h in layer.lower() for h in NOTLICHT_HINT)
            if typ == "INSERT":
                name = e.dxf.name
                if ist_not or any(h in name.lower() for h in NOTLICHT_HINT):
                    inserts.append({
                        "name": name, "layer": layer,
                        "x": round(e.dxf.insert.x, 1), "y": round(e.dxf.insert.y, 1),
                        "rot": round(e.dxf.rotation, 1),
                        "xscale": round(e.dxf.xscale, 3),
                    })
                    block_counter[name] += 1
            elif typ in ("TEXT", "MTEXT"):
                txt = (e.dxf.text if typ == "TEXT" else e.text).strip()
                if not txt:
                    continue
                x, y = round(e.dxf.insert.x, 1), round(e.dxf.insert.y, 1)
                eintrag = {"text": txt[:160], "layer": layer, "x": x, "y": y}
                if ist_not:
                    texte_not.append(eintrag)
                if e.dxf.get("color", 256) == 1 or "rot" in layer.lower():
                    texte_rot.append(eintrag)
        except (AttributeError, ezdxf.DXFError, UnicodeDecodeError):
            continue                       # kaputte Einzel-Entity: Analyse-Tool, skip

    # Blockdefinitionen der Notlicht-Blöcke: Entity-Arten (für Basis-/Symbolik-Fragen)
    blockdefs = {}
    for bname in list(block_counter):
        try:
            blk = doc.blocks.get(bname)
            arten = Counter(x.dxftype() for x in blk)
            blockdefs[bname] = dict(arten)
        except (KeyError, AttributeError, ezdxf.DXFError):
            pass                           # Blockdef fehlt/defekt: Zählung reicht

    ext = None
    try:
        ext = [round(v, 0) for v in (*doc.header["$EXTMIN"][:2], *doc.header["$EXTMAX"][:2])]
    except (KeyError, TypeError):
        ext = None                         # Header ohne Extents: bewusst leer

    return {
        "datei": pfad.name,
        "insunits": doc.header.get("$INSUNITS", None),
        "extents": ext,
        "layer_notlicht": layer_not,
        "n_layer_gesamt": len(layer_alle),
        "bloecke_zaehlung": dict(block_counter.most_common()),
        "blockdefs": blockdefs,
        "inserts": inserts,
        "texte_notlicht_layer": texte_not[:200],
        "texte_rot": texte_rot[:200],
        "layouts": [lo.name for lo in doc.layouts],
    }


if __name__ == "__main__":
    dateien = sorted(SRC.glob("*.dxf"))
    if len(sys.argv) > 1:
        dateien = [d for d in dateien if sys.argv[1] in d.name]
    for d in dateien:
        print("==", d.name, flush=True)
        data = extrahiere(d)
        kurz = d.stem.split("_MOP_")[1].split("_")[0]   # EG/OG1/…/UG
        (OUT / f"{kurz}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        print("   ->", kurz, "inserts:", len(data["inserts"]),
              "layer:", data["layer_notlicht"], flush=True)
