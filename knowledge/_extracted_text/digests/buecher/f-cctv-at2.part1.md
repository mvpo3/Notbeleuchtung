# f-cctv-at2 — Teil 1
> Quelle: f-cctv-at2 (buecher) · Seiten 41-48.

Dieses Dokument ist die **Schrack Technik CCTV-Produktbroschüre/Preisliste** (Video-Überwachung, Serien NEXT/ADVANCED/SMART). Teil 1 (S. 41-48) umfasst das **Glossar der Netzwerk-/Video-Begriffe**, die **Produktübersicht mit Bestellnummern und UVP-Preisen** (IP-Kameras, NVR-/XVR-Recorder, AHD-Kameras, Installationszubehör, Serviceleistungen), einen DSGVO-Hinweis, Preis-/Lieferbedingungen sowie die Standort-/Niederlassungsliste von Schrack. Es ist kein ÖNorm-/OVE-Normtext, sondern ein Hersteller-Katalog — relevant primär als Produkt- und Komponentenreferenz für CCTV-Planung.

## Inhalt

### Glossar — Netzwerk- und Video-Begriffe (S. 41-42)

- **ARP (Address Resolution Protocol):** Netzwerkprotokoll, ermittelt zu einer Netzwerkadresse (IP-Adresse) die zugehörige physische MAC-Adresse und trägt die Zuordnung in die ARP-Tabellen der beteiligten Rechner ein. Fast ausschließlich zur MAC-Ermittlung bei IPv4-Adressen; bei IPv6 übernimmt ein anderes Protokoll diese Funktion.
- **IPv4/IPv6 (Internet Protocol Version 4/6):**
  - IPv4-Adressen sind **32 Bit** lang → maximal **4.294.967.296** Adressen (real nicht alle verteilbar, da Adressblöcke reserviert).
  - IPv6-Adressen sind **128 Bit** lang: erste **64 Bit** = Präfix, letzte **64 Bit** = (bis auf seltene Ausnahmen) eindeutiger Interface-Identifier der Netzwerkschnittstelle.
- **SMTP (Simple Mail Transfer Protocol):** Protokoll der Internetprotokollfamilie zum Austausch von E-Mails; vorrangig zum Einspeisen und Weiterleiten. Das Abholen erfolgt durch andere, spezialisierte Protokolle.
- **API (Application Programming Interface):** Programmteil, den ein Softwaresystem anderen Programmen zur Anbindung bereitstellt. Definiert die Programmanbindung nur auf Quelltext-Ebene; benötigt detaillierte Dokumentation der Schnittstellen-Funktionen samt Parametern (Papier oder elektronisch).
- **PPPoE (Point-to-Point over Ethernet):** Verwendung des PPP-Protokolls über Ethernet. Zwei Phasen: (1) **PPPoE Discovery** — MAC-Adresse eines Access Concentrators wird ermittelt (logischer Endpunkt der PPP-Sitzungen, zuständig u.a. für Zuweisung von Sitzungsparametern wie IP-Adressen); (2) **PPP Session** — Datenaustausch nach PPP.
- **CBR/VBR:**
  - **CBR (Constant Bit Rate):** Bitrate bleibt immer gleich, unabhängig von Bildänderung.
  - **VBR (Variable Bit Rate):** Bitrate passt sich an, spart Speicherplatz (Qualitätsverlust möglich).
- **WAN (Wide Area Network):** Rechnernetz über sehr großen geografischen Bereich (mehrere Länder/Kontinente), im Gegensatz zu LAN/MAN. Verbindet verschiedene LANs (auch einzelne Rechner). Teils organisationseigen, teils von Internetanbietern errichtet zur Internet-Anbindung.
- **UPnP (Universal Plug and Play):** Herstellerübergreifende Ansteuerung von Geräten (Audio-Geräte, Router, Drucker) über IP-basiertes Netzwerk, unabhängig von zentraler Kontrolle durch ein Residential Gateway (Schnittstelle zwischen Wohnumgebung und Außenwelt).
- **P2P (Peer-to-Peer):** Kommunikation unter Gleichgestellten in einem Rechnernetz. In reinem P2P-Netz sind alle Computer gleichberechtigt und können Dienste nutzen wie bereitstellen.
- **FTP (File Transfer Protocol):** Netzwerkprotokoll zur Datenübertragung über IP-Netze: Client→Server (Hochladen), Server→Client (Herunterladen), clientgesteuert zwischen zwei FTP-Servern (File Exchange Protocol). Erlaubt auch Anlegen/Auslesen von Verzeichnissen, Umbenennen/Löschen von Dateien und Verzeichnissen.
- **SNMP (Simple Network Management Protocol):** Netzwerkprotokoll zur Überwachung und Steuerung von Netzwerkelementen (Router, Server, Switches) von zentraler Station aus.
- **CVBS (Composite Video):** Analoges Verfahren zur Übertragung eines Bildkanals (vergleichbar einem einzelnen Fernsehkanal), **ohne Audio/Ton**. Gesamte Bildinformation über eine einzige Leitung → vergleichsweise schlechte Bildqualität. Bildformat PAL, SECAM oder NTSC; stets analoges Signal in normaler Auflösung, **niemals HDTV**.
- **PAL/NTSC:** Zwei Verfahren zur Farbübertragung beim analogen Fernsehen.
  - **PAL (Phase-Alternating-Line):** v.a. Europa, Australien, viele Länder in Afrika/Asien/Südamerika. Entwickelt, um die bei NTSC auftretenden störenden Farbton-Fehler automatisch zu kompensieren.
  - **NTSC (National Television Systems Committee):** weite Teile Amerikas, einige Länder Ostasiens; Farbton-Korrektur nur manuell und unbefriedigend.
  - Beide Verfahren gegen Ende der 2000er größtenteils durch digitales Fernsehen ersetzt.
- **NTP (Network Time Protocol):** Standard zur Mitteilung der aktuellen Uhrzeit an intelligente Endgeräte über das Internet; Synchronisierung von Echtzeituhren über paketbasierte Netze. Zusätzlich **SNTP (Simple NTP)** als vereinfachte Version.
- **ISP (Internet Service Provider / Provider):** Anbieter von Diensten/Inhalten/technischen Leistungen für Nutzung und Betrieb von Internetinhalten (z.B. Internetzugang, Domain-Hosting, Server-Hosting).

### Produktübersicht — IP-Kameras NEXT (S. 43)

Format: Bezeichnung · Best.-Nr. · PREG · UVP (EUR, exkl. MWSt.).

| Bezeichnung | Best.-Nr. | PREG | UVP |
|---|---|---|---|
| BASIC Bullet colour 4MP IP-Kamera, 2.8mm, IR20m, IP67, AI | CTIBN4F1A- | 3600 | 164,10 |
| PRO Bullet colour 4MP IP-Kamera, 2.8mm, IR50m, IP67, AI | CTIBN4FA-- | 3600 | 329,00 |
| PRO Bullet colour 4MP IP-Kamera, 2.8-12mm, IR50m, IP67, AI | CTIBN4ZA-- | 3600 | 458,90 |
| 4K Bullet colour 8MP IP-Kamera, 2.8mm, IR50m, IP67, AI | CTIBN8FA-- | 3600 | 536,40 |
| 4K Bullet colour 8MP IP-Kamera, 2,8-12mm, IR50m, IP67, AI | CTIBN8ZA-- | 3600 | 698,20 |
| BASIC Turret colour 4MP IP-Kamera, 2.8mm, IR20m, IP67, AI | CTITN4F1A- | 3600 | 164,10 |
| PRO Turret colour 4MP IP-Kamera, 2.8mm, IR30m, IP67, AI | CTITN4FA-- | 3600 | 314,00 |
| PRO Turret colour 4MP IP-Kamera, 2.8-12mm, IR50m, IP67, AI | CTITN4ZA-- | 3600 | 460,70 |
| 4K Turret colour 8MP IP-Kamera, 2.8mm, IR30m, IP67, AI | CTITN8FA-- | 3600 | 489,80 |
| 4K Turret colour 8MP IP-Kamera, 2.8-12mm, IR50m, IP67, AI | CTITN8ZA-- | 3600 | 699,70 |

### NVR-Recorder NEXT (S. 43)

| Bezeichnung | Best.-Nr. | PREG | UVP |
|---|---|---|---|
| Video Recorder-NVR NEXT Serie 4CH, 6MP, 4 PoE, 1 TB HDD | CTN4N6PA-- | 3600 | 618,70 |
| Video Recorder-NVR 8CH, 4K, 8 PoE, NO TB HDD, 8MP | CTN4N6PASL | 3600 | 359,00 |
| Video Recorder-NVR NEXT Serie 8CH, 6MP, 8 PoE, 1TB HDD | CTN8N6PA-- | 3600 | 785,90 |

### IP-Kameras ADVANCED (S. 43)

| Bezeichnung | Best.-Nr. | PREG | UVP |
|---|---|---|---|
| 4K Bullet colour 8MP IP-Kamera, 2.8-12mm, IR70m, IP67, AI | CTIBA8Z1B- | 3600 | 982,80 |
| 4K Turret colour 8MP IP-Kamera, 2.8-12mm, IR50m, IP67, AI | CTITA8ZB-- | 3600 | 881,50 |
| Kennzeichenerkennungs-IP-Kamera, 7-22mm, IR50m, IP67, AI | CTILPA02ZA | 3600 | 1.651,00 |
| PTZ IP-Kamera, 4.8-120mm, IR150m, IP67, 25x Opt. Zoom, AI | CTIPT2Z25A | 3600 | 1.489,00 |

### NVR-Recorder ADVANCED (S. 43)

| Bezeichnung | Best.-Nr. | PREG | UVP |
|---|---|---|---|
| Video Recorder-NVR ADVANCED Serie 4CH, 8MP, 4 PoE, 1TB HDD | CTN4A8PB-- | 3600 | 882,60 |
| Video Recorder-NVR ADVANCED Serie 8CH, 8MP, 8 PoE, 1TB HDD | CTN8A8PB-- | 3600 | 1.414,00 |
| Video Recorder-NVR ADVANCED Serie 32CH, 8MP, NO HDD, AI | CTN32A8SL- | 3600 | 2.118,00 |
| Video Recorder-NVR ADVANCED Serie 64CH, 8MP, NO HDD, AI | CTN64A8SL- | 3600 | 4.440,00 |

### AHD-Kameras SMART (S. 43)

| Bezeichnung | Best.-Nr. | PREG | UVP |
|---|---|---|---|
| BASIC Bullet colour 5MP AHD-Kamera, 3,6mm, IR25m, IP67 | CTABS5FB-- | 3600 | 143,38 |
| PRO Minidome colour 5MP AHD-Kamera, 3,6mm, IR20m, IP67 | CTADS5FB-- | 3600 | 143,38 |

### XVR-Recorder SMART (S. 43)

| Bezeichnung | Best.-Nr. | PREG | UVP |
|---|---|---|---|
| Video Recorder-XVR NEXT Serie 4 BNC/2IP, 5MP, 1TB HDD | CTD4N5A--- | 3600 | 572,60 |

### IP/AHD-Kamera-Zubehör (S. 43)

| Bezeichnung | Best.-Nr. | PREG | UVP |
|---|---|---|---|
| Kunststoff-Anschlussdose für IP-Kameras, weiß | CTJS1PA--- | 3600 | 10,32 |
| Metall-Anschlussdose für Kameras, weiß | CTJSF66A-- | 3600 | 41,26 |
| Rückwand zur Montage von Kameras | CTPS1A---- | 3600 | 61,85 |
| Grundplatte für Minidome-Kamera, Druckguß Aluminium, weiß | CTWSF1A--- | 3600 | 46,43 |
| Mastbefestigung zur Montage von NEXT/ADVANCED-IP-Kameras | CTPMAA---- | 3600 | 102,10 |
| Metall-Anschlussdose, Bullet IP-Kameras, IP66, weiß | CTJBABA--- | 3600 | 70,84 |
| Metall-Anschlussdose, Turret IP-Kameras, IP66, weiß | CTJBATVA-- | 3600 | 90,19 |
| Metall-Anschlussdose für ADVANCED IP-Kameras, IP66, weiß | CTJBATBBA- | 3600 | 79,90 |
| Deckenmontage-Zubehör für IP-PTZ-Kameras, weiß | CTCMAPTZA- | 3600 | 96,75 |

Hinweis: Best.-Nr. blau = Lagerware, üblicherweise versandbereit am Bestelltag.

### Installationszubehör (S. 44)

| Bezeichnung | Best.-Nr. | PREG | UVP |
|---|---|---|---|
| S/FTP Kabel Cat.7, 4x2xAWG23/1, 1000 MHz, PE OUTDOOR, schwarz | HCKP10N04E | 5100 | 479,50 |
| F/FTP Kabel Cat.6a, 4x2xAWG23/1, 500 MHz, LS0H-3, Dca, blau | HSEKP423HA | 5120 | 77,16 |
| TOOLLESS LINE Buchse RJ45 geschirmt Cat.6 (SFB) | HSEMRJ6GBS | 5100 | 7,39 |
| Feldkonfektionierbarer RJ45-Stecker geschirmt Cat.6a, gerade | HSISR6SI3A | 5390 | 30,91 |
| Durchführungskupplung RJ45 geschirmt Klasse Ea 10GB (SFA) | HSEMRKRGWS | 5100 | 11,09 |
| Patchkabel flach RJ45 ungeschirmt Cat.6, PVC, grau, 0,15 m | H6UXG00K1G | 5100 | 7,87 |
| PoE-Injektor (802.3af), Fast Ethernet, Netzteil intern, 15,4 W | QLPOI2002 | 5900 | 67,66 |
| Krimpzange für BNC | CT43670--- | 3600 | 99,46 |
| BNC-Stecker zum Krimpen | SP43661--- | 3600 | 2,24 |
| Steckerbuchse zum Krimpen | CTCONAL01A | 3600 | 4,14 |
| Koaxialkabel RG-59/U, 75 Ohm, 100 m | HRG59BU000 | 6600 | 98,88 |
| Koaxialkabel RG-59/U + 2x 1 mm², 75 Ohm, 100 m | CT43755--- | 3600 | 186,90 |
| Einphasiges Netzgerät, geregelt, REG, 230/12 VDC, 2 A | LP743201-A | 2320 | 87,97 |

### Serviceleistungen (S. 44)

| Bezeichnung | Best.-Nr. | PREG | UVP |
|---|---|---|---|
| Fahrtkostenpauschale pro km | CT-FAHRT-- | 3690 | 0,54 |
| Fahrzeit für An- und Abreise | CT-FAHRTKO | 3690 | 89,20 |
| Remote-Inbetriebnahme CCTV | CT-IBR-IP- | 3690 | 148,20 |
| Inbetriebnahme CCTV-Analog | CT-INB-ANA | 3690 | 297,50 |
| Inbetriebnahme Technikerstunde | CT-INBETR- | 3690 | 148,20 |
| Inbetriebnahme CCTV IP-System | CT-INB-IP- | 3690 | 314,30 |

### DSGVO-Hinweis (S. 45)

- **Vor Installation** ist eine **Abklärung mit der Datenschutz-Grundverordnung (DSGVO)** notwendig.
- Weitere Informationen: https://www.dsb.gv.at/recht-entscheidungen/gesetze-in-oesterreich.html (Stand 6.4.2022).

### Preise und Lieferbedingungen (S. 45)

- Angegebene Preise sind **unverbindliche Schrack-Technik-Preisempfehlungen (UVP) in EUR exkl. MWSt.**, gültig ab sofort; ersetzen alle bisherigen Preisangaben für die enthaltenen Bestellnummern.
- **PREG** = Angabe der dem Artikel zugeordneten **Preisgruppe**.
- Alle UVP- und PREG-Angaben gelten bis auf Widerruf bzw. bis Erscheinen eines Folgekatalogs/einer neuen Preisliste; Änderungen vorbehalten.
- Preise können sich aufgrund der Weltmarktsituation dynamisch ändern; tagesaktuelle Preise auf www.schrack.at oder per Datanorm-Datei-Download im Bereich „Mein Konto".
- Es gelten ausschließlich die **Allgemeinen Lieferbedingungen des Fachverbandes der Elektro- und Elektronikindustrie Österreichs** (www.feei.at).
- Irrtümer, Satzfehler und Änderungen der Produktpalette vorbehalten.

### Schrack Store / Digital Tools / Online-Shop (S. 45-47, Werbeinhalt knapp)

- **SCHRACK STORE** in allen Geschäftsstellen; duales System (lokale + zentrale Verfügbarkeit): Versandzustellung oder Storeabholung.
  - Regionale Verfügbarkeit von **mehr als 3.000 Artikeln** für Sofortabholung; begehbarer Katalog.
- Digital Tools: mobile Webseite mit Scanfunktion, elektronische Schnittstellen, **Schrack Design** (Tool für Verteilerplanung).
- Online-Shop-Sortiment: Energietechnik, Industrieanwendungen, Gebäudetechnik, Notbeleuchtung, Netzwerktechnik, Beleuchtung, alternative Energie.
- **Bestellannahmezeit bis 18:00 Uhr**, Next Day Delivery. Slogan: „Get Ready. Get Schrack".

### Standorte / Niederlassungen (S. 48)

- **Zentrale:** SCHRACK TECHNIK GMBH, Seybelgasse 13, 1230 Wien · Tel. +43(0)1/866 85-5900 · Fax +43(0)1/866 85-98800 · info@schrack.at.
- **SCHRACK TECHNIK ENERGIE GMBH:** Seybelgasse 13, 1230 Wien · Tel. +43(0)1/866 85-5058 · energie@schrack.com.
- **Österreichische Niederlassungen:**
  - Kärnten: Ledererstraße 3, 9020 Klagenfurt · +43(0)463/333 40-0 · klagenfurt@schrack.com.
  - Oberösterreich: Franzosenhausweg 51b, 4030 Linz · +43(0)732/376 699-0 · linz@schrack.com.
  - Salzburg: Bachstraße 59-61, 5023 Salzburg · +43(0)662/650 640-0 · salzburg@schrack.com.
  - Steiermark/Burgenland: Kärntnerstraße 341, 8054 Graz · +43(0)316/283 434-0 · graz@schrack.com.
  - Tirol: Richard-Berger-Straße 12, 6020 Innsbruck · +43(0)512/392 580-5300 · innsbruck@schrack.com.
  - Vorarlberg: Wallenmahd 23, 6850 Dornbirn · +43(0)5572/238 33-0 · dornbirn@schrack.com.
  - Wien/Niederösterreich/Burgenland: Seybelgasse 13, 1230 Wien · +43(0)1/866 85-5700 · wien@schrack.com.
- **Tochtergesellschaften (Auswahl):** Belgien (St-Denijs-Westrem), Bosnien-Herzegowina (Mostar), Bulgarien (Sofia), Deutschland (München), Kroatien (Zagreb), Polen (Warschau), Rumänien (Bukarest), Serbien (Belgrad), Slowakei (Bratislava), Slowenien (Slovenj Gradec), Tschechien (Prag), Ungarn (Budapest).

### Einordnungs-Hinweis für die Wissensbasis

- Dieses Dokument enthält **keine ÖNorm-/OVE-Normwerte** (keine E 8101, EN 1838 o.ä.). Es ist ein CCTV-Hersteller-Katalog; einziger normativ/rechtlich relevanter Hinweis ist die **DSGVO-Abklärungspflicht vor Installation**.
- Wert für die Wissensbasis: Komponenten- und Bestellnummern-Referenz für Video-Überwachungsanlagen (IP-/AHD-Kameras, NVR/XVR, PoE-Zubehör, Koax/Netzwerkkabel) sowie Schrack-Service-Positionen.
