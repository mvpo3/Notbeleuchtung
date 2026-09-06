# ADR-0006 — Fluchtweg-SL: `rotation_deg` = Optik-Zusicherung aus der Korridor-Achse

**Status:** bindend · **Datum:** 2026-09-06 (#119, Leonis; adressiert Enis'
#117-Vorbehalt)

**Entscheidung:** Für Fluchtweg-Sicherheitsleuchten leitet der Verdichter den
Korridor-Achsen-Azimut ab, rechnet die C-Ebene RELATIV dazu und schreibt
DENSELBEN Azimut als `rotation_deg` — der Plan selbst ist die
Montage-/Ausrichtungs-Zusicherung (Kette: abgeleitet → gerechnet → vermerkt).
Für alle Leuchten OHNE Achsen-Azimut gilt weiter ADR-0005 (Minimum über C).

**Abgrenzung:** `rotation_deg` anderer Symbole (RZ-Pfeile etc.) bleibt reine
CAD-Symbol-Rotation und trägt KEINE Optik-Aussage.

**Guard:** `tests/platzierung/test_optik_aus_achse.py`.
