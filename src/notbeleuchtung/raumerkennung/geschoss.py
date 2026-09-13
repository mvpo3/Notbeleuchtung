r"""geschoss — Geschoss mehrstufig bestimmen, jede Stufe mit ihrer Quelle.

OWNER-ENTSCHEIDUNG 2026-09-13, wörtlich:

    "Geschoss mehrstufig bestimmen, in dieser Reihenfolge, jede Stufe mit
    Quelle: DATEINAME (EG, OG1..n, UG, KG, E2, BT1-EG) -> SCHRIFTFELD/PLANTEXT
    -> HOEHENKOTE (FOK/ROK/+-0,00, z.B. Rennweg +10,72: ueber 3 m heisst
    Obergeschoss, unter -1 m Keller) -> UNBEKANNT. Bei UNBEKANNT fail-closed:
    kein final_exit, stattdessen Warnung 'Geschoss unbekannt, Endausgang nicht
    bestimmbar'. Kein Standardwert EG."

Die Stufen sind KURZSCHLÜSSIG: die erste Stufe mit Treffer entscheidet, die
teuren Plan-Scans laufen nur, wenn ``floor`` und Dateiname nichts hergeben.
``GeschossBefund.quelle`` trägt die entscheidende Stufe mit — sonst ist die
Messung „welche Quelle entscheidet wie oft" später nicht möglich.

STUFE 0 ``floor`` (Quelle ``floor``) — der Contract-Parameter aus
``RaumProvider.parse(dxf_path, floor)``. Steht VOR dem Dateinamen, weil das die
bisherige Semantik von ``geschoss_aus`` ist und ``api/main.py`` ihn als echte
Benutzereingabe führt. Neu ist nur, dass ein erkannter ``floor`` nicht mehr am
Dateinamen vorbei verloren geht (vorher gemessen: ``floor="E2"`` ergab ``""``).

STUFE 1 DATEINAME (Quelle ``dateiname``) — drei Muster-Gruppen in dieser
Reihenfolge, weil die späteren die unsichereren sind:

  (a) Kürzel: das Regex von vor dieser Änderung, unverändert übernommen
      (EG/UG/KG/DG/OG<n>/<n>OG). Deckt auch das Owner-Muster ``BT1-EG`` ab.
  (b) Deutsche Wortformen, im Repo gemessen in BEIDEN Schreibweisen: ``ß``
      (Mollgasse ``1.Obergeschoß``) und ``ss`` (Fischamend
      ``…_ERDGESCHOSS BT1``, ``…_1-OBERGESCHOSS BT1``). Die Ziffer davor darf
      mit ``.``, ``-``, ``_``, Leerzeichen oder ohne Trenner stehen — alle vier
      Formen kommen im Korpus vor. ``DACHDRAUFSICHT`` ist bewusst KEIN Treffer:
      eine Dachdraufsicht ist kein Geschoss.
  (c) Etagen-Nummerierung ``E<n>`` → ``OG<n>``. Grundlage ist
      ``docs/ENIS_STAND_1_5_0.md:51`` („Geschoss **E2 = 2. Obergeschoss**"),
      nicht eine eigene Annahme. Sie läuft NACH (a) und (b), damit ein echtes
      Geschoss-Kürzel im selben Namen gewinnt: das Projekt „Baufeld E2"
      (``Handoff/LEONIS.md:810``, 8 Geschosse) trägt ``E2`` als PROJEKTnamen,
      und ein Name wie ``Baufeld_E2_UG`` muss ``UG`` liefern, nicht ``OG2``.
      Im Repo ist diese Kollision heute nicht messbar (``Baufeld E2`` liegt nur
      als ZIP vor) — die Reihenfolge ist die Vorsorge dafür.

VORSCHALTUNG zu Stufe 2-4: Blätter, die KEIN Geschoss SIND — Schnitt,
Lageplan, Legende, Symbolbibliothek, Vorlage, Dachdraufsicht
(``_NICHT_PLAN_RE``). Sie tragen den Plankopf IHRER SERIE, also lieferten die
Plan-Stufen dort das Geschoss des Projekts statt des Blattes. Der Marker sperrt
nur die Plan-Stufen; der Dateiname darf weiter entscheiden.

STUFE 2 SCHRIFTFELD (Quelle ``schriftfeld``) — Layoutnamen und Text der
Paperspace-Layouts. Erreichbar über ``plan.doc``, NICHT über
``plan.entities()``: ``dxf_load`` iteriert nur ``space`` (Modelspace bzw.
wandtragender Block). Layoutname vor Layouttext, weil der Name das Schriftfeld
am direktesten trägt (Barawitzka: Layout ``415_260415_PP_VA_1_3 0 EG``).

Der Layoutname darf das blanke Kürzel tragen — er benennt das BLATT. Der freie
Plankopf-TEXT darf es NICHT: dort ist ``KG`` im Korpus ausnahmslos die
Katastralgemeinde (``KG.: 01503 Heiligenstadt``, ``GST-NR. 184; EZ 76; KG 05219
SCHWADORF``) oder die Rechtsform (``Toga 2 Immobilienverwaltungs GmbH & Co
KG``). Beides steht auf JEDEM Blatt der Serie. GEMESSEN: diese zwei Zeilen
machten den 1. Stock der Barawitzka-Serie zu einem Keller — mit vier
``final_exit`` und ohne eine einzige Warnung, während der Plankopf desselben
Blattes ``1.Stock PP STG1`` sagt. Aus freiem Text zählt daher nur die
ausgeschriebene WORTFORM (``mit_kuerzel=False``).

STUFE 3 PLANTEXT (Quelle ``plantext``) — MTEXT/TEXT/ATTRIB des
Architektur-Raums, ebenfalls NUR die ausgeschriebene Wortform. Der Modelspace
ist freier Text wie der Plankopf: ``HEIGHT=RBVK OG 01`` und ``HEIGHT=RBVK KG``
auf Mollgasse_EG sind Höhenlisten über mehrere Geschosse, keine
Geschossaussage. GEMESSEN: mit blankem Kürzel kam der 3. Stock der
Barawitzka-Serie über ``EG 2×`` als ausgangsfähiges Erdgeschoss heraus.
MEHRHEITSENTSCHEID, kein Erst-Treffer. ``E<n>`` wird auf dieser Stufe NICHT
gelesen: im Plantext ist ``E1``/``E2`` die Notausgangs-Kennzeichnung, die
``tuer_typisierung._NOTAUSGANG_TEXT`` schon auswertet — dieselbe
Zeichenfolge, andere Bedeutung.

RESTBEFUND, nicht eigenmächtig behoben: auf ``…1_6 3 St`` trägt der Modelspace
zweimal ``Erdgeschoß\PTop 01`` / ``…Top 02`` — ein Wohnungsverzeichnis, das die
ERDGESCHOSS-Tops auf dem Blatt des 3. Stocks auflistet. Die Wortform ist damit
auch im Modelspace nicht sicher, und der Mehrheitsentscheid hilft nicht: die
falsche Aussage steht 2:0. Die Höhenkote desselben Blattes sähe es richtig
(Median +8,79 m aus 7 Koten → OG), aber die Owner-Reihenfolge stellt PLANTEXT
VOR HOEHENKOTE. Ob die Höhenkote vorzuziehen ist, ist eine OWNER-Entscheidung
(s. OFFEN unten) — die vorgegebene Reihenfolge steht unverändert.

STUFE 4 HOEHENKOTE (Quelle ``hoehenkote``) — Median der FOK/FBOK/ROK/RDOK-Koten
im Text. GRENZEN, ehrlich benannt:

  - Nur MIT Präfix. ``STUK`` (Sturzunterkante) und blankes ``UK``/``OK``
    bleiben außen vor: das sind Sturz- und Bauteilkanten, keine Geschosshöhen.
  - Das Owner-Beispiel „Rennweg +10,72" ist mit dem heutigen Loader NICHT
    erreichbar: der Wert steht präfixlos in der BLOCKdefinition
    ``Level Dimension_1``, und ``plan.entities()`` iteriert keine
    Blockdefinitionen. Rennweg_EG trifft die Stufe aus demselben Grund nicht
    (``+0,32 +180,83 UE.WN``, präfixlos). Die Stufe ist damit DÜNN — sie ist
    implementiert, weil die Texte belegt da sind, aber sie greift nur, wo ein
    Büro seine Koten beschriftet. Wie oft sie im Korpus wirklich entscheidet,
    steht im Prüfbericht je Plan (``quelle``), nicht in einer Schätzung hier.
  - Eine z-Koordinate gibt es nicht: ``dxf_load._scale`` verwirft sie. Der
    Höhenbezug kann nur aus dem TEXT kommen.

STUFE 5 UNBEKANNT (Quelle ``unbekannt``) — ``geschoss == ""``, kein
Standardwert EG. Die fail-closed-Auswertung sitzt bei den Ausgängen
(``ausgaenge.ohne_unzulaessige_final_exits``), nicht hier: dieses Modul
entscheidet nur, WAS das Geschoss ist, nicht was daraus folgt.

KOSTEN: Stufe 2-4 brauchen den geladenen Plan; ``provider.parse`` gibt seinen
schon geöffneten mit, es wird keine DXF zweimal gelesen. Auf einem Plan, dessen
Geschoss weder ``floor`` noch Dateiname hergeben, laufen bis zu zwei weitere
Durchläufe über den Architektur-Raum (erst Plantext, dann Höhenkote).

GEMESSEN — eigene Läufe 2026-09-13 im PRODUKTIONSPFAD, also mit geladenem
Plan (``provider.py:109``, ``plan_pruefen.py:1222``). Die frühere Kennzahl
„28 verbliebene UNBEKANNT" war OHNE Plan gemessen, lief also nur über die
Dateiname-Stufe und galt für die Produktion nicht.

  Über alle 83 DXF des Repos (``rglob``, ohne ``.git``):

  - OHNE Plan (nur Dateiname): 55 entschieden, 28 UNBEKANNT.
  - MIT Plan, VOR dieser Reparatur: 6 UNBEKANNT — 55 ``dateiname``,
    19 ``schriftfeld``, 2 ``plantext``, 1 ``hoehenkote``. Von den 22
    Plan-Stufen-Treffern war KEIN EINZIGER ein richtig erkannter Grundriss:
    15× Katastralgemeinde/Rechtsform (7 Schnitte, Lageplan, 1./2./3. Stock,
    FDM, DD STG1 …), 4× blankes DG/KG auf einer Dachdraufsicht, 2× ein echtes
    „Erdgeschoss" auf Symbolbibliothek bzw. Plan-Vorlage, 1× eine Einzelkote
    auf ``GRUNDRISS DD``.
  - MIT Plan, NACH dieser Reparatur: 26 UNBEKANNT — 55 ``dateiname``,
    1 ``hoehenkote`` (``…1_5 2 St``, Median +5,76 m aus 10 Koten → OG),
    1 ``plantext`` (``…1_6 3 St`` → EG, der Restbefund oben). 20 erfundene
    Geschosse sind damit fail closed geworden; keines davon war richtig.

  - HÖHENKOTE, Mindestzahl ``_MIND_KOTEN`` = 3 (EIGENE Setzung): entfernt genau
    die beiden Ein-Koten-Urteile (``…1_9 DD STG1`` n=1 → OG,
    ``…GRUNDRISS DD`` n=1 → OG). Die kleinste ECHTE Geschossaussage im Korpus
    steht bei n=3 (Muthgasse E3..E6) und bleibt erhalten.
  - KEIN Standardwert EG mehr zwischen den Schwellen: ``…1_4 1 St`` hat Median
    +2,88 m aus 10 Koten und war damit ein ausgangsfähiges Erdgeschoss — jetzt
    UNBEKANNT. Die EG-Pläne, die die Kote früher nullnah bestätigte
    (Barawitzka n=41, Mollgasse n=108), entscheidet ohnehin schon der
    Dateiname; die Produktion verliert dadurch keinen Befund.

  - SCHREIBWEISE, eine kanonische Form ``<n>OG``/``<n>KG``: 27 Pläne
    normalisiert (``OG1``→``1OG`` …). Kein Plan ändert seine Schreibweise
    unerwartet: die Pläne, die schon auf ``25a2e35`` die Ziffer vorn trugen
    (``20230228_po_1og_V``, ``po_2og_V``), bleiben unverändert; normalisiert
    wird nur die zweite Schreibweise, die sonst beim Renderer
    (``dxf_renderer.py:1066``) auf den Rohstring durchgefallen wäre.

OFFEN (Owner-Entscheidungen, hier NICHT eigenmächtig getroffen):

  - ``…1_6 3 St`` bleibt über das Wohnungsverzeichnis ein falsches ``EG``.
    Der Fix wäre HOEHENKOTE VOR PLANTEXT — das ändert die Owner-Stufenfolge.
  - ``…1_4 1 St``, ``2 St``, ``3 St`` tragen ihr Geschoss als „1.Stock" im
    Plankopf. ``STOCK`` ist bewusst KEIN Muster: das wäre eine neue Wortform
    ohne Owner-Deckung. Mit ihr wären die drei Blätter sauber belegt.
  - Der Mollgasse-Gleichstand ``EG 11× : KG 11×`` im Plantext ist mit der
    Wortform-Regel gegenstandslos geworden: blanke Kürzel zählen nicht mehr.
"""
from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path
from statistics import median
from typing import Literal

#: Wortlaut aus der Owner-Entscheidung — Warnung bei UNBEKANNT.
GESCHOSS_UNBEKANNT_WARNUNG = "Geschoss unbekannt, Endausgang nicht bestimmbar"

Quelle = Literal["floor", "dateiname", "schriftfeld", "plantext", "hoehenkote",
                 "unbekannt"]

# (a) Kürzel — unverändert aus tuer_typisierung.py übernommen, damit kein
# Aufrufer und kein Band an einer stillen Muster-Änderung kippt.
_KUERZEL_RE = re.compile(r"(?<![A-Z0-9])(EG|UG\d*|KG\d*|DG|OG\s?\d+|\d+\.?\s?OG)",
                         re.IGNORECASE)
# (b) Deutsche Wortformen, beide Schreibweisen (ß und ss), Ziffer optional mit
# . - _ oder Leerzeichen davor. DACHDRAUFSICHT trifft nicht (kein „GESCHOSS").
_WORTFORM_RE = re.compile(
    r"(?:(\d)\s*[.\-_ ]?\s*)?(ERD|OBER|UNTER|KELLER|DACH)GESCHO(?:SS|ß)",
    re.IGNORECASE)
_WORT_KUERZEL = {"ERD": "EG", "OBER": "OG", "UNTER": "UG", "KELLER": "KG",
                 "DACH": "DG"}
#: (c) Etagen-Nummerierung E1..E9 (Muthgasse-Familie). E2 = 2. Obergeschoss
#: laut docs/ENIS_STAND_1_5_0.md:51.
_ETAGE_RE = re.compile(r"(?<![A-Z0-9])E([1-9])(?![0-9])", re.IGNORECASE)
#: Höhenkoten MIT Präfix — FOK/FBOK = Fertigboden-, ROK/RDOK = Rohdecken-
#: Oberkante. Zwischen Präfix und Wert stehen im Korpus bis zu elf Zeichen
#: (``RDOK EG = -0.18``, ``FOK STGH = %%p0.00``), aber keine Ziffer.
_KOTE_RE = re.compile(
    r"\b(?:FOK|FBOK|ROK|RDOK)\b[^0-9+-]{0,12}([+-]?\d{1,3}[.,]\d{1,3})",
    re.IGNORECASE)
#: Blätter, die KEIN Geschoss tragen: Schnitt, Lageplan, Legende,
#: Symbolbibliothek, Vorlage, Dachdraufsicht. Der Marker sperrt die drei
#: PLAN-Stufen — ein Schnitt und ein Lageplan SIND kein Geschoss, egal was ihr
#: Schriftfeld sagt. Der DATEINAME darf weiter entscheiden, damit kein bereits
#: erkannter Plan sein Geschoss verliert.
_NICHT_PLAN_RE = re.compile(
    r"SCHNITT|(?<![A-Z])SCHN(?![A-Z])|LAGEPLAN|LEGENDE|SYMBOL|VORLAGE"
    r"|DRAUFSICHT|(?<![A-Z])DD(?![A-Z])|PLANUNGSUNTERST|_SUPPORT",
    re.IGNORECASE)
#: Kanonische Schreibweise: die Ziffer steht VORN (``1OG``, ``2KG``). So
#: schreiben es die Fixtures (``raum_modell_wohnbau_1og.json`` führt
#: ``"floor": "1OG"``, ``raum_modell_4og.json`` ``"4OG"``, die
#: Mollgasse-Referenzen ``"1KG"``/``"2KG"``), die Renderer-Tabelle
#: (``dxf_renderer.py:1066``) und die API (``main.py:125``, „z.B. '4OG'").
#: ``OG1`` wäre die zweite Schreibweise für dasselbe Geschoss und fiele beim
#: Renderer auf den Rohstring durch.
_ZIFFER_HINTEN_RE = re.compile(r"^(OG|KG|UG)(\d+)$")
# OWNER-SETZUNG 2026-09-13, NICHT gemessen: „ueber 3 m heisst Obergeschoss,
# unter -1 m Keller". Beide Schwellen stammen aus der Owner-Entscheidung, nicht
# aus einer Auswertung des Korpus — wer sie verschiebt, braucht den Owner.
_OG_AB_M = 3.0
_KG_UNTER_M = -1.0
# EIGENE SETZUNG (nicht Owner, nicht Norm) — unter dieser Kotenzahl urteilt die
# Stufe gar nicht. Grund, am Korpus gemessen: zwei Blätter wurden von einer
# EINZIGEN Kote entschieden (``…1_9 DD STG1`` n=1 → OG, ``…GRUNDRISS DD`` n=1
# → OG), beide Dachdraufsichten. Die kleinste im Korpus belegte ECHTE
# Geschossaussage steht bei n=3 (Muthgasse E3..E6, Median +12,10 bis
# +21,25 m). 3 trennt beides und kostet keinen richtigen Befund.
_MIND_KOTEN = 3


@dataclass(frozen=True)
class GeschossBefund:
    """Geschoss + die Stufe, die es entschieden hat, + ihr wörtlicher Beleg."""

    geschoss: str          # "" = UNBEKANNT
    quelle: Quelle
    beleg: str = ""

    @property
    def unbekannt(self) -> bool:
        return not geschoss_bekannt(self.geschoss)


def geschoss_bekannt(geschoss: str) -> bool:
    """True, wenn eine Stufe ein Geschoss belegt hat (``""`` = UNBEKANNT)."""
    return bool((geschoss or "").strip())


def ist_erdgeschoss(geschoss: str) -> bool:
    return geschoss.upper().startswith("EG")


def ist_obergeschoss(geschoss: str) -> bool:
    g = geschoss.upper()
    return "OG" in g and not g.startswith("EG") or g == "DG"


def geschoss_befund(floor: str | None = None, dxf_pfad: str | None = None,
                    plan=None) -> GeschossBefund:
    """Geschoss mehrstufig bestimmen (Stufen: s. Modul-Docstring).

    ``plan`` = geladener ``DxfPlan`` (optional). Fehlt er, enden die Stufen
    nach dem Dateinamen — Schriftfeld/Plantext/Höhenkote brauchen den Plan.
    """
    if floor:
        treffer = _aus_text(floor, mit_etage=True)
        if treffer:
            return GeschossBefund(treffer[0], "floor",
                                  f"floor-Parameter {floor!r} → {treffer[1]!r}")
    if dxf_pfad:
        stem = Path(dxf_pfad).stem
        treffer = _aus_text(stem, mit_etage=True)
        if treffer:
            return GeschossBefund(treffer[0], "dateiname",
                                  f"Dateiname {stem!r} → {treffer[1]!r}")
    if plan is not None and not _ist_nicht_plan(dxf_pfad):
        befund = (_aus_schriftfeld(plan) or _aus_plantext(plan)
                  or _aus_hoehenkote(plan))
        if befund is not None:
            return befund
    return GeschossBefund("", "unbekannt", GESCHOSS_UNBEKANNT_WARNUNG)


def geschoss_aus(floor: str | None, dxf_pfad: str | None = None) -> str:
    """Geschoss-Kürzel — dünne Hülle über ``geschoss_befund``.

    Signatur und Aufrufer unverändert; ohne Plan laufen nur die Stufen
    ``floor`` und ``dateiname``. Wer die Plan-Stufen braucht, ruft
    ``geschoss_befund(floor, pfad, plan)`` und bekommt die Quelle mit.
    """
    return geschoss_befund(floor, dxf_pfad).geschoss


def _ist_nicht_plan(dxf_pfad: str | None) -> bool:
    """Schnitt/Lageplan/Legende/Symbolbibliothek/Vorlage/Draufsicht?

    Solche Blätter tragen KEIN Geschoss, haben aber denselben Plankopf wie die
    Grundrisse derselben Serie — die Plan-Stufen lieferten dort das Geschoss
    des PROJEKTS statt des Blattes.
    """
    return bool(dxf_pfad and _NICHT_PLAN_RE.search(Path(dxf_pfad).stem))


# ── Stufe 0/1: floor-Parameter + Dateiname ──────────────────────────────────

def _aus_text(text: str, mit_etage: bool,
              mit_kuerzel: bool = True) -> tuple[str, str] | None:
    """(Geschoss, wörtlicher Treffer) oder None.

    ``mit_etage`` schaltet E<n>. ``mit_kuerzel=False`` verbietet das BLANKE
    Kürzel und lässt nur die ausgeschriebene Wortform gelten — für freien
    Fließtext, in dem ``KG`` die Katastralgemeinde oder die Rechtsform ist
    (s. Modul-Docstring, Stufe 2).
    """
    m = _KUERZEL_RE.search(text) if mit_kuerzel else None
    if m:
        return _norm(m.group(1)), m.group(1)
    m = _WORTFORM_RE.search(text)
    if m:
        kuerzel = _WORT_KUERZEL[m.group(2).upper()]
        ziffer = m.group(1)
        # Die Ziffer zählt nur, wo sie ein Geschoss numeriert (1.OG, 2.KG) —
        # „Erdgeschoss" und „Dachgeschoss" gibt es nicht numeriert.
        if ziffer and kuerzel in ("OG", "KG", "UG"):
            return _kanonisch(f"{kuerzel}{ziffer}"), m.group(0)
        return kuerzel, m.group(0)
    if mit_etage:
        m = _ETAGE_RE.search(text)
        if m:
            return _kanonisch(f"OG{m.group(1)}"), m.group(0)
    return None


def _norm(token: str) -> str:
    return _kanonisch(token.upper().replace(" ", "").replace(".", ""))


def _kanonisch(geschoss: str) -> str:
    """``OG1`` → ``1OG`` — EINE Schreibweise, die auch der Renderer kennt."""
    m = _ZIFFER_HINTEN_RE.match(geschoss)
    return f"{m.group(2)}{m.group(1)}" if m else geschoss


# ── Stufe 2/3: Schriftfeld + Plantext ───────────────────────────────────────

def _aus_schriftfeld(plan) -> GeschossBefund | None:
    """Layoutnamen + Paperspace-Text; der Modelspace bleibt Stufe 3."""
    doc = getattr(plan, "doc", None)
    if doc is None:
        return None
    namen: list[str] = []
    texte: list[str] = []
    for name in doc.layout_names():
        if name.lower() == "model":
            continue
        namen.append(name)
        texte.extend(_entity_texte(doc.layout(name)))
    # Layoutname: Kürzel erlaubt — er benennt das BLATT, nicht den Fließtext.
    # Plankopf-TEXT: nur die ausgeschriebene Wortform. Blankes KG/EG/DG aus
    # Fließtext ist im Korpus ausnahmslos Katastralgemeinde („KG.: 01503
    # Heiligenstadt", „KG 05219 SCHWADORF") oder Rechtsform („GmbH & Co KG") —
    # beides steht auf JEDEM Blatt der Serie und machte den 1. Stock zum Keller.
    return (_mehrheit(_tokens(namen), "schriftfeld", "Layoutname")
            or _mehrheit(_tokens(texte, mit_kuerzel=False), "schriftfeld",
                         "Plankopf-Wortform"))


def _aus_plantext(plan) -> GeschossBefund | None:
    # Wie beim Plankopf nur die ausgeschriebene WORTFORM. Blankes EG/KG/OG im
    # Modelspace ist Höhenlisten-Rauschen (``HEIGHT=RBVK OG 01``,
    # ``HEIGHT=RBVK KG``) und keine Geschossaussage. GEMESSEN 2026-09-13: mit
    # blankem Kürzel kam der 3. Stock der Barawitzka-Serie als ``EG`` heraus
    # (EG 2×) — ein Obergeschoss als ausgangsfähiges Erdgeschoss. Ohne
    # entscheidet ihn die Höhenkote zu ``OG`` (Median +8,79 m aus 7 Koten).
    # Der Mehrheitsentscheid allein hat das NICHT aufgefangen.
    return _mehrheit(_tokens(_entity_texte(plan.entities()), mit_kuerzel=False),
                     "plantext", "MTEXT/TEXT/ATTRIB-Wortform")


def _entity_texte(entities: Iterable) -> Iterator[str]:
    """Textinhalte: MTEXT, TEXT und die ATTRIBs eines INSERT."""
    for e in entities:
        t = e.dxftype()
        if t == "MTEXT":
            yield e.text or ""
        elif t == "TEXT":
            yield e.dxf.text or ""
        elif t == "INSERT":
            for a in e.attribs:
                yield a.dxf.text or ""


def _tokens(texte: Iterable[str], mit_kuerzel: bool = True) -> Counter[str]:
    """Geschoss-Treffer je TEXTZEILE zählen (ohne E<n>, s. Modul-Docstring)."""
    c: Counter[str] = Counter()
    for text in texte:
        for zeile in (text or "").splitlines():
            treffer = _aus_text(zeile, mit_etage=False,
                                mit_kuerzel=mit_kuerzel)
            if treffer:
                c[treffer[0]] += 1
    return c


def _mehrheit(c: Counter[str], quelle: Quelle,
              woher: str) -> GeschossBefund | None:
    """Häufigstes Geschoss gewinnt; Gleichstand alphabetisch (deterministisch)."""
    if not c:
        return None
    rang = sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))
    beleg = ", ".join(f"{g} {n}×" for g, n in rang[:4])
    return GeschossBefund(rang[0][0], quelle, f"{woher}: {beleg}")


# ── Stufe 4: Höhenkote ──────────────────────────────────────────────────────

def _aus_hoehenkote(plan) -> GeschossBefund | None:
    werte: list[float] = []
    for text in _entity_texte(plan.entities()):
        for m in _KOTE_RE.finditer(text):
            try:
                werte.append(float(m.group(1).replace(",", ".")))
            except ValueError:      # unvollständige Kote → überspringen
                continue
    if len(werte) < _MIND_KOTEN:
        return None
    mitte = median(werte)
    if mitte > _OG_AB_M:
        geschoss = "OG"         # WELCHES Obergeschoss, sagt die Kote nicht
    elif mitte < _KG_UNTER_M:
        geschoss = "KG"
    else:
        # KEIN Standardwert EG (Owner-Entscheidung 2026-09-13). Zwischen den
        # Schwellen ist die Kote KEIN Befund: der 1. Stock der Barawitzka-Serie
        # hat Median +2,88 m aus 10 Koten und wäre sonst ein ausgangsfähiges
        # Erdgeschoss. Kein Befund heißt UNBEKANNT heißt fail closed.
        return None
    return GeschossBefund(
        geschoss, "hoehenkote",
        f"Median {mitte:+.2f} m aus {len(werte)} FOK/ROK-Koten → {geschoss} "
        f"(Schwellen +{_OG_AB_M:.0f} m / {_KG_UNTER_M:.0f} m = Owner-Setzung)")
