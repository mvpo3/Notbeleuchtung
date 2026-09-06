# Vokabular — kanonische Begriffe der 3-Owner-Naht

Antwort auf die offene COORDINATION-Frage *„Wo ist die Liste kanonisch?"*:
**hier** — mit der Maschine als Quelle. Dieses Dokument benennt, die Tests
erzwingen; driftet Code gegen dieses Dokument, bricht
`tests/contract/test_vokabular_doku.py`.

## 1. Raumtypen (Kanon)

**Maschinen-Quelle:** `raumerkennung/raumtyp.py` (`_TYP_MAP` + `_EXTRA_DIRECT`,
Owner Selman). Enis' LB-Stützliste (`normwissen/data/lb_extraktion.yaml`) ist
beidseitig dagegen geguardet (`tests/contract/test_lb_raumtyp_naht.py`) —
NIEMALS eine der Listen allein ändern.

| Raumtyp | Notlicht-Konsum (Leonis) |
|---|---|
| ABSTELLRAUM | LB-adressierbar |
| BAD | Sanitär-Flächen-Trigger (OVE, OIB-gegated) |
| BALKON | — |
| GANG | **Fluchtweg-Korridor**: Mittellinien-Verdichtung + RZ-GANG-Fallback |
| GARAGE | LB-adressierbar (`notlicht_kw_garage`) |
| KELLER | LB-adressierbar |
| KINDERZIMMER | — |
| KÜCHE | — |
| LAGER | LB-adressierbar |
| LIFT | — (Pflicht-POI „Aufzugsflur" = offener Track C) |
| MUELLRAUM | LB-adressierbar |
| SCHLAFZIMMER | — |
| STIEGENHAUS | Fluchtweg + communal; Ausgangs-Anker; **Nachweis-Lücke offen** (Enis-Punkt 5) |
| TECHNIK | LB-adressierbar; Anlagen-Symbol-Standort |
| TERRASSE | — |
| VORRAUM | — |
| WC | Sanitär-Flächen-Trigger |
| WOHNZIMMER | — |
| ZIMMER | — |

**Defensiv akzeptierte Synonyme** (Leonis konsumiert sie, Selman vergibt sie
heute NICHT — Quelle `platzierung/bausteine.py`): `FLUR`, `KORRIDOR` (wie GANG)
· `SANITAER`, `SANITÄR`, `DUSCHE`, `NASSRAUM` (wie WC/BAD). Vergibt die
Erkennung eines Tages solche Labels, wirken sie sofort; neu vergebene Typen
außerhalb des Kanons brechen bewusst den LB-Naht-Guard.

Leerer `raum_typ` = **untypisiert** (kein Raumtyp „UNBEKANNT" im Contract);
Coverage-Warnung im Summary, Leuchten-Arten nicht ableitbar.

## 2. Naht-Begriffe (Glossar)

- **Rolle ≠ Produkt** — RZ/SL/Antipanik sind NORM-Rollen; das Produkt kann
  dasselbe sein (din nutzt die Antipanikleuchte AP3 universal, mit
  Pikto-Scheibe wird sie zum RZ). Lux zählt die PRODUKT-Optik, Stückliste das
  Produkt, Prüfbericht die Rolle.
- **Kaskade L/H/F/R** — Selmans Raum-Polygonquellen in Prioritätsfolge:
  **L**ayer-Polygone → Raum-**H**ATCHes → Stempel-**F**lutung →
  **R**est-Komponenten. `flutung_unsicher` = Flutung brach aus (Fläche weicht
  stark vom Stempel ab).
- **Blatt-Modus** — Rivoplan-Vorlage im Repo ⇒ das Blatt trägt ALLES
  (ADR-0003); Fallback ohne Vorlage = Schriftfeld-Boxen.
- **in-band** — Library-Block mit Extents < 50 units = platzierbares
  Punktsymbol (Kurations-Regel `schrack_symbol_mapping.yaml`).
- **Optik-aus-Achse** — Fluchtweg-SL: Korridor-Achsen-Azimut wird gerechnet UND
  als `rotation_deg` vermerkt; der Plan ist die Ausrichtungs-Zusicherung
  (ADR-0006).
- **konservativ (Photometrie)** — ohne Ausrichtungs-Zusicherung Minimum über
  alle C-Ebenen; nie Überschätzung (ADR-0005).
- **fail closed / „ungeprüft ≠ erfüllt"** — fehlende Erkennung/Nachweis wird
  Warnung, nie stilles ok (Prüfregeln 8b/8c/12/13/15).
- **circuit_hint** — `AGV-<Gebäude A|B>-F<Feeder>`; final vergeben als
  Anlage/Kreis/Adresse (Cap ≈ 20 je Kreis) durch `circuit_zuordnung`.
- **NODEID** — eindeutige Leuchten-Kennung am Symbol (`RZ-001`…), zweizeilig
  mit Anlage/Kreis/Adresse.
- **PlatzierungsKontext** — querschneidende place()-Eingaben
  (lb/oib/Photometrie-Callables) als ein Objekt (`platzierung/kontext.py`).

## 3. Pflege

Begriffs-/Typ-Änderungen sind Naht-Änderungen: Doku + betroffene
Maschinen-Quellen + Guards im SELBEN PR, Owner der Quelle taggt die anderen.
Bindende Entscheidungen dazu: `docs/adr/`.
