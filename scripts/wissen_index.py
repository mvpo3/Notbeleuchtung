"""wissen_index — deterministischer Index über den Wissens-Korpus (Skill `wissen`).

Erzeugt `knowledge/INDEX.md`: eine verlinkte Landkarte aller Wissens-Quellen (Digests,
Entscheidungen/Vokabular, Handoffs, autoritatives Norm-Wissen) — je Datei Titel + ein
Ein-Zeilen-Haken. Das ist der DETERMINISTISCHE Teil des Second-Brain: der Index wird
GENERIERT (jederzeit reproduzierbar, kein Token-Rätsel), NICHT von Hand gepflegt und
NICHT von der KI umgeschrieben. Die Quell-Dateien selbst bleibt der Generator NICHT an —
er liest nur und verlinkt (Provenienz bleibt erhalten, `norm_quelle`-DNA).

Aufruf:  python scripts/wissen_index.py         # schreibt knowledge/INDEX.md
         python scripts/wissen_index.py --check  # Exit≠0, wenn INDEX.md veraltet ist (CI)
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ZIEL = REPO / "knowledge" / "INDEX.md"

#: (Überschrift, Glob relativ zum Repo, kurze Sektions-Notiz). Reihenfolge = Ausgabe.
SEKTIONEN = [
    ("Norm-Wissen — AUTORITATIV (nur abfragen, nie umschreiben; Enis' Lane)",
     "src/notbeleuchtung/normwissen/data/**/*.yaml",
     "Single-Source-of-Truth der EN-1838/ÖNorm-Werte. Änderungen NUR über Enis + Contract."),
    ("Extrahiertes Wissen / Digests",
     "knowledge/extracted/**/*.md",
     "Produkt-/Norm-/Referenz-Digests, Wettbewerb. Prosa — KI darf verlinken/zusammenfassen."),
    ("Entscheidungen, Vokabular & Koordination (docs)",
     "docs/**/*.md",
     "ADRs, VOKABULAR, COORDINATION, OFFENE_FRAGEN, PORT_LOG — das WARUM (Begruendungen)."),
    ("Handoffs (Owner-Sessions)",
     "Handoff/**/*.md",
     "Rollen, Packages, Contracts, Slice-Stände je Owner."),
]


def _titel_und_haken(pfad: Path) -> tuple[str, str]:
    """(Titel, Ein-Zeilen-Haken) aus einer Datei — robust, ohne Inhalt zu verändern."""
    titel = pfad.stem
    haken = ""
    try:
        zeilen = pfad.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:  # noqa: BLE001 — unlesbar → nur der Dateiname
        return titel, ""
    if pfad.suffix == ".yaml":
        for z in zeilen:
            s = z.strip()
            if not s.startswith("#"):
                continue
            txt = s.lstrip("# ").strip()
            # Deko-/Trenner-Banner (═══, ---, ===) überspringen: braucht echten Text.
            if sum(c.isalpha() for c in txt) >= 4:
                haken = txt
                break
        return titel, haken
    # Markdown: erster '# '-Titel, dann erste inhaltliche Zeile als Haken.
    for z in zeilen:
        s = z.strip()
        if s.startswith("# "):
            titel = s[2:].strip()
            break
    for z in zeilen:
        s = z.strip()
        if not s or s.startswith(("#", ">", "---", "|", "```", "!", "-")):
            continue
        haken = s
        break
    return titel, haken


def _kurz(text: str, n: int = 140) -> str:
    text = " ".join(text.split())
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def baue_index(repo: Path = REPO) -> str:
    aus = [
        "# Wissens-Index (GENERIERT — nicht von Hand editieren)",
        "",
        "Landkarte des Wissens-Korpus. Regenerieren: `python scripts/wissen_index.py`.",
        "Der Index verlinkt nur; die Quell-Dateien sind die Wahrheit. **Norm-Werte niemals",
        "aus dem Index zitieren — immer der autoritativen YAML/dem Contract folgen.**",
    ]
    for titel, glob, notiz in SEKTIONEN:
        treffer = sorted(repo.glob(glob), key=lambda p: str(p).lower())
        aus += ["", f"## {titel}", f"*{notiz}*", ""]
        if not treffer:
            aus.append("_(keine Dateien gefunden)_")
            continue
        for p in treffer:
            rel = p.relative_to(repo).as_posix()
            t, h = _titel_und_haken(p)
            aus.append(f"- [{t}]({rel})" + (f" — {_kurz(h)}" if h else ""))
    return "\n".join(aus) + "\n"


def main(argv: list[str]) -> int:
    with __import__("contextlib").suppress(Exception):
        sys.stdout.reconfigure(encoding="utf-8")
    inhalt = baue_index()
    if "--check" in argv:
        alt = ZIEL.read_text(encoding="utf-8") if ZIEL.exists() else ""
        if alt != inhalt:
            print("knowledge/INDEX.md ist veraltet — `python scripts/wissen_index.py` ausführen.")
            return 1
        print("knowledge/INDEX.md aktuell.")
        return 0
    ZIEL.parent.mkdir(parents=True, exist_ok=True)
    ZIEL.write_text(inhalt, encoding="utf-8")
    n = inhalt.count("\n- ")
    print(f"knowledge/INDEX.md geschrieben ({n} Einträge).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
