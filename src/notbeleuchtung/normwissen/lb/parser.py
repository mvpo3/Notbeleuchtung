"""LbParser — Leistungsbeschreibung (2. Input) → LBVorgabe.

Erfüllt `hauptengine.contracts.ports.LBProvider` (`parse_lb(lb_path) -> LBVorgabe`).
Deterministisch, regelbasiert, quellengebunden — **kein NLP**. Alle Fachwörter,
Muster und Einheiten stehen in `data/lb_extraktion.yaml`.

**Fail closed.** Der Parser gibt lieber sichtbar auf, als eine erkannte
projektspezifische Anforderung still zu verlieren:

* `parse_lb()` liefert eine `LBVorgabe` **nur**, wenn kein blockierender Befund
  vorliegt — sonst `LbReviewRequired` (mit vollständigem Bericht) bzw.
  `LbNichtLesbar`.
* `parse_bericht()` liefert immer den vollen Audit-Trail inkl. Kandidatenwerten,
  auch für die blockierten Fälle.

Blockierend sind: Dokument nicht lesbar · kein Notbeleuchtungs-Abschnitt · reiner
Verweis auf ein fremdes Dokument · ein erkannter Raumtyp, den die Raumerkennung
heute nicht erzeugt (die Regel wäre im Platzierer ein stiller No-op) · derselbe
Raumtyp gleichzeitig ein- und ausgeschlossen.

Was NICHT blockiert: ein Feld, das im Notbeleuchtungs-Abschnitt schlicht nicht
vorkommt. Das ist `nicht_spezifiziert` → `None` → der Norm-Default greift, genau
wie es die Hierarchie `LB-explizit → Norm` vorsieht.
"""
from __future__ import annotations

from pathlib import Path

import yaml

from notbeleuchtung.hauptengine.contracts import BereichsRegel, LBVorgabe, SonderLux

from . import felder, struktur, text
from .bericht import LbBericht, LbReviewRequired

DATA_DIR = Path(__file__).parent.parent / "data"
DATEI = "lb_extraktion.yaml"


class LbParser:
    """LBProvider-Impl gegen data/lb_extraktion.yaml."""

    def __init__(self, data_dir: Path | None = None) -> None:
        self._dir = data_dir or DATA_DIR
        with open(self._dir / DATEI, encoding="utf-8") as fh:
            self._cfg = yaml.safe_load(fh)

    # ── LBProvider-Protocol ─────────────────────────────────────────────────
    def parse_lb(self, lb_path: str) -> LBVorgabe:
        """LB-Datei → LBVorgabe. Wirft bei jedem blockierenden Zweifel."""
        vorgabe, bericht = self._parse(lb_path)
        if bericht.blockierende:
            raise LbReviewRequired(bericht)
        return vorgabe

    # ── Audit ───────────────────────────────────────────────────────────────
    def parse_bericht(self, lb_path: str) -> LbBericht:
        """Vollständiger Befund inkl. Kandidatenwerten — auch wenn blockiert."""
        return self._parse(lb_path)[1]

    # ── Kern ────────────────────────────────────────────────────────────────
    def _parse(self, lb_path: str) -> tuple[LBVorgabe, LbBericht]:
        cfg = self._cfg
        name = Path(lb_path).name
        bericht = LbBericht(datei=name)

        seiten = text.lade_seiten(lb_path)      # wirft LbNichtLesbar
        abschnitte = struktur.baue_abschnitte(seiten, cfg["struktur"])
        volltext = "\n".join(s.text for s in seiten)
        bericht.dokument_art = struktur.klassifiziere(volltext, cfg["dokument_arten"])

        relevante = struktur.sl_abschnitte(
            abschnitte, cfg["sl_abschnitt_anker"], cfg["sl_abschnitt_ausschluss"]
        )

        # Unaufgelöste Verweise auf fremde Dokumente: ohne sie fehlen die Vorgaben.
        # Nur dort prüfen, wo die Vorgaben stehen müssten — ein Verweis in einem
        # fachfremden Abschnitt (z.B. Fabrikate der Allgemeinbeleuchtung) blockiert
        # die Notbeleuchtung nicht.
        for a, anker in struktur.offene_verweise(relevante or abschnitte, cfg["verweis_muster"]):
            bericht.add(
                feld="verweis", status="review_blockierend", abschnitt=a.fundstelle,
                seite=a.seite, anker=anker,
                begruendung="Verweist auf ein Dokument, das hier nicht vorliegt — die "
                            "Vorgaben stehen dort, nicht in dieser Datei.",
            )

        if not relevante:
            bericht.add(
                feld="notbeleuchtungs_abschnitt", status="review_blockierend",
                begruendung=f"Kein Abschnitt zur Notbeleuchtung gefunden (Dokument erkannt "
                            f"als '{bericht.dokument_art}'). Eine leere LBVorgabe wäre hier "
                            "nicht von 'die LB macht keine Vorgaben' unterscheidbar.",
            )
            return LBVorgabe(lb_quelle=name), bericht

        vorgabe = LBVorgabe(
            lb_quelle=self._quelle(name, relevante),
            **self._skalare(relevante, bericht),
            **self._enums(relevante, bericht, alle=abschnitte),
            **self._listen(relevante, bericht),
            **self._bereiche(relevante, bericht),
        )
        self._funktionserhalt(relevante, bericht)
        return vorgabe, bericht

    # ── Feldgruppen ─────────────────────────────────────────────────────────
    def _skalare(self, relevante, bericht: LbBericht) -> dict:
        werte: dict = {}
        for feld, cfg in self._cfg["felder"].items():
            treffer = felder.zahl_feld(relevante, cfg)
            if treffer is None:
                werte[feld] = None
                bericht.add(
                    feld=feld, status="nicht_spezifiziert",
                    begruendung=f"{cfg['bezeichnung']} steht nicht in der LB → Norm-Default "
                                "greift. Ein bloßer Normverweis erzeugt bewusst KEINEN Wert.",
                )
                continue
            wert = treffer.wert
            werte[feld] = int(wert) if feld.endswith("_min") else float(wert)
            bericht.add(
                feld=feld, status="wert", kandidat=str(werte[feld]),
                abschnitt=treffer.abschnitt.fundstelle, seite=treffer.abschnitt.seite,
                anker=treffer.anker, begruendung=f"{cfg['bezeichnung']} explizit in der LB.",
            )
        return werte

    def _enums(self, relevante, bericht: LbBericht, alle: list) -> dict:
        werte: dict = {}
        for feld, cfg in self._cfg["enums"].items():
            quelle = alle if cfg.get("dokumentweit") else relevante
            treffer = felder.enum_feld(quelle, cfg)
            if len(treffer) > 1 and cfg.get("prioritaet"):
                # Kein Widerspruch, sondern gestaffelte Aussagen: der erste Wert in
                # Deklarationsreihenfolge ist der speziellere.
                reihenfolge = list(cfg["werte"])
                treffer = [min(treffer, key=lambda t: reihenfolge.index(t.wert))]

            if not treffer:
                werte[feld] = None
                bericht.add(feld=feld, status="nicht_spezifiziert",
                            begruendung=f"{cfg['bezeichnung']} nicht in der LB genannt.")
            elif len(treffer) == 1:
                werte[feld] = treffer[0].wert
                bericht.add(
                    feld=feld, status="wert", kandidat=str(treffer[0].wert),
                    abschnitt=treffer[0].abschnitt.fundstelle,
                    seite=treffer[0].abschnitt.seite, anker=treffer[0].anker,
                    begruendung=f"{cfg['bezeichnung']} explizit in der LB.",
                )
            else:
                # Widerspruch im selben Dokument — jede Auflösung wäre geraten.
                werte[feld] = None
                kandidaten = ", ".join(
                    f"{t.wert} ({t.abschnitt.fundstelle}, S. {t.abschnitt.seite})"
                    for t in treffer
                )
                bericht.add(
                    feld=feld, status="review_informativ",
                    kandidat=kandidaten, anker=treffer[0].anker,
                    abschnitt=treffer[0].abschnitt.fundstelle, seite=treffer[0].abschnitt.seite,
                    begruendung=f"Widerspruch in der LB: {cfg['bezeichnung']} ist mehrfach "
                                "und unterschiedlich angegeben. Kein Wert gesetzt — jede "
                                "Auflösung wäre geraten.",
                )
        return werte

    def _listen(self, relevante, bericht: LbBericht) -> dict:
        cfg = self._cfg
        werte: dict = {}

        rz = felder.stellen(relevante, cfg["rz_stellen"])
        werte["rz_stellen"] = [t.wert for t in rz]
        for t in rz:
            bericht.add(feld="rz_stellen", status="wert", kandidat=str(t.wert),
                        abschnitt=t.abschnitt.fundstelle, seite=t.abschnitt.seite,
                        anker=t.anker, begruendung="Rettungszeichen-Stelle in der LB genannt.")
        if not rz:
            bericht.add(feld="rz_stellen", status="nicht_spezifiziert",
                        begruendung="Keine Platzierungsregel für Rettungszeichen in der LB.")

        lux = felder.sonder_lux(relevante, cfg["sonder_lux"])
        werte["sonder_lux"] = [SonderLux(ort=t.wert[0], min_lux=t.wert[1]) for t in lux]
        for t in lux:
            bericht.add(feld="sonder_lux", status="wert", kandidat=f"{t.wert[0]}={t.wert[1]}",
                        abschnitt=t.abschnitt.fundstelle, seite=t.abschnitt.seite,
                        anker=t.anker, begruendung="Erhöhte Mindest-Lux an einem Ort.")
        if not lux:
            bericht.add(feld="sonder_lux", status="nicht_spezifiziert",
                        begruendung="Keine erhöhte Mindest-Beleuchtungsstärke in der LB.")

        pikto = felder.erstes_muster(relevante, cfg["piktogramm_muster"])
        werte["piktogramm_norm"] = pikto.wert if pikto else None
        bericht.add(
            feld="piktogramm_norm",
            status="wert" if pikto else "nicht_spezifiziert",
            kandidat=str(pikto.wert) if pikto else None,
            abschnitt=pikto.abschnitt.fundstelle if pikto else None,
            seite=pikto.abschnitt.seite if pikto else None,
            anker=pikto.anker if pikto else None,
            begruendung="Piktogramm-Norm explizit genannt." if pikto
            else "Keine Piktogramm-Norm in der LB genannt.",
        )

        normen = felder.norm_bezug(relevante, cfg["norm_bezug"])
        werte["norm_bezug"] = [t.wert for t in normen]
        for t in normen:
            bericht.add(
                feld="norm_bezug", status="wert", kandidat=str(t.wert),
                abschnitt=t.abschnitt.fundstelle, seite=t.abschnitt.seite, anker=t.anker,
                begruendung="Zitiertes Regelwerk — reine Nennung, daraus wird KEIN Wert "
                            "abgeleitet (sonst würde ein Norm-Default als LB-Vorgabe gelten).",
            )
        return werte

    def _bereiche(self, relevante, bericht: LbBericht) -> dict:
        cfg = self._cfg
        unterstuetzt = set(cfg["unterstuetzte_raum_typen"])
        treffer = felder.bereiche(relevante, cfg)

        inkl: list[BereichsRegel] = []
        exkl: list[BereichsRegel] = []
        gesehen: dict[str, bool] = {}

        for t in treffer:
            # Contract-Validator verbietet denselben Raumtyp in beiden Listen.
            if t.raum_typ in gesehen and gesehen[t.raum_typ] != t.sicherheitsbeleuchtung:
                bericht.add(
                    feld="bereiche", status="review_blockierend", kandidat=t.raum_typ,
                    abschnitt=t.abschnitt.fundstelle, seite=t.abschnitt.seite, anker=t.anker,
                    begruendung=f"'{t.raum_typ}' ist in der LB gleichzeitig ein- und "
                                "ausgeschlossen — Widerspruch, nicht auflösbar.",
                )
                continue
            gesehen[t.raum_typ] = t.sicherheitsbeleuchtung

            if t.raum_typ not in unterstuetzt:
                # Erkannt, aber im Platzierer wirkungslos: die Raumerkennung
                # erzeugt diesen raum_typ nicht → die Regel fände nie einen Raum.
                bericht.add(
                    feld="bereiche", status="review_blockierend", kandidat=(
                        f"{'inklusion' if t.sicherheitsbeleuchtung else 'exklusion'}: "
                        f"{t.raum_typ}"
                    ),
                    abschnitt=t.abschnitt.fundstelle, seite=t.abschnitt.seite, anker=t.anker,
                    begruendung=f"LB verlangt eine Regel für '{t.raum_typ}', aber die "
                                "Raumerkennung erzeugt diesen raum_typ nicht "
                                "(raumerkennung/raumtyp.py) — im Platzierer wäre die Regel "
                                "ein stiller No-op. Die Anforderung darf nicht verloren gehen.",
                )
                continue

            regel = BereichsRegel(raum_typ=t.raum_typ,
                                  sicherheitsbeleuchtung=t.sicherheitsbeleuchtung,
                                  begruendung=t.begruendung)
            (inkl if t.sicherheitsbeleuchtung else exkl).append(regel)
            bericht.add(
                feld="bereiche", status="wert",
                kandidat=f"{'inklusion' if t.sicherheitsbeleuchtung else 'exklusion'}: "
                         f"{t.raum_typ}",
                abschnitt=t.abschnitt.fundstelle, seite=t.abschnitt.seite, anker=t.anker,
                begruendung="Explizite LB-Vorgabe" + (f" ({t.begruendung})" if t.begruendung else ""),
            )

        if not treffer:
            bericht.add(feld="bereiche", status="nicht_spezifiziert",
                        begruendung="Keine bereichsbezogene LB-Vorgabe gefunden.")
        return {"bereiche_inklusion": inkl, "bereiche_exklusion": exkl}

    def _funktionserhalt(self, relevante, bericht: LbBericht) -> None:
        """Kein Contract-Feld — der Befund wird nur dokumentiert."""
        t = felder.erstes_muster(relevante, self._cfg["funktionserhalt_muster"])
        if t:
            bericht.add(
                feld="funktionserhalt", status="review_informativ", kandidat=str(t.wert),
                abschnitt=t.abschnitt.fundstelle, seite=t.abschnitt.seite, anker=t.anker,
                begruendung="Funktionserhalt in der LB gefordert. `LBVorgabe` hat dafür kein "
                            "Feld — bewusst nicht erfunden, nur dokumentiert.",
            )

    @staticmethod
    def _quelle(name: str, relevante: list[struktur.Abschnitt]) -> str:
        """Audit-Trail: Datei + die tragenden Abschnitte + Seiten."""
        teile = [f"§{a.nummer} (S. {a.seite})" for a in relevante]
        return f"{name} {', '.join(teile)}" if teile else name
