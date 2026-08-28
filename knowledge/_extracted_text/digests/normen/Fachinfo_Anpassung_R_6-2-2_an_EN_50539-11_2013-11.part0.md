# Fachinfo_Anpassung_R_6-2-2_an_EN_50539-11_2013-11 — Teil 0
> Quelle: Fachinfo_Anpassung_R_6-2-2_an_EN_50539-11_2013-11 (normen) · dieser Teil.

## Inhalt

### Dokument-Metadaten
- **Herausgeber:** OVE — Österreichischer Verband für Elektrotechnik, Eschenbachgasse 9, 1010 Wien.
  - Tel.: +43 1 587 63 73 · Fax: +43 1 587 63 73-99
  - E-Mail: ove@ove.at · Internet: www.ove.at · ZVR: 327279890
  - ATU36808601 · Banken: BA-CA Kto.-Nr. 0043-28423/00 · PSK Kto.-Nr. 1.935.655
- **Titel:** Fachinformation des Österreichischen Elektrotechnischen Komitees – OEK: „Anpassung von OVE-Richtlinie R 6-2-2:2012 an EN 50539-11:2013".
- **Ausarbeitung:** Technisches Komitee Blitzschutz (TK BL) und Technisches Subkomitee Überspannungsableiter für Niederspannung (TSK IS 37A) des OVE.
- **Hinweis:** Im Falle eines Nachdruckes darf der Inhalt nur wortgetreu und ohne Auslassung oder Zusatz wiedergegeben werden.
- **Ausgabe:** November 2013.

### Hintergrund / Anlass
- Die mit **2012-04-01** veröffentlichte OVE-Richtlinie **R 6-2-2** „Blitz- und Überspannungsschutz – Teil 2-2: Photovoltaikanlagen – Auswahl und Anwendungsgrundsätze an Überspannungsschutzgeräte" basiert auf der CENELEC-Spezifikation **CLC/TS 50539-12:2010**.
- Im Zuge der Entwicklung des Produktstandards **EN 50539-11:2013** „Überspannungsschutzgeräte für Niederspannung – Überspannungsschutzgeräte für besondere Anwendungen einschließlich Gleichspannung – Teil 11: Anforderungen und Prüfungen für Überspannungsschutzgeräte für den Einsatz in Photovoltaik-Installationen" wurde bei CENELEC — zur besseren Unterscheidung von SPDs für andere Anwendungsgebiete — beschlossen, die „höchste Dauerspannung" **nicht** wie bei SPDs für a.c.-Anwendungen mit **U_C**, sondern abweichend zu definieren (siehe Klausel 3.1.11).

### Klausel 3.1.11 — Definition
- **3.1.11 höchste Dauerspannung für PV-Anwendungen — U_CPV**
  - Definition: höchste **Gleichspannung**, die dauernd an den Schutzpfaden des SPDs angelegt werden darf.

### Anzupassender Abschnitt der R 6-2-2:2012
Aus dem o.g. Grund ist **Abschnitt 4.6.2.2** in OVE-Richtlinie R 6-2-2:2012 wie folgt anzupassen:

**4.6.2.2 Auswahl von U_CPV der SPDs auf der DC-Seite von PV-Anlagen**
- Die maximale Dauerspannung **U_CPV** des SPDs muss so gewählt werden, dass sie unter allen Bedingungen (Einstrahlung und Umgebungstemperatur) über der maximalen Leerlaufspannung des PV-Generators liegt oder mindestens den gleichen Wert hat.
- Der **minimale Wert für U_CPV** muss **größer oder gleich 1,2 · U_OC STC** sein.
- **U_CPV** muss für **jeden Schutzpfad** (+/–, +/Erde und –/Erde) betrachtet werden.
- **ANMERKUNG:** Die Spannungen zwischen den DC-Leitern und Erde hängen von der PV-Wechselrichtertechnologie ab und sind nicht immer reine DC-Spannungen.

### Ausblick / Frist
- **CLC/TS 50539-12:2010** wird aktuell bei CENELEC überarbeitet und an **EN 50539-11:2013** angepasst.
- Wenn die Arbeiten abgeschlossen sind (**voraussichtlich Ende 2013**), wird auch OVE-Richtlinie R 6-2-2 überarbeitet und die Inhalte dieser Fachinformation werden in der neuen Ausgabe berücksichtigt.

## Maschinen-Regeln
- [DEFINITION] U_CPV = höchste Dauerspannung für PV-Anwendungen = höchste Gleichspannung, die dauernd an den Schutzpfaden des SPDs angelegt werden darf (Klausel 3.1.11, EN 50539-11:2013, S.1).
- [DEFINITION] Bei SPDs für a.c.-Anwendungen wird die höchste Dauerspannung mit U_C bezeichnet; bei PV-/DC-Anwendungen abweichend mit U_CPV (Klausel 3.1.11 / Hintergrund, S.1).
- [PFLICHT] U_CPV des SPDs muss unter allen Bedingungen (Einstrahlung und Umgebungstemperatur) ≥ der maximalen Leerlaufspannung des PV-Generators sein (R 6-2-2 §4.6.2.2, S.1).
- [STROMKREIS] Minimaler Wert für U_CPV ≥ 1,2 · U_OC STC (R 6-2-2 §4.6.2.2, S.1).
- [PFLICHT] U_CPV muss für jeden Schutzpfad einzeln betrachtet werden: +/–, +/Erde und –/Erde (R 6-2-2 §4.6.2.2, S.1).
- [FRIST] Überarbeitung der CLC/TS 50539-12:2010 (Anpassung an EN 50539-11:2013) voraussichtlich Ende 2013; danach Überarbeitung der OVE-Richtlinie R 6-2-2 (S.1).
- [FRIST] OVE-Richtlinie R 6-2-2 veröffentlicht am 2012-04-01; diese Fachinformation Ausgabe November 2013 (Metadaten, S.1).
