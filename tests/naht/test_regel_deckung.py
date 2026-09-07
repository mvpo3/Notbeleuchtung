"""Naht-Guard: regel_deckung.yaml deckt den Raumtyp-Kanon lückenlos ab.

Jeder Typ, den die Raumerkennung vergibt (derselbe Kanon wie in
`test_vokabular_doku.py`), hat in `normwissen/data/regel_deckung.yaml` GENAU
einen Eintrag mit GENAU einer der drei Aussagen `platzierungsregel` /
`bewusst_keine` / `offen`. Referenzierte Regel-IDs müssen im Regelwerk
existieren (platzierung_regeln.yaml `id:` oder raumtyp_regeln.yaml
`raum_typ:`). Ein neuer Kanon-Typ ohne Deckungs-Eintrag bricht hier —
keine stillen Regel-Lücken.
"""
from pathlib import Path

import yaml

from notbeleuchtung.raumerkennung import raumtyp

DATA = Path(__file__).parent.parent.parent / "src/notbeleuchtung/normwissen/data"


def _kanon() -> set[str]:
    return (
        {v[0] for v in raumtyp._TYP_MAP.values()}
        | {v[0] for v in raumtyp._EXTRA_DIRECT.values()}
        | {v[0] for v in raumtyp._EXTRA_OVERRIDE.values()}
    )


def _deckung() -> dict:
    return yaml.safe_load((DATA / "regel_deckung.yaml").read_text(encoding="utf-8"))["deckung"]


def _bekannte_regel_ids() -> set[str]:
    pl = yaml.safe_load((DATA / "platzierung_regeln.yaml").read_text(encoding="utf-8"))
    ids = {
        r["id"]
        for key in ("rettungszeichen", "sicherheitsleuchten", "hard_stops")
        for r in pl.get(key, [])
    }
    rt = yaml.safe_load((DATA / "raumtyp_regeln.yaml").read_text(encoding="utf-8"))
    ids |= {r["raum_typ"] for r in rt.get("regeln", [])}
    return ids


def test_jeder_kanon_typ_genau_ein_eintrag():
    deckung, kanon = _deckung(), _kanon()
    assert set(deckung) == kanon, (
        f"fehlend: {sorted(kanon - set(deckung))} / "
        f"überzählig: {sorted(set(deckung) - kanon)}"
    )


def test_jeder_eintrag_genau_eine_aussage():
    erlaubt = {"platzierungsregel", "bewusst_keine", "offen"}
    for typ, eintrag in _deckung().items():
        keys = set(eintrag)
        assert len(keys) == 1 and keys <= erlaubt, f"{typ}: {sorted(keys)}"
        if "offen" in keys:
            assert set(eintrag["offen"]) == {"frage", "owner"}, f"{typ}: offen braucht frage+owner"


def test_referenzierte_regel_ids_existieren():
    bekannt = _bekannte_regel_ids()
    for typ, eintrag in _deckung().items():
        rid = eintrag.get("platzierungsregel")
        if rid is not None:
            assert rid in bekannt, f"{typ}: Regel-ID {rid!r} existiert im Regelwerk nicht"
