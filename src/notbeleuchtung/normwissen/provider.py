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

from .sonderstellen import (
    LuxAnforderung,
    SonderstellenAnforderung,
    SonderstellenKatalog,
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

    # ── PROTOTYP: Sonderstellen (§4.1.2) + Raum-Attribute (§4.3.8/§4.4.1) ───
    #
    # ⚠️ Diese vier Methoden sind ein **lokal vorbereiteter Prototyp**, KEINE
    # vereinbarte Schnittstelle. Sie stehen nicht im `ports.NormProvider`-
    # Protocol; `SonderstellenAnforderung` ist ein normwissen-eigener Typ und
    # damit für `platzierung` nicht importierbar (Owner-Grenze, CLAUDE.md).
    # Ein `getattr`-Zugriff aus einem fremden Paket wäre eine stille Kopplung an
    # eine ungeprüfte Signatur und ersetzt keine Vereinbarung — der konkrete
    # 3-Owner-Vorschlag (Rückgabetyp + Methodensignatur + Auswirkungen) steht in
    # docs/SPEC_SONDERSTELLEN_CONTRACT.md §8. Bis zum GO nur intern + in Tests
    # verwenden.
    def fuer_sonderstelle(self, typ: str) -> list[SonderstellenAnforderung]:
        """PROTOTYP — norm-belegte Anforderung(en) für eine Stelle nach §4.1.2.

        Liefert ausschließlich Norm-Defaults. §4.1.2 verlangt an einer
        hervorzuhebenden Stelle eine **Sicherheitsleuchte** (Einleitung des
        Abschnitts) — nicht mehrere Leuchtenarten. Was in der Praxis zusätzlich
        gesetzt wird, kommt über `zur_pruefung()` und trägt keine Norm-Quelle.
        """
        if self._sonderstellen.ist_raum_attribut(typ):
            raise KeyError(f"{typ!r} ist ein Raum-Attribut → fuer_raum_attribut()")
        return self._baue(typ, self._sonderstellen.norm_anforderung_roh(typ))

    def zur_pruefung(self, typ: str) -> list[SonderstellenAnforderung]:
        """PROTOTYP — Kandidaten OHNE Norm-Beleg (`ist_norm_default=False`).

        Heute genau einer: das zusätzliche Rettungszeichen an einer
        Niveauänderung. §4.1.2 c) belegt dort die Sicherheitsleuchte; ein
        Rettungszeichen fordert die Norm an dieser Stelle nicht (d) verlangt nur,
        dass **vorhandene** Sicherheitszeichen beleuchtet sind). Ohne eigene
        Entscheidungs-Quelle — in der Praxis die LB — entsteht daraus **keine**
        RZ-Pflicht. Die Kandidaten tragen deshalb `quelle=None`.
        """
        if self._sonderstellen.ist_raum_attribut(typ):
            raise KeyError(f"{typ!r} ist ein Raum-Attribut → fuer_raum_attribut()")
        return self._baue(typ, self._sonderstellen.zur_pruefung_roh(typ))

    def fuer_raum_attribut(
        self, attribut: str, raum_typ: str | None = None
    ) -> list[SonderstellenAnforderung]:
        """PROTOTYP — Anforderung für `ist_barrierefrei` (§4.3.8) bzw.
        `besondere_gefaehrdung` (§4.4.1).

        `raum_typ` ist Teil des Auslösers, nicht Beiwerk: §4.3.8 fordert
        Antipanikbeleuchtung „in Toiletten für Menschen mit Behinderung" — das
        Flag `ist_barrierefrei` allein genügt nicht. Ein barrierefreies ZIMMER
        löst §4.3.8 nicht aus und bekommt hier eine leere Liste.

        **Leere Liste heißt nicht „kein Licht":** andere Anforderungen (Raumtyp-
        Regel, Fluchtweg, Flächen-Trigger) gelten unabhängig weiter — sie kommen
        über `fuer_raum()` bzw. den Fluchtweg-Pfad.

        Fail closed: ist der Raumtyp für die Entscheidung nötig und fehlt er,
        gibt es keinen Default, sondern einen Fehler.
        """
        kat = self._sonderstellen
        if not kat.ist_raum_attribut(attribut):
            raise KeyError(f"{attribut!r} ist kein Raum-Attribut → fuer_sonderstelle()")
        if kat.braucht_raumtyp(attribut) and raum_typ is None:
            raise ValueError(
                f"{attribut!r} ist raumtyp-gebunden ({', '.join(kat.gilt_nur_fuer_raumtypen(attribut))}) "
                "— ohne raum_typ ist die Anforderung nicht entscheidbar"
            )
        if raum_typ is not None and not kat.gilt_fuer_raum(attribut, raum_typ):
            return []
        return self._baue(attribut, kat.norm_anforderung_roh(attribut))

    def _baue(self, ausloeser: str, bloecke: list[dict]) -> list[SonderstellenAnforderung]:
        kat = self._sonderstellen
        ist_attribut = kat.ist_raum_attribut(ausloeser)
        raus: list[SonderstellenAnforderung] = []
        for block in bloecke:
            regel = self._index[(
                block["symbol_wie"]["raum_typ"],
                bool(block["symbol_wie"]["ist_fluchtweg"]),
            )]
            ist_norm = bool(block.get("quelle"))
            lux = self._lux_anforderung(ausloeser, ist_attribut, block)
            offen, grund = self._nachweis_status(ausloeser, lux, block, ist_norm)
            raus.append(SonderstellenAnforderung(
                ausloeser=ausloeser,
                klassifikation=block["klassifikation"],
                quelle=block.get("quelle"),
                norm_ref=kat.norm_ref(ausloeser),
                beleg=kat.beleg_von(ausloeser),
                symbol_katalog_keys=list(regel.get("symbol_katalog_keys", [])),
                montagehoehe_mm=self._montagehoehe(regel),
                max_abstand_mm=None if ist_attribut else kat.max_abstand_mm(ausloeser),
                lux=lux,
                ist_norm_default=ist_norm,
                decision_source=block.get("decision_source", "norm_default"),
                begruendung=(block.get("begruendung") or "").strip(),
                gilt_nur_fuer_raumtypen=kat.gilt_nur_fuer_raumtypen(ausloeser),
                nachweis_offen=offen,
                nachweis_offen_grund=grund,
            ))
        return raus

    def _lux_anforderung(
        self, ausloeser: str, ist_attribut: bool, block: dict
    ) -> LuxAnforderung | None:
        """Der Lux-Wert MIT Bezugsfläche — oder None, wo die Norm keinen nennt."""
        flaeche = block.get("lux_bezugsflaeche")
        if flaeche is None:
            return None
        if flaeche == "arbeitsflaeche":
            # §4.4.1: 10 % des Aufgaben-Wartungswertes, mindestens 15 lx. Der
            # Prozentsatz ist ohne die Aufgabenbeleuchtung nicht auswertbar →
            # `wert` bleibt None, die belegten Teilgrößen stehen daneben.
            return LuxAnforderung(
                wert=None,
                bezugsflaeche="arbeitsflaeche",
                quelle=block["quelle"],
                mindestwert=block.get("lux_mindestwert"),
                anteil_nennbeleuchtung=block.get("lux_anteil_nennbeleuchtung"),
                vollstaendig_bestimmbar=False,
                offen_grund=(block.get("nachweis_offen_grund") or "").strip(),
            )
        if flaeche == "horizontal_boden":
            ref = block["lux_wie"]
            return LuxAnforderung(
                wert=self._lux(ref),
                bezugsflaeche="horizontal_boden",
                quelle=self._quelle(ref),
            )
        # vertikal_am_geraet — §4.1.2 h)/i), Wert am Gerät, nie am Boden.
        wert = None if ist_attribut else self._sonderstellen.norm_lux_vertikal(ausloeser)
        if wert is None:
            return None
        lux_cfg = self._sonderstellen.eintrag(ausloeser)["lux_anforderung"]
        return LuxAnforderung(
            wert=wert,
            bezugsflaeche="vertikal_am_geraet",
            quelle=lux_cfg.get("norm_quelle") or block["quelle"],
            vollstaendig_bestimmbar=False,
            offen_grund=(
                "Vertikaler Wert am Gerät; der Lux-Nachweis der Engine "
                "(lux_raster) rechnet horizontal am Boden."
            ),
        )

    def _nachweis_status(
        self, ausloeser: str, lux: LuxAnforderung | None, block: dict, ist_norm: bool
    ) -> tuple[bool, str]:
        """Ist die Anforderung heute vollständig nachweisbar — und wenn nicht, warum?

        Ehrlichkeits-Regel: eine gelieferte Quelle ersetzt keinen Nachweis. Wer
        die Anforderung konsumiert, muss ein offenes `nachweis_offen` sichtbar
        machen (Prüfbericht), sonst sieht ein unvollständiger Plan „ok" aus.
        """
        if not ist_norm:
            return True, (
                "Kein EN-1838-Beleg für diese Leuchte — sie braucht eine eigene "
                "Entscheidungs-Quelle (LB/Praxis), sonst wird sie nicht gesetzt."
            )
        if lux is not None and not lux.vollstaendig_bestimmbar:
            return True, lux.offen_grund
        if lux is None and not self._sonderstellen.ist_raum_attribut(ausloeser) \
                and self._sonderstellen.lux_ist_ungeklaert(ausloeser):
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
