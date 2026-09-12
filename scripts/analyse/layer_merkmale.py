"""layer_merkmale — Merkmalstabelle je Plan/Layer, Korpus-Schreiben, ML-Smoke-Test.

Aufruf:
    python scripts/analyse/layer_merkmale.py [<dxf>…] [--korpus] [--smoke]
                                             [--out <verzeichnis>]

Ohne <dxf>: die fünf Pläne aus ``Projekte/_eingang/``,
``Projekte/EG_Grundriss_DE_NEU.dxf`` (``$INSUNITS`` 4, aber in Metern
gezeichnet) und der Fischamend-Elektroplan (Wrapper-Fall, bringt die einzigen
Nur-Modelspace-Layer mit ``massstab_verdacht``) — SIEBEN Pläne, damit Artefakt
und Bericht deckungsgleich sind. Ausgabe nach ``--out``
(Default ``Projekte/_layermerkmale``): ``merkmale.json`` + ``merkmale.md``.

Das Skript zeigt drei Dinge:
1. Was der geometrische Extraktor je Layer sieht (``layer_features``).
2. Wie der regelbasierte Entscheid gegen die HEUTIGEN namensbasierten Rollen
   steht — Treffer und Abweichungen, ohne irgendetwas umzustellen.
3. Was der Objekt-Matcher ``objekt_stiege`` findet, verglichen mit
   ``geometrie_typ.stiege_rechtecke`` (das heute nur Block-NAMEN erkennt).

``--smoke`` ist Leonis Schritt 2 und ausdrücklich NUR ein Smoke-Test
(s. ``_SMOKE_WARNUNG``). ``--korpus`` schreibt Leonis Schritt 4.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
import traceback
from collections import Counter
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.stdout.reconfigure(encoding="utf-8")

from notbeleuchtung.raumerkennung import geometrie_typ, raumlayer, tueren
from notbeleuchtung.raumerkennung.dxf_load import WALL_PATTERN, lade_dxf
from notbeleuchtung.raumerkennung.layer_features import (
    FEATURE_LAYOUT_VERSION,
    FEATURE_NAMES,
    LABEL_NAMENSREGEL,
    RollenBefund,
    klassifiziere_plan,
    schreibe_korpus,
)
from notbeleuchtung.raumerkennung.objekt_stiege import finde_stiegen

EINGANG = REPO / "Projekte" / "_eingang"
#: Zwei Pflichtfälle außerhalb von ``_eingang``: der INSUNITS-4-aber-Meter-Plan
#: und der Wrapper-Plan (nur er bringt Nur-Modelspace-Layer in den Korpus).
EXTRA = (
    REPO / "Projekte" / "EG_Grundriss_DE_NEU.dxf",
    REPO / "Projekte" / "BVH Fischamenderstraße" / "fertige Elektromontagepläne"
    / "BT1" / "Elektromontageapläne_ERDGESCHOSS BT1.dxf",
)
AUSGABE = REPO / "Projekte" / "_layermerkmale"

_SMOKE_WARNUNG = (
    "SMOKE-TEST. 7 Pläne, Test-Split = 1 Plan, Labels aus Namensregeln. "
    "Keine Schlussfolgerung — nicht über Machbarkeit, nicht über Modellwahl, "
    "nicht über Features. Schritt 5 (GBM) wird hier nicht gebaut.")

#: Tiefe des Smoke-Baums. Gesetzt (nicht gemessen) — Leonis Vorgabe „Tiefe 3".
_BAUM_TIEFE = 3

#: Tür-Schwenkbogen-Radius ≈ Blattbreite (wie dxf_load._DOOR_MIN/_MAX_MM).
_BOGEN_MIN_MM, _BOGEN_MAX_MM = 600.0, 1300.0


# ── Label-Quelle ─────────────────────────────────────────────────────────────
def label_aus_namensregel(layer: str, bogen_radien: list[float]) -> str:
    """Rolle aus den HEUTIGEN Namensregeln des Repos.

    Nur das LABEL kommt vom Namen. Der Merkmalsvektor sieht keinen Namen —
    sonst ist das Ergebnis zirkulär.

    Quellen: ``dxf_load.WALL_PATTERN`` · ``raumlayer._ROOM_LAYER`` /
    ``_HATCH_ROOM_LAYER`` (ohne ``_ROOM_LAYER_EXCLUDE``) ·
    ``tueren._DOOR_HINT`` / ``_AUSSENTUER`` minus ``_DOOR_EXCLUDE``, plus
    Layer mit Bogenradien in Tür-Blattbreite. Reihenfolge = Vorrang.
    """
    if WALL_PATTERN.search(layer):
        return "wand"
    if ((raumlayer._ROOM_LAYER.search(layer)
         or raumlayer._HATCH_ROOM_LAYER.search(layer))
            and not raumlayer._ROOM_LAYER_EXCLUDE.search(layer)):
        return "raumkontur"
    if ((tueren._DOOR_HINT.search(layer) or tueren._AUSSENTUER.search(layer))
            and not tueren._DOOR_EXCLUDE.search(layer)):
        return "oeffnung"
    if any(_BOGEN_MIN_MM <= r <= _BOGEN_MAX_MM for r in bogen_radien):
        return "oeffnung"
    return "rest"


def _bogen_radien(plan) -> dict[str, list[float]]:
    """ARC-/CIRCLE-Radien in mm je Layer (Modelspace + Blöcke, Tiefe ≤3)."""
    out: dict[str, list[float]] = {}

    def walk(entities, tiefe: int = 0) -> None:
        for e in entities:
            t = e.dxftype()
            if t in ("ARC", "CIRCLE"):
                r = float(getattr(e.dxf, "radius", 0.0) or 0.0) * plan.factor
                if r > 0:
                    out.setdefault(str(e.dxf.layer), []).append(r)
            elif t == "INSERT" and tiefe < 3:
                try:
                    walk(e.virtual_entities(), tiefe + 1)
                except Exception:  # noqa: BLE001, S112
                    continue

    walk(plan.space)
    return out


# ── Auswertung je Plan ───────────────────────────────────────────────────────
def _zeile(b: RollenBefund, label: str) -> dict:
    m = b.merkmale
    return {
        "layer_name": m.layer_name, "quelle": m.quelle, "n_entities": m.n_entities,
        "n_punkte": m.n_punkte, "rolle": b.rolle, "confidence": b.confidence,
        "modus": b.modus, "label_namensregel": label,
        "treffer": b.rolle == label,
        "massstab_verdacht": m.massstab_verdacht,
        "variante_verdacht": m.variante_verdacht,
        "runde2_belegt": m.runde2_belegt,
        "faktor_plausibel": m.faktor_plausibel,
        "scores": b.scores,
        "begruendung": b.begruendung,
        "features": dict(zip(FEATURE_NAMES, m.to_vector(), strict=True)),
    }


def auswerte_plan(pfad: Path) -> tuple[dict, list[RollenBefund]]:
    """(Tabellen-Daten, Befunde) — die Befunde gehen unverändert in den Korpus.

    Ein zweiter ``klassifiziere_plan``-Lauf für ``--korpus`` wäre der teuerste
    Teil doppelt und könnte auseinanderlaufen; Artefakt und Korpus kommen
    deshalb aus DEMSELBEN Lauf.
    """
    t0 = time.time()
    plan = lade_dxf(pfad)
    t_laden = time.time() - t0
    t0 = time.time()
    befunde = klassifiziere_plan(plan, pfad.stem)
    t_klass = time.time() - t0
    radien = _bogen_radien(plan)
    zeilen = [_zeile(b, label_aus_namensregel(b.layer_name,
                                              radien.get(b.layer_name, [])))
              for b in befunde]
    t0 = time.time()
    stiegen = finde_stiegen(plan)
    t_stiege = time.time() - t0
    alt = geometrie_typ.stiege_rechtecke(plan)
    return {
        "plan": pfad.stem, "dxf": str(pfad), "factor": plan.factor,
        "insunits": int(plan.doc.header.get("$INSUNITS", 0) or 0),
        "wrapper": plan.space is not plan.doc.modelspace(),
        "layout_version": FEATURE_LAYOUT_VERSION,
        "sekunden": {"laden": round(t_laden, 1), "klassifizieren": round(t_klass, 1),
                     "stiege": round(t_stiege, 1)},
        "layer": zeilen,
        "zusammenfassung": {
            "layer_gesamt": len(zeilen),
            "je_rolle": dict(Counter(z["rolle"] for z in zeilen)),
            "je_modus": dict(Counter(z["modus"] for z in zeilen)),
            "je_label_namensregel": dict(Counter(z["label_namensregel"]
                                                 for z in zeilen)),
            "treffer": sum(1 for z in zeilen if z["treffer"]),
            "abweichungen": sum(1 for z in zeilen if not z["treffer"]),
            "massstab_verdacht": sum(1 for z in zeilen if z["massstab_verdacht"]),
            "variante_verdacht": sum(1 for z in zeilen if z["variante_verdacht"]),
            "runde2_belegt": sum(1 for z in zeilen if z["runde2_belegt"]),
        },
        "stiege": {
            "kandidaten": [
                {"layer_name": k.layer_name, "quelle": k.quelle,
                 "n_stufen": k.n_stufen, "teilung_mm": k.teilung_mm,
                 "konsistenz": k.konsistenz, "laufrichtung": k.laufrichtung,
                 "winkel_grad": k.winkel_grad, "flaeche_m2": k.flaeche_m2,
                 "confidence": k.confidence} for k in stiegen],
            "heute_stiege_rechtecke": len(alt),
        },
    }, befunde


# ── Markdown ─────────────────────────────────────────────────────────────────
def _md(daten: list[dict]) -> str:
    kopf = (f"Layout-Version `{FEATURE_LAYOUT_VERSION}`. Der Merkmalsvektor sieht "
            "KEINEN Layernamen; die Spalte `Label (Name)` kommt aus den heutigen "
            "Namensregeln und dient nur dem Vergleich.")
    z = ["# Layer-Merkmale und regelbasierte Rollen", "", kopf, ""]
    for d in daten:
        if "fehler" in d:
            z += [f"## {d['plan']}", "", f"FEHLER: `{d['fehler']}`", ""]
            continue
        s = d["zusammenfassung"]
        spalten = ("| Layer | Quelle | n | Rolle | Conf | Modus | Label (Name) "
                   "| par | hatch | hs | geschl | bogen | naehe | diag_mm |")
        z += [f"## {d['plan']}", "",
              (f"- Faktor **{d['factor']}** (`$INSUNITS` {d['insunits']}), "
               f"Wrapper-Plan: {d['wrapper']}"),
              f"- Layer: **{s['layer_gesamt']}**, Rollen: {s['je_rolle']}",
              f"- Modus: {s['je_modus']}",
              f"- Namensregel-Label: {s['je_label_namensregel']}",
              (f"- Übereinstimmung Regel vs. Name: **{s['treffer']}** von "
               f"{s['layer_gesamt']}, Abweichungen {s['abweichungen']}"),
              (f"- massstab_verdacht {s['massstab_verdacht']}, "
               f"variante_verdacht {s['variante_verdacht']}, "
               f"runde2_belegt {s['runde2_belegt']}"),
              f"- Laufzeit {d['sekunden']}", "", spalten,
              "|---|---|--:|---|--:|---|---|--:|--:|--:|--:|--:|--:|--:|"]
        for r in sorted(d["layer"], key=lambda x: -x["confidence"]):
            f = r["features"]
            marke = "" if r["treffer"] else " ⚠"
            z.append(
                f"| `{r['layer_name']}` | {r['quelle']} | {r['n_entities']} | "
                f"{r['rolle']} | {r['confidence']:.2f} | {r['modus']} | "
                f"{r['label_namensregel']}{marke} | {f['parallel_quote']:.2f} | "
                f"{f['anteil_hatch']:.2f} | {f['hatch_schmal_quote']:.2f} | "
                f"{f['anteil_geschlossen']:.2f} | {f['anteil_bogen']:.2f} | "
                f"{f['wand_naehe_quote']:.2f} | {f['layer_diag_mm']:.0f} |")
        st = d["stiege"]
        titel = (f"### Stiegen-Kandidaten ({len(st['kandidaten'])}) — heute über "
                 f"Blocknamen: {st['heute_stiege_rechtecke']} Rechtecke")
        z += ["", titel, ""]
        if st["kandidaten"]:
            z += [("| Layer | Quelle | Stufen | Teilung mm | Konsistenz | "
                   "Richtung | Winkel | m² | Conf |"),
                  "|---|---|--:|--:|--:|---|--:|--:|--:|"]
            for k in st["kandidaten"]:
                z.append(f"| `{k['layer_name']}` | {k['quelle']} | "
                         f"{k['n_stufen']} | {k['teilung_mm']} | "
                         f"{k['konsistenz']} | {k['laufrichtung']} | "
                         f"{k['winkel_grad']} | {k['flaeche_m2']} | "
                         f"{k['confidence']} |")
        z.append("")
    return "\n".join(z)


# ── Smoke-Test (Leonis Schritt 2) ────────────────────────────────────────────
def _codes(y: list[str]) -> tuple[np.ndarray, list[str]]:
    """Labels → Integer-Codes + sortierte Klassenliste (deterministisch)."""
    klassen = sorted(set(y))
    return np.array([klassen.index(v) for v in y], dtype=np.int64), klassen


def _bester_split(x: np.ndarray, y: np.ndarray, k: int) -> tuple[int, float] | None:
    """Bester Gini-Split ``(Feature-Index, Schwelle)`` — oder None (rein/zu klein).

    Kandidaten sind die Mittelpunkte benachbarter BEOBACHTETER Werte je Feature.
    Tie-Break: kleinster Feature-Index, dann kleinste Schwelle. Keine
    Zufallskomponente — dieselbe Eingabe gibt denselben Baum.
    """
    n = len(y)
    if n < 2 or len(np.unique(y)) < 2:
        return None
    eins = np.eye(k, dtype=np.int64)
    bestes: tuple[float, int, float] | None = None
    for j in range(x.shape[1]):
        ordnung = np.argsort(x[:, j], kind="stable")
        xs = x[ordnung, j]
        heiss = eins[y[ordnung]]
        links = np.cumsum(heiss, axis=0)[:-1]          # Schnitt NACH Position i
        rechts = heiss.sum(axis=0) - links
        nl = links.sum(axis=1).astype(float)
        nr = n - nl
        guete = (nl * (1.0 - (links ** 2).sum(axis=1) / nl ** 2)
                 + nr * (1.0 - (rechts ** 2).sum(axis=1) / nr ** 2)) / n
        guete[xs[:-1] >= xs[1:]] = np.inf              # nicht zwischen Gleichwerten
        i = int(np.argmin(guete))
        if np.isfinite(guete[i]) and (bestes is None or guete[i] < bestes[0]):
            bestes = (float(guete[i]), j, float((xs[i] + xs[i + 1]) / 2))
    return (bestes[1], bestes[2]) if bestes is not None else None


def _baum(x: np.ndarray, y: np.ndarray, k: int, tiefe: int) -> dict:
    """CART-Knoten: Blatt ``{"klasse": code}`` oder Split ``{"j","s","l","r"}``.

    Blatt-Tie-Break über ``bincount().argmax()`` = kleinster Klassencode =
    alphabetisch erste Klasse.
    """
    blatt = {"klasse": int(np.bincount(y, minlength=k).argmax())}
    if tiefe <= 0:
        return blatt
    s = _bester_split(x, y, k)
    if s is None:
        return blatt
    j, schwelle = s
    m = x[:, j] <= schwelle
    return {"j": j, "s": schwelle, "l": _baum(x[m], y[m], k, tiefe - 1),
            "r": _baum(x[~m], y[~m], k, tiefe - 1)}


def _vorhersage(knoten: dict, zeile: np.ndarray) -> int:
    while "klasse" not in knoten:
        knoten = knoten["l"] if zeile[knoten["j"]] <= knoten["s"] else knoten["r"]
    return int(knoten["klasse"])


def _regeltext(knoten: dict, klassen: list[str], tiefe: int = 0) -> list[str]:
    """Baum als Text (Ersatz für ``sklearn.tree.export_text``)."""
    if "klasse" in knoten:
        return [f"{'|   ' * tiefe}--> {klassen[knoten['klasse']]}"]
    f = FEATURE_NAMES[knoten["j"]]
    return [f"{'|   ' * tiefe}{f} <= {knoten['s']:.6g}",
            *_regeltext(knoten["l"], klassen, tiefe + 1),
            f"{'|   ' * tiefe}{f} >  {knoten['s']:.6g}",
            *_regeltext(knoten["r"], klassen, tiefe + 1)]


def _accuracy(wahr: list[str], vorher: list[str]) -> float:
    return (round(sum(1 for a, b in zip(wahr, vorher, strict=True) if a == b)
                  / len(wahr), 4) if wahr else 0.0)


def _f1_je_klasse(wahr: list[str], vorher: list[str],
                  klassen: list[str]) -> dict[str, float]:
    """F1 je Klasse, ohne sklearn — F1 = 0 wenn es keinen Treffer gibt."""
    paare = list(zip(wahr, vorher, strict=True))
    out: dict[str, float] = {}
    for kl in klassen:
        tp = sum(1 for a, b in paare if a == kl and b == kl)
        fp = sum(1 for a, b in paare if a != kl and b == kl)
        fn = sum(1 for a, b in paare if a == kl and b != kl)
        out[kl] = round(2 * tp / (2 * tp + fp + fn), 4) if tp else 0.0
    return out


def smoke(daten: list[dict]) -> dict:
    """Leave-one-plan-out mit EIGENER CART (Tiefe 3, Gini) — abhängigkeitsfrei.

    Das ist der Smoke-STANDARD: scikit-learn ist hier nicht installiert, und ein
    stillschweigend übersprungener Smoke-Test ist kein Smoke-Test. Die
    Mehrheitsklassen-Baseline läuft PFLICHT daneben — ein Baum, der „immer
    Mehrheitsklasse" nicht schlägt, hat nichts gezeigt. Deterministisch: keine
    Zufallskomponente, Tie-Breaks über Feature-Index, Schwelle und Klassencode.
    ``--smoke-sklearn`` fährt zusätzlich ``smoke_sklearn`` (optional).

    Ausdrücklich ein Smoke-Test (``_SMOKE_WARNUNG``) — keine Schlüsse.
    """
    print(f"\n=== SMOKE-TEST (Schritt 2, abhängigkeitsfrei) ===\n{_SMOKE_WARNUNG}")
    zeilen = [(d["plan"], r) for d in daten if "layer" in d for r in d["layer"]]
    plaene = sorted({p for p, _ in zeilen})
    if len(plaene) < 2:
        print("weniger als zwei Pläne — kein leave-one-plan-out möglich")
        return {"uebersprungen": "zu wenige Pläne"}
    x = np.array([[float(v) for v in r["features"].values()] for _, r in zeilen])
    y_text = [r["label_namensregel"] for _, r in zeilen]
    gruppe = [p for p, _ in zeilen]
    y, klassen = _codes(y_text)

    folds: list[dict] = []
    wahr: list[str] = []
    vorher: list[str] = []
    mehrheit: list[str] = []
    for nr, plan in enumerate(plaene, start=1):
        te = [i for i, p in enumerate(gruppe) if p == plan]
        tr = [i for i, p in enumerate(gruppe) if p != plan]
        if not te or not tr:
            continue
        baum = _baum(x[tr], y[tr], len(klassen), _BAUM_TIEFE)
        p_fold = [klassen[_vorhersage(baum, x[i])] for i in te]
        w_fold = [y_text[i] for i in te]
        haeufig = Counter(y_text[i] for i in tr)
        top = min(haeufig, key=lambda kl: (-haeufig[kl], kl))
        folds.append({
            "fold": nr, "testplan": [plan], "n_test": len(te),
            "accuracy": _accuracy(w_fold, p_fold),
            "macro_f1": round(sum(_f1_je_klasse(w_fold, p_fold, klassen).values())
                              / len(klassen), 4),
            "mehrheitsklasse": top,
            "accuracy_mehrheitsklasse": _accuracy(w_fold, [top] * len(te)),
            "support": dict(Counter(w_fold)),
        })
        wahr += w_fold
        vorher += p_fold
        mehrheit += [top] * len(te)

    gesehen = sorted(set(wahr) | set(vorher))
    pos = {kl: i for i, kl in enumerate(gesehen)}
    cm = [[0] * len(gesehen) for _ in gesehen]
    for a, b in zip(wahr, vorher, strict=True):
        cm[pos[a]][pos[b]] += 1
    f1 = _f1_je_klasse(wahr, vorher, klassen)
    baum_alle = _baum(x, y, len(klassen), _BAUM_TIEFE)
    erg = {
        "warnung": _SMOKE_WARNUNG,
        "implementierung": (f"eigene CART, Tiefe {_BAUM_TIEFE}, Gini, "
                            "leave-one-plan-out, ohne scikit-learn"),
        "n_zeilen": len(y_text), "n_plaene": len(plaene),
        "klassen_gesamt": dict(Counter(y_text)), "folds": folds,
        "accuracy_gesamt": _accuracy(wahr, vorher),
        "macro_f1_gesamt": round(sum(f1.values()) / len(klassen), 4),
        "f1_je_klasse": f1,
        "accuracy_mehrheitsklasse_gesamt": _accuracy(wahr, mehrheit),
        "konfusion_labels": gesehen, "konfusion": cm,
        "regeln_auf_allen_daten": "\n".join(_regeltext(baum_alle, klassen)),
        "varianten_zeilen": sum(1 for _, r in zeilen if r["variante_verdacht"]),
    }
    for f in folds:
        print(f"  Fold {f['fold']} Test={f['testplan']} n={f['n_test']:4d} "
              f"acc={f['accuracy']:.3f} macroF1={f['macro_f1']:.3f} "
              f"Mehrheit({f['mehrheitsklasse']})={f['accuracy_mehrheitsklasse']:.3f} "
              f"support={f['support']}")
    print(f"  gesamt acc={erg['accuracy_gesamt']:.3f} "
          f"macroF1={erg['macro_f1_gesamt']:.3f} "
          f"Mehrheitsklassen-Baseline={erg['accuracy_mehrheitsklasse_gesamt']:.3f}")
    print(f"  F1 je Klasse: {f1}")
    print(f"  Konfusion (Zeilen=wahr, Spalten=vorhergesagt) {gesehen}:")
    for name, row in zip(gesehen, cm, strict=True):
        print(f"    {name:11s} {row}")
    print(f"  als Variante markierte Zeilen: {erg['varianten_zeilen']}")
    return erg


def smoke_sklearn(daten: list[dict]) -> dict:
    """Optionaler Zweitpfad: DecisionTree(max_depth=3), GroupKFold LOPO.

    Nur zum Abgleich mit ``smoke``. Ohne scikit-learn wird übersprungen,
    Exit-Code bleibt 0 — deshalb ist DIESER Pfad nicht der Standard.
    """
    print(f"\n=== SMOKE-TEST (Schritt 2) ===\n{_SMOKE_WARNUNG}")
    try:
        from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
        from sklearn.model_selection import GroupKFold
        from sklearn.tree import DecisionTreeClassifier, export_text
    except ImportError:
        zeile = ("SMOKE-TEST uebersprungen: scikit-learn nicht installiert "
                 "(pip install -e .[layerml])")
        print(zeile)
        return {"uebersprungen": zeile}

    x = [[f for f in r["features"].values()] for d in daten if "layer" in d
         for r in d["layer"]]
    y = [r["label_namensregel"] for d in daten if "layer" in d for r in d["layer"]]
    g = [d["plan"] for d in daten if "layer" in d for _ in d["layer"]]
    plaene = sorted(set(g))
    if len(plaene) < 2:
        print("weniger als zwei Pläne — kein leave-one-plan-out möglich")
        return {"uebersprungen": "zu wenige Pläne"}

    folds, wahr, vorher, mehrheit = [], [], [], []
    gkf = GroupKFold(n_splits=len(plaene))
    for nr, (tr, te) in enumerate(gkf.split(x, y, groups=g), start=1):
        baum = DecisionTreeClassifier(max_depth=3, random_state=0)
        baum.fit([x[i] for i in tr], [y[i] for i in tr])
        p = list(baum.predict([x[i] for i in te]))
        yt = [y[i] for i in te]
        top = Counter(y[i] for i in tr).most_common(1)[0][0]
        folds.append({
            "fold": nr, "testplan": sorted({g[i] for i in te}),
            "n_test": len(te),
            "accuracy": round(accuracy_score(yt, p), 4),
            "macro_f1": round(f1_score(yt, p, average="macro", zero_division=0), 4),
            "mehrheitsklasse": top,
            "accuracy_mehrheitsklasse": round(
                accuracy_score(yt, [top] * len(yt)), 4),
            "support": dict(Counter(yt)),
        })
        wahr += yt
        vorher += p
        mehrheit += [top] * len(yt)

    klassen = sorted(set(wahr) | set(vorher))
    cm = confusion_matrix(wahr, vorher, labels=klassen).tolist()
    baum = DecisionTreeClassifier(max_depth=3, random_state=0).fit(x, y)
    regeln = export_text(baum, feature_names=list(FEATURE_NAMES))
    erg = {
        "warnung": _SMOKE_WARNUNG, "n_zeilen": len(y), "n_plaene": len(plaene),
        "klassen_gesamt": dict(Counter(y)), "folds": folds,
        "accuracy_gesamt": round(accuracy_score(wahr, vorher), 4),
        "macro_f1_gesamt": round(f1_score(wahr, vorher, average="macro",
                                          zero_division=0), 4),
        "accuracy_mehrheitsklasse_gesamt": round(
            accuracy_score(wahr, mehrheit), 4),
        "konfusion_labels": klassen, "konfusion": cm,
        "regeln_auf_allen_daten": regeln,
        "varianten_zeilen": sum(1 for d in daten if "layer" in d
                                for r in d["layer"] if r["variante_verdacht"]),
    }
    for f in folds:
        print(f"  Fold {f['fold']} Test={f['testplan']} n={f['n_test']:4d} "
              f"acc={f['accuracy']:.3f} macroF1={f['macro_f1']:.3f} "
              f"Mehrheit({f['mehrheitsklasse']})={f['accuracy_mehrheitsklasse']:.3f} "
              f"support={f['support']}")
    print(f"  gesamt acc={erg['accuracy_gesamt']:.3f} "
          f"macroF1={erg['macro_f1_gesamt']:.3f} "
          f"Mehrheitsklassen-Baseline={erg['accuracy_mehrheitsklasse_gesamt']:.3f}")
    print(f"  Konfusion (Zeilen=wahr, Spalten=vorhergesagt) {klassen}:")
    for name, row in zip(klassen, cm, strict=True):
        print(f"    {name:11s} {row}")
    print(f"  als Variante markierte Zeilen: {erg['varianten_zeilen']}")
    return erg


# ── main ─────────────────────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dxf", nargs="*", help="DXF-Dateien; ohne = _eingang + EG_Grundriss")
    ap.add_argument("--korpus", action="store_true",
                    help="Korpuszeilen nach corpus/layer_labels.* schreiben")
    ap.add_argument("--smoke", action="store_true",
                    help="eigene CART Tiefe 3, leave-one-plan-out (SMOKE-TEST)")
    ap.add_argument("--smoke-sklearn", action="store_true",
                    help="zusätzlich der sklearn-Pfad (skippt ohne scikit-learn)")
    ap.add_argument("--out", default=str(AUSGABE))
    a = ap.parse_args()

    pfade = [Path(p) for p in a.dxf] if a.dxf else [
        *sorted(EINGANG.glob("*.dxf")), *(p for p in EXTRA if p.exists())]
    ziel = Path(a.out)
    ziel.mkdir(parents=True, exist_ok=True)

    daten: list[dict] = []
    befunde_alle: list[RollenBefund] = []
    for p in pfade:
        print(f"\n=== {p.stem} ===", flush=True)
        if not p.exists():
            print(f"  fehlt: {p}")
            daten.append({"plan": p.stem, "dxf": str(p), "fehler": "Datei fehlt"})
            continue
        try:
            d, befunde = auswerte_plan(p)
        except Exception as e:  # noqa: BLE001 — ein kaputter Plan stoppt den Lauf nicht
            traceback.print_exc()
            daten.append({"plan": p.stem, "dxf": str(p), "fehler": repr(e)})
            continue
        daten.append(d)
        befunde_alle += befunde
        s = d["zusammenfassung"]
        print(f"  factor={d['factor']} insunits={d['insunits']} "
              f"wrapper={d['wrapper']} layer={s['layer_gesamt']} {d['sekunden']}")
        print(f"  rollen={s['je_rolle']}")
        print(f"  modus ={s['je_modus']}")
        print(f"  namensregel={s['je_label_namensregel']} "
              f"treffer={s['treffer']} abweichungen={s['abweichungen']}")
        print(f"  massstab_verdacht={s['massstab_verdacht']} "
              f"variante_verdacht={s['variante_verdacht']} "
              f"runde2_belegt={s['runde2_belegt']}")
        print(f"  stiegen={len(d['stiege']['kandidaten'])} "
              f"(heute über Blocknamen: {d['stiege']['heute_stiege_rechtecke']})")

    ergebnis: dict = {"layout_version": FEATURE_LAYOUT_VERSION, "plaene": daten}
    if a.smoke:
        ergebnis["smoke"] = smoke(daten)
    if a.smoke_sklearn:
        ergebnis["smoke_sklearn"] = smoke_sklearn(daten)
    if a.korpus:
        # Dieselben Befunde wie die Tabelle (s. auswerte_plan) — nicht neu rechnen.
        pfad = schreibe_korpus(befunde_alle, LABEL_NAMENSREGEL,
                               ordner=REPO / "corpus")
        n = len(pfad.read_text(encoding="utf-8").splitlines()) if (
            pfad.suffix == ".jsonl") else math.nan
        ergebnis["korpus"] = {"datei": str(pfad), "zeilen": n,
                              "layout_version": FEATURE_LAYOUT_VERSION,
                              "label_quelle": LABEL_NAMENSREGEL}
        print(f"\nKorpus: {pfad} ({n} Zeilen, label_quelle={LABEL_NAMENSREGEL})")

    (ziel / "merkmale.json").write_text(
        json.dumps(ergebnis, ensure_ascii=False, indent=2), encoding="utf-8")
    (ziel / "merkmale.md").write_text(_md(daten), encoding="utf-8")
    print(f"\ngeschrieben: {ziel / 'merkmale.json'} · {ziel / 'merkmale.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
