"""oib_gate — projekt-globales Gate für OVE-scope-gebundene Trigger (v1).

Die Flächen-Schwellen des Antipanik-Triggers (`NormRegelwerk.flaechen_schwellen`)
stammen aus OVE E 8101:2019 718.560.9.001.AT bzw. ÖVE/ÖNORM E 8002-1 und gelten
dort nur für Bauvorhaben mit „erhöhten Anforderungen nach der Art der Nutzung"
(OVE R 12-2 / OIB-RL 2) — nicht global aus EN 1838. Genau diese Frage beantwortet
der OIB-Pfad (`OibProvider.bewerte_oib` über einen `ProjektKontext`). Dieses Modul
übersetzt dessen Befund in das Gate-Signal für `flaechen_strategy`.

v1 wertet **projekt-global** aus (`Gebaeudeteil.raum_referenzen` werden noch nicht
raum-genau zugeordnet) und ist **fail-closed**: ohne Befund oder bei ausschließlich
`review_required`/`nicht_erforderlich` bleibt das Gate zu — das ist exakt das
Verhalten vor dem OIB-Anschluss (Schwellen inert), es fällt keine Leuchte weg.
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import OibBefund

# Stufen, die die „erhöhten Anforderungen" des OVE-Scopes bestätigen → Gate offen.
_OFFEN = {"eingeschraenkt", "uneingeschraenkt"}

_HINWEIS_GLOBAL = (
    "OIB-Gate v1 wertet projekt-global aus — Gebaeudeteil.raum_referenzen werden "
    "nicht raum-genau zugeordnet."
)


def flaechen_trigger_offen(oib: OibBefund | None) -> bool:
    """Darf der Antipanik-Flächen-Trigger feuern?

    Offen, sobald mindestens ein Gebäudeteil Sicherheitsbeleuchtung eingeschränkt
    oder uneingeschränkt erfordert. `None` (kein OIB-Pfad gefahren) und
    `review_required` lassen das Gate zu — fail-closed, weil „zu" dem bisherigen
    Verhalten entspricht.
    """
    if oib is None:
        return False
    return any(e.stufe in _OFFEN for e in oib.ergebnisse)


def gate_summary(oib: OibBefund) -> dict:
    """Audit-Block für `render_summary["oib"]` — Stufen je Gebäudeteil + Gate-Zustand."""
    offen = flaechen_trigger_offen(oib)
    hinweise = [_HINWEIS_GLOBAL]
    if not offen and any(e.stufe == "review_required" for e in oib.ergebnisse):
        hinweise.append(
            "OIB-Erforderlichkeit review_required — Antipanik-Flächen-Trigger bleibt "
            "zu (fail-closed), bis der Befund geklärt ist."
        )
    return {
        "stufen": {e.gebaeudeteil_id: e.stufe for e in oib.ergebnisse},
        "flaechen_trigger_gate": "offen" if offen else "zu",
        "hinweise": hinweise,
    }
