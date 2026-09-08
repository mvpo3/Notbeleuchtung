"""norm_coverage — Wissens-Konsum je Plan sichtbar machen (Skill plan-verify)."""
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "scripts"))
import norm_coverage as nc

QUELLEN = ["ÖNORM EN 1838:2013 §4.2.1", "ÖNORM EN 1838:2013 §4.3.1"]


@dataclass
class P:
    norm_quelle: str
    kind: str = "rz"
    catalog_key: str = "x"


def test_klassifikation_norm_praxis_unbegruendet():
    plz = [
        P("ÖNORM EN 1838:2013 §4.2.1", "rz"),                 # norm
        P("ÖNORM EN 1838:2013 §4.3.1", "antipanik"),          # norm
        P("Referenz-Praxis: Technik-/Nebenraum-SL", "rz"),    # praxis
        P("fachpraxis: aufheller-500mm", "sicherheitsleuchte"),  # praxis
        P("", "sicherheitsleuchte", "mystery"),               # unbegruendet
    ]
    b = nc.norm_deckung(plz, QUELLEN)
    assert (b.gesamt, b.norm, b.praxis, b.unbegruendet) == (5, 2, 2, 1)
    assert b.unbegruendet_liste == [("sicherheitsleuchte", "mystery")]
    assert b.gesund is False
    assert "NO-GO" in nc.report(b)


def test_alles_begruendet_ist_gesund():
    plz = [P("ÖNORM EN 1838:2013 §4.2.1"), P("fachpraxis: aufheller-500mm", "sicherheitsleuchte")]
    b = nc.norm_deckung(plz, QUELLEN)
    assert b.gesund is True
    assert b.norm == 1 and b.praxis == 1
    assert "GO" in nc.report(b) and "NO-GO" not in nc.report(b)


def test_unbekannte_quelle_zaehlt_als_unbegruendet():
    # Ein Norm-artiger String, der NICHT in quellen liegt (Provider vergibt ihn nicht)
    # → unbegründet, nicht still als norm durchgewinkt.
    b = nc.norm_deckung([P("ÖNORM EN 1838:2013 §9.9.9 (erfunden)")], QUELLEN)
    assert b.unbegruendet == 1 and b.norm == 0


def test_je_kind_aufschluesselung():
    plz = [P("ÖNORM EN 1838:2013 §4.2.1", "rz"), P("", "rz", "z")]
    b = nc.norm_deckung(plz, QUELLEN)
    assert b.je_kind["rz"] == {"norm": 1, "praxis": 0, "unbegruendet": 1}
