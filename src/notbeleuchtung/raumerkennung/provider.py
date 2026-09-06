"""ArchitekturRaumProvider — echter RaumProvider (Selman).

Übersetzt einen leeren Architekturplan (DXF) in das ``RaumModell``-Contract:
Räume/Türen/Ausgänge/Fluchtweg-Zirkulation. Reine Geometrie/Topologie, kein
Norm-Urteil (das machen Enis/Leonis).

Baut inkrementell auf schlanken Modulen dieses Packages auf und verwendet die
sauberen, self-contained Port-Helfer (``._port.parsers.room_faces``,
``._port.models.room``) wieder. Ersetzt schrittweise den ``FakeRaumProvider``.
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import RaumModell
from notbeleuchtung.hauptengine.contracts.raum_modell import Tuer

from .dxf_load import bounds_mm, lade_dxf
from .footprint import hauptausgaenge
from .geometrie_typ import typisiere_geometrisch
from .kaskade import KaskadeErgebnis, raeume_aus_kaskade
from .raumtyp import beschrifte_raeume
from .tueren import tueren_aus_dxf
from .waende import raeume_aus_waenden
from .wandkoerper import bounds_aus_wandkoerpern
from .zirkulation import zirkulation_aus_dxf


class ArchitekturRaumProvider:
    """Erfüllt das ``RaumProvider``-Protocol (``parse(dxf_path, floor)``).

    Verdrahtet die Slice-Module zu einem ``RaumModell``. Räume/Türen/Fluchtweg
    aus echter DXF-Geometrie; Norm-Urteile bleiben Enis/Leonis.

    Räume kommen aus der Kaskade L→H→F→R (``kaskade.raeume_aus_kaskade``) —
    derselben Orchestrierung wie in der Prüfstrecke ``scripts/plan_pruefen.py``.
    """

    def parse(self, dxf_path: str, floor: str) -> RaumModell:
        plan = lade_dxf(dxf_path)
        # Greift kein Wand-Layer-Muster (Muthgasse-Familie), bleibt die Kaskade aus:
        # ihr Raster wäre auf einem unerschlossenen Plan nur teuer, und `bounds_mm`
        # bricht gleich darauf definiert ab (kein stilles Leer-Ergebnis).
        hat_wand_entities = next(plan.wall_entities(), None) is not None
        k = raeume_aus_kaskade(plan) if hat_wand_entities else KaskadeErgebnis()
        try:
            bounds = bounds_mm(plan)
        except ValueError:
            # Hatch-only-Pläne haben keine Wand-Linien, aber Wandkörper.
            if not k.wandkoerper:
                raise
            bounds = bounds_aus_wandkoerpern(k.wandkoerper)
        raeume = k.alle_raeume
        if not raeume:
            raeume = beschrifte_raeume(plan, raeume_aus_waenden(plan))
        # Geometrische Typ-Ableitung (STIEGENHAUS aus Treppen-Blöcken) — greift auch
        # auf Plänen ohne Text-Labels (z.B. Mollgasse), ergänzt Text/Layer-Typisierung.
        raeume = typisiere_geometrisch(plan, raeume)
        tueren = tueren_aus_dxf(plan)
        if not tueren:
            # Rennweg: keine benannten Tür-Blöcke im Modelspace, aber Öffnungen
            # in den Blockdefinitionen — die Kaskade hat sie bereits gesucht.
            tueren = [
                Tuer(id=f"tuer_{i}", xy_mm=o.xy_mm, breite_mm=o.breite_mm,
                     ist_notausgang=False)
                for i, o in enumerate(k.tueroeffnungen, start=1)
            ]
        ausgaenge = hauptausgaenge(plan, bounds)
        zirkulation = zirkulation_aus_dxf(plan)
        return RaumModell(
            floor=floor,
            bounds_mm=bounds,
            raeume=raeume,
            tueren=tueren,
            ausgaenge=ausgaenge,
            zirkulation=zirkulation,
        )
