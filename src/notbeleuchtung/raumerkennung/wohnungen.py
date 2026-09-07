"""wohnungen — Wohnungsbildung über zimmertuer-Kanten (``Raum.wohnung_id``).

Zusammenhangskomponenten der WOHNUNG_PRIVAT-Basisräume über ``zimmertuer``-
Kanten; abgeschlossen durch ``wohnungseingang``-Türen. ``wohnung_id`` wird als
``top_1..n`` vergeben (deterministisch nach kleinster Raum-ID).

Verfeinerung der Nutzungsklasse: ein GANG/VORRAUM, der nur an private Räume
(ZIMMER/BAD/WC/KUECHE/ABSTELLRAUM …) grenzt und KEINE Tür in STIEGENHAUS oder
AUSSEN hat, ist ein Wohnungs-Flur → WOHNUNG_PRIVAT (Befund-Fallback).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer

from .nutzungsklasse import nutzungsklasse_fuer
from .tuer_zuordnung import AUSSEN


@dataclass
class Wohnung:
    id: str
    raum_ids: list[str] = field(default_factory=list)
    eingangs_tuer_ids: list[str] = field(default_factory=list)


def _klasse(r: Raum) -> str | None:
    return r.nutzungsklasse or nutzungsklasse_fuer(r.raum_typ)


def _verfeinere_gang_privat(raeume: list[Raum], tueren: list[Tuer]) -> None:
    """Flur-Verfeinerung in BEIDE Richtungen (der statische Default kann falsch
    liegen): ein GANG/VORRAUM nur an Privaträumen, ohne Tür in STIEGENHAUS
    oder AUSSEN, ist ein Wohnungs-Flur → WOHNUNG_PRIVAT; mit einer solchen
    Tür ist er Erschließung → ALLGEMEIN_ERSCHLIESSUNG."""
    by_id = {r.id: r for r in raeume}
    for r in raeume:
        if r.raum_typ not in ("GANG", "VORRAUM"):
            continue
        nachbarn: list[str | None] = []
        privat_ok = True
        for t in tueren:
            if r.id not in (t.von_raum, t.nach_raum):
                continue
            andere = t.nach_raum if t.von_raum == r.id else t.von_raum
            nachbarn.append(andere)
            fremd = andere in by_id and (
                by_id[andere].raum_typ == "STIEGENHAUS"
                or _klasse(by_id[andere]) not in ("WOHNUNG_PRIVAT", None))
            if andere == AUSSEN or fremd:
                privat_ok = False
        if nachbarn:
            r.nutzungsklasse = ("WOHNUNG_PRIVAT" if privat_ok
                                else "ALLGEMEIN_ERSCHLIESSUNG")


def bilde_wohnungen(raeume: list[Raum], tueren: list[Tuer]) -> list[Wohnung]:
    """Setzt ``nutzungsklasse`` (statischer Default) + ``wohnung_id`` in-place;
    liefert die Wohnungen (id, raum_ids, eingangs_tuer_ids)."""
    for r in raeume:
        if r.nutzungsklasse is None:
            r.nutzungsklasse = nutzungsklasse_fuer(r.raum_typ)
    _verfeinere_gang_privat(raeume, tueren)

    privat = {r.id for r in raeume if _klasse(r) == "WOHNUNG_PRIVAT"}
    # Verfeinerung korrigiert die Tür-Rollen nach: Türen eines jetzt privaten
    # Wohnungs-Flurs zu Zimmern sind zimmertueren, keine Wohnungseingänge mehr —
    # und umgekehrt wird die Tür eines jetzt communalen Flurs zum Privatraum
    # ein Wohnungseingang.
    for t in tueren:
        beide_privat = t.von_raum in privat and t.nach_raum in privat
        if t.tuer_detail == "wohnungseingang" and beide_privat:
            t.tuer_detail = "zimmertuer"
        elif (t.tuer_detail == "zimmertuer" and not beide_privat
              and (t.von_raum in privat) != (t.nach_raum in privat)):
            andere = t.nach_raum if t.von_raum in privat else t.von_raum
            if andere in {r.id for r in raeume
                          if _klasse(r) == "ALLGEMEIN_ERSCHLIESSUNG"}:
                t.tuer_detail = "wohnungseingang"
    # Union-Find über zimmertuer-Kanten (klein genug für Pfad-Naivität).
    parent = {rid: rid for rid in privat}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for t in tueren:
        a, b = t.von_raum, t.nach_raum
        if a in privat and b in privat and t.tuer_detail in ("zimmertuer", None):
            parent[find(a)] = find(b)

    gruppen: dict[str, list[str]] = {}
    for rid in privat:
        gruppen.setdefault(find(rid), []).append(rid)

    by_id = {r.id: r for r in raeume}
    wohnungen: list[Wohnung] = []
    for i, wurzel in enumerate(sorted(gruppen, key=lambda w: min(gruppen[w])),
                               start=1):
        raum_ids = sorted(gruppen[wurzel])
        eingaenge = [t.id for t in tueren
                     if t.tuer_detail == "wohnungseingang"
                     and (t.von_raum in raum_ids or t.nach_raum in raum_ids)]
        w = Wohnung(id=f"top_{i}", raum_ids=raum_ids,
                    eingangs_tuer_ids=eingaenge)
        wohnungen.append(w)
        for rid in raum_ids:
            by_id[rid].wohnung_id = w.id
    return wohnungen
