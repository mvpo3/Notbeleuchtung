"""Migration Phase A (2026-09-18) — Guard: kein Pfad zurück zu den alten Symbolen.

Die alte Bibliothek (CAD_Symbole/Notbeleuchtungssymbole.dxf, per git rm entfernt —
Git-Historie ist das Backup) und ihre Blocknamen dürfen in Code, Tests, Skripten
und Konfigs NICHT mehr vorkommen; ebenso wenig der entfernte gelbe SL-Zwilling-
Layer und der gestrichene rz_sl_farbtrennung-Parameter. docs/ ist bewusst
ausgenommen (die Migrations-Doku dokumentiert das Mapping alt → neu, ADRs sind
Historie).
"""
from __future__ import annotations

from pathlib import Path

from notbeleuchtung.symbols import library, load_symbol_mapping
from notbeleuchtung.symbols.orientation import ZIEL_DEG, basis_deg, transformation

_REPO = Path(__file__).resolve().parents[2]
_SELBST = Path(__file__).resolve()

# Alt-Marker (case-insensitiv). Der alte Bibliothekspfad matcht NICHT die neue
# Datei (Notbeleuchtungssymbole_neu+.dxf hat "_neu+" vor ".dxf").
# Bewusst NICHT verboten: "din_SIBEL_10_emergency_lighting_yellow" — der String
# lebt legitim im din-REFERENZPLAN-Leser weiter (scripts/plan_pruefen._REF_LAYER_KIND
# liest den Fachplaner-Plan Barawitzkagasse, dessen Fremd-Konvention grün/gelb ist);
# als ENGINE-Ausgabe-Layer ist er über das Streichen von library.SAFETY_LAYER_SL tot.
_VERBOTEN = (
    "richtungspfeil nach",                  # alte Pfeil-Blocknamen (alle drei)
    "notbeleuchtung- antipanikleuchte",     # alter Antipanik-Block
    "notbeleuchtungssymbole.dxf",           # alter Bibliothekspfad
    "safety_layer_sl",                      # entfernte SL-Zwilling-Konstante
    "rz_sl_farbtrennung",                   # gestrichener Render-Parameter
)

_SCAN_ORDNER = ("src", "tests", "scripts")
_SCAN_ENDUNGEN = {".py", ".yaml", ".yml", ".json", ".toml"}


def test_keine_alt_referenzen_im_code():
    funde: list[str] = []
    for ordner in _SCAN_ORDNER:
        for datei in (_REPO / ordner).rglob("*"):
            if datei.suffix.lower() not in _SCAN_ENDUNGEN or datei.resolve() == _SELBST:
                continue
            try:
                text = datei.read_text(encoding="utf-8", errors="ignore").lower()
            except OSError:
                continue
            for marker in _VERBOTEN:
                if marker in text:
                    funde.append(f"{datei.relative_to(_REPO)}: {marker!r}")
    assert not funde, "Alt-Referenzen gefunden:\n  " + "\n  ".join(funde)


def test_alte_bibliothek_ist_entfernt():
    assert not (_REPO / "CAD_Symbole" / "Notbeleuchtungssymbole.dxf").exists()
    assert (_REPO / "CAD_Symbole" / "Notbeleuchtungssymbole_neu+.dxf").is_file()


def test_registry_loest_jeden_typ_genau_einmal_auf():
    """Jeder catalog_key der Registry löst zu genau einem existierenden Block der
    neuen Bibliothek auf (load_mapping validiert die Existenz fail-loud)."""
    mapping = library.load_mapping()
    namen = {n.lower() for n in library.load_library().blocks.block_names()}
    for key, entry in mapping.items():
        assert entry["block_name"].lower() in namen, key
    # Richtungs-Keys kennen ihre Basisorientierung (sonst stiller rot-0-Rückfall).
    for key in ("notlicht_ks_stiege", "notlicht_ks_stiege_unten",
                "notlicht_ks_stiege_links", "notlicht_ks_stiege_rechts",
                "notlicht_kw_garage"):
        assert basis_deg(load_symbol_mapping()[key]["block_name"]) is not None, key


def test_rotationstest_welt_pfeil_je_typ():
    """A6-Rotationstest: für jeden Richtungs-Typ ergibt Basis + transformation()
    exakt die Ziel-Weltrichtung (Pfeilvektor-Algebra der Registry)."""
    for key in ("notlicht_ks_stiege_links", "notlicht_ks_stiege_rechts",
                "notlicht_ks_stiege_unten"):
        block = load_symbol_mapping()[key]["block_name"]
        basis = basis_deg(block)
        for richtung, ziel in ZIEL_DEG.items():
            rot, mirror = transformation(key, richtung)
            assert mirror is False
            assert (basis + rot) % 360.0 == ziel, (key, richtung)
