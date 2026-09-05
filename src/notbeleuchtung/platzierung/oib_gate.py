"""oib_gate — Gate für OVE-scope-gebundene Trigger (projekt-global oder raum-genau).

Die Flächen-Schwellen des Antipanik-Triggers (`NormRegelwerk.flaechen_schwellen`)
stammen aus OVE E 8101:2019 718.560.9.001.AT bzw. ÖVE/ÖNORM E 8002-1 und gelten
dort nur für Bauvorhaben mit „erhöhten Anforderungen nach der Art der Nutzung"
(OVE R 12-2 / OIB-RL 2) — nicht global aus EN 1838. Genau diese Frage beantwortet
der OIB-Pfad (`OibProvider.bewerte_oib` über einen `ProjektKontext`). Dieses Modul
übersetzt dessen Befund in das Gate-Signal für `flaechen_strategy`.

Das Gate ist **fail-closed**: ohne Befund oder bei ausschließlich
`review_required`/`nicht_erforderlich` bleibt es zu — das ist exakt das Verhalten
vor dem OIB-Anschluss (Schwellen inert), es fällt keine Leuchte weg.

Auflösung in zwei Stufen: tragen ALLE bestätigenden Gebäudeteile
`raum_referenzen`, gilt das offene Gate **raum-genau** nur für die referenzierten
Räume (`freigegebene_raeume`); fehlt auch nur einem bestätigenden Teil die
Raum-Zuordnung, gilt es **projekt-global** für alle Räume — ein Befund ohne
Zuordnung darf nicht stillschweigend enger ausgelegt werden.
"""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts import OibBefund

# Stufen, die die „erhöhten Anforderungen" des OVE-Scopes bestätigen → Gate offen.
_OFFEN = {"eingeschraenkt", "uneingeschraenkt"}

_HINWEIS_GLOBAL = (
    "OIB-Gate projekt-global (mindestens ein bestätigender Gebäudeteil ohne "
    "raum_referenzen) — der Flächen-Trigger gilt für alle Räume."
)

_HINWEIS_RAUM_GENAU = (
    "OIB-Gate raum-genau: der Flächen-Trigger gilt nur für die in "
    "raum_referenzen benannten Räume der bestätigenden Gebäudeteile."
)


def _bestaetigende(oib: OibBefund):
    return [e for e in oib.ergebnisse if e.stufe in _OFFEN]


def flaechen_trigger_offen(oib: OibBefund | None) -> bool:
    """Darf der Antipanik-Flächen-Trigger feuern?

    Offen, sobald mindestens ein Gebäudeteil Sicherheitsbeleuchtung eingeschränkt
    oder uneingeschränkt erfordert. `None` (kein OIB-Pfad gefahren) und
    `review_required` lassen das Gate zu — fail-closed, weil „zu" dem bisherigen
    Verhalten entspricht.
    """
    if oib is None:
        return False
    return bool(_bestaetigende(oib))


def freigegebene_raeume(oib: OibBefund | None, floor: str) -> set[str] | None:
    """Raum-Scope des offenen Gates für ein Geschoss.

    `None` = keine raum-genaue Einschränkung — das (offene) Gate gilt für alle
    Räume. Das ist der Fall ohne Befund oder wenn mindestens ein bestätigender
    Gebäudeteil keine `raum_referenzen` trägt. Tragen ALLE bestätigenden Teile
    Referenzen, kommt die Menge der referenzierten `raum_id`s dieses Geschosses
    zurück (ggf. leer → auf diesem Geschoss feuert nichts). Nur in Kombination
    mit `flaechen_trigger_offen` sinnvoll — ein zues Gate bleibt zu.
    """
    if oib is None:
        return None
    bestaetigend = _bestaetigende(oib)
    if not bestaetigend or any(not e.raum_referenzen for e in bestaetigend):
        return None
    return {
        ref.raum_id
        for e in bestaetigend
        for ref in e.raum_referenzen
        if ref.floor == floor
    }


def gate_summary(oib: OibBefund) -> dict:
    """Audit-Block für `render_summary["oib"]` — Stufen je Gebäudeteil + Gate-Zustand."""
    offen = flaechen_trigger_offen(oib)
    bestaetigend = _bestaetigende(oib)
    raum_genau = bool(bestaetigend) and all(e.raum_referenzen for e in bestaetigend)
    hinweise = [_HINWEIS_RAUM_GENAU if offen and raum_genau else _HINWEIS_GLOBAL]
    if not offen and any(e.stufe == "review_required" for e in oib.ergebnisse):
        hinweise.append(
            "OIB-Erforderlichkeit review_required — Antipanik-Flächen-Trigger bleibt "
            "zu (fail-closed), bis der Befund geklärt ist."
        )
    return {
        "stufen": {e.gebaeudeteil_id: e.stufe for e in oib.ergebnisse},
        "flaechen_trigger_gate": "offen" if offen else "zu",
        "raum_genau": offen and raum_genau,
        "hinweise": hinweise,
    }
