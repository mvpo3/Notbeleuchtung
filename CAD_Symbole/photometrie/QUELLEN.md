# Photometrie-Katalog — Herkunft (Audit-Trail)

Hersteller-Lichtverteilungen (EULUMDAT/`.ldt`) für den EN-1838-Lux-Nachweis
(`platzierung/lux.py` via `i_cd_fn`). Quelle: öffentlicher Download-Bereich der
Schrack-Technik-Produktseiten (Stand **2026-09-03**, ohne Login frei zugänglich;
Nutzung als Hersteller-Planungsdaten). **Wichtig:** je Betriebsdauer liegt eine
eigene LDT vor (Notbetrieb ist gedimmt) — hier die Notbetriebs-Dateien.

| Datei | Artikel | Produkt | Optik/Betrieb | Download-URL |
|---|---|---|---|---|
| `rz_nlpxw433_1h3h_picto.ldt` | NLPXW433SC | Notleuchte PX Autotest 4×1W ERT-LED | Piktogramm-Linse, 1h/3h | https://image.schrackcdn.com/ldt/l_nlpxw433.._1h_3h_picto_square.ldt |
| `sl_nlkbu433_3h_round.ldt` | NLKBU433SC | Notleuchte KB Autotest LED, Universalmontage | Rundlinse (Fläche), 3h | https://image.schrackcdn.com/ldt/l_nlkbu433.._3h_round.ldt |
| `sl_nlkbu433_3h_corridor.ldt` | NLKBU433SC | Notleuchte KB Autotest LED, Universalmontage | Corridor-Linse (Fluchtweg), 3h | https://image.schrackcdn.com/ldt/l_nlkbu433.._3h_corridor_across.ldt |
| `antipanik_nlildl423_round.ldt` | NLILDL423S | Notleuchte IL Autotest 1×3W ERT-LED | Rundlinse (Antipanik), Betriebsdauer-unabhängig | https://image.schrackcdn.com/ldt/l_nlil.l423._round.ldt |

Produktseiten:
- PX: https://www.schrack.at/shop/notleuchte-px-autotest-4x1w-ert-led-3h-230v-ac-nlpxw433sc.html
- KB: https://www.schrack.at/shop/notleuchte-kb-autotest-led-3h-230v-ac-universalmontage-nlkbu433sc.html
- IL: https://www.schrack.at/shop/notleuchte-il-autotest-1x3w-ert-led-3h-230v-ac-nlildl423s.html

Hinweise für Nach-Downloads:
- Dateinamens-Muster der aktuellen Generation: `l_<artikel-wildcard>_<dauer>_<linse>.ldt`
  (die Punkte sind LITERALE Zeichen). Ältere Serien: `l_<artnr>-<1h|3h>.ldt`.
- Das CDN liefert für nicht existierende Pfade KEIN 404, sondern ein ~737-Byte-JPEG —
  Downloads immer auf Text-Header „Schrack" prüfen.
- Abgekündigte Vorgänger: NLKBU003SC→NLKBU433SC, NLKCWP033S/NLKCWP433S (KC, EOL),
  KM-Serie (NLKMU013SC) ohne LDT-Downloads → PX-Serie verwenden.
