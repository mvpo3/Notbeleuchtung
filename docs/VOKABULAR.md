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
| AUFZUGSVORPLATZ | Erschließungsfläche vor dem Lift (Pflicht-POI „Aufzugsflur", Track C); Fluchtweg + communal — *neu 2026-09: Stempel-Label, Vorschlag zur Abnahme* |
| BAD | Sanitär-Flächen-Trigger (OVE, OIB-gegated) |
| BALKON | — |
| GANG | **Fluchtweg-Korridor**: Mittellinien-Verdichtung + RZ-GANG-Fallback |
| GARAGE | LB-adressierbar (`notlicht_kw_garage`) |
| KELLER | LB-adressierbar |
| KINDERWAGENRAUM | Türleuchten-Regel (Referenz-Praxis): RZ an der Tür — *neu 2026-09-08: vorher nach ABSTELLRAUM eingeebnet, dadurch griff die Regel auf echten Plänen nie* |
| KINDERZIMMER | — |
| KÜCHE | — |
| LAGER | LB-adressierbar |
| LIFT | — (Pflicht-POI „Aufzugsflur" = offener Track C) |
| MUELLRAUM | LB-adressierbar |
| SCHACHT | — (kein begehbarer Raum) — *neu 2026-09: `rest_komponenten` vergab das Label schon geometrisch (türlose Kleinfläche/STO-Kästchen); jetzt im Kanon statt außerhalb* |
| SCHLAFZIMMER | — |
| SCHLEUSE | **offen** — Notbeleuchtungsanforderung gesondert zu prüfen (`normwissen/data/regel_deckung.yaml`: `offen`, Owner Enis); Nutzungsklasse `ALLGEMEIN_ERSCHLIESSUNG`, Fluchtweg + communal — *neu 2026-09-11: Entscheidung Enis für die Rauch-/Brandschutzschleuse vor dem Stiegenkern. Begründung: Lage beim Stiegenkern (0 mm Kontakt zu den Treppen-Extents) und der ausgeschriebene Vergleichstext `DBA-Abstr. Schleuse` im Vergleichsgeschoss E8 (627 mm) bzw. E9 (10 mm) an derselben Lage. Fundstelle: Muthgasse_E2, Stempel `Schl.` / Stempelnummer `E2-VF-11a` (MTEXT `A-AREA-IDEN`, 335 239 / 108 646). Das AUSGESCHRIEBENE Wort steht im Wörterbuch (`raumtyp._EXTRA_DIRECT`); das mehrdeutige Kürzel `Schl.` typisiert NUR mit Zusatzbeleg + Owner-Entscheidung je Stempelnummer (`raumerkennung/kuerzel_entscheid.py`) — `E2-VF-11b` bleibt offen. **Nachtrag 2026-09-12:** außerhalb der fünf Prüfpläne tragen 2 Stempel den ausgeschriebenen Namen `SCHLEUSE` (`Projekte/_ergebnis_alle/2.Kellergeschoß`, bisher untypisiert); dort ändert der Kanon-Eintrag Typ und Flags — nicht nachgemessen, der Quellplan liegt nicht in `Projekte/_eingang`* |
| STIEGENHAUS | Fluchtweg + communal; Ausgangs-Anker; **Nachweis-Lücke offen** (Enis-Punkt 5) |
| TECHNIK | LB-adressierbar; Anlagen-Symbol-Standort |
| TERRASSE | — |
| VORRAUM | — |
| WASCHKÜCHE | communale Nasszelle — *neu 2026-09: `raumtyp._EXTRA_OVERRIDE` vergab das Label schon (Waschküche ≠ Wohnungsküche), stand aber außerhalb beider Guards; jetzt im Kanon* |
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
