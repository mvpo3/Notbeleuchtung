# Scharfer Vektorexport – Revision 5

Die vorige Lernbuch-PDF enthielt 35 gerasterte Planabbildungen. Beim starken Vergrößern wurden deren Pixel sichtbar. Die ursprünglichen Plan-PDFs besitzen dagegen Vektorgeometrie.

Die aktuelle Fassung übernimmt die Originalpläne und die 29 erklärten Ausschnitte direkt als Vektoren. Auch Beschriftungen, Pfeile, Rechteckrahmen und farbige Bogenmarkierungen sind Vektorelemente. Die 39-seitige PDF enthält keine eingebetteten Rasterbilder. Alle 120 Beschriftungen, 38 Erklärrahmen und elf zusätzlichen Bogenmarkierungen sind erhalten.

`plaene/EG_Erklaerte_Details_Vektor.pdf` enthält die 29 erklärten Ausschnitte in derselben Reihenfolge wie `daten/04_BEISPIELE_EG.json`. Die Gesamtpläne und die vier grünen Bereichsausschnitte werden ebenfalls direkt aus den Vektorquellen gesetzt. Die PNG-Dateien bleiben als Vorschauen für Markdown und andere Programme enthalten; die PDF verwendet sie nicht mehr.

## Erneut erzeugen

```bash
python3 skripte/erzeuge_markierte_details.py --vector
python3 skripte/baue_lernbuch.py
```

Die neue PDF liegt danach unter `_neu_erstellt/Leopold_Kohr_Schule_EG_Lernbuch_final.pdf`. Der erste Befehl erneuert die Vektordetails; der zweite setzt das Lernbuch. Die vorhandenen PNG-Vorschauen können bei Bedarf separat erneuert werden.

Die Schärfe wurde anhand der gerenderten Seiten und eines Detailvergleichs bei zwölfmaliger Skalierung geprüft. Vektoren vermeiden die feste Pixelauflösung. Wie klein ein Detail auf dem Bildschirm erscheint, hängt weiterhin von der Zoomstufe ab.
