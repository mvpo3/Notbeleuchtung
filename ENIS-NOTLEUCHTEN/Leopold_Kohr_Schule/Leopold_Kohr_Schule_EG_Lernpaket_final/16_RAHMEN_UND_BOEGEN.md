# Deine Rahmen- und Bogenkorrektur – Revision 4

Grundlage ist die erneut kommentierte Datei `Leopold_Kohr_Schule_EG_Lernbuch_verbessert(1).pdf` sowie dein Auftrag, die einmal gezeigte Korrektur auf alle vergleichbaren Wand-Erklärungen zu übertragen. Gleiche Original-DXF und Original-PDF; 39 Seiten bleiben erhalten.

- Jedes erläuterte Wandstück ist zusätzlich zum Pfeil mit einem geschlossenen, farblich zugeordneten Rechteck eingerahmt. Bei schrägen Wänden ist der Rahmen gedreht. Innenkante, Außenkante und Materialband können denselben Rahmen verwenden, wenn sie denselben Wandabschnitt beschreiben.
- 38 geschlossene Erklärrahmen insgesamt: Wandkörper, Wandschichten, Stütze, feste Abschlüsse und die korrigierte Tischreihe. Schraffuren bleiben sichtbar.
- 11 zusätzlich farbig nachgezogene Originalbögen an Türen und Fenstern. Bestehende Markierungen bleiben erhalten.
- 21 Originaldetails neu gerendert; die Texte und Daten für Claude Code sind synchronisiert.

| Hinweis in deiner Datei | Umsetzung |
|---|---|
| Seite 7: Innenwand mit Strichen besser markieren | Blauer geschlossener Rahmen um das schraffierte Innenwandstück. Pfeilziel liegt im festen Material. |
| Seite 8: alte Tischmarkierung durchgestrichen, höheres Rechteck | Orange umrandet die vollständige von dir bezeichnete Tischreihe. |
| Seite 11: Bogen markieren | Der echte Viertelkreis des WC-Türblatts ist orange nachgezogen. Beide erklärten dünnen Wandstücke sind eingerahmt. |
| Seite 13: Bögen farbig markieren | Beide Schwenkbögen der zweiflügeligen Tür sind orange nachgezogen. |
| Seite 15: Wand als Rechteck statt nur Pfeil | Roter Rahmen entspricht dem von dir eingezeichneten Fassadenabschnitt. Beide Fensterbögen sind orange. |
| Übertragung auf weitere Wand-Erklärungen | Alle vergleichbaren Pfeile haben zugeordnete geschlossene Rahmen, auch bei Außenwand, Innenwand, schräger Wand, dünner Trennwand, Schachtwand und Wanddetail. |

Die Rahmendaten und Bögen stehen in `daten/13_BILDANNOTATIONEN_EG.json`, die Zuordnung deiner Hinweise in `daten/17_RAHMEN_UND_BOEGEN_KORREKTUR_EG.json`. `skripte/erzeuge_markierte_details.py` zeichnet die überarbeiteten Details aus den gespeicherten Koordinaten. Rechteckrahmen sind Lernmarkierungen und keine bauteilgenauen Masken. Keine Raumerkennungs-Engine wurde ausgeführt.
