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

# Wasserscheide-Doppelpfeil für richtung="gerade": ein beidseitiger RZ steht in der
# Flur-Mitte zwischen zwei Ausgängen und weist in BEIDE Richtungen (Profi-Plan
# RZ_PLPR, Referenz PROFI_DIN_PLAN_UND_VORSCHRIFTEN.md §1.1). Gerendert als zwei
# horizontale Richtungspfeil-Blocks (links + rechts), gemeinsam um `rotation_deg`
# gedreht — kein Contract-Feld, rein Render-seitig aus `richtung` abgeleitet.
_DOPPELPFEIL_KEYS = ("notlicht_ks_stiege_links", "notlicht_ks_stiege_rechts")


def _ensure_appid(output_doc: Drawing) -> None:
    if _APPID not in output_doc.appids:
        output_doc.appids.add(_APPID)


def _skalen(entry: dict, p: Platzierung) -> tuple[float, float]:
    """(yscale, xscale) aus Mapping-Eintrag + Contract — Faktor/scale_abs + Spiegelung.

    Effektive Spiegelung = Mapping-`mirror_x` XOR Contract-`mirror_x` (das Mapping
    spiegelt z.B. den 'nach links'-Block für die rechts-Variante, der Platzierer
    spiegelt zusätzlich je Fluchtweg-Geometrie).
    """
    if "scale_abs" in entry:
        scale = float(entry["scale_abs"])
    else:
        scale = DE_GLOBAL_SCALE * float(entry.get("scale", 1.0))
    mirrored = bool(entry.get("mirror_x", False)) ^ bool(p.mirror_x)
    return scale, (-scale if mirrored else scale)


def _insert_block(
    output_doc: Drawing,
    block_name: str,
    xy: tuple[float, float],
    rotation: float,
    xscale: float,
    yscale: float,
    layer: str,
) -> Insert:
    """Einen Library-Block als INSERT setzen (Sync + Import + Blockref)."""
    library.sync_layers(output_doc)
    library.import_block(output_doc, block_name)
    return output_doc.modelspace().add_blockref(
        block_name,
        xy,
        dxfattribs={
            "layer": layer,
            "rotation": rotation,
            "xscale": xscale,
            "yscale": yscale,
        },
    )


def insert_platzierung(
    output_doc: Drawing,
    p: Platzierung,
    layer: str = library.SAFETY_LAYER,
) -> Insert:
    """Eine Platzierung als Schrack-INSERT in die Modelspace setzen.

    Output ist mm-Welt; `p.xy_mm` wird 1:1 geschrieben. Rotationen kommen
    unverändert aus dem Contract (359.7° etc. werden NICHT normalisiert). Bei einem
    **Rettungszeichen** mit `richtung="gerade"` wird statt eines Einzelpfeils ein
    **beidseitiger Doppelpfeil** (links+rechts, Wasserscheide) gezeichnet;
    zurückgegeben wird der primäre (linke) Insert, der auch den Stromkreis-XDATA-Tag
    trägt. Andere Leuchtenarten mit `richtung="gerade"` (Sicherheitsleuchte,
    Antipanik = „keine Richtung") behalten ihr eigenes Katalog-Symbol.

    Raises
    ------
    KeyError
        catalog_key nicht im Mapping — per Naht-Invariante ein Bug, kein
        Fallback.
    """
    mapping = library.load_mapping()
    if p.catalog_key not in mapping:
        raise KeyError(f"No Schrack mapping for catalog_key {p.catalog_key!r}")

    # Doppelpfeil NUR für Rettungszeichen-Wasserscheiden. Sicherheitsleuchten und
    # Antipanik tragen ebenfalls richtung="gerade" (= keine Richtung), sind aber keine
    # Pfeil-Zeichen → sie behalten ihr eigenes Katalog-Symbol.
    if p.richtung == "gerade" and p.kind == "rz":
        insert = _insert_doppelpfeil(output_doc, p, mapping, layer)
    else:
        entry = mapping[p.catalog_key]
        yscale, xscale = _skalen(entry, p)
        insert = _insert_block(
            output_doc, entry["block_name"], p.xy_mm, p.rotation_deg, xscale, yscale, layer
        )

    if p.circuit_hint:
        _ensure_appid(output_doc)
        insert.set_xdata(_APPID, [(1000, f"stromkreis={p.circuit_hint}")])

    return insert


def _insert_doppelpfeil(
    output_doc: Drawing, p: Platzierung, mapping: dict, layer: str
) -> Insert:
    """Beidseitiger RZ: horizontaler Links- + Rechts-Pfeil am selben Punkt.

    Beide Pfeile teilen `p.xy_mm` und `p.rotation_deg` (die Fluchtweg-Achse) und
    zeigen so entlang derselben Achse in Gegenrichtung. Zurück kommt der linke
    (primäre) Insert.
    """
    primary: Insert | None = None
    for key in _DOPPELPFEIL_KEYS:
        entry = mapping[key]
        yscale, xscale = _skalen(entry, p)
        insert = _insert_block(
            output_doc, entry["block_name"], p.xy_mm, p.rotation_deg, xscale, yscale, layer
        )
        if primary is None:
            primary = insert
    assert primary is not None  # _DOPPELPFEIL_KEYS ist nie leer
    return primary
