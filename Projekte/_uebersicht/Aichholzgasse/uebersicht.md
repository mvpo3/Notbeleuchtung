# Übersicht — 26_0507_AICH

**nicht auswertbar**

DXF: `C:\Users\selma\AppData\Local\Temp\claude\D--KI-Projekt\8fc32369-9bee-42cd-9e07-20d9eeb9eff5\scratchpad\zips\Aichholzgasse\26_0507_AICH.dxf`

```
Traceback (most recent call last):
  File "D:\KI Projekt\Notbeleuchtung\scripts\analyse\uebersicht_karte.py", line 529, in main
    d = karte_bauen(p, a.floor, out, a.name if a.dxf else None)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\KI Projekt\Notbeleuchtung\scripts\analyse\uebersicht_karte.py", line 456, in karte_bauen
    modell = provider.parse(str(dxf), geschoss)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\KI Projekt\Notbeleuchtung\src\notbeleuchtung\raumerkennung\provider.py", line 75, in parse
    bounds = bounds_mm(plan)
             ^^^^^^^^^^^^^^^
  File "D:\KI Projekt\Notbeleuchtung\src\notbeleuchtung\raumerkennung\dxf_load.py", line 258, in bounds_mm
    raise ValueError("Keine Wand-Entities gefunden — Layer-Muster prüfen.")
ValueError: Keine Wand-Entities gefunden — Layer-Muster prüfen.

```
