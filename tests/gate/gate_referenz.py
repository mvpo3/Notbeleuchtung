"""Verbindungen zwischen zwei OG1-Räumen, wie die Referenz sie verneint bzw. fordert.

Die Referenz (Übergabepaket, Stand pending_owner_review) nennt Raumpaare, die im
OG1 KEINE direkte Verbindung haben dürfen, und offene Übergänge, die es geben
muss. Beides ist Vorgabe, keine Wahrheit — hier wird nur gemessen, geurteilt
wird in ``gate_regel`` (Bedingungen (7) und (8)).

Räume werden über ``raum_typ`` + Fläche (m², Toleranz ``FLAECHE_TOL_M2``)
identifiziert, nicht über IDs: die IDs wandern zwischen Codeständen, Typ und
Fläche nicht. Passt kein oder mehr als ein Raum, ist der Fall NICHT messbar
(``anzahl`` None mit ``grund``) — und kein stilles Bestehen.

Gezählt werden Türen JEDER Quelle (``block``, ``arc``, ``durchgang`` …), die
beide Raum-IDs verbinden; ``ohne_tuerblatt`` sagt, wie viele davon Durchgänge
ohne Türblatt sind. Koordinaten und Texte der Referenz stehen hier NICHT (das
Repo ist öffentlich, das Paket nicht) — nur Typ, Fläche und die Fundstelle.
"""
from __future__ import annotations

from collections import Counter

FLAECHE_TOL_M2 = 0.05

# Die Wohnküche trägt im Modell keinen Raumtyp (raum_typ "").
WOHNKUECHE = ("", 73.06)

# (Referenz, Raum A, Raum B, zusatz) — Owner-Liste 2026-09-18.
# ``zusatz`` markiert die Paare aus Bsp. 14 „keine direkte Verbindung aus bloßer
# Nachbarschaft": heute schon 0, hier als Schutz gegen einen Rückschritt.
VERNEINT = (
    ("M17-02 / Bsp. 07, 08, 14", ("BAD", 11.76), ("BAD", 4.66), False),
    ("Bsp. 06, 14", ("ZIMMER", 17.04), ("GANG", 6.48), False),
    ("Bsp. 08, 09, 14", ("VORRAUM", 3.40), ("BAD", 4.66), False),
    ("Bsp. 08, 14", ("ZIMMER", 10.59), ("BAD", 4.66), False),
    ("Bsp. 09, 14", ("ZIMMER", 16.86), ("VORRAUM", 3.40), False),
    ("Bsp. 07, 14", ("BAD", 11.76), ("ZIMMER", 17.04), False),
    ("Bsp. 14", ("ZIMMER", 16.86), ("BALKON", 7.51), True),
    ("Bsp. 14", ("ZIMMER", 16.11), ("BALKON", 7.51), True),
    ("Bsp. 14", ("WC", 3.50), ("STIEGENHAUS", 11.21), True),
    ("Bsp. 14", ("GANG", 6.48), ("STIEGENHAUS", 11.21), True),
    ("Bsp. 14", ("GANG", 6.48), ("BAD", 4.66), True),
)

# (Referenz, Raum A, Raum B, Hinweis) — offene Übergänge der Referenz.
GEFORDERT = (
    ("O03 (Bsp. 06, 09, 14)", ("GANG", 6.48), WOHNKUECHE, ""),
    ("O04 (Bsp. 06, 09, 14)", ("GANG", 6.48), ("ZIMMER", 10.59), ""),
    ("O05 (Bsp. 06, 09, 14)", ("VORRAUM", 2.59), ("VORRAUM", 3.40), ""),
    ("O01/O02 (Bsp. 06, 09, 14)", ("VORRAUM", 10.94), WOHNKUECHE,
     "Ersatzfall für O01/O02, solange Bereich E kein eigener Raum ist"),
)


def _bezeichnung(raum_typ: str, flaeche_m2: float) -> str:
    return f"{raum_typ or '(ohne Typ)'} {flaeche_m2:.2f} m²"


def _raum_id(modell, raum_typ: str, flaeche_m2: float) -> tuple[str | None, str]:
    """(ID, Grund) — Grund ist leer, wenn genau ein Raum passt."""
    treffer = [r.id for r in modell.raeume
               if (r.raum_typ or "") == raum_typ
               and abs(float(r.flaeche_m2) - flaeche_m2) <= FLAECHE_TOL_M2]
    if len(treffer) == 1:
        return treffer[0], ""
    name = _bezeichnung(raum_typ, flaeche_m2)
    if not treffer:
        return None, f"kein Raum {name} (±{FLAECHE_TOL_M2} m²) im Modell"
    return None, f"{len(treffer)} Räume passen auf {name}: {sorted(treffer)}"


def _messe(modell, referenz: str, a: tuple[str, float], b: tuple[str, float]) -> dict:
    """Ein Messfall: beide Räume auflösen, dann die verbindenden Türen zählen."""
    id_a, grund_a = _raum_id(modell, *a)
    id_b, grund_b = _raum_id(modell, *b)
    eintrag = {
        "referenz": referenz,
        "raum_a": {"raum_typ": a[0], "flaeche_m2": a[1], "id": id_a},
        "raum_b": {"raum_typ": b[0], "flaeche_m2": b[1], "id": id_b},
    }
    grund = "; ".join(g for g in (grund_a, grund_b) if g)
    if grund:
        return {**eintrag, "anzahl": None, "ids": [], "quellen": {},
                "ohne_tuerblatt": 0, "grund": grund}
    tueren = [t for t in modell.tueren if {t.von_raum, t.nach_raum} == {id_a, id_b}]
    return {**eintrag,
            "anzahl": len(tueren),
            "ids": sorted(t.id for t in tueren),
            "quellen": dict(sorted(Counter(t.quelle or "" for t in tueren).items())),
            "ohne_tuerblatt": sum(1 for t in tueren if t.ohne_tuerblatt),
            "grund": ""}


def verbindungen(modell) -> dict:
    """Die Referenz-Messfälle des OG1-Modells: verneinte und geforderte Verbindungen."""
    return {
        "verneint": [{**_messe(modell, referenz, a, b), "zusatz": zusatz}
                     for referenz, a, b, zusatz in VERNEINT],
        "gefordert": [{**_messe(modell, referenz, a, b), "hinweis": hinweis}
                      for referenz, a, b, hinweis in GEFORDERT],
    }
