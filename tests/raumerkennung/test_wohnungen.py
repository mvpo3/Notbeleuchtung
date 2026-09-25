"""wohnungen — Zusammenhang über zimmertuer-Kanten + Gang-Verfeinerung."""
from __future__ import annotations

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum, Tuer
from notbeleuchtung.raumerkennung.wohnungen import bilde_wohnungen


def _tuer(tid, von, nach, detail=None):
    return Tuer(id=tid, xy_mm=(0.0, 0.0), von_raum=von, nach_raum=nach,
                tuer_detail=detail)


def test_zwei_wohnungen_getrennt():
    raeume = [Raum(id=r, raum_typ="ZIMMER") for r in ("a1", "a2", "b1")]
    raeume.append(Raum(id="gang", raum_typ="GANG"))
    raeume.append(Raum(id="stgh", raum_typ="STIEGENHAUS"))
    tueren = [
        _tuer("t1", "a1", "a2", "zimmertuer"),
        _tuer("t2", "gang", "a1", "wohnungseingang"),
        _tuer("t3", "gang", "b1", "wohnungseingang"),
        _tuer("t4", "gang", "stgh", "stiegenhaustuer"),
    ]
    wohnungen = bilde_wohnungen(raeume, tueren)
    assert [w.id for w in wohnungen] == ["top_1", "top_2"]
    by_id = {r.id: r for r in raeume}
    assert by_id["a1"].wohnung_id == by_id["a2"].wohnung_id
    assert by_id["b1"].wohnung_id != by_id["a1"].wohnung_id
    assert by_id["gang"].wohnung_id is None
    top1 = next(w for w in wohnungen if "a1" in w.raum_ids)
    assert top1.eingangs_tuer_ids == ["t2"]


def test_wohnungs_flur_ohne_stiegenhaus_behaelt_notlicht_und_gilt_als_allgemein():
    """VORRAUM nur an Zimmer/Bad, keine Tür in STIEGENHAUS/AUSSEN.

    Bis Runde 3 machte ``_verfeinere_gang_privat`` ihn privat. Seit dem
    Fail-Safe-Riegel (Owner 2026-09-21) gilt: Notlicht wird nur entzogen, wo
    die ANKERREGEL privat bestätigt — und hier gibt es gar kein Stiegenhaus,
    von dem aus sie prüfen könnte: laut Owner ein Tür- oder
    Raumerkennungsloch, kein Klassifikationsproblem (Messfall S4c/S3b). Bis
    Runde 7 blieb er darum offen IN der Wohnung {vor, zi, bad} — einer
    Wohnung ohne Eingang. Seit dem Owner-Grundsatz 2026-09-22 („Wohnung folgt
    rohen Türen", G1.2) ist er nur über rohe Wohnungseingänge angebunden →
    Erschließung, ALLGEMEIN; der Messfall bleibt als Warnung."""
    raeume = [
        Raum(id="vor", raum_typ="VORRAUM"),
        Raum(id="zi", raum_typ="ZIMMER"),
        Raum(id="bad", raum_typ="BAD"),
    ]
    tueren = [_tuer("t1", "vor", "zi", "wohnungseingang"),
              _tuer("t2", "vor", "bad", "wohnungseingang")]
    warnungen: list[str] = []
    bilde_wohnungen(raeume, tueren, warnungen)
    assert raeume[0].nutzungsklasse == "ALLGEMEIN_ERSCHLIESSUNG"
    assert (raeume[0].ist_fluchtweg, raeume[0].ist_communal) == (True, True)
    assert [w for w in warnungen if w.startswith("loch: vor — ")
            and "Messfall S4c/S3b" in w], warnungen


def test_loch_raum_ohne_eingang_loest_die_wohnung_in_raeume_mit_eingang_auf():
    """Derselbe Flur, die Wohnungsseite. Bis Runde 7 hieß die Regel
    „unbestimmt heißt NICHT ausgezogen": der Flur blieb offen in seiner
    Wohnung, alle Türen waren Zimmertüren — und die Wohnung hatte KEINEN
    Eingang, also keinen Fluchtweg-Start (Reviewer Runde 7, Linse Regel,
    blockierend 1). Seit dem Owner-Grundsatz 2026-09-22 (G1.2) ist der Flur,
    nur über rohe Wohnungseingänge angebunden, Erschließung, und jeder Raum
    dahinter hat seinen Wohnungseingang (Rennweg OG3 ``raum_10``: Einraum 0 → 4,
    Ursache im Bericht Runde 10).

    Seit E7 (Owner Board 7) trägt das Modell die ROHEN Rollen; die
    korrigierten leitet ``korrigierte_rollen`` danach ab."""
    from notbeleuchtung.raumerkennung.wohnungsklasse import korrigierte_rollen

    raeume = [
        Raum(id="vor", raum_typ="VORRAUM"),
        Raum(id="zi", raum_typ="ZIMMER"),
        Raum(id="bad", raum_typ="BAD"),
    ]
    tueren = [_tuer("t1", "vor", "zi", "wohnungseingang"),
              _tuer("t2", "vor", "bad", "wohnungseingang")]
    wohnungen = bilde_wohnungen(raeume, tueren)
    assert sorted((w.raum_ids, w.eingangs_tuer_ids) for w in wohnungen) == [
        (["bad"], ["t2"]), (["zi"], ["t1"])]
    assert raeume[0].wohnung_id is None
    assert all(t.tuer_detail == "wohnungseingang" for t in tueren)   # roh
    assert set(korrigierte_rollen(raeume, tueren).values()) == {"wohnungseingang"}


def test_flur_mit_stiegenhaustuer_und_einer_wohnung_wird_privat():
    """Schritt 1 gibt ihn offen an Schritt 2 (F11 ist ein UND), und Schritt 2
    findet nur EINE Wohnung, keinen Ausgang und keinen allgemeinen Nebenraum →
    privat. Bis Runde 3 entschied die bloße Erreichbarkeit ALLGEMEIN. Das
    Notlicht behält er trotzdem: die Ankerregel bestätigt privat nicht."""
    raeume = [Raum(id="vor", raum_typ="VORRAUM"),
              Raum(id="zi", raum_typ="ZIMMER"),
              Raum(id="stgh", raum_typ="STIEGENHAUS")]
    tueren = [_tuer("t1", "vor", "zi", "wohnungseingang"),
              _tuer("t2", "vor", "stgh", "stiegenhaustuer")]
    bilde_wohnungen(raeume, tueren)
    assert raeume[0].nutzungsklasse == "WOHNUNG_PRIVAT"
    assert (raeume[0].ist_fluchtweg, raeume[0].ist_communal) == (True, True)


def test_flur_mit_stiegenhaustuer_und_zwei_wohnungen_bleibt_erschliessung():
    """Die zweite Hälfte von F11 erfüllt → ALLGEMEIN."""
    raeume = [Raum(id="vor", raum_typ="VORRAUM"),
              Raum(id="zi1", raum_typ="ZIMMER"),
              Raum(id="zi2", raum_typ="ZIMMER"),
              Raum(id="stgh", raum_typ="STIEGENHAUS")]
    tueren = [_tuer("t1", "vor", "zi1", "wohnungseingang"),
              _tuer("t2", "vor", "zi2", "wohnungseingang"),
              _tuer("t3", "vor", "stgh", "stiegenhaustuer")]
    bilde_wohnungen(raeume, tueren)
    assert raeume[0].nutzungsklasse == "ALLGEMEIN_ERSCHLIESSUNG"
