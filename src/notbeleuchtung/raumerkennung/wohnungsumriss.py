"""wohnungsumriss — liegt ein Raum im Umriss einer Wohnung? Kontrolle, keine Zuordnung.

Owner (K3, 2026-09-30): „Der Top-Stempel ist Kontrolle: der Raum muss innerhalb
eines Wohnungsumrisses liegen, sonst bleibt UNBEKANNT." Welche Räume eine
Wohnung bilden, entscheiden ausschließlich rohe Türen (``wohnungen.
bilde_wohnungen``, Grundsatz (b) 2026-09-22). Dieses Modul liest ``wohnung_id``
nur und setzt nie eine.

**Umriss** = die Räume einer Wohnung samt dem, was zwischen ihnen und der
Gebäudehülle liegt. Gemessen an Rennweg OG3 ``rest_6`` („UNBEKANNT 6,6 m²"): der
Raum sitzt in einer Bucht von ``top_2`` an der Fassade — Nachbarn nur Räume von
``top_2`` (0–152 mm), links die Außenwand. Die Außenkontur der Raumvereinigung
(±250 mm geschlossen, ohne Löcher) deckt 0 % von ihm, weil die Bucht zur
Fassade offen ist; erst ±2 000 mm schlössen sie. Darum hier die Prüfung über die
Nachbarschaft statt über ein Schließ-Maß:

* jeder Nachbarraum bis Wanddicke (``NACHBAR_MM``) gehört zu derselben Wohnung —
  Schacht/Lift (``KEIN_RAUM``) und Freiflächen (``AUSSEN``) zählen nicht mit,
  sie gehören keiner Wohnung und keiner Erschließung;
* jede Tür des Raums führt in diese Wohnung — eine Tür ins Freie, ins
  Unerkannte oder zu einem fremden Raum nimmt ihn heraus (im Zweifel bleibt der
  Raum, was er war, und behält sein Notlicht).

**Umriss als Fläche (K4, Owner 2026-09-30)** — ``wohnungsumrisse`` /
``anteile_im_umriss``: die Außenkontur ohne Löcher von ``unary_union(Räume
gleicher wohnung_id).buffer(+SCHLIESS_MM).buffer(−SCHLIESS_MM)`` (Definition aus
dem K1-Auftrag; die Darstellung zeichnet dieselbe Union mit ±200 mm).
„Vollständig innerhalb" heißt ≥ ``VOLL`` der Raumfläche (Planer-Präzisierung
K4); ein Mitglied von ``top_n`` liegt in ``top_n``.
"""
from __future__ import annotations

from shapely.geometry import Polygon
from shapely.ops import unary_union

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer

#: Bis zu diesem Abstand ist ein Raum Nachbar (Wanddicke). ponytail: Knopf,
#: gemessen an den K3-Kandidaten (Nachbarn 0–152 mm); Wohnungstrenn- und
#: Stiegenhauswände bis 500 mm. Nachmessen, wenn eine dickere Trennwand einen
#: fremden Raum verdeckt.
NACHBAR_MM = 500.0
#: Klassen, die keiner Wohnung und keiner Erschließung gehören.
_NEUTRAL = frozenset({"KEIN_RAUM", "AUSSEN"})
#: Schließmaß des Flächen-Umrisses: Wände bis 2 × 250 mm fallen zu.
SCHLIESS_MM = 250.0
#: „Vollständig innerhalb" = mindestens dieser Anteil der Raumfläche.
VOLL = 0.98


def wohnungsumrisse(raeume: list[Raum]) -> dict:
    """``{wohnung_id: Umriss}`` — Außenkontur ohne Löcher der geschlossenen
    Raumvereinigung jeder Wohnung. Liest nur ``wohnung_id`` und Polygone."""
    je: dict[str, list[Polygon]] = {}
    for r in raeume:
        if r.wohnung_id and len(r.polygon_mm) >= 3:
            je.setdefault(r.wohnung_id, []).append(Polygon(r.polygon_mm).buffer(0))
    out = {}
    for wid, ps in je.items():
        g = unary_union(ps).buffer(SCHLIESS_MM).buffer(-SCHLIESS_MM)
        out[wid] = unary_union([Polygon(p.exterior)
                                for p in getattr(g, "geoms", [g]) if not p.is_empty])
    return out


def anteile_im_umriss(raum: Raum, umrisse: dict) -> dict[str, float]:
    """Anteil der Raumfläche je Wohnungsumriss (0..1); ein Mitglied liegt in
    seiner eigenen Wohnung ganz (1.0), gleich wie der Umriss verläuft."""
    g = Polygon(raum.polygon_mm).buffer(0) if len(raum.polygon_mm) >= 3 else None
    out: dict[str, float] = {raum.wohnung_id: 1.0} if raum.wohnung_id else {}
    for wid, u in umrisse.items():
        if wid == raum.wohnung_id:
            continue
        if g is None or g.area <= 0:
            out[wid] = 0.0
        else:
            out[wid] = g.intersection(u).area / g.area
    return out


def umschliessende_wohnung(raum: Raum, raeume: list[Raum], tueren: list[Tuer],
                           nachbar_mm: float = NACHBAR_MM) -> tuple[str | None, str]:
    """``(wohnung_id, grund)`` der Wohnung, in deren Umriss ``raum`` liegt,
    sonst ``(None, grund)``. Liest nur ``wohnung_id``, Klasse und Türen."""
    g = Polygon(raum.polygon_mm).buffer(0)
    nachbarn = [r for r in raeume
                if r.id != raum.id and len(r.polygon_mm) >= 3
                and r.nutzungsklasse not in _NEUTRAL
                and Polygon(r.polygon_mm).buffer(0).distance(g) <= nachbar_mm]
    liste = ", ".join(f"{r.id} {r.raum_typ or '—'} {r.wohnung_id or 'ohne Wohnung'}"
                      for r in nachbarn)
    wohnungen = {r.wohnung_id for r in nachbarn}
    if not nachbarn:
        return None, f"kein Nachbarraum bis {nachbar_mm:.0f} mm"
    if len(wohnungen) != 1 or None in wohnungen:
        return None, f"Nachbarn nicht alle in einer Wohnung: {liste}"
    (wid,) = wohnungen
    drin = {r.id for r in raeume if r.wohnung_id == wid}
    for t in tueren:
        if raum.id not in (t.von_raum, t.nach_raum):
            continue
        andere = t.nach_raum if t.von_raum == raum.id else t.von_raum
        if andere not in drin:
            return None, f"Tür {t.id} führt nach {andere or '—'}, nicht in {wid}"
    return wid, f"Nachbarn nur {wid}: {liste}"
