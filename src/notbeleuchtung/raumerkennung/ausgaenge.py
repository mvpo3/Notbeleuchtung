"""ausgaenge — Geschossausgänge aus typisierten Türen ableiten.

- ``final_exit``: hauseingang bzw. Notausgangstür ins Freie — nur bei BELEGTEM
  Geschoss und nicht im Obergeschoss (Obergeschosse haben keine Ausgänge ins
  Freie). Ist das Geschoss UNBEKANNT, entsteht fail closed KEIN ``final_exit``,
  sondern die Warnung ``GESCHOSS_UNBEKANNT_WARNUNG`` (Owner-Entscheidung
  2026-09-13, „kein Standardwert EG").
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

import math
from dataclasses import dataclass, field

from notbeleuchtung.hauptengine.contracts.raum_modell import Ausgang, Raum, Tuer

from .geschoss import (
    GESCHOSS_UNBEKANNT_WARNUNG,
    geschoss_bekannt,
    ist_obergeschoss,
)
from .tuer_zuordnung import AUSSEN

_GARAGENTOR_FLW_NAH_MM = 2000.0


@dataclass
class AusgangsWarnung:
    geschoss: str
    grund: str
    gescheiterte_regeln: list[str] = field(default_factory=list)


def _stiegen_seite(t: Tuer, by_id: dict[str, Raum]) -> bool:
    return any(by_id.get(s or "") is not None
               and by_id[s].raum_typ == "STIEGENHAUS"
               for s in (t.von_raum, t.nach_raum))


def leite_ausgaenge(tueren: list[Tuer], raeume: list[Raum], geschoss: str,
                    fluchtweg_enden: list = (),
                    ) -> tuple[list[Ausgang], list[AusgangsWarnung]]:
    """``fluchtweg_enden`` = Endpunkte expliziter Fluchtweglinien (mm) — ein
    Garagentor wird NUR Endausgang, wenn ein Fluchtweg dort endet."""
    by_id = {r.id: r for r in raeume}
    # final_exit in EG UND UG/KG (Kellerausgänge ins Freie); nur Obergeschosse
    # haben keine Ausgänge ins Freie.
    # Fail closed (Owner 2026-09-13): ein UNBEKANNTes Geschoss ist kein
    # Erdgeschoss. Vorher zählte der Leerstring über ``not ist_obergeschoss("")``
    # als ausgangsfähig — daran hingen die final_exit jedes Plans, dessen
    # Geschoss nicht erkannt wurde.
    bekannt = geschoss_bekannt(geschoss)
    eg_oder_ug = bekannt and not ist_obergeschoss(geschoss)
    out: list[Ausgang] = []
    for t in tueren:
        ins_freie = AUSSEN in (t.von_raum, t.nach_raum)
        tor_mit_flw_ende = (
            t.tuer_detail == "garagentor" and ins_freie
            and any(math.dist(t.xy_mm, p) < _GARAGENTOR_FLW_NAH_MM
                    for p in fluchtweg_enden))
        if eg_oder_ug and (
                t.tuer_detail == "hauseingang"
                or (t.ist_notausgang and ins_freie)
                or tor_mit_flw_ende):
            out.append(Ausgang(id=f"exit_{t.id}", xy_mm=t.xy_mm, typ="final_exit"))
        elif (_stiegen_seite(t, by_id)
              and t.tuer_detail in ("stiegenhaustuer", "brandschutztuer")):
            out.append(Ausgang(id=f"exit_{t.id}", xy_mm=t.xy_mm, typ="stair_exit"))
    warnungen: list[AusgangsWarnung] = []
    if not bekannt:
        # Wortlaut aus der Owner-Entscheidung. Unabhängig davon, ob Ausgänge
        # entstanden sind: ein stair_exit macht das fehlende Geschoss nicht
        # harmlos, der ENDausgang bleibt unbestimmbar.
        warnungen.append(AusgangsWarnung(
            geschoss=geschoss,
            grund=GESCHOSS_UNBEKANNT_WARNUNG,
            gescheiterte_regeln=[
                ("final_exit: Geschoss weder aus floor/Dateiname noch aus "
                 "Schriftfeld/Plantext/Höhenkote belegt (kein Standardwert EG)"),
            ]))
    if not out:
        warnungen.append(AusgangsWarnung(
            geschoss=geschoss,
            grund="kein Geschossausgang ableitbar",
            gescheiterte_regeln=[
                "final_exit: keine hauseingang-/Notausgangstür ins Freie (EG)",
                "stair_exit: keine stiegenhaustuer/wohnungseingang am STIEGENHAUS",
            ]))
    return out, warnungen


def ohne_unzulaessige_final_exits(ausgaenge: list[Ausgang],
                                  geschoss: str) -> list[Ausgang]:
    """``final_exit`` nur, wo das Geschoss BELEGT und kein Obergeschoss ist.

    Die einzige Stelle, durch die BEIDE ``final_exit``-Erzeuger laufen: die
    Ableitung in ``leite_ausgaenge`` und ``footprint.hauptausgaenge``
    (``provider.py:102``), das seine ``final_exit`` rein geometrisch an der
    Gebäude-Außenkante bildet — ohne Raum-, Typ- und Geschossbezug. Ein Gate
    nur in ``leite_ausgaenge`` ließe den footprint-Pfad offen.
    """
    if geschoss_bekannt(geschoss) and not ist_obergeschoss(geschoss):
        return list(ausgaenge)
    return [a for a in ausgaenge if a.typ != "final_exit"]
