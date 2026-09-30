"""Die Gate-Regel des Türstapels S4a → S4b → S5b → S5c als eine Funktion.

``pruefe_gate(vorher, nachher)`` vergleicht zwei Messungen im Format von
``gate_messung.messung`` und gibt die Verstöße im Klartext zurück — leere Liste
heißt: der Stapel darf gemerged werden. Beide Stände müssen vollständig sein;
fehlt ein Wert, ist das ein Verstoß und kein stilles Bestehen.

Die Bedingungen (Owner-Vorgabe, § 3 des Gate-Auftrags; (0) ist die Vorbedingung):
  (0) Vergleichbarkeit, VOR allem anderen: dieselben 7 Eingabe-DXF (SHA-256),
      dasselbe Referenzpaket (SHA-256) und dieselben Toleranzen in beiden
      Ständen — sonst vergleicht man zwei verschiedene Messungen und jede
      weitere Aussage ist wertlos. Dazu muss der Nachher-Stand mit sauberem
      Arbeitsbaum unter src/ und scripts/ gemessen sein
      (``meta.arbeitsbaum_src_scripts_sauber is True``), sonst gehören die
      Zahlen zu keinem Commit. Fehlt ``meta`` auf EINER Seite ganz (synthetische
      Messungen der Regel-Tests), wird (0) übersprungen — die Regel selbst lässt
      sich auch ohne Herkunft prüfen.
  (1) keine der 18 Erwartungen fällt von BESTANDEN ab. Gemessen wird gegen
      JEDE Nicht-BESTANDEN-Folge: auch BESTANDEN → NICHT_MESSBAR zählt als
      Verstoß. Die Owner-Vorgabe nennt nur NICHT_BESTANDEN; NICHT_MESSBAR ist
      hier bewusst die sicherere Seite, weil eine Erwartung, die sich nicht mehr
      messen lässt, den Beleg verliert statt ihn zu erbringen. Der umgekehrte
      Weg NICHT_MESSBAR → NICHT_BESTANDEN ist dagegen KEIN Verstoß: die
      Owner-Regel zählt nur Verluste von BESTANDEN, und ein Fall, der vorher
      keinen Beleg trug, verliert auch keinen. Das ist bewusst so belassen;
      heute trägt kein Fall der Nullmessung NICHT_MESSBAR. Zusätzlich muss der
      Nenner 18 bleiben und die IDs müssen dieselben sein (Reihenfolge der
      Referenz) — sonst ist der Vergleich selbst wertlos.
  (2) M17-02-b UND M17-04-c sind BESTANDEN, und M17-02-a bleibt BESTANDEN: die
      drei Durchgänge zwischen den Bädern verschwinden, an der Sonde O steht
      genau eine Türverbindung MIT Türblatt (Lesart B, Entscheidung Enis
      2026-09-18) UND die Wand bleibt erkannt. Beide roten Fälle müssen drehen.
  (3) keine Gate-Kennzahl aus M1-M4 steigt — je Plan (alle 7) und je Kennzahl
      (``gate_m1_m4.GATE_KENNZAHLEN``) muss nachher ≤ vorher gelten. Jede
      Kennzahl muss in BEIDEN Ständen stehen und eine Zahl ≥ 0 sein (int/float,
      kein bool, kein NaN). Fließkommazahlen werden mit ``TOLERANZ`` verglichen
      (nachher ≤ vorher + 0,001), Ganzzahlen exakt.
  (4) OG1: Türen mit raum_a == raum_b sind null.
  (5) OG1: die Einraum-Wohnungen sinken (echt kleiner, nicht nur gleich).
  (6) Rennweg OG3: ``segmente_graph`` ≥ 1 UND ``anker_in_wohnung_privat`` == 0.
      Das ist wörtlich die Aussage der beiden Tests ``test_soll_segmente_aus_graph``
      und ``test_keine_anker_in_wohnung_privat`` (tests/naht/test_soll_rennweg.py),
      die auf dem Türstapel-Branch als strict-xfail geführt werden (Grund: „S4a
      allein, Türstapel unvollständig, muss vor Merge XPASS sein"). Vor dem Merge
      müssen sie XPASS sein — (6) prüft genau das an den Zahlen, damit das Gate
      nicht davon abhängt, ob jemand den Marker rechtzeitig entfernt. Gemessen
      wird nur der NACHHER-Stand: die Aussage ist absolut, kein Vergleich. Fehlt
      der Abschnitt ``og3``, ist das ein Verstoß und kein stilles Bestehen.
"""
from __future__ import annotations

import math

from gate_m1_m4 import GATE_KENNZAHLEN, PLAENE

NENNER = 18
TOLERANZ = 0.001


def _m17_status(messung: dict) -> dict[str, str]:
    return {e["id"]: e["status"] for e in messung.get("m17", [])}


def _pruefe_vergleichbarkeit(vorher: dict, nachher: dict) -> list[str]:
    """(0) Messen beide Stände dasselbe? Ohne ``meta`` übersprungen."""
    mv, mn = vorher.get("meta"), nachher.get("meta")
    if not mv or not mn:
        return []
    verstoesse = []
    for plan in PLAENE:
        alt = (mv.get("dxf") or {}).get(plan)
        neu = (mn.get("dxf") or {}).get(plan)
        if alt != neu:
            verstoesse.append(
                f"(0) andere Eingabe-DXF für {plan}: {alt or 'fehlt'} → {neu or 'fehlt'}")
    if mv.get("referenz_sha256") != mn.get("referenz_sha256"):
        verstoesse.append(
            f"(0) anderes Referenzpaket: {mv.get('referenz_sha256') or 'fehlt'} → "
            f"{mn.get('referenz_sha256') or 'fehlt'}")
    if mv.get("toleranzen") != mn.get("toleranzen"):
        verstoesse.append(
            f"(0) andere Toleranzen: {mv.get('toleranzen')} → {mn.get('toleranzen')}")
    if mn.get("arbeitsbaum_src_scripts_sauber") is not True:
        verstoesse.append(
            "(0) Nachher-Stand mit unsauberem Arbeitsbaum unter src/ oder scripts/ gemessen "
            f"(arbeitsbaum_src_scripts_sauber={mn.get('arbeitsbaum_src_scripts_sauber')!r}) — "
            "die Zahlen gehören zu keinem Commit")
    return verstoesse


def _pruefe_m17(vorher: dict, nachher: dict) -> list[str]:
    ids_v = [e["id"] for e in vorher.get("m17", [])]
    ids_n = [e["id"] for e in nachher.get("m17", [])]
    verstoesse = []
    if len(ids_n) != NENNER:
        verstoesse.append(
            f"(1) Nenner: {len(ids_n)} Erwartungen gemessen, erwartet sind {NENNER}")
    if ids_n != ids_v:
        fehlend = [i for i in ids_v if i not in ids_n]
        neu = [i for i in ids_n if i not in ids_v]
        verstoesse.append(
            "(1) andere Erwartungen als im Vorher-Stand: "
            f"fehlend {fehlend or 'keine'}, neu {neu or 'keine'}"
            + ("" if fehlend or neu else " (nur die Reihenfolge weicht ab)"))
    vor, nach = _m17_status(vorher), _m17_status(nachher)
    for eid in ids_v:
        if vor[eid] == "BESTANDEN" and nach.get(eid) != "BESTANDEN":
            verstoesse.append(
                f"(1) {eid} fällt von BESTANDEN auf {nach.get(eid) or 'nicht gemessen'}")
    for eid in ("M17-02-a", "M17-02-b", "M17-04-c"):
        if nach.get(eid) != "BESTANDEN":
            verstoesse.append(f"(2) {eid} ist {nach.get(eid) or 'nicht gemessen'}, "
                              "erwartet: BESTANDEN")
    return verstoesse


def _ist_zahl(wert) -> bool:
    """int/float ≥ 0 — bool und NaN zählen nicht als Zahl."""
    return (isinstance(wert, (int, float)) and not isinstance(wert, bool)
            and not math.isnan(wert) and wert >= 0)


def _pruefe_m1_m4(vorher: dict, nachher: dict) -> list[str]:
    verstoesse = []
    for kennzahl in GATE_KENNZAHLEN:
        skript, kopf = kennzahl.split(".")
        for plan in PLAENE:
            werte = []
            for seite, messung in (("Vorher", vorher), ("Nachher", nachher)):
                werte.append((messung.get("m1_m4", {}).get(skript, {}).get(plan) or {}).get(kopf))
                if werte[-1] is None:
                    verstoesse.append(f"(3) {kennzahl} fehlt im {seite}-Stand für Plan {plan}")
            alt, neu = werte
            if alt is None or neu is None:
                continue
            keine_zahl = [f"{seite} {w!r}" for seite, w in (("vorher", alt), ("nachher", neu))
                          if not _ist_zahl(w)]
            if keine_zahl:
                verstoesse.append(
                    f"(3) {kennzahl} in {plan} ist keine Zahl ≥ 0: {', '.join(keine_zahl)}")
                continue
            # Flächen sind Fließkommazahlen — Rechen-Rauschen ist kein Rückschritt.
            grenze = alt + (TOLERANZ if isinstance(alt, float) or isinstance(neu, float) else 0)
            if neu > grenze:
                verstoesse.append(f"(3) {kennzahl} steigt in {plan}: {alt} → {neu}")
    return verstoesse


def _pruefe_og1(vorher: dict, nachher: dict) -> list[str]:
    verstoesse = []
    gleich = nachher.get("og1", {}).get("tueren_raum_a_gleich_b")
    if gleich != 0:
        verstoesse.append(f"(4) Türen mit raum_a == raum_b: {gleich}, erwartet: 0")
    alt = vorher.get("og1", {}).get("einraum_wohnungen")
    neu = nachher.get("og1", {}).get("einraum_wohnungen")
    if alt is None or neu is None:
        verstoesse.append(f"(5) Einraum-Wohnungen nicht vergleichbar: vorher {alt}, nachher {neu}")
    elif neu >= alt:
        verstoesse.append(f"(5) Einraum-Wohnungen sinken nicht: {alt} → {neu}")
    return verstoesse


def _pruefe_og3(nachher: dict) -> list[str]:
    """(6) Rennweg OG3: Wege aus dem Graphen, keine Anker in Privatwohnungen."""
    og3 = nachher.get("og3")
    if not og3:
        return ["(6) Rennweg OG3 nicht gemessen — Abschnitt »og3« fehlt"]
    verstoesse = []
    graph = og3.get("segmente_graph")
    if not _ist_zahl(graph) or graph < 1:
        verstoesse.append(
            f"(6) Rennweg OG3 ohne GRAPH-Segment: segmente_graph={graph!r}, erwartet: >= 1")
    anker = og3.get("anker_in_wohnung_privat")
    if not _ist_zahl(anker) or anker != 0:
        verstoesse.append(
            f"(6) Anker in WOHNUNG_PRIVAT (Rennweg OG3): {anker!r}, erwartet: 0")
    return verstoesse


def pruefe_gate(vorher: dict, nachher: dict) -> list[str]:
    """Verstöße gegen die Gate-Regel im Klartext; leere Liste = Gate erfüllt."""
    return (_pruefe_vergleichbarkeit(vorher, nachher)
            + _pruefe_m17(vorher, nachher)
            + _pruefe_m1_m4(vorher, nachher)
            + _pruefe_og1(vorher, nachher)
            + _pruefe_og3(nachher))
