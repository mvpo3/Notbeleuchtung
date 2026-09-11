"""kuerzel_entscheid — mehrdeutige Stempel-Kürzel: Typ nur mit Beleg UND Entscheidung.

Ein Stempel-Kürzel wie „Schl." ist im Plan mehrdeutig (Schleuse oder
Schlafzimmer — Entscheidungsvorlage in `docs/OFFENE_FRAGEN.md`). Das Wörterbuch
in `raumtyp.py` darf es deshalb NICHT tragen: ein Eintrag dort typisiert JEDES
Vorkommen des Kürzels, also auch die, über die niemand entschieden hat. Hier
gilt die umgekehrte Reihenfolge — drei Bedingungen, alle nötig:

    Kandidaten-Kürzel  +  Zusatzbeleg im Plan  +  Owner-Entscheidung für GENAU
    diese Stempelnummer                        →  raum_typ

Fehlt eine davon, bleibt der Raum untypisiert und bekommt einen Hinweis (der im
Prüfbericht landet) — nie einen geratenen Typ. Das ausgeschriebene Wort
(„Schleuse") ist dagegen eindeutig und steht regulär im Kanon (`raumtyp.py`).

Der Typ selbst (inkl. Flags) kommt aus `raumtyp_flags` — dieses Modul entscheidet
nur, OB ein Kürzel als dieser Typ gelesen werden darf, nicht welche Flags er hat.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from shapely.geometry import Polygon

from notbeleuchtung.hauptengine.contracts.raum_modell import Raum

from .dxf_load import XY, DxfPlan
from .geometrie_typ import stiege_rechtecke
from .raumtyp import _WORT, raumtyp_flags  # _WORT: dieselbe Token-Regel wie das Wörterbuch

if TYPE_CHECKING:  # nur fürs Typ-Bild — sonst Import-Zyklus über stempel_anker
    from .stempel_anker import Stempel

# Kürzel → möglicher Kanon-Typ. Token-exakt, lowercase. Ein Eintrag hier ist
# KEINE Typisierung, sondern nur die Erlaubnis, mit Beleg + Entscheidung zu
# typisieren. Gemessen über die fünf Prüfpläne (2026-09-11): Token `schl`
# kommt 2× vor (beide in Muthgasse_E2 auf A-AREA-IDEN), Token `schleuse` 0×.
KANDIDATEN: dict[str, str] = {"schl": "SCHLEUSE"}


@dataclass(frozen=True)
class Entscheidung:
    """Owner-Entscheidung für ein Kürzel an EINER Stempelnummer."""

    typ: str
    owner: str
    datum: str
    grundlage: str
    quelle: str


# (Kürzel, Stempelnummer) → Entscheidung. Nur hier eingetragene Nummern werden
# typisiert; jedes andere Vorkommen desselben Kürzels bleibt untypisiert.
# ponytail: Stempelnummern sind nur innerhalb einer Planfamilie eindeutig, und der
# Eintrag greift nur, wenn der Nummerntext im Stempelumkreis steht (s. _nummer).
# Bringt eine zweite Familie dieselbe Nummernserie, gilt die Entscheidung dort
# mit — dann die Planfamilie als dritten Schlüssel aufnehmen. Gemessen
# (Muthgasse_E2, 2026-09-12): der Plan trägt schon Nummern FREMDER Geschosse
# ('E3-VF-12b' 4816 mm neben dem Kandidaten, 'E3-25-02a' 2x) — es braucht also
# keine zweite Planfamilie; dass 'E2-VF-11a' genau 1x vorkommt, ist gemessen,
# nicht strukturell garantiert.
# `datum` = Tag, an dem der Owner die Entscheidung übermittelt hat
# (Owner-Auftrag 2026-09-11); umgesetzt am 2026-09-12.
ENTSCHEIDUNGEN: dict[tuple[str, str], Entscheidung] = {
    ("schl", "E2-VF-11a"): Entscheidung(
        typ="SCHLEUSE",
        owner="Enis",
        datum="2026-09-11",
        grundlage=("Lage beim Stiegenkern; Vergleichsgeschoss E8 "
                   "'DBA-Abstr. Schleuse' 627 mm (E9 10 mm) an derselben Lage"),
        quelle="docs/OFFENE_FRAGEN.md § Entscheidung Schl. (Enis, 2026-09-11)",
    ),
}

# Stempelnummer-Muster der Muthgasse-Familie: 'E2-VF-11a', 'E2-15-03'.
_NUMMER = re.compile(r"^[A-Z]{1,2}\d?-[A-Z0-9]{1,3}-\d+[a-z]?$")
# Nummern-Suchradius = Gruppierungsradius von `stempel_anker.finde_stempel`;
# die Entscheidung gilt nur, wenn die Nummer wirklich am Stempel steht.
# Gemessen im Lauf (Muthgasse_E2), gerechnet ab `Stempel.position_mm` — das ist
# der m²-Anker, NICHT der Namens-Text: Nummer 350 mm bei E2-VF-11a UND bei
# E2-VF-11b. Im 1500-mm-Ring von E2-VF-11b liegt zusätzlich das Fremdfragment
# 'E2-15-03' (Inventar: 1469 mm ab Namens-Text), deshalb gewinnt die NÄCHSTE
# Nummer, nicht die erste gefundene.
_NUMMER_RADIUS_MM = 1500.0

# Text-Beleg: Brandschutz-/Schleusen-Vokabular im Stempelumkreis.
_BELEG_TOKEN = re.compile(r"^(?:dba|abstr|schleuse)$", re.IGNORECASE)
# Gemessen im Lauf (Muthgasse_E2), gerechnet ab `Stempel.position_mm` (m²-Anker):
# 'DBA' 1663 mm bei E2-VF-11a, 'WDB DBA' 1232 mm bei E2-VF-11b. 2000 mm deckt
# beide mit ~340 mm Luft. (Das Inventar nennt 1495 bzw. 1042 mm — dort ab dem
# NAMENS-Text gemessen, der ~190–350 mm neben dem Anker liegt; beide Bezugs-
# punkte sind richtig, nur eben verschieden.) Wird der Radius kleiner als
# ~1700 mm, verliert E2-VF-11a seinen Text-Beleg.
_BELEG_RADIUS_MM = 2000.0

# Stiegenkern-Lage = Kontakt/Überlappung. Gemessen (Muthgasse_E2): die 0-mm-Klasse
# ist durch eine Lücke von der nächsten getrennt (nächster wandgetrennter Nachbar
# 26 mm, typisch 176–280 mm) — 0.0 ist damit eine echte Grenze, kein Schwellenwert
# nach Gefühl. Achtung: die Klasse trennt Schleuse NICHT von Küchen — sie ist
# genau deshalb nur Beleg, nie Entscheidung.
_KONTAKT_MM = 0.0


def kandidat_kuerzel(name: str) -> str | None:
    """Stempelname → Kandidaten-Kürzel (token-exakt, lowercase), sonst None."""
    tokens = {t.lower() for t in _WORT.findall(name)}
    return next((k for k in KANDIDATEN if k in tokens), None)


def _texte(plan: DxfPlan) -> list[tuple[str, XY]]:
    """(Text, xy_mm) aller TEXT/MTEXT des Architektur-Raums — layerunabhängig.

    Wie `stempel_anker.finde_stempel`: die Muthgasse-Stempel liegen auf
    A-AREA-IDEN/A-GENM-IDEN, also NICHT auf `raumtyp.TEXT_PREFIXES`.
    """
    out: list[tuple[str, XY]] = []
    for e in plan.space:
        t = e.dxftype()
        if t not in ("MTEXT", "TEXT"):
            continue
        txt = e.plain_text() if t == "MTEXT" else e.dxf.text
        if txt and txt.strip():
            out.append((txt.strip(), plan._scale(e.dxf.insert)))
    return out


def _abstand(a: XY, b: XY) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def _nummer(texte: list[tuple[str, XY]], xy: XY) -> tuple[str | None, float]:
    """Nächster Stempelnummern-Text im Umkreis → (Nummer, Abstand_mm)."""
    treffer = [(t, _abstand(p, xy)) for t, p in texte
               if _NUMMER.match(t) and _abstand(p, xy) <= _NUMMER_RADIUS_MM]
    if not treffer:
        return None, 0.0
    nummer, d = min(treffer, key=lambda x: x[1])
    return nummer, d


def _belege(raum: Raum, stempel: Stempel, stiegenhaus: list[Polygon],
            stiegen: list[Polygon], texte: list[tuple[str, XY]]) -> list[str]:
    """Zusatzbelege des Kandidaten — mindestens einer nötig, keiner allein genug."""
    gefunden: list[str] = []
    poly = Polygon(raum.polygon_mm).buffer(0) if len(raum.polygon_mm) >= 3 else None
    if poly is not None and not poly.is_empty:
        kern = next((q for q in stiegenhaus + stiegen
                     if poly.distance(q) <= _KONTAKT_MM), None)
        if kern is not None:
            gefunden.append("Stiegenkern-Lage (0 mm Kontakt/Überlappung)")
    nah = [(t, round(_abstand(p, stempel.position_mm)))
           for t, p in texte
           if _abstand(p, stempel.position_mm) <= _BELEG_RADIUS_MM
           and any(_BELEG_TOKEN.match(w) for w in _WORT.findall(t))]
    if nah:
        t, d = min(nah, key=lambda x: x[1])
        gefunden.append(f"Text-Beleg »{t}« in {d} mm")
    return gefunden


def loese_kuerzel(plan: DxfPlan, kandidaten: list[tuple[Raum, Stempel]],
                  raeume: list[Raum]) -> list[str]:
    """Kandidaten-Kuerzel aufloesen; setzt ``raum_typ`` + Flags NUR bei Beleg UND
    Entscheidung. Rueckgabe: Hinweis-Zeilen (auch fuer die nicht typisierten Faelle).

    Grenze des Polygon-Belegwegs: sichtbar sind hier nur die STIEGENHAUS-Raeume,
    die INNERHALB der Kaskade schon typisiert sind (Stempel-Rueckschreibung) --
    ``typisiere_geometrisch`` laeuft erst spaeter (``provider.py``). Auf
    label-losen Plaenen traegt deshalb allein ``stiege_rechtecke``.
    """
    if not kandidaten:
        return []
    texte = _texte(plan)
    # Stiegenkern-Quelle: dieselben Treppen-Block-Extents, aus denen
    # `geometrie_typ.typisiere_stiegenhaus` STIEGENHAUS ableitet - nicht nachgebaut.
    stiegen = [Polygon(rect).buffer(0) for rect, _c, _a in stiege_rechtecke(plan)]
    stiegenhaus = [Polygon(r.polygon_mm).buffer(0) for r in raeume
                   if (r.raum_typ or "").strip() == "STIEGENHAUS"
                   and len(r.polygon_mm) >= 3]
    hinweise: list[str] = []
    for raum, stempel in kandidaten:
        if kandidat_kuerzel(stempel.name or "") is None:
            continue
        # Je Kandidat gekapselt: ein Fehler darf weder die anderen Kandidaten
        # mitnehmen noch die schon gesammelten Hinweise verlieren - ein typisierter
        # Raum ohne Nachweis-Zeile im Bericht waere schlimmer als kein Typ.
        try:
            hinweise.append(_ein_kandidat(raum, stempel, stiegenhaus, stiegen, texte))
        except Exception as exc:  # noqa: BLE001
            hinweise.append(f"{raum.id}: Stempel »{stempel.name}« - "
                            f"Kuerzel-Aufloesung fehlgeschlagen ({exc}), "
                            f"bleibt untypisiert")
    return hinweise


def _ein_kandidat(raum: Raum, stempel: Stempel, stiegenhaus: list[Polygon],
                  stiegen: list[Polygon], texte: list[tuple[str, XY]]) -> str:
    """Ein Kandidat: typisiert nur bei Entscheidung UND Beleg; liefert den Hinweis.

    Reihenfolge: ERST das Entscheidungs-Register, DANN die Belege. Sonst waere im
    Bericht "Beleg weggefallen" nicht von "niemand hat entschieden" zu
    unterscheiden, und eine gefaellte Owner-Entscheidung verpuffte still -- der
    Text-Beleg von `E2-VF-11a` hat nur ~340 mm Luft zum Radius.
    """
    kuerzel = kandidat_kuerzel(stempel.name or "")
    nummer, d_nummer = _nummer(texte, stempel.position_mm)
    nr_txt = f"Nummer {nummer} ({d_nummer:.0f} mm)" if nummer else "keine Nummer gefunden"
    kopf = f"{raum.id}: Stempel »{stempel.name}« (Kuerzel `{kuerzel}`), {nr_txt}"
    ent = ENTSCHEIDUNGEN.get((kuerzel, nummer)) if nummer else None
    belege = _belege(raum, stempel, stiegenhaus, stiegen, texte)
    if ent is None:
        if not belege:
            return (f"{kopf} - bleibt untypisiert: kein Zusatzbeleg (weder "
                    f"Stiegenkern-Lage noch Text-Beleg); Entscheidung ausstehend")
        return (f"{kopf} - bleibt untypisiert: Entscheidung ausstehend. "
                f"Belege: {'; '.join(belege)}")
    if not belege:
        return (f"{kopf} - bleibt untypisiert: Entscheidung {ent.owner} {ent.datum} "
                f"liegt vor, aber kein Zusatzbeleg (weder Stiegenkern-Lage noch "
                f"Text-Beleg) - Beleg-Regel/Radius pruefen")
    tf = raumtyp_flags(ent.typ)
    if tf is None:      # Kanon-Typ fehlt im Woerterbuch -> nichts erfinden
        return (f"{kopf} - bleibt untypisiert: Entscheidungs-Typ {ent.typ} steht "
                f"nicht im Kanon (raumtyp.py)")
    label, flucht, communal = tf
    raum.raum_typ = label
    raum.ist_fluchtweg = raum.ist_fluchtweg or flucht
    raum.ist_communal = raum.ist_communal or communal
    return (f"{kopf} -> {label} (Entscheidung {ent.owner} {ent.datum}: "
            f"{ent.grundlage}; {ent.quelle}). Belege: {'; '.join(belege)}")
