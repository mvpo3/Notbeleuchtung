"""OVE-Fachinfo E07 (Funktionserhalt) und OIB-RL 4 Kapitel 2 (Fluchtwegbreiten).

Beide Blöcke sind **Quellenarbeit ohne Umsetzung** — der Engine fehlen die
tragenden Modelle (Leitungen/Stromkreise bzw. gemessene Breiten). Diese Tests
sichern deshalb nicht Verhalten, sondern die **Grenzen der Aussage**:

* Ebenen und Ausgabestände bleiben getrennt und benannt.
* Historische Werte werden nicht als aktuelle allgemeine Anforderung geführt.
* Aus Illustrationen wird keine Platzierungsregel.
* Die erforderliche Mindestbreite wandert nirgends in die Lichtberechnung.
* Keine der beiden Dateien erzeugt einen Contract-Wert oder einen Konsumenten.
"""
from __future__ import annotations

import ast
from collections.abc import Iterator
from pathlib import Path

import yaml

from notbeleuchtung.normwissen import En1838NormProvider

DATA = Path(__file__).parents[2] / "src" / "notbeleuchtung" / "normwissen" / "data"
SRC = Path(__file__).parents[2] / "src" / "notbeleuchtung"


def _lade(name: str) -> dict:
    with open(DATA / name, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


#: Dateien, die Quellenarbeit ohne Verbraucher sind — niemand im Produktivcode
#: darf sie laden, solange die zugehörige Semantik nicht geklärt ist.
_BEWACHTE_DATEIEN = ("ove_e07_funktionserhalt", "oib_rl4_fluchtwegbreiten")

#: Aufzählende Zugriffe: damit ließe sich eine Datei ohne Namensnennung laden.
#: Pfad-Methoden (``p.glob(…)``) und Modulfunktionen (``os.listdir(p)``,
#: ``from os import listdir``) werden gleich behandelt.
_ENUM_METHODEN = ("glob", "rglob", "iterdir")
_ENUM_FUNKTIONEN = ("listdir", "scandir", "walk", "glob", "iglob")
#: Module, aus denen eine aufzählende Funktion importiert worden sein kann.
_ENUM_MODULE = ("os", "os.path", "glob")


def _docstring_knoten(baum: ast.Module) -> set[int]:
    """`id()` aller Konstanten, die Docstring sind — die zählen nicht als Zugriff."""
    ids: set[int] = set()
    for knoten in ast.walk(baum):
        if not isinstance(knoten, ast.Module | ast.ClassDef
                          | ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        erste = knoten.body[0] if knoten.body else None
        if (isinstance(erste, ast.Expr) and isinstance(erste.value, ast.Constant)
                and isinstance(erste.value.value, str)):
            ids.add(id(erste.value))
    return ids


def _code_strings(baum: ast.Module) -> Iterator[tuple[int, str]]:
    """Alle String-Literale **außerhalb** von Docstrings (Kommentare hat der AST nie)."""
    docs = _docstring_knoten(baum)
    for knoten in ast.walk(baum):
        if (isinstance(knoten, ast.Constant) and isinstance(knoten.value, str)
                and id(knoten) not in docs):
            yield knoten.lineno, knoten.value


def _zeigt_auf_daten(knoten: ast.AST, namen: set[str]) -> bool:
    """Zeigt dieser Ausdruck auf ein Datenverzeichnis?

    Erkannt wird ein Pfadbestandteil ``"data"`` (``Path(__file__).parent /
    "data"``), ein bereits als Datenpfad bekannter Name und ein Attribut wie
    ``provider.DATA_DIR``. Namen mit ``data`` im Bezeichner zählen mit — genau
    so heißt der Einstiegspunkt im Produktivcode (``DATA_DIR``).
    """
    for teil in ast.walk(knoten):
        if (isinstance(teil, ast.Constant) and isinstance(teil.value, str)
                and "data" in teil.value.lower()):
            return True
        if isinstance(teil, ast.Name) and (teil.id in namen or "data" in teil.id.lower()):
            return True
        if isinstance(teil, ast.Attribute) and "data" in teil.attr.lower():
            return True
    return False


def _daten_namen(baum: ast.Module) -> set[str]:
    """Namen, die (auch über mehrere Zuweisungen) auf ein Datenverzeichnis zeigen.

    Deckt die Umbenennung ab, an der ein reiner Textvergleich vorbeiläuft:
    ``ROOT = DATA_DIR`` bzw. ``ROOT = Path(__file__).parent / "data"`` — danach
    ist ``ROOT.glob("*.yaml")`` ein Verzeichniszugriff auf die Normdaten.
    """
    namen: set[str] = set()
    geaendert = True
    while geaendert:                      # Fixpunkt: Ketten von Zuweisungen
        geaendert = False
        for knoten in ast.walk(baum):
            if isinstance(knoten, ast.Assign):
                ziele, wert = knoten.targets, knoten.value
            elif isinstance(knoten, ast.AnnAssign) and knoten.value is not None:
                ziele, wert = [knoten.target], knoten.value
            else:
                continue
            if not _zeigt_auf_daten(wert, namen):
                continue
            for ziel in ziele:
                if isinstance(ziel, ast.Name) and ziel.id not in namen:
                    namen.add(ziel.id)
                    geaendert = True
    return namen


def _enum_namen(baum: ast.Module) -> set[str]:
    """Lokale Namen aufzählender Funktionen, inklusive Import-Aliassen.

    ``from os import listdir`` → ``listdir``; ``from os import listdir as ls``
    → ``ls``. Ohne diese Zuordnung bliebe der direkt importierte Aufruf
    unsichtbar, weil er kein Attribut-Zugriff ist.
    """
    namen: set[str] = set()
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.ImportFrom) and (knoten.module or "") in _ENUM_MODULE:
            for alias in knoten.names:
                if alias.name in _ENUM_FUNKTIONEN:
                    namen.add(alias.asname or alias.name)
    return namen


def _aufzaehlungen(quelle: str, baum: ast.Module) -> list[tuple[int, str]]:
    """Aufzählende Zugriffe auf ein Datenverzeichnis — Zeile und Quelltext.

    Drei Formen, alle mit Namensauflösung im Modul:

    * ``DATA_DIR.glob("*.yaml")`` und ``ROOT.iterdir()`` (Pfad-Methode),
    * ``os.listdir(DATA_DIR)`` (Modul-Attribut),
    * ``listdir(DATA_DIR)`` nach ``from os import listdir`` (Import-Alias).

    ⚠️ **Grenzen, ausdrücklich:** nicht auflösbar sind Zugriffe über
    Funktionsgrenzen hinweg (das Verzeichnis wird übergeben und anderswo
    aufgezählt), Pfade, die ohne erkennbaren ``data``-Bestandteil aus Variablen
    zusammengesetzt werden, sowie zur Laufzeit gebildete Namen
    (``getattr``, ``importlib.resources``, f-Strings). Der Wächter ist damit
    eine **Schranke gegen das Naheliegende**, kein Beweis der Abwesenheit.
    """
    daten = _daten_namen(baum)
    enum_lokal = _enum_namen(baum)
    treffer: list[tuple[int, str]] = []
    for knoten in ast.walk(baum):
        if not isinstance(knoten, ast.Call):
            continue
        funktion = knoten.func
        if isinstance(funktion, ast.Attribute) and (
                funktion.attr in _ENUM_METHODEN or funktion.attr in _ENUM_FUNKTIONEN):
            kandidaten = [funktion.value, *knoten.args]      # Empfänger und Argumente
        elif isinstance(funktion, ast.Name) and (
                funktion.id in enum_lokal or funktion.id in _ENUM_FUNKTIONEN):
            kandidaten = list(knoten.args)
        else:
            continue
        if any(_zeigt_auf_daten(k, daten) for k in kandidaten):
            treffer.append((knoten.lineno,
                            ast.get_source_segment(quelle, knoten) or "<Aufruf>"))
    return treffer


E07 = _lade("ove_e07_funktionserhalt.yaml")
RL4 = _lade("oib_rl4_fluchtwegbreiten.yaml")


# ── E07: Ebenen, Ausgaben, Grenzen ───────────────────────────────────────────
def test_e07_ist_fachinformation_und_nennt_seine_bezugsnorm() -> None:
    """E07 ist Ebene D und laut eigenem Schlusssatz nur mit E 8002-1 anwendbar."""
    q = E07["quellen"]["e07"]
    assert q["ebene"] == "D"
    assert "E 8002-1:2002" in q["bezugsnorm"]
    assert "NICHT im Repo" in q["bezugsnorm"]
    assert "nur gemeinsam" in q["anwendungsvorbehalt"].lower()


def test_e07_traegt_seinen_historischen_stand() -> None:
    """Ausgabe 2021, Inhalt von 2006 — beides muss sichtbar bleiben."""
    ausgabe = E07["quellen"]["e07"]["ausgabe"]
    assert "2021-01-01" in ausgabe
    assert "April 2006" in ausgabe
    assert "2020-12" in ausgabe          # Aktualitätsprüfung


def test_30_minuten_werden_nicht_als_aktuelle_anforderung_gefuehrt() -> None:
    """Die 30 min stammen aus E 8002-1:2002; OVE E 8101 nennt keine Minutenzahl."""
    regel = next(r for r in E07["regeln"] if r["kennung"] == "e07_grundsatz_30min")
    assert "2002" in regel["ausgabenvorbehalt"]
    assert "angemessene Dauer" in regel["ausgabenvorbehalt"]
    assert "Nicht als aktuelle allgemeine Anforderung" in regel["ausgabenvorbehalt"]


def test_struktur_der_regel_ist_an_der_geltenden_norm_gegengeprueft() -> None:
    """Queren/Innerhalb ist in OVE E 8101 belegt — die Dauer ausdrücklich nicht."""
    regel = next(r for r in E07["regeln"] if r["kennung"] == "e07_queren_von_brandabschnitten")
    gegen = regel["gegenprobe_e8101"]
    assert gegen["ergebnis"] == "bestaetigt"
    assert "560.9.2" in gegen["fundstelle_2025"]
    assert "keine Anforderungen an den Funktionserhalt" in gegen["wortlaut_2025"]
    assert "Die DAUER ist es nicht" in gegen["⚠_unterschied"]


def test_aus_den_bildern_folgt_keine_platzierungsregel() -> None:
    """Bilder 2–6 zeigen Leuchten in Nebenräumen — das ist Illustration."""
    hinweis = E07["bilder"]["⚠_keine_platzierungsableitung"]
    assert "KEINE Platzierungsvorgabe" in hinweis
    assert "kein Norm-Trigger" in hinweis


def test_bildluecken_des_digests_sind_geschlossen() -> None:
    """Der Digest nannte Bilder 1–6 und den Text zu 2.2 als Lücke."""
    bilder = E07["bilder"]
    assert {f"bild_{i}" for i in range(1, 7)} <= set(bilder)
    legende = bilder["symbollegende"]["eintraege"]
    assert any("maximal 1.600 m²" in e for e in legende)     # Grenze steht in der Legende
    assert any("CPS" in e for e in legende) and any("HVS" in e for e in legende)
    assert "Unterbrandabschnitten" in bilder["bild_2"]["titel"]


def test_1600_m2_bleibt_eine_offene_luecke() -> None:
    """„Weiter gehende Überlegungen" — die Quelle sagt nicht, welche."""
    offen = next(o for o in E07["offen_in_der_quelle"] if "1.600" in o["punkt"])
    assert "sagt NICHT" in offen["befund"]
    assert "keine Erlaubnis und kein Verbot" in offen["befund"]


def test_e07_regeln_haben_keinen_verbraucher_und_nennen_das() -> None:
    """Ehrliche Grenze: jede Regel steht auf `nicht_pruefbar`, ohne Konsument."""
    for r in E07["regeln"]:
        assert r["verbraucher"] is None, r["kennung"]
        assert r["status"] == "nicht_pruefbar", r["kennung"]
        assert r["benoetigte_angaben"], r["kennung"]


def test_fehlende_modelle_sind_als_uebergabe_benannt() -> None:
    """Leitungen, Stromkreise, Verteiler — mit Adressat."""
    modelle = E07["fehlende_modelle"]
    assert len(modelle) == 3
    assert any("Stromkreis" in m["modell"] for m in modelle)
    assert all(m["braucht"] for m in modelle)


def test_endstromkreisgrenze_ist_normativ_belegt() -> None:
    """Die Grenze je Endstromkreis steht in OVE E 8101 selbst (Ebene C).

    ⚠️ Nur diese eine Aussage — die E08-Prüfeinrichtung ist ein anderer
    Sachverhalt, siehe `test_zwanzig_leuchten_zwei_verschiedene_aussagen`.
    """
    eintrag = E07["e8101_gegenprobe"][0]
    assert eintrag["ebene"] == "C"
    assert eintrag["werte"]["max_leuchten_je_endstromkreis"] == 20
    assert eintrag["werte"]["max_belastung_prozent"] == 60
    assert eintrag["status"] == "nicht_abgebildet"


# ── RL 4: Soll-Breite bleibt Soll-Breite ─────────────────────────────────────
def test_rl4_trennt_erforderliche_von_gemessener_breite() -> None:
    """Die zentrale Abgrenzung — sie steht ausdrücklich in der Datei."""
    a = RL4["abgrenzung_en1838"]
    assert "TATSAECHLICHE Breite" in " ".join(a["was_en1838_braucht"])
    assert "ERFORDERLICHE Mindestbreite" in " ".join(a["was_rl4_liefert"])
    assert "NICHT als `breite_mm`" in a["verbot"]
    assert "weder als Default noch als Fallback" in a["verbot"]


def test_rl4_werte_sind_vollstaendig_und_quellengebunden() -> None:
    """Jede Zahl trägt ihre Fundstelle."""
    m = RL4["mindestbreiten"]
    assert m["gaenge"]["hauptgang_m"] == 1.20
    assert m["treppen"]["haupttreppe_ausgenommen_wohnungstreppe_m"] == 1.20
    assert m["treppen"]["wohnungstreppe_m"] == 0.90
    assert m["treppen"]["nebentreppe_m"] == 0.60
    assert m["durchgangshoehe"]["mindesthoehe_m"] == 2.10
    assert m["personenabhaengige_erhoehung"]["schwelle_personen"] == 120
    for block in ("gaenge", "treppen", "rampen", "personenabhaengige_erhoehung", "durchgangshoehe"):
        assert "RL 4, Punkt 2." in m[block]["fundstelle"], block


def test_tuerbaender_sind_vollstaendig() -> None:
    """80/90/100 cm nach Personenzahl — mit der 20-cm-Regel für Doppeltüren."""
    t = RL4["tueren"]["im_verlauf_von_fluchtwegen"]
    assert [(b["bis_personen"], b["nutzbare_breite_m"]) for b in t["baender"]] == [
        (40, 0.80), (80, 0.90), (120, 1.00)
    ]
    assert "20 cm" in t["zwei_tueren_regel"]


def test_einengungen_begruenden_warum_soll_nicht_ist_ist() -> None:
    """RL 4 lässt Einengungen zu — deshalb ist die Mindestbreite kein Messwert."""
    e = RL4["einengungen"]
    assert len(e["zulaessige_ausnahmen"]) >= 6
    assert "UNTER der Mindestbreite liegen darf" in e["folge_fuer_die_engine"]


def test_rl4_benennt_die_fehlenden_eingaben_mit_adressat() -> None:
    """Fünf Angaben, jede mit Herkunft."""
    angaben = RL4["benoetigte_angaben"]
    assert len(angaben) == 5
    assert any("lichte Breite" in a["angabe"] for a in angaben)
    assert all(a["heute"] and a["braucht"] for a in angaben)
    assert RL4["status"] == "nicht_pruefbar"


# ── Beide Blöcke: keine Aktivierung ──────────────────────────────────────────
def test_kein_contract_wert_und_kein_konsument() -> None:
    """Weder E07 noch RL 4 verändern das Regelwerk oder werden irgendwo geladen.

    Geprüft wird der **Zugriff**, nicht der Dateiinhalt: der Wächter liest jedes
    Modul unter `src/` als AST und sieht nur String-Literale, die im **Code**
    stehen — Ladepfad (`_lade("…yaml")`, Importname) und Dateizugriff
    (`open(DATA_DIR / "…")`) gleichermaßen. **Docstrings und Kommentare sind
    ausgenommen**: eine wörtliche Quellenangabe in Prosa ist ein Beleg, kein
    Verbraucher (zuvor schlug der Substring-Wächter genau daran an —
    `raumerkennung/breitenprofil.py`, Modul-Docstring).

    Die zweite Hälfte schließt die Lücke, die ein reiner Namensvergleich lässt:
    wird irgendwo im Produktivcode ein **Datenverzeichnis aufgezählt**
    (`DATA_DIR.glob(…)`, `os.listdir(DATA_DIR)`, `listdir(DATA_DIR)` nach
    `from os import listdir`), ließe sich eine Datei ohne Namensnennung laden —
    dann trägt dieser Wächter nicht mehr und sagt das, statt still grün zu
    bleiben. Umbenennungen (`ROOT = DATA_DIR`) werden dabei aufgelöst.

    ⚠️ Die Grenzen dieser Auflösung stehen bei `_aufzaehlungen`: über
    Funktionsgrenzen hinweg, ohne erkennbaren `data`-Bestandteil oder zur
    Laufzeit gebildet bleibt ein Zugriff unsichtbar.
    """
    snap = En1838NormProvider().regelwerk_snapshot()
    assert snap.arbeitsplatz_lux.min_lux_absolut is None
    assert snap.flaechen_schwellen.antipanik_min_m2 is None

    zugriffe: list[str] = []
    aufzaehlungen: list[str] = []
    for pfad in sorted(SRC.rglob("*.py")):
        quelle = pfad.read_text(encoding="utf-8")
        baum = ast.parse(quelle, filename=str(pfad))
        rel = pfad.relative_to(SRC).as_posix()
        for zeile, wert in _code_strings(baum):
            if any(name in wert for name in _BEWACHTE_DATEIEN):
                zugriffe.append(f"{rel}:{zeile} -> {wert!r}")
        aufzaehlungen += [f"{rel}:{zeile} -> {text}"
                          for zeile, text in _aufzaehlungen(quelle, baum)]

    assert zugriffe == [], zugriffe
    assert aufzaehlungen == [], (
        "Ein Datenverzeichnis wird aufgezählt — der Namensvergleich oben kann "
        f"einen Verbraucher dann nicht mehr ausschließen: {aufzaehlungen}"
    )


def test_waechter_erkennt_umbenanntes_verzeichnis_und_direkten_import() -> None:
    """Zwei Zugriffsformen, die der frühere Textvergleich übersehen hat.

    Geprüft wird der **tatsächlich verwendete** Prüfer `_aufzaehlungen`, nicht
    eine Nachbildung: `ROOT.glob("*.yaml")` mit `ROOT` auf dem Normdaten-
    verzeichnis (der Quelltext nennt an der Aufrufstelle kein „data"), und
    `listdir(DATA_DIR)` nach `from os import listdir` (kein Attribut-Zugriff).
    """
    umbenannt = (
        'from pathlib import Path\n'
        'ROOT = Path(__file__).parent / "data"\n'
        'def laden():\n'
        '    return [p for p in ROOT.glob("*.yaml")]\n'
    )
    direkt_importiert = (
        'from os import listdir\n'
        'from pathlib import Path\n'
        'DATA_DIR = Path(__file__).parent / "data"\n'
        'def laden():\n'
        '    return listdir(DATA_DIR)\n'
    )
    for quelle in (umbenannt, direkt_importiert):
        treffer = _aufzaehlungen(quelle, ast.parse(quelle))
        assert treffer, quelle

    # Kette über zwei Zuweisungen — dieselbe Lücke, eine Stufe tiefer.
    kette = (
        'from pathlib import Path\n'
        'DATA_DIR = Path(__file__).parent / "data"\n'
        'ROOT = DATA_DIR\n'
        'ORDNER = ROOT\n'
        'def laden():\n'
        '    return list(ORDNER.iterdir())\n'
    )
    assert _aufzaehlungen(kette, ast.parse(kette))

    # Aufzählung, die nichts mit den Normdaten zu tun hat, bleibt erlaubt.
    fremd = (
        'from pathlib import Path\n'
        'def plaene():\n'
        '    return list(Path("Projekte").glob("*.dxf"))\n'
    )
    assert _aufzaehlungen(fremd, ast.parse(fremd)) == []

    # Prosa bleibt Prosa — auch für diesen Prüfer.
    prosa = (
        '"""Lädt nichts; beschreibt nur DATA_DIR.glob(\'*.yaml\')."""\n'
        '# auch als Kommentar: os.listdir(DATA_DIR)\n'
        'WERT = 1\n'
    )
    assert _aufzaehlungen(prosa, ast.parse(prosa)) == []


def test_waechter_sieht_code_aber_keine_prosa(tmp_path: Path) -> None:
    """Der Wächter unterscheidet Ladepfad von Quellenangabe — beides gezielt geprüft."""
    prosa = ast.parse(
        '"""Quelle: oib_rl4_fluchtwegbreiten.yaml, Punkt 2.7.1."""\n'
        "# auch als Kommentar: oib_rl4_fluchtwegbreiten.yaml\n"
        "WERT = 1\n"
    )
    assert not [w for _, w in _code_strings(prosa)
                if any(n in w for n in _BEWACHTE_DATEIEN)]

    for quelltext in (
        '_lade("oib_rl4_fluchtwegbreiten.yaml")',              # Ladepfad
        'open(DATA_DIR / "ove_e07_funktionserhalt.yaml")',     # Dateizugriff
    ):
        baum = ast.parse(quelltext)
        assert [w for _, w in _code_strings(baum)
                if any(n in w for n in _BEWACHTE_DATEIEN)], quelltext


# ── E05 / E06: Anwendungsbereich und Bezugsnorm binden ───────────────────────
E0506 = _lade("ove_e05_e06_anlagen.yaml")


def test_e05_ist_an_eine_norm_von_1991_gebunden() -> None:
    """Aktuelles Deckblatt, historischer Inhalt — beides muss sichtbar sein."""
    q = E0506["e05"]["quelle"]
    assert "2021-01-01" in q["ausgabe"] and "1991" in q["ausgabe"]
    assert "§ 90:1991" in q["bezugsnorm"] and "NICHT im Repo" in q["bezugsnorm"]


def test_e05_klassifikation_bleibt_im_eigenen_geltungsbereich() -> None:
    """Genau das ist E05s Kernaussage — und unsere Regel gegen Begriffsgleichsetzung."""
    kern = E0506["e05"]["kernaussage"]
    assert "IM SINNE DIESER BESTIMMUNGEN" in kern["aussage"]
    assert "eigenen Geltungsbereich" in kern["aussage"]
    assert "NICHT ergaenzt oder geraten" in kern["⚠_inhalt_nicht_ergaenzt"]


def test_e05_wird_nicht_mit_der_oib_garagenschwelle_vermischt() -> None:
    """Installationsart (E05) und Erforderlichkeit (OIB-RL 2.2) sind zwei Fragen."""
    v = E0506["e05"]["verhaeltnis_zu_oib_rl2_2"]
    assert "250 m²" in v["oib_fundstelle"]
    assert "begruendet KEINE" in v["⚠_keine_uebertragung"]
    assert "Begriffsgleichheit" in v["⚠_keine_uebertragung"]


def test_e05_gegenprobe_an_der_geltenden_norm() -> None:
    """OVE E 8101 Teil 7-7N90 wiederholt die pauschale Einstufung nicht."""
    g = E0506["e05"]["gegenprobe_e8101"]
    assert "7N90" in g["fundstelle"]
    assert "NICHT wiederholt" in g["⚠_folge"]
    assert "1991" in g["⚠_folge"]


def test_e06_gilt_nur_fuer_kombinierte_bussysteme() -> None:
    """Der Anwendungsbereich ist eng — und wird ausdrücklich begrenzt."""
    a = E0506["e06"]["anwendungsbereich"]
    assert "7.8.3" in a["definition"]
    assert "NUR fuer diesen Fall" in a["⚠_grenze"]
    assert "getrenntes Bussystem" in a["grundsatz"]


def test_e06_05s_ist_nicht_die_en1838_umschaltzeit() -> None:
    """Drei verschiedene 0,5-s-/Umschalt-Aussagen dürfen nicht verschmelzen."""
    u = E0506["e06"]["umschaltzeit_abgrenzung"]
    assert "kombinierte Bussysteme" in u["e06_wert"]
    assert "§ 4.4.6" in u["en1838_werte"]
    assert "KEINE allgemeine Verschaerfung" in u["⚠_nicht_gleichsetzen"]
    # Der Contract-Wert bleibt, was EN 1838 sagt.
    assert En1838NormProvider().fuer_raum("GANG", True).umschaltzeit_max_s == 60.0


def test_e06_pruefungen_sind_vollstaendig_und_getrennt() -> None:
    """Erst- und Wiederholungsprüfung stehen getrennt, mit ihrem Unterschied."""
    p = E0506["e06"]["pruefungen"]
    assert len(p["erstpruefung"]["punkte"]) == 5
    assert len(p["wiederholungspruefung"]["punkte"]) == 4
    assert "AKTUALITAET" in p["wiederholungspruefung"]["⚠_unterschied_zur_erstpruefung"]
    assert "kein Intervall" in p["wiederholungspruefung"]["⚠_unterschied_zur_erstpruefung"]


def test_e05_e06_haben_keinen_verbraucher() -> None:
    """Beide betreffen Anlagentechnik — kein Platzierungs- oder Normwert."""
    for block in ("e05", "e06"):
        r = E0506[block]["relevanz_notbeleuchtung"]
        assert r["einstufung"] == "mittelbar"
        assert r["verbraucher"] is None
        assert r["status"] == "nicht_pruefbar"


def test_fehlende_primaerquellen_sind_benannt_nicht_ersetzt() -> None:
    """Drei fehlende Bezugsnormen, je mit Zweck und Beschaffungsweg."""
    quellen = E0506["fehlende_primaerquellen"]
    assert len(quellen) == 3
    assert all(q["braucht_fuer"] and q["beschaffung"] for q in quellen)
    assert any("E 8002-1:2007" in q["quelle"] for q in quellen)


# ── Die zwei Aussagen mit der Zahl 20 ────────────────────────────────────────
def test_zwanzig_leuchten_zwei_verschiedene_aussagen() -> None:
    """Endstromkreis-Grenze (Ebene C) ≠ Prüfeinrichtung je Gebäudeteil (Ebene D).

    Die E-8101-Fundstelle darf nicht als Beleg für die Prüfeinrichtung dienen —
    dieser Test hält die Trennung fest.
    """
    e8101 = E07["e8101_gegenprobe"][0]
    trennung = e8101["⚠_nicht_verwechseln_mit_e08"]
    assert "JE ENDSTROMKREIS" in trennung
    assert "ZUSAMMENHAENGENDEN GEBAEUDETEIL" in trennung
    assert "EN 62034" in trennung
    assert "darf NICHT" in trennung and "als Beleg" in trennung
    # Und die E08-Seite nennt ihre eigene Bezugsgröße.
    astv = _lade("astv_arbeitsstaetten.yaml")
    e08 = next(a for a in astv["ausfuehrung_e08"] if a["kennung"] == "e08_anlagenanforderungen")
    assert "Gebaeudeteil" in e08["deckung_mit_engine"]["pruefeinrichtung_ab_20_leuchten"]
    assert "ENDSTROMKREIS" in e08["deckung_mit_engine"]["stromkreis_aufteilung"]
    assert "getrennt zu fuehren" in e08["deckung_mit_engine"]["⚠_zwei_mal_die_zahl_20"]


# ── RL 4: was mit vorhandenen Daten heute schon messbar wäre ────────────────
def test_rl4_tuerpruefung_bleibt_bis_zur_semantik_blockiert() -> None:
    """⚠️ Korrektur: `Tuer.breite_mm` taugt HEUTE nicht als Prüfgröße.

    Am Code von `origin/main` `e79276b` geprüft: das Feld trägt **vier**
    Messherkünfte — Nennmaß aus dem Blocknamen (`TUER-80` → 800 mm),
    Schwenkradius, Doppelflügel-Summe und lichte Wandöffnung. RL 4 verlangt
    dagegen die **nutzbare Durchgangslichte als Fertigmaß** (Vorbemerkungen).
    Ein Vergleich wäre systematisch zu günstig. Der Messwert der Fixtures steht
    hier nur als Beobachtung, nicht als Freigabe.

    Die Zahl ist **scharf** gepinnt (`== 4`, ausdrücklich nicht `>= 4`): ein
    fünfter Schreibpfad soll rot werden statt still mitzulaufen. `befunde` zählt
    **Bedeutungen**, nicht Codestellen — `tuer_zuordnung.py:158` und `:220`
    setzen dieselbe Bedeutung und stehen deshalb in **einem** Befund.
    """
    import json

    herkunft = RL4["tuerbreite_herkunft"]
    assert herkunft["status"] == "blockiert_bis_semantik_geklaert"
    assert len(herkunft["befunde"]) == 4
    assert [b["herkunft"] for b in herkunft["befunde"]] == [
        "BLOCKNAME",
        "GEOMETRIE_SCHWENKRADIUS",
        "GEOMETRIE_SUMME",
        "GEOMETRIE_OEFFNUNG",
    ]
    # Die Namen sind nicht frei gewählt: sie müssen im Contract-Vokabular
    # `BreiteQuelle` stehen, sonst beschreibt die YAML etwas, das es nicht gibt.
    from typing import get_args

    from notbeleuchtung.hauptengine.contracts.raum_modell import BreiteQuelle

    assert {b["herkunft"] for b in herkunft["befunde"]} <= set(get_args(BreiteQuelle))
    # Jede Herkunft nennt ihre Fundstelle im Erkennungscode — sonst ist der
    # Befund nicht nachprüfbar.
    assert all(b["pfad"].split("::")[0].split(":")[0].endswith(".py")
               for b in herkunft["befunde"])
    # Der Doppelflügel-Befund darf nicht mit RL 4 Punkt 2.8.1 begründet werden.
    summe = next(b for b in herkunft["befunde"] if b["herkunft"] == "GEOMETRIE_SUMME")
    assert "NICHT die Zwei-Tueren-Regel" in summe["was"]
    assert "UNZULAESSIG" in herkunft["folge"]
    # „nicht gemessen" ist keine Messherkunft und steht deshalb außerhalb.
    keine = herkunft["keine_messung"]
    assert "None" in keine["was"] and '"UNBEKANNT"' in keine["was"]
    assert "0.0" not in keine["was"], "0.0 ist seit Contract 1.4.0 keine gültige Lesart"
    assert "1.4.0" in keine["⚠_0_0_ist_ueberholt"]
    assert RL4["anwendungsbereich"]["⚠_fertigmass"].strip().startswith('"Alle in dieser')

    fixtures = sorted((Path(__file__).parents[1] / "fixtures").glob("raum_modell_*.json"))
    breiten = [t.get("breite_mm", 0.0)
               for f in fixtures
               for t in json.loads(f.read_text(encoding="utf-8")).get("tueren", [])]
    assert breiten, "Fixtures führen keine Türen"
    # Beobachtung, kein Nachweis: die Werte sind 900/1000/1400 — typische
    # NENNmaße, was den Befund oben stützt.
    assert set(breiten) <= {900.0, 1000.0, 1400.0}, sorted(set(breiten))


def test_keine_messung_heisst_none_nicht_null() -> None:
    """Die YAML-Aussage über „keine Messung" muss zum Contract passen.

    Seit `raum_modell` 1.4.0 ist `Tuer.breite_mm` `float | None`: `None` heißt
    **nicht gemessen**, `0.0` hieße **gemessen null** und kommt nicht mehr vor.
    Steht in unserer YAML wieder die alte 0.0-Lesart, prüft RL 4 gegen eine
    Bedeutung, die es nicht gibt — genau das fängt dieser Test.
    """
    from notbeleuchtung.hauptengine.contracts.raum_modell import Tuer

    ohne_messung = Tuer(id="t1", xy_mm=(0.0, 0.0))
    assert ohne_messung.breite_mm is None
    assert ohne_messung.breite_quelle == "UNBEKANNT"

    herkunft = RL4["tuerbreite_herkunft"]
    fragen = herkunft["vor_jeder_pruefung_zu_klaeren"]
    assert [f["stand"] for f in fragen] == ["beantwortet", "offen", "beantwortet"]
    # Die offene Frage ist die Umrechnung zur Durchgangslichte — und nur sie
    # hält den Status.
    offen = next(f for f in fragen if f["stand"] == "offen")
    assert "Durchgangslichte" in offen["frage"]
    assert herkunft["status"] == "blockiert_bis_semantik_geklaert"
    assert "VERGLEICHBARKEIT" in herkunft["⚠_status_bleibt"]


def test_drei_breitenbegriffe_bleiben_getrennt() -> None:
    """Mindestbreite, örtliche Engstelle und Breite entlang des Weges."""
    begriffe = {b["begriff"]: b for b in RL4["breiten_begriffe"]}
    assert set(begriffe) == {
        "erforderliche Mindestbreite",
        "oertliche Engstelle",
        "tatsaechliche Breite entlang des Weges",
    }
    eng = begriffe["oertliche Engstelle"]["verwendung"]
    assert "NICHT als Breite des ganzen" in eng
    assert "breitere Bereiche aus der" in eng          # dürfen nicht verschwinden
    profil = begriffe["tatsaechliche Breite entlang des Weges"]["verwendung"]
    assert "Abschnitte konstanter Breite" in profil and "Breitenprofil" in profil
    assert "2-m-Grenze" in profil
    assert "Drei Groessen, drei Aussagen" in RL4["breiten_begriffe_regel"]


def test_rl4_anwendungsbereich_und_ausnahmen_am_original() -> None:
    """Vorbemerkungen: Kleingebäude-Ausnahme, Landesrecht, Fertigmaß, Personenzahl."""
    a = RL4["anwendungsbereich"]
    assert "15 m²" in a["ausnahme_kleingebaeude"]
    assert "landesrechtlichen" in a["barrierefreiheit_kommt_aus_landesrecht"]
    assert "drei Geschosse" in a["personenzahl_definition"]
    assert "angewiesen sind" in a["personenzahl_definition"]
    assert "nicht nachgewiesen" in a["abweichungsklausel"]


def test_zwanzig_leuchten_zwei_fundstellen_zwei_bezugseinheiten() -> None:
    """⚠️ Korrektur: die Prüfeinrichtung ist NORMATIV belegt, nicht nur über E08.

    OVE E 8101 Teil 5-56 **560.9.001.AT** trägt sie in **beiden** Ausgaben
    (2019 und 2025) wortgleich; E08 5.2 wiederholt sie nur. Die zweite Regel —
    höchstens 20 Leuchten je Endstromkreis — steht in **560.9.2**. Zwei
    Fundstellen, zwei Bezugseinheiten, keine belegt die andere.
    """
    z = _lade("astv_arbeitsstaetten.yaml")["zwanzig_leuchten"]
    a, b = z["a_endstromkreis"], z["b_automatische_pruefeinrichtung"]
    assert a["ebene"] == "C" and a["bezugseinheit"] == "Endstromkreis"
    assert "560.9.2" in a["fundstelle"]
    assert b["ebene"] == "C"                       # nicht D
    assert "560.9.001.AT" in b["fundstelle_norm"]
    assert "2019" in b["fundstelle_norm"] and "2025" in b["fundstelle_norm"]
    assert "E08:2021-04-01" in b["fundstelle_fachinformation"]
    assert "wiederholt" in b["fundstelle_fachinformation"]
    assert b["bezugseinheit"] == "zusammenhaengender Gebaeudeteil"
    assert "WORTGLEICH" in b["unterschied_2019_zu_2025"]
    assert len(b["zusatzanforderungen_2025"]) == 3
    assert "nicht definiert" in b["⚠_begriffsgrenze"]
    assert "belegt die andere" in z["⚠_keine_kreuzbelege"]


def test_vorhandener_verbraucher_ist_als_vorlaeufig_dokumentiert() -> None:
    """`pipeline._coverage` ist der Verbraucher — sein Hinweis bleibt vorläufig.

    Die Geschosszählung ist **kein** Nachweis für die Gebäudeteilzählung der
    Norm; aus ihr folgt weder Pflicht noch Entwarnung. Was fehlt, ist keine
    Quelle, sondern zwei Projektangaben. Leonis' Datei bleibt unverändert, und
    es entsteht **keine zweite Regel** daneben.
    """
    v = _lade("astv_arbeitsstaetten.yaml")["zwanzig_leuchten"]["vorhandener_verbraucher"]
    assert "_coverage" in v["stelle"] and "_AUTO_PRUEF_SCHWELLE" in v["stelle"]
    assert v["quelle_korrekt"] is True
    assert v["einstufung"] == "vorlaeufiger_hinweis"
    assert "NICHT von Enis geaendert" in v["owner"]

    z = v["zwei_zaehlungen_die_nicht_dasselbe_sind"]
    assert "EINES\n        GESCHOSSES" in z["geschosszaehlung_heute"] or "GESCHOSSES" in z["geschosszaehlung_heute"]
    assert "ZUSAMMENHAENGENDEN" in z["gebaeudeteilzaehlung_der_norm"]
    assert "KEIN Nachweis" in z["⚠_kein_ersatz"]
    assert "Halbsatz" in z["⚠_kein_ersatz"]          # erläuternder Zusatz genügt nicht

    schluss = v["⚠_keine_schlussfolgerung_aus_der_geschosszahl"]
    assert len(schluss) == 3
    assert any("KEINE abschliessende Pflicht" in s for s in schluss)
    assert any("KEINE Entwarnung" in s for s in schluss)
    assert any("nicht behaupten, eine Pruefeinrichtung fehle" in s for s in schluss)

    fehlt = v["fehlende_angaben_fuer_einen_belastbaren_befund"]
    assert len(fehlt) == 3
    assert any("Abgrenzung" in f for f in fehlt) and any("Zuordnung" in f for f in fehlt)
    assert "keine zweite Regel" in v["empfehlung_an_den_owner"]

    # Die Begriffsgrenze sagt jetzt, WAS fehlt — nicht, dass es unmöglich wäre.
    b = _lade("astv_arbeitsstaetten.yaml")["zwanzig_leuchten"]["b_automatische_pruefeinrichtung"]
    assert "folgt NICHT, dass die Regel unumsetzbar" in b["⚠_begriffsgrenze"]
    assert "FACHLICHE ABGRENZUNG" in b["⚠_begriffsgrenze"]
    assert "exakt auswertbar" in b["⚠_begriffsgrenze"]

    # Und die Stelle existiert wirklich so im Code (sonst ist die Doku veraltet).
    pipeline = (SRC / "hauptengine" / "pipeline.py").read_text(encoding="utf-8")
    assert "_AUTO_PRUEF_SCHWELLE = 20" in pipeline
    assert "560.9.001.AT" in pipeline
    assert "len(platzierung.platzierungen)" in pipeline
