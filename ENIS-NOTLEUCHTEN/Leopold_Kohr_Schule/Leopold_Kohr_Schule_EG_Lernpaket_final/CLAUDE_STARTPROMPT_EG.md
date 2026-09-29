# Startauftrag für Claude Code – EG vollständig einlesen und umsetzen

Arbeite mit dem entpackten Ordner dieses EG-Lernpakets und dem vorhandenen Rivoplan-Repository. Ziel ist, das Wissen über Mauern, Türen, Fenster, freie Verbindungen und Treppen in die bestehende Raumerkennung zu übertragen und die Wirkung am Original-EG nachzuweisen.

## 1. Paket verstehen

Lies zuerst `00_START_HIER.md`, `02_CLAUDE_AUFTRAG_EG.md`, `11_DATENVERTRAG_EG.md` und `18_UMSETZUNG_UND_UEBERGABE_EG.md`. Prüfe das Paket mit `python3 skripte/pruefe_paket.py` aus dem Paketordner. Berücksichtige die Abhängigkeiten aus `skripte/requirements.txt` in einer geeigneten bestehenden oder separaten Python-Umgebung.

Lies danach das vollständige Lernwissen, die Regeln, alle 29 Beispiele und die 20 Prüffallspezifikationen. Betrachte die 39-seitige `Leopold_Kohr_Schule_EG_Lernbuch_final.pdf` einschließlich der farbigen Rahmen, Pfeile und Bogenmarkierungen. Vergleiche Aussagen mit den Originalquellen. Nutze bei Bedarf gezielt gerenderte PDF-Ausschnitte; bloße Textextraktion zeigt die farbigen Erklärungen nicht. Die PDF ist die scharfe Vektorfassung. Die PNGs sind zusätzliche Vorschauen.

Beachte: Rote Konturen, grüne Bodenflächen, Pfeile und Rechteckrahmen sind Lernhilfen. Leite die tatsächliche Bauteilgeometrie aus der Original-DXF ab. Rechteckige Suchbereiche dürfen keine neuen Mauern oder Räume erzeugen. Lies nahe Beschriftungen mit, bevor du eine Linie klassifizierst. Bauteilname, Geometrie und räumlicher Zusammenhang müssen zusammenpassen. Unklare Höhen und Anschlüsse bleiben offen.

## 2. Bestehende Software untersuchen

Ermittle den echten Repository-Pfad, aktuellen Commit, Arbeitsstand, Projektanweisungen, Startbefehl, Konfiguration und relevante Tests. Suche die vorhandenen Schritte für Import, Wände, Türen/Fenster, Räume, Verbindungen und Treppen. Benenne die tatsächlichen Dateien und Funktionen. Erfinde keine Schnittstellen. Erhalte vorhandene Teamänderungen und arbeite in einem getrennten Branch oder Worktree, wenn dies für parallele Arbeit nötig ist.

Wenn das Repository oder eine notwendige Laufvoraussetzung fehlt, benenne genau, was fehlt. Erfinde keinen Engine-Lauf und keine Testergebnisse. Erledige die mit dem vorhandenen Material mögliche Zuordnung trotzdem.

## 3. Umsetzen und nachweisen

Führe mit der enthaltenen Original-EG-DXF einen reproduzierbaren Ausgangslauf aus. Sichere Codeversion, Konfiguration, Protokoll, Zwischendaten und Ergebnisoverlay.

Ordne die beobachteten Fehler den Regeln, Originalbeispielen und Prüffällen zu. Beginne beim ersten belegten Fehler in der Verarbeitungskette. Überführe den zugehörigen Prüffall und einen passenden Gegenfall in die vorhandene Teststruktur. Ändere die belegte Ursache und prüfe den Fehlerfall, den Gegenfall und relevante bestehende Regressionen. Verwende keine Sonderregel, die lediglich die Koordinaten dieses einen Gebäudes auswendig abbildet.

Bleibe nicht bei einer Zusammenfassung der Unterlagen stehen. Gehe nach dem Einlesen und der Diagnose zur nachvollziehbaren Umsetzung über, soweit der vorhandene Code und die Belege dies erlauben. Vergleiche anschließend denselben Eingabeplan mit derselben Konfiguration vor und nach der Änderung. Entscheide über weitere Änderungen anhand dieses Vergleichs.

## 4. Ergebnis übergeben

Lege in einem eigenen Ergebnisordner ab: Startanweisung, Codeänderungen oder Diff, Zuordnung von Regel zu Code, Vorher-/Nachher-Daten, beschriftete Overlays, tatsächlich ausgeführte Tests und offene Punkte. Berichte, welche Fehler behoben wurden, welche bestehen bleiben und wodurch dies belegt ist. Speichere einen Fortsetzungsstand für die nächste Sitzung.

Dieser Auftrag betrifft die Raumerkennung im EG der Leopold-Kohr-Schule. Halte die Arbeit an UG und anderen Geschossen getrennt. Die Notleuchtenplatzierung und Normregeln sind ein späterer Arbeitsstrang. Die genaue fachliche Aufgabe und die Behandlung der Treppenübergaben stehen in `02_CLAUDE_AUFTRAG_EG.md`.
