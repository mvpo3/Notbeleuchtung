# Haustechnik-Grundlagen-Planung-Ausführung — Teil 13
> Quelle: Haustechnik-Grundlagen-Planung-Ausführung (buecher) · Seiten 521-560.

Dieser Abschnitt behandelt Kapitel 8 "Waermeversorgung" — konkret: Berechnung von U-Werten fuer Fenster und inhomogene Bauteile (DIN EN ISO 6946, 10077-1), die Anforderungen und Nachweisverfahren der Energieeinsparverordnung (EnEV) inklusive Primaerenergiebedarfsberechnung, Anlagen-Aufwandszahlen fuer sechs Referenzanlagen sowie die Grundlagen der Heizlastberechnung nach DIN EN 12831 mit Aussentemperatur-Tabelle und Wiederaufheizfaktoren.

## Inhalt

### Berechnung U-Wert thermisch inhomogener Bauteile (DIN EN ISO 6946)

Fuer Bauteile mit Bereichen unterschiedlicher Waermeleitfaehigkeit (z.B. Holz-Tragwerk in Daemmschicht) werden oberer und unterer Grenzwert des Waermedurchgangswiderstands R_T ermittelt.

- **Oberer Grenzwert R'_T:** Eindimensionaler Waermestrom senkrecht zu den Bauteiloberflaechen wird angenommen. Fuer jeden Abschnitt (a, b, … q) wird der Waermedurchgangswiderstand separat nach der Gleichung fuer homogene Bauteile bestimmt. Der Gesamtwiderstand ergibt sich als flaechengewichtetes Mittel der Abschnittswiderstaaende: 1/R'_T = f_a/R'_Ta + f_b/R'_Tb + … + f_q/R'_Tq
- **Unterer Grenzwert R''_T:** Alle zur Bauteiloberflaeche parallelen Ebenen werden als isotherm angenommen. Der Gesamtwiderstand ist: R''_T = R_si + R_1 + R_2 + … + R_j + R_se. Fuer inhomogene Schicht j gilt: 1/R_j = f_aj/R_aj + f_bj/R_bj + … + f_qj/R_qj

### U-Wert-Berechnung Fenster nach DIN EN ISO 10077-1

Der Gesamtwaermedurchgangskoeffizient einer Fensterkonstruktion U_w ergibt sich aus Verglasung (U_g), Rahmen (U_f) und dem Waermebr?ckeneffekt am Glasrand (Psi-Wert):

**Formel:** U_w = (A_g · U_g + A_f · U_f + l_g · psi) / (A_g + A_f)

- A_f = Rahmenflaeche, A_g = Glasflaeche, A_w = Gesamtfensterflaeche (A_f + A_g)
- l_g = aeussere Gesamtumfangslaenge der Verglasung (Summe sichtbarer Umfangslaengen der Scheiben)
- Bei vertikalen/leicht geneigten Fenstern (>60°): R_se = 0,04 m²·K/W, R_si = 0,13 m²·K/W
- Waermeleitfaehigkeit Glas bei fehlenden Angaben: lambda = 1,0 W/(m·K)

**U_g-Wert Mehrscheiben-Isolierverglasung (Tabelle 8.7, nach DIN EN ISO 10077-1):**

| Verglasung | Beschichtung (Emissionsgrad) | Aufbau (mm) | Luft | Argon | Krypton | SF6 |
|---|---|---|---|---|---|---|
| Zweischeiben | unbeschichtet (0,89) | 4-6-4 | 3,3 | 3,0 | 2,8 | 3,0 |
| Zweischeiben | unbeschichtet (0,89) | 4-9-4 | 3,0 | 2,8 | 2,6 | 3,1 |
| Zweischeiben | unbeschichtet (0,89) | 4-12-4 | 2,9 | 2,7 | 2,6 | 3,1 |
| Zweischeiben | unbeschichtet (0,89) | 4-15-4 | 2,7 | 2,6 | 2,6 | 3,1 |
| Zweischeiben | unbeschichtet (0,89) | 4-20-4 | 2,7 | 2,6 | 2,6 | 3,1 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,4) | 4-6-4 | 2,9 | 2,6 | 2,2 | 2,6 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,4) | 4-9-4 | 2,6 | 2,3 | 2,0 | 2,7 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,4) | 4-12-4 | 2,4 | 2,1 | 2,0 | 2,7 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,4) | 4-15-4 | 2,2 | 2,0 | 2,0 | 2,7 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,4) | 4-20-4 | 2,2 | 2,0 | 2,0 | 2,7 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,2) | 4-6-4 | 2,7 | 2,3 | 1,9 | 2,3 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,2) | 4-9-4 | 2,3 | 2,0 | 1,6 | 2,4 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,2) | 4-12-4 | 1,9 | 1,7 | 1,5 | 2,4 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,2) | 4-15-4 | 1,8 | 1,6 | 1,6 | 2,5 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,2) | 4-20-4 | 1,8 | 1,7 | 1,6 | 2,5 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,1) | 4-6-4 | 2,6 | 2,2 | 1,7 | 2,1 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,1) | 4-9-4 | 2,1 | 1,7 | 1,3 | 2,2 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,1) | 4-12-4 | 1,8 | 1,5 | 1,3 | 2,3 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,1) | 4-15-4 | 1,6 | 1,4 | 1,3 | 2,3 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,1) | 4-20-4 | 1,6 | 1,4 | 1,3 | 2,3 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,05) | 4-6-4 | 2,5 | 2,1 | 1,5 | 2,0 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,05) | 4-9-4 | 2,0 | 1,6 | 1,3 | 2,1 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,05) | 4-12-4 | 1,7 | 1,3 | 1,1 | 2,2 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,05) | 4-15-4 | 1,5 | 1,2 | 1,1 | 2,2 |
| Zweischeiben | 1 Scheibe beschichtet (≤0,05) | 4-20-4 | 1,5 | 1,2 | 1,2 | 2,2 |
| Dreischeiben | unbeschichtet (0,89) | 4-6-4-6-4 | 2,3 | 2,1 | 1,8 | 2,0 |
| Dreischeiben | unbeschichtet (0,89) | 4-9-4-9-4 | 2,0 | 1,9 | 1,7 | 2,0 |
| Dreischeiben | unbeschichtet (0,89) | 4-12-4-12-4 | 1,9 | 1,8 | 1,6 | 2,0 |
| Dreischeiben | 2 Scheiben beschichtet (≤0,4) | 4-6-4-6-4 | 2,0 | 1,7 | 1,4 | 1,6 |
| Dreischeiben | 2 Scheiben beschichtet (≤0,4) | 4-9-4-9-4 | 1,7 | 1,5 | 1,2 | 1,6 |
| Dreischeiben | 2 Scheiben beschichtet (≤0,4) | 4-12-4-12-4 | 1,5 | 1,3 | 1,1 | 1,6 |
| Dreischeiben | 2 Scheiben beschichtet (≤0,2) | 4-6-4-6-4 | 1,8 | 1,5 | 1,1 | 1,3 |
| Dreischeiben | 2 Scheiben beschichtet (≤0,2) | 4-9-4-9-4 | 1,4 | 1,2 | 0,9 | 1,3 |
| Dreischeiben | 2 Scheiben beschichtet (≤0,2) | 4-12-4-12-4 | 1,2 | 1,0 | 0,8 | 1,4 |
| Dreischeiben | 2 Scheiben beschichtet (≤0,1) | 4-6-4-6-4 | 1,7 | 1,3 | 1,0 | 1,2 |
| Dreischeiben | 2 Scheiben beschichtet (≤0,1) | 4-9-4-9-4 | 1,3 | 1,0 | 0,8 | 1,2 |
| Dreischeiben | 2 Scheiben beschichtet (≤0,1) | 4-12-4-12-4 | 1,1 | 0,9 | 0,6 | 1,2 |
| Dreischeiben | 2 Scheiben beschichtet (≤0,05) | 4-6-4-6-4 | 1,6 | 1,3 | 0,9 | 1,1 |
| Dreischeiben | 2 Scheiben beschichtet (≤0,05) | 4-9-4-9-4 | 1,2 | 0,9 | 0,7 | 1,1 |
| Dreischeiben | 2 Scheiben beschichtet (≤0,05) | 4-12-4-12-4 | 1,0 | 0,8 | 0,5 | — |

Alle Werte in W/(m²·K). Gaskonzentration im Scheibenzwischenraum muss ≥90 % betragen.

**U_f-Werte Rahmen (Tabelle 8.8, DIN EN ISO 10077-1):**

| Rahmenmaterial | Typ | U_f [W/(m²·K)] |
|---|---|---|
| Polyurethan | Mit Metallkern, PUR-Dicke ≥ 5 mm | 2,8 |
| PVC-Hohlprofile | 2 Hohlkammern | 2,2 |
| PVC-Hohlprofile | 3 Hohlkammern | 2,0 |
| Metall | ohne waermetechnische Trennung | 5,9 |

Anmerkung PVC: Wandabstand Hohlkammern mindestens 5 mm.

**Holzrahmen-U_f-Werte (Tabelle 8.9):** Nach DIN EN ISO 10077-1, wird im Quelldokument als Tabelle angefuehrt — Werte sind hersteller- bzw. querschnittsabhaengig.

**Psi-Werte Glasrandverbund Aluminium-Abstandshalter (Tabelle 8.10):**

| Rahmenwerkstoff | Zwei- oder Dreischeiben unbeschichtet/Luft oder Gas | Zweischeiben Niedrigemission oder Dreischeiben 2 Beschichtungen |
|---|---|---|
| Holz- und Kunststoffrahmen | 0,04 | 0,06 |
| Metallrahmen mit waermetechn. Trennung | 0,06 | 0,08 |
| Metallrahmen ohne waermetechn. Trennung | 0,00 | 0,02 |

### Waermetransport: Konvektion (Waermemitfuehrung)

Fluessige und gasfoermige Stoffe transportieren Waerme nicht nur durch Leitung, sondern auch durch Umwaelzung: Erwaermte Stoffe dehnen sich aus, werden leichter und steigen auf — an kaelteren Flaechen geben sie Waerme ab, kuehlen sich ab, sinken und der Kreislauf schliesst sich. Dieser Vorgang wird durch aeussere Antriebe (Pumpen, Geblaese) beschleunigt. Daemmstoffwirkung beruht auf ruhender Luft in kleinen Poren: groessere Poren erlauben Umwaelzung und Abstrahlung, wodurch die Daemmwirkung sinkt — kleinere Poren bedeuten bessere Daemmwirkung.

---

### EnEV — Grundprinzip und Systemgrenze

Die Energieeinsparverordnung (EnEV) ersetzt die frueheren Waermeschutzverordnung WschVO und Heizanlagenverordnung durch eine gesamtenergetische Bewertung. Nicht nur Waermeverluste werden begrenzt, sondern der vollstaendige Jahres-Primaarenergiebedarf unter Einbeziehung von solaren Gewinnen, Anlagentechnik (Heizung, Lueftung, Warmwasser) und Energietraegerart. Ergebnis ist ein verbindlicher Energiebedarfsausweis (fuer Gebaeude mit normalen Innentemperaturen) bzw. Waermebedarfsausweis (fuer Gebaeude mit niedrigen Innentemperaturen).

### EnEV Anforderungen nach Gebaeudekategorie

**Normale Innentemperaturen:** Gebaeude, die mehr als 4 Monate im Jahr auf ≥19 °C beheizt werden (typisch Wohngebaeude).

**Niedrige Innentemperaturen:** Gebaeude, die mehr als 4 Monate auf >12 °C und <19 °C beheizt werden.

**Grenzwerte fuer Gebaeude mit normalen Innentemperaturen (Tabelle 8.13):**

| A/Ve [m⁻¹] | Q''p Wohngebaeude [kWh/(m²·a)] | Q''p Wohngebaeude elekr. Warmwasser [kWh/(m²·a)] | Q'p andere Gebaeude [kWh/(m³·a)] | H'_T Fensterflaeche ≤30 % [W/(m²·K)] | H'_T Fensterflaeche >30 % [W/(m²·K)] |
|---|---|---|---|---|---|
| ≤0,2 | 66,00 + 2600/(100+AN) | 88,00 | 14,72 | 1,05 | 1,55 |
| 0,3 | 73,53 + 2600/(100+AN) | 95,53 | 17,13 | 0,80 | 1,15 |
| 0,4 | 81,06 + 2600/(100+AN) | 103,06 | 19,54 | 0,68 | 0,95 |
| 0,5 | 88,58 + 2600/(100+AN) | 110,58 | 21,95 | 0,60 | 0,83 |
| 0,6 | 96,11 + 2600/(100+AN) | 118,11 | 24,36 | 0,55 | 0,75 |
| 0,7 | 103,64 + 2600/(100+AN) | 125,64 | 26,77 | 0,51 | 0,69 |
| 0,8 | 111,17 + 2600/(100+AN) | 133,17 | 29,18 | 0,49 | 0,65 |
| 0,9 | 118,70 + 2600/(100+AN) | 140,70 | 31,59 | 0,47 | 0,62 |
| 1,0 | 126,23 + 2600/(100+AN) | 148,23 | 34,00 | 0,45 | 0,59 |
| ≥1,05 | 130,00 + 2600/(100+AN) | 152,00 | 35,21 | 0,44 | 0,58 |

Interpolationsformeln:
- Sp. 2: Q''p = 50,94 + 75,29 · A/Ve + 2600/(100 + AN)
- Sp. 3: Q''p = 72,94 + 75,29 · A/Ve
- Sp. 4: Q'p = 9,90 + 24,10 · A/Ve
- Sp. 5: H'_T = 0,30 + 0,15/(A/Ve)
- Sp. 6: H'_T = 0,35 + 0,24/(A/Ve)

**Ausnahmen Jahres-Primaerenergiebedarf-Hoechstwerte:** Gelten nicht fuer Gebaeude, die zu ≥70 % durch KWK-Waerme oder ≥70 % durch erneuerbare Energien aus selbsttaetig arbeitenden Waermeerzeugern beheizt werden. Fuer Raeume mit Einzelfeuerstaetten darf der auf die Umfassungsflaeche bezogene Transmissionswaermeverlust max. 76 % des Hoechstwerts betragen.

**Gebaeude mit Fensterflaeche >30 %:** Zusaetzlich Nachweis nach DIN 4108-2 (Sonneneintragskennwert) erforderlich.

**Grenzwerte fuer Gebaeude mit niedrigen Innentemperaturen (Tabelle 8.14):**

| A/Ve [m⁻¹] | H'_T max [W/(m²·K)] |
|---|---|
| ≤0,20 | 1,03 |
| 0,30 | 0,86 |
| 0,40 | 0,78 |
| 0,50 | 0,73 |
| 0,60 | 0,70 |
| 0,70 | 0,67 |
| 0,80 | 0,66 |
| 0,90 | 0,64 |
| ≥1,00 | 0,63 |

Interpolation: H'_T = 0,53 + 0,1 · Ve/A

**Luftdichtheit und Mindestlueftwechsel:**
- Gebaeudehuehlle dauerhaft luftundurchlaessig abzudichten
- Fugendurchlaessigkeit Fenster/Fenstertuer/Dachflaechenfenster nach DIN EN 12207:
  - Bis zu 2 Vollgeschosse: Klasse 2
  - Mehr als 2 Vollgeschosse: Klasse 3
- Blower-Door-Test nach DIN EN 13829 bei 50 Pa Druckdifferenz:
  - Gebaeude ohne raumlufttechnische Anlagen: max. 3 h⁻¹
  - Gebaeude mit raumlufttechnischen Anlagen: max. 1,5 h⁻¹
- Lueftungseinrichtungen in der Gebaeudehuehlle muessen einstellbar und regulierbar sein

**Mindeswaermeschutz und Waermebruecken:**
- Bauteile gegen Aussenluft, Erdreich oder wesentlich kuehler temperierte Gebaeudeteile muessen anerkannte Mindeswaermeschutzanforderungen erfuellen
- Einfluss konstruktiver Waermebruecken ist auf den Jahres-Heizwaermebedarf zu minimieren und in Transmissionswaermeverlust/Jahres-Primaerenergiebedarf einzurechnen
- Pauschalzuschlag standardmaessig — Einzelnachweis nach DIN V 4108-6 mit Psi-Werten bei Bedarf

**Gebaeude mit geringem Volumen (<100 m³):** Bei Erfuellung der Anforderungen fuer Heizungs-/Warmwasseranlagen sowie U_max-Hoechstwerte nach Tabelle 8.16 — keine weiteren Anforderungen.

**Aenderungen an bestehenden Gebaenden:**
- Betroffene Aussenteile duerfen U_max nach Tabelle 8.16 nicht ueberschreiten
- Ausnahme: geringfuegige Aenderungen <20 % der Bauteilflaeche je Himmelsrichtung
- Wird Jahres-Primaerenergiebedarf/spez. Transmissionswaermeverlust um <40 % ueberschritten: Tabelle 8.16 gilt als erfuellt
- Erweiterung um >30 m³ beheiztes Volumen: Vorschriften wie bei Neubau anwendbar

**Hoechstwerte U_max bei Bauteilmassnahmen (Tabelle 8.16):**

| Bauteil | Massnahme | U_max normal [W/(m²·K)] | U_max niedrig [W/(m²·K)] |
|---|---|---|---|
| Aussenwand | allgemein | 0,45 | 0,75 |
| Aussenwand | Platten/Verschalungen/Vorsatzschalen | 0,35 | 0,75 |
| Aussenwand | Einbauen Daemmschichten | 0,35 | 0,75 |
| Aussenwand | Ausssenputz erneuern bei U>0,9 | 0,35 | 0,75 |
| Fenster/Fenstertuer/Dachflaechenfenster | Ersetzen/Ersteinbau | 1,70 | 2,80 |
| Verglasung | Einbauen Vor-/Innenfenster | 1,50 | keine Anf. |
| Vorhangfassaden | allgemein | 1,90 | 3,00 |
| Fenster/Tuer mit Sonderverglasung | Ersetzen/Ersteinbau | 2,00 | 2,80 |
| Sonderverglasung | Vor-/Innenfenster einbauen | 1,60 | keine Anf. |
| Vorhangfassaden mit Sonderverglasung | Fuellung (Verglasung/Paneele) ersetzen | 2,30 | 3,00 |
| Aussentuer | Erneuern | 2,90 | keine Anf. |
| Decken/Daecher/Dachschraegen | Steildach | 0,30 | 0,40 |
| Daecher | Flachdach | 0,25 | 0,40 |
| Decken/Waende gegen unbeheizte/Erdreich | Aussenbekleidungen/Feuchtigkeitssperren | 0,40 | keine Anf. |
| Decken/Waende gegen unbeheizte/Erdreich | Deckenbekleidungen (Kaltseite) | 0,40 | keine Anf. |
| Decken/Waende gegen unbeheizte/Erdreich | Ersetzen/Ersteinbau | 0,50 | keine Anf. |
| Waende | Innenbekleidungen/-verschalungen | 0,50 | keine Anf. |
| Fussboden | Fussbodenaufbau beheizte Seite | 0,50 | keine Anf. |

**Nachruehstpflichten bestehende Gebaeude:**
- Heizkessel fuer fluessige/gasfoermige Brennstoffe, eingebaut vor 1.10.1978: Betrieb bis 31.12.2006 einzustellen (Brenner nach 1.11.1996 erneuert: Frist bis 31.12.2008)
- Ausgenommen: Niedertemperatur- und Brennwertkessel sowie Anlagen <4 kW oder >400 kW Nennwaermeleistung
- Ungedaemmte zugaengliche Waermeverteilungs-/Warmwasserleitungen und Armaturen ausserhalb beheizter Raeume: bis 31.12.2006 daemmen
- Nicht begehbare aber zugaengliche oberste Geschossdecken: bis 31.12.2006 auf U ≤0,30 W/(m²·K) daemmen
- Eigengenutzte Gebaeude mit max. 2 Wohnungen: ausgenommen, Pflicht bei Eigentumswechsel innerhalb 2 Jahren

**Daemmdicken Waermeverteilungs-/Warmwasserleitungen (Tabelle 8.17, bezogen auf lambda = 0,035 W/(m·K)):**

| Zeile | Leitungstyp | Mindestdaemmdicke |
|---|---|---|
| 1 | Innendurchmesser bis 22 mm | 20 mm |
| 2 | Innendurchmesser >22 bis 35 mm | 30 mm |
| 3 | Innendurchmesser >35 bis 100 mm | gleich Innendurchmesser |
| 4 | Innendurchmesser >100 mm | 100 mm |
| 5 | Wand-/Deckendurchbrueche, Kreuzungsbereiche, Verbindungsstellen, zentrale Verteiler | 1/2 der Anforderungen Zeilen 1-4 |
| 6 | Zentralheizungsleitungen in Bauteilen zwischen beheizten Raeumen verschiedener Nutzer (nach Inkrafttreten der Verordnung) | 1/2 der Anforderungen Zeilen 1-4 |
| 7 | Leitungen nach Zeile 6 im Fussbodenaufbau | 6 mm |

**Anlagenanforderungen:**
- Zentralheizungen mit selbsttaetigen Einrichtungen zur Verringerung/Abschaltung elektrischer Antriebe in Abhaengigkeit von Aussentemperatur und Zeit auszustatten
- Heizungsanlagen mit Wasser als Waermetraeger: selbsttaetige raumweise Temperaturregelung (Ausnahme: Einzelheizgeraete, Gruppenregelungen fuer gleiche Raumarten)
- Umwaelzpumpen in Heizkreisen mit >25 kW Nennwaermeleistung: selbsttaetiger Leistungsanpassung in mindestens 3 Stufen
- Zirkulationspumpen: selbsttaetig wirkende Ein-/Ausschalteinrichtungen
- Heizkessel mit Nennwaermeleistung 4-400 kW und fluessige/gasfoermige Brennstoffe: CE-Kennzeichnung und EWG-Richtlinien-Konformitaet

### EnEV Nachweisverfahren

**Energiebedarfsausweis (Tabelle 8.11)** fuer Gebaeude mit normalen Innentemperaturen:
- Pflicht bei jedem Neubau
- Pflicht bei wesentlichen Aenderungen: mindestens 3 Aenderungen nach Anhang 3 Nr. 1-6 kombiniert mit Kesselaustausch/Energietraegerwechsel, oder Erweiterung beheiztes Volumen >50 %
- Inhalt: Objektbeschreibung, geometrische Angaben (A, Ve, A/Ve, AN), Beheizungs-/Warmwasserart, Jahres-Primaerenergiebedarf (zulaessig + berechnet), Endenergiebedarf nach Energietraeger, Transmissionswaermeverlust, Anlagenaufwandszahl, Waermebruecken-Beruecksichtigung, Dichtheitsnachweise, sommerlicher Waermeschutz
- Hinweis: Berechnete Werte basieren auf normierten Randbedingungen (Klima, Heizdauer, Innentemperaturen, Luftwechsel, solare/interne Gewinne, Warmwasserbedarf nach DIN V 4701-10 und DIN V 4108-6 Anhang D)

**Waermebedarfsausweis (Tabelle 8.12)** fuer Gebaeude mit niedrigen Innentemperaturen:
- Inhalt: Objektbeschreibung, geometrische Angaben, Transmissionswaermeverlust, Einzelnachweise/Ausnahmen/Befreiungen

Beide Ausweise sind Kaufinteressenten, Mietern, Nutzern und Behoerden auf Anfrage zugaenglich zu machen.

### Berechnung Jahres-Primaerenergiebedarf Q_P

**Hauptgleichung:**
Q_P = (Q_h + Q_w) · e_P [kWh/a]

- Q_h = Jahres-Heizwaermebedarf [kWh/a]
- Q_w = Waermebedarf Warmwasserbereitung [kWh/a]
- e_P = Anlagen-Aufwandszahl

Bei e_P > 1: Anlage erhoht Primaerenergiebedarf; bei e_P < 1 (z.B. Waermepumpe): Reduzierung. Energetisch unguenstige Anlagen koennen Gesamtwaermebedarf mehr als verdoppeln (e_P > 2).

**Jahres-Heizwaermebedarf Q_h:** Waermemenge, die Heizungsanlage zufuehren muss, um mittlere Raumtemperatur (19 °C nach EnEV) zu erzielen. Zwei Berechnungsverfahren:
- Heizperiodenbilanzverfahren (vereinfacht, fuer Wohngebaeude mit Fensterflaeche ≤30 %)
- Monatsbilanzverfahren (ausfuehrlich, rechnerunterstuetzt)

**Waermebedarf Warmwasserbereitung Q_w:** Pauschal: Q_w = 12,5 · AN [kWh/a]. Entspricht etwa 23 Liter/Person/Tag bei 50 °C Wassertemperatur.

### Heizperiodenbilanzverfahren (8.2.2.2)

Anwendbar fuer neue Wohngebaeude mit Fensterflaeche max. 30 %.

**Grundgleichung:**
Q_h = 66 · (H_T + H_V) − 0,95 · (Q_S + Q_i) [kWh/a]

- 66 = Gradtagszahlfaktor (beruecksichtigt Heizdauer, Heizgrenztemperatur, Nachtabsenkung)
- 0,95 = Abminderungsfaktor fuer Ausnutzungsgrad Waermegewinne
- H_T = Transmissionswaermeverlust [W/K]
- H_V = Lueftungswaermeverlust [W/K]
- Q_S = solare Waermegewinne [kWh/a]
- Q_i = interne Waermegewinne [kWh/a]

**Transmissionswaermeverlust H_T:**
H_T = Sum(Fx_i · U_i · A_i) + U_WB · A_ges [W/K]

- Fx_i = Temperatur-Korrekturfaktor (Anpassung an Bauteile, die nicht direkt an Aussenluft grenzen)
- U_WB = Waermebrückenverlustkoeffizient

**Temperatur-Korrekturfaktoren Fx_i (Tabelle 8.18):**

| Bauteil-Situation | Fx_i |
|---|---|
| Aussenwand, Fenster | 1,0 |
| Dach (als Systemgrenze) | 1,0 |
| Oberste Geschossdecke (Dachraum nicht ausgebaut) | 0,8 |
| Abseitenwand (Drempelwand) | 0,8 |
| Waende und Decken zu unbeheizten Raeumen | 0,5 |
| Kellerdecke/-waende zu unbeheiztem Keller, Fussboden auf Erdreich, Beheizter Keller gegen Erdreich | 0,6 |

**Waermebrückenverlustkoeffizient U_WB:** Geometrische Ursachen (z.B. Gebaeudeecke) oder Materialmix. Empfohlene Pauschalwerte:
- U_WB = 0,10 W/(m²·K): Konstruktionen nach anerkannten Regeln der Technik
- U_WB = 0,05 W/(m²·K): Konstruktionen nach DIN 4108 Beiblatt 2 (Planungs- und Ausfuehrungsbeispiele fuer Waermebruecken)
- Individuelle Berechnung nach DIN V 4108-6 moeglich, aber aufwendig

**Lueftungswaermeverlust H_V:**
H_V = rho_L · c_pL · n · V [W/K]
- Waermespeicherfaehigkeit Luft: rho_L · c_pL = 0,34 Wh/(m³·K)
- Luftvolumenstrom V = 0,80 · Ve (grosses Gebaeude), V = 0,76 · Ve (bis 3 Vollgeschosse)

Vereinfachung nach Luftwechselzahl n:
- Fensterlueeftung ohne Dichtigkeitspruefung (n = 0,7 h⁻¹): H_V = 0,190 · Ve
- Fensterlueeftung mit Dichtigkeitspruefung (n = 0,6 h⁻¹): H_V = 0,163 · Ve
- n = 0,6 h⁻¹ nur bei anerkanntem Nachweisverfahren (DIN EN 13829) zulaeassig

Grenzwerte Luftdichtheit (Blower-Door, 50 Pa):
- Ohne raumlufttechnische Anlage: max. 3 h⁻¹
- Mit raumlufttechnischen Anlage: max. 1,5 h⁻¹; Dichtigkeitspruefung bei Lueftungsanlage zwingend

Fugendurchlaessigkeit Fenster/Fenstertuer/Dachflaechenfenster (DIN EN 12207):
- Bis 2 Vollgeschosse: Klasse 2
- Mehr als 2 Vollgeschosse: Klasse 3

**Solare Gewinne Q_S:**
Q_S = Sum(0,567 · (I_S)_j,HP · g_i · A_i) [kWh/a]

Faktor 0,567 beruecksichtigt durchschnittlichen Rahmenanteil, Teilverschattung, Absorption/Reflexion. A_i = lichte Rohbaumasse, g_i = Gesamtenergiedurchlass (Herstellerangabe oder nach DIN EN 410).

**Solares Strahlungsangebot nach Himmelsrichtung (Tabelle 8.19):**

| Himmelsrichtung | (I_S)_j,HP [kWh/(m²·a)] |
|---|---|
| Suedost bis Suedwest | 270 |
| Suedwest bis Nordwest | 155 |
| Nordost bis Suedost | 155 |
| Nordwest bis Nordost | 100 |
| Dachflaechenfenster (Neigung <30°) | 250 |

**Interne Gewinne Q_i:**
Q_i = 22 · AN [kWh/a]
Faktor 22 = 185 Heiztage (DIN V 4701-10) × 24 h × 5 W/m². Bei Buerogebaeuden 6 W/m² annehmbar.

### Anlagen-Aufwandszahl e_P (8.2.2.3)

Effizienzmasszahl der Gesamtanlage. Niedrig = effizient. Beruecksichtigt auch Primaerenergiefaktor f_P des Energietraegers.

**Primaerenergiefaktoren f_P (Tabelle 8.20, DIN V 4701-10):**

| Energietraeger | f_P |
|---|---|
| Heizoel EL | 1,1 |
| Erdgas H | 1,1 |
| Fluessiggas | 1,1 |
| Steinkohle | 1,1 |
| Braunkohle | 1,2 |
| Holz | 0,2 |
| Nah-/Fernwaerme KWK fossiler Brennstoff | 0,7 |
| Nah-/Fernwaerme KWK erneuerbarer Brennstoff | 0,0 |
| Nah-/Fernwaerme Heizwerke fossiler Brennstoff | 1,3 |
| Nah-/Fernwaerme Heizwerke erneuerbarer Brennstoff | 0,1 |
| Strom-Mix | 3,0 |

**Drei Verfahren zur Ermittlung e_P nach DIN V 4701-10:**
1. **Diagrammverfahren:** Einfachste Methode — grafische Ablesung aus Diagrammen und Tabellen der DIN V 4701-10 und Beiblatt 1 (65 weitere Anlagenbeispiele). Voraussetzung: flaechenbezogener Primaerenergiebedarf q_h = Q_h/AN bekannt.
2. **Tabellenverfahren:** Bei noch nicht feststehenden Komponenten — Kennwerte fuer Standardprodukte aus Anhang C.1-C.4 der DIN V 4701-10. Orientiert sich am unteren energetischen Marktdurchschnitt — fuehrt nicht zu guenstigsten Werten, aber immer anwendbar.
3. **Detailliertes Verfahren:** Sehr aufwendig, erfordert genaue Komponentenkennwerte. Ergibt in der Regel guenstigere Ergebnisse als Tabellenverfahren.

**Variationsparameter Anlagenbeispiele (Tabelle 8.21, DIN V 4701-10 Beiblatt 1):**
- Heizung: Waermeuebergabe Heizkoerper im Aussenwandbereich, 2 K Regelabweichung; Fussbodenheizung und Radiatoren energetisch gleichwertig
- Verteilung Heizung: Steigstraenge immer innenliegend; Verteilstraenge ausserhalb thermischer Huelle wenn Erzeuger/Speicher auch aussen
- Umwaelzpumpen immer geregelt
- Speicherung: Pufferspeicher bei Waermepumpenanlagen immer vorhanden
- Solare Heizungsunterstuetzung: Deckungsanteil alpha = 0,1
- Fernwaerme: Vor-/Ruecklauf 70/55 °C und 55/45 °C
- Waermepumpen: Temperaturpaarung immer 35/28 °C
- NT-Kessel: 70/55 °C; Brennwertkessel: 55/45 °C und 35/28 °C
- Trinkwarmwasser: Speicher und Erzeuger gemeinsam innen oder aussen
- Lueftung: Luftauslaesse im Ausssenbereich; Anlagenluftwechsel n_A = 0,4 h⁻¹; DC-Ventilatoren; Waermerueckgewinnung eta_WRG = 0,6 (bzw. 0,8 bei energieeffizienten Komponenten)

### Sechs Referenz-Anlagenbeispiele mit Anlagen-Aufwandszahl e_P

**Anlage 1 — Niedertemperatur-Kessel, gebaeudezentrale Trinkwassererwaaermung:**
- Heizung: Radiatoren mit Thermostatventil 1 K; Vor-/Ruecklauf max. 70/55 °C, horizontale Verteilung innerhalb thermischer Huelle, Stranglaeitungen innenliegend, geregelte Pumpe; NT-Kessel Erdgas/Erdoel EL ausserhalb thermischer Huelle
- Trinkwarmwasser: horizontale Verteilung innerhalb th. H., mit Zirkulation; indirekt beheizter Speicher ausserhalb th. H.; Erzeugung: NT-Kessel zentral

e_P-Tabelle (Tabelle 8.24), Auszug (qh in kWh/(m²·a), AN in m²):

| q_h | AN=100 | AN=150 | AN=200 | AN=300 | AN=500 | AN=1000 | AN=1500 | AN=2500 | AN=5000 | AN=10000 |
|---|---|---|---|---|---|---|---|---|---|---|
| 40 | 2,34 | 2,07 | 1,93 | 1,79 | 1,66 | 1,57 | 1,54 | 1,51 | 1,49 | 1,46 |
| 50 | 2,17 | 1,94 | 1,82 | 1,70 | 1,59 | 1,51 | 1,49 | 1,46 | 1,44 | 1,42 |
| 60 | 2,05 | 1,84 | 1,74 | 1,63 | 1,54 | 1,47 | 1,45 | 1,42 | 1,41 | 1,38 |
| 70 | 1,95 | 1,77 | 1,68 | 1,58 | 1,50 | 1,44 | 1,42 | 1,39 | 1,38 | 1,36 |
| 80 | 1,88 | 1,72 | 1,63 | 1,55 | 1,47 | 1,41 | 1,40 | 1,37 | 1,36 | 1,34 |
| 90 | 1,82 | 1,67 | 1,59 | 1,52 | 1,45 | 1,39 | 1,38 | 1,36 | 1,35 | 1,33 |

**Anlage 2 — Brennwert-Kessel, gebaeudezentrale Trinkwassererwaaermung:**
- Heizung: Radiatoren 1 K; Vor-/Ruecklauf max. 55/45 °C, horizontale Verteilung ausserhalb th. H., Straenge innenliegend; Brennwertkessel Erdgas/Erdoel EL ausserhalb th. H.
- Trinkwarmwasser: horizontale Verteilung ausserhalb th. H., mit Zirkulation; indirekt beheizter Speicher ausserhalb; Erzeugung: Brennwertkessel zentral

e_P-Tabelle (Tabelle 8.27):

| q_h | AN=100 | AN=150 | AN=200 | AN=300 | AN=500 | AN=1000 | AN=1500 | AN=2500 | AN=5000 | AN=10000 |
|---|---|---|---|---|---|---|---|---|---|---|
| 40 | 2,16 | 1,91 | 1,79 | 1,67 | 1,56 | 1,46 | 1,44 | 1,42 | 1,39 | 1,38 |
| 50 | 2,00 | 1,78 | 1,68 | 1,58 | 1,49 | 1,41 | 1,39 | 1,37 | 1,34 | 1,33 |
| 60 | 1,88 | 1,70 | 1,61 | 1,52 | 1,44 | 1,37 | 1,35 | 1,34 | 1,31 | 1,30 |
| 70 | 1,79 | 1,63 | 1,55 | 1,48 | 1,40 | 1,34 | 1,33 | 1,31 | 1,29 | 1,28 |
| 80 | 1,72 | 1,58 | 1,51 | 1,44 | 1,37 | 1,32 | 1,30 | 1,29 | 1,27 | 1,26 |
| 90 | 1,67 | 1,53 | 1,47 | 1,41 | 1,35 | 1,30 | 1,29 | 1,27 | 1,25 | 1,25 |

**Anlage 3 — Brennwert-Kessel und solar unterstuetzte Trinkwassererwaaermung:**
- Heizung: Radiatoren 1 K; Vor-/Ruecklauf max. 55/45 °C, horizontal innerhalb th. H., Straenge innenliegend; Brennwertkessel innerhalb th. H.
- Trinkwarmwasser: gebaeudezentral ohne Zirkulation, horizontal innerhalb th. H.; bivalenter Solarspeicher innerhalb th. H.; Erzeugung: Brennwertkessel + Solaranlage
- Nur fuer kleinere Gebaeude (AN bis 500 m²) tabelliert

e_P-Tabelle (Tabelle 8.30):

| q_h | AN=100 | AN=150 | AN=200 | AN=300 | AN=500 |
|---|---|---|---|---|---|
| 40 | 1,25 | 1,21 | 1,18 | 1,17 | 1,12 |
| 50 | 1,23 | 1,19 | 1,17 | 1,16 | 1,12 |
| 60 | 1,21 | 1,18 | 1,16 | 1,15 | 1,11 |
| 70 | 1,20 | 1,17 | 1,16 | 1,15 | 1,11 |
| 80 | 1,19 | 1,16 | 1,15 | 1,14 | 1,11 |
| 90 | 1,18 | 1,16 | 1,15 | 1,14 | 1,11 |

**Anlage 4 — Brennwert-Kessel und Lueftungsanlage mit Waermerueckgewinnung:**
- Heizung: Radiatoren 1 K; Vor-/Ruecklauf max. 55/45 °C, horizontal innerhalb th. H.; Brennwertkessel innerhalb th. H.
- Trinkwarmwasser: horizontal innerhalb th. H., mit Zirkulation; indirekt beheizter Speicher innerhalb th. H.; Erzeugung: Brennwertkessel zentral
- Lueftung: zentrale Zu-/Abluftanlage; Verteilleitungen innerhalb th. H.; Luftwechsel 0,4 h⁻¹; DC-Ventilator; Waermerueckgewinnung durch Waermeuebertraeger, Waermebereitstellungsgrad 80 %

e_P-Tabelle (Tabelle 8.33):

| q_h | AN=100 | AN=150 | AN=200 | AN=300 | AN=500 |
|---|---|---|---|---|---|
| 40 | 1,56 | 1,42 | 1,35 | 1,28 | 1,23 |
| 50 | 1,49 | 1,37 | 1,31 | 1,25 | 1,21 |
| 60 | 1,44 | 1,33 | 1,29 | 1,23 | 1,19 |
| 70 | 1,40 | 1,31 | 1,26 | 1,22 | 1,18 |
| 80 | 1,37 | 1,29 | 1,25 | 1,21 | 1,18 |
| 90 | 1,34 | 1,27 | 1,23 | 1,20 | 1,17 |

**Anlage 5 — Waermepumpe (Erdreich/Wasser), gebaeudezentrale Trinkwassererwaaermung:**
- Heizung: Flaechenheizung mit Einzelraumregelung; Pufferspeicher ausserhalb th. H.; Vor-/Ruecklauf max. 35/28 °C, horizontal ausserhalb th. H.; Elektrowaermepumpe Erdreich/Wasser ausserhalb
- Trinkwarmwasser: horizontal ausserhalb th. H., keine Zirkulation; indirekt beheizter Speicher ausserhalb; Erzeugung: Elektrowaermepumpe

e_P-Tabelle (Tabelle 8.36):

| q_h | AN=100 | AN=150 | AN=200 | AN=300 | AN=500 |
|---|---|---|---|---|---|
| 40 | 1,42 | 1,25 | 1,17 | 1,08 | 1,01 |
| 50 | 1,31 | 1,16 | 1,09 | 1,02 | 0,96 |
| 60 | 1,22 | 1,10 | 1,04 | 0,98 | 0,92 |
| 70 | 1,16 | 1,05 | 1,00 | 0,94 | 0,90 |
| 80 | 1,11 | 1,01 | 0,96 | 0,91 | 0,87 |
| 90 | 1,07 | 0,98 | 0,94 | 0,89 | 0,86 |

**Anlage 6 — Dezentrale elektrische Direktheizung, Lueftungsanlage, dezentrale Trinkwassererwaaermung:**
- Heizung: Direktheizung mit Einzelraumregelung, dezentral elektrisch
- Trinkwarmwasser: dezentral, Elektro-Kleinspeicher und Durchlauferhitzer innerhalb th. H.
- Lueftung: zentrale Zu-/Abluftanlage; Luftauslaesse im Aussenbereich ohne Einzelraumregelung mit zentraler Vorregelung; innerhalb th. H.; Abluft-/Zuluft-Waermepumpe; Luftwechsel n = 0,4 h⁻¹; DC-Ventilator; Waermerueckgewinnung durch Waermeuebertraeger, Waermebereitstellungsgrad 60 %; innerhalb th. H.

e_P-Tabelle (Tabelle 8.39):

| q_h | AN=100 | AN=150 | AN=200 | AN=300 | AN=500 |
|---|---|---|---|---|---|
| 40 | 1,89 | 1,88 | 1,88 | 1,87 | 1,86 |
| 50 | 1,93 | 1,92 | 1,92 | 1,91 | 1,91 |
| 60 | 2,00 | 1,99 | 1,99 | 1,98 | 1,98 |
| 70 | 2,07 | 2,06 | 2,05 | 2,05 | 2,05 |
| 80 | 2,14 | 2,13 | 2,13 | 2,13 | 2,13 |
| 90 | 2,21 | 2,21 | 2,20 | 2,20 | 2,20 |

---

### Heizlast nach DIN EN 12831 (ab 1.8.2003, ersetzt DIN 4701-1 bis -3)

**Norm-Heizlast** bezeichnet die Waermemenge in W oder kW, die notwendig ist, um einen bestimmten Temperaturzustand herzustellen. Der frueherer Begriff "Waermebedarf Q" wurde durch "Norm-Heizlast Phi_HL" ersetzt.

**Standardfaelle:** Alle Gebaeude mit max. 5 m Raumhoehe und stationaer zu beheizenden Bedingungen. Sonderfaelle (z.B. Kirchen, Hallenbauten) erfordern Sonderberechnungen.

**Vereinfachtes Berechnungsverfahren:** Anwendbar fuer Wohngebaeude bis 3 Wohneinheiten mit Luftdichtheit n50 ≤ 3 h⁻¹.

**Ausfuehrliches Berechnungsverfahren:** Fuer Wohngebaeude, Buero-/Verwaltungsgebaeude, Schulen, Bibliotheken, Krankenhaeuser, Kurheime, Hotels/Gaststaetten, Warenhaeuser, Industriegebaeude mit normalen Geschosshoehen und weitgehend konstanter Beheizung.

**Grundgleichung pro Raum:**
Phi_i = Phi_T,i + Phi_V,i [W]

Summe aller Raumheizlasten = Gesamtheizlast Gebaeude.

**Formblattstruktur nach DIN EN 12831:**
- G1: allgemeine Gebaeudedaten
- V: Vereinbarungen (temperaturrelevante Raumdaten mit Nutzer/Auftraggeber abzustimmen)
- R: Raumberechnungen
- G2: Raumzusammenstellung
- G3: Gebaeudezusammenstellung

**Berechnungsgrundlagen (erforderliche Unterlagen):**
- Lageplan mit Himmelsrichtung, geographischer Lage, Windanfall, Nachbargebaeudehöhen
- Grundriss-/Schnitt-/Ansichtszeichnungen mit allen Massen
- Raumnutzung und Innentemperaturen
- Wandaufbau, Deckenkonstruktion, Dachkonstruktion (Material und Aufbau)
- Fensterdaten: Konstruktionsart, Verglasung, Rahmenmaterial, Fugenanzahl/-laenge
- Aussentuer-Daten: Konstruktionsart, Material, Verglasungsanteil, Fugenanzahl/-laenge

### G1-Gebaeudedaten: Kenngroessen und Parameter

**Gebaeudetyp:** Bestimmt n50-Wert fuer Luftdurchlaessigkeit.

**Gebaeude-Abschirmungsklassen:**
- Gute Abschirmung: mittlere Gebaeude in Stadtzentren oder bewaldete Lagen
- Moderate Abschirmung: Gebaeude im Freien umgeben von Baeumen oder anderen Gebaeuden, Vorstaedte
- Keine Abschirmung: windreiche Gegenden, Hochhaeuser in Stadtzentren

**Gebaeude-Luftdichtheit:**
- Sehr dicht: hoch abgedichtete Fenster und Tueren
- Dicht: Doppelverglasung, normale Abdichtung
- Weniger dicht: Einfachverglasung, keine Abdichtung

**Luftdurchlaessigkeitswerte n50 (Tabelle 8.44, DIN EN 12831):**

| Konstruktionstyp | sehr dicht [h⁻¹] | dicht [h⁻¹] | weniger dicht [h⁻¹] |
|---|---|---|---|
| Einfamilienhaeuser | 3 | 6 | 9 |
| Mehrfamilienhaeuser, Nicht-Wohngebaeude | 2 | 4 | 6 |

Hinweis: Bei Hochhaeusern koennen in unteren Geschossen erheblich hoehere Werte auftreten (z.B. Schachttyp) — Einzelfallpruefung erforderlich.

**Aussentemperaturen:**
- Norm-Aussentemperatur theta_e: tiefstes Zweitagesmittel das 10× in 20 Jahren erreicht/unterschritten wird, je nach geographischer Lage
- Jahresmittel Aussentemperatur theta_m,e: fuer Erdreichwaermeverluste
- Beide aus Tabelle 8.40 (DIN EN 12831 Beiblatt 1)

**Norm-Aussentemperaturen ausgewaehlter Staedte (Tabelle 8.40):**

Beispiele (Format: Klimazone / theta_e [°C] / theta_m,e [°C]):
- Aachen: 5 / −12 / 8,1
- Berlin: 4 / −14 / 9,5
- Hamburg: 3 / −12 / 8,5
- Koeln: 5 / −10 / 8,1
- Muenchen: 13 / −16 / 7,9
- Stuttgart: 12 / −12 / 10,2
- Frankfurt/Main: 12 / −12 / 10,2
- Hannover: 3 / −14 / 8,5
- Nuernberg: 6 / −14 / 6,8
- Dresden: 4 / −14 / 9,5
- Leipzig: 4 / −14 / 8,7
- Duesseldorf: 5 / −10 / 8,1
- Bremen: 3 / −12 / 8,5
- Heidelberg: 12 / −10 / 10,2
- Freiburg i. Br.: 12 / −12 / 10,2
- Garmisch-Partenkirchen: 15 / −18 / 6,8
- Hof/Saale: 11 / −18 / 3,0
- Feldberg Schwarzwald: 11 / −18 / 3,0
- Oberstdorf: 15 / −20 / 6,8
- Bremerhaven: 1 / −10 / 9,0

Die vollstaendige Tabelle umfasst alphabetisch ca. 200 deutsche Orte mit jeweils Klimazone, theta_e und theta_m,e. Fuer nicht aufgefuehrte Orte: Naechstgelegenen Ort aehnlicher Klimalage waehlen (Isothermenkarte 8.41 als Orientierung). Grundsatz: Temperaturen in °C ohne Nachkommastellen, gerundet.

**Norm-Innentemperaturen (Tabelle 8.42, DIN EN 12831 Beiblatt 1):**

| Raumart | theta_int [°C] |
|---|---|
| Wohn- und Schlafraum | +20 |
| Bueroraum, Sitzungszimmer, Ausstellungsraum, Treppenraum, Schalterhalle | +20 |
| Hotelzimmer | +20 |
| Verkaufsraeume/Laeden | +20 |
| Unterrichtsraeume | +20 |
| Theater-/Konzertraeume | +20 |
| Bade-/Duschraum, Baeder, Umkleideraeume, Untersuchungszimmer (unbekleideter Bereich) | +24 |
| WC-Raeume | +20 |
| Beheizte Nebenraeume (Flure, Treppenhaeuser) | +15 |
| Unbeheizte Nebenraeume (Keller, Abstellraeume) | +10 |

### Erdreich-Parameter (G1)

- Tiefe Bodenplatte z: Abstand Gelaendeoberflaeche bis Unterkante Bodenplatte — aus Planunterlagen
- Umfang P: Erdreich-beruehrender Umfang der Bodenplatte; bei Teilgebaeuden nur Aussenwaende zur Umgebung
- Parameter B': B' = A_Geb / (0,5 · P) — kann gebaeude- oder raumweise bestimmt werden
  - Verwendung Gebaeudewert fuer alle Raeume ohne Aussenwaende oder gut gedaemmte Boeden (U_boden < 0,5 W/(m²·K))
  - Raumweise Berechnung fuer alle anderen Raeume (sicherste Methode)
- Grundwassertiefe T: Abstand Grundwasserspiegel zur Fundamentplatte
- Korrekturfaktor periodisch fg1 = 1,45 (jaehrliche Schwankung Aussentemperatur, Deutschland)
- Korrekturfaktor Grundwasser G_W:
  - Abstand Grundwasserspiegel ≥ 3 m: G_W = 1,00
  - Abstand Grundwasserspiegel < 3 m: G_W = 1,15

Beispiel B'-Bestimmung (Tabelle 8.43):
- a) A_g = 150 m², P = 50 m → B' = 6
- b) A_g = 75 m², P = 15 m → B' = 10

### Lueftungsparameter (G1)

**Gleichzeitig wirksamer Lueftungsanteil zeta_v:** Standardannahme 0,5; Sonderfaelle (Hallen/Einraumgebaeude): 0,5 bis 1,0.

**Waermerueckgewinnung:** Wenn vorhanden — Wirkungsgrad eta_v des Systems (Herstellerangabe) in Berechnung einbeziehen.

### Zusatz-Aufheizung und Wiederaufheizfaktoren

Bei Heizungsunterbrechung (Nacht-/Wochenendabsenkung) sinken Raumtemperatur und Bauteiltemperaturen. Beim Wiederaufheizen muss erhoehte Waermemenge zugefuehrt werden — erfasst durch Wiederaufheizfaktor f_RH.

**Kein Wiederaufheizfaktor erforderlich:**
- Wenn Anlage durchgehenden Heizbetrieb an kaeltesten Tagen sicherstellt
- Wenn andere Normen Heizlast bereits beruecksichtigen (dann Netto-Heizlast zugrunde legen)

**Absenkphase — Temperaturabfall Delta_theta_RH:**
Delta_theta_RH = (theta_int,i - theta_e) · (1 - e^(-t_Abs/tau))

- Raumzeitkonstante tau = c_wirk / H_abs
- Waermeverlustkoeffizient Absenkphase: H_abs = (H_T/V_i) + 0,34 · n
- n_Abs: Luftwechselrate Absenkphase: 0,1 h⁻¹ (reduziert) bis 0,5 h⁻¹ (durchgaengig)
- t_Abs Absenkdauer: individuell festlegen, z.B. 8 h bei Nachtabsenkung

Erfahrungswerte Innentemperaturabfall bei 8 h Nachtabsenkung:
- Schwere, gut gedaemmte, luftdichte Gebaeude: ca. 1-2 K
- Buerounterbrechungen/Urlaubsunterbrechung: 3-7 K (laengere Wiederaufheizzeit empfohlen)

**Abschirmungskoeffizient e fuer Aufheizphase (Tabelle 8.45, DIN EN 12831):**

| Abschirmungsklasse | 0 Oeffnungen | 1 Oeffnung | 2 Oeffnungen | 3 Oeffnungen | >3 Oeffnungen |
|---|---|---|---|---|---|
| Keine Abschirmung | 0 | 0,05 | 0,10 | 0,15 | +0,05 je |
| Moderate Abschirmung | 0 | 0,03 | 0,06 | 0,09 | +0,03 je |
| Gute Abschirmung | 0 | 0,01 | 0,02 | 0,03 | +0,01 je |

**Wiederaufheizfaktoren f_RH [W/m²] (Tabellen 8.46 und 8.47):**

Tabelle 8.46 — Luftwechselrate n = 0,1 h⁻¹ (nur Fugenlueeftung):

| Wiederaufheizzeit [h] | 1 K — l/m/s | 2 K — l/m/s | 3 K — l/m/s | 4 K — l/m/s | 5 K — l/m/s | 7 K — l/m/s |
|---|---|---|---|---|---|---|
| 0,5 | 12/12/12 | 27/28/28 | 39/44/44 | 50/59/60 | —/—/— | —/—/— |
| 1 | 8/8/8 | 18/21/21 | 26/34/34 | 33/47/48 | —/—/— | —/—/— |
| 2 | 5/5/5 | 10/15/15 | 15/25/25 | 20/34/35 | 43/81/88 | 61/117/126 |
| 3 | 3/3/3 | 7/12/12 | 9/19/20 | 14/28/30 | 33/70/79 | 47/103/112 |
| 4 | 2/2/2 | 5/9/10 | 7/17/19 | 10/25/27 | 28/63/72 | 38/92/102 |

Tabelle 8.47 — Luftwechselrate n = 0,5 h⁻¹ (geringe Fensterlueeftung/Aussenluftdurchlaesse/RLT):

| Wiederaufheizzeit [h] | 1 K — l/m/s | 2 K — l/m/s | 3 K — l/m/s | 4 K — l/m/s | 5 K — l/m/s | 7 K — l/m/s |
|---|---|---|---|---|---|---|
| 0,5 | 14/17/18 | 29/34/35 | 44/52/53 | 58/68/70 | —/—/— | —/—/— |
| 1 | 10/13/14 | 21/27/28 | 32/42/44 | 41/55/57 | —/—/— | —/—/— |
| 2 | 7/10/11 | 13/21/23 | 21/32/34 | 28/42/44 | 47/89/99 | 67/125/137 |
| 3 | 5/9/10 | 10/18/20 | 15/26/28 | 21/35/38 | 37/78/89 | 53/110/122 |
| 4 | 4/8/9 | 8/16/18 | 13/24/26 | 17/32/35 | 31/70/81 | 43/99/111 |

Legende: l = leicht, m = mittelschwer, s = schwer (Gebaedemasse)

### Vereinbarungen (Formblatt V)

Alle temperaturrelevanten Raumdaten sind mit Nutzer/Auftraggeber abzustimmen:
- Raeume nummerieren und Nummerierung in Planunterlagen und Formblatt eintragen
- Raumbezeichnung und -nutzung fuer jeden Raum festlegen
- Norm-Innentemperatur pro Raum (Tabelle 8.42 als Richtwert)
- Heizunterbrechungsdauer und Wiederaufheizzeit festlegen (global oder raumweise)
- Bei globalem Wiederaufheizfaktor: beheiztes Gebaeudevolumen V_N,Ge und Transmissionswaermeverlustkoeffizient Sigma_H_T,e aus Formblatt G3 nach Abschluss der Berechnung entnehmen
