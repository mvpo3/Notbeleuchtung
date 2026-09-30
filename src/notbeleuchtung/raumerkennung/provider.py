"""ArchitekturRaumProvider — echter RaumProvider (Selman).

Übersetzt einen leeren Architekturplan (DXF) in das ``RaumModell``-Contract:
Räume/Türen/Ausgänge/Fluchtweg-Zirkulation. Reine Geometrie/Topologie, kein
Norm-Urteil (das machen Enis/Leonis).

Baut inkrementell auf schlanken Modulen dieses Packages auf und verwendet die
sauberen, self-contained Port-Helfer (``._port.parsers.room_faces``,
``._port.models.room``) wieder. Ersetzt schrittweise den ``FakeRaumProvider``.
"""
from __future__ import annotations

import copy

from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

from notbeleuchtung.hauptengine.contracts import RaumModell
from notbeleuchtung.hauptengine.contracts.raum_modell import Tuer

from .ausgaenge import leite_ausgaenge, ohne_unzulaessige_final_exits
from .aussenbereich import erkenne_aussenbereiche, waehle_innen_zonen
from .dxf_load import bounds_mm, lade_dxf
from .fluchtweg import explizite_linien, fluchtwege, linien_segmente
from .footprint import hauptausgaenge
from .gang_anker import anker_fuer_gang
from .geometrie_typ import typisiere_geometrisch
from .geschoss import geschoss_befund
from .kaskade import KaskadeErgebnis, raeume_aus_kaskade
from .kreuzcheck import kreuzcheck
from .lift_erkennung import finde_lifte, liftschacht_reste
from .raumtyp import beschrifte_raeume
from .sanitaer import kandidaten as sanitaer_kandidaten
from .sanitaer import sanitaerobjekte, typisiere_sanitaer
from .stiegenhaus import baue_stiegenhaus_modell
from .tuer_typisierung import brandschutz_hinweise_aus_dxf, typisiere_tueren
from .tuer_zuordnung import (
    AUSSEN,
    aussen_durchgaenge,
    durchgaenge_ohne_tuerblatt,
    ordne_tueren,
)
from .tueren import (
    aussentor_tueren,
    im_planbereich,
    text_tueren,
    tuer_texte,
    tueren_aus_dxf,
    verschmelze_doppelfluegel,
)
from .waende import raeume_aus_waenden, wand_segmente
from .wandkoerper import aussenkontur, bounds_aus_wandkoerpern, wand_union
from .wohnungen import bilde_wohnungen
from .wohnungsklasse import anker_aus_privat_ziehen, bestaetigt_privat
from .zirkulation import zirkulation_aus_dxf


def _tueren_und_wohnungen(plan, k: KaskadeErgebnis, raeume: list, tueren: list[Tuer],
                          kontur, wu, aussen, geschoss: str, flw_enden: list
                          ) -> tuple[list[Tuer], list[str], list[str], list[str]]:
    """Türzuordnung → Liftschacht-Reste → Durchgänge → rohe Türrollen →
    Wohnungen, in place auf ``raeume``/``tueren``. Liefert ``(tueren,
    tuer_warnungen, schacht_reste, wohnungsklasse_warnungen)``. Läuft einmal
    regulär und — nur mit K3-Kandidaten — vorher einmal als Probe auf Kopien."""
    fehlende_seiten: list = []
    ordne_tueren(tueren, k.tueroeffnungen, raeume, kontur, wu, fehlende_seiten)
    # Eine Tür braucht mindestens einen Innenraum: beidseits AUSSEN ist
    # keine Tür des Gebäudes (Fassaden-Bögen, Rest-Phantome).
    tueren = [t for t in tueren if not (t.von_raum == t.nach_raum == AUSSEN)]
    for i, t in enumerate(tueren, start=1):   # lückenlose IDs nach dem Filtern
        t.id = f"tuer_{i}"
    # Seiten, die bis 500 mm weder Raum noch AUSSEN fanden — Prüfstrecken-
    # Ausgabe wie `ausgangs_warnungen`, kein Contract-Feld (`Tuer` kennt
    # kein `seite_fehlt`). Erst NACH der Neunummerierung formatiert, sonst
    # nennt der Text eine Tür-ID, die inzwischen einer anderen Tür gehört.
    tuer_warnungen = [
        f"seite_fehlt: {t.id} Seite {zeichen} bis {stufe:.0f} mm kein Raum "
        "und kein AUSSEN (nur Wandkörper oder gedeckte Freifläche)"
        for t, zeichen, stufe in fehlende_seiten]
    # S5c, Owner-Entscheid F1 (K1_T): eine Stiegenhausfläche, die zu mehr
    # als der Hälfte Liftkabine ist, ist Liftschacht — VOR den Durchgängen
    # und der Türtypisierung, damit der S5a-Guard an ihr keine blattlose
    # Öffnung bildet (Liftkern-Phantom VA-5, Lifttür-Ausgänge). Erst nach
    # der Außenanalyse: die liest die Raumtypen für die Innen-Zonen.
    schacht_reste = liftschacht_reste(plan, raeume)
    if k.wandkoerper:
        tueren = tueren + durchgaenge_ohne_tuerblatt(raeume, tueren, wu,
                                                     k.tueroeffnungen)
        tueren = tueren + aussen_durchgaenge(raeume, tueren, wu, kontur)
    typisiere_tueren(tueren, raeume, geschoss,
                     brandschutz_hinweise_aus_dxf(plan), flw_enden,
                     tuer_texte(plan),
                     unary_union(aussen.geschlossen)
                     if aussen is not None and aussen.geschlossen else None)
    # Unbestimmt gebliebene Räume (§ 6g Schritt 3) und die Durchleitung
    # privater Räume sind Prüfstrecken-Ausgabe wie `tuer_warnungen` —
    # der Contract führt sie nicht (Board-Antrag: Segment-Feld
    # `durchleitung`, docs/GATE_TUERSTAPEL.md § 6g).
    wohnungsklasse_warnungen: list[str] = []
    bilde_wohnungen(raeume, tueren, wohnungsklasse_warnungen)
    return tueren, tuer_warnungen, schacht_reste, wohnungsklasse_warnungen


class ArchitekturRaumProvider:
    """Erfüllt das ``RaumProvider``-Protocol (``parse(dxf_path, floor)``).

    Verdrahtet die Slice-Module zu einem ``RaumModell``. Räume/Türen/Fluchtweg
    aus echter DXF-Geometrie; Norm-Urteile bleiben Enis/Leonis.

    Räume kommen aus der Kaskade L→H→F→R (``kaskade.raeume_aus_kaskade``) —
    derselben Orchestrierung wie in der Prüfstrecke ``scripts/plan_pruefen.py``.
    """

    def parse(self, dxf_path: str, floor: str) -> RaumModell:
        plan = lade_dxf(dxf_path)
        # Greift kein Wand-Layer-Muster (Muthgasse-Familie), bleibt die Kaskade aus:
        # ihr Raster wäre auf einem unerschlossenen Plan nur teuer, und `bounds_mm`
        # bricht gleich darauf definiert ab (kein stilles Leer-Ergebnis).
        hat_wand_entities = next(plan.wall_entities(), None) is not None
        k = raeume_aus_kaskade(plan) if hat_wand_entities else KaskadeErgebnis()
        try:
            bounds = bounds_mm(plan)
        except ValueError:
            # Hatch-only-Pläne haben keine Wand-Linien, aber Wandkörper.
            if not k.wandkoerper:
                raise
            bounds = bounds_aus_wandkoerpern(k.wandkoerper)
        raeume = k.alle_raeume
        if not raeume:
            raeume = beschrifte_raeume(plan, raeume_aus_waenden(plan))
        # Geometrische Typ-Ableitung (STIEGENHAUS aus Treppen-Blöcken) — greift auch
        # auf Plänen ohne Text-Labels (z.B. Mollgasse), ergänzt Text/Layer-Typisierung.
        raeume = typisiere_geometrisch(plan, raeume)
        tueren = tueren_aus_dxf(plan)
        if not tueren:
            # Rennweg: keine benannten Tür-Blöcke im Modelspace, aber Öffnungen
            # in den Blockdefinitionen — die Kaskade hat sie bereits gesucht.
            # Diagnose U12/S4a: den spezifischen Grund der Öffnung durchreichen
            # (Schiebetür: ``tueren._GRUND_OHNE_BOGEN``), sonst bleibt nur der
            # allgemeine Satz.
            tueren = [
                Tuer(id=f"tuer_{i}", xy_mm=o.xy_mm, breite_mm=o.breite_mm,
                     breite_quelle=o.breite_quelle,
                     breite_grund=(None if o.breite_mm is not None else
                                   (o.breite_grund
                                    or "Tueroeffnung ohne messbare Breite")),
                     ist_notausgang=False, quelle=o.quelle)
                for i, o in enumerate(k.tueroeffnungen, start=1)
            ]
        if k.wandkoerper:
            # Türen anderer Plan-Cluster/Etagen-Varianten raus (s. tueren.im_planbereich).
            tueren = im_planbereich(tueren, bounds_aus_wandkoerpern(k.wandkoerper))
        ausgaenge = hauptausgaenge(plan, bounds)
        zirkulation = zirkulation_aus_dxf(plan)

        # ── Fachteil 1: Zuordnung → Typisierung → Wohnungen → Ausgänge →
        # Fluchtwege — rein ERGÄNZEND zu hauptausgaenge/zirkulation.
        # Geschoss mehrstufig (Owner-Entscheidung 2026-09-13): floor →
        # Dateiname → Schriftfeld/Plantext → Höhenkote → UNBEKANNT. Der Befund
        # trägt die entscheidende QUELLE mit und liegt — wie
        # letzte_aussenbereiche — als Attribut für Prüfstrecke/bericht.md
        # bereit; der Contract führt ihn nicht. Der bereits geöffnete `plan`
        # speist die drei Plan-Stufen, es wird keine DXF zweimal gelesen.
        self.geschoss_befund = geschoss_befund(floor, dxf_path, plan)
        geschoss = self.geschoss_befund.geschoss
        # Außen-Analyse je Gebäude-Komponente (Barawitzka: 2 Trakte) + Hof-
        # Erkennung (Mollgasse: Hof mit Weg ins Freie = AUSSEN → Hoftüren
        # werden Endausgänge). Fallback = alte Ein-Konturen-Heuristik.
        # Innen-Zonen mitgeben (Diagnose U8, Slice S2, Owner-Entscheid F6
        # Option 4): Räume und Stempel liegen längst vor — ohne sie legt die
        # Außenanalyse Wohn-/Bad-Zonen hinter dünnen Fassaden ins Freie.
        aussen = None
        if k.wandkoerper:
            aussen = erkenne_aussenbereiche(
                plan, k.wandkoerper, waehle_innen_zonen(plan, raeume, k.zuordnungen))
        self.letzte_aussenbereiche = aussen   # Prüfstrecken-Output (Bericht)
        if aussen is not None and aussen.komponenten:
            kontur = aussen.gedeckt()
        else:
            kontur = aussenkontur(k.wandkoerper) if k.wandkoerper else None
        # Zusätzliche Türquellen (additiv, je Tür mit `quelle`-Audit-Trail):
        # Doppelflügel verschmelzen, Türbögen an der AUSSEN-Grenze ohne
        # Block (Mollgasse-Hoftüren), türimplizierende Texte (Rennweg EG).
        tueren += aussentor_tueren(k.tueroeffnungen, tueren, kontur)
        # Verschmelzen NACH aussentor_tueren: nur so sieht es auch die
        # 'arc_aussen'-Türen (Hoftüren), deren Doppelflügel-Paare sonst nie
        # zusammenfinden — verschmelze_doppelfluegel akzeptiert sie ausdrücklich.
        tueren = verschmelze_doppelfluegel(tueren, wand_segmente(plan))
        tueren += text_tueren(plan, tueren)
        # Wand-Union EINMAL, schon hier: die Seitenprobe überspringt damit
        # Probepunkte im Wandkörper (Slice S4b), die Durchgänge unten nutzen
        # dieselbe Variable.
        wu = wand_union(k.wandkoerper) if k.wandkoerper else None
        for s in zirkulation.segmente:      # 09-WEG = explizite Linien
            s.quelle = "LINIE"
        flw_enden = [p for s in zirkulation.segmente
                     for p in (s.polyline_mm[0], s.polyline_mm[-1])
                     if s.polyline_mm]
        # K3 (Enis Referenz 07): ein stempelloser Raum mit Sanitärbeleg im
        # Umriss einer Wohnung wird BAD/WC. Der Umriss steht erst nach der
        # Wohnungsbildung fest, die Türrollen brauchen den Typ vorher — darum
        # ein einmaliger Vorlauf: Türen und Wohnungen einmal als Probe auf
        # Kopien, dann setzt `typisiere_sanitaer` am echten Raum nur Typ und
        # Flags (wie ein Stempel), und es folgt EIN regulärer Durchlauf.
        # Klasse und Wohnung entstehen dort aus rohen Türen (Grundsatz (b)).
        # Einmalige Rückkante Probe-Klasse/-Wohnung → Typ → rohe Türrolle,
        # keine Iteration (Owner-Frage zu Board 7, docs/SLICES_K1_K4.md).
        # Ohne Kandidaten keine Probe — der Lauf ist dann derselbe wie vorher.
        kand = sanitaer_kandidaten(
            raeume, sanitaerobjekte(plan),
            {z.raum.id for z in k.zuordnungen if z.raum is not None})
        self.sanitaer_befund: list[str] = []   # Prüfstrecken-Ausgabe
        if kand:
            probe_r, probe_t = copy.deepcopy(raeume), copy.deepcopy(tueren)
            probe_t = _tueren_und_wohnungen(plan, k, probe_r, probe_t, kontur, wu,
                                            aussen, geschoss, flw_enden)[0]
            self.sanitaer_befund = typisiere_sanitaer(raeume, kand, probe_r, probe_t)
        (tueren, self.tuer_warnungen, schacht_reste,
         self.wohnungsklasse_warnungen) = _tueren_und_wohnungen(
            plan, k, raeume, tueren, kontur, wu, aussen, geschoss, flw_enden)
        # Ausgangs-Warnungen (u.a. „Geschoss unbekannt, Endausgang nicht
        # bestimmbar") als Prüfstrecken-Output — kein Contract-Feld.
        neue, self.ausgangs_warnungen = leite_ausgaenge(
            tueren, raeume, geschoss, flw_enden)
        vorhandene = list(ausgaenge)
        for a in neue:
            if not any(a.typ == v.typ
                       and abs(a.xy_mm[0] - v.xy_mm[0])
                       + abs(a.xy_mm[1] - v.xy_mm[1]) < 1500.0
                       for v in vorhandene):
                vorhandene.append(a)
        # Obergeschosse haben keine Ausgänge ins Freie (Fenster-/Balkontüren
        # der Fassade sind keine hauseingang-Endausgänge); bei UNBEKANNTem
        # Geschoss entsteht fail closed ebenfalls keiner. Der Filter sitzt
        # hinter dem Zusammenlegen, also greift er auch für die
        # footprint-Ausgänge (Z.102), die ohne Geschossbezug entstehen.
        ausgaenge = ohne_unzulaessige_final_exits(vorhandene, geschoss)
        zirkulation.segmente += linien_segmente(
            explizite_linien(plan), len(zirkulation.segmente))
        # Geschoss-Zielregel (EG/UG → final_exit, OG → stair_exit); Warnungen
        # (kein erreichbarer final_exit im EG) landen als Attribut für die
        # Prüfstrecke/bericht.md — der Contract führt sie nicht.
        self.fluchtweg_warnungen = []
        zirkulation.segmente += fluchtwege(raeume, tueren, ausgaenge,
                                           zirkulation.segmente, geschoss,
                                           self.fluchtweg_warnungen,
                                           self.wohnungsklasse_warnungen)

        # ── Fachteil 2: Lifte (LIFT/KEIN_RAUM, aus STIEGENHAUS ausgestanzt)
        # + Stiegenhaus-Modelle + Anker (Stiegenhaus + Gang). Anker liefern
        # nur Azimute (ADR-0006) — Platzierung bleibt Leonis.
        lifte = finde_lifte(plan, raeume, schacht_reste)
        stiegenhaeuser = []
        anker = []
        wohnungsintern = bestaetigt_privat(raeume, tueren)
        for r in raeume:
            if len(r.polygon_mm) < 3:
                continue
            if r.raum_typ == "STIEGENHAUS":
                modell, a = baue_stiegenhaus_modell(plan, r, lifte, tueren)
                stiegenhaeuser.append(modell)
                anker += a
            elif r.raum_typ == "GANG" and r.id not in wohnungsintern:
                # R4 (§ 6f) unter dem Fail-Safe-Riegel: Anker nur noch auf
                # Gängen, denen die ANKERREGEL nicht privat bestätigt — ein so
                # bestätigter Gang trägt nach R3 beide Flags False.
                anker += anker_fuer_gang(r, tueren, zirkulation.segmente)
        # B2: Der Türanker des Stiegenhauses liegt auf der Schwelle und kann
        # geometrisch in den privat gewordenen Nachbarraum fallen. Er wird auf
        # die Stiegenhaus-Seite gezogen, nicht gestrichen.
        anker = anker_aus_privat_ziehen(anker, raeume, tueren)
        # Kein Anker im Liftschacht (Verbotszone — dort wird nichts montiert).
        if lifte:
            schaechte = [Polygon(lf.polygon_mm) for lf in lifte
                         if len(lf.polygon_mm) >= 3]
            anker = [a for a in anker
                     if not any(s.contains(Point(a.xy_mm)) for s in schaechte)]
        modell = RaumModell(
            # Der Contract führt nur `floor` (eingefroren — kein neues Feld).
            # Gab der Aufrufer nichts vor, trägt hier das ENTSCHIEDENE Geschoss
            # ein: vorher stand im Modell "", während die Ausgangslogik mit
            # einem belegten Geschoss lief, und die 12 floor-Leser
            # (dxf_renderer, validierung, oib_gate, …) sahen den Leerstring.
            # Ein vom Aufrufer gesetztes `floor` bleibt unangetastet — an ihm
            # hängen die OIB-Raumreferenzen.
            floor=floor or geschoss,
            bounds_mm=bounds,
            raeume=raeume,
            tueren=tueren,
            ausgaenge=ausgaenge,
            zirkulation=zirkulation,
            stiegenhaeuser=stiegenhaeuser,
            anker=anker,
        )
        # Kreuzcheck Fluchtweglinien ↔ final_exit — Prüfstrecken-Output
        # (Warnungen/Kandidaten/unbenutzte Exits), bewusst NICHT im Contract.
        # Kante = echte GEBÄUDE-Außenkante (Komponenten-Konturen), damit
        # Außenweg-Endpunkte im Gelände nicht zählen (Mollgasse: ~95 Stück).
        kante = None
        if aussen is not None and aussen.komponenten:
            kante = unary_union([p.exterior for p in aussen.komponenten])
        self.letzter_kreuzcheck = kreuzcheck(modell, kontur, kante)
        return modell
