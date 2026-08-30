"""tabelle6 — reine Auswertungs-Logik für OIB-Richtlinie 2, Tabelle 6.

Kennt **keinen einzigen fachlichen Wert**: Zeilen, Schwellen, Fußnoten und
Unsicherheiten kommen als Roh-Dicts aus `data/oib_rl2_tabelle6.yaml`. Dieses
Modul entscheidet nur, WELCHE Zeile gilt und WIE die Schwellen zu lesen sind.

Die drei Härte-Regeln (Owner-Entscheidung 2026-08-30):

* **Kein Umkehrschluss** — unter der Eingangsschwelle liefert die Auswertung
  `review_required`, nie `nicht_erforderlich`.
* **Nichts raten** — ein fehlender Fakt (`None` = nicht erhoben) führt zu
  `review_required` und landet in `fehlende_fakten`.
* **Blockierende Unsicherheit schlägt Rechnen** — trägt eine Zeile eine
  `unsicherheit` mit `wirkung: blockiert`, wird die rechnerisch ermittelte
  Stufe nur als `kandidat_stufe` im Audit-Trail geführt; verbindlich ist
  `review_required`.
"""
from __future__ import annotations

from dataclasses import dataclass, field

REVIEW = "review_required"

# Schlüssel, die eine numerische Grenze aufspannen (siehe YAML-Kopf).
_GRENZ_KEYS = ("ueber", "ab", "bis")


@dataclass
class Auswertung:
    """Ergebnis der Zeilen-Auswertung für genau einen Gebäudeteil."""

    stufe: str
    zeile: dict | None = None
    kandidat_stufe: str | None = None
    angewandter_schwellenwert: str | None = None
    eingangswerte: dict[str, str] = field(default_factory=dict)
    fehlende_fakten: list[str] = field(default_factory=list)
    hinweise: list[str] = field(default_factory=list)


def wert_text(wert: object) -> str:
    """Fakt → Audit-String. `None` heißt ausdrücklich 'nicht erhoben'."""
    if wert is None:
        return "nicht erhoben"
    if isinstance(wert, bool):
        return "ja" if wert else "nein"
    if isinstance(wert, float):
        return f"{wert:g}"
    return str(wert)


def ist_zahlgrenze(grenze: object) -> bool:
    """True, wenn das Dict eine auswertbare numerische Grenze aufspannt.

    Spalten wie `{nicht_aufloesbar: …}` (Zeile 10, AStV) oder `{entfaellt: …}`
    (Zeile 11.2) sind bewusst KEINE Grenze — sie tragen nur Prosa.
    """
    return isinstance(grenze, dict) and any(k in grenze for k in _GRENZ_KEYS)


def trifft(grenze: dict, wert: float) -> bool:
    """Prüft einen Wert gegen `ueber` (>), `ab` (>=) und `bis` (<=)."""
    if "ueber" in grenze and not wert > grenze["ueber"]:
        return False
    if "ab" in grenze and not wert >= grenze["ab"]:
        return False
    return not ("bis" in grenze and not wert <= grenze["bis"])


def waehle_zeile(zeilen: list[dict], teil) -> tuple[dict | None, list[str], list[str]]:
    """Nutzungsart (+ ggf. Fluchtniveau) → die eine zutreffende Tabellenzeile.

    Rückgabe: (Zeile oder None, fehlende Fakten, Hinweise). `None` heißt: für
    diese Nutzungsart trägt Tabelle 6 keine auswertbare Zeile — der Aufrufer
    entscheidet, ob das ein Review-Fall aus `review_nutzungsarten` ist.
    """
    kandidaten = [z for z in zeilen if teil.nutzungsart in z.get("nutzungsarten", [])]
    if not kandidaten:
        return None, [], []
    if len(kandidaten) == 1 and "auswahl" not in kandidaten[0]:
        return kandidaten[0], [], []

    # Mehrere Zeilen je Nutzungsart werden ausschließlich über das Fluchtniveau
    # getrennt (Gruppe 1 ≤ 22 m vs. Gruppe 12 > 22 m).
    if teil.fluchtniveau_m is None:
        namen = ", ".join(z["zeile"] for z in kandidaten)
        return None, ["fluchtniveau_m"], [
            (
                f"Die Zeilenauswahl für diese Nutzungsart ({namen}) hängt am "
                "Fluchtniveau; ohne diesen Fakt ist nicht bestimmbar, welche "
                "Tabellenzeile gilt."
            )
        ]
    for z in kandidaten:
        grenze = z.get("auswahl", {}).get("fluchtniveau_m")
        if ist_zahlgrenze(grenze) and trifft(grenze, teil.fluchtniveau_m):
            return z, [], []
    return None, [], [
        (
            "Keine Zeile der Tabelle 6 deckt diese Kombination aus Nutzungsart "
            "und Fluchtniveau ab (kein Umkehrschluss)."
        )
    ]


def _pruefe_voraussetzungen(zeile: dict, teil, aus: Auswertung) -> bool:
    """Gebäudeklasse / Lage zur Wohnung. False = Zeile trägt hier nicht."""
    vor = zeile.get("voraussetzungen")
    if not vor:
        return True
    ok = True

    if "gebaeudeklasse_in" in vor:
        aus.eingangswerte["gebaeudeklasse"] = wert_text(teil.gebaeudeklasse)
        if teil.gebaeudeklasse is None:
            aus.fehlende_fakten.append("gebaeudeklasse")
            ok = False
        elif teil.gebaeudeklasse not in vor["gebaeudeklasse_in"]:
            aus.hinweise.append(vor["nicht_abgedeckt_text"])
            ok = False

    if "lage_zur_wohnung" in vor:
        aus.eingangswerte["lage_zur_wohnung"] = wert_text(teil.lage_zur_wohnung)
        if teil.lage_zur_wohnung is None:
            # Ohne bekannte Lage ist nicht belegt, dass der Geltungsbereich
            # "außerhalb von Wohnungen" erfüllt ist -> keine definitive Stufe.
            aus.fehlende_fakten.append("lage_zur_wohnung")
            ok = False
        elif teil.lage_zur_wohnung != vor["lage_zur_wohnung"]:
            aus.hinweise.append(vor["lage_nicht_abgedeckt_text"])
            ok = False

    return ok


def _pruefe_anwendungsschwelle(zeile: dict, teil, aus: Auswertung) -> bool:
    """Eingangsschwelle einer Zeile (z.B. 9.1 '> 60 Personen bestimmt')."""
    schwelle = zeile.get("anwendungsschwelle")
    if not schwelle:
        return True
    feld = schwelle["feld"]
    wert = getattr(teil, feld)
    aus.eingangswerte[feld] = wert_text(wert)
    if wert is None:
        aus.fehlende_fakten.append(feld)
        return False
    if not trifft(schwelle["grenze"], wert):
        aus.hinweise.append(schwelle["unterhalb_text"])
        return False
    return True


def _werte_entscheidung_aus(zeile: dict, teil, aus: Auswertung) -> str | None:
    """Feste Stufe oder Band-Auswertung → rechnerische Stufe (oder None)."""
    ents = zeile["entscheidung"]
    if ents["art"] == "fest":
        aus.angewandter_schwellenwert = ents["schwellenwert_text"]
        return ents["stufe"]

    feld = zeile["kriterium"]["feld"]
    wert = getattr(teil, feld)
    aus.eingangswerte[feld] = wert_text(wert)
    if wert is None:
        aus.fehlende_fakten.append(feld)
        return None

    texte = ents.get("schwellentexte", {})
    # Spalten, die keine numerische Grenze aufspannen, tragen nur Prosa
    # (Zeile 10 'gemäß AStV', Zeile 11.2 'nicht erforderlich') — sie werden
    # als Hinweis geführt und können nie eine Stufe auslösen.
    for spalte in ("uneingeschraenkt", "eingeschraenkt"):
        grenze = ents.get(spalte)
        if grenze is None:
            continue
        if not ist_zahlgrenze(grenze):
            for prosa in grenze.values():
                if prosa not in aus.hinweise:
                    aus.hinweise.append(prosa)
            continue
        if trifft(grenze, wert):
            aus.angewandter_schwellenwert = texte.get(spalte)
            return spalte

    unterhalb = ents.get("unterhalb")
    if unterhalb:
        aus.hinweise.append(unterhalb["text"])
    return None


def werte_zeile_aus(zeile: dict, teil) -> Auswertung:
    """Eine ausgewählte Tabellenzeile gegen einen Gebäudeteil auswerten."""
    aus = Auswertung(stufe=REVIEW, zeile=zeile)
    aus.eingangswerte["nutzungsart"] = teil.nutzungsart
    if "auswahl" in zeile:
        aus.eingangswerte["fluchtniveau_m"] = wert_text(teil.fluchtniveau_m)
    aus.hinweise.extend(zeile.get("hinweise", []))

    kandidat: str | None = None
    if _pruefe_voraussetzungen(zeile, teil, aus) and _pruefe_anwendungsschwelle(
        zeile, teil, aus
    ):
        kandidat = _werte_entscheidung_aus(zeile, teil, aus)

    # Blockierende Unsicherheit: rechnen ja, entscheiden nein.
    blockiert = [
        u for u in zeile.get("unsicherheiten", []) if u.get("wirkung") == "blockiert"
    ]
    for u in zeile.get("unsicherheiten", []):
        aus.hinweise.append(u["text"])

    if kandidat is not None and not blockiert and not aus.fehlende_fakten:
        aus.stufe = kandidat
        return aus

    aus.stufe = REVIEW
    if kandidat is not None:
        aus.kandidat_stufe = kandidat
        aus.hinweise.append(
            f"Kandidatenstufe (NICHT verbindlich, nur Audit-Information): {kandidat}."
        )
    return aus
