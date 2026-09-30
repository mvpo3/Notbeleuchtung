"""Ein Erkennungslauf als Messobjekt — Modell, Plan und Kaskade in einem Griff.

Das ``RaumModell`` führt keine Wandkörper; das Gate misst aber gegen die
physischen Wandkörper. Beide kommen aus demselben Lauf: ``provider.parse``
wird einmal gestartet, ``lade_dxf`` und ``raeume_aus_kaskade`` sind währenddessen
kurz umgehängt und reichen ihr Ergebnis nur durch (dasselbe Muster wie
``scripts/analyse/raumerkennung_darstellung.py::_erkennen``). Nichts an der
Erkennung wird verändert, nichts gerendert.
"""
from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Lauf:
    """Ergebnis eines Erkennungslaufs samt Eingabe-Fingerabdruck."""

    dxf: Path
    sha256: str
    modell: Any            # RaumModell
    plan: Any              # DxfPlan (trägt u.a. `factor`)
    kaskade: Any | None    # KaskadeErgebnis (trägt `wandkoerper`) oder None
    laufzeit_s: float


def sha256_datei(pfad: Path) -> str:
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


@lru_cache(maxsize=4)
def erkenne(dxf: Path, floor: str = "") -> Lauf:
    """Erkennung laufen lassen und Plan + KaskadeErgebnis mit abgreifen."""
    import notbeleuchtung.raumerkennung.provider as pm

    gefangen: dict = {}
    orig_lade, orig_kask = pm.lade_dxf, pm.raeume_aus_kaskade

    def lade(pfad):
        gefangen["plan"] = orig_lade(pfad)
        return gefangen["plan"]

    def kask(plan, *a, **kw):
        gefangen["kaskade"] = orig_kask(plan, *a, **kw)
        return gefangen["kaskade"]

    t0 = time.time()
    pm.lade_dxf, pm.raeume_aus_kaskade = lade, kask
    try:
        modell = pm.ArchitekturRaumProvider().parse(str(dxf), floor)
    finally:
        pm.lade_dxf, pm.raeume_aus_kaskade = orig_lade, orig_kask
    return Lauf(dxf=dxf, sha256=sha256_datei(dxf), modell=modell,
                plan=gefangen.get("plan"), kaskade=gefangen.get("kaskade"),
                laufzeit_s=round(time.time() - t0, 1))
