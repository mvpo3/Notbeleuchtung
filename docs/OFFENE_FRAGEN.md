# Offene Fragen — Plan-Befunde & Regel-Lücken

Sammelstelle für Befunde, die eine Owner-Entscheidung brauchen. Regel-Lücken
je Raumtyp stehen maschinenlesbar in `normwissen/data/regel_deckung.yaml`
(`offen:`-Einträge, Guard `tests/naht/test_regel_deckung.py`).

## Barawitzka EG — keine expliziten Fluchtweg-Linien (2026-09)

Korrektur einer früheren Annahme: die 16 Farbe-96-Linien im Plan sind
**Katastergrenzen** (Layer »Kataster Grenzen«), keine FLW-Linien; Farbe 30 ist
ein Wand-/Bau-Layer, keine Brandabschnittslinie; kein BST/T30-Text. Brandschutz
real vorhanden: Layer »0._EG PP_2_970 Brandschutz« (Messlinien Farbe 16 mit
Distanz-Texten) + 6× »Glaswand EI30 + A2«-Texte (Layer 870).

Folgen:
- Die Soll-Erwartung »≥16 Segmente quelle LINIE« ist mit diesem Plan **nicht
  erfüllbar** — `tests/naht/test_soll_barawitzka.py` bleibt xfail und
  dokumentiert das.
- Die Quelle »explizite FLW-Linie« wird trotzdem **generisch** gebaut:
  Layer-Muster FLW/09-WEG + `materialien.yaml`-Semantik FLUCHTWEG + Farbe 96
  NUR wenn der Layername nicht Kataster/Grenze/verm enthält.

## Rennweg — Erkennungs-Lücken (2026-09)

- Lift OG3: kein X-Rechteck, nur MTEXT »AUFZUG 8 PERS. …« → Lift-Erkennung
  muss textbasiert + nächstes geschlossenes Rechteck 1.0-2.8 m funktionieren.
- Stufenlinien-Abstand OG3 gemessen 186-227 mm — Toleranz der
  Stiegen-Erkennung (150-350 mm) beachten.
- EG: Hauseingang ist KEIN Türblock in der Straßenfassade (nur
  »TÜRSCHLIESSER«-MTEXT); zweiter Plan-Cluster im selben Modelspace.

## Mollgasse — LIFT-Block (2026-09)

LIFT-Block 1.65×1.90 m mit **Achsenkreuz** (Mittellinien) statt X-Diagonalen;
Lift-Erkennung muss Achsenkreuz UND Diagonalen akzeptieren + Blockname »LIFT«.
