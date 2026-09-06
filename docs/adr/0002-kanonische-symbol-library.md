# ADR-0002 — Kanonische Symbol-Library = `CAD_Symbole/Notbeleuchtungssymbole.dxf`

**Status:** bindend · **Datum:** 2026-09-05 · **Owner:** Owner-Entscheidung

**Entscheidung:** NUR Blöcke aus dieser (Owner-kuratierten) Library werden
platziert; `E-Symbole.dxf` ist reine Herkunfts-Referenz. Kurations-Regel:
in-band (< 50 units). Neue Blöcke zeichnet/nimmt der Owner ab (AutoCAD) oder
gibt den Nachbau explizit frei (Beispiel: Spot 2026-09-06).

**Maschinen-Guard:** `tests/render/test_symbols_library.py`.
