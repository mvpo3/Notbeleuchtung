"""Block-/Layer-Inventur ueber alle Erklaer-DXFs der 5 Referenzprojekte.

Liest jede DXF NUR lesend, zaehlt INSERT-Blocknamen (mit Layer), Layer-Belegung
und Farbverteilung, und schreibt evidenz/inventur.json + Konsolen-Summary.
Grundlage fuer SYMBOLE_UND_LAYER.md und die Alias-Tabelle der Leuchten-Bloecke.
"""
from __future__ import annotations

import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

import ezdxf

WISSEN = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parents[1] / "evidenz"

PROJEKTE = {
    "Mollgasse": {
        "ordner": "Mollgasse-Notbeleuchtungserklärung",
        "muster": r"^WHA_MOL_.+_Notbeleuchtung_Erklärung\.dxf$",
    },
    "Tomaschek": {
        "ordner": "Tomaschek-Schule -Notbeleuchtungserklärung",
        "muster": r"^.+_RIVO_Erklaerung\.dxf$",
    },
    "AmRain": {
        "ordner": "Am Rain Notbeleuchtungserklärung",
        "muster": r"^ARAI5_FE_XEL_ZZ_MOP_.+_TEILSTAND_v2\.dxf$",
    },
    "Hausfeld": {
        "ordner": "Hausfeldstraße Notbeleuchtung zeichnen",
        "muster": r"^Hausfeldstraße_.+_Notbeleuchtung_RIVO\.dxf$",
    },
    "BaufeldE2": {
        "ordner": "Baufeld E2 Notbeleuchtung zeichnen",
        "muster": r"^Notbeleuchtungspläne_UG_RIVO_mit_Lehrlayern\.dxf$",
    },
}

# Kandidaten-Hinweise fuer Leuchten-/Lehr-Inhalte (nur Heuristik fuers Summary)
LEUCHTEN_HINT = re.compile(r"rivo|sibel|arr|notbel|antipanik|aufheller|flucht", re.IGNORECASE)
PERSON_HINT = re.compile(r"person|mensch|lehrperson", re.IGNORECASE)


def inventarisiere(pfad: Path) -> dict:
    t0 = time.time()
    doc = ezdxf.readfile(str(pfad))
    msp = doc.modelspace()
    bloecke: Counter[tuple[str, str]] = Counter()  # (blockname, layer)
    layer: Counter[str] = Counter()
    farben_je_layer: dict[str, Counter] = {}
    typen: Counter[str] = Counter()
    for e in msp:
        lay = e.dxf.layer
        layer[lay] += 1
        typen[e.dxftype()] += 1
        farbe = getattr(e.dxf, "color", 256)
        tc = getattr(e.dxf, "true_color", None)
        key = f"tc:{tc:06x}" if tc is not None else f"aci:{farbe}"
        farben_je_layer.setdefault(lay, Counter())[key] += 1
        if e.dxftype() == "INSERT":
            bloecke[(e.dxf.name, lay)] += 1
    return {
        "datei": str(pfad.relative_to(WISSEN)),
        "groesse_mb": round(pfad.stat().st_size / 1e6, 1),
        "insunits": doc.header.get("$INSUNITS", None),
        "n_entities": sum(typen.values()),
        "entity_typen": dict(typen.most_common()),
        "bloecke": [
            {"block": b, "layer": l, "n": n} for (b, l), n in bloecke.most_common()
        ],
        "layer": dict(layer.most_common()),
        "farben_je_layer": {
            l: dict(c.most_common(6)) for l, c in farben_je_layer.items()
        },
        "dauer_s": round(time.time() - t0, 1),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ergebnis: dict[str, list] = {}
    protokoll: list[str] = []
    for projekt, cfg in PROJEKTE.items():
        ordner = WISSEN / cfg["ordner"]
        if not ordner.is_dir():
            protokoll.append(f"FEHLT: Ordner {ordner}")
            continue
        dateien = sorted(
            p for p in ordner.iterdir()
            if p.is_file() and re.match(cfg["muster"], p.name)
        )
        if not dateien:
            protokoll.append(f"FEHLT: keine DXF nach Muster in {ordner}")
        ergebnis[projekt] = []
        for p in dateien:
            try:
                inv = inventarisiere(p)
                ergebnis[projekt].append(inv)
                print(f"[{projekt}] {p.name}: {inv['n_entities']} Entities, "
                      f"{len(inv['bloecke'])} Blockarten, {inv['dauer_s']}s",
                      flush=True)
            except Exception as exc:  # noqa: BLE001 — Protokoll statt Abbruch
                protokoll.append(f"FEHLER {p.name}: {exc}")
                print(f"[{projekt}] FEHLER {p.name}: {exc}", flush=True)

    (OUT / "inventur.json").write_text(
        json.dumps({"projekte": ergebnis, "protokoll": protokoll},
                   ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    # Kompakt-Summary: Leuchten-/Personen-Kandidaten je Projekt
    print("\n===== KANDIDATEN =====")
    for projekt, invs in ergebnis.items():
        alle: Counter[str] = Counter()
        for inv in invs:
            for b in inv["bloecke"]:
                alle[b["block"]] += b["n"]
        leuchten = {b: n for b, n in alle.items() if LEUCHTEN_HINT.search(b)}
        personen = {b: n for b, n in alle.items() if PERSON_HINT.search(b)}
        print(f"\n[{projekt}] {len(invs)} DXFs")
        print(f"  Leuchten-Kandidaten: {leuchten}")
        print(f"  Personen-Kandidaten: {personen}")
    if protokoll:
        print("\n===== PROTOKOLL =====")
        for z in protokoll:
            print(" ", z)


if __name__ == "__main__":
    sys.exit(main())
