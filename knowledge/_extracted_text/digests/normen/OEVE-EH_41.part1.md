# OEVE-EH_41 — Teil 1
> Quelle: OEVE-EH_41 (normen) · Seiten 41-61.

ÖVE-EH 41 (Ausgabe 1987) ist die österreichische Bestimmung für **Erdungen in Wechselstromanlagen mit Nennspannungen über 1 kV** (Hochspannungs-Erdungen). Dieser Teil deckt die §§ 18–25 (Freileitungsmaste, Mastschalter/Maststationen, ortsveränderliche Umspannstellen, Zusammenschluss von Erdungen, Blitzschutz-Erfordernisse, Überwachung) sowie die Anhänge 1–3 (Blitzschutz §124, Überwachung/Messung von Erdungsanlagen §§125–130, Berechnungsbeispiel §131) und das Sachverzeichnis ab. Hinweis: Das Dokument ist OCR-erfasst, viele Formelzeichen/Werte sind verstümmelt — Plausibilisierung bei Verwendung nötig.

## Inhalt

### § 18/§ 19 — Freileitungsmaste: Allgemeines & Erdung
- Masten aus Stahl, anderem leitfähigem Material oder Stahlbeton sind durch ihren **Mastfuß geerdet**.
- Masten aus Holz oder anderem nicht-leitfähigem Material **ohne metallene Überbrückung** zwischen Isolatorträgern und Erde: **Schutzerdung nicht erforderlich**.
- Bei Leitungen mit durchlaufendem Erdseil gilt als Erdungsimpedanz für die Schutzerdung der Wert bei aufgelegtem Erdseil.
- Erdungsleitungen an Masten sind thermisch nur für den über sie fließenden Anteil des Erdfehlerstroms zu bemessen (gemäß Abb. 5-1); die **Mindestquerschnitte gemäß § 14** sind einzuhalten.

### § 19.2 — Netze mit isoliertem Sternpunkt oder Erdschlusskompensation
- Am Mast darf die **Berührungsspannung 65 V nicht überschreiten** (OCR „85V" ist als 65 V zu lesen, vgl. § 20.2).
- Forderung gilt als erfüllt, wenn die Erdungsimpedanz Z_E den Wert **125 V / I_E** nicht überschreitet; dabei ist I_E der Erdungsstrom im Sinne des § 9.3.
- Ermittlung des Erdungsstromes: **I_E = r · I_E'** (Reduktionsfaktor r).
- Bei Freileitungen **ohne Erdseil ist der Reduktionsfaktor r = 1**.
- Reduktionsfaktoren für Freileitungen mit Erdseil: aus einschlägigen technischen Bestimmungen.
- Erdfehlerstrom I_E' (§ 9.2): in Netzen mit isoliertem Sternpunkt der **kapazitive Erdschlussstrom I_C**, in Netzen mit Erdschlusskompensation der **Erdschlussreststrom**.

#### § 19.2.2 — Ersatzmaßnahmen statt § 19.2.1
Anstelle der Einhaltung von § 19.2.1 können Maßnahmen treten, die einen Erdschluss am Mast unwahrscheinlich machen oder seine Dauer kurz halten:
- (1) Verwendung von **Langstab- oder Vollkernisolatoren**, oder
- (2) Verwendung von Isolatoren, deren innerer Isolationszustand von außen erkennbar ist (z. B. **Kappenisolatoren aus vorgespanntem Glas**) und Überwachung der Isolatoren im Betrieb in **Abständen von etwa einem Jahr**, oder
- (3) Einbau von **Erdschluss-Sucheinrichtungen**, umgehende Suche und Abschaltung erdschlussbehafteter Leitungen.
- **Bei Masten in Freibädern oder auf Campingplätzen** darf Maßnahme (3) **nicht** angewendet werden. Maßnahme (2) nur, wenn die Leitung **kein Erdseil** besitzt und an den betreffenden Masten **Isolatorenketten aus vorgespanntem Glas** verwendet werden, deren **Isoliervermögen um etwa 50 % erhöht** ist und die mit **Lichtbogenschutzarmaturen** ausgerüstet sind. Maßnahme (1) ist zulässig, wenn die Isolatorenketten mit Lichtbogenschutzarmaturen ausgestattet sind.

### § 19.3 — Netze mit niederohmiger Sternpunkterdung
- Leitungen, deren Maste überwiegend aus Stahl/leitfähigem Material bestehen, müssen ein **durchlaufendes Erdseil** haben, das mit der Stationserdungsanlage verbunden werden muss. Das Erdseil darf (z. B. bei Leitungskreuzungen) auch durch ein **Bodenseil** ersetzt werden.
- Erdungsstrom (Abb. 5-1): **I_E = w · r · I_E'**.
- Erwartungsfaktor **w = 1** für Netze mit Nennspannungen **unter 110 kV**; für Netze **≥ 110 kV** darf **w = 0,7** eingesetzt werden. Kleinere Werte sind ggf. nachzuweisen.
- Reduktionsfaktoren r für Freileitungen aus einschlägigen technischen Bestimmungen.
- Als Erdfehlerstrom I_E' ist der **Anfangs-Kurzschlusswechselstrom I_k''** einzusetzen.
- **§ 19.3.3**: Bei Masten (außer § 19.3.4) sind **keine Grenzwerte** der Berührungs- und Erdungsspannung einzuhalten, wenn eine **automatische Schnellausschaltung** des Erdfehlerstroms eingeleitet wird. Andernfalls sind beim Fließen des Erdungsstroms nach § 19.3.2 die **Berührungsspannungen nach Abb. 18-1** einzuhalten.
- **§ 19.3.4** (Freibäder/Campingplätze): Berührungsspannung am Mast und die Spannung zwischen zwei beliebigen, **1,5 m voneinander entfernten Punkten** der Mastumgebung dürfen die Werte nach Abb. 18-1 nicht überschreiten, wenn der Erdungsstrom nach § 19.3.2 fließt. Maßnahmen: **Schotter- oder Asphaltschichten nach § 8.8** oder Potentialsteuerung. Alternativ darf der gefährdete Bereich durch einen **Zaun** abgegrenzt werden.

### § 19.4 — Netze mit vorübergehend niederohmiger Sternpunkterdung
- Die Erdung von Freileitungsmasten ist **nach § 19.2** zu bemessen.

### § 20 — Mastschalter, Maststationen und Kabelendmaste
- **§ 20.1 (Mastschalter auf Holzmasten):** Gerüstteile brauchen nicht geerdet zu werden. In die Betätigungsgestänge müssen dann **außerhalb des Handbereiches mechanisch zuverlässige Isolatoren** eingebaut werden, die für die Nennisolation des Schalters bemessen sind. Der vom Erdboden aus berührbare Teil des Antriebes ist zur Ableitung von Kriechströmen zu erden — dafür genügt ein **Vertikalerder von mindestens 1 m Länge** oder ein **Horizontalerder um den Mast in etwa 1 m Abstand**. Für Erder und Erdungsleitung genügen die Mindestquerschnitte nach § 13 bzw. § 14.
- **§ 20.2 (Mastschalter auf Stahl-/Stahlbetonmasten):** So zu erden, dass die **Berührungsspannung bei Erdschluss 65 V nicht überschreitet**. Gilt als erfüllt, wenn um den Mast ein **Horizontalerder in etwa 1 m Abstand und in höchstens 0,5 m Tiefe (Steuererder)** verlegt ist und die **Erdungsspannung 250 V nicht überschreitet**. Erder und Erdungsleitung nach § 13 bzw. § 14.
- **§ 20.3:** Mastschalter auf Holzmasten mit geerdeten Isolatorträgern am Schaltermast → nach § 20.2 verfahren. Wird die Erdungsleitung der Mastschaltererdung bis in eine **Entfernung von mindestens 20 m isoliert verlegt** (Kabel oder Erdung an einem Nachbarmast), ist das Betätigungsgestänge am Schaltermast nach § 20.1 zu behandeln; Erdungs- und Berührungsspannung an der Mastschaltererdung sind dann **nicht begrenzt**. Erder/Erdungsleitung nach § 13 bzw. § 14.
- **§ 20.4 (Maststationen-Traggerüste):** Unter Beachtung von § 13/§ 14 eine der Maßnahmen:
  - (1) **Horizontalerder** um den Mast in etwa **1 m Abstand** und bis höchstens **0,5 m Tiefe**, mit der Erdung des Traggerüsts verbunden. Vorhandene metallene Schaltkästen im Bereich des Horizontalerders sind ebenfalls mit dem Erder zu verbinden. Bemessung so, dass **Berührungsspannung bei Erdschluss ≤ 65 V**; gilt als erfüllt, wenn **Erdungsspannung ≤ 250 V**. (Hinweis: Ein Fehlerstromkreis über die Erdung des Traggerüstes und die Niederspannungs-Betriebserde wird i. A. von der Transformator-Niederspannungssicherung nicht unterbrochen.)
  - (2) Erdungsleitung des Traggerüsts gemäß § 20.3 bis in **≥ 20 m isoliert** verlegt. Metallene Schaltkästen mit der **Niederspannungs-Betriebserdung** verbinden. Unter dem Schaltkasten ein damit verbundener **Horizontalerder in etwa 1 m Abstand und höchstens 0,5 m Tiefe**.
- **§ 20.5 (Kabelendmaste):** Kabelmäntel und metallene Endverschlussgehäuse auf Holz-, Stahl- oder Stahlbetonmasten sind nach § 14 und § 15 am Mast zu erden. **Ausgenommen** sind metallene Endverschlüsse von Kunststoffkabeln mit konzentrischem Leiter/Schirm und nicht leitendem Kunststoffmantel, **wenn der konzentrische Leiter/Schirm wenigstens an einer anderen Stelle geerdet** ist.

### § 21 — Ortsveränderliche Umspannstellen
- **Schutz gegen zufälliges Abgreifen der Berührungsspannung** muss durch geeignete Absperrung sichergestellt sein; für Bedienungsstandorte ist die **Standortisolierung** anzuwenden, oder die Bedingungen des § 15 sind einzuhalten.
- Für die angeschlossenen Anlagen bis 1000 V gilt § 23.
- **§ 21.2 (Baustromversorgung):** Bei Baustromversorgung aus ortsveränderlichen/provisorischen Umspannstellen ist die **Hochspannungserdung vom niederspannungsseitigen Schutzleiter zu trennen**, wenn die **Erdungsspannung bei hochspannungsseitigem Erdschluss 125 V überschreitet**.

### § 22 — Vorrichtungen zum Erden und Kurzschließen an Ausschaltstellen
- **§ 22.1:** Fest eingebaute Erdungs- und Kurzschließvorrichtungen müssen den am Einbauort auftretenden Kurzschlussbeanspruchungen gewachsen sein. Für Anschlussstellen, Erdungsschalter und transportable Erdungs-/Kurzschließvorrichtungen wird auf einschlägige technische Bestimmungen verwiesen.
- **§ 22.2:** Vorübergehende Erdungen an Arbeits- und Ausschaltstellen müssen durch Anschluss an **geerdete Teile** (z. B. Metallmaste) erfolgen. Ist das nicht möglich, ist eine Erdung zu verlegen, die mindestens **einem Vertikalerder mit 1 m Länge** gleichwertig ist.

### § 23 — Zusammenschluss von Erdungen (>1 kV mit ≤1000 V)
- **§ 23.1 (NS-Versorgung innerhalb einer HS-Erdungsanlage):** Werden von einer Hochspannungsanlage nur Niederspannungsverbraucher versorgt, die **innerhalb** einer Hochspannungs-Erdungsanlage/-Station liegen, sind **alle Schutz- und Betriebserdungen an eine gemeinsame Erdungsanlage** anzuschließen.
- **§ 23.2 (NS-Versorgung außerhalb einer HS-Erdungsanlage):** Anschluss aller Schutz-/Betriebserdungen an eine gemeinsame Erdungsanlage wird empfohlen, wenn:
  - (1) die Bedingungen gemäß **Tab. 23-1** erfüllt sind, oder nachgewiesen wird, dass die Berührungsspannung gemäß Abb. 18-1 eingehalten ist. Bei mehreren Spannungsebenen auf gemeinsamer Erdungsanlage ist der **ungünstigste Fall** zugrunde zu legen.
  - (2) Ist die Erdungsanlage eines TN-Netzes mit der entfernten Erdungsanlage einer übergeordneten Spannungsebene leitend verbunden, darf die **Erdungsspannung U_E der übergeordneten Anlage 125 V** nicht überschreiten (in Netzen mit isoliertem Sternpunkt oder Erdschlusskompensation) bzw. **nicht das Zweifache** der Berührungsspannungs-Werte gemäß Abb. 18-1 (in Netzen mit niederohmiger Sternpunkterdung).
- **§ 23.2.2:** Hochspannungs- und Niederspannungs-Erdungsanlage **müssen getrennt** werden, wenn die Bedingungen gemäß Tab. 23-1 nicht erfüllt sind und nicht nachweisbar ist, dass die Berührungsspannung gemäß Abb. 18-1 eingehalten wird. **Der Abstand der getrennten Erder darf 10 m nicht unterschreiten** (Abb. 23-1, Abb. 23-2). Zwischen die getrennten Erder darf aus Blitzschutzgründen ein **Überspannungsableiter** geschaltet werden.
- Abbildungen: **Abb. 23-1** = getrennte Erdungsanlage mit Freileitungsanschluss; **Abb. 23-2** = getrennte Erdungsanlage mit Kabelanschluss.
- Die Körper der elektrischen Betriebsmittel der Niederspannungsanlage, die sich **innerhalb der Hochspannungsanlage** befinden, sind über Schutzleiter an die **Hochspannungs-Erdungsanlage** anzuschließen.

#### Tab. 23-1 (Hinweis)
Tabelle stark OCR-verstümmelt. Erkennbare Inhalte: Unterscheidung nach Sternpunktbehandlung — Netze mit **isoliertem Sternpunkt** bzw. **Erdschlusskompensation** mit Bedingung **U_E ≤ 125 V** (vgl. § 23.2(2)), gegenüber Netzen mit **niederohmiger Sternpunkterdung** (Bezug auf Berührungsspannung Abb. 18-1). Verweise auf § 19.2.2(2)/(3), § 16.x. Exakte Tabellenwerte aus Original-Norm zu verifizieren.

### § 24 — Berücksichtigung der Erfordernisse des Blitzschutzes
- Die Berücksichtigung des Blitzschutzes erfolgt **nicht aus sicherheitstechnischen, sondern aus betriebstechnischen Erwägungen** (vgl. Anhang 1).

### § 25 — Überwachung von Erdungsanlagen
- Erdungsanlagen sind zur Feststellung allfälliger **Korrosionsschäden periodisch an kritischen Stellen** zu kontrollieren.

### Anhang 1 / § 124 — Berücksichtigung der Erfordernisse des Blitzschutzes
- **§ 124.1:** Bei Blitzeinschlägen in geerdete Teile elektrischer Anlagen (Erdseile, Stahlbetonmaste, Holzmaste mit herabgeführter Erdungsleitung, Gerüste von Freiluftanlagen) kann es zwischen geerdeten Anlagenteilen und betriebsmäßig spannungführenden Teilen zum Überschlag kommen (**rückwärtiger Überschlag**).
- Rückwärtige Überschläge sind i. A. nicht zu erwarten, wenn der **Stoß-Erdungswiderstand R_st** der Beziehung **R_st ≤ U_s / I** genügt. Dabei: **R_st** = Stoß-Erdungswiderstand der Mast-/Gerüsterdung, **U_s** = Stehstoßspannung der Isolierung, **I** = Scheitelwert des Blitzstromes im Mast bzw. Gerüst.
- **§ 124.1.1 / Tab. 124-1:** Anhaltswerte über die Häufigkeit von Blitzströmen in Masten von Freileitungen mit Erdseil — gibt an, mit welcher Summenhäufigkeit Blitzströme bis zu einer bestimmten Stromstärke (Blitzstrom I im Mast) auftreten. Konkrete Wertepaare im OCR unleserlich (Summenhäufigkeit in %, abnehmend mit steigender Stromstärke).
- **§ 124.1.2:** Ob Maßnahmen zur Verringerung der Wahrscheinlichkeit rückwärtiger Überschläge getroffen werden, hängt **nur von betriebstechnischen Erwägungen** ab. In Freiluftanlagen ist der Stoß-Erdungswiderstand i. A. so niedrig, dass rückwärtige Überschläge nicht zu erwarten sind.
- **§ 124.2:** Der Stoß-Erdungswiderstand weicht mehr oder weniger von der Erdungsimpedanz Z_E ab. Bei Erdungsanlagen geringer räumlicher Ausdehnung (z. B. Mastfüße, **Vertikalerder bis etwa 10 m Länge**, Plattenerder, Strahlenerder mit Einzelstrahlen, die **20 m nicht wesentlich überschreiten**) kann er näherungsweise gleich dem **Ausbreitungswiderstand** (bei abgehobenen Erdseilen) gesetzt werden.
- **§ 124.3:** Bei Herstellung von Masterdungsanlagen wird empfohlen, statt eines sehr langen Vertikal-/Horizontalerders **mehrere weniger lange Erder** in der Umgebung des Mastes anzuordnen.
- **§ 124.4:** Erdseile von Freileitungen sollen möglichst über den Leiterseilen bis zur Anlage weitergeführt und mit deren Erdungsanlage verbunden werden.
- **§ 124.5:** Erdseile bei Freileitungen mit Holzmasten sollen nach Möglichkeit an **jedem Mast**, mindestens jedoch in **Abständen von 300 m** geerdet sein (ausgenommen Weitspannfelder).
- **§ 124.6:** Ableitungen vorhandener Blitzschutzanlagen sind auf **kürzestem Wege** mit der Hochspannungs-Erdungsanlage zu verbinden. Im Hinblick auf Berührungsspannung bei Erdschluss ist **§ 15.2.1** zu beachten.

### Anhang 2 — Überwachung und Messung von Erdungsanlagen (§§ 125–130)

#### § 125 — Allgemeines zur Nachprüfung/Überwachung
- **§ 125.1:** Bei ausgedehnten Erdungsanlagen empfiehlt sich ein **Lageplan**.
- **§ 125.2:** Für die periodische Überprüfung von Erdungsanlagen wird ein Zeitraum von **etwa 5 Jahren** empfohlen. Für große Anlagen (z. B. Umspannwerke) sowie Masterdungen genügt ein Zeitraum von etwa **10 Jahren**.

#### § 126 — Messung von spezifischen Erdwiderständen
- Messungen des spezifischen Erdwiderstandes zur Vorausbestimmung des Ausbreitungswiderstandes/der Erdungsimpedanz sind nach einem **Viersondenverfahren (z. B. Wenner-Verfahren)** durchzuführen; der spezifische Erdwiderstand wird für verschiedene Tiefen mit geoelektrischen Messverfahren ermittelt.

#### § 127 — Messung von Ausbreitungswiderständen und Erdungsimpedanzen
- **§ 127.1:** Messverfahren hängt von Ausdehnung der Anlage und Grad der Beeinflussung (§ 130) ab. Warnung: Bei Messungen können auch im abgeschalteten Zustand, insbesondere während der Messung, an und zwischen geerdeten Teilen (z. B. zwischen Kästen und abgehobenem Erdseil) **Berührungsspannungen auftreten**.
- **§ 127.2.1 — Erdungsmessbrücke:** Eingesetzt bei Erdern/Erdungsanlagen kleinerer oder mittlerer Ausdehnung (z. B. Staberder, Banderder, Freileitungsmasterder bei abgehobenem Erdseil, Hochspannungserdungen von Ortsnetzstationen in Freileitungsnetzen bei Trennung von der NS-Erdung). **Frequenz der verwendeten Wechselspannung soll 150 Hz nicht überschreiten.** Zu prüfender Erder, Sonde und Hilfserder sollen möglichst auf einer Geraden liegen.
  - Abstand der **Sonde** vom zu prüfenden Erder: **mindestens das 2-Fache der größten Erderausdehnung** (in Maßrichtung), jedoch **nicht weniger als 20 m**.
  - Abstand des **Hilfserders**: **mindestens das 4-Fache** (ebenfalls Mindestwert; konkreter Meterwert im OCR abgeschnitten — laut Norm typ. ≥ 40 m).
- **§ 127.2.2 — Strom- und Spannungsmessung (Abb. 127-1):** Insbesondere zur Messung der Erdungsimpedanz **großer Erdungsanlagen**. Durch Anlegen einer Wechselspannung etwa von Netzfrequenz zwischen Erdungsanlage und Gegenerder wird ein Versuchsstrom I eingeleitet, der zu messbarer Potentialanhebung führt. Erdseile und Kabelmäntel mit Erdwirkung, die betriebsmäßig angeschlossen sind, **dürfen nicht abgetrennt werden**.
  - Erdungsimpedanz: **Z_E = (r_E · U_EV) / I** mit U_EV = gemessene Spannung zwischen Erdungsanlage und Sonde im Bereich der Bezugserde (neutrale Erde), I = gemessener Versuchsstrom, r_E = Reduktionsfaktor der Leitung zum Gegenerder (durch Rechnung oder Messung bestimmbar).
  - Für Leitungen **ohne Erdseile** und Kabel ohne Schirm/Bewehrung ist **r_E = 1**.
  - Erdseile anderer parallel zur Versuchsleitung verlaufender Leitungen sind zu berücksichtigen. Bei Kabel mit beidseitig geerdeter, gut leitender metallischer Hülle fließt der größte Teil des Versuchsstroms über die Hülle zurück; liegt ein isolierender Außenmantel vor, kann es zweckmäßig sein, die Erdungen der Hülle aufzuheben. Bei Kabeln mit **erdfühliger metallener Außenhülle dürfen die Erdungen jedoch nicht aufgetrennt werden**.
  - Entfernung zwischen Erder und Gegenerder soll nach Möglichkeit **5 km nicht unterschreiten**.
  - Versuchsstrom möglichst so hoch wählen, dass zu messende Spannungen größer als Fremd-/Störspannungen sind — i. A. gewährleistet **ab 50 A** Versuchsstrom.
- **§ 127.2.3:** Innenwiderstand des Spannungsmessers soll **mindestens das 10-Fache des Ausbreitungswiderstandes der Sonde** betragen. Fremd-/Störspannungen sind zu eliminieren (§ 130).
- **§ 127.2.3 (Ermittlung aus Einzelwiderständen):** Besteht die Erdungsanlage aus einzelnen, sich praktisch nicht beeinflussenden Erdern, die über Erdungsleitungen verbunden sind, kann Z_E bestimmt werden, indem der **Ausbreitungswiderstand jedes Erders bei aufgetrennten Verbindungsleitungen** mit der Erdungsmessbrücke ermittelt, die Impedanzen der Erdungsleitungen errechnet und Z_E aus der **Ersatzschaltung** der Ausbreitungswiderstände und Leitungsimpedanzen bestimmt wird. Bei Verbindung über Freileitungserdseile statt Erdungsleitungen gilt dasselbe Verfahren.

#### § 128 — Ermittlung der Erdungsspannung
- Es gilt: **U_E = Z_E · I_E**. Dabei: U_E = Erdungsspannung entsprechend § 8.1, Z_E = Erdungsimpedanz (aus Messung § 127.2.2 oder Rechnung § 127.2.3), I_E = Erdungsstrom entsprechend § 9.3.
- **§ 128.1 (Erdschluss innerhalb einer Anlage, Abb. 5-2):** Für den Erdungsstrom: **I_E = r₁·3·I₀₁ + r₂·3·I₀₂ + … = Σ rᵢ·3·I₀ᵢ**. I₀ᵢ = Nullströme der einzelnen in die Anlage führenden Leitungen, rᵢ = Erdseilreduktionsfaktoren der einzelnen fehlerstromführenden Leitungen. Sind alle Reduktionsfaktoren gleich: **I_E = r · (I_k − I_w)**, mit I_k = Erdfehlerstrom und I_w = Strom über den Transformatorsternpunkt.
- **§ 129 (vorgezogener Block — Erdkurzschluss außerhalb einer Anlage, Abb. 5-3):** Für große Entfernungen zwischen Fehlerstelle F und Anlage A gelten gesonderte Beziehungen für den Erdungsstrom der Anlage A und des Fehlermastes F (Formeln OCR-verstümmelt; Grundprinzip: Aufteilung der Nullströme abzüglich der vom Fehler betroffenen Leitung, gewichtet mit Erdseilreduktionsfaktoren). Hinweis: Bei Erdkurzschlüssen außerhalb, aber in der Nähe der Anlage fließt ein größerer Teil des Fehlerstroms als (1−r)·3·I₀ über das Erdseil → günstigere Verhältnisse möglich.

#### § 129 — Messung von Berührungsspannungen
- Berührungsspannung mit Spannungsmesser mit **Innenwiderstand etwa 1 kΩ** ermitteln.
- Messelektrode(n) zur Nachbildung der Füße: **Fläche insgesamt 400 cm²**, Mindestgewicht insgesamt **500 N** auf dem Boden aufliegend. Ersatzweise darf eine **mindestens 20 cm tief eingetriebene Sonde** statt der Messelektrode verwendet werden.
- Als Messelektrode zur Nachbildung der Hand kann eine Spitzenelektrode verwendet werden; Farbanstriche an der Messstelle (jedoch nicht Isolierungen) sind zuverlässig zu durchstoßen.
- Bei der Messung am Anlagenteil ist die Elektrode in **1 m Abstand** vom berührbaren Anlagenteil auf den Standort aufzusetzen — bei Beton oder ausgetrocknetem Boden auf einer **angefeuchteten Zwischenlage**.
- Eine Klemme des Spannungsmessers wird mit der Handelektrode, die andere mit der/den Fußelektrode(n) verbunden. Stichprobenartige Messungen genügen.
- Bewährt: **kombinierte hoch- und niederohmige Messung** — bricht die Spannung beim Umschalten von hohem Innenwiderstand auf den Eingangswiderstand von 1 kΩ erheblich zusammen, können zu hohe Übergangswiderstände im Messkreis vorhanden sein. Für Überblick über die obere Grenze der Berührungsspannungen ist die Messung mit hohem Eingangswiderstand und Sonde zweckmäßig.

#### § 130 — Eliminierung von Fremd- und Störspannungen bei Erdungsmessungen
Bei Bestimmung von Erdungs-/Berührungsspannungen (§ 127.2.2, § 129) können Messwertverfälschungen durch Fremd-/Störspannungen jeder Art auftreten (z. B. induktive Beeinflussung langer Messleitungen, induktive Beeinflussung des Versuchsstromkreises durch in Betrieb befindliche Nachbarsysteme). Bewährte Methoden:
- **§ 130.1 Schwebungsmethode:** Spannungsquelle (z. B. Notstromaggregat), deren Frequenz um **einige Zehntel Hertz** von der Netzfrequenz abweicht. Durch asynchrone Überlagerung pendelt der Zeiger zwischen Maximalwert U₁ und Minimalwert U₂; die vom Versuchsstrom hervorgerufene Spannung wird daraus berechnet (U = (U₁ ± U₂)/2 je nach Verhältnis zur Störspannung).
- **§ 130.2 Umpolungsmethode:** Netzsynchrone Spannungsquelle (Transformator), deren Phasenlage nach einer stromlosen Pause um **180° el.** gedreht wird. Gemessen werden U₁ (vor Umpolen), U₂ (nach Umpolen) und Störspannung U_S (bei abgeschaltetem Versuchsstrom); aus geometrischen Beziehungen folgt die vom Versuchsstrom hervorgerufene Spannung.
- **§ 130.3 Kompensationsverfahren:** Längere Messleitungen (z. B. zur Sonde nach Abb. 127-1) möglichst **rechtwinklig zur Versuchsleitung** führen. Ist das räumlich nicht möglich, kann der induzierte Spannungsanteil durch Kompensation eliminiert werden.
- **Abblockung von Gleichströmen:** Bei hohen Gleichspannungsanteilen der Störspannungen kann ein Spannungsmesser erforderlich werden, bei dem die Gleichspannung abgeblockt wird.

### Anhang 3 / § 131 — Berechnungsbeispiel (Länge von Horizontalerdern/Kabeln mit Erderwirkung)
Gegeben:
- Erdkurzschlussstrom **I_F = 800 A**
- Erdkurzschlussdauer **= 1,2 s**
- **U_B = 75 V** gemäß Abb. 18-1 (OCR „76V")
- Eingeführte Kabel: Kabelsysteme mit Kupferschirm, resultierender **Reduktionsfaktor r = 0,7**
- Oberflächenerder: verzinkte **Stahlbänder 40 mm × 4 mm**
- Kabel gehen auf **drei verschiedenen Trassen** ab → Erdungsimpedanz je Trasse **Z_ET ≈ 0,271 Ω** (Berechnung über r · I_F = 0,7 · 800 A = 560 A), Gesamt (Parallelschaltung dreier Trassen) **Z_E ≈ 0,271/3 ≈ 0,0903 Ω** (OCR „0,084"/„0,0841")
- Spezifischer Erdwiderstand **ρ = 50 Ωm**
- Ergebnis aus Abb. 15-1: erforderliche **Erderlänge 250 m** je Trasse (für jede der drei Trassen)

### Sachverzeichnis (Stichwort → Paragraph, Auswahl)
- Abschaltung → § 7.3, 7.4; Ausschaltzeit → § 12.3; Ausschaltstelle → § 22
- Ausbreitungswiderstand → § 5.2, 10.2, 18.1, 127
- Baustromversorgung → § 21.2; Bahnanlage → § 1.2, 18.6
- Beanspruchung, thermische → § 13.3, 14.1
- Berührungsspannung → § 8.3, 12.2, 15.1, 18.3(1), 18.7, 19.2.1, 19.3.3, 20.2, 20.4, 23.2.2, 129
- Betätigungsgestänge → § 20.3; Betriebserdung → § 6.2, 125, 23
- Bezugserde → § 3.2, 6.2, 5.3, 8.1; Blitzschutz → § 24, 124; Blitzschutzerdung → § 8.3
- Campingplatz → § 19.2.2, 19.3.4; Eigenbedarfsnetz → § 18.8
- Endverschluss → § 20.5; Erdfehlerstrom → § 9.2, 8.4; Erdkurzschluss → § 21.2; Erdkurzschlussstrom → § 9.3
- Erdoberflächenpotential → § 8.2, 8.5; Erdschluss → § 9.1, 18.2.2; Erdschlusskompensation → § 7.2, 13.2
- Erdschlussreststrom → § 8.2; Erdschlussspule → § 19.1, 124.4, 124.5; Erdschlussstrom → § 7.2
- Erdung, vorübergehende → § 126 (bzw. 22.2); Erdungsanlage → § 3.5, 5.3, 12
- Erdungsimpedanz → § 5.3, 19.1, 19.2, 127; Erdungsleitung → § 3.4, 14, 17, 18.1
- Erdungssammelleitung → § 3.5, 17.1, 17.3; Erdungsspannung → § 8, 12.2, 18.7
- Erdwiderstand, spezifischer → § 5.1, 10.1, 126; Erwartungsfaktor → § 2.6 (Kontext 19.3.2: w = 1 bzw. 0,7)
- Fernmeldekabel → § 18.3(2); Freibad → § 19.2.2, 19.3.4; Freileitungsmast → § 18; Freiluftanlage → § 16.2.4
- Fundamenterder → § 3.3, 4.5, 10.1, 18.7; Gleichstrombahn → § 1.2, 18.6.3
- Horizontalerder → § 4.1.1, 10.2, 15.2, 16; Innenanlage → § 18.2.3
- Kabel → § 4.4, 15.3, 18.3; Korrosion → § 131, 13.2, 17.1, 18.3(1)
- Maschenerder → § 10.2; Mastschalter → § 20; Maststation → § 20.4; Messwandler → § 18.4
- Metallgerüst → § 17.2, 18.1; Mindestabmessungen → § 13.2; Nennspannung → § 1.1, 124; Nullung → § 23.2.2
- Potentialausgleich → § 8.5, 15.2.3, 15.2.4; Potentialsteuerung → § 4.8, 8.6, 15.2, 18.7; Potentialverschleppung → § 8.7, 18.7
- Reduktionsfaktor → § 9.5; Schaltkasten → § 20.4; Schnellausschaltung → § 8.4, 19.3.3; Schrittspannung → § 8.4
- Schutzerdung → § 6.1, 125, 23; Standortisolierung → § 8.8, 16.2, 18.6.1, 21.1
- Sternpunkt → § 7, 19.2; Sternpunkterdung → § 7.3, 7.4, 19.3, 19.4; Steuererder → § 4.8, 15.2.4, 18.5, 20.2
- Stoß-Erdungswiderstand → § 5.4, 124.1, 124.2; Strahlenerder → § 16.1
- Überspannungsableiter → § 18.1(6); Umzäunung → § 15.2.2, 18.5; Verbindungsstelle → § 16.3, 17.2, 17.5
- Vertikalerder → § 4.1.2, 10.2, 18.2; Werkstoff → § 13; Zusammenschluss → § 23
