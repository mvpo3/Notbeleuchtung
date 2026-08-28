# Elektropläne zeichnen — Zeichenmethode (Ground-Truth-Digest)

> **Quelle:** `knowledge/Elektropläne-zeichnen Wissen/Elektropläne zeichnen Skill.pdf(.docx)`
> (Leonis, ~39k Zeichen, Raum-für-Raum-Anleitung eines echten E-Plan-Zeichners).
> Maschinlesbare Fassung: `backend/ground_truth/drawing_rules_pdf.yaml`
> (Slice 2.48.3). Komplementär zu `stromkreisbeschriftung_wohnungen.md`
> (Beschriftung) und `placement_patterns_top24.yaml` (Positions-Patterns aus
> fertigen Plänen).

## Kern-Regel: Schalter-Typ folgt der Zahl der Schaltstellen

Der entscheidende, im PDF explizit formulierte Zusammenhang (adressiert direkt
den AUS/WECHSEL-Undercount im Parity-Report):

| Schaltstellen je Auslass | Symbol | Wann |
|---|---|---|
| 1 | **Ausschalter** | Raum ohne Durchgangstür zu Aufenthalts-/Schlafraum (Küche, Gang ohne SZ-Tür, Terrasse) |
| 2 | **Wechselschalter** | Tür zu Schlaf-/Wohnraum ODER Schlafzimmer (Tür + Bett) |
| 3+ | **+Kreuzschalter** | sobald >2 Wechsel für EINEN Auslass — je weitere Stelle ein Kreuz dazwischen |
| — | **Aus + Kontrolllampe** | Nassräume/Nebenräume (Bad, WC, ASR) — Licht-Zustand von außen sichtbar |

Zitat Gang-Fazit: *„Wenn im Gang eine Tür ins Schlafzimmer führt brauchen wir für
die Deckenauslässe oder Spots einen Wechselschalter, ansonsten reicht ein
Ausschalter."* — Zitat WZ: *„ab dem Moment wo du mehr als zwei Wechselschalter
für einen Deckenauslass benötigst muss man einen Kreuzschalter anhängen."*

**Referenz-Beobachtung 4OG (Pre-Read 2.48.0):** Kreuz sitzt in WOHNKÜCHE/GANG/VR,
NIE im separaten WOHNZIMMER — das offene WOHNKÜCHE-Zimmer ist der Zirkulations-Hub.

## Querschnitts-Regeln

- **Schalter-Seite:** immer Türaufgehseite (komfortable Bedienung).
- **Türleisten-Abstand:** Schalter/Thermostat 150 mm von der Türleiste (wenn
  ≥150 mm Platz), sonst an eine Wand mit min. 150 mm Platz.
- **Stack-Reihenfolge** an einer Anker-Seite: Thermostat → Schalter → Klingel →
  ATÖ → Steckdose. An gemeinsamer Stelle **zuerst Schalter, dann Steckdose**.
- **Rauchmelder:** 600 mm vom Deckenauslass, auf der **Nicht-Fensterseite**.
- **Thermostat:** nur WZ/SZ/Bad und nur bei Deckentemperierung (LB); 600 mm vom
  Heizkörper.
- **Mittelpunkt-Strategie:** Deckenauslass-/Spot-Mitte über Diagonale/Polyline-
  Halbierung des Raum-/Möbelbereichs; Spots min. 2.

## Raum-für-Raum (Zeichen-Reihenfolge)

Vorraum → Wohnzimmer → Küche → Terrasse → Schlafzimmer → Gang → Bad → WC → ASR.
Details je Raum (Licht, Schalter-Typ, Steckdosen, Geräte, Verteiler, Abstände) in
`drawing_rules_pdf.yaml → per_room_type`.

**Anwendungs-Roadmap:** Slice 2.0 = diese Daten (kein Wiring). Slice 2.1 = die
Schalter-Typ-Topologie + Positions-Patterns in den generativen Resolver hängen
(adressiert AUS-Undercount ZIMMER/WOHNZIMMER + generalisiert auf alle Floors).
Normative mm-Werte (`track_b: true`) gehören fachlich zu Track B.
