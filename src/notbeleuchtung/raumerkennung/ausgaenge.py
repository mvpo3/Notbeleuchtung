"""ausgaenge — Geschossausgänge aus typisierten Türen ableiten.

- ``final_exit``: hauseingang bzw. Notausgangstür ins Freie — nur im EG
  (Obergeschosse haben keine Ausgänge ins Freie).
- ``stair_exit``: Tür ins STIEGENHAUS aus der Erschließung (GANG/VORRAUM,
  ``stiegenhaustuer``) sowie eine Brandschutztür an der Stiege (Tür über die
  Brandabschnittsgrenze). Wohnungseingänge direkt ins Stiegenhaus sind KEINE
  Geschossausgänge — sie sind die Start-, nicht die Zielseite des Fluchtwegs
  (sonst produziert jede Wohnungstür einen Pfeil, Mollgasse-Befund).

Referenz über die ID-Konvention ``exit_<tuer_id>``. Findet sich kein
Geschossausgang, kommt ein ``AusgangsWarnung``-Objekt mit den gescheiterten
Regeln zurück (für bericht.md).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from notbeleuchtung.hauptengine.contracts.raum_modell import Ausgang, Raum, Tuer

from .tuer_typisierung import ist_erdgeschoss
from .tuer_zuordnung import AUSSEN


@dataclass
class AusgangsWarnung:
    geschoss: str
    grund: str
    gescheiterte_regeln: list[str] = field(default_factory=list)


def _stiegen_seite(t: Tuer, by_id: dict[str, Raum]) -> bool:
    return any(by_id.get(s or "") is not None
               and by_id[s].raum_typ == "STIEGENHAUS"
               for s in (t.von_raum, t.nach_raum))


def leite_ausgaenge(tueren: list[Tuer], raeume: list[Raum],
                    geschoss: str) -> tuple[list[Ausgang], list[AusgangsWarnung]]:
    by_id = {r.id: r for r in raeume}
    out: list[Ausgang] = []
    for t in tueren:
        ins_freie = AUSSEN in (t.von_raum, t.nach_raum)
        if ist_erdgeschoss(geschoss) and (
                t.tuer_detail == "hauseingang"
                or (t.ist_notausgang and ins_freie)):
            out.append(Ausgang(id=f"exit_{t.id}", xy_mm=t.xy_mm, typ="final_exit"))
        elif (_stiegen_seite(t, by_id)
              and t.tuer_detail in ("stiegenhaustuer", "brandschutztuer")):
            out.append(Ausgang(id=f"exit_{t.id}", xy_mm=t.xy_mm, typ="stair_exit"))
    warnungen: list[AusgangsWarnung] = []
    if not out:
        warnungen.append(AusgangsWarnung(
            geschoss=geschoss,
            grund="kein Geschossausgang ableitbar",
            gescheiterte_regeln=[
                "final_exit: keine hauseingang-/Notausgangstür ins Freie (EG)",
                "stair_exit: keine stiegenhaustuer/wohnungseingang am STIEGENHAUS",
            ]))
    return out, warnungen
