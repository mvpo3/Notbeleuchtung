# k-sort-a20 — Teil 7
> Quelle: k-sort-a20 (buecher) · Seiten 281-320.

Dieses Dokument ist der **Schrack-Produkt-/Preiskatalog** (Best.-Nr.-Listen). Dieser Teil deckt zwei große Kapitel ab: (1) **Blitzstromableiter, Überspannungsableiter und Erdung** (S. 281–289) und (2) **Schmelzsicherungs- und Sammelschienensysteme** — Neozed D0, Diazed D, NH-Sicherungen, Sammelschienen 60/100/185 mm (S. 290–320). Inhaltlich = Typenübersicht mit technischen Daten (Netzform, Ableiterklasse, Iimp/kA, Spannung, Größe, Nennstrom, Querschnitt, Maße). Best.-Nr./UVP-Preise sind nicht-fachlich und nur exemplarisch erwähnt. Relevant für ElektroPlaner: konkrete **Bauteil-Spezifikationen** für Verteiler-Stückliste (Ableiterklassen, NH-/D0-Größen, Querschnitte, Stromtragfähigkeit von Sammelschienen).

## Inhalt

### Blitz- & Überspannungsableiter — Netzsystem-Zuordnung (Pflicht-Logik)
Ableiter werden nach **Netzform** (TN-C, TN-S, TT) und **Anzahl/Schaltung der Pfade** ausgewählt:
- **TN-C-Netz:** Schaltung **3+0** (3 Phasen, kein separater N-Pfad).
- **TN-S-Netz:** Schaltung **4+0** (3 Phasen + N als vollwertige Pfade); einphasig **2+0**.
- **TT-Netz:** Schaltung **3+1** (3 Phasen + 1 N-PE-Funkenstrecke), einphasig **1+1**.
- Ableiterklassen-Nomenklatur: **Klasse I = Typ T1 (B)** Blitzstromableiter, **Klasse II = T2 (C)** Überspannungsableiter, **Klasse III = T3 (D)** Feinschutz. Kombiableiter = T1+T2 (B+C).
- Suffix **„+H"** = mit Fernmelde-/Hilfskontakt (Remote Signalling).

### Kombiableiter T1+T2 (B+C) — Kennwerte je Serie
- **Serie Protec (25 kA):** Iimp 25 kA, 275 V; TN-C 3+0 (IS211330-A), TN-S 4+0 (IS211340-A), TT 3+1 (IS211311-A). Cu-Gewicht 1400 g/Stk.
- **Serie Combtec (12,5 kA):** Iimp 12,5 kA, 275 V bzw. steckbar 300 V; TN-C 3+0 (IS211230-A), TN-S 4+0 (IS211240-A), TT 3+1 (IS211210-A); auch 7,5 kA TT (IS211161, 300 V).
- **Serie Settec (12,5 kA):** z.B. SETTEC BC TNC 275/12,5+H (IS221231), BC TT 275/12,5+H (IS221211).
- **Serie Powertec (Kombiableiter):** Blitzstromableiter 25 kA und 60 kA, Klasse T1/T2 B/C (IS010111/…113); Summenableiter N/PE 50 kA (SG50, IS010084) und 100 kA (G100, T1/B, IS010094); steckbar 25 kA T1/2 + HK.

### Überspannungsableiter T2 (C)
- **Serie Vartec:** C-TNC-/TNS-/TT-Set 255 V / 20 kA (mit/ohne +H). Einzelteile: VVM-Modul T2 255 V/20 kA, 255 V/15 kA, 320 V/15 kA, 320 V/20 kA; VGM-Modul 20 kA; Sockel 1p/2+0/3+0/3+1/4+0 jeweils mit/ohne Hilfskontakt (HK).
- **Serie Settec:** C TNC 275 V/20 kA, C TT 275 V/20 kA.
- **Serie Vartec 1TE:** C/T2-Ableiter Modul 1TE, L+N, 10 kA, 335 V (VEPG, IS010073) + Sockel.
- **Serie UAS:** Ableiter komplett 1p/2p/3p/4p je 20 kA/280 V; 1+1 und 3+1 (4×20 kA/280 V); 1p 20 kA/580 V. Moduleinsätze VV 20 kA/280 V, GG 60 kA/260 V. Verschienung 3-fach TN-C, 4-fach TN-S/TT.

### Feinschutz T3 (D) — Energie, Daten, Steuerung
- **Versorgungsleitungen:** Vartec D/T3-Modul 1TE, L+N, 3 kA, 275 V (VMG, IS010200); UAS-Ableiter 1+1 / 2p 280 V.
- **Schukosteckdosen-Feinschutz:** D-Steckdosenableiter 2,5 kA (IS010003); D/III Zwischenstecker Klasse III (D) 230 V; UP-Steckdoseneinsatz mit Überspannungsschutz (perlweiß EL215130 / reinweiß EL215134).
- **Steuerungstechnik (Klasse 3/D):** Datenableiter Kat-6-LAN/PoE (IS212080); Steuerleitungen max. 5 VDC/1 A, 24 VDC/1 A, 30 VDC/1 A (je 1 A); ADSL/ISDN/analog Telefon TAE/DSL (IS212085); KNX-Bussystem-Ableiter (IS212075).
- **Datenübertragung/Koax:** F-Stecker und BNC-Stecker Koaxableiter (IS210424/…425, IS212070).

### Photovoltaik-Ableiter — Serie Photec
- **Kombi T1+T2 (B+C) 12,5 kA:** steckbar 1100 VDC (Iimp 12,5 kA+H), 1500 VDC (Iimp 10,0 kA+H), 1000 VDC 12,5 kA, 550 VDC 12,5 kA.
- **Überspannungsableiter T2 (C):** steckbar 1100 VDC / 20 kA, 1500 VDC / 20 kA, 1000 VDC / 20 kA, 550 VDC / 20 kA (je mit/ohne +H); Ersatzmodule 550 V / 1000 V.
- Merke: **DC-Bemessungsspannungen 550 / 1000 / 1100 / 1500 VDC** — Auswahl nach PV-String-Spannung.

### Erder & Erdungsmaterial
- **Kreuzerder** St/fvz 3× 50×50 mm, Länge **1,5 m** (BG635150).
- **Tiefenerder** mit Rändelung, Länge **1,5 m**: St/fvz Ø20 mm, Ø25 mm; V4A Ø20 mm. Schlagspitze Ø20/Ø25 mm, Schlagkopf Ø20 mm.
- **Bandeisen** St/fvz: 30×3,0 mm (1 Bund ≈ 50 kg ≈ 69 m); 40×4,0 mm (≈ 50 kg ≈ 39 m).
- **Runddraht** St/fvz: Ø8 mm (≈ 50 kg ≈ 125 m), Ø10 mm (≈ 50 kg ≈ 81 m); V4A Ø10 mm (≈ 25 kg ≈ 40 m); Alu weich Ø8 mm (≈ 10 kg ≈ 74 m).
- **Potentialausgleichschiene** (BS900200) bzw. kurze Ausführung mit **7 Klemmstellen** (BS900205).
- **Revisionstür** für UP-Trennstellen St/fvz **155×205 mm**. Banderderdose.
- **Regenrohrschellen** V2A Ø80 / Ø100 / Ø120 mm.
- **Erdungsbandschellen** V2A: Rohre Ø8–18 / Ø8–50 / Ø8–114 / Ø8–165 mm, Anschluss jeweils 2,5–16 mm².

### Verbindungs-/Anschlussklemmen (Blitzschutz/Erdung)
- Multiklemmen Ø8–10 mm (St/fvz, V2A, V4A).
- Stangenklemme U-Verbinder Ø8–10 auf Ø16 mm.
- Trennklemme ES-Verbinder ZG Ø8–10 mm; KS-Verbinder Ø6–10 mm.
- Diagonal-Kreuzklemme fl. 30 mm / Ø8–10 mm; Kreuzklemmen fl. 30/40 mm Kombinationen; Erdungskreuzklemme EVN 8-10/40.
- Tiefenerder-Anschlussklemmen für Ø20/Ø25 mm Erder auf Rundleiter Ø10 mm bzw. fl. 30.

### SAT-Fangeinrichtung & Blitzschutz-Zubehör
- Rohrfangstange Alu Ø16/10 mm, Länge 1,5 m bzw. 2 m.
- Isotraverse mit Rohrschelle 5/4–2", **45 sm ISO-Strecke, 60 cm**.
- Niro-Clip-Schnapphalter V2A Ø8 mm.
- Korrosionsschutzbinde Breite **50 mm**, Länge **10 m**.
- Drahtrichteisen Ø8–10 mm; Richteisen Flachband 30 mm / Runddraht Ø8–10 mm.

---

### Neozed D0-Sicherungsmaterial — Serie SCHRACK
- **D0-Sicherungslastschalter TYTAN I** bis 16 A: 1-/2-/3-polig.
- **D0-Lastschalter ARROW S** bis 63 A: 1-polig 16/25/63 A; 3-polig 16/20/25/35/50/63 A. Verschienung 35 mm², TE=27 mm.
- **D0-Lastschalter TYTAN II** bis 63 A: 1-/2-/3-polig; feste Einsätze 25/35/50 A; 1+N, 3+N, 3-polig + PEN-Klemme.
- **Sicherungsstecker TYTAN II**, 60–400 VAC, Kennlinie **gG/gL** — Farbcode/Strom: 2 A rosa (D01), 4 A braun (D01), 6 A grün (D01), 10 A rot (D01), 16 A grau (D01), 20 A blau (D02), 25 A gelb (D02), 32 A lila (D02), 35 A schwarz (D02), 40 A violett (D02), 50 A weiß (D02), 63 A kupfer (D02).
- **D0-Lasttrennschalter TYTAN T** 3-polig / 3+N (mit Hilfskontakt); Reduzierfeder D02→D01.
- **TYTAN T4P** (Notstromversorgung) 3+N: 20/25/35/50/63 A mit fixierten Passhülsen.
- **CORON 2** 1-/3-polig, 3+N; 20/25/35 A mit fixer Passhülse; Reduzierhülse D02→D01.
- **ARROW ON** Sicherungslastschalter D02; Servicebox mit 12 Einsätzen D02/40 A.
- **Sicherungsüberwachung:** TYTAN TH1-Hauptschutz 3-polig / 3+N mit Überwachung; Relais Sammel-/Einzelstörmeldung 2 Wechsler 5 A / 250 VAC; Steckerleitungen RJ10 15/100 cm.
- **TYTAN-II Superkurzschluss-Schutz** 1-polig / 1+N / 2-/3-polig / 3+N.
- **Lasttrennleisten** D0: ARROW R 63 A (Seitenmodul ab 35 A nötig) und mit fix. Passhülsen 20/25/35/50 A; TYTAN R 63 A 3-polig/3+N + fix. Passhülsen 20/25/35/50 A; CORON R 63 A + fix. 20/25/35 A; Messstecker; Sicherungsüberwachung RH1/RH4R.
- **ARROW Stripe** D02-Reitersicherungssockel E18 für 60 mm Sammelschienensystem; Streifenabdeckungen 27/36/54 mm.

### Neozed D0 — Serie Wöhner
- **D02-Lasttrennschalter 63 A:** 1-polig+N, 3-polig, 3-polig+N.
- **Schmelzeinsätze/Sockel:** D01 E14 16 A; D02 E18 63 A (1-/3-polig). Schraubkappen Kunststoff D01 E14 16 A/400 V, D02 E18 63 A/400 V; Porzellan D0 E14/E18.
- **Verschienung Teilung 27 mm:** 3-polig Stift 16 mm² (280 A); 3-polig 35 mm² (130 A).
- **Triton nach BGV A3 (VBG4)** bis 63 A: D01 1-polig 16 A; D02 1-/3-polig 63 A.
- **Secur PowerLiner / Easyliner** (60 mm Reiter): D01/D02 bis 63 A; Seitenmodul 9 mm ab 35 A bindend; D02-Reduziereinsatz für D01 2–16 A; Meldeschalter 1 Wechsler 250 VAC/5 A bzw. 30 VDC/4 A.
- **Reiter-Sicherungssockel** E18 63 A/400 V, Breiten 27/36/54 mm.

### Neozed D0 — Schmelzeinsätze & Passhülsen (Zubehör)
- **Schmelzeinsätze gG/gL** (Farbcode wie TYTAN II oben): D01 2/4/6/10/16 A; D02 20/25/35/50/63 A. Servicebox 12× D02/40 A bzw. /32 A; D0-Blindeinsatz für TYTAN R / Coron R.
- **Passhülsen D01:** 2/4/6/10 A; **D01 in D02** (Reduzier): 2/4/6/10/16 A; **D02:** 20/25/35/50 A.

### Diazed D-Sicherungsmaterial (Serie SCHRACK / Wöhner)
- Schraubkappen Sockel **EZII / EZIII** ohne Prüfloch.
- **Triton BGV A3 (VBG4)** bis 63 A: DII E27 1-/3-polig 25 A; DIII E33 1-/3-polig 63 A.
- **Schmelzeinsätze gG/gL für EZII/EZIII:** EZ II 2/4/6/10/16/20/25 A; EZ III 35/50/63 A.
- **Passeinsätze** EZII 2/4/6/10/16/20/25 A; EZIII 35/50/63 A.

---

### NH-Sicherungsmaterial — Größen, Nennströme, Schraubmaße
Durchgängige **NH-Größen-Skala** (gilt herstellerübergreifend ARROW/Wöhner):
- **Gr. 000 → 100 A bzw. 125 A** (Wöhner-Reiter); Anschluss kleinste Bauform.
- **Gr. 00 → 160 A**, Schraube **M8**.
- **Gr. 1 → 250 A**, Schraube **M10**.
- **Gr. 2 → 400 A**, Schraube **M10** (teils M12 bei Leisten).
- **Gr. 3 → 630 A**, Schraube **M12**.
- **Gr. 4a → 1600 A**, Anschluss 2× Schraube M12, 500 mm² (Wöhner SI332040).

### NH-Trenner / Unterteile — Serie ARROW (II / BLOC / BLUE)
- **ARROW BLOC Aufbau:** Gr. 000 bis 100 A (Schelle/Clips); Gr. 00 160 A M8 (1-/3-/4-polig, mit Fenstersperre); Gr. 1 250 A M10; Gr. 3 630 A M12. Prismenklemme 1,5–70 mm² (Al/Cu) für Gr. 00.
- **ARROW BLUE Aufbau:** Gr. 00 160 A M8/Schelle; Gr. 1 250 A M10; Gr. 2 400 A M10; Höhenausgleichsadapter 70→90 mm.
- **NH-Unterteile ARROW II:** Gr. 00 (M8/Bride, V-Klemme/Bride, 1-/3-polig); Gr. 1 250 A 2×M10; Gr. 2 400 A 2×M10; Neutralleiter-Stützen Gr. 00 (2×M8, lösbare PEN-Verbindung 4×/6×M8).
- **Sammelschiene 60 mm-Reiter:** ARROW BLOC Gr. 000 100 A; ARROW BLUE Gr. 00 160 A, Gr. 1 250 A, Gr. 2 400 A (Abgang oben/unten frei wählbar). 100 mm-System: Gr. 1 250 A, Gr. 2 400 A.
- **ARROW LINE Lasttrennleisten (60/100/185 mm):** Gr. 00 160 A, Gr. 1 250 A, Gr. 2 400 A schaltbar M12, Gr. 3 630 A schaltbar M12; Kuppel-Lasttrennleiste Gr. 3 630 A (Sammelschienen-Längstrennung, Abgang links/rechts). Wandler 150/400/600 A für Wandlermessung integrierbar.
- Zubehör: V-Klemmen VK160 (35–70 mm²) und VK400 (35–185/240 mm²); Sammelschiene 20×3 mm gelocht Ø8,5, Lochabstand 32 mm.

### NH-Sicherungsmaterial — Serie Wöhner
- **NH-Trenner Aufbau:** Gr. 000 125 A (Rahmenklemme 50 mm²); Gr. 00 160 A (Schelle 70 mm² / Schraube M8), optional mit elektromechanischer oder elektronischer **Sicherungsüberwachung**; **Cross Link Switch** 125 A; Gr. 1 250 A M10; Gr. 2 400 A M10; Gr. 3 630 A M12; Gr. 4a 1600 A (2×M12, 500 mm²).
- **NH-Unterteile:** Gr. 00 160 A (M8 / Schelle 1,5–70 mm², mit/ohne Berührungsschutz); Gr. 1 250 A M10; Gr. 2 400 A M10; Gr. 3 630 A M12 (1-/3-polig).
- **Neutralleiterstützen:** Gr. 00 160 A (Schelle 1,5–70 mm², trennbar); Gr. 1 250 A M8 trennbar; Gr. 2 400 A; Gr. 3 630 A M12.
- **60 mm-Reiter-Lasttrenner:** Gr. 000 125 A (Rahmenklemme 50 mm²); Gr. 00 160 A (Rahmenklemme 70 mm², auch verkürzt, mit Überwachung, Cross Link Switch 125 A, Türkupplungsdrehgriff); Gr. 1 250 A M10 (Prismenklemme Cu/Al 35–150 mm², doppelt 2×35–70 mm²); Gr. 2 400 A M10 (Prismenkl. 2×70–120 mm²); Gr. 3 630 A M12 (Prismenkl. 150–300 mm²).
- **Reiter-Lasttrennleisten (60 mm):** Gr. 00 160 A schaltbar M8/Schelle 70 mm², mit/ohne elektronische Überwachung; Prismenklemme.
- **Reiter-Lasttrennleisten (100/185 mm):** Gr. 00 160 A M8; Gr. 1 250 A M12 (Rahmenklemme Cu/Al 70–240 mm²); Gr. 2 400 A M12; Gr. 3 630 A M12 (Rahmenklemme 120–300 mm²); Klemmbügel zum bohrungslosen Aufsetzen.
- **Stromwandler für NH-Leisten:** 80/5 (5 VA), 150/5 (1,5 VA), 200/5 (1,5 VA), 250/5 / 400/5 / 600/5 (2,5 VA), Klasse GK1.
- **Türkupplungs-Drehantriebe** für LTS/LTS-F (rot/gelb), Verlängerungsachsen 300/550 mm, Meldeschalter Schalterstellung.

### NH-Sicherungseinsätze gG/gL — Nennstromreihen
- **Gr. 000/00, 400 VAC:** 4, 6, 10, 16, 20, 25, 32, 35, 40, 50, 63, 80, 100, 125, 160 A; 100/125 A auch mit „Bauchnabelmelder".
- **Gr. 000, 500 VAC:** 63, 100, 125, 160 A.
- **690 VAC:** 50, 63, 80, 100 A (Gr. 000/00); Gr. 1: 160, 200 A.
- **Gr. 1, 400 VAC:** 35, 50, 63, 80, 100, 125, 160, 200, 224, 250 A.
- **Gr. 2, 400 VAC:** 35, 50, 63, 80, 100, 125, 160, 200, 225, 250, 315, 350, 355, 400 A.
- **Gr. 3, 400 VAC:** 200, 250, 315, 400, 500, 630 A; mit Anschlusslaschen **800 A**.
- **Trennmesser:** Gr. 00 160 A, Gr. 1 250 A, Gr. 2 400 A, Gr. 3 630 A.

### Sammelschienensysteme 60 mm — Serie Wöhner
- **Universal-Sammelschienenträger** 3-/4-/5-polig (3 Phasen + N + PE); für Schienen 10/12/20/30 × 5/10 mm. Träger für T-/TT-Profil: 60 mm 1600 A (3-polig, TT-Profil), 2500 A (TTT-Profil).
- **Sammelschiene verzinnt — Stromtragfähigkeit nach Querschnitt** (jeweils 2,4 m lang, wenn nicht anders):
  - 12×5 mm → **200 A**; 15×5 mm → 250 A; 20×5 mm → 320 A; 30×5 mm → 450 A.
  - 20×10 mm → 520 A; 30×10 mm → **630 A** (auch 3,6 m); 40×10 mm → 850 A; 50×10 mm → 1000 A; 60×10 mm → 1250 A.
  - 80×10 mm → 1500 A; 100×10 mm → 1800 A; 120×10 mm → 2100 A.
- **Sammelschienen-Längsverbindungen:** für 12×5…20×10 (630 A); 20–30×5/10 (630 A, Längen 40/95/150 mm); TT-Profil 1600 A (75/150 mm) und 2500 A; 30–120×10 (750 A 40 mm / 1000 A 60 mm); elastische Verbindungssets 1600 A.
- **Leiteranschlussklemmen** 5 mm / 10 mm Schienen für 1,5–16, 4–35, 16–70, 16–120 mm².
- **Spreizklemmen:** Cu/Al 95–185 mm² (max 500 A); 35–150 mm² (max 480 A); für lamellierte Cu-Schienen 5×24×1 … 10×30×1; bis 20×5…30×10 (Cu 95–300, Al 120–300 mm², max 600 A).
- **Anschlussklemmplatten 60 mm:** 1,5–16, 6–50, 35–120, 95–185, 150–300 mm² (Cu/Al); Anschlusssets 120–300 mm² 3-/4-polig.
- **Abdeckhauben** 54/84/135/270 mm breit (Anschlussraum/Reserveplätze).
- **Profilklemmen:** TT-Profil 1600 A (Klemmenraum 51×21 / 41×20–42 mm); T/TT 51×20–42 mm; TTT 101×23–45 mm.
- **Schraubanschluss aufsteckbar:** 10 mm/M8 (490 A), 10 mm/M10 (630 A).
- **Verbindungsklemmen** für 5/10 mm Schienen, Höhe 5–20 mm, diverse Breiten (25×20 bis 63×50).
- **Sammelschienenabdeckung** für Schienen 12–30×5 / 12–30×10 mm; Leerfeldabdeckung 60 mm-System 700 mm breit.
- **Bezeichnungsschilder** Ø15 mm selbstklebend: PE (grün-gelb), N (blau), PE/N; **PE/N-Auftrennpunkt-Sticker nach E 8001** (VE = 1 Bogen, 70 Stk) — einzige explizite Norm-Referenz in diesem Teil (**ÖVE/ÖNORM E 8001**).

### Norm- & Praxis-Relevanz (Zusammenfassung)
- **Ableiter-Auswahl** strikt nach Netzform: TN-C = 3+0, TN-S = 4+0, TT = 3+1 (Hard Rule für Verteiler-Stückliste).
- **Sicherungs-Farbcode gG/gL** (D01/D02) ist eindeutig strom-zugeordnet → nutzbar zur Plausibilisierung von Stromkreis-Absicherung.
- **NH-Größenraster** (000=100/125 A, 00=160 A, 1=250 A, 2=400 A, 3=630 A, 4a=1600 A) und **Schienen-Strombelastbarkeit** (12×5=200 A … 120×10=2100 A) sind dimensionierungsrelevant für Hauptverteiler/Zuleitungen.
- **E 8001** als einzige Norm explizit (PE/N-Auftrennpunkt-Kennzeichnung).
