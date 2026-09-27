"""wohnungsklasse — Klasse eines GANG/VORRAUM MIT Stiegenhaustür, zweistufig,
plus der Fail-Safe-Riegel, der entscheidet, wem Notlicht entzogen wird.

Verfahren nach ``docs/GATE_TUERSTAPEL.md`` § 6g in der Fassung der
OWNER-ENTSCHEIDE VOM 2026-09-21 (früh und nachmittags, Board 4-7); sie gehen
dem Stand § 6g (2026-09-20) vor. Über allem steht der Grundsatz des Owners:
**im Zweifel Notlicht behalten. Fehlendes Notlicht ist gefährlich,
überflüssiges nur teurer.** Wo eine Regel nicht greift oder sich
widerspricht, wird NICHT entzogen.

**Zwei getrennte Fragen (Owner-Grundsatz 2026-09-22, geht vor):** (a)
„Bekommt der Raum Notlicht?" — fail-safe, im Zweifel ja; nur hier gilt der
Tiebreak von Board 4, und ein voll ankerbestätigter Fixpunkt geht ihm vor.
(b) „Zu welcher Wohnung gehört der Raum?" — ausschließlich rohe Türen
(``wohnungszugehoerigkeit``); keine Regel zu (a) zerteilt eine Wohnung.

**Einbahn (Board 7):** rohe Türrolle → Klasse → korrigierte Rolle →
Fluchtweg, nie zurück. Die Ankerregel liest nur die ROHEN Rollen (so, wie die
Türerkennung sie liefert); die korrigierten Rollen leitet
``korrigierte_rollen`` erst aus der fertigen Klassifikation ab, und nur
Fluchtweg und Zirkulation lesen sie. ``tuer_detail`` bleibt roh.

Die Regel aus § 6b ist zirkulär („erschließt zwei Wohnungen" hängt an den
Klassen der Nachbarn, die daran hängen, ob dieser Gang allgemein ist). Der
Owner löst das zweistufig:

1. **Ankerregel zuerst, ohne Iteration** (``ankerurteil``/``schritt1``):
   Erreichbarkeit vom STIEGENHAUS über Türen. Sie entscheidet **nur PRIVAT
   endgültig** — F11 ist ein UND: „ALLGEMEIN nur, wenn vom Stiegenhaus ohne
   Wohnungseingang erreichbar UND mindestens zwei Wohnungen oder ein Ausgang
   darüber erschlossen werden." Die Erreichbarkeit ist bloß die VORAUSSETZUNG:

   * nur über eine ``wohnungseingang``-Tür **mit Türblatt** erreichbar →
     ``WOHNUNG_PRIVAT``, endgültig, keine weitere Prüfung;
   * ohne Wohnungseingang erreichbar → offen an Schritt 2;
   * nur durch eine **blattlose** Öffnung getrennt → ebenfalls offen an
     Schritt 2 (eine blattlose Öffnung schließt keine Wohnung ab — die
     Normfrage dazu liegt bei Enis, siehe Bericht);
   * gar nicht erreichbar → offen an Schritt 2.

   Das ist Topologie und TÜRTYP, **keine Raumklasse** — ``_erreichbar``
   bekommt darum Raum-IDs und Türen, keine ``Raum``-Objekte, und kann
   ``nutzungsklasse`` nicht lesen.
2. **Erschließungsregel** (``schritt2``) auf allem, was Schritt 1 offen lässt:
   ``PRIVAT`` genau dann, wenn der Raum genau EINE Wohnung erschließt und
   nichts Allgemeines — keinen AUSGANG, keinen ALLGEMEINEN NEBENRAUM
   (Nutzungsklasse ``ALLGEMEIN_NEBENRAUM`` — Kellerabteil, Keller, Technik,
   Müll, Fahrrad, Kinderwagen, Waschküche, Lager; die Menge steht in
   ``nutzungsklasse.py``), keine zweite Wohnung. Sonst ``ALLGEMEIN`` — auch
   bei NULL Wohnungen (Owner Board 5: „Ein Raum, der null Wohnungen
   erschließt (Podest, Foyer), kann nicht privat sein"). „Erschließt" zählt
   TRANSITIV über allgemeine Räume (``_erschliesst``). Der Nebenraum-Zweig
   ist die Owner-Erweiterung vom 2026-09-21: **in UG/KG gibt es keine
   Wohnungen — ein Kellergang würde sonst privat und verlöre sein
   Notlicht.** Iterativ bis zum Fixpunkt, Start bei ``ALLGEMEIN`` (Board 4:
   von zwei Fixpunkten gilt der, der Notlicht behält), Deckel ``DECKEL``
   Runden, Oszillation → unbestimmt mit Grund.
3. **Unbestimmt statt Raten**: ``nutzungsklasse`` bleibt ``None`` (Contract:
   „None/leer = unbestimmt") und der Grund geht als Warnung in den Bericht.
   Ein unbestimmter Raum wird KONSERVATIV behandelt — er ist nicht privat,
   verliert also weder Leuchte noch Anker und bleibt Knoten im Fluchtweg-Graph.

**Fail-Safe-Riegel (Owner-Entscheid 2026-09-21, ``bestaetigt_privat``).**
Notlicht wird NUR dort entzogen, wo die ANKERREGEL privat BESTÄTIGT. Daraus
folgt dreierlei, und es gilt unabhängig davon, welche Stufe die Klasse gesetzt
hat:

* Ein Raum, den die Ankerregel als privat bestätigt, verliert beide Flags
  (R3), seine Anker und seine Leuchten (R4).
* Ein Raum, den die Ankerregel OHNE Wohnungseingang erreicht, den die alte
  Verfeinerung aber privat gemacht hat, wird ``ALLGEMEIN_ERSCHLIESSUNG`` und
  behält alles — „die Ankerregel sagt allgemein, also gilt allgemein".
* Ein Raum, den die Ankerregel gar nicht auswerten kann, wird als unbestimmt
  geführt und behält alles. Der Owner ordnet diesen Fall ausdrücklich NICHT
  der Klassifikation zu: „das ist ein Tür- oder Raumerkennungsloch"
  (Messfall für S4c und S3b).
* Liegt ein Kandidat des Geltungsbereichs V2 außerhalb der bestätigten Menge
  (Schritt 2 hat ihn privat gemacht, die Ankerregel bestätigt das nicht),
  behält er ebenfalls alles.

Geltungsbereich **V2 (eng)** für das zweistufige Verfahren: nur GANG/VORRAUM
mit mindestens einer Tür zu einem STIEGENHAUS (``kandidaten``). Für alle
anderen bleibt ``wohnungen._verfeinere_gang_privat`` zuständig — unter
demselben Riegel.
"""
from __future__ import annotations

from collections import deque

from shapely.geometry import Point, Polygon
from shapely.ops import nearest_points

from notbeleuchtung.hauptengine.contracts.raum_modell import Anker, Raum, Tuer

from .nutzungsklasse import nutzungsklasse_fuer
from .tuer_zuordnung import AUSSEN, KEIN_RAUM

#: Räume, die überhaupt in den Geltungsbereich fallen können.
SCOPE_TYPEN = frozenset({"GANG", "VORRAUM"})
#: G4 (Owner 2026-09-22): Aufenthaltsräume, die eine Wohnung belegen — die
#: Kanon-Namen aus ``raumtyp._TYP_MAP``. Der Owner-Entscheid R4 (2026-09-22)
#: nennt zwei Erweiterungen, beide ausdrücklich NICHT in S7:
#: * KINDERZIMMER steht im Kanon und WIRD Aufenthaltsraum — als **eigener
#:   Slice nach dem Türstapel**; auf den 12 Plänen heute 0 Fälle, Wirkung 0.
#: * „Wohnküche" fehlt im Kanon und ist **Board-Punkt an @Enis** — nicht selbst
#:   einführen. Bis dahin kein Aufenthaltsraum (fail-safe: Notlicht bleibt).
AUFENTHALTSRAUM = frozenset({"ZIMMER", "WOHNZIMMER", "SCHLAFZIMMER", "KÜCHE"})
#: Schritt 2: so viele Fixpunkt-Runden, danach gilt der Raum als unbestimmt.
DECKEL = 10

PRIVAT = "WOHNUNG_PRIVAT"
ALLGEMEIN = "ALLGEMEIN_ERSCHLIESSUNG"
NEBENRAUM = "ALLGEMEIN_NEBENRAUM"

#: Urteil der Ankerregel (Schritt 1 UND Fail-Safe-Riegel lesen dasselbe).
A_PRIVAT, A_ALLGEMEIN, A_UNKLAR = "privat", "allgemein", "unklar"


def _seiten(t: Tuer) -> tuple[str | None, str | None]:
    return t.von_raum, t.nach_raum


def kandidaten(raeume: list[Raum], tueren: list[Tuer]) -> set[str]:
    """Geltungsbereich V2: GANG/VORRAUM mit mindestens einer Tür zum STIEGENHAUS."""
    stiegenhaus = {r.id for r in raeume if r.raum_typ == "STIEGENHAUS"}
    scope = {r.id for r in raeume if r.raum_typ in SCOPE_TYPEN}
    out: set[str] = set()
    for t in tueren:
        a, b = _seiten(t)
        if a in scope and b in stiegenhaus:
            out.add(a)
        if b in scope and a in stiegenhaus:
            out.add(b)
    return out


#: Wie weit ``_erreichbar`` durch ``wohnungseingang``-Türen laufen darf.
NIE, NUR_BLATTLOS, IMMER = "nie", "nur_blattlos", "immer"


def _erreichbar(start: set[str], tueren: list[Tuer],
                durch_wohnungseingang: str) -> dict[str, str]:
    """BFS über Türen ab ``start``; liefert ``{raum_id: tuer_id}``.

    ``durch_wohnungseingang``: ``NIE`` sperrt jeden Wohnungseingang,
    ``NUR_BLATTLOS`` lässt nur die blattlosen Öffnungen passieren (ein
    Wohnungseingang MIT Türblatt schließt ab), ``IMMER`` alle.

    Die Tür im Ergebnis ist die, die der Grund nennen muss (§ 6g Punkt 4,
    „über welche Tür"): bei ``NIE`` die Tür, über die der Raum erreicht wurde;
    bei ``NUR_BLATTLOS`` die letzte blattlose Wohnungseingangs-Öffnung auf dem
    Pfad; bei ``IMMER`` der letzte Wohnungseingang MIT Türblatt. Vorher stand
    dort immer die letzte Tür des Pfads — gemessen nannte OG1 ``raum_4`` so
    eine blattlose Zimmertür als „Wohnungseingangstür mit Türblatt".

    Bekommt ausdrücklich nur IDs und Türen — die Ankerregel kann damit keine
    Raumklasse lesen (§ 6g, „per Konstruktion, nicht per Kommentar").
    """
    nachbarn: dict[str, list[tuple[str, str]]] = {}
    for t in tueren:
        a, b = _seiten(t)
        # Über die Sentinels wird NICHT gelaufen: sonst verbindet „AUSSEN"
        # oder „KEIN_RAUM" als Scheinknoten zwei Räume, die keine Tür teilen.
        if not a or not b or {a, b} & {AUSSEN, KEIN_RAUM}:
            continue
        we = t.tuer_detail == "wohnungseingang"
        if we and (durch_wohnungseingang == NIE
                   or (durch_wohnungseingang == NUR_BLATTLOS
                       and not t.ohne_tuerblatt)):
            continue
        if durch_wohnungseingang == NIE:
            merken = True
        elif durch_wohnungseingang == NUR_BLATTLOS:
            merken = we                      # hier nur blattlose passierbar
        else:
            merken = we and not t.ohne_tuerblatt
        nachbarn.setdefault(a, []).append((b, t.id, merken))
        nachbarn.setdefault(b, []).append((a, t.id, merken))
    gesehen: dict[str, str] = {}
    q = deque(sorted(start))
    besucht = set(start)
    while q:
        rid = q.popleft()
        for nachbar, tid, merken in sorted(nachbarn.get(rid, [])):
            if nachbar in besucht:
                continue
            besucht.add(nachbar)
            gesehen[nachbar] = tid if merken else gesehen.get(rid, tid)
            q.append(nachbar)
    return gesehen


def ankerurteil(raeume: list[Raum],
                tueren: list[Tuer]) -> dict[str, tuple[str, str]]:
    """Für JEDEN GANG/VORRAUM ``(urteil, grund)`` — die EINE Ankerregel.

    Schritt 1 und der Fail-Safe-Riegel lesen dieselbe Funktion; sie wird nicht
    zweimal gebaut (Owner-Auflage). Reine Topologie plus Türtyp, damit
    reihenfolgeunabhängig und frei von jeder Raumklasse.

    PRIVAT heißt: JEDER Weg vom Stiegenhaus läuft durch einen Wohnungseingang
    MIT Türblatt — der schließt die Wohnung ab, auch wenn dahinter noch eine
    blattlose Öffnung folgt. UNKLAR (blattlos) heißt: den Raum trennen vom
    Stiegenhaus NUR blattlose Öffnungen (E1: „eine blattlose Öffnung schließt
    keine Wohnung ab").
    """
    stiegenhaus = {r.id for r in raeume if r.raum_typ == "STIEGENHAUS"}
    ohne_we = _erreichbar(stiegenhaus, tueren, NIE)
    blattlos = _erreichbar(stiegenhaus, tueren, NUR_BLATTLOS)
    alle = _erreichbar(stiegenhaus, tueren, IMMER)
    out: dict[str, tuple[str, str]] = {}
    for r in raeume:
        if r.raum_typ not in SCOPE_TYPEN:
            continue
        if r.id in ohne_we:
            out[r.id] = (A_ALLGEMEIN, ("vom Stiegenhaus ohne Wohnungseingang "
                                       f"erreichbar (über {ohne_we[r.id]})"))
        elif r.id in blattlos:
            out[r.id] = (A_UNKLAR, ("vom Stiegenhaus nur durch die Öffnung "
                                    f"{blattlos[r.id]} OHNE Türblatt getrennt — "
                                    "eine blattlose Öffnung schließt keine "
                                    "Wohnung ab"))
        elif r.id in alle:
            out[r.id] = (A_PRIVAT, ("nur über die Wohnungseingangstür "
                                    f"{alle[r.id]} (mit Türblatt) erreichbar"))
        else:
            out[r.id] = (A_UNKLAR, ("vom Stiegenhaus über keine Tür erreichbar "
                                    "— Tür- oder Raumerkennungsloch, kein "
                                    "Klassifikationsproblem"))
    return out


def schritt1(raeume: list[Raum], tueren: list[Tuer],
             offene: set[str]) -> dict[str, tuple[str | None, str]]:
    """Ankerschritt: ``{raum_id: (WOHNUNG_PRIVAT, grund)}``.

    Er entscheidet **nur PRIVAT endgültig** (Owner-Korrektur 2026-09-21, das
    UND aus F11). Alles andere steht NICHT im Ergebnis und geht offen an
    Schritt 2 — auch der nur durch eine blattlose Öffnung getrennte Raum, der
    in Runde 3 noch sofort unbestimmt wurde. Nie ein Raum des Riegels
    (``riegel_nie_privat``, Owner 2026-09-22: „auch nicht in Schritt 1").
    """
    urteil = ankerurteil(raeume, tueren)
    sperre = riegel_nie_privat(raeume, tueren)
    return {rid: (PRIVAT, f"Schritt 1: {urteil[rid][1]}")
            for rid in sorted(offene)
            if rid not in sperre and urteil.get(rid, (A_UNKLAR, ""))[0] == A_PRIVAT}


def riegel_nie_privat(raeume: list[Raum], tueren: list[Tuer]) -> dict[str, str]:
    """G3 (Owner 2026-09-22): „Ein Raum mit Hauseingang, Tür ins Freie oder Tür
    zu einem allgemeinen Nebenraum ist in keinem Schritt PRIVAT, auch nicht in
    Schritt 1 und nicht an der E8-Grenze." ``{raum_id: grund}`` für jeden
    GANG/VORRAUM mit einer solchen Tür; Nebenraum = Nutzungsklasse
    ``ALLGEMEIN_NEBENRAUM`` des Raumtyps (``nutzungsklasse.py``). Liest nur
    Raumtyp, Tür-Topologie und rohe Rolle.

    **Asymmetrie, offengelegt** (Reviewer Runde 10, Linse Regel, Hinweis 6):
    „Tür ins Freie" zählt hier JEDE Tür nach ``AUSSEN``, auch eine Balkontür;
    der (b)-Ursprung in ``wohnungszugehoerigkeit`` schließt die Balkontür
    ausdrücklich aus. Die Richtung ist sicher (der Riegel nimmt kein Notlicht,
    er verhindert nur den Entzug), und auf den 12 Prüfplänen hat kein
    GANG/VORRAUM eine Balkontür."""
    scope = {r.id for r in raeume if r.raum_typ in SCOPE_TYPEN}
    neben = {r.id for r in raeume if nutzungsklasse_fuer(r.raum_typ) == NEBENRAUM}
    out: dict[str, str] = {}
    for t in sorted(tueren, key=lambda x: x.id):
        for a, b in ((t.von_raum, t.nach_raum), (t.nach_raum, t.von_raum)):
            if a not in scope or a in out:
                continue
            if b == AUSSEN:
                out[a] = f"Tür ins Freie {t.id}"
            elif t.tuer_detail == "hauseingang":
                out[a] = f"Hauseingang {t.id}"
            elif b in neben:
                out[a] = f"Tür {t.id} zum allgemeinen Nebenraum {b}"
    return out


def _erschliesst(rid: str, tueren: list[Tuer], klasse: dict[str, str | None],
                 stiegenhaus: set[str] = frozenset()
                 ) -> tuple[int, bool, list[str]]:
    """``(Zahl erschlossener Wohnungen, Ausgang ins Freie?, Nebenräume)``.

    § 6b: jede getrennte private Komponente zählt als eigene Wohnung, auch ein
    einzelnes WC. Nebenräume sind Räume der Nutzungsklasse
    ``ALLGEMEIN_NEBENRAUM`` (Owner-Erweiterung 2026-09-21).

    **Transitiv** (Owner Board 5, 2026-09-21): Z ist von ``rid`` erschlossen,
    wenn Z über Türen erreichbar ist und alle Zwischenräume nicht privat
    sind. Eine erreichte Wohnung zählt und beendet den Weg dort (nicht in die
    Wohnung hinein). Das STIEGENHAUS ist Ursprung, nicht Durchgang
    (Planer-Auslegung): was nur über das Stiegenhaus erreichbar ist,
    erschließt das Stiegenhaus. Ausgang wie bisher: Tür ins Freie (AUSSEN).
    Liest nur Topologie und Klassen — keine Türrolle.
    """
    privat = {r for r, k in klasse.items() if k == PRIVAT and r != rid}
    eltern = {r: r for r in privat}

    def find(x: str) -> str:
        while eltern[x] != x:
            eltern[x] = eltern[eltern[x]]
            x = eltern[x]
        return x

    nachbarn: dict[str, list[str]] = {}
    for t in tueren:
        a, b = _seiten(t)
        if a in privat and b in privat:
            eltern[find(a)] = find(b)
        if a and b:
            nachbarn.setdefault(a, []).append(b)
            nachbarn.setdefault(b, []).append(a)
    wurzeln: set[str] = set()
    nebenraeume: set[str] = set()
    ins_freie = False
    besucht = {rid}
    q = deque([rid])
    while q:
        for y in nachbarn.get(q.popleft(), ()):
            if y == AUSSEN:
                ins_freie = True
            elif y != KEIN_RAUM and y not in besucht:
                besucht.add(y)
                if y in privat:
                    wurzeln.add(find(y))
                    continue
                if klasse.get(y) == NEBENRAUM:
                    nebenraeume.add(y)
                if y not in stiegenhaus:
                    q.append(y)
    return len(wurzeln), ins_freie, sorted(nebenraeume)


def schritt2_urteil(rid: str, tueren: list[Tuer], klasse: dict[str, str | None],
                    stiegenhaus: set[str], runde: int) -> tuple[str, str]:
    """Eine Anwendung der Erschließungsregel auf ``rid`` (Board 5): PRIVAT
    genau bei EINER Wohnung und nichts Allgemeinem, sonst ALLGEMEIN — auch
    bei null Wohnungen. Liefert ``(klasse, grund)``."""
    n, ins_freie, neben = _erschliesst(rid, tueren, klasse, stiegenhaus)
    privat = n == 1 and not ins_freie and not neben
    teile = [f"{n} Wohnung(en)"]
    if ins_freie:
        teile.append("eine Tür ins Freie")
    if neben:
        teile.append(f"allgemeine(r) Nebenraum/-räume {', '.join(neben)}")
    grund = (f"Schritt 2: erschließt (transitiv) {' und '.join(teile)} → "
             f"{'privat' if privat else 'allgemein'} (Runde {runde})")
    return (PRIVAT if privat else ALLGEMEIN), grund


def schritt2(tueren: list[Tuer], basis: dict[str, str | None], offene: set[str],
             stiegenhaus: set[str] = frozenset()
             ) -> tuple[dict[str, str | None], dict[str, str]]:
    """Erschließungsregel (``schritt2_urteil``) auf ``offene``, iterativ bis
    zum Fixpunkt. ``basis`` = Klassen aller übrigen Räume. Die offenen Räume
    starten bei ``ALLGEMEIN`` (Owner Board 4: hat die Regel mehrere
    Fixpunkte, gilt der, der Notlicht behält) — Schritt 1 hat sie nicht
    entschieden, der statische Default wäre eine Vorentscheidung. Konvergiert
    es nicht in ``DECKEL`` Runden, bleiben sie unbestimmt.
    """
    klasse: dict[str, str | None] = dict(basis)
    for rid in offene:
        klasse[rid] = ALLGEMEIN
    gruende: dict[str, str] = {}
    for runde in range(1, DECKEL + 1):
        neu: dict[str, str | None] = {}
        for rid in sorted(offene):
            neu[rid], gruende[rid] = schritt2_urteil(rid, tueren, klasse,
                                                     stiegenhaus, runde)
        if all(klasse[rid] == neu[rid] for rid in offene):
            return {rid: klasse[rid] for rid in offene}, gruende
        klasse.update(neu)
    # Nur behaupten, was gemessen ist: die Iteration kommt nicht zur Ruhe.
    # Ob die Regel einen Fixpunkt HAT, sagt das nicht — ein Oszillator aus
    # zwei gleichen Startwerten hat oft asymmetrische (Reviewer Runde 5, O4).
    return ({rid: None for rid in offene},
            {rid: f"Schritt 3: Schritt 2 oszilliert — die Iteration erreicht in "
                  f"{DECKEL} Runden keinen Fixpunkt (ob die Regel einen hat, ist "
                  "nicht geprüft) — unbestimmt statt Raten" for rid in offene})


def klassifiziere(raeume: list[Raum],
                  tueren: list[Tuer]) -> tuple[dict[str, str | None], dict[str, str]]:
    """``({raum_id: klasse|None}, {raum_id: grund})`` für alle Kandidaten."""
    offene = kandidaten(raeume, tueren)
    eins = schritt1(raeume, tueren, offene)
    klassen: dict[str, str | None] = {rid: k for rid, (k, _) in eins.items()}
    gruende = {rid: g for rid, (_, g) in eins.items()}
    for rid, g in riegel_nie_privat(raeume, tueren).items():
        if rid in offene:
            klassen[rid], gruende[rid] = ALLGEMEIN, f"Riegel (G3): {g} → nie privat"
    rest = offene - set(klassen)
    if rest:
        basis: dict[str, str | None] = {r.id: r.nutzungsklasse for r in raeume}
        basis.update(klassen)
        zwei, gruende_zwei = schritt2(
            tueren, basis, rest,
            {r.id for r in raeume if r.raum_typ == "STIEGENHAUS"})
        klassen.update(zwei)
        gruende.update({rid: gruende_zwei[rid] for rid in rest})
    return klassen, gruende


def bestaetigt_privat(raeume: list[Raum], tueren: list[Tuer]) -> set[str]:
    """Die EINZIGE Menge, der R3/R4 Notlicht entziehen (Fail-Safe, Owner
    2026-09-21): GANG/VORRAUM der Klasse ``WOHNUNG_PRIVAT``, die die
    ANKERREGEL als privat BESTÄTIGT — und (Owner 2026-09-22) nur, wenn in
    derselben Wohnung nach rohen Türen (``wohnungszugehoerigkeit``)
    mindestens ein Aufenthaltsraum liegt (G4: „Bad, WC, Abstellraum oder
    untypisierte Räume allein belegen keine Wohnung, dort bleibt Notlicht")
    und kein Riegel greift (G3).

    „Im Zweifel Notlicht behalten": wer hier fehlt — weil die Ankerregel
    widerspricht, weil sie den Raum nicht auswerten kann, weil erst
    Schritt 2 ihn privat gemacht hat oder weil hinter dem Wohnungseingang
    kein Aufenthaltsraum belegt ist — behält Flags, Anker und Leuchten.
    """
    urteil = ankerurteil(raeume, tueren)
    # Die Menge liegt ohne eigenen raum_typ-Filter ganz in GANG/VORRAUM:
    # ``ankerurteil`` bewertet nur den S7-Scope und lässt alles andere auf
    # A_UNKLAR (gemessen Runde 13/14: 12/12 Pläne und 20 000 Zufallstopologien
    # ohne Ausnahme). Auf dieser Invariante ruht die zweite Zusicherung von
    # tests/naht/test_s7_wohnungsklasse.py::test_keine_anker_wo_das_notlicht_
    # entzogen_wurde — sie ist die WEITERE der beiden und bleibt darum wörtlich.
    kandidat = {r.id for r in raeume
                if r.nutzungsklasse == PRIVAT
                and urteil.get(r.id, (A_UNKLAR, ""))[0] == A_PRIVAT}
    if not kandidat:
        return set()
    typ = {r.id: r.raum_typ for r in raeume}
    belegt = {rid for gruppe, _ in wohnungszugehoerigkeit(raeume, tueren)[0]
              if any(typ[x] in AUFENTHALTSRAUM for x in gruppe) for rid in gruppe}
    return kandidat & belegt - set(riegel_nie_privat(raeume, tueren))


def unbestaetigt_privat(raeume: list[Raum], tueren: list[Tuer]) -> set[str]:
    """GANG/VORRAUM der Klasse ``WOHNUNG_PRIVAT``, die die Ankerregel NICHT
    bestätigt — nach dem Riegel sind das die Kandidaten, die erst Schritt 2
    privat gemacht hat (gemessen Runde 7: Rennweg DG1 ``raum_8``). Sie
    behalten ihr Notlicht; für die KORRIGIERTEN Türrollen — also Fluchtweg und
    Zirkulation, Frage (a) — zählen sie als Erschließung (Option W,
    ``wohnungsraeume``). Die Wohnungsgrenze (b) kommt seit dem Owner-Grundsatz
    2026-09-22 allein aus ``wohnungszugehoerigkeit`` (rohe Türen) und liest
    diese Menge NICHT."""
    entzug = bestaetigt_privat(raeume, tueren)
    return {r.id for r in raeume
            if r.raum_typ in SCOPE_TYPEN and r.nutzungsklasse == PRIVAT
            and r.id not in entzug}


def erschliessung_erwiesen(raeume: list[Raum], tueren: list[Tuer]) -> set[str]:
    """E8 (Owner Board 6): die Räume, an denen ein Wohnungseingang MIT Blatt
    die Flur-Verfeinerung begrenzt — die Stiegenhäuser und JEDER Raum, den
    die Ankerregel von dort OHNE Wohnungseingang erreicht, gleich welchen
    Typs (auch ein Zimmer; dieselbe Erreichbarkeit, rohe Rollen, keine
    Klasse). Liegt vor dem Wohnungseingang ein Raum, den die Ankerregel nicht
    erreicht (Tür- oder Raumerkennungsloch), ist nicht belegt, dass die Tür
    eine Wohnung gegen die Erschließung abschließt — dort begrenzt sie nicht
    (Grundsatz: im Zweifel Notlicht behalten; gemessen Muthgasse E2
    ``raum_51``/``raum_94``, Mollgasse EG ``raum_29``/``raum_57``)."""
    stiegenhaus = {r.id for r in raeume if r.raum_typ == "STIEGENHAUS"}
    return set(_erreichbar(stiegenhaus, tueren, NIE)) | stiegenhaus


def loch_raeume(raeume: list[Raum], tueren: list[Tuer]) -> set[str]:
    """Die GANG/VORRAUM, die die Ankerregel vom Stiegenhaus über KEINE Tür
    erreicht — laut Owner (2026-09-21) „ein Tür- oder Raumerkennungsloch, kein
    Klassifikationsproblem" (Messfall S4c/S3b). NICHT dazu gehört der nur
    durch eine blattlose Öffnung getrennte Raum: „eine blattlose Öffnung
    schließt keine Wohnung ab" (E1; Reviewer Runde 7, Linse Naht,
    blockierend 4 — Mollgasse EG ``raum_23``)."""
    stiegenhaus = {r.id for r in raeume if r.raum_typ == "STIEGENHAUS"}
    erreicht = _erreichbar(stiegenhaus, tueren, IMMER)
    return {r.id for r in raeume
            if r.raum_typ in SCOPE_TYPEN and r.id not in erreicht}


def wohnungsraeume(raeume: list[Raum], tueren: list[Tuer]) -> tuple[set[str], set[str]]:
    """``(privat, erschliessung)`` — die Mengen, aus denen die KORRIGIERTEN
    Rollen folgen (Fluchtweg und Zirkulation, also Frage (a) Notlicht); aus
    den fertigen Klassen und der Ankerregel auf den rohen Rollen. Die
    Wohnungszugehörigkeit (b) liest sie NICHT (``wohnungszugehoerigkeit``).

    * privat: Klasse ``WOHNUNG_PRIVAT`` ohne die unbestätigt privaten
      GANG/VORRAUM (Option W, Runde 5: wer Notlicht behält, behält seine
      Zirkulation), dazu die unbestimmten LOCH-Räume (``loch_raeume``) — nach
      dem Owner-Grundsatz 2026-09-22 genau die, die über eine rohe Zimmertür
      an ihre Wohnung gebunden sind.
    * erschliessung: Klasse ``ALLGEMEIN_ERSCHLIESSUNG``, die übrigen
      unbestimmten GANG/VORRAUM (unbestimmt heißt nicht privat — auch der
      nur blattlos getrennte, Runde 8) und die unbestätigt privaten.
    """
    kand = kandidaten(raeume, tueren)
    weich = unbestaetigt_privat(raeume, tueren)
    unbestimmt = {r.id for r in raeume
                  if r.raum_typ in SCOPE_TYPEN and r.nutzungsklasse is None}
    loch = (unbestimmt - kand) & loch_raeume(raeume, tueren)
    privat = ({r.id for r in raeume if r.nutzungsklasse == PRIVAT} - weich) | loch
    erschliessung = ({r.id for r in raeume if r.nutzungsklasse == ALLGEMEIN}
                     | (unbestimmt - loch) | weich)
    return privat, erschliessung


def wohnungsgruppen(privat: set[str], tueren: list[Tuer]) -> list[list[str]]:
    """Die Wohnungen als Raumlisten: Zusammenhang der Wohnungsmenge über die
    Türen, die ROH Zimmertür, Wohnungseingang oder ohne Rolle sind — nicht
    über Balkon-, Stiegenhaus-, Brandschutz- oder Hauseingangstüren. Sortiert
    nach kleinster Raum-ID (deterministisch, ``top_1..n``)."""
    eltern = {rid: rid for rid in privat}

    def find(x: str) -> str:
        while eltern[x] != x:
            eltern[x] = eltern[eltern[x]]
            x = eltern[x]
        return x

    for t in tueren:
        a, b = _seiten(t)
        if (a in privat and b in privat
                and t.tuer_detail in ("zimmertuer", "wohnungseingang", None)):
            eltern[find(a)] = find(b)
    gruppen: dict[str, list[str]] = {}
    for rid in privat:
        gruppen.setdefault(find(rid), []).append(rid)
    return sorted((sorted(g) for g in gruppen.values()), key=lambda g: g[0])


def wohnungseingaenge(gruppe: list[str], tueren: list[Tuer],
                      erschliessung: set[str]) -> list[str]:
    """Die Wohnungseingänge einer Wohnung nach (b), aus ROHEN Rollen und der
    klassenfreien Erschließung von ``wohnungszugehoerigkeit``: eine Tür mit
    genau einer Seite in der Wohnung, die roh ``wohnungseingang`` ist oder als
    ``zimmertuer`` in einen Erschließungsraum führt. Liest keine Klasse und
    keine korrigierte Rolle (E7.2: „die gesamte Klassifikation (…,
    Wohnungsbildung) liest KEINE korrigierte Rolle").

    Die Liste ist NICHT dasselbe wie ``korrigierte_rollen(…) ==
    "wohnungseingang"`` (Frage (a), Fluchtweg): beide lesen verschiedene
    Erschließungs-Begriffe, Gleichheit ginge nur durch Rückspeisen von (a)
    nach (b). Gemessen (S7c Runde 2, 66 Topologien, 12 Prüfpläne) stimmen
    beide Tür für Tür überein, außer: NUR hier, wenn der Raum auf der
    Wohnungsseite für (a) nicht privat ist (unbestimmt, allgemein
    klassifiziert, Option W); NUR korrigiert ausschließlich an einer Tür mit
    anderer roher Rolle als Zimmertür/Wohnungseingang, die S7c an der Grenze
    privat|Erschließung zum Wohnungseingang macht. Auf den 12 Prüfplänen:
    0 Abweichungen.
    Gebunden in ``test_e7_bilde_wohnungen_liest_keine_korrigierte_rolle``."""
    drin = set(gruppe)
    out: list[str] = []
    for t in tueren:
        if (t.von_raum in drin) == (t.nach_raum in drin):
            continue
        andere = t.nach_raum if t.von_raum in drin else t.von_raum
        if t.tuer_detail == "wohnungseingang" or (
                t.tuer_detail == "zimmertuer" and andere in erschliessung):
            out.append(t.id)
    return out


#: R1-Erweiterung, Bedingung C (Owner 2026-09-27): neben einem
#: Aufenthaltsraum belegt einer dieser Räume hinter dem Gang eine Wohnung.
NEBENRAUM_C = frozenset({"BAD", "WC", "ABSTELLRAUM"})


def _gang_einzelraeume(raeume: list[Raum], tueren: list[Tuer], drin: set[str],
                       offen: set[str], loch: set[str]) -> set[str]:
    """R1: die GÄNGE aus ``offen`` (noch in keiner Wohnung), hinter deren rohen
    Wohnungseingängen NUR Einzelräume liegen — jede dahinterliegende
    Raumgruppe hat genau EINEN Raum, und keiner führt aus der Wohnungsmenge
    heraus (Erschließung, ``KEIN_RAUM``, ``AUSSEN``; Muthgasse E2 ``raum_94``
    bindet darum nicht). Sie bilden mit diesen Räumen eine Wohnung.

    Ein VORRAUM oder GANG zählt nie als Einzelraum (Owner 2026-09-27, § 7e
    Frage 3/4): „Vestibül oder Flur hinter einer Wohnungseingangstür zählt
    nicht als Einzelraum … Ein Durchgangsraum ist kein Beleg für eine eigene
    Wohnung, er erschließt nur." Liegt einer hinter einem rohen
    Wohnungseingang des Gangs, bindet der Gang nicht; der Nachbar behält, was
    er ohne R1 hat, und verliert sein Notlicht nicht (im Zweifel Notlicht
    behalten). Im Loch-Fall strukturell ohne Wirkung (§ 6g.5).

    * **Loch-GANG** (``loch``; Owner 2026-09-22): die Einzelraum-Bedingung
      genügt, in der Wirkung unverändert (der Typfilter oben greift dort nie).
    * **Erschlossener GANG** (R1-Erweiterung, Owner 2026-09-27, Fassung A+C —
      der Wohnungsflur hinter der Stiegenhaustür, gemessen Rennweg OG3
      ``raum_10`` seit S3b hinter ``tuer_5``, 940 mm mit Blatt) nur, wenn
      zusätzlich **A** alle übrigen Türen des Gangs — sein Zugang —
      Stiegenhaustüren MIT Türblatt ohne rohe Rolle Wohnungseingang sind
      (ein Hauseingang, eine Tür ins Freie, eine rollenlose Tür zu einem
      anderen Raum oder eine blattlose Öffnung genügt nicht: Mollgasse EG
      ``raum_34``/``raum_39``, Rennweg UG ``raum_12``), und **C** unter den
      Einzelräumen ein Aufenthaltsraum UND ein Bad, WC oder Abstellraum liegt
      (ein Gang vor Studios oder nur vor Nassräumen ist kein Wohnungsflur).

    Reine Topologie der ROHEN Türen und Raumtypen, keine Klasse. Alle
    Kandidaten werden gegen DENSELBEN Stand geprüft, darum hängt das Ergebnis
    nicht an der Reihenfolge.
    """
    typ = {r.id: r.raum_typ for r in raeume}
    groesse = {rid: len(g) for g in wohnungsgruppen(drin, tueren) for rid in g}
    hinter: dict[str, set[str]] = {}
    zugang: dict[str, bool] = {}
    for t in tueren:
        for a, b in ((t.von_raum, t.nach_raum), (t.nach_raum, t.von_raum)):
            if a not in offen or typ.get(a) != "GANG":
                continue
            if t.tuer_detail == "wohnungseingang":
                hinter.setdefault(a, set()).add(b)
            else:                                           # A
                zugang[a] = (zugang.get(a, True) and typ.get(b) == "STIEGENHAUS"
                             and not t.ohne_tuerblatt)
    out: set[str] = set()
    for rid, nachbarn in hinter.items():
        if not all(groesse.get(x) == 1 and typ.get(x) not in SCOPE_TYPEN for x in nachbarn):
            continue
        typen = {typ.get(x) for x in nachbarn}
        if rid in loch or (zugang.get(rid, False)
                           and typen & AUFENTHALTSRAUM and typen & NEBENRAUM_C):
            out.add(rid)
    return out


def wohnungszugehoerigkeit(raeume: list[Raum], tueren: list[Tuer]
                           ) -> tuple[list[tuple[list[str], list[str]]],
                                      set[str], set[str], set[str]]:
    """(b) „Zu welcher Wohnung gehört der Raum? Entscheiden ausschließlich
    rohe Türen: Wohnungseingang ist Grenze, Zimmertür ist innen. Board 4 gilt
    hierfür nie. Eine Regel zu (a) darf keine Wohnung zerteilen." (Owner
    2026-09-22). Liefert ``([(raum_ids, eingangs_tuer_ids)], loch_in_wohnung,
    loch_erschliessung, r1_gaenge)`` — ``r1_gaenge`` sind die Gänge, die R1
    gebunden hat, Loch-Raum oder nicht; ``loch_in_wohnung`` führt davon nur
    die Loch-Räume. (a) liest beide: diese Räume bleiben unbestimmt mit
    Notlicht (``wohnungen.bilde_wohnungen``).

    Liest NUR Raumtyp, Tür-Topologie, rohe Rolle und Türblatt — nie
    ``nutzungsklasse``, nie ein Ergebnis von Schritt 1/2/3, nie den
    Fixpunkt-Tiebreak (G1). Darum kann keine Notlicht-Regel eine Wohnung
    zerteilen.

    * Wohnungsräume nach Typ (statische Klasse ``WOHNUNG_PRIVAT``: Zimmer,
      Küche, Bad, WC, Abstellraum …) gehören immer zu einer Wohnung, wie auf
      HEAD.
    * Erschließung ist, was die Flut vom STIEGENHAUS und von den Ausgängen
      (Tür ins Freie, keine Balkontür) erreicht, ohne einen rohen
      Wohnungseingang MIT Türblatt oder eine rohe Zimmertür zu durchqueren und
      ohne einen Wohnungsraum zu betreten — der Wohnungseingang ist die
      Grenze, die Zimmertür ist innen. Eine blattlose Öffnung schließt keine
      Wohnung ab (E1), die Flut geht durch.
    * Ein GANG/VORRAUM dahinter gehört zur Wohnung. Ein Loch-Raum
      (``loch_raeume``) gehört zu ihr, wenn er über eine rohe Zimmertür an sie
      gebunden ist; sonst — nur über rohe Wohnungseingänge angebunden — ist er
      Erschließung (Owner-Fragebogen 2026-09-22). Ausnahme R1 (Owner
      2026-09-22): ein Loch-GANG, hinter dessen rohen Wohnungseingängen NUR
      Einzelräume liegen, bildet mit ihnen eine Wohnung; ebenso — R1-
      Erweiterung, Owner 2026-09-27, Fassung A+C — ein erschlossener GANG,
      dessen Zugang nur Stiegenhaustüren mit Blatt sind und hinter dem ein
      Aufenthaltsraum und ein Bad/WC/Abstellraum liegen
      (``_gang_einzelraeume``).
    * Die Wohnungen sind die Zusammenhänge darin (``wohnungsgruppen``: innen
      verbinden Zimmertür, Wohnungseingang und Tür ohne Rolle); ihre Eingänge
      sind die Türen zur Erschließung (``wohnungseingaenge``).
    """
    wohnraum = {r.id for r in raeume if r.raum_typ not in SCOPE_TYPEN
                and nutzungsklasse_fuer(r.raum_typ) == PRIVAT}
    scope = {r.id for r in raeume if r.raum_typ in SCOPE_TYPEN}
    ursprung = {r.id for r in raeume if r.raum_typ == "STIEGENHAUS"}
    for t in tueren:
        if AUSSEN in (t.von_raum, t.nach_raum) and t.tuer_detail != "balkontuer":
            ursprung |= {t.von_raum, t.nach_raum} - wohnraum - {AUSSEN, KEIN_RAUM, None}
    flut = [t for t in tueren if t.tuer_detail != "zimmertuer"
            and not {t.von_raum, t.nach_raum} & wohnraum]
    erschlossen = ursprung | set(_erreichbar(ursprung, flut, NUR_BLATTLOS))
    loch = loch_raeume(raeume, tueren)
    drin = wohnraum | (scope - erschlossen - loch)
    zimmertuer: dict[str, set[str]] = {}
    for t in tueren:
        if t.tuer_detail == "zimmertuer":
            zimmertuer.setdefault(t.von_raum, set()).add(t.nach_raum)
            zimmertuer.setdefault(t.nach_raum, set()).add(t.von_raum)
    frei = set(loch)
    einzel: set[str] = set()
    while True:
        gebunden = {rid for rid in frei if zimmertuer.get(rid, set()) & drin}
        if not gebunden:
            gebunden = _gang_einzelraeume(raeume, tueren, drin, scope - drin, loch)
            einzel |= gebunden
        if not gebunden:
            break
        drin |= gebunden
        frei -= gebunden
    erschliessung = {r.id for r in raeume if r.id not in drin and (
        r.raum_typ in SCOPE_TYPEN or nutzungsklasse_fuer(r.raum_typ) == ALLGEMEIN)}
    return ([(g, wohnungseingaenge(g, tueren, erschliessung))
             for g in wohnungsgruppen(drin, tueren)], loch - frei, frei, einzel)


def korrigierte_rollen(raeume: list[Raum], tueren: list[Tuer]) -> dict[str, str | None]:
    """E7 (Owner Board 7): die KORRIGIERTEN Türrollen ``{tuer_id: rolle}`` —
    genau einmal aus der fertigen Klassifikation und den ROHEN Rollen
    abgeleitet, gelesen nur von Fluchtweg und Zirkulation. Sie werden NICHT
    in ``tuer_detail`` geschrieben (Entscheidung (i), Bericht Runde 7): das
    Modell trägt die rohen Rollen, ein zweiter Lauf liest dieselbe Eingabe.

    Eine Zimmertür oder ein Wohnungseingang zwischen zwei Räumen der
    Wohnungsmenge ist eine Zimmertür; zwischen Wohnung und Erschließung ein
    Wohnungseingang; sonst bleibt die rohe Rolle (``wohnungsraeume``).

    **S7c (Owner 2026-09-26):** „Wird ein Vorraum privat, wandert die Rolle
    Wohnungseingang an die ÄUSSERE Tür (Vorraum zu Stiegenhaus oder allgemeinem
    Gang). Die innere Tür wird zimmertuer." Der Wohnungseingang ist damit
    ausschließlich eine Frage der Grenze privat|Erschließung — die ROHE Rolle
    der äußeren Tür entscheidet nicht mit. Vorher stand der Filter
    ``rolle in ("zimmertuer", "wohnungseingang")`` auch vor diesem Zweig: die
    äußere Tür eines privat gewordenen GANGES trägt roh ``stiegenhaustuer``
    (Regel 4: GANG ist im Kanon statisch allgemein) oder gar keine Rolle
    (GANG × GANG) und blieb liegen. Der HERABSTUFENDE Zweig behält den Filter:
    innen ist nur die Rolle zu korrigieren, die dort eine Grenze behauptet.
    Eine ``balkontuer`` wandert nie: das Modul zählt sie weder als
    Wohnungsgrenze (``wohnungsgruppen``) noch als Ausgang.
    """
    privat, erschliessung = wohnungsraeume(raeume, tueren)
    out: dict[str, str | None] = {}
    for t in tueren:
        rolle = t.tuer_detail
        a, b = t.von_raum in privat, t.nach_raum in privat
        if a and b and rolle in ("zimmertuer", "wohnungseingang"):
            rolle = "zimmertuer"
        elif (a != b and rolle != "balkontuer"
              and (t.nach_raum if a else t.von_raum) in erschliessung):
            rolle = "wohnungseingang"
        out[t.id] = rolle
    return out


def riegel(raeume: list[Raum], tueren: list[Tuer],
           ausser: set[str]) -> dict[str, str]:
    """Fail-Safe-Riegel auf den NICHT-Kandidaten: korrigiert die Klasse dort,
    wo die alte Verfeinerung privat sagt und die Ankerregel widerspricht oder
    schweigt. ``ausser`` = Kandidaten (die entscheidet das zweistufige
    Verfahren selbst). Liefert die Gründe.
    """
    urteil = ankerurteil(raeume, tueren)
    gruende: dict[str, str] = {}
    for r in raeume:
        if (r.id in ausser or r.raum_typ not in SCOPE_TYPEN
                or r.nutzungsklasse != PRIVAT):
            continue
        u, grund = urteil[r.id]
        if u == A_ALLGEMEIN:
            r.nutzungsklasse = ALLGEMEIN
            gruende[r.id] = f"Ankerregel: {grund} → allgemein (Fail-Safe)"
        elif u == A_UNKLAR:
            r.nutzungsklasse = None
            gruende[r.id] = f"Ankerregel nicht auswertbar: {grund}"
    return gruende


def warnungen_aus(klassen: dict[str, str | None],
                  gruende: dict[str, str]) -> list[str]:
    """Berichtszeilen für die unbestimmt gebliebenen Räume (§ 6g Schritt 3)."""
    return [f"unbestimmt: {rid} — {gruende.get(rid, 'ohne Grund')}"
            for rid in sorted(klassen) if klassen[rid] is None]


def loch_warnungen(raeume: list[Raum], tueren: list[Tuer],
                   in_wohnung: set[str],
                   einzelraeume: set[str] = frozenset()) -> list[str]:
    """Der Messfall S4c/S3b als Berichtszeilen: JEDER Loch-Raum
    (``loch_raeume``), gleich welche Klasse er bekommen hat, mit seiner
    Wohnungszugehörigkeit nach rohen Türen (``in_wohnung`` = an eine Wohnung
    gebunden, ``einzelraeume`` = die nach R1 gebundenen GÄNGE; beide aus
    ``wohnungszugehoerigkeit``). Dazu je GANG, den R1 OHNE Loch gebunden hat
    (R1-Erweiterung A+C, Owner 2026-09-27), eine ``r1:``-Zeile, die seinen
    Zugang nennt — seine Türen außer den rohen Wohnungseingängen."""
    urteil = ankerurteil(raeume, tueren)
    klasse = {r.id: r.nutzungsklasse for r in raeume}
    kurz = {PRIVAT: "privat", ALLGEMEIN: "allgemein", None: "offen"}
    loch = loch_raeume(raeume, tueren)
    out: list[str] = []
    for rid in sorted(set(einzelraeume) - loch):
        zugang = sorted(t.id for t in tueren if rid in (t.von_raum, t.nach_raum)
                        and t.tuer_detail != "wohnungseingang")
        out.append(f"r1: {rid} — Zugang nur über {', '.join(zugang)} vom Stiegenhaus "
                   "(mit Türblatt, kein Wohnungseingang); hinter seinen rohen "
                   "Wohnungseingängen nur Einzelräume (kein Vorraum oder Gang — ein "
                   "Durchgangsraum erschließt nur), darunter Aufenthaltsraum und "
                   "Bad/WC/Abstellraum → Wohnungsflur, er bildet mit ihnen eine "
                   f"Wohnung (R1); Klasse {kurz.get(klasse[rid], klasse[rid])}: gehört "
                   "zur Wohnung, ist kein Beleg für eine eigene Wohnung (Wohnung "
                   "folgt rohen Türen, Owner 2026-09-27), Notlicht bleibt")
    for rid in sorted(loch):
        if rid in einzelraeume:
            wie = ("hinter seinen rohen Wohnungseingängen liegen nur "
                   "Einzelräume → er bildet mit ihnen eine Wohnung (R1)")
        elif rid in in_wohnung:
            wie = "über eine rohe Zimmertür an seine Wohnung gebunden → gehört zu ihr"
        else:
            wie = ("weder über eine rohe Zimmertür an eine Wohnung gebunden noch "
                   "ein Loch-GANG mit nur Einzelräumen hinter seinen rohen "
                   "Wohnungseingängen (R1) → keine Wohnung, Erschließung")
        out.append(f"loch: {rid} — {urteil[rid][1]} (Messfall S4c/S3b); Klasse "
                   f"{kurz.get(klasse[rid], klasse[rid])}; {wie} (Wohnung folgt "
                   "rohen Türen, Owner 2026-09-22), Notlicht bleibt")
    return out


def unbestimmte_raeume(raeume: list[Raum], tueren: list[Tuer]) -> set[str]:
    """KANDIDATEN ohne entschiedene Klasse. Unbestimmt (``None``) sind nach
    ``bilde_wohnungen`` auch Nicht-Kandidaten — Loch-Räume und Räume, in
    denen die Iteration nicht zur Ruhe kommt; die vollständige Liste mit
    Grund steht in den Warnungen von ``bilde_wohnungen``. Im Produktionspfad
    nicht benutzt."""
    offen = kandidaten(raeume, tueren)
    return {r.id for r in raeume if r.id in offen and r.nutzungsklasse is None}


def volle_knoten(raeume: list[Raum], tueren: list[Tuer]) -> set[str]:
    """GANG/VORRAUM, denen der Fail-Safe-Riegel NICHTS nimmt — sie bleiben
    volle Erschließungsknoten mit eigenen Stützpunkten, egal welche Klasse sie
    tragen. Wer sein Notlicht behält, behält auch seine Zirkulation.

    Das schließt die UNBESTIMMTEN ausdrücklich ein, § 6g Schritt 3 wörtlich:
    „Ein unbestimmter Raum wird konservativ behandelt: er verliert weder
    Leuchte noch Anker und reißt den Graph nicht auf." Ohne sie fiel
    Barawitzka EG ``raum_30`` als Knoten aus dem Graph und verlor seine
    Zirkulation, obwohl keine Regel ihn privat gesprochen hat.
    """
    entzug = bestaetigt_privat(raeume, tueren)
    return {r.id for r in raeume
            if r.raum_typ in SCOPE_TYPEN and r.id not in entzug}


def durchleitung_raeume(raeume: list[Raum], tueren: list[Tuer]) -> set[str]:
    """Kandidaten, denen die Ankerregel privat bestätigt — sie bleiben Knoten
    im Fluchtweg-Graph (Durchleitung, § 6g), bekommen aber keine eigenen
    Stützpunkte, Anker oder Leuchten."""
    return kandidaten(raeume, tueren) & bestaetigt_privat(raeume, tueren)


def setze_wohnungsflags(raeume: list[Raum], tueren: list[Tuer]) -> list[str]:
    """R3 (§ 6f Punkt 3) unter dem Fail-Safe-Riegel: beide Flags ``False`` NUR
    für ankerbestätigt private GANG/VORRAUM — und beide ``True`` für alle
    anderen GANG/VORRAUM.

    **In BEIDE Richtungen** (Befund B1): eine Regel, die Flags nur wegnimmt,
    liefert keinen Fixpunkt ihrer selbst. Verlässt ein Raum die private Menge,
    entsteht sonst der Mischzustand „Klasse allgemein, Flags [0,0]" — gemessen
    an Barawitzka EG ``raum_30``. Jede Typisierungsquelle stempelt GANG und
    VORRAUM mit ``(True, True)`` (``raumtyp._TYP_MAP``), das ist also der
    Rückweg, kein erfundener Wert.
    """
    intern = bestaetigt_privat(raeume, tueren)
    geaendert: list[str] = []
    for r in raeume:
        if r.raum_typ not in SCOPE_TYPEN:
            continue
        soll = r.id not in intern
        if (r.ist_fluchtweg, r.ist_communal) != (soll, soll):
            r.ist_fluchtweg = soll
            r.ist_communal = soll
            geaendert.append(r.id)
    return geaendert


#: Wie tief ein Anker hinter die Türschwelle in den eigenen Raum gesetzt wird —
#: erst knapp, dann tiefer, falls sich die Polygone an der Wand überlappen.
_ZUG_MM = (50.0, 350.0)


def anker_aus_privat_ziehen(anker: list[Anker], raeume: list[Raum],
                            tueren: list[Tuer]) -> list[Anker]:
    """Befund B2: Türanker des Stiegenhauses liegen auf der Schwelle. Wird der
    Nachbarraum privat, liegt der Anker geometrisch IN einer Wohnung — genau
    die Verletzung, deren Beseitigung die Abnahmezahl des Slices ist.

    Der Anker wird auf die Seite SEINES EIGENEN Raums gezogen, nicht
    gestrichen: ein gestrichener Türanker kostet das Rettungszeichen an der
    Stiegenhaustür, und fehlendes Notlicht ist gefährlich, überflüssiges nur
    teurer. Ziel ist der nächste Punkt des eigenen Raums, ``_ZUG_MM`` hinter
    dessen Rand — also die Stiegenhaus-Seite derselben Schwelle. Lässt er sich
    so nicht ziehen, fällt er weg — ein Anker in einer Wohnung bleibt keine
    Option. Gemessen (Runde 4, elf Prüfpläne ohne Muthgasse): „nicht setzen"
    striche 8 Anker (Mollgasse EG 4, Mollgasse 1OG 4), „ziehen" keinen — die
    Anker wandern 50 bis 189 mm.

    Gesperrt ist jeder Raum der Klasse ``WOHNUNG_PRIVAT`` — auch ohne
    Bestätigung der Ankerregel (gemessen Mollgasse EG ``raum_7``, von Schritt 2
    privat: vier Anker von STIEGENHAUS ``raum_51`` darin) und seit Slice S3b
    auch Zimmer, Bäder usw., nicht nur GANG/VORRAUM: erreicht die Restfläche
    des Stiegenhauses eine Blocktür, liegt ihr Türanker auf dem Türpunkt, den
    das gestempelte Zimmer deckt (Rennweg OG3 ``rest_3_tuer_tuer_4`` in ZIMMER
    ``raum_2``, Gate (6) zählt jeden ``WOHNUNG_PRIVAT``-Raum). Gezogen werden
    nur FREMDE Anker; die eigenen eines unbestätigt privaten Raums bleiben, er
    behält sein Notlicht.

    **Planer-Entscheid P2 (Runde 11) — gemessen, NICHT gebaut (Runde 14):**
    hier ``bestaetigt_privat`` zu lesen statt der Klasse ändert auf keinem der
    12 Prüfpläne die Ankerzahl; die einzige Wirkung ist, dass Mollgasse 1OG
    ``raum_64_tuer_tuer_51``/``_54`` auf ihrer rohen Schwellenlage in
    ``raum_69``/``raum_72`` liegen blieben. Der Owner-Grundsatz „nur der
    bestätigte Entzug wirkt" entscheidet das NICHT: hier wird nichts entzogen.
    Die beiden Anker gehören STIEGENHAUS ``raum_64``, nicht den Vorräumen;
    ``raum_69``/``raum_72`` behalten in beiden Lesarten Flags 11, ihre EIGENEN
    Anker, ihre Zirkulation und ihre Leuchten (gemessen Runde 13/14: Anker je
    Raum, Segmente, Zirkulation und Platzierung md5-gleich). Gekostet hätte die
    Umstellung die Abnahmezahl des Slices — Anker geometrisch in
    WOHNUNG_PRIVAT (Zählweise ``tests/gate/gate_og3.py``) auf Mollgasse 1OG
    0 → 2. Sie bleibt darum ungebaut; die heutige Lesart halten vier
    Zusicherungen fest: ``tests/naht/test_s7_wohnungsklasse.py::test_keine_
    anker_wo_das_notlicht_entzogen_wurde`` und die drei Unit-Zusicherungen in
    ``tests/raumerkennung/test_wohnungsklasse.py`` Abschnitt „(j) B2".
    """
    polys = {r.id: Polygon(r.polygon_mm).buffer(0) for r in raeume
             if len(r.polygon_mm) >= 3}
    sperren = [(r.id, polys[r.id]) for r in sorted(raeume, key=lambda x: x.id)
               if r.nutzungsklasse == PRIVAT and r.id in polys]
    if not sperren:
        return anker

    def liegt_fremd_privat(xy, eigen_id) -> bool:
        p = Point(xy)
        return any(rid != eigen_id and poly.contains(p) for rid, poly in sperren)

    out: list[Anker] = []
    for a in anker:
        if not liegt_fremd_privat(a.xy_mm, a.raum_id):
            out.append(a)
            continue
        eigen = polys.get(a.raum_id or "")
        if eigen is None or eigen.is_empty:
            continue
        for tiefe in _ZUG_MM:
            innen = eigen.buffer(-tiefe)
            if innen.is_empty:
                continue
            ziel = nearest_points(innen, Point(a.xy_mm))[0]
            if not liegt_fremd_privat((ziel.x, ziel.y), a.raum_id):
                out.append(a.model_copy(update={"xy_mm": (ziel.x, ziel.y)}))
                break
    return out
