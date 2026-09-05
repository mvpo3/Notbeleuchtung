"""En1838NormProvider — Enis' Query-API über das ÖNorm-EN-1838-Wissen.

Erfüllt das Protocol `hauptengine.contracts.ports.NormProvider`. Leonis FRAGT
diesen Provider (`fuer_raum`, `fuer_fluchtweg_abschnitt`, `erkennungsweite_m`,
`regelwerk_snapshot`) — er parst nie YAML. Alle Werte kommen aus
`data/en1838_grundwerte.yaml` (Norm-Grundwerte) + `data/raumtyp_regeln.yaml`
(Raumtyp → Anforderung); dieses Modul hardcodet nichts.

Seit Contract v1.1.0 liefert der Provider zusaetzlich `gleichmaessigkeit_max`
(Ud, §4.2.2/§4.3.2) und `umschaltzeit_max_s` (§4.2.6/§4.3.6/§5.4.6). Die beiden
uebrigen v1.1.0-Felder — `NormRegelwerk.flaechen_schwellen` und
`arbeitsplatz_lux` — bleiben bewusst leer: fuer sie liegt kein EN-1838-Beleg vor
(Begruendung in `data/en1838_grundwerte.yaml` + `docs/NORMQUELLEN_AT.md` 2b).

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

from .sonderstellen import SonderstellenAnforderung, SonderstellenKatalog

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
        # §4.1.2-Stellen + die zwei Raum-Attribute (§4.3.8/§4.4.1). Eigener
        # Katalog, weil diese Anforderungen nicht an einem Raumtyp haengen.
        self._sonderstellen = SonderstellenKatalog(self._dir)

    def _read(self, name: str) -> dict:
        with open(self._dir / name, encoding="utf-8") as fh:
            return yaml.safe_load(fh)

    # ── Wert-Auflösung (refs → Grundwerte) ──────────────────────────────────
    def _lux(self, ref: str) -> float:
        return float(self._grund["lux"][ref])

    def _quelle(self, ref: str) -> str:
        return str(self._grund["quellen"][ref])

    def _gleichmaessigkeit(self, regel: dict) -> float | None:
        """Ud als max:min (§4.2.2 Rettungsweg / §4.3.2 Antipanik — beide 1:40).

        Kein `gleichmaessigkeit_ref` = die Norm gibt fuer diese Anforderung nichts
        her (z.B. Aufheller nach §4.1) -> `None`. Der Konsument faellt dann auf
        seinen eigenen Default zurueck; es entsteht kein stiller Norm-Default.
        """
        ref = regel.get("gleichmaessigkeit_ref")
        return float(self._grund["gleichmaessigkeit"][ref]) if ref else None

    def _umschaltzeit(self) -> float | None:
        """Umschaltzeit bis zum VOLLwert (§4.2.6/§4.3.6/§5.4.6: 100 % in 60 s).

        Global wie `dauer_min` — die Norm nennt fuer Rettungsweg, Antipanik und
        Sicherheitszeichen denselben Wortlaut. Die zweite Stufe (50 % in 5 s)
        steht in der YAML als `halbwert_s`, hat aber kein Contract-Feld.
        """
        wert = (self._grund.get("umschaltzeit") or {}).get("vollwert_s")
        return float(wert) if wert is not None else None

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
            gleichmaessigkeit_max=self._gleichmaessigkeit(regel),
            umschaltzeit_max_s=self._umschaltzeit(),
            quelle=self._quelle(regel["quelle_ref"]),
        )

    def _montagehoehe(self, regel: dict) -> int:
        """Fachpraxis-Montagehöhe, nie unter dem Norm-Floor §4.1.1 (2000 mm)."""
        floor = int(self._grund["montagehoehe_min_mm"])
        return max(int(regel.get("montagehoehe_mm", floor)), floor)

    def _default_erkennungsweite_m(self) -> float:
        e = self._grund["erkennungsweite"]
        return round(e["z_hinterleuchtet"] * e["piktogramm_hoehe_default_m"], 3)

    # ── Sonderstellen (EN 1838 §4.1.2) + Raum-Attribute (§4.3.8/§4.4.1) ─────
    # NOCH NICHT im Ports-Protocol — Vorschlag liegt bei den 3 Ownern
    # (docs/SPEC_SONDERSTELLEN_CONTRACT.md §8). Bis dahin duck-typed abfragbar.
    def fuer_sonderstelle(self, typ: str) -> list[SonderstellenAnforderung]:
        """Anforderung(en) für eine punktförmige Stelle nach §4.1.2.

        Liste, weil `niveauaenderung` nach §4.1.2 c) zwei Leuchten auslöst
        (Sicherheitsleuchte SL-04 + Rettungszeichen RZ-06). Jede Anforderung
        trägt die **eigene** Fundstelle — nicht die einer fremden Raumregel.
        """
        if self._sonderstellen.ist_raum_attribut(typ):
            raise KeyError(f"{typ!r} ist ein Raum-Attribut → fuer_raum_attribut()")
        return self._baue(typ)

    def fuer_raum_attribut(self, attribut: str) -> list[SonderstellenAnforderung]:
        """Anforderung für `ist_barrierefrei` (§4.3.8) bzw. `besondere_gefaehrdung`
        (§4.4.1) — Eigenschaften eines Raums, nicht eines Punktes."""
        if not self._sonderstellen.ist_raum_attribut(attribut):
            raise KeyError(f"{attribut!r} ist kein Raum-Attribut → fuer_sonderstelle()")
        return self._baue(attribut)

    def _baue(self, ausloeser: str) -> list[SonderstellenAnforderung]:
        kat = self._sonderstellen
        ist_attribut = kat.ist_raum_attribut(ausloeser)
        raus: list[SonderstellenAnforderung] = []
        for block in kat.norm_anforderung_roh(ausloeser):
            regel = self._index[(
                block["symbol_wie"]["raum_typ"],
                bool(block["symbol_wie"]["ist_fluchtweg"]),
            )]
            lux_v = None if ist_attribut else kat.norm_lux_vertikal(ausloeser)
            lux_h_ref = block.get("lux_horizontal_wie")
            offen, grund = self._nachweis_status(ausloeser, ist_attribut, lux_v, block)
            raus.append(SonderstellenAnforderung(
                ausloeser=ausloeser,
                klassifikation=block["klassifikation"],
                quelle=block["quelle"],
                norm_ref=kat.norm_ref(ausloeser),
                beleg=kat.beleg_von(ausloeser),
                symbol_katalog_keys=list(regel.get("symbol_katalog_keys", [])),
                montagehoehe_mm=self._montagehoehe(regel),
                max_abstand_mm=None if ist_attribut else kat.max_abstand_mm(ausloeser),
                lux_vertikal=lux_v,
                lux_vertikal_quelle=(
                    kat.eintrag(ausloeser)["lux_anforderung"].get("norm_quelle")
                    if lux_v is not None else None
                ),
                lux_horizontal=self._lux(lux_h_ref) if lux_h_ref else None,
                lux_horizontal_quelle=self._quelle(lux_h_ref) if lux_h_ref else None,
                nachweis_offen=offen,
                nachweis_offen_grund=grund,
            ))
        return raus

    def _nachweis_status(
        self, ausloeser: str, ist_attribut: bool, lux_v: float | None, block: dict
    ) -> tuple[bool, str]:
        """Ist die lichttechnische Anforderung heute nachweisbar — und wenn nicht, warum?

        Ehrlichkeits-Regel: eine gelieferte Quelle ersetzt keinen Nachweis. Wer
        die Anforderung konsumiert, muss ein offenes `nachweis_offen` sichtbar
        machen (Prüfbericht), sonst sieht ein unvollständiger Plan „ok" aus.
        """
        if ist_attribut:
            grund = block.get("nachweis_offen_grund") or ""
            return bool(grund), grund.strip()
        if lux_v is not None:
            return True, (
                f"§4.1.2 fordert {lux_v:g} lx VERTIKAL am Gerät; der Lux-Nachweis "
                "der Engine rechnet horizontal am Boden — der vertikale Nachweis "
                "wird heute nicht erbracht."
            )
        if self._sonderstellen.lux_ist_ungeklaert(ausloeser):
            return True, (
                "§4.1.2 c) nennt für diese Stelle kein Beleuchtungsniveau — die "
                "Hervorhebungspflicht gilt, das Niveau bleibt zu prüfen."
            )
        return False, ""

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
        # Die §4.1.2-/§4.3.8-/§4.4.1-Fundstellen kommen dazu, sobald der Provider
        # sie vergeben kann — sonst bricht die Naht-Invariante
        # `Platzierung.norm_quelle ∈ quellen` an der ersten Sonderstelle. Rein
        # additiv: die Menge wird groesser, kein bestehender String faellt weg.
        quellen = sorted(
            {r.anforderung.quelle for r in regeln} | set(self._sonderstellen.quellen())
        )
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
