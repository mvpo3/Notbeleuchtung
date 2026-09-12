"""Fehlende Fenstererkennung ist kein ``False`` — Enis' Regel, festgeschrieben.

Owner-Auftrag 2026-09-12, Punkt 2e: *fehlende Fenstererkennung allein begründet
kein ``False`` bei ``natuerlich_belichtet``, bei unvollständiger Grundlage
bleibt es ``None``.*

**Messstand `91ad7cc`: das Feld existiert nicht.** Zur Laufzeit geprüft —
``Raum`` führt ``bereinigung``, ``besondere_gefaehrdung``, ``flaeche_m2``,
``id``, ``ist_barrierefrei``, ``ist_communal``, ``ist_fluchtweg``,
``nutzungsklasse``, ``polygon_mm``, ``polygon_roh``, ``raum_typ``,
``wohnung_id``; ``natuerlich_belichtet``, ``belichtung_quelle`` und
``belichtung_vollstaendigkeit`` sind **Vorschlag** (`docs/ENIS_UEBERGABE_0908.md`
§ 4.4), und ``fenster_signatur`` sagt das im Modul-Docstring selbst.

Deshalb ist dieser Test **kein grüner Guard auf einem bestehenden Verhalten** —
das wäre die Absicherung von etwas, das es nicht gibt. Er hat drei Aufgaben:

1. den Ist-Stand als selbstprüfenden Beleg festhalten (kein Belichtungsfeld),
2. die Regel dort festschreiben, wo sie heute messbar ist: eine leere Antwort
   von ``fenster_signatur`` trägt **keine** Aussage über Belichtung,
3. das Zielbild als strict-xfail stehen lassen, damit die Regel beim ersten
   Erzeuger des Feldes nicht vergessen wird. Dieselbe Bauform wie Enis' Auflage
   A zu ``lichte_quelle``.

Fachliche Deckung im Normteil: ``normwissen/data/astv_arbeitsstaetten.yaml``
führt ``z1_nicht_natuerlich_belichtet`` mit ``heute_im_modell: false`` und
``status: ungeprueft`` und grenzt ausdrücklich ab, dass fehlende Belichtung
allein einen Raum nicht zum Arbeitsraum macht (AStV § 1 Abs. 4).
"""
import pytest

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum
from notbeleuchtung.raumerkennung.fenster_signatur import finde_rahmenfenster

_BELICHTUNGSFELDER = ("natuerlich_belichtet", "belichtung_quelle",
                      "belichtung_vollstaendigkeit")


def test_contract_fuehrt_kein_belichtungsfeld():
    """Wächter, nicht Wunsch: wird rot, sobald das Feld eingeführt wird.

    Rot heißt dann nicht „Fehler", sondern: jetzt ist der Erzeuger da, also muss
    die Regel aus ``test_soll_natuerlich_belichtet_...`` mit umgesetzt und
    dieser Test durch sie ersetzt werden. Ohne den Wächter könnte das Feld
    stillschweigend mit ``False``-Default erscheinen — genau der Fall, den Enis
    ausschließt.
    """
    vorhanden = [f for f in _BELICHTUNGSFELDER if f in Raum.model_fields]
    assert vorhanden == [], (
        f"Belichtungsfeld(er) {vorhanden} sind neu am Contract. Enis' Regel "
        "(2026-09-12) gilt ab jetzt: fehlende Fenstererkennung begründet kein "
        "False, bei unvollständiger Grundlage bleibt der Wert None."
    )


def test_leere_antwort_traegt_keine_belichtungsaussage():
    """Ohne Eingabe gibt es kein Ergebnis — und das ist keine Verneinung.

    ``finde_rahmenfenster`` liefert für eine leere Segmentliste dasselbe wie
    für eine Segmentliste ohne Fenstersignatur: eine leere Liste. Die beiden
    Sachlagen sind fachlich verschieden („nicht gesucht" gegen „nichts
    gefunden"), und die Funktion kann sie nicht unterscheiden — die
    Unterscheidung hängt an ``wandsegmente(plan)``, das auf Plänen mit Wänden
    in Blockdefinitionen (Rennweg) leer ist. Wer aus dieser leeren Liste ein
    ``natuerlich_belichtet = False`` macht, erfindet eine Messung.
    """
    assert finde_rahmenfenster([]) == []

    # Zwei Segmente, die keine Rahmensignatur bilden (Abstand 5000 mm statt
    # 80-100 mm): ebenfalls leer — also nicht von „nicht gesucht" zu trennen.
    weit = [((0.0, 0.0), (2000.0, 0.0), "A-WALL"),
            ((0.0, 5000.0), (2000.0, 5000.0), "A-WALL")]
    assert finde_rahmenfenster(weit) == []


@pytest.mark.xfail(strict=True, reason=(
    "ZIELBILD, kein Fehler. Gemessen auf 91ad7cc: Raum führt kein Feld "
    "natuerlich_belichtet (Raum.model_fields = bereinigung, "
    "besondere_gefaehrdung, flaeche_m2, id, ist_barrierefrei, ist_communal, "
    "ist_fluchtweg, nutzungsklasse, polygon_mm, polygon_roh, raum_typ, "
    "wohnung_id), und es gibt keinen Belichtungs-Code am Raum. Die drei "
    "Felder sind Vorschlag (ENIS_UEBERGABE § 4.4). Sobald der erste Erzeuger "
    "das Feld anlegt, wird dieser Test XPASS und damit — strict — rot: dann "
    "ist zu prüfen, dass bei unvollständiger Grundlage None herauskommt und "
    "nicht False."))
def test_soll_natuerlich_belichtet_bleibt_none_ohne_grundlage():
    """Enis' Regel als Zielbild am Contract-Feld selbst."""
    assert "natuerlich_belichtet" in Raum.model_fields
    raum = Raum(id="r1", raum_typ="ZIMMER")
    assert raum.natuerlich_belichtet is None, (
        "ohne Fenstererkennung muss der Wert None sein, nicht False"
    )
