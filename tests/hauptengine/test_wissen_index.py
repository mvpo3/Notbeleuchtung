"""wissen_index — deterministischer Wissens-Index (Skill `wissen`)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "scripts"))
import wissen_index as wi


def _korpus(root: Path):
    (root / "knowledge/extracted").mkdir(parents=True)
    (root / "src/notbeleuchtung/normwissen/data").mkdir(parents=True)
    (root / "docs/adr").mkdir(parents=True)
    (root / "Handoff").mkdir(parents=True)
    (root / "knowledge/extracted/foo.md").write_text(
        "# Foo-Digest\n\nDies ist die erste inhaltliche Zeile.\n", encoding="utf-8"
    )
    (root / "src/notbeleuchtung/normwissen/data/bar.yaml").write_text(
        "# ═══════════════════\n# bar — echte Beschreibung der Norm-Datei\nk: 1\n",
        encoding="utf-8",
    )
    (root / "docs/adr/0001-x.md").write_text("# ADR-0001 X\n\nStatus bindend.\n", encoding="utf-8")
    (root / "Handoff/LEONIS.md").write_text("# Handoff Leonis\n\nOwner-Package.\n", encoding="utf-8")


def test_index_verlinkt_und_belegt(tmp_path):
    _korpus(tmp_path)
    idx = wi.baue_index(tmp_path)
    # Header + Autoritativ-Warnung
    assert "GENERIERT" in idx and "AUTORITATIV" in idx
    # Verlinkt jede Quelle relativ + mit Haken
    assert "(knowledge/extracted/foo.md)" in idx
    assert "Dies ist die erste inhaltliche Zeile." in idx
    assert "(src/notbeleuchtung/normwissen/data/bar.yaml)" in idx
    # YAML-Haken: Deko-Banner übersprungen, echter Text genommen
    assert "echte Beschreibung der Norm-Datei" in idx
    assert "═══" not in idx.split("bar.yaml")[1].splitlines()[0]
    # md-Titel = erste '# '-Überschrift, nicht Dateiname
    assert "[Foo-Digest]" in idx and "[ADR-0001 X]" in idx


def test_deterministisch(tmp_path):
    _korpus(tmp_path)
    assert wi.baue_index(tmp_path) == wi.baue_index(tmp_path)


def test_leere_sektion_meldet_statt_crashen(tmp_path):
    (tmp_path / "knowledge/extracted").mkdir(parents=True)
    idx = wi.baue_index(tmp_path)
    assert "(keine Dateien gefunden)" in idx
