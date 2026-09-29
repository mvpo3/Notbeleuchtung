# Frühere Seitenkorrekturen – weiterhin enthalten

Diese Fassung übernimmt die handschriftlichen Markierungen und Texthinweise aus `Leopold_Kohr_Schule_EG_Lernbuch_final(1).pdf`.
Das Lernbuch hat jetzt **39 Seiten**, **29 Originalbeispiele** und **120 beschriftete Pfeile**. Die zusätzliche Lift-Seite ist Seite 23. Ab dort verschieben sich die bisherigen Seitenzahlen um eins.

| Bisherige Seite | Neue Seite | Änderung |
|---|---|---|
| 5 | 5 | Außen- und Innenwandkanten direkt nachgezeichnet; Türöffnung und Raumstempel getrennt und präzise markiert. |
| 6 | 6 | Je zwei Wandkanten markiert; Stützenpfeil auf die tatsächliche schraffierte Stütze gesetzt; Deckenrand nachgezogen. |
| 8 | 8 | Massives Küchenwandstück, Türöffnung, gesamte Außenwand und Tischgruppe räumlich eindeutig markiert. |
| 9 | 9 | Schräge Wandkanten ergänzt; die markierten Möbel und länglichen Einbauten separat umrandet. |
| 10 | 10 | Sauberer Originalausschnitt; Kern und Dämmlage als Flächen umrandet; innere Kante und Türöffnung direkt verfolgt; unbelegte Tragfunktion entfernt. |
| 18 | 18 | Möbel und Sessel weiß ausgespart; Wandpfeil von einem Möbel auf die tatsächliche schraffierte Wand versetzt. |
| 21 | 21 | Stark vergrößerter Ausschnitt; Techniktext, Wandmaterial und Einbau getrennt markiert; genaue Durchbruchkontur ausdrücklich ungeklärt. |
| 22 | 22 | Lift, Treppe und Vorbereich gemeinsam dargestellt; Lift vollständig aus grüner Fläche ausgespart. |
| neu | 23 | Gewünschte zusätzliche Lift-Seite mit Kabine, Schiebetürlinien, Schachtwand, Technikabstand, Beschriftung und Vorbereich. |
| 31 | 32 | Außenwand-Nahaufnahme erhalten; in Revision 4 zusätzlich mit geschlossenen Rahmen versehen. |
| 35 | 36 | Alle sechs markierten Möbel-/Waschbeckenstellen weiß ausgespart; auch Gesamtplan und andere betroffene Ausschnitte aktualisiert. |

## Grüne Flächen

Die Möbelaufbereitung berücksichtigt jetzt auch Kurven aus den CAD-Layern für Möblierung, Küche und Sanitäreinrichtung. Offene Symbole aus den Nutzerkorrekturen erhalten zusätzlich nachvollziehbare äußere Lernumrisse. Die markierten Möbel und Waschbecken sind weiß; ihre schwarzen Originalkonturen bleiben sichtbar. Der gesamte Liftbereich ist aus der allgemeinen Gehfläche ausgespart. Eine betretbare Kabine wird als eigene Verbindung und nicht als normaler Gang modelliert.

Die ergänzten Umrisse sind Lerninterpretationen. Sie liefern keine geprüften Körperabstände oder lichten Durchgangsbreiten. Die technischen Grenzen der vorigen Fassung gelten weiter; insbesondere bleiben die Geschossanschlüsse der Treppen offen.

## Dateien für Claude Code

- `daten/04_BEISPIELE_EG.json`: überarbeitete Texte, Bildpfade und Suchbereiche; neu EG-29.
- `daten/13_BILDANNOTATIONEN_EG.json`: aktuelle Pfeilziele und direkt nachgezogene Merkmale.
- `daten/12_GEHFLaECHEN_EG.geojson`: aktualisierte grüne Lernflächen.
- `daten/15_MOEBEL_KORREKTUREN_EG.geojson`: ergänzte, manuell zugeordnete Möbelumrisse.
- `daten/15a_EINBAUKONTUREN_EG.geojson`: aus CAD-Linien und Kurven abgeleitete Einbaukonturen in PDF-Punkten.
- `daten/16_NUTZERKORREKTUREN_EG.json`: Zuordnung der Nutzerhinweise und Seitenwechsel.

`skripte/baue_lernbuch.py` setzt die aktuelle PDF aus den enthaltenen Bildern und JSON-Daten erneut. `herstellung_dokumentation.py` dokumentiert die frühere Revision und ist kein Generator für die jetzige Fassung. Der Paketprüfer überprüft Dateien und Bezüge; er führt keine Raumerkennung aus.
