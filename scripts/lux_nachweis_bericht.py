"""lux_nachweis_bericht — CLI-Wrapper über den Render-Bericht.

Der eigentliche Bericht lebt in
`notbeleuchtung.hauptengine.render.lux_nachweis_bericht.schreibe_bericht` (wird von
der Pipeline je Plan aufgerufen). Dieses Skript platziert für ein RaumModell-Fixture
und ruft denselben Generator — für Demo/Vorschau.

    python scripts/lux_nachweis_bericht.py <raum_modell.json> [out.png]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "src"))
sys.path.insert(0, str(_ROOT / "tests"))

from fakes import FakeNormProvider
from notbeleuchtung.hauptengine.contracts import RaumModell
from notbeleuchtung.hauptengine.render.lux_nachweis_bericht import schreibe_bericht
from notbeleuchtung.normwissen.photometrie import lade_ldt
from notbeleuchtung.platzierung.platzierer import NotlichtPlatzierer


def main() -> None:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else _ROOT / "tests/fixtures/raum_modell_wohnbau_eg.json"
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else _ROOT / "output_lux_nachweis_bericht.png"
    raum = RaumModell.model_validate(json.loads(src.read_text(encoding="utf-8")))
    ldt = _ROOT / "CAD_Symbole" / "photometrie" / "sl_nlkbu433_3h_corridor.ldt"
    icd = lade_ldt(ldt).intensitaet if ldt.exists() else None
    norm = FakeNormProvider()
    plc = NotlichtPlatzierer(i_cd_fn=icd).place(raum, norm)
    projekt = src.stem.replace("raum_modell_", "").rsplit("_", 1)[0].replace("_", " ").title()
    print("Bericht:", schreibe_bericht(raum, plc, norm, out, i_cd_fn=icd, projekt=projekt))


if __name__ == "__main__":
    main()
