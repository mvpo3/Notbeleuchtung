# k-sort-a20 — Teil 24
> Quelle: k-sort-a20 (buecher) · Seiten 961-1000.

Dieser Teil ist ein Ausschnitt aus dem Schrack-Produktkatalog (Bestellteil, Spalten BEST. NR. / STORE / UVP) und behandelt durchgehend die **strukturierte Netzwerkverkabelung (Kupfer + LWL)**: Patchkabel (RJ45 Cu, LWL, Koax), TOOLLESS-LINE-Modulsystem (RJ45-Buchsen, Kupplungen, Datendosen, Patchpanele) sowie Installations-/Verlegekabel S/FTP, F/FTP, U/FTP, U/UTP, SF/UTP, F/UTP. Kein normativer Fließtext (keine ÖNorm/OVE-Paragraphen) — der bewahrenswerte Fachinhalt sind die technischen Produktspezifikationen (Kategorien, Brandklassen nach CPR, AWG-Querschnitte, Schirmung, Frequenzbänder, Maße, Cu-Gewichte). Diese sind für Materialauswahl/Stückliste im E-Plan (Datenverkabelung) relevant.

## Inhalt

### Bestell-/Katalogkonvention
- "Best. Nr. blau" = Lagerware, üblicherweise versandbereit am Bestelltag; zusätzliche Abholverfügbarkeit in jedem Schrack Store.
- Spalten je Produktzeile: BEZEICHNUNG · VERFÜGBAR · STORE · BEST. NR. · PREG · UVP. STORE-Nummern gruppieren Produktbereiche: 5100/5110/5111/5112/5120 = Netzwerk Cu, 5400/5410 = LWL, 5500 = Koax/SAT/BK, 5900 = Adapter.
- Naming-Logik Patchkabel-BestNr. (Cu): H + Kat (5=Cat.5e, 6=Cat.6/6A) + G/U (Geschirmt/Ungeschirmt) + S/T/L (Bauform: S=LED, T=Standard geschirmt Cat.6A, L=PVC/LS0H Standard) + Farbcode + Länge (z.B. 02K0 = 2,0 m; 00K5 = 0,5 m) + Farbsuffix (G grau, B blau, R rot, Y gelb, U grün, N orange, S schwarz, A aqua).

### Patchkabel RJ45 Cu — Kategorien, Mantel, Längen
- **LED Patchkabel RJ45 geschirmt Cat.6A 10GB, LS0H** (Serie H6GS…): Längen 0,33 / 0,5 / 1,0 / 2,0 / 3,0 / 5,0 / 7,0 / 10,0 / 15,0 / 20,0 / 30,0 / 50,0 m. Farben grau/blau/rot/gelb/grün/aqua. Preisbeispiele grau: 0,33 m=8,91; 0,5 m=9,05; 1,0 m=10,23; 2,0 m=12,40; 3,0 m=14,55; 5,0 m=18,94; 10,0 m=29,85; 50,0 m=126,90.
- **Push-Pull Patchkabel RJ45 geschirmt Cat.6A 10GB, LS0H** (H6GP…), grau, 0,5–10,0 m: 0,5 m=9,76; 1,0 m=10,16; 1,5 m=10,78; 2,0 m=11,06; 3,0 m=14,09; 5,0 m=16,66; 10,0 m=28,23.
- **Patchkabel RJ45 geschirmt Cat.6A 10GB, LS0H** (Standard, H6GT…, STORE 5112): bis 50,0 m (grau), Farben inkl. orange/schwarz. Preise grau: 0,5 m=8,04; 1,0 m=9,26; 2,0 m=11,29; 3,0 m=13,38; 5,0 m=17,63; 7,0 m=19,93; 10,0 m=25,45; 15,0 m=35,29; 20,0 m=46,55; 30,0 m=67,92; 50,0 m=110,30.
- **Patchkabel RJ45 geschirmt Cat.6, PVC** (H6GL…, STORE 5111): 0,5–20,0 m, grau 0,5 m=4,67 … 20,0 m=36,01.
- **Patchkabel RJ45 geschirmt Cat.5e, PVC** (H5GL…, STORE 5110): 0,5–20,0 m, grau 0,5 m=1,92 … 20,0 m=26,23.
- **LED Patchkabel RJ45 ungeschirmt Cat.6, LS0H** (H6US…): bis 30,0 m, grau 0,5 m=7,97 … 30,0 m=58,33.
- **Patchkabel RJ45 ungeschirmt Cat.6, PVC** (H6UL…): bis 20,0 m, grau 0,5 m=4,21 … 20,0 m=28,34.
- **Patchkabel RJ45 ungeschirmt Cat.5e, PVC** (H5UL…): bis 20,0 m, grau 0,5 m=1,74 … 20,0 m=23,83.
- Mantelmaterialien durchgängig: **LS0H** (halogenfrei) bei Cat.6A/LED-Serien, **PVC** bei Cat.6/Cat.5e-Budget-Serien.

### Patchkabel-Zubehör LED
- **Patchfinder Lichtquelle** HLEDTOOL = 56,35; **LED Detektor Pro** (mit Akku + USB-Ladekabel) HLEDTOOL1 = 140,20.
- **Clips zur Farbcodierung** je 100 Stück (blau/rot/gelb/grün) je 33,16.

### LWL-Patchkabel Duplex (Glasfaser)
Konventionen: Serie HLP2x + Steckerpaar (LL=LC/LC, LC=LC/SC, LT=LC/ST, LF=LC/FC, CC=SC/SC, CF=SC/FC, TT=ST/ST, TC=ST/SC, TF=ST/FC, FF=FC/FC) + Länge + F. Fasertyp über Ziffer x kodiert.
- **OM2 50/125 µm**, LS0H-3, **orange** (HLP25…): z.B. LC/LC 1,0 m=40,47; 10,0 m=53,28; 20,0 m=67,44. SC/SC 1,0 m=25,05; 10,0 m=37,78. ST/ST 1,0 m=24,59. Auch LC/SC, LC/ST, LC/FC, SC/FC, ST/SC, ST/FC, FC/FC.
- **OM3 50/125 µm**, LS0H-3, **aqua** (HLP23…): LC/LC 1,0 m=46,69; 10,0 m=70,56. SC/SC 1,0 m=29,52; 10,0 m=53,36. Auch LC/SC, LC/ST, ST/ST, ST/SC.
- **OM4 50/125 µm**, LS0H-3, **violett** (HLP24…): LC/LC 1,0 m=51,90; 10,0 m=104,90. LC/SC 1,0 m=49,73; 10,0 m=102,80. SC/SC 1,0 m=47,51; 10,0 m=102,40.
- **OM1 62,5/125 µm**, LS0H, **orange** (HLP26…): LC/LC 1,0 m=40,86; 10,0 m=55,79. SC/SC 1,0 m=25,46; 10,0 m=40,47. Auch LC/SC, LC/ST, LC/FC, SC/FC, ST/ST, ST/SC, ST/FC, FC/FC.
- **OS2 9/125 µm** (Singlemode), LS0H-3, **gelb** (HLP29…): LC/LC 1,0 m=41,62; 10,0 m=52,24. SC/SC 1,0 m=32,85; 10,0 m=43,46. Auch LC/SC, LC/FC, SC/FC, ST/ST, ST/SC, ST/FC, FC/FC.
- **Farbcode-Merkregel Faserklasse:** OM2=orange, OM3=aqua, OM4=violett, OM1=orange, OS2=gelb (Singlemode).

### Koax-/SAT-/BK-Patchkabel (STORE 5500)
- **Koax 2×F-Quick gerade, >90 dB, Class A, weiß** (HS4HC…): 0,5 m=3,64; 1,0 m=4,14; 1,5 m=4,80; 2,5 m=5,78; 3,5 m=6,82; 5,0 m=8,51.
- **SAT Koax 2×F-Quick gerade, Class A, weiß** (HSATPQG…, Serie SAK): 1,5 m=4,45; 2,5 m=5,62; 5,0 m=8,81; 10,0 m=14,02.
- **SAT Koax 2×F-Stecker verschraubbar, gerade, Class A** (HSATPSG…, Serie MAK): 0,2 m=5,32; 0,5 m=6,09; 1,5 m=5,87; 2,0 m=7,89.
- **BK Koax 2×IEC (Male/Female) gerade, Class A, weiß** (HSBKPIG…, Serie BAK): 1,5 m=3,81; 2,5 m=5,09; 5,0 m=8,07.
- **BK Koax 2×IEC gewinkelt, Class A, weiß** (HSBKPIW…): 1,5 m=4,13; 2,5 m=4,99; 5,0 m=7,86; 10,0 m=13,92.
- **SAT Fensterdurchführung**, Leiterplattenfolie transparent, 2×F-Buchse, 25 cm (HSATPFD, SAK 25-01) = 14,12.

### TOOLLESS LINE Modulsystem — RJ45-Buchsen (Cu)
Schrack-Formate: **SFA (Format A)** und **SFB (Format B)**. Klassenbezeichnung "Klasse EA" = Cat.6A.
- **Cat.6A 10GB 4PPoE (100 W), SFA**: HSEMRJ6GWA = 7,95. **Klasse EA 10GB 4PPoE 100 W, SFA**: HSEMRJ6GWT = 7,56.
- **Cat.6A 10GB 4PPoE 100 W, SFB**: HSEMRJ6GBA = 8,29.
- **Cat.6 geschirmt, SFA**: HSEMRJ6GWS = 6,65. **Cat.6 geschirmt, SFB**: HSEMRJ6GBS = 6,99.
- **Cat.5e geschirmt, SFA**: HSEMRJ5GWS = 6,37.
- **Cat.6 ungeschirmt, SFA**: HSEMRJ6UWS = 6,55. **Cat.5e ungeschirmt, SFA**: HSEMRJ5UWS = 5,24.
- **Staubschutzklappensets** für HSEMRJ6GWA/T, je 25 Stück, Farben weiß/blau/rot/gelb/grün/schwarz, je 7,46.
- **Staubschutzkappe** für RJ45 Buchse, grau, HM5LFDUS07 = 0,71.
- **Reparaturkit/Kabelverbinder** für Installationskabel Cat.6A 10GB 4PPoE (100 W), AWG26–AWG22, kurze Bauform, HCAT6AREPT = 44,11.
- **Durchführungskupplung RJ45 geschirmt Klasse EA 10GB, SFA**: HSEMRKRGWS = 10,51.

### Koax-/HDMI-/USB-/LWL-Kupplungen (SFA)
- **Koax F-Buchse/F-Buchse, SFA**: HSEMRKFFWS = 5,78.
- **HDMI Kupplung weiß** (A-Buchse/A-Buchse) HSEMRHDMWS = 10,77; **USB 3.0 A-A Kupplung weiß** HSEMRU3AWS = 11,20; **HDMI Adapter 90°** (A-Stecker/A-Buchse) Q7AH0005 = 4,90.
- **LWL Kupplungen**: leer LC-Duplex/SC-Simplex (SFA) HSEMRLLLWS = 2,93; LC-Duplex Kunststoff Multimode (phbr, ohne Flansch, grau) HMOL000103 = 9,71; LC-Duplex Singlemode (zirc, ohne Flansch, blau) HMOL000104 = 16,58; SC-Simplex Multimode (phbr, Flansch, grau) HMOL000058 = 2,92; SC-Simplex Singlemode (zirc, Flansch, blau) HMOL000055 = 5,99; SC/APC-Simplex Singlemode (ohne Flansch, grün, ECO) HMOL000107 = 2,92.

### Datendosen (Aufnahme für SFA/SFB-Module)
- **80×80 mm leer, schräg, RAL9010 Reinweiß**: 1 Modul HSED01UW2S=4,85; 2 Module HSED02UW2S=5,07; 3 Module HSED03UW2S=7,66; 2 Module gerade HSED02UW1S=5,07. Beschriftungsfeld+Schraubenset HSEDZBES=0,62. AP-Rahmen B80×H40×T80 mm HSEAP842WF=2,60.
- **80×80 mm SFB, UAE-Zentralplatte** (Design-Schalterprogramm-kompatibel), 2 Module, schräg, RAL9010: HSED02UWBS=5,63.
- **Aufputz-Gehäuse leer (SFA/SFB), RAL9010 Reinweiß**: 1 Modul B46×H30×T65 HSED01AW3S=4,36; 2 Module B68×H30×T65 HSED02AW3S=4,88; 4 Module B118×H30×T85 HSED04AW3S=12,12; 6 Module B173×H30×T85 HSED06AW3S=15,26; 12 Module (SFA) B172×H38×T122 HSED12AW3S=20,23.
- **Einsätze 45×45 mm leer (SFA/SFB), RAL9010**: 2 Module schräg HSEMD02W2F=2,34; 45×22,5 1 Modul gerade HSEMD01W1F=1,82; Blindabdeckung 45×22,5 HSEMDZ1W1F=0,74. Tragring-Rahmen: 1-fach B80×H80 HSEMDR2W0F=2,55; 2-fach B148×H80 HSEMDR4W0F=2,88; 3-fach B205×H80 HSEMDR6W0F=3,97. AP-Rahmen 2-fach B148×H45×T80 HSEMAP4W3F=5,61; 3-fach B205×H45×T80 HSEMAP6W3F=7,93. Hutschienenadapter HSEMHUT001=8,20.

### IP44-Datendosen + Hutschienenadapter
- **IP44 AP-Gehäuse leer**, versperrbar/gleichschließend, 90×90×90 mm, RAL7035 Lichtgrau: HSEIP44APT=109,20. Kabelverschraubung **M25** mit Dichtung für 2 Kabel **3–8 mm** HSEIP44AKT=14,02. Einsatz für 2 Module HSEIP44AUT=16,60.
- **IP44 UP-Gehäuse leer**, versperrbar/gleichschließend, 90×35×90 mm, RAL7035: HSEIP44UPT=123,50; UP-Einbaudose HSEIP44UDT=10,41.
- **IP44/IP20 geschlossen/offen AP-Gehäuse** für 2 Module, B76×H58×T88 mm, schwarz/grau: HSEIP44AP=44,32.
- **Hutschienenadapter leer** für 1 Modul (SFA/SFB): HSERH010GS=16,34.

### Patchpanele 19" / 10" / Aufputz
- **19" leer, 24 Module, 1HE, RAL7035, Verriegelung unten**: HSER0240GS=44,65. **48 Module, 2HE**: HSER0480GS=93,82.
- **19" einteilig, 24 Module, 1HE**: RAL7035 Verriegelung unten HSER0240GP=44,70; RAL9005 schwarz HSER0240SP=44,70; RAL7035 Verriegelung oben HSER0240GV=44,65.
- **19" einteilig, 24 Module, mit Beschriftungsfeldern, Verriegelung oben**: HSER0240GZ=107,50.
- **19" High Density 48 Module, 1HE, Edelstahl (SFB)**: HSER0480SB=94,10.
- **10" leer, 12 Module, 1HE, RAL7035, Verriegelung unten**: HSER0120GS=45,67.
- **Patchpanel AP-Gehäuse leer, 8 Module, RAL7035**: HSER0080GV=79,20; Adapter-Clips Hutschienenmontage (2 Stück) HSERHUTADA=11,77.
- **Blindabdeckung unbenutzte Patchpanel-Ports, RAL9010**: HSEMRZ01WF=0,68.

### Werkzeuge
- Seitenschneider watenfrei, Draht bis 1,3 mm DM: HTOOL00002=49,81; bis 1,0 mm DM: HTOOL00003=25,93.
- Abisolierwerkzeug Mantel von Installationskabeln HTOOL00004=60,74; Mantel + Folie HTOOL00005=51,11.

### Installations-/Verlegekabel (mit Cu-Gewicht kg/km, CPR-Brandklasse)
CPR-Klassen (DIN EN 50575/CPR-Kennung Brandverhalten): Bca > B2ca > Cca > Dca > Eca; Zusätze s=Rauch, d=brennendes Abtropfen, a=Säure (jeweils niedrigere Zahl = besser). Schirmungs-Code: S/FTP, F/FTP, U/FTP, U/UTP, SF/UTP, F/UTP.
- **S/FTP Cat.7A 1200 MHz, 50 % Geflecht, LS0H-3** (HSEKP422…, STORE 5120): 4×2×AWG22/1, B2ca-s1a-d1-a1, blau/gelb, Cu 35 kg/km, UVP 110,20 (Box) bzw. als Trommel 1000 m/500 m. Doppelvariante 2×(4×2×AWG22/1), Cca-s1-d1-a1, Cu 70 kg/km, UVP 220,50.
- **S/FTP Cat.7A 1500 MHz, LS0H-3** (HSEKP422HP): 4×2×AWG22/1, Dca-s2-d2-a1, blau, Cu 34 kg/km, 110,20.
- **S/FTP Cat.7 1000 MHz, 40 % Geflecht, LS0H** (HSEKP423HB): 4×2×AWG23/1, Dca-s2-d1-a1, blau, Cu 28 kg/km, 81,93 (Trommel/Box 100 m). Doppel 2×(4×2×AWG23/1) Dca-s2-d2-a1, Cu 56 kg/km, 163,90.
- **S/FTP Cat.7 1000 MHz, 30 % Geflecht, LS0H/LS0H-3** (HSEKP4233P u.a.): 4×2×AWG23/1, Dca-s1-d1-a1 bzw. Dca-s2-d1-a1, Cu 25,5 kg/km, UVP 94,06 / 78,03. Doppel 2×(4×2×AWG23/1) Cca-s1-d1-a1 bzw. Dca-s1-d1-a1, Cu 51 kg/km, 188,00 / 156,00.
- **S/FTP Cat.7 1200 MHz, 65 % Geflecht, LS0H-3, B2ca, wasserblau** (HVSKP423BA): 4×2×AWG23/1, Cu 32,5 kg/km, 227,20.
- **S/FTP Cat.7 1200 MHz, 65 %, LS0H-3, B2ca, wasserblau, mit LWL-Röhrchen** (HVSKT823BA): 2×(4×2×AWG23/1), Cu 65 kg/km, 475,30.
- **S/FTP Cat.7 800 MHz, PE OUTDOOR, schwarz** (HCKP08-04E): 4×2×AWG23/1, Cu 33 kg/km, 660,50.
- **S/FTP Cat.7 1000 MHz, PE OUTDOOR, schwarz** (HCKP10N04E): 4×2×AWG23/1, Cu 34 kg/km, 453,70.
- **S/FTP Cat.6A 500 MHz, 30 % Geflecht, LS0H-3** (HSEKP4233A): 4×2×AWG23/1, Dca-s2-d2-a1, schwarz, Cu 24 kg/km, 76,90.
- **F/FTP Cat.6A 500 MHz, LS0H** (HSEKP423HA): 4×2×AWG23/1, Dca-s2-d2-a1, blau, Cu 20 kg/km, 69,90. Doppel 2×(4×2×AWG23/1) Cu 40 kg/km, 139,70.
- **U/FTP Cat.6A 500 MHz, LS0H, Cca s1a,d1,a1** (HSEKF423CA): 4×2×AWG23/1, blau, Cu 20 kg/km, 100,50.
- **SF/UTP Cat.5e** (HSEKS424PP): 4×2×AWG24/1, PVC, Eca, blau, Cu 23 kg/km, 67,63.
- **F/UTP Cat.5e** (HSEKF424…): 4×2×AWG24/1, Eca, blau, Cu 17 kg/km; PVC 60,07 / LS0H 65,97 / PE OUTDOOR schwarz 87,40 (Box-Variante PVC 54,61).
- **U/UTP Cat.6 300 MHz, LS0H-3-25** (HSEKU4233B): 4×2×AWG24/1, B2ca-s1a-d1-a1, blau, Cu 19 kg/km, 99,53.
- **U/UTP Cat.6 300 MHz, LS0H-3-25, Cca s1a,d1,a1** (HSEKU423CB): 4×2×AWG24/1, blau, Cu 18,5 kg/km, 93,48.
- Liefereinheiten durchgängig: Box 100 m, Trommel 500 m, Trommel 1000 m.
