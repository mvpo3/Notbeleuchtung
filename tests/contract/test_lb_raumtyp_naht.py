"""Naht-Invariante Enis↔Selman: LB-Raumtypen ⊆ Raumtypen der Raumerkennung.

Der LB-Parser entscheidet fail closed anhand von `unterstuetzte_raum_typen`
(`normwissen/data/lb_extraktion.yaml`), ob eine Bereichsregel im Platzierer
überhaupt wirken kann. Diese Liste ist eine **Kopie** der Labels, die
`raumerkennung/raumtyp.py` vergibt — und Kopien driften.

Beide Richtungen sind echte Fehler, keine Kosmetik:

* **Typ fehlt in der YAML** → der Parser blockiert eine Vorgabe, die der
  Platzierer umsetzen könnte (real passiert: GARAGE blockierte noch, nachdem
  PR #49 das Label eingeführt hatte — beide realen Elektro-LBs waren dadurch
  unparsebar).
* **Typ steht nur in der YAML** → der Parser lässt eine Regel durch, die im
  Platzierer ein stiller No-op ist. Genau das soll fail closed verhindern.

Der Test liegt bewusst in `tests/contract/`: er prüft die Naht zwischen zwei
Owner-Packages, nicht das Innere eines der beiden. Die Packages selbst
importieren einander weiterhin nicht.
"""
import yaml

from notbeleuchtung.normwissen.lb.parser import DATA_DIR, DATEI
from notbeleuchtung.raumerkennung import raumtyp


def _lb_typen() -> set[str]:
    cfg = yaml.safe_load((DATA_DIR / DATEI).read_text(encoding="utf-8"))
    return set(cfg["unterstuetzte_raum_typen"])


def _raumerkennung_typen() -> set[str]:
    """Alle Labels, die `raumtyp_flags()` vergeben kann."""
    return {v[0] for v in raumtyp._TYP_MAP.values()} | {
        v[0] for v in raumtyp._EXTRA_DIRECT.values()
    }


def test_lb_stuetzliste_deckt_sich_mit_raumerkennung():
    lb, rt = _lb_typen(), _raumerkennung_typen()
    assert lb - rt == set(), (
        "LB-Stützliste kennt Typen, die die Raumerkennung nicht vergibt — "
        "die Regel wäre im Platzierer ein stiller No-op: " + repr(sorted(lb - rt))
    )
    assert rt - lb == set(), (
        "Die Raumerkennung vergibt Typen, die die LB-Stützliste nicht kennt — "
        "der Parser blockiert erfüllbare Vorgaben: " + repr(sorted(rt - lb))
    )


def test_lb_vokabular_zeigt_nur_auf_stuetzbare_typen():
    """Jedes Label im Begriffs-Vokabular muss auch in der Stützliste stehen —
    sonst kann der Parser einen Typ erkennen, den er anschließend weder als Wert
    noch als Review korrekt einordnet."""
    cfg = yaml.safe_load((DATA_DIR / DATEI).read_text(encoding="utf-8"))
    vokabular = set(cfg["raum_typ_vokabular"])
    assert vokabular <= _lb_typen(), repr(sorted(vokabular - _lb_typen()))
