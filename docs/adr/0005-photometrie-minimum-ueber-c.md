# ADR-0005 — Photometrie ohne Ausrichtungs-Zusicherung: Minimum über C

**Status:** bindend · **Datum:** 2026-09-05 (#117, Enis)

**Kontext:** Der Lux-Nachweis rechnete jede Leuchte in ihrer C0-Ebene — für die
Corridor-Optik die STÄRKSTE Richtung (γ=60°: 149,93 cd C0 vs. 19,53 cd C90);
falsch bestandene 1-lx-Nachweise (Faktor 7,7).

**Entscheidung:** Anisotrope Verteilung ohne zugesicherte physische
Optik-Ausrichtung wird konservativ mit der KLEINSTEN Lichtstärke über alle
C-Ebenen gerechnet — nie Mittelwert, nie fester C-Winkel, nie Überschätzung.
Die Rechengrundlage steht als Regel 15 im Prüfbericht.

**Guard:** `tests/platzierung/test_lux_c_ebene.py`.
