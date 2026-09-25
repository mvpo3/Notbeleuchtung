"""wohnungen — Wohnungsbildung (``Raum.wohnung_id``) und Klassen-Iteration.

Owner-Grundsatz 2026-09-22: zwei getrennte Fragen, nie vermischt. (b) Die
Wohnungen (``wohnung_id``, ``top_1..n`` nach kleinster Raum-ID, Eingänge)
kommen allein aus den ROHEN Türen (``wohnungsklasse.wohnungszugehoerigkeit``);
(a) die Klassen-Iteration entscheidet nur Notlicht und ändert keine Wohnung.

Verfeinerung der Nutzungsklasse: ein GANG/VORRAUM, der nur an private Räume
(ZIMMER/BAD/WC/KUECHE/ABSTELLRAUM …) grenzt und KEINE Tür in STIEGENHAUS oder
AUSSEN hat, ist ein Wohnungs-Flur → WOHNUNG_PRIVAT (Befund-Fallback).

Für GANG/VORRAUM MIT Stiegenhaustür ist seit S7a nicht mehr diese Verfeinerung
zuständig, sondern das zweistufige Verfahren in ``wohnungsklasse`` (Geltungs-
bereich V2, docs/GATE_TUERSTAPEL.md § 6g). Ein dort unbestimmt gebliebener Raum
behält ``nutzungsklasse = None``; ``_klasse`` fällt deshalb NICHT mehr still auf
den statischen Default zurück — genau die willkürliche Festlegung, die § 6g
ausschließt. Innerhalb dieses Moduls ändert das nichts, weil
``bilde_wohnungen`` die statischen Defaults vorher setzt.

**Einbahn (Owner Board 7, 2026-09-21):** rohe Türrolle → Klasse → korrigierte
Rolle → Fluchtweg, nie zurück. ``bilde_wohnungen`` liest nur die ROHEN Rollen
— auch für Wohnungsgrenze und Eingangsliste (``wohnungsklasse.
wohnungseingaenge``) — und schreibt ``tuer_detail`` nicht um; die korrigierten
Rollen leitet ``wohnungsklasse.korrigierte_rollen`` danach aus der fertigen
Klassifikation ab, und nur Fluchtweg und Zirkulation lesen sie.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer

from .nutzungsklasse import nutzungsklasse_fuer
from .tuer_zuordnung import AUSSEN
from .wohnungsklasse import (
    A_PRIVAT,
    ALLGEMEIN,
    DECKEL,
    PRIVAT,
    SCOPE_TYPEN,
    ankerurteil,
    erschliessung_erwiesen,
    kandidaten,
    loch_warnungen,
    riegel,
    riegel_nie_privat,
    schritt1,
    schritt2_urteil,
    setze_wohnungsflags,
    warnungen_aus,
    wohnungszugehoerigkeit,
)


@dataclass
class Wohnung:
    id: str
    raum_ids: list[str] = field(default_factory=list)
    eingangs_tuer_ids: list[str] = field(default_factory=list)


def _klasse(r: Raum) -> str | None:
    return r.nutzungsklasse


def _verfeinere_gang_privat(raeume: list[Raum], tueren: list[Tuer],
                            ausser: set[str] = frozenset(),
                            unbestimmt: set[str] = frozenset(),
                            grenze: set[str] = frozenset()) -> None:
    """Flur-Verfeinerung in BEIDE Richtungen (der statische Default kann falsch
    liegen): ein GANG/VORRAUM nur an Privaträumen, ohne Tür in STIEGENHAUS
    oder AUSSEN, ist ein Wohnungs-Flur → WOHNUNG_PRIVAT; mit einer solchen
    Tür ist er Erschließung → ALLGEMEIN_ERSCHLIESSUNG. ``ausser`` = Räume, die
    ``wohnungsklasse`` entscheidet (Geltungsbereich V2); ``unbestimmt`` = die
    KANDIDATEN ohne Klasse — sie gelten hier ausdrücklich als NICHT privat
    (§ 6g Schritt 3, konservativ), sonst würde ein Nachbar über einen Raum
    privat, über den gerade keine Regel entschieden hat. Ein Nicht-Kandidat
    mit Klasse ``None`` (Loch-Raum) zählt wie ein privater Nachbar.

    **Grenze (E8, Owner Board 6, 2026-09-21):** „Ein Wohnungseingang mit
    Türblatt ist physischer Beleg und begrenzt die Flur-Verfeinerung." Eine
    Tür, die ROH ``wohnungseingang`` MIT Blatt ist und deren andere Seite in
    ``grenze`` liegt (erwiesene Erschließung, ``erschliessung_erwiesen``),
    macht den Raum dahinter nicht allgemein — gemessen Mollgasse 1OG
    ``raum_16``/``19``/``26`` hinter ``tuer_14``/``20``/``21``.

    **Reihenfolgeunabhängig (Befund B6, Runde 5):** alle Räume lesen die
    Nachbarklassen aus DEMSELBEN Schnappschuss vor dem Durchlauf und werden
    erst danach gesetzt (Jacobi). Vorher las die Schleife Klassen, die sie im
    selben Durchlauf schon überschrieben hatte (Gauß-Seidel) — dann entschied
    die Listenreihenfolge, gemessen an Rennweg OG2 ``raum_9``/``raum_10``,
    Mollgasse EG ``raum_29``/``raum_57`` und Muthgasse E2 ``raum_51``/
    ``raum_94``. Zwei Nachbarn, die sich gegenseitig entscheiden, haben zwei
    Fixpunkte; welcher gilt, entscheidet ``bilde_wohnungen`` (Board 4, Beleg
    vor Tiebreak)."""
    by_id = {r.id: r for r in raeume}
    alt = {r.id: r.nutzungsklasse for r in raeume}
    neu: dict[str, str] = {}
    for r in raeume:
        if r.raum_typ not in ("GANG", "VORRAUM") or r.id in ausser:
            continue
        nachbarn: list[str | None] = []
        privat_ok = True
        for t in tueren:
            if r.id not in (t.von_raum, t.nach_raum):
                continue
            andere = t.nach_raum if t.von_raum == r.id else t.von_raum
            nachbarn.append(andere)
            if (t.tuer_detail == "wohnungseingang" and not t.ohne_tuerblatt
                    and andere in grenze):
                continue
            fremd = andere in unbestimmt or (andere in by_id and (
                by_id[andere].raum_typ == "STIEGENHAUS"
                or alt[andere] not in ("WOHNUNG_PRIVAT", None)))
            if andere == AUSSEN or fremd:
                privat_ok = False
        if nachbarn:
            neu[r.id] = ("WOHNUNG_PRIVAT" if privat_ok
                         else "ALLGEMEIN_ERSCHLIESSUNG")
    for rid, klasse in neu.items():
        by_id[rid].nutzungsklasse = klasse


def _gruppen(rids: set[str], knoten: list[str], tueren: list[Tuer]) -> list[set[str]]:
    """``rids`` nach Zusammenhang über Türen zwischen ``knoten`` (die
    beweglichen GANG/VORRAUM), sortiert nach kleinster Raum-ID."""
    nachbarn: dict[str, set[str]] = {k: set() for k in knoten}
    for t in tueren:
        if t.von_raum in nachbarn and t.nach_raum in nachbarn:
            nachbarn[t.von_raum].add(t.nach_raum)
            nachbarn[t.nach_raum].add(t.von_raum)
    out: list[set[str]] = []
    frei = set(rids)
    for start in sorted(rids):
        if start not in frei:
            continue
        teil, stapel = {start}, [start]
        while stapel:
            for n in nachbarn[stapel.pop()] - teil:
                teil.add(n)
                stapel.append(n)
        out.append(teil & frei)
        frei -= teil
    return out


#: Klassen im Grund, ausgeschrieben.
_KURZ = {"WOHNUNG_PRIVAT": "privat", "ALLGEMEIN_ERSCHLIESSUNG": "allgemein",
         None: "offen"}


def bilde_wohnungen(raeume: list[Raum], tueren: list[Tuer],
                    warnungen: list[str] | None = None) -> list[Wohnung]:
    """Setzt ``nutzungsklasse`` + ``wohnung_id`` in-place; liefert die
    Wohnungen (id, raum_ids, eingangs_tuer_ids). ``warnungen`` (optional,
    in-place) nimmt die unbestimmt gebliebenen Räume mit Grund, die
    Loch-Räume und die Tiebreak-Fälle auf.

    **(b) zuerst und für sich (Owner-Grundsatz 2026-09-22, G1):** die
    Wohnungen kommen allein aus ``wohnungszugehoerigkeit`` (rohe Türen);
    nichts, was danach über Klassen entschieden wird, ändert sie.

    **(a) EINE Klassen-Iteration, nur rohe Rollen (E7).** Schritt 1
    (Ankerregel) entscheidet PRIVAT endgültig; die Loch-Räume stehen fest
    (über rohe Zimmertür an ihre Wohnung gebunden oder — R1, Owner
    2026-09-22 — ein Loch-GANG mit nur Einzelräumen hinter seinen rohen
    Wohnungseingängen → unbestimmt mit Notlicht, sonst allgemein), ebenso
    der Riegel (G3: Hauseingang, Tür ins Freie oder Tür
    zu einem Nebenraum → allgemein). Die übrigen Kandidaten (Schritt 2) und
    GANG/VORRAUM (Flur-Verfeinerung + Riegel der Ankerregel) werden
    gemeinsam iteriert, jede Runde aus demselben Schnappschuss (Jacobi), Start
    bei ALLGEMEIN (Board 4: von mehreren Fixpunkten gilt der, der Notlicht
    behält). Pendelt die Iteration, starten die pendelnden Räume neu bei
    ALLGEMEIN; pendeln sie weiter oder erreicht sie in ``DECKEL`` Runden
    keinen Fixpunkt, werden sie unbestimmt — mit Grund, Notlicht bleibt.

    **Beleg vor Tiebreak (G2):** bleiben dabei ankerprivate Räume allgemein,
    läuft die Iteration noch einmal mit ihnen privat gestartet — erst alle
    zusammen, dann je Gruppe benachbarter beweglicher Räume (``_gruppen``).
    Ist das Ergebnis ein Fixpunkt, in dem ALLE abweichenden Räume privat und
    ankerbestätigt sind (Wohnungseingang mit Türblatt, rohe Rollen) und
    keiner offen bleibt, gilt er — gemessen Rennweg OG1 ``raum_4``/``raum_5``.
    Sonst gilt der allgemeine, und jeder solche Raum bekommt eine
    ``tiebreak:``-Zeile mit Grund.
    """
    for r in raeume:
        if r.nutzungsklasse is None and r.raum_typ not in SCOPE_TYPEN:
            r.nutzungsklasse = nutzungsklasse_fuer(r.raum_typ)
    by_id = {r.id: r for r in raeume}
    (zugehoerig, loch_in_wohnung, loch_erschliessung,
     loch_einzelraeume) = wohnungszugehoerigkeit(raeume, tueren)
    kand = kandidaten(raeume, tueren)
    stiegenhaus = {r.id for r in raeume if r.raum_typ == "STIEGENHAUS"}
    grenze = erschliessung_erwiesen(raeume, tueren)
    urteil = ankerurteil(raeume, tueren)
    fest: dict[str, str | None] = dict.fromkeys(loch_in_wohnung)
    fest.update(dict.fromkeys(loch_erschliessung, ALLGEMEIN))
    for rid in riegel_nie_privat(raeume, tueren):
        fest.setdefault(rid, ALLGEMEIN)
    eins = schritt1(raeume, tueren, kand)
    offen = kand - set(eins) - set(fest)
    scope = sorted(r.id for r in raeume if r.raum_typ in SCOPE_TYPEN)
    beweglich = [rid for rid in scope if rid not in eins and rid not in fest]

    def iteriere(privat_start: set[str],
                 basis: dict[str, str | None] | None = None
                 ) -> tuple[dict[str, str], bool]:
        """Die Klassen-Iteration; ``privat_start`` = die Beleg-Probe (G2).
        Liefert die Gründe und ob ein Fixpunkt erreicht wurde.

        ``basis`` (Reviewer Runde 10, Linse Regel, Hinweis 1): der Stand, ab
        dem die Probe startet. Ohne ihn starteten alle übrigen beweglichen
        Räume wieder bei ALLGEMEIN — von dort fiel ein voll belegter Fixpunkt
        zusammen, den es gab (gemessen 13 von 20 000 Zufallstopologien)."""
        gruende = {rid: g for rid, (_, g) in eins.items()}
        gruende.update({rid: (f"Ankerregel nicht auswertbar: {urteil[rid][1]}; "
                              + ("hinter seinen rohen Wohnungseingängen liegen nur "
                                 "Einzelräume, er bildet mit ihnen eine Wohnung (R1)"
                                 if rid in loch_einzelraeume else
                                 "über eine rohe Zimmertür an seine Wohnung gebunden")
                              + " — die Wohnung folgt rohen Türen, die Klasse bleibt "
                              "offen (Owner 2026-09-22)") for rid in loch_in_wohnung})
        for rid in scope:
            by_id[rid].nutzungsklasse = fest.get(
                rid, PRIVAT if rid in eins or rid in privat_start
                else (basis or {}).get(rid, ALLGEMEIN))
        ausser = kand | set(fest)

        def zustand() -> dict[str, str | None]:
            return {rid: by_id[rid].nutzungsklasse for rid in beweglich}

        def runde(nr: int) -> None:
            alt = {r.id: r.nutzungsklasse for r in raeume}
            zwei = {rid: schritt2_urteil(rid, tueren, alt, stiegenhaus, nr)
                    for rid in sorted(offen)}
            _verfeinere_gang_privat(raeume, tueren, ausser=ausser, grenze=grenze,
                                    unbestimmt={rid for rid in kand
                                                if alt[rid] is None})
            gruende.update(riegel(raeume, tueren, ausser))
            for rid, (k, g) in zwei.items():
                by_id[rid].nutzungsklasse = k
                gruende[rid] = g

        def unbestimmt(rids: set[str], verlauf: list, nr: int, wie: str) -> None:
            for rid in rids:
                klassen = " und ".join(sorted({_KURZ.get(z[rid], str(z[rid]))
                                               for z in verlauf}))
                by_id[rid].nutzungsklasse = None
                gruende[rid] = (f"Schritt 3: die Iteration (Schritt 2 und "
                                f"Flur-Verfeinerung) erreicht in {nr} Runden "
                                f"keinen Fixpunkt — {rid} wechselt zwischen "
                                f"{klassen}; {wie} — unbestimmt statt Raten (ob "
                                "die Regel einen Fixpunkt hat, ist nicht geprüft)")

        gesehen = [zustand()]
        neu_gestartet: set[str] = set()
        for nr in range(1, DECKEL + 1):
            runde(nr)
            z = zustand()
            if z == gesehen[-1]:
                return gruende, True
            if z in gesehen:
                zyklus = gesehen[gesehen.index(z):]
                wechselnd = {rid for rid in beweglich
                             if len({s[rid] for s in zyklus}) > 1}
                if wechselnd - neu_gestartet:
                    for rid in wechselnd:
                        by_id[rid].nutzungsklasse = ALLGEMEIN
                    neu_gestartet |= wechselnd
                    gesehen = [zustand()]
                    continue
                unbestimmt(wechselnd, zyklus, nr, "auch neu gestartet bei "
                           "allgemein (Board 4) pendelt sie weiter")
                return gruende, False
            gesehen.append(z)
        if len(gesehen) == 1:           # zuletzt neu gestartet: nachprüfen
            runde(DECKEL + 1)
            gesehen.append(zustand())
        unbestimmt({rid for rid in beweglich
                    if len({s[rid] for s in gesehen}) > 1}, gesehen, DECKEL,
                   f"Deckel {DECKEL} erreicht")
        return gruende, False

    gruende, fixpunkt = iteriere(set())
    stand = {rid: by_id[rid].nutzungsklasse for rid in scope}
    strittig = {rid for rid in beweglich
                if urteil[rid][0] == A_PRIVAT and stand[rid] != PRIVAT}
    warum = dict.fromkeys(strittig, "die Iteration erreicht keinen Fixpunkt, "
                          "kein Probelauf")
    belegt: set[str] = set()
    # Probe erst für alle strittigen zusammen (sie können einander tragen),
    # dann je Gruppe benachbarter beweglicher Räume: ein unbelegter Rest an
    # anderer Stelle nimmt einer voll belegten Gruppe den Beleg nicht
    # (gemessen Runde 10: 1 von 2000 Zufallspaaren ohne diese Trennung).
    gruppen = [strittig] + [g for g in _gruppen(strittig, beweglich, tueren)
                            if g != strittig]
    # ponytail: Probe nur bei Fixpunkt des GANZEN Plans — pendelt ein fremder
    # Teil (Schritt 3), gilt überall der Tiebreak (sicher: Notlicht bleibt;
    # gemessen 3 von 4000 Zufallspaaren). Upgrade: Iteration je Komponente.
    for gruppe in gruppen if fixpunkt and strittig else []:
        if not gruppe - belegt:
            continue
        probe_gruende, probe_fix = iteriere(belegt | gruppe, stand)
        probe = {rid: by_id[rid].nutzungsklasse for rid in scope}
        anders = sorted(rid for rid in scope if probe[rid] != stand[rid])
        unbelegt = [rid for rid in anders
                    if probe[rid] != PRIVAT or urteil[rid][0] != A_PRIVAT]
        if probe_fix and anders and not unbelegt:
            stand, gruende = probe, probe_gruende
            belegt |= set(anders)
            continue
        for rid, k in stand.items():
            by_id[rid].nutzungsklasse = k
        for rid in gruppe - belegt:
            if not probe_fix:
                warum[rid] = "der Probelauf ab privat erreicht keinen Fixpunkt"
            elif rid not in anders:
                warum[rid] = (f"privat gestartet, fällt er auf "
                              f"{_KURZ.get(probe[rid], probe[rid])} zurück")
            else:
                warum[rid] = ("privat hielte er sich nur mit "
                              + ", ".join(f"{x} {_KURZ.get(probe[x], probe[x])}"
                                          for x in unbelegt) + " ohne Ankerbestätigung")
    for rid in sorted(belegt):
        gruende[rid] = (f"Beleg vor Tiebreak (Owner 2026-09-22): {urteil[rid][1]}; "
                        f"der Fixpunkt mit {rid} privat ist voll ankerbestätigt und "
                        "lässt keinen Raum offen")
    # Nur sagen, was belegt ist (Reviewer Runde 10, Linse Naht, Hinweis 4):
    # die Probe zeigt, dass KEIN voll ankerbestätigter Fixpunkt gefunden wurde
    # — ob daneben überhaupt ein zweiter Fixpunkt besteht, prüft sie nicht.
    tiebreak = [
        f"tiebreak: {rid} — Ankerregel privat ({urteil[rid][1]}), Klasse "
        f"allgemein: kein voll ankerbestätigter Fixpunkt ({warum[rid]}); ob "
        "daneben ein zweiter Fixpunkt besteht, ist nicht geprüft — es bleibt "
        "beim allgemeinen (Board 4: von mehreren Fixpunkten gilt der, der "
        "Notlicht behält), Notlicht bleibt"
        for rid in sorted(strittig - belegt) if stand[rid] == ALLGEMEIN]
    if warnungen is not None:
        warnungen.extend(warnungen_aus(
            {rid: by_id[rid].nutzungsklasse for rid in scope}, gruende))
        warnungen.extend(loch_warnungen(raeume, tueren, loch_in_wohnung,
                                        loch_einzelraeume))
        warnungen.extend(tiebreak)

    # `wohnung_id` ZUERST leeren (Befund B1): wer keine Wohnung mehr hat,
    # behielt sonst still die des vorigen Laufs.
    for r in raeume:
        r.wohnung_id = None
    wohnungen: list[Wohnung] = []
    for i, (raum_ids, eingaenge) in enumerate(zugehoerig, start=1):
        w = Wohnung(id=f"top_{i}", raum_ids=raum_ids, eingangs_tuer_ids=eingaenge)
        wohnungen.append(w)
        for rid in raum_ids:
            by_id[rid].wohnung_id = w.id
    # R3 (§ 6f Punkt 3) zuletzt: erst jetzt stehen die Klassen endgültig.
    setze_wohnungsflags(raeume, tueren)
    return wohnungen
