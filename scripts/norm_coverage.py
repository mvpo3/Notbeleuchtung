"""norm_coverage — macht sichtbar, ob die Engine das Norm-Wissen wirklich konsumiert.

Der Owner-Auftrag: „die Hauptengine muss das Wissen (v.a. Enis' Norm-Wissen) immer
abrufen — daraus entstehen die Pläne." Diese Prüfung zeigt je erzeugtem Plan, WORAUF
jede Platzierung fußt:

- **norm** — `norm_quelle ∈ NormRegelwerk.quellen`: von Enis' `normwissen/data`-YAML
  begründet (das Wissen HAT die Engine erreicht). ✓
- **praxis** — Owner-Referenz-Praxis (`fachpraxis:` / `Referenz-Praxis`): legitime
  Nicht-Norm-Entscheidung.
- **unbegruendet** — leere/unbekannte `norm_quelle`: die Leuchte fußt auf KEINEM
  aufgezeichneten Wissen (Lücke/Bug — roter Alarm).

So SIEHT man, wenn ein Wert fehlt und die Engine still auf einen Default zurückfällt,
statt Enis' Wissen zu nutzen. Rein contract-basiert (liest `Platzierung.norm_quelle`),
kein Nachrechnen von Norm-Werten (Owner-Grenze).

Aufruf:  python scripts/norm_coverage.py "<plan.dxf>" "<floor>"   # rendert + berichtet
Funktion: `norm_deckung(platzierungen, quellen) -> Bericht`  (rein, für die Skill/Tests)
"""
from __future__ import annotations

import contextlib
import sys
from dataclasses import dataclass, field

#: Präfixe der Owner-Referenz-Praxis (bewusst NICHT Norm). Wertgleich zu den
#: `QUELLE_*`-Konstanten in platzierung/fachpraxis.py, aber lokal gehalten.
_PRAXIS_PREFIXE = ("fachpraxis:", "Referenz-Praxis")


@dataclass
class Bericht:
    gesamt: int = 0
    norm: int = 0
    praxis: int = 0
    unbegruendet: int = 0
    unbegruendet_liste: list = field(default_factory=list)   # (kind, catalog_key)
    je_kind: dict = field(default_factory=dict)              # kind → {norm, praxis, unbegruendet}

    @property
    def norm_pct(self) -> float:
        return 100.0 * self.norm / self.gesamt if self.gesamt else 0.0

    @property
    def gesund(self) -> bool:
        # Jede Leuchte muss von Norm ODER expliziter Praxis begründet sein — nie „nichts".
        return self.gesamt > 0 and self.unbegruendet == 0


def _klasse(norm_quelle: str, quellen: set[str]) -> str:
    q = (norm_quelle or "").strip()
    if q and q in quellen:
        return "norm"
    if q.startswith(_PRAXIS_PREFIXE):
        return "praxis"
    return "unbegruendet"


def norm_deckung(platzierungen, quellen) -> Bericht:
    """Klassifiziert jede Platzierung nach der Herkunft ihrer `norm_quelle`.

    `platzierungen` = Iterable mit `.norm_quelle`, `.kind`, `.catalog_key`.
    `quellen` = die autoritativen Norm-Quellen-Strings (`regelwerk_snapshot().quellen`)."""
    quellen = set(quellen)
    b = Bericht()
    for p in platzierungen:
        b.gesamt += 1
        k = _klasse(getattr(p, "norm_quelle", ""), quellen)
        setattr(b, k, getattr(b, k) + 1)
        kind = getattr(p, "kind", "?")
        eintrag = b.je_kind.setdefault(kind, {"norm": 0, "praxis": 0, "unbegruendet": 0})
        eintrag[k] += 1
        if k == "unbegruendet":
            b.unbegruendet_liste.append((kind, getattr(p, "catalog_key", "?")))
    return b


def report(b: Bericht, titel: str = "") -> str:
    kopf = f"NORM-COVERAGE {titel}".rstrip()
    z = [
        kopf,
        f"  Platzierungen: {b.gesamt}",
        f"  norm-gesourct (Enis' YAML): {b.norm} ({b.norm_pct:.0f}%)",
        f"  Referenz-Praxis (Owner):    {b.praxis}",
        f"  UNBEGRÜNDET:                {b.unbegruendet}",
    ]
    for kind, d in sorted(b.je_kind.items()):
        z.append(f"    {kind}: norm {d['norm']} · praxis {d['praxis']} · unbegruendet {d['unbegruendet']}")
    if b.unbegruendet:
        beispiele = ", ".join(f"{k}/{ck}" for k, ck in b.unbegruendet_liste[:8])
        z.append(f"  VERDIKT: NO-GO — {b.unbegruendet} Platzierung(en) ohne Wissens-Beleg: {beispiele}")
        z.append("  -> fehlt der Norm-Wert (Enis' YAML) oder greift eine Default-Fallback-Regel?")
    else:
        z.append("  VERDIKT: GO — jede Leuchte ist norm- oder praxis-begründet (Wissen konsumiert).")
    return "\n".join(z)


def main(argv: list[str]) -> int:
    with contextlib.suppress(Exception):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(argv) < 2:
        print('usage: python scripts/norm_coverage.py "<plan.dxf>" "<floor>"')
        return 2
    dxf, floor = argv[0], argv[1]
    from notbeleuchtung.hauptengine.pipeline import run
    from notbeleuchtung.hauptengine.registry import build_default_bundle
    bundle = build_default_bundle()
    erg = run(bundle, dxf, floor)
    quellen = bundle.norm.regelwerk_snapshot().quellen
    b = norm_deckung(erg.platzierung.platzierungen, quellen)
    print(report(b, f"{dxf} [{floor}]"))
    return 0 if b.gesund else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
