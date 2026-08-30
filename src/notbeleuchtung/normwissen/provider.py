"""En1838NormProvider — Enis' Query-API über das ÖNorm-EN-1838-Wissen.

Erfüllt das Protocol `hauptengine.contracts.ports.NormProvider`. Leonis FRAGT
diesen Provider (`fuer_raum`, `fuer_fluchtweg_abschnitt`, `erkennungsweite_m`,
`regelwerk_snapshot`) — er parst nie YAML. Alle Werte kommen aus
`data/en1838_grundwerte.yaml` (Norm-Grundwerte) + `data/raumtyp_regeln.yaml`
(Raumtyp → Anforderung); dieses Modul hardcodet nichts.

Jede NormAnforderung.quelle ist eine echte Norm-Fundstelle (Audit-Trail). Die
Naht-Invariante (tests/contract) prüft, dass jede Platzierung.norm_quelle in
`regelwerk_snapshot().quellen` liegt.
"""
from __future__ import annotations

from functools import cached_property
from pathlib import Path

import yaml

from notbeleuchtung.hauptengine.contracts import (
    ErkennungsweiteParameter,
    FluchtwegSegment,
    NormAnforderung,
    NormRegelwerk,
    RaumRegel,
)

DATA_DIR = Path(__file__).parent / "data"


def _load_yaml(name: str) -> dict:
    with open(DATA_DIR / name, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


class En1838NormProvider:
    """NormProvider-Impl gegen data/*.yaml (ÖNORM EN 1838:2013)."""

    def __init__(self, data_dir: Path | None = None) -> None:
        self._dir = data_dir or DATA_DIR
        self._grund = self._read("en1838_grundwerte.yaml")
        self._regeln_doc = self._read("raumtyp_regeln.yaml")
        # (raum_typ, ist_fluchtweg) -> Roh-Regel-Dict; erster Treffer gewinnt.
        self._index = {
            (r["raum_typ"], bool(r["ist_fluchtweg"])): r
            for r in self._regeln_doc["regeln"]
        }

    def _read(self, name: str) -> dict:
        with open(self._dir / name, encoding="utf-8") as fh:
            return yaml.safe_load(fh)

    # ── Wert-Auflösung (refs → Grundwerte) ──────────────────────────────────
    def _lux(self, ref: str) -> float:
        return float(self._grund["lux"][ref])

    def _quelle(self, ref: str) -> str:
        return str(self._grund["quellen"][ref])

    def _anforderung_aus_regel(self, regel: dict) -> NormAnforderung:
        """Ein Roh-Regel-Dict (aus raumtyp_regeln.yaml) → typisierte NormAnforderung."""
        klass = regel["klassifikation"]
        # Erkennungsweite gilt nur für Rettungszeichen (§5.5), sonst None.
        erk = self._default_erkennungsweite_m() if klass == "rz" else None
        return NormAnforderung(
            min_lux=self._lux(regel["min_lux_ref"]),
            klassifikation=klass,
            montagehoehe_mm=self._montagehoehe(regel),
            erkennungsweite_m=erk,
            symbol_katalog_keys=list(regel.get("symbol_katalog_keys", [])),
            mindest_anzahl=int(regel.get("mindest_anzahl", 1)),
            dauer_min=int(self._grund["dauer_min"]),
            quelle=self._quelle(regel["quelle_ref"]),
        )

    def _montagehoehe(self, regel: dict) -> int:
        """Fachpraxis-Montagehöhe, nie unter dem Norm-Floor §4.1.1 (2000 mm)."""
        floor = int(self._grund["montagehoehe_min_mm"])
        return max(int(regel.get("montagehoehe_mm", floor)), floor)

    def _default_erkennungsweite_m(self) -> float:
        e = self._grund["erkennungsweite"]
        return round(e["z_hinterleuchtet"] * e["piktogramm_hoehe_default_m"], 3)

    # ── NormProvider-Protocol ───────────────────────────────────────────────
    def fuer_raum(self, raum_typ: str, ist_fluchtweg: bool) -> NormAnforderung:
        regel = self._index.get((raum_typ, bool(ist_fluchtweg)))
        if regel is None:
            regel = self._regeln_doc["default"]
        return self._anforderung_aus_regel(regel)

    def fuer_fluchtweg_abschnitt(self, segment: FluchtwegSegment) -> NormAnforderung:
        # Jeder Fluchtweg-Abschnitt ist ein Rettungsweg → Gang-Anforderung (§4.2.1).
        return self.fuer_raum("GANG", True)

    def erkennungsweite_m(self, piktogramm_hoehe_m: float, hinterleuchtet: bool) -> float:
        e = self._grund["erkennungsweite"]
        z = e["z_hinterleuchtet"] if hinterleuchtet else e["z_beleuchtet"]
        return z * piktogramm_hoehe_m

    @cached_property
    def _snapshot(self) -> NormRegelwerk:
        e = self._grund["erkennungsweite"]
        regeln = [
            RaumRegel(
                raum_typ=r["raum_typ"],
                ist_fluchtweg=bool(r["ist_fluchtweg"]),
                anforderung=self._anforderung_aus_regel(r),
            )
            for r in self._regeln_doc["regeln"]
        ]
        quellen = sorted({r.anforderung.quelle for r in regeln})
        return NormRegelwerk(
            norm=self._grund["norm"],
            erkennungsweite=ErkennungsweiteParameter(
                z_hinterleuchtet=e["z_hinterleuchtet"],
                z_beleuchtet=e["z_beleuchtet"],
            ),
            regeln=regeln,
            quellen=quellen,
        )

    def regelwerk_snapshot(self) -> NormRegelwerk:
        return self._snapshot
