# Gebäudetechnik und Technischer Ausbau von Gebäuden — Teil 4
> Quelle: Gebäudetechnik und Technischer Ausbau von Gebäuden (buecher) · Seiten 161-200.

Dieser Teil schließt Kapitel 3 (Abwasser- und Wassertechnik) ab — mit Dränagebemessung, Trinkwasserversorgung, Warm­wasser­bereitung und Feuerlöschanlagen — und beginnt Kapitel 4 (Wärme- und Kälteversorgungs­anlagen) mit der Heizlast­berechnung nach DIN EN 12 831.

## Inhalt

### 3.3 Gebäudedränung — Bemessung und Ableitung (Seiten 161-163)

#### Senkrechte Dränschichten
- Mineralische Dränschichten (Sand, Kies): Mindestabmessungen für den **Regelfall** nach Tab. 3.34; Regelfall ist in Tab. 3.33 definiert (Einbautiefe bis 3 m, Gebäudehöhe 3–6 m, keine Hanglage u. a.).
- Abweichungen vom Regelfall → **Sonderfall**: DIN 4095 verlangt Eignungsnachweis; DIN 4095 ist bisher nicht allgemein bauaufsichtlich eingeführt.
- Nichtmineralische verformbare Dränelemente (EPS-Dränplatten, Dränmatten): Auch im Regelfall ist nachzuweisen, dass eine Abflussspende von **≥ 0,30 l/(s·m)** abgeführt werden kann — ermittelt für Zustand nach **50 Jahren** unter dem einbautiefenbedingten Erddruck (Kunststoffe unterliegen druckabhängiger Stauchung und zeitabhängiger Verformung). Dimensionierung i. d. R. nach Herstellerkatalogen oder EDV-Programmen.

#### Dränschichten unter Bodenplatten
- Regelfall: bebaute Fläche ≤ **200 m²** bei geringer Bodendurchlässigkeit.
- Flächendränungen > 200 m²: Sonderfall, eingebettete Dränleitungen (Sauger) erforderlich.
  - Mit Stufenfilter (≥ 15 cm Kies 8/16 + Geotextil): Abstände der Sauger ~**12 m**.
  - Mit Mischfilter (z. B. 30 cm Kiessand Sieblinie B 32): Abstände **2,5–8 m** je nach Wasserandrang.
- Hydraulische Berechnung bei Flächen > 200 m² erfordert Fachingenieur oder Hersteller-EDV-Programme; DIN 4095 gibt hierfür keine vollständige Anleitung.

**Tab. 3.36 — Anzunehmender Wasseranfall bei Flächendränungen (DIN 4095):**

| Zufluss | Bodenart | Abflussspende q′ [l/(s·m)] |
|---------|----------|--------------------------|
| Gering | Sehr schwach durchlässige Böden | < 0,001 |
| Mittel | Schwach durchlässige Böden | 0,001–0,005 |
| Groß | Durchlässige Böden | 0,005–0,010 |

#### Dränrohrbemessung — Berechnungsbeispiel
Beispiel (Hanglage, Sonderfall):
- Einbautiefe bis 3 m, Gebäudehöhe 3–6 m
- Bergseitig: großer Wasserzudrang 0,30 l/(s·m); übrige Seiten: mittlerer Zudrang 0,10 l/(s·m)
- Gefälle: 0,5 %; keine Flächendränung unter Bodenplatte
- EPS-Dränplatten mit Nachweis ≥ 0,30 l/(s·m) in 3 m Tiefe

Berechnungsresultate (Abschnitte A–B, B–C, A–D, C–D, C–E):
- A–B: 17 m × 0,30 = 5,1 l/s → DN 125
- B–C: 0,8 + 5,1 = 5,9 l/s → DN 160
- A–D: 8 m × 0,10 = 0,8 l/s → DN 100
- C–D: 1,7 + 0,8 = 2,5 l/s → DN 100
- C–E: 5,9 + 2,5 = 8,4 l/s → DN 160

**Tab. 3.37 — Anhaltswerte Dränrohrbemessung (DIN 4095) und max. Rohrlängen bei 0,5 % Gefälle (opti-drän-Rohre):**

| Zufluss | Bodenart | q′ [l/(s·m)] | Max. Länge ø100 | Max. Länge ø125 | Max. Länge ø200 | Max. Länge ø300 |
|---------|----------|--------------|-----------------|-----------------|-----------------|-----------------|
| Gering | Sehr schwach durchlässig | < 0,05 | 50 m | 100 m | 200 m | 300 m |
| Mittel | Schwach durchlässig | 0,05–0,10 | 25–50 m | 50–100 m | 100–200 m | 150–300 m |
| Groß | Schichtwasser/Stauwasser | 0,10–0,30 | 10–25 m | 15–50 m | 30–100 m | 50–150 m |

#### Ableitung des Dränwassers
- Gemäß DIN 1986-100: Dränwasser darf nur in **Regenwasserkanäle** oder in **Gewässer** eingeleitet werden — behördliche Zustimmung erforderlich (kann verweigert werden, frühzeitige Rückfrage empfohlen).
- Anschluss an **Mischkanalisation** ist **unzulässig** (rückstauendes Mischwasser hinterlässt Ablagerungen von Schmutz­stoffen und Fäkalien in der Dränanlage).
- Alternative: Versickerung auf dem Grundstück:
  - Untergrundverrieselung
  - Sickerschächte (behördliche Zustimmung nötig)
  - Mulden- oder Rohrrigolen nach DWA-A 138
- Versickerungsanlagen: **mind. 6 m** Abstand von unterkellerten Gebäudeteilen (DWA-A 138).
- Rigolen nach DWA-A 138: wasseraufnahmefähige Kiespackungen (z. B. Betonierkies B 32 nach DIN 1045), Zufuhr über perforiertes Rohr DN 300; zusätzlich Kontrollschacht mit Entlüftungsöffnungen.
- Sohle des Sickersammlers: **mind. 50 cm** unterhalb des Einlaufs (wirkt als Absetzbecken für Bodenteilchen).
- Rückstaugefahr: Dränwasser in Grube sammeln + Hebeanlage (Unterwasserpumpe) bis über Rückstauebene (meist OK Bordstein).
- Rückstauklappen bieten keinen sicheren Schutz, da mitgeführte Feststoffe die Klappe offen halten können.
- Hebeanlagen innerhalb von Gebäuden: ständige Betriebsbereitschaft durch Notstromaggregat oder benzinbetriebene Reserve­pumpe sicherstellen.
- DIN 4095: Dränanlage in Bauplänen darstellen (Lage, Art der Baustoffe, Dicke, Sohlenhöhen, Abmessungen); nach Verfüllung Funktionsprüfung der Dränleitungen (z. B. Spiegelung) und Protokollierung.

---

### 3.4 Wasseranlagen (Seiten 163–184)

#### 3.4.1 Wasserbeschaffenheit
- Trinkwasser aus öffentlichem Netz: hygienisch einwandfrei, kristallklar, geruch- und geschmacklos (außer etwaigen Chlorbeimischungen), Temperatur **7–17 °C**.
- Zapfstellen für Nichttrinkwasser (Brauch-/Betriebswasser) müssen gekennzeichnet sein.
- **Wasserhärte:**
  - Bisherige Einheit °dH: 1 °dH = 0,179 mmol/l; 1 mmol/l = 56 mg CaO/l bzw. 40 mg MgO/l Wasser
  - Gesetzliche Einheit heute: mmol/l (mol/m³) nach Gesetz über Einheiten im Messwesen
  - Drei Härtebereiche nach Wasch- und Reinigungsmittelgesetz (WRmG):

**Tab. 3.38 — Härtebereiche und Maßnahmen:**

| Härtebereich | Gesamthärte [mmol/l CaO] | Maßnahmen ≤ 60 °C | Maßnahmen ≥ 60 °C |
|---|---|---|---|
| 1 — Weich (bis ca. 8,4 °dH) | < 1,5 | Keine | Keine |
| 2 — Mittel (ca. 8,4–14 °dH) | 1,5–2,5 | Keine | Keine |
| 3 — Hart (über 14 °dH) | > 2,5 | Keine/Stabilisierung | Stabilisierung/Enthärtung |

- Nachteil großer Wasserhärte: Mehrverbrauch Waschmittel, Kalkschleier beim maschinellen Spülen, Inkrustationen (Kesselstein) in Rohren und Geräten, besonders ab **60 °C** Wassertemperatur (dort Störung des Kalk-Kohlensäure-Gleichgewichts).
- Nachteil zu geringer Wasserhärte: Korrosion metallischer Rohre; Korrosionsgeschwindigkeit verdoppelt sich bei Temperaturerhöhung um **10 K** → Wassertemperatur auf max. **50–60 °C** begrenzen.
- **pH-Wert** nach TrinkwV: nicht unter **6,5**, nicht über **9,5**.
  - pH < 7: saures Wasser; pH 7: neutral; pH > 7: alkalisch
  - Unter pH 6,5 + Kupfer- oder verzinkte Stahlrohre + längere Verweilzeit (≥ 12 h): gelöstes Kupfer/Zink kann für Säuglinge gesundheitsgefährdend sein.
  - Ab pH > 7 (Regelfall Trinkwasser): Einsatz von unverzinntem Kupferrohr und normgerecht verzinkten Stahlrohren unbedenklich.
  - Bleileitungen gelten als erheblich gesundheitsgefährdend auch bei normalem pH-Wert > 7.

#### 3.4.2 Wasseraufbereitung
- Nachaufbereitung im Wohnungsbau: strenge Maßstäbe anlegen (unsachgemäße Wartung führt zu Verkeimung oder falscher Dosierung von Chemikalien).
- **Schutz gegen Kalkablagerungen:**
  - Enthärtung ab ~**16 °dH** (2,5 mmol/l) sinnvoll; ab **21 °dH** (3,8 mmol/l) technisch notwendig (wenn WW-Temperatur > 60 °C).
  - Vollentsalzung auf 0 mmol/l nicht empfehlenswert (Geschmackseinbußen, vermutlich Herzerkrankungsrisiko). TrinkwV: nach Enthärtung mind. **1,5 mmol/l (8 °dH)** einhalten.
  - **Härtestabilisierung durch Phosphat-Dosierung (Impfung):** Verhindert festsitzende Kalkschichten durch Anlagerung langkettiger Phosphatmoleküle; wirksam bis **17 °dH (3,0 mmol/l)** und bis **75 °C**; geringer Platzbedarf, fast wartungsfrei, geringe Kosten; baut Korrosionsschutzschicht an Rohrin­nen­wandungen auf; zu hohe Dosierung kann Gesundheitsprobleme aufwerfen + belastet Abwässer.
  - **Enthärtung durch Ionenaustausch:** Kunstharz­kügelchen tauschen Natrium- gegen Kalziumionen; periodische Regeneration mit Kochsalzlösung; Kompaktgeräte für Wohngebäude ~ Größe einer Waschmaschine; diskontinuierlicher Betrieb + unsachgemäße Wartung begünstigt Keimwachstum; Salzbelastung der Abwässer.
  - **Membranverfahren (Nanofiltration):** Entfernt partikuläre und zweiwertige Ionen (Härtebildner); komplex und aufwändig; 15–30 % Abwasseranfall je Liter enthärteten Wassers.
  - **Physikalische Wasserbehandlung** (Magnet-/Elektrofeldsysteme, elektrochemische und elektrogalvanische Systeme, heterogene Katalyse): Wirkungsweise nicht ausreichend erforscht; DVGW hat bis dato keine Empfehlungen veröffentlicht.
- **Schutz gegen Korrosion:** Entsäuerung oder kathodischer Korrosionsschutz nur bei sehr weichem Wasser (0,2–0,3 mmol/l) mit hohem Kohlensäuregehalt oder im gewerblichen/industriellen Bereich.
- **Mechanische Filter:** Einbau bei metallenen Leitungen obligatorisch (DIN 1988-2), bei Kunststoffleitungen empfohlen; Filterschärfe 0,05 mm hält Sand-, Kalk- und Rostpartikelchen zurück; Filter unmittelbar hinter Wasserzähleranlage, vor erstmaliger Füllung montieren; regelmäßige Wartung (sonst Keimbildung am Filtereinsatz).
- **Enteisenung, Entchlorung, Vollentsalzung:** Für industriell-gewerbliche Zwecke; vollentsalztes Wasser erfordert Kunststoffleitungen und Edelstahlbehälter.

#### 3.4.3 Rohrleitungsmaterial
- Kupfer, Stahl, Kunststoff → > 20 Systeme; Unterschiede hauptsächlich in Verbindungstechniken (Löten, Klemmen, Pressen, Schweißen, Schrauben).

**Marktanteile (ungefähre Werte):**
- Kupfer: 60 %
- Verzinkter Stahl: 13 %
- Kunststoff: 22 %
- Edelstahl: 3 %
- Mehrschicht-Systeme: 2 %

- **Kupferrohre** (häufigste Anwendung): relativ korrosionsunempfindlich. Empfehlungen für Abmessungen 12×1 bis 28×1,5 mm (AD×Wandstärke): Weichlöten statt Hartlöten oder Kaltverbindungen per Pressfitting; Kaltbiegen statt Warmbiegen. PE-Ummantelung reduziert Schallübertragung, Wärmeverluste, Tauwasserbildung.
- **Verzinkte Stahlrohre**: preisgünstiger; nicht biegbar (Korrosionsbeschichtung); Tempergussfittings bei Richtungsänderungen. Bei Mischinstallation: Stahlrohr **niemals** in Fließrichtung **hinter** Kupferrohren oder kupfernen Bauteilen einbauen.
- **Bleirohre**: für Trinkwasser nicht zugelassen; in Gebäuden vor 1935 (teils bis 1973) verbaut → ersetzen.
- **Edelstahlrohre** (AD 15–54 mm, Pressfitting): weitgehend korrosionsbeständig, hygienisch, einfach verarbeitbar; Mischinstallation beeinflusst Korrosionsbeständigkeit nicht, aber an unlegiertem feuerverzinkten Stahl kann Kontaktkorrosion auftreten.
- **Kunststoffrohre**: absolut korrosionsunempfindlich, resistent gegen Inkrustationen, geringere Geräuschemission; i. A. ungeeignet für Dauerbetrieb > **60 °C** (Thermoplaste); große Wärmedehnung → Ausdehnungsbögen, gleitende Rohrschellen mind. 50 cm vor Richtungsänderungen, Spielraum in Wandschlitzen. Gebräuchliche Typen: PE-X (vernetztes Polyethylen), PB (Polybuten), PVC-C (nachchloriertes PVC), PP-C (nachchloriertes PP), Mehrschichtenrohr (PE-X innen, Aluminiumschicht, PE-HD außen), Rohr-in-Rohr (PE-X in gewelltem PE-Schutzrohr).
- **Rohr-in-Rohr-Systeme**: bevorzugt in Vorwandinstallationen, Leichtbauständerwänden, Fußbodenebene unter schwimmendem Estrich, auch einbetonierbar; Mindestbiegeradius **15 cm**; DVGW-Zulassung für Trinkwasserinstallation prüfen.

#### 3.4.4 Hausanschluss
- Bis Wasserzähler: Aufgabe des Wasserversorgungsunternehmens (WVU); frühzeitiger Wasserlieferungsantrag durch Bauherrn.
- Anschlussleitungen: nicht überbaubar, kürzester Weg von Versorgungsleitung zum Gebäude, möglichst geradlinig und rechtwinklig zur Grundstücksgrenze, nicht über Nachbargrundstücke.
- Jedes Grundstück erhält eigenen Anschluss.
- Abstand Trinkwasserleitung zu Abwasserleitung: wenn < **1 m**, Abwasserleitung tiefer als Trinkwasserleitung verlegen.
- Abstand zu anderen Rohrleitungen oder Kabeln < **20 cm** (Außenflächen): Trinkwasserleitung in Schutzrohr verlegen oder andere Schutzmaßnahmen (DIN 1988-100 und -200; DIN EN 805).
- **Überdeckungshöhe** (DIN EN 805): in der Regel **1,0–1,8 m** (je nach Klima, Nennweite, Bodenverhältnissen).
- Gebäudeeinführung: Mantelrohr in Außenwand; Zwischenraum gas- und wasserdicht mit dauerelastischen/plastischen Füllmitteln verfüllen.
- Bevorzugtes Material für Anschlussleitungen: PE (korrosionsunempfindlich, elastisch). Metallische Anschlussleitungen: Korrosionsschutz im Bereich der Gebäudeeinführung.
- **Wohnungszähler**: jede Wohnung/Nutzungseinheit erhält eigenen Wasserzähler; in frostfreiem Raum (Hausanschlussraum mit straßenseitiger Außenwand).
- Wasserzählerschächte außerhalb Gebäude: lichte Mindestabmessungen für Anschlussleitungen bis DN 40: **1,20 × 1,00 m** bei mind. **1,80 m** Höhe und mind. **70 cm** breitem Einstieg.

#### 3.4.5 Leitungsinstallation in Gebäuden
- Hinter Wasserzähler: 2 Absperrventile (für Zählertausch) + Entleerungsventil + Rückflussverhinderer.
- Verteilerbatterie: Stränge übersichtlich beschildert, einzeln absperrbar und entleerbar; Stockwerksleitungen zweigen ab **mind. 1,10 m** über OK Fußboden.
- Je Geschoss/Wohnung: eigene Absperreinrichtung.
- Zapfstellen: mind. **40 mm** Abstand zwischen Auslauf und höchstmöglichem Wasserspiegel darunter liegender Becken/Wannen.
- Bei Bidets, Wasch- und Spülmaschinen: Durchfluss-Rohrbelüfter gegen Rücksaugen.
- Übliche Nennweiten Wohnungsbau: DN 15, 20, 25 (mm) bzw. 1/2″, 3/4″, 1″; Kupferrohr 15×1, 22×1,5, 28×1,5 mm.
- **Druckabfall-Schutz** (Rohrbruch, Pumpenausfall): Rückflussverhinderer, Rohrbelüfter oder Rohrtrenner nach DIN 1988.
- Schallschutz: Rohrschellen mit elastischer Dämmeinlage; in Wandschlitzen verdeckte Rohrstränge mit Dämmstoffen umhüllen.
- **Wärmedämmung** (DIN 1988-200): immer erforderlich — nicht nur in Außenwandschlitzen, auch gegen Schwitzwasserbildung und Erwärmung des Trinkwassers im Bereich von Wärmequellen.

**Tab. 3.39 — Mindestdämmschichtdicken für Kaltwasserleitungen (DIN 1988-200, λ = 0,040 W/(m·K), bezogen auf d = 20 mm):**

| Einbausituation | Dämmschichtdicke |
|---|---|
| Frei verlegt, nicht beheizte Räume, Umgebungstemperatur ≤ 20 °C (nur Tauwasserschutz) | 9 mm |
| Rohrschächte, Bodenkanäle, abgehängte Decken, Umgebungstemperatur ≤ 25 °C | 13 mm |
| Stockwerksleitungen und Einzelzuleitungen in Vorwandinstallationen | Rohr-in-Rohr oder 4 mm |
| Stockwerksleitungen im Fußbodenaufbau (auch neben nicht zirkulierenden WW-Leitungen) | Rohr-in-Rohr oder 4 mm |
| Stockwerksleitungen im Fußbodenaufbau neben warmgehenden zirkulierenden Rohrleitungen | 13 mm |

- Kaltwasserleitung bei horizontaler Führung: nicht oberhalb anderer Leitungen, um Abtropfen von Schwitzwasser zu vermeiden.
- Frostgefährdete Leitungen: im kritischen Bereich entleerbar oder anderweitig schützen (Begleitheizung); Frostsichere Armaturen (langer Spindelschaft) montieren Ventil tief in der Wand außerhalb Frostbereich, selbstentleerend beim Schließen.
- **Rohrbelüfter Bauart E** (an oberen Enden von Steigleitungen): lässt beim Füllen Luft entweichen; verhindert bei Reparaturen Unterdruck und Rücksaugen von Wasser aus angeschlossenen Geräten; Tropfwasserleitungen mind. DN 20 über Geruchverschluss an Entwässerung anschließen.
- **Rohrbelüfter Bauart D** (ohne Tropfwasserleitung, DIN 1988-200): nur zulässig, wo austretendes Wasser keinen Schaden anrichten kann (z. B. geschlossene Duschkabinen).
- Nach Fertigstellung: Dichtheitsprüfung + gründliche Spülung (filtriertes Wasser, nach Installation des Feinfilters); bis Übergabe Leitungen vollständig mit Wasser füllen (Teilfüllung → Dreiphasen-Grenzlinie → Oxidschichten → weitere Korrosion).

#### 3.4.6 Wasserdruck
- Ruhedruck: statischer Überdruck ohne Wasserentnahme (netzdruckabhängig).
- Fließdruck: statischer Überdruck während Entnahme (niedriger als Ruhedruck).
- **Erforderliche Mindest-Fließdrücke:**
  - Alle Zapfventile: ≥ **0,5 bar**
  - Elektrische Durchlauferhitzer ab 9/18 kW: ≥ **1,0 bar**
  - Druckspüler Nennweite 20 (gängig): ≥ **1,2 bar**
  - Angestrebter Mindestfließdruck (Druckschwankungen): **1,5 bar**
- Schalldämmnorm DIN 4109: Obergrenze **5 bar**.
- Ab **6 bar**: Sicherheitsventile elektrischer Warmwasserbereiter sprechen an.
- Druckabnahme/­zunahme grob: **1 bar pro 10 m** Höhenunterschied.
- Reibungswiderstände: ca. **0,15–0,03 bar/m** Rohrleitung.
- Wasserzählerwiderstand: ca. **0,5 bar**; Filterwiderstand: ca. **0,2 bar**.
- Hochhaus: am obersten Hydranten der Feuerlöschsteigleitung im Regelfall **mind. 3 bar** Ruhedruck; an oberen Zapfstellen möglichst nicht unter **1,5 bar**, an tiefer liegenden nicht über **5 bar** → mehrere Druckzonen.

#### 3.4.7 Leitungsdimensionierung
Überschlägliche 8-Schritt-Berechnung:
1. Mindestversorgungsdruck nach Druckminderer/DEA ermitteln (pmin)
2. Geodätischer Druckverlust (pgeo, 1 bar/10 m)
3. Druckverlust in Apparaten (Zähler, Filter, Enthärtung) schätzen (pA)
4. Mindestfließdruck der Zapfstellen festlegen (pmin FI)
5. Druckverlust Stockwerks- und Einzelzuleitungen schätzen (pSt)
6. Einzelwiderstände prozentual schätzen
7. Summe aller Druckverluste (Ziff. 2–6)
8. Verfügbarer Druck = pmin − Summe; aus Rohrreibungsdiagramm (DIN 1988) Rohrdurchmesser ermitteln (vereinfacht: Tabellen DIN 1988-300).

#### 3.4.8 Wasserdruckerhöhungsanlagen
- Wird installiert wenn Versorgungsdruck nicht ausreicht (auch bei Eigenversorgung oder Regenwasserspeicherung).
- **Behälteranlagen**: Druckkessel + Pumpen; Druckreservoir aus Wasser + komprimierter Luft (Luftpolster dämpft Druckstöße); Platzbedarf: ca. **1,5–2,5 m²**.
- **Behälterlose Durchlaufanlagen**: mehrere drehzahlgeregelte Kreiselpumpen in Kaskadenschaltung, druckstoßfrei; Platzbedarf ca. **0,5–2 m²**.
- Bei Pumpenausfall: weitere Pumpe muss einschalten und Störung anzeigen.
- Aufstellraum: belüfteter Kellerraum, nicht in unmittelbarer Nähe von Schlaf-/Wohnräumen; schallgedämmte Aufstellung; ausreichend bemessener Entwässerungsanschluss.
- Bemessung nach DIN 1988 bzw. DIN EN 806.

#### 3.4.9 Regenwasser- und Grauwassernutzungsanlagen

**Regenwassernutzung:**
- In Deutschland > 95 % der Gebäude an öffentliches Trinkwassernetz angeschlossen; Grundwasserspiegel sinkt durch technische Eingriffe.
- Nutzungsmöglichkeiten von Regenwasser: Toilettenspülung/Urinale (Hauptanwendung), Wäschewaschen, Gartenbewässerung. Grauwasser: ungeeignet für Wäsche und Garten.
- Vorteile: Trinkwasserersparnis, Kanalentlastung, Abflachung von Abflussspitzen.
- Speichergröße für Dreipersonenhaushalt: **2000–3000 l** (ca. **800–1000 l/Person**); Verbrauch WC + Waschmaschine ~**50 l/Person·Tag**; nutzbare Dachfläche mind. **25–30 m²/Person**.
- Optimale Speichermenge: **2–4 Wochen** Verbrauch; Überdimensionierung → Algenbildung; Unterdimensionierung → hoher Trinkwassernachspeisebedarf.
- Speichervolumen durch Simulationsrechnung ermitteln (Regenangebot × Bedarf).
- Faktoren: regionale Niederschlagsmengen, Auffangfläche × Abflussbeiwert, Personenzahl, Bedarfsstellen, Gartenflächen.

**Geeignete Auffangflächen:**
- Flachdächer mit Kiesschüttung: gut geeignet; bituminöse Teerpappen: völlig ungeeignet.
- Betondachsteine: leichte Aufhärtung des sauren Regenwassers.
- Ton, Schiefer: chemisch neutral.
- Metalleindeckungen (Kupfer, Zink, Blei): erhöhter Metallgehalt → weniger geeignet für Gartenbewässerung.
- Gründächer (intensive Begrünung): ungeeignet; Abflussverringerung um ~50 %, bräunlich gefärbt, erdig; extensive Begrünung: ggf. möglich.
- Asbestzement-Dächer: ungeeignet (gesundheitsgefährdend, verstopft feine Filter).
- Straßen-/Parkflächen: ungeeignet (Reifenabrieb, Mineralölrückstände).
- Industriegebäude oder Gebiete mit hohem Schadstoffanteil: ungeeignet.

**Filtration:**
- Fallrohrfilter: perforierte Wandungen leiten Wasser zur Zisterne ab; Verunreinigungen fließen in Kanalisation/Sickeranlage; weitgehend wartungsfrei; je Fallrohr ein Filter.
- Zentrale Filter (Zyklonenfilter/Wirbelfilter): Zentrifugalkraft drückt Wasser durch Filterwandungen; im Erdreich oder im oberen Bereich des Speichers; nur ein Filter für alle Fallrohre. Höhenversatz Ein-/Auslauf: ca. **40 cm**.
- Nachgeschalteter Feinfilter: Maschenweite **0,2 mm**.
- Erstverwurf (Beginn des Regenwasserabflusses): erhöhte Schmutz- und Keimkonzentration (Dachabrieb, Moos, Laub, Exkremente) → Ableitung empfohlen.

**Qualität und Betrieb:**
- Keimbelastung im Allgemeinen unter Grenzwerten für Badegewässer; bei längerer Verweilzeit, höherer Temperatur oder Lichteinwirkung: Algen/Gerüche.
- Keine Desinfektion des Wassers empfohlen.
- Wäschemaschinentyp: muss für Regenwasser geeignet sein (saures Wasser greift Metallteile an).
- Regenwasserzentralgerät: fasst Druckerhöhungsanlage, Nachspeisemodul, Feinfilter und Anlagensteuerung zusammen.
- Duplexanlage: zusätzlich Trinkwasser-Zwischenspeicher für Regenmangel/Wartung.
- Zisternensiphon: ca. **30 cm** Geruchverschlusshöhe; Versickerung des Überlaufwassers: mind. **1,5 m** Abstand zum Grundwasserspiegel.
- Trennungsgebot: Nichttrinkwasser-Rohrnetz ↔ Trinkwasser-Rohrnetz dürfen keine Verbindung haben (weder fest noch lösbar); Nachspeiseleitung muss frei über Einlauftrichter enden, Abstand mind. **2 × DN** Wasserleitung, aber mind. **20 mm** (DIN 1988).
- Rohrmaterial für Regenwasser: PE, PP oder Edelstahl (beständig gegen leicht saures Regenwasser); Kennzeichnungspflicht für Rohre und Entnahmestellen; abnehmbare Steckschlüssel an Zapfhähnen (Kindersicherung).
- Anzeigepflicht: Erstellung der Anlage dem WVU mitteilen; nach TrinkwV § 13 Betriebswasseranlagen grundsätzlich dem Gesundheitsamt anzeigen; im öffentlichen Bereich (Schulen, Kindergärten, Krankenhäuser, Gaststätten, Gemeinschaftseinrichtungen) Überwachung durch Gesundheitsamt nach TrinkwV § 18.
- In Mietshäusern: neben Regenwasseranschluss (z. B. Waschmaschine) muss auch Trinkwasseranschluss vorhanden sein (freie Wahl des Nutzers).
- Trinkwasser- und Regenwasserleitungen dürfen nicht miteinander verbunden werden (DIN 1988, DIN 1989, DIN EN 1717).
- Bei größeren Projekten (Fahrzeugwaschanlagen, Löschbehälter, Kühlsysteme, Grünflächenberegnung): Fachingenieure erforderlich.

**Grauwassernutzung (Abwasserrecycling):**
- DIN EN 12 056-2: Grauwasser enthält keine menschlichen Exkremente (im Gegensatz zu Schwarzwasser); Verwendung ausschließlich für Toilettenspülung.
- Anforderungen an Grauwasser: keine Sink-/Schlamm-/Schwebstoffe (Sand, Haare, Textilfasern → Verstopfungsgefahr), keine fäulnisfähigen Stoffe, keine pathogenen Keime, möglichst keine Trübung.
- Diese Anforderungen nur durch biologische Klärverfahren mit Belüftung erfüllbar (Belebtschlammanlagen, Tropfkörper mit Rückspülung).
- Zur Keim-Eliminierung müssen Chemikalien eingesetzt werden.
- Leitungsnetz aus laugenresistenten/korrosionsbeständigen Materialien (z. B. VPE).
- Allgemein anerkanntes, technisch ausgereiftes Grauwasser-Recycling-Verfahren steht noch aus.

#### 3.4.10 Warmwasserversorgung

**Trinkwarmwasserversorgung (TWW) im Wohnungsbau:**
- Erzeugung zentral (Gas/Öl/Wärmepumpe/Abwärme/Solarkollektoren) oder dezentral (Strom oder Erdgas).
- Strom für Warmwasserbereitung: Einsatz von Exergie für Wärme grundsätzlich ineffizient; vertretbar bei selten genutzten Bädern oder Waschtischen im Nichtwohnungsbau.
- Mindesttemperatur an Zapfstelle: **40 °C**; bei Großküchen bis **95 °C**; für thermische Desinfektion (Legionellen) bei zentralen Systemen: **≥ 60 °C**.
- Warmwasserverbrauch pro Zapfstelle:
  - Badewanne: im Mittel **160 l** (120–180 l) bei **40 °C** (35 °C + 5 K Wannenerwärmung)
  - Dusche (5 min): **40 l** bei **37 °C**
  - Waschtisch: **5–20 l** bei **35 °C**
  - Bidet: **10–20 l** bei **40 °C**
  - Spüle: **10–20 l** bei **50 °C** pro Spülvorgang
- Durchschnittlicher Warmwasserverbrauch Haushalte: **30–60 l**, Mittel **40 l/Person·Tag** (bei 60 °C).
- Energiebedarf: 1 l × 1 K = **1,163 Wh**; 40 l × 50 K (10→60 °C) = **2,326 kWh**; jahres­ener­gie­verbrauch je Person (mit 10 % Bereitschaftsverluste): ~**943 kWh**.

**Tab. 3.40 — Warmwasserbedarf nach Gebäudetyp:**

| Gebäudetyp | WW-Bedarf | Einheit | Temperatur |
|---|---|---|---|
| Wohngebäude | 30–60 | l/Tag·Person | 60–65 °C |
| Gaststätte/Restaurant | 15–45 | l/Sitzplatz | 60–65 °C |
| Hotel/Altenheim/Kinder-/Pflegeheim | 30–150 | l/Person | 60–70 °C |
| Sportstätten | 30–50 | l/Person | 60–65 °C |

**Tab. 3.41 — Warmwasserbedarf nach Wohnungsgröße (60 °C/Tag):**

| Wohnungsgröße | Personen | WW-Bedarf [l] |
|---|---|---|
| 1-Zimmer | 1 | 50–95 |
| 2-Zimmer | 2–3 | 70–200 |
| 3-Zimmer | 2–5 | 95–250 |
| 4-Zimmer | 3–7 | 120–500 |
| 5-Zimmer | 4–9 | 200–500 |
| 6-Zimmer | 5–11 | 400–600 |

**Elektrisch betriebene Warmwasserbereiter:**
- Bereitschaftstemperatur i. d. R. **55–60 °C** (Kompromiss Legionellenschutz/Kalkablagerung/Energieverluste).
- Drucklose Speicher: versorgen nur eine Zapfstelle; Temperatur einstellbar **+35 bis +85 °C**.
- Druckfeste Speicher: versorgen mehrere Zapfstellen; müssen Leitungsdruck (max. **6 bar**) standhalten; teurer (dickere Wandungen).
- Sicherheitsarmaturen Druckspeicher: Rückflussverhinderer (mit Prüfhahn) + Sicherheitsventil (mit Ablauftrichter, muss bei Aufheizen sichtbar Ausdehnungswasser freigeben).
- Speicher 5, 10, 15 l bis **3,3 kW** können an Steckdose angeschlossen werden; eigener Stromkreis notwendig.
- Ab **30 l**: auch Zweikreisschaltung (Tag-/Nachtstrom, z. B. 1/6 kW).
- Wärme­verluste (DIN EN 60 379, max. zulässig in 24 h): 5 l → 0,45 kWh; 10 l → 0,55 kWh; 15 l → 0,60 kWh; 30 l → 0,75 kWh; 80 l → 1,10 kWh; 100 l → 1,30 kWh; 300 l → 2,60 kWh.
- Korrosionsschutz Innenbehälter: emaillierter Stahl + Magnesium-Schutzanode (Opferanode, mittlere Lebensdauer **7 Jahre**); Kupfer (kleinere Behälter, ggf. verzinnt) bietet besten Korrosionsschutz; Kunststoff (PP, PA) bis 15 l.
- Hinter Geräten mit Kupferbehältern: keine verzinkten Stahlrohre.
- Boiler: ohne Wärmedämmung, preisgünstiger; 80 l bei 6 kW braucht > 1 Stunde auf 85 °C.
- **Durchlauferhitzer:** erwärmt Wasser im Durchfluss bis ~**65 °C**; Wirkungsgrad ~100 %; keine Bereitschaftsverluste; keine Kalkablagerungen. Leistungsaufnahme 12, 18, 21, 24 kW (selten 33 kW) → meist EVU-Einverständnis erforderlich. DIN 18 015-1: Drehstromleitung Belastbarkeit **mind. 35 A** für Bade-/Duschzwecke.
  - 12 kW: für Waschbecken und Spüle ausreichend
  - Mind. **18 kW**, besser **21 kW**: für Wanne oder Dusche
  - Faustwert Auslaufmenge: ca. halbe elektrische Leistungsaufnahme in l/min bei 40 °C (18 kW → ca. 8–10 l/min).
  - Hydraulisch gesteuert (9/18 oder 10/21 kW, größter Marktanteil, preisgünstigst): Zweistufen-Leistung; bei geringem Durchfluss (~4–6 l/min) halbe, bei großem volle Heizleistung; weniger geeignet für Kleinzapfungen; Temperatursprünge bei Druckschwankungen.
  - Thermisch geregelt: Temperaturfühler steuern Heizelemente; funktioniert auch bei niedrigem Netzdruck; Zapfcharakteristik günstiger (konstantere Temperatur); teurer als hydraulisch gesteuert.
  - Elektronisch geregelt: konstante vorgewählte Temperatur (30–60 °C) unabhängig von Durchflussmenge und Druckschwankungen; Einschaltung ab 2–3,5 l/min; schutzklasse IP 25 (strahlwassergeschützt) → in Spritzbereich 1 von Bade-/Duschwannen montierbar; für alle handelsüblichen Armaturen geeignet; Nennleistungen ca. **5–27 kW**.
  - Durchlauferhitzer mit WW-Vorrat (Durchlaufspeicher): Inhalt 15–100 l; Heizstufen z. B. 3/18 kW oder 3,5/10,5/21 kW; ~3 kW für Kleinverbraucher, bei Überschreitung Kapazität schaltet höhere Stufe zu.
  - Ab **5 m Leitungslänge**: Wassertemperatur im Rohrnetz max. **60 °C** (Thermostatarmatur erforderlich für Druckspeicher > 4 kW und Durchlaufspeicher).
- **Wärmepumpenspeicher** (Ein-/Zweifamilienhäuser): 200–400 l; entzieht Wärme aus Umgebungsluft; elektrische Direktheizung 1,5–2 kW zuschaltbar; Arbeitszahl 1,4–2,7 (relativ niedrig); Aufheizzeiten lang wegen geringer Heizleistung (300–2000 W); temporär Temperaturen > **60 °C** erreichen (Legionellen); nicht im Heizraum aufstellen (Wärmekurzschluss); Geräuschpegel ~ Gefrierschrank; benötigt Wechselstromsteckdose + Kalt-/Warmwasseranschluss.
- **Elektrowassererwärmer:** bis **4,6 kW** → Wechselstrom 230 V; darüber Drehstrom. Energiebedarf 100 l Aufheizung von 10 auf 37 °C: ~**3,3 kWh**; von 10 auf 60 °C: ~**5,6 kWh**.
- **Elektro-Standspeicher** (200–1000 l): druckfest, zentrale Versorgung, Schwachlaststrom, gewerbliche Betriebe/Landwirtschaft.

**Gas-Warmwasserbereiter:**
- Gas-Wasserheizer: hydraulisch gesteuert; Geräteleistung auf Spitzenbedarf (Wannenbad) abstimmen: 160-l-Wanne von 10→40 °C: **17,5 kW in ~20 min** oder **22,7 kW in ~15 min**.
- Raumluftabhängige Geräte (Art B nach TRGI): 150 cm² bzw. 300 cm² Verbrennungsluftöffnungen erforderlich.
- Gas-Vorratswasserheizer: druckfeste Behälter **80–280 l**, atmosphärische Gasbrenner; bei größerem WW-Bedarf.
- Kombi-Gaswasserheizer (Kombithermen): WW-Versorgung + zentrale Warmwasserheizung bis ~**24 kW**; wandhängend, Niedertemperatur- oder Brennwertausführung; modulierende oder zweistufige Arbeitsweise empfohlen (WW-Bedarf: 18–30 kW, Heizung: 6–12 kW bei Niedrig­energie­häusern).

**Solare Trinkwassererwärmung:**
- Sonnenscheindauer Deutschland: **1300–1900 h/a** (Mittel 1045 kWh/(m²·a)); Sommerhalbjahr 1000–1400 h, Winterhalbjahr 300–500 h.

**Tab. 3.44 — Sonnenstrahlungsdaten Deutschland:**

| Parameter | Wert |
|---|---|
| Maximale Strahlungsleistung (senkrecht bestrahlt) | ~1 kW/m² |
| Sehr dichte Bewölkung | ~0,02 kW/m² |
| Diffuse Strahlung bei bewölktem Himmel | 0,02–0,25 kW/m² |
| Jährliche Einstrahlung (horizontal bzw. 45° Süd) | 900–1200 kWh/(m²·a) |
| Tages-Maximum (sehr klares Sommerwetter) | ~8 kWh/(m²·d) |
| Tages-Minimum (sehr trübes Wetter) | ~0,1 kWh/(m²·d) |
| Mittel an den 100 besten Sonnentagen | ~5,5 kWh/(m²·d) |
| An den 100 ungünstigsten Tagen | < 1 kWh/(m²·d) |

- **Flachkollektoren** (verbreitetste Bauart): verglaste Oberseite, gedämmte Unterseite, Treibhauseffekt, schwarze Absorberfläche, Wärmeträger (Wasser + Frostschutzmittel).
- **Vakuumröhrenkollektoren**: evakuierte Glasröhren, deutlich geringere Wärmeverluste, ~30 % geringere Kollektorfläche nötig, drehbarer Absorber → auch an senkrechten Flächen montierbar, teurerer Aufbau.
- Kollektorfläche: **1,5–2 m²/Person** (Flachkollektoren); Vakuumkollektor: ~30 % weniger.
- Speichervolumen: **50–70 l/m² Kollektorfläche** (alternativ: 80–140 l/Person).
- Kollektorneigung für WW-Bereitung (Sommer): **20°–45°**; für Raumheizung (Herbst/Frühjahr): **35°–60°**.
- Azimut: Für Sommernutzung bis ±50°–60° von Süd tolerierbar; für Winternutzung max. ±35°.
- Solare Wärmedeckung: Sommer ~80 %, Winter ~10 %, Jahresmittel ~50 %; Nachheizung zwingend notwendig.
- Ertrag pro m² Kollektorfläche: ca. **500 kWh** Solarwärme.
- Überdimensionierung → unwirtschaftliche Sommerüberschüsse; Auslegung für ~50 % Jahresdeckungsanteil.
- Montagearten: Auf-Dach (bevorzugt bei Nachrüstung), In-Dach (standardisierte Einbaurahmen), Flachdach (Rahmengestelle, zusätzliche Dachlast ca. **20–30 kg/m²**, statischer Nachweis).
- Rohranschlüsse (Vor-/Rücklauf): wärmegedämmt; im Freien: UV-beständige, feuchtigkeitsresistente und temperaturbeständige Dämmung; Schutz vor Vogel-/Marderschäden berücksichtigen.
- Bauaufsichtliche Bestimmungen je Bundesland unterschiedlich (Bauantrag/Anzeige/Anmeldung).

**Mit Wärmeerzeugungsanlage gekoppelte WW-Versorgung:**
- Kombinationskessel: WW-Speicher baulich mit Wärmeerzeuger verbunden oder daneben aufgestellt.
- Heizperiode: WW-Bereitung mit Vorrangschaltung.
- Sommerbetrieb: erzeugte Wärme ausschließlich für WW.
- Speicherinhalt Einfamilienhäuser: ca. **80–200 l**; Zweifamilienhäuser: **200–300 l** (Rechenwerte nach DIN 4708-2).
- Mindesttemperatur > **55 °C** (Legionellen).
- Alternative Durchlaufprinzip: leitungsfrisches Wasser, höhere Dauerleistung nötig → unwirtschaftlicher.
- Bei größeren Anlagen (Krankenhäuser, Hotels): gesonderter Sommerwärmeerzeuger sinnvoll.
- Zellenspeicher: transportfreundlicher als Einzelspeicher, flexiblere Betriebsweise.
- Nichtwohnungsbau-Kleinverbraucherstellen (Handwaschbecken, Teeküchen, Putzräume): elektrische Einzelversorgung meist vorteilhafter (5-l-Druckloser bis 30-l-Druckloser je nach Nutzung).

**Rohrleitungen für Warmwasserversorgung:**
- Kupfer oder Edelstahl bevorzugt; Kunststoff (Rohr-in-Rohr-Systeme) zunehmend.
- Kupfer: geringerer Druckverlust (glattere Innenwandung), kaum Inkrustationen; laut Positivliste UBA: nur Kupfer, Edelstahl und bestimmte Kunststoffe zulässig.
- Blei: für Warmwasserleitungen nicht zugelassen.
- Mischinstallation: Kupfer **niemals** in Fließrichtung vor verzinkten Stahl­rohren/-behältern (Lochfraß durch galvanische Lokalelemente; Korrosionsgeschwindigkeit verdoppelt sich je 10 K); Armaturen aus Messing/Rotguss: korrosionsneutral.
- Ab **5 m** Leitungslänge: Netztemperatur max. **60 °C** begrenzen (Thermostatarmatur).
- Dämmstoffdicke: Rohre < 8 m Länge ~ halber Rohrdurchmesser; Rohre > 8 m ~ voller Rohrdurchmesser.
- Warmgehende Leitungen in Wandschlitzen: nicht starr einbauen; Abzweige und Richtungsänderungen mit Dämmstoff abpolstern; werkseitig ummantelte Kupferrohre zwischen Richtungsänderungen bis ~3 m ohne zusätzliches Ausdehnungspolster.
- Rohr­befestigungen: mind. **50 cm** von Richtungsänderungen entfernt; längere Leitungen: Schiebeschellen + Ausgleichsbögen/Kompensatoren.

**Zirkulationsleitungen (WW-Umlaufleitungen):**
- Ermöglichen verzögerungsfreies Zapfen warmen Wassers auch bei größerer Entfernung.
- Umwälzpumpe hält Kreislauf ständig in Bewegung; Schaltuhren erlauben Nachtabschaltung.
- Ab ca. **8 m** Leitungsweg empfohlen; 10 m DN 15 enthält 1,8 l Wasser → ~6–8 s Wartezeit ohne Zirkulation.
- **"3-Liter-Regel" (DVGW):**

| Gebäudetyp | Speichervolumen | Leitungsvolumen (bis Entnahme) | Anforderung |
|---|---|---|---|
| Ein-/Zweifamilienhaus | egal | egal | Kleinanlage |
| Andere Gebäude | < 400 l | ≤ 3 l | Kleinanlage |
| Andere Gebäude | > 400 l | ≤ 3 l | Großanlage |
| Andere Gebäude | > 400 l | > 3 l | Großanlage + Einbau Zirkulation |
| Andere Gebäude | < 400 l | > 3 l | Großanlage + Einbau Zirkulation |

- Bei Mehrfamilienwohnhäusern mit zentraler WW-Versorgung und **> 400 l** Speicherinhalt: Zirkulationsleitungen oder Rohrbegleitheizungen zwingend (Legionellenverminderung).
- Mangelhafte Durchströmung (Luftsäcke, zugesetzte Drosselventile, längere Stichleitungen) → Temperaturen 30–50 °C in Teilsträngen → Legionellengefahr.

**Elektrische Rohrbegleitheizungen:**
- Selbstregelnde Heizbänder: Heizleistung steigt bei sinkender Rohrtemperatur, fällt bei steigender; zweipoliges flaches Band vor Dämmarbeiten am Rohr befestigen.
- Können Stichleitungen einbeziehen, die von Zirkulation nicht erreichbar sind.
- Temperaturbereich legionellenkritisch (**30–50 °C**) ausschließbar.
- Zeitliche Steuerung zur Energieeinsparung notwendig.
- Besonders geeignet für Alten-/Pflegeheime, Krankenhäuser, Rehazentren.
- Nachteil: Einsatz von hochwertiger Energie (Strom).

**Legionellen:**
- Stäbchenbakterien; überall außer Meerwasser; im Kaltwasser harmlos geringe Konzentration.
- Gesundheitsgefährdend bei **30–45 °C** und langer Verweilzeit (mehrere Tage/Wochen).
- Übertragung ausschließlich durch Einatmen erregerangereicherter Aerosole (Duschen, Whirlpools); nicht durch Trinken oder Mensch-zu-Mensch.
- Risikogruppen: Immungeschwächte, Diabetiker, chronische Bronchitis, Emphysem, starke Raucher, ältere Menschen.
- Krankheitsformen: Pontiac-Fieber (~95 % der Fälle, grippeähnlich, harmlos); Legionärskrankheit (schwere Lungenentzündung, tödlich möglich wenn falsch diagnostiziert) → Behandlung mit Erythromycin.
- Ab **50 °C**: keine Vermehrung mehr; bei **60–65 °C**: Absterben in Minuten; bei **~70 °C**: Absterben in Sekunden.
- Vermehrung auf inneren wasserbenetzten Oberflächen; begünstigt durch Inkrustationen, Schlamm in WW-Speichern bei Temperaturschichtung (30–40 °C im unteren Bereich).
- Risikogebäude: Hotels, Krankenhäuser (weitverzweigte Netze); Einfamilienhäuser: geringes Risiko.
- Anerkannte Regel: DVGW Arbeitsblatt W 551 (Maßnahmen zur Legionellenverminderung).

**Anforderungen an Trinkwassererwärmer (DVGW W 551):**
- Dezentrale Durchfluss-TWW-Erhitzer ohne weitere Maßnahmen verwendbar, wenn nachgeschaltetes Leitungsvolumen ≤ **3 l**.
- Speicher-TWW-Erhitzer: ausreichend große Reinigungs-/Wartungsöffnungen (Handloch) nach DIN 4753-1.
- WW-Austrittstemperatur am Speicher: bei bestimmungsgemäßem Betrieb **≥ 60 °C**.
- Speicher > **400 l**: gleichmäßige Erwärmung an allen Stellen sicherstellen (Umwälzung, serielle Schaltung).
- Großanlagen: WW-Austrittstemperatur stets ≥ **60 °C**; Vorwärmstufen mind. **1 × täglich** auf ≥ 60 °C erwärmen; kurzzeitige Abweichungen im Minutenbereich tolerierbar (DIN 4708), systematische Unterschreitungen nicht.
- Kleinanlagen: Einstellung auf **60 °C** empfohlen; Betriebstemperaturen unter **50 °C** vermeiden; Auftraggeber über Legionellenrisiko informieren.
- Zirkulationssysteme: Wassertemperatur im System darf Austrittstemperatur um nicht mehr als **5 K** unterschreiten; zur Energieeinsparung max. **8 h innerhalb 24 h** abgesenkt betreiben.
- Gewerbliche Betreiber (Vermieter): nach TrinkwV regelmäßige Legionellenprüfungen; bei Grenzwertüberschreitung: Gefährdungsanalyse durch Sachverständigen.
- Abstand warm-/kaltgehender Leitungen: ausreichend einhalten (auch mit Dämmung); bei langen Verweilzeiten sonst Legionellenwachstum auch im Kaltwassernetz möglich.

---

### 3.5 Feuerlöschanlagen (Seiten 185–189)

#### 3.5.1 Hydrantenanlagen
- Feuerlösch-Steigleitungen mit Wandhydranten: in meisten Bundesländern für **notwendige Treppenräume** von Hochhäusern (Fußboden mind. eines Aufenthaltsraumes > **22 m** über festgelegter Geländeoberfläche) und bestimmte Gewerbeobjekte obligatorisch.
- **„Nasse" Steigleitungen**: ständig unter Leitungsdruck; Brandbekämpfung vor Eintreffen der Feuerwehr möglich; Mindest-Ruhedruck am höchsten Wandhydranten: **3 bar**; ggf. Druckerhöhungsanlage + Notstromanlage erforderlich (Kellerraum planerisch freihalten).
- **„Trockene" Steigleitungen**: nicht mit Wassernetz verbunden; nur für Feuerwehr; kein Schlauchausheben nötig; B-Kupplung in Gebäudenähe; Hydrant für Feuerwehr max. **80 m** entfernt; frostunempfindlich.
- **„Nass/Trocken"-Leitungen**: werden erst unmittelbar vor Einsatz geflutet; nach Nutzung automatisch entleert; bei Stromausfall automatisch mit Wasser gefüllt.

**Wandhydranten-Abmessungen (DIN 14 461-2, in cm, Auszug):**

| Typ | Breite (Schrank) | Breite (Nische) | Höhe (Schrank) | Höhe (Nische) | Tiefe (Schrank) | Tiefe (Nische) |
|---|---|---|---|---|---|---|
| Trocken | 30 | 32 | 60 | 62 | 14 | 15 |
| Trocken mit Feuerlöscher/-melder | 40 | 42 | 70 | 72 | 22 | 23 |
| Nass | 60 | 62 | 86 | 88 | 14 | 15 |
| Nass mit Feuerlöscher/-melder | 70 | 72 | 86 | 88 | 18 | 19 |
| Trocken + Nass mit Feuerlöscher/-melder | 90 | 92 | 70 | 72 | 22 | 23 |
| Einspeisung unten B-Kupplung | 70 | 72 | 70 | 72 | 30 | 31 |

- Wandhydranten nass/nass-trocken: Kupplung + schwenkbare Haspel mit Schlauch (**15–30 m**) und Strahlrohr, evtl. Handfeuerlöscher und Feuermelder; Nischengröße nach DIN 14 461-1: **70/80/25 bis 74/80/25 cm** (B × H × T).
- DN 50 = „C-Kupplung"; DN 80 = „B-Kupplung".

#### 3.5.2 Sprinkleranlagen
- Selbsttätige Feuerlöschanlagen; erkennen, melden und löschen Feuer, bevor unkontrollierbarer Großbrand entsteht.
- Auslöseelemente: flüssigkeitsgefüllte Glasfässchen oder Schmelzlote; Auslösetemperatur ~**30 K** über höchstmöglicher normaler Raumtemperatur (i. d. R. **68–78 °C**).
- Schutzfläche pro Sprinklerkopf: **9–21 m²** Bodenfläche (abhängig von Brandgefahrenklasse).
- Brandgefahrenklassen (VdS CEA 4001):
  - **LH** (Light Hazard): geringe Brandgefahr, z. B. Büro
  - **OH** (Ordinary Hazard): mittlere Brandgefahr
  - **HHP** (High Hazard Production), **HHS** (High Hazard Storage): hohe Brandgefahr
- Beispiel Bürogebäude LH, max. 1000 Sprinklerköpfe: Wasserversorgung Art 1 (erschöpflich, z. B. Druckluftwasserbehälter oder Hochbehälter).
- Wasserversorgungsarten:
  - Art 1: nur eine erschöpfliche Quelle
  - Art 2: nur eine unerschöpfliche Quelle
  - Art 3: eine unerschöpfliche + eine erschöpfliche Quelle
  - Art 4: zwei unerschöpfliche + eine erschöpfliche Quelle
- Wasserquellen: öffentliches Netz, Vorratsbehälter, unerschöpfliche natürliche Quellen, Druckluftwasserbehälter.
- Sprinklerköpfe-Unterschiede: Art der thermischen Auslösung (Schmelzlot- oder Glasfass), Wasserleistung, Anordnung (stehend/hängend), Sprühbild.
- ~**75 %** aller Brände in sprinklergeschützten Räumen mit **1–4 Düsen** gelöscht.
- Einsatz in Krankenhäusern, Hochhäusern, Theatern, Tiefgaragen, Lagerhallen, Fabrikations-räumen, Warenhäusern.
- Elektromotorischer Antrieb an Ersatzstromaggregat anschließen; Sprinkleranlage ersetzt keine anderen Brandschutzmaßnahmen, sondern ist Teil eines Gesamtkonzepts (Brandabschnitte, Brandmeldeanlagen, Entrauchungsanlagen).
- Bei Einhaltung VdS-Richtlinien: Versicherungsprämienrabatte.
- In frostgefährdeten Räumen: **Trockenanlagen** mit Druckluft in Rohrleitungen; Druckabfall bei Öffnung eines Sprinklers → Wasserfreigabe.

**Sonderformen:**
- **Sprühwasser-Löschanlagen (Regenanlagen)**: offene Düsen; bei extrem schneller Brandausbreitung (Müllbunker, Theaterbühnen); sofort gesamte Bodenfläche besprühen; Auslösung ~30 K über Umgebungstemperatur; Wasseranfall über Deckenabläufe unverzüglich ableiten.
- **Wasserschleieranlagen (Regenvorhänge)**: verhindert Brandausbreitung über Abschnitte hinaus; kann Öffnungen in Brandmauern abschirmen; ab **8 m** Raumhöhe Wirksamkeit fraglich; Bodenabläufe erforderlich.
- **Wassernebel-Löschanlage (Niederdruck)**: Wassertropfen **10–100 μm**; wie herkömmliche Sprinkleranlage aufgebaut (thermisch auslösende Sprühköpfe, Rohrnetz, Alarmventilstation, Pumpe, Vorratsbehälter); Löschwassermenge und Bevorratung reduziert; Bauteile geringer dimensionierbar; geeignet für Nachrüstungen; betrieben mit Höchstdrücken **100–125 bar** (Hochdruck-Variante).

#### 3.5.3 Inertgas-Löschsysteme
- Schützt hochwertige Anlagen, Wertgegenstände, sensible Einrichtungen, die andere Löschmittel beschädigen würden.
- Eingesetzte Gase: Argon (Ar), Stickstoff (N₂), Kohlendioxid (CO₂).
- Löschwirkung: Verdrängung des Luftsauerstoffs (Stickeffekt); bei sauerstoffärmeren Brandgütern (Acetylen, CO, H₂): höhere Löschgaskonzentration nötig.
- **Argon**: ungiftig, edel, kein Kühleffekt; geeignet für Räume mit höherer Personendichte oder elektrischen/elektronischen Anlagen.
- **Stickstoff**: ungiftig, kein Auskühlen; geeignet für Räume mit brennbaren Flüssigkeiten.
- **Kohlendioxid**: schwerer als Luft → durchsetzt Flutungsbereich schnell; zielgenau ausrichtbare Aerosol-wolke; Kühleffekt durch Verdampfen. Geeignet für nicht umhüllte freistehende Objekte.
- Flaschendruck: bis **300 bar**; Auslösung durch Branderkennungs- und Steuerungssysteme automatisch; Flaschenlager außerhalb des zu schützenden Bereichs.
- Einsatzbereiche: EDV-Einrichtungen, Telekommunikationsanlagen, Schalträume, Schalt-/Steueranlagen, Turbinen, Transformatoren.

---

### 4.1 Heiz- und Kühllast — Heizlastberechnung (Seiten 191–193)

#### 4.1.1 Heizlast
- **Norm-Gebäudeheizlast ΦHL**: maßgebend für Auslegung der Wärmeerzeugungsanlage, Planung von Heizzentralen, Brennstoffräumen und Schornsteinen; gibt Aufschluss über Bau- und Betriebskosten.
- Norm: **DIN EN 12 831** „Heizungsanlagen in Gebäuden — Verfahren zur Berechnung der Heizlast" + Beiblatt 1 (Nationaler Anhang Deutschland).
- Heizlast setzt sich zusammen aus:
  - **Transmissionsheizlast** (ΦT): Wärmeverluste durch Umschließungsflächen (Außenwände, Fenster, Türen, Decke/Dach, unterer Abschluss); bei erdberührenden Bauteilen ggf. Wärmeverluste ans Grundwasser berücksichtigen.
  - **Lüftungsheizlast** (ΦV): Wärmeverluste durch Luftdurchlässigkeit der Gebäudehülle (Schließfugen von Fenstern/Türen, Fugen zwischen Blendrahmen und Wand, Außenwandfugen, Rollladenkastenschlitze); beeinflusst durch Lage (Stadtkern, freie Lage) und Gebäudehöhe; kann bei unzureichender Winddichtheit die Transmissionsverluste erheblich übersteigen.
- Berechnungsformel Heizleistung je Raum: **ΦHL,i = ΦT,i + ΦV,i + Φhu,i − Φgain,i**
  - ΦT,i: Transmissionsverluste
  - ΦV,i: Lüftungswärmeverluste
  - Φhu,i: zusätzliche Aufheizleistungen (nach Temperaturabsenkung)
  - Φgain,i: optionaler Wärmegewinn (unter Norm-Außenbedingungen)
- Berechnungsschritte (DIN EN 12 831):
  1. Norm-Außentemperatur und Jahresmittel der Außenlufttemperatur (nach Postleitzahl)
  2. Räume als beheizt/unbeheizt einordnen; Norm-Innentemperatur festlegen
  3. Abmessungen und wärmetechnische Eigenschaften aller Bauteile
  4. Transmissionswärmeverlust-Koeffizient × Norm-Temperaturdifferenz → Norm-Transmissionswärmeverluste
  5. Lüftungswärmeverlust-Koeffizient × Norm-Temperaturdifferenz → Norm-Lüftungswärmeverluste
  6. Norm-Transmissions- + Norm-Lüftungswärmeverluste addieren
  7. Korrekturfaktor für Aufheizleistung anwenden → Norm-Heizlast des Raums
  8. Auslegungs-Heizleistung = Summe Norm-Wärmeverluste + Aufheizleistung

- **Norm-Transmissionswärmeverlust-Koeffizient** (vereinfacht):
  HT,ie = Σk [Ak × (Uk + UTB) × fU,k × fie,k]
  - Ak: Bauteilfläche
  - Uk: Wärmedurchgangskoeffizient des Bauteils
  - UTB: Wärmebrückenkorrektur
  - Gewichtungsfaktoren fU,k und fie,k für Temperatur- und Ausrichtungskorrektur

- **Wärmebilanz** (Heizleistungsbedarf des Gebäudes):
  - Transmissionsverluste (Gebäudehülle)
  - ± Verluste durch freie Lüftung
  - ± Zuschläge für Anheizvorgänge
  - ± Leistung für Raumlufttechnische Anlagen (RLT)
  - − Wärmerückgewinnung aus RLT-Anlagen
  - ± Zuschläge für Warmwasserbereitung (nur Ausnahmen)
  - ± Zuschläge für Prozesstechnik u. a.
  - − Wärmegewinne (bei Auslegungszustand)
