"""OG1-Kennzahlen des Türstapel-Gates — nackte Zahlen aus dem ``RaumModell``.

Kein Urteil, keine Schwelle: das Gate vergleicht diese Zahlen zwischen zwei
Ständen (Nullmessung vs. Stapel). Listen stehen neben den Zählern, damit ein
Rückschritt sofort auf die verursachende Tür bzw. Wohnung zeigt.

``tueren_raum_a_gleich_b`` zählt Türen, bei denen BEIDE Seiten gesetzt sind und
gleich sind (``von_raum == nach_raum``). Eine Tür mit nur einer gesetzten Seite
(``nach_raum`` leer/None) zählt hier NICHT mit — sie ist ein anderer Befund.
"""
from __future__ import annotations

from collections import Counter

UNBEKANNT = ("", "UNBEKANNT")


def kennzahlen(modell) -> dict:
    """Die sieben OG1-Zahlen aus § 1c des Gate-Auftrags."""
    je_wohnung = Counter(r.wohnung_id for r in modell.raeume if r.wohnung_id)
    einraum = sorted(w for w, n in je_wohnung.items() if n == 1)
    gleich = [{"id": t.id, "raum": t.von_raum} for t in modell.tueren
              if t.von_raum and t.nach_raum and t.von_raum == t.nach_raum]
    return {
        "raeume_gesamt": len(modell.raeume),
        "unbekannt": sum(1 for r in modell.raeume if (r.raum_typ or "") in UNBEKANNT),
        "tueren_gesamt": len(modell.tueren),
        "tueren_raum_a_gleich_b": len(gleich),
        "tueren_raum_a_gleich_b_liste": gleich,
        "durchgaenge_ohne_tuerblatt": sum(1 for t in modell.tueren if t.ohne_tuerblatt),
        "wohnungen": len(je_wohnung),
        "einraum_wohnungen": len(einraum),
        "einraum_wohnungen_liste": einraum,
    }
