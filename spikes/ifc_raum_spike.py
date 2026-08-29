"""Spike — IFC/BIM als 2. Input-Pfad: IfcSpace/IfcDoor → RaumModell-Contract.

Beweist, dass IfcOpenShell die Raumerkennung (Input 1) für BIM-Projekte ersetzen
kann: IFC liefert Räume/Türen SEMANTISCH (IfcSpace = Raum mit Name/Typ/Fläche),
statt sie aus DXF-Wandlinien zu erraten. KEIN Produktions-Code — Owner-Grenze:
der echte IFC-`RaumProvider` gehört in Selmans `raumerkennung/` (dieser Spike
importiert es nicht, konstruiert nur den gemeinsamen Contract).

Lauf: .venv/Scripts/python.exe spikes/ifc_raum_spike.py
Braucht das `ifc`-Extra (ifcopenshell; auf py3.14 manuell vendored).
"""
from __future__ import annotations

from pathlib import Path

import ifcopenshell
import ifcopenshell.api.aggregate
import ifcopenshell.api.pset
import ifcopenshell.api.root
import ifcopenshell.api.unit
import ifcopenshell.util.element

from notbeleuchtung.hauptengine.contracts import BBox, Raum, RaumModell, Tuer


def demo_ifc() -> ifcopenshell.file:
    """Minimales IFC4-Modell: Projekt → Bauwerk → Geschoss mit 2 Räumen + 1 Tür."""
    m = ifcopenshell.file(schema="IFC4")
    project = ifcopenshell.api.root.create_entity(m, ifc_class="IfcProject", name="Demo")
    ifcopenshell.api.unit.assign_unit(m)
    site = ifcopenshell.api.root.create_entity(m, ifc_class="IfcSite", name="Gelände")
    building = ifcopenshell.api.root.create_entity(m, ifc_class="IfcBuilding", name="Haus")
    storey = ifcopenshell.api.root.create_entity(m, ifc_class="IfcBuildingStorey", name="4OG")
    ifcopenshell.api.aggregate.assign_object(m, products=[site], relating_object=project)
    ifcopenshell.api.aggregate.assign_object(m, products=[building], relating_object=site)
    ifcopenshell.api.aggregate.assign_object(m, products=[storey], relating_object=building)

    def space(name: str, typ: str, area: float) -> None:
        sp = ifcopenshell.api.root.create_entity(m, ifc_class="IfcSpace", name=name)
        sp.LongName = typ
        ifcopenshell.api.aggregate.assign_object(m, products=[sp], relating_object=storey)
        qto = ifcopenshell.api.pset.add_qto(m, product=sp, name="Qto_SpaceBaseQuantities")
        ifcopenshell.api.pset.edit_qto(m, qto=qto, properties={"GrossFloorArea": area})

    space("R-STGH-B", "STIEGENHAUS", 25.0)
    space("R-SAAL-1", "SAAL", 180.0)

    door = ifcopenshell.api.root.create_entity(m, ifc_class="IfcDoor", name="T-B1")
    door.OverallWidth = 900.0  # Tür ohne Wand-Host — für den Spike genügt die Semantik
    return m


_FLUCHT_TYPEN = {"STIEGENHAUS", "GANG", "FLUR", "KORRIDOR"}


def ifc_to_raummodell(model: ifcopenshell.file, floor: str) -> RaumModell:
    """IfcSpace → Raum, IfcDoor → Tuer. Fläche aus Qto_SpaceBaseQuantities."""
    raeume: list[Raum] = []
    for sp in model.by_type("IfcSpace"):
        psets = ifcopenshell.util.element.get_psets(sp)
        area = psets.get("Qto_SpaceBaseQuantities", {}).get("GrossFloorArea", 0.0)
        typ = (sp.LongName or sp.ObjectType or "UNBEKANNT").upper()
        raeume.append(
            Raum(
                id=sp.Name or sp.GlobalId,
                raum_typ=typ,
                flaeche_m2=float(area or 0.0),
                ist_fluchtweg=typ in _FLUCHT_TYPEN,
            )
        )
    tueren = [
        Tuer(id=d.Name or d.GlobalId, xy_mm=(0.0, 0.0), breite_mm=float(d.OverallWidth or 0.0))
        for d in model.by_type("IfcDoor")
    ]
    return RaumModell(
        floor=floor,
        bounds_mm=BBox(min_xy=(0.0, 0.0), max_xy=(0.0, 0.0)),
        raeume=raeume,
        tueren=tueren,
    )


def main() -> None:
    out = Path(__file__).with_name("_demo.ifc")
    m = demo_ifc()
    m.write(str(out))
    print(f"IFC geschrieben: {out.name}  ({out.stat().st_size} B)")

    model = ifcopenshell.open(str(out))
    rm = ifc_to_raummodell(model, floor="4OG")
    print(f"\nRaumModell aus IFC — floor={rm.floor}, {len(rm.raeume)} Räume, {len(rm.tueren)} Türen:")
    for r in rm.raeume:
        print(f"  {r.id:<12} typ={r.raum_typ:<12} {r.flaeche_m2:>6.1f} m²  fluchtweg={r.ist_fluchtweg}")
    for t in rm.tueren:
        print(f"  Tür {t.id:<10} {t.breite_mm:.0f} mm")
    print("\nContract-Roundtrip OK:", rm.contract, rm.contract_version)


if __name__ == "__main__":
    main()
