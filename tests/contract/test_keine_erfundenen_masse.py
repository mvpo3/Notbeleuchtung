"""Riegel gegen erfundene Masse: kein Zahlen-Literal in einem Messfeld.

Kernregel des Projekts: der Code erfindet keine Masse. Fehlt eine Messung, ist
das Feld ``None`` mit ``quelle=UNBEKANNT`` und einem Grund — nie ein Default,
nie ein Normwert, nie ein Mittelwert.

Der Test arbeitet statisch (AST) statt zur Laufzeit, weil genau die kritischen
Faelle selten sind (Tueren ohne Messung) und ein gruener Prueflauf ueber fuenf
Plaene nichts beweist. Regex scheitert am Unterschied zwischen
``t.breite_mm or 900.0`` (Mass) und ``farbe or 256`` (DXF-Farbindex) — der steckt
im Feldnamen links, nicht in der Zahl. Der AST sieht den Namen.

Was ein Messfeld ist, kommt aus den Contracts selbst (Pydantic ``model_fields``),
damit ein neues Massfeld automatisch mitgeschuetzt ist.

Erlaubt bleibt ``0.0``/``0`` — das ist der bekannte, separat gefuehrte Fall
"falsch typisiertes Nicht-Mass", kein erfundener Wert.
"""
import ast
import importlib
import pkgutil
from pathlib import Path

import pytest
from pydantic import BaseModel

import notbeleuchtung
from notbeleuchtung.hauptengine import contracts

_SRC = Path(notbeleuchtung.__file__).resolve().parent

# Koordinaten, keine Masse — ein Literal kann hier gar kein Mass sein.
_KOORDINATEN = {"xy_mm", "bounds_mm", "polygon_mm", "polyline_mm",
                "verbotszonen_mm", "antritt_mm", "austritt_mm",
                "min_xy", "max_xy"}
# norm_regelwerk traegt Norm-Grenzen und Schwellen (EN 1838 / OIB), keine
# Messungen am Bestand — dort IST die Zahl der Inhalt.
_NORM_MODUL = "norm_regelwerk"

# Ausnahmen als Modulpfad-Praefix + Pflicht-Begruendung, damit keine wortlos waechst.
ERLAUBT: dict[str, str] = {
    # Erfindet 800/1000/200 mm, ist aber seit dem Port nicht importierbar
    # (siehe test_port_bleibt_tot). Wird es je angeschlossen, muss es mit.
    "raumerkennung/_port/": "toter Port, nicht importierbar",
}


def _messfelder() -> set[str]:
    namen: set[str] = set()
    for modul in pkgutil.iter_modules(contracts.__path__):
        if modul.name == _NORM_MODUL:
            continue
        mod = importlib.import_module(f"{contracts.__name__}.{modul.name}")
        for obj in vars(mod).values():
            if isinstance(obj, type) and issubclass(obj, BaseModel):
                namen |= {f for f in obj.model_fields
                          if f.endswith(("_mm", "_m2")) and f not in _KOORDINATEN}
    return namen


MESSFELDER = _messfelder()


def _zahl(node) -> float | None:
    """Numerisches Literal != 0, sonst None. 0.0 ist erlaubt."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) \
            and not isinstance(node.value, bool) and node.value != 0:
        return float(node.value)
    return None


def _feldname(node) -> str | None:
    if isinstance(node, ast.Attribute) and node.attr in MESSFELDER:
        return node.attr
    if isinstance(node, ast.Name) and node.id in MESSFELDER:
        return node.id
    return None


def _feldname_flach(node) -> str | None:
    """Wie _feldname, sieht aber durch ein vorgeschaltetes 'or 0.0' hindurch."""
    if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or):
        for wert in node.values:
            if (feld := _feldname(wert)):
                return feld
        return None
    return _feldname(node)


def _pruefe_datei(pfad: Path) -> list[str]:
    baum = ast.parse(pfad.read_text(encoding="utf-8"), filename=str(pfad))
    treffer: list[str] = []

    def melde(node, text: str) -> None:
        treffer.append(f"{pfad.relative_to(_SRC).as_posix()}:{node.lineno} — {text}")

    for node in ast.walk(baum):
        # (1) t.breite_mm or 900.0  → Ersatzmass statt None
        if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or):
            for links, rechts in zip(node.values, node.values[1:]):
                feld, wert = _feldname(links), _zahl(rechts)
                if feld and wert is not None:
                    melde(node, f"'{feld} or {wert}' erfindet ein Mass — None + Grund benutzen")
        # (2) Tuer(breite_mm=900.0)
        if isinstance(node, ast.Call):
            for kw in node.keywords:
                if kw.arg in MESSFELDER and (wert := _zahl(kw.value)) is not None:
                    melde(node, f"'{kw.arg}={wert}' schreibt ein erfundenes Mass in ein Messfeld")
            # (3) min/max(t.breite_mm, 400.0) → deckelt/hebt ein Mass auf eine Zahl
            fn = node.func
            if isinstance(fn, ast.Name) and fn.id in ("min", "max"):
                # ein 'or 0.0' davor zaehlt mit: max(t.breite_mm or 0.0, 400.0).
                # Tiefer wird NICHT gesucht — max(1, round(max(_KONST, x)/res)) ist
                # eine Raster-Schwelle, kein Ersatzmass.
                felder = [f for a in node.args if (f := _feldname_flach(a))]
                zahlen = [z for a in node.args if (z := _zahl(a)) is not None]
                if felder and zahlen:
                    melde(node, f"'{fn.id}({felder[0]}, {zahlen[0]})' ersetzt ein Mass "
                                f"durch eine Zahl — benannte Zeichen-Konstante benutzen")
    return treffer


def test_messfelder_aus_contract_gefunden():
    """Schutzschalter: waechst die Feldliste nicht mit, prueft der Test nichts."""
    assert {"breite_mm", "flaeche_m2", "laenge_mm", "len_mm"} <= MESSFELDER, MESSFELDER


def test_keine_erfundenen_masse():
    befunde: list[str] = []
    for pfad in sorted(_SRC.rglob("*.py")):
        rel = pfad.relative_to(_SRC).as_posix()
        if any(rel.startswith(p) for p in ERLAUBT):
            continue
        befunde += _pruefe_datei(pfad)
    assert not befunde, "Erfundene Masse in Messfeldern:\n" + "\n".join(befunde)


def test_port_bleibt_tot():
    """_port/engine_walls erfindet 800/1000/200 mm. Solange es nicht importierbar
    ist, ist das folgenlos — wird es je angeschlossen, muss dieser Test rot werden
    und die Erfindungen muessen mit aufgeraeumt werden."""
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module("notbeleuchtung.raumerkennung._port.engine_walls")
