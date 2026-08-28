"""inserter.py — Contract-B-Platzierung → INSERT im Output-DXF.

Portiert aus elektro-planer backend/symbols/schrack_inserter.py, generativ
statt faithful (siehe docs/PORT_LOG.md): keine Catalog-Key-Aliases, keine
Notlicht-Variant-Heuristik (Leonis emittiert finale catalog_keys, die
Naht-Invariante garantiert sie im Mapping), keine Verteiler-Farben, kein
Marker-Fallback. Behalten: DE_GLOBAL_SCALE, scale/scale_abs, Spiegelung via
negativem xscale, XDATA-Stromkreis-Tag.
"""
from __future__ import annotations

from ezdxf.document import Drawing
from ezdxf.entities import Insert

from notbeleuchtung.hauptengine.contracts import Platzierung
from notbeleuchtung.symbols import library

_APPID = "NOTBELEUCHTUNG"

# elektro-planer Slice 18.64.0 (Scale-Spike): die German-Lib zeichnet Symbole
# bei ~1-5 native units; dieser globale Faktor hebt sie ins produktions-
# erprobte ~200-450-mm-Band. Zwei unabhängige Anker (~183/~190) → 185,
# kalibriert gegen die MOL_GR-Referenz-PDF. Ausreißer-Blöcke tragen
# per-Entry `scale_abs` und umgehen den Faktor.
DE_GLOBAL_SCALE = 185.0


def _ensure_appid(output_doc: Drawing) -> None:
    if _APPID not in output_doc.appids:
        output_doc.appids.add(_APPID)


def insert_platzierung(
    output_doc: Drawing,
    p: Platzierung,
    layer: str = library.SAFETY_LAYER,
) -> Insert:
    """Eine Platzierung als Schrack-INSERT in die Modelspace setzen.

    Output ist mm-Welt; `p.xy_mm` wird 1:1 geschrieben. Effektive Spiegelung =
    Mapping-`mirror_x` XOR Contract-`mirror_x` (das Mapping spiegelt z.B. den
    'nach links'-Block für die rechts-Variante, der Platzierer spiegelt
    zusätzlich je Fluchtweg-Geometrie). Rotationen kommen unverändert aus dem
    Contract (359.7° etc. werden NICHT normalisiert).

    Raises
    ------
    KeyError
        catalog_key nicht im Mapping — per Naht-Invariante ein Bug, kein
        Fallback.
    """
    mapping = library.load_mapping()
    if p.catalog_key not in mapping:
        raise KeyError(f"No Schrack mapping for catalog_key {p.catalog_key!r}")
    entry = mapping[p.catalog_key]
    block_name = entry["block_name"]

    if "scale_abs" in entry:
        scale = float(entry["scale_abs"])
    else:
        scale = DE_GLOBAL_SCALE * float(entry.get("scale", 1.0))
    mirrored = bool(entry.get("mirror_x", False)) ^ bool(p.mirror_x)
    xscale = -scale if mirrored else scale

    library.sync_layers(output_doc)
    library.import_block(output_doc, block_name)

    insert = output_doc.modelspace().add_blockref(
        block_name,
        p.xy_mm,
        dxfattribs={
            "layer": layer,
            "rotation": p.rotation_deg,
            "xscale": xscale,
            "yscale": scale,
        },
    )

    if p.circuit_hint:
        _ensure_appid(output_doc)
        insert.set_xdata(_APPID, [(1000, f"stromkreis={p.circuit_hint}")])

    return insert
