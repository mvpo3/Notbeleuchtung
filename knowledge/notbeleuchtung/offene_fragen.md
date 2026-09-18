# Offene Fragen — Symbol-/Vorlagen-Migration (Phase A) + Wissensaufbau (Phase B)

Nichts hiervon wurde selbst entschieden — jeder Punkt braucht Owner-Antwort oder
weitere Quelle. Belege: Workflow-Analyse 2026-09-18 (5 Agenten über Bibliothek
alt/neu, Vorlage, Erklärungs-DXFs) + Messskripte (Session-Scratchpad).

## Phase A (Symbole + Vorlage)

1. **Kein Block „Haupteingang/Ausgang" und kein „Pfeil nach oben"** in der neuen
   Bibliothek. Die Owner-Erklärungspläne rotieren das down-Schild für alle
   Richtungen (RIVO-SIBEL-ARR-down mit rot 90/180/270 gemessen) — die Engine tut
   dasselbe (orientation.transformation). Eigener Haupteingangs-Block gewünscht?
2. **„RZ-beidseitig" hat keinen eigenen Block.** Die Vorlagen-Legende komponiert
   ihn aus 2× `RIVO-SIBEL-ARR-left` übereinander (eine Instanz gespiegelt
   xscale=−1/rot=180). Die Engine zeichnet den Wasserscheide-Doppelpfeil weiterhin
   als left+right-Paar am selben Punkt (beide ≈636 mm) — der Owner-Komposition
   folgen oder Paar behalten? (Optisch nahe, aber nicht identisch.)
3. **Namenszwillinge in der Bibliothek:** `RIVO-SIBEL-ARR-down` (klein-nativ,
   17,7 units) vs. `RIVO-SIBEL-ARR_down` (groß-nativ, 463,6 units — Unterstrich!),
   `484848` = optischer Zwilling von RIVO-RZ-ARR_left, `A$C84bb8b19`/`A$C64426be2` =
   identische Wrapper um RIVO-RZ-ARR_down, `595995`/`9809550` = numerische
   Teil-Glyphen (Pfeil/Läufer). Registry nutzt nur die kanonischen; Bibliothek
   aufräumen = Owner-Entscheid (Originale werden nicht verändert).
4. **Fluchtweg-Symbole fehlen in der Bibliothek:** die zwei meistgenutzten grünen
   Symbole der Erklärungspläne — `4444444` (Fluchtweg-Richtungspfeil, 204×) und
   `750298750` (grün gefülltes RZ-Männchen, 155×; Beispiel-Handles EG 20332/20359)
   — existieren NICHT in Notbeleuchtungssymbole_neu+.dxf. In die Bibliothek
   aufnehmen (die Engine zeichnet Fluchtwege bisher als Linien+Chevrons)?
5. ~~Antipanik-Skala uneinheitlich~~ **BEANTWORTET 2026-09-18 (Owner:
   „vergrößern, gut erkennbar, passend zum Plan"):** Soll = Papier-Größe der
   Owner-Legende in der neuen Vorlage × Maßstab 50 → AP 586 mm (RZ 883,
   Aufheller/Spot 192, Anlage 852). Umgesetzt `95c6b82`.
6. **RZ-Zweitgröße 446 mm:** neben der dominanten ~636-mm-Größe kommen RZ mit
   Skala 25,246 (446 mm) vor (6× down, 6× left, 4× right). Kontext-Regel
   (kleine Räume → kleineres Schild)? Engine nutzt bisher EINE Größe.
7. **Vorlagen-Logo** (IMAGE) referenziert den absoluten Fremd-Pfad
   `C:\Users\mvpst\Downloads\…\rivoplan_logo…png` — der Renderer biegt auf
   `Vorlagen-Legende/rivoplan_logo.png` um, aber die Vorlage selbst ist nicht
   portabel (Owner-Original, nicht angefasst).
8. **Vorlagen-Plot-Setup inkonsistent:** Layout1-Papierformat steht auf A4
   (210×297), gezeichnetes Blatt ist ~3119×977 mm; Haupt-Viewport 1:1,
   „1:50" nur als Text. Die Engine stellt den Viewport selbst auf 1:50 —
   funktioniert, aber das Plot-Setup der Vorlage bleibt irreführend.
9. **Namenskollision „Rauchmelder":** Erklärungs-DXF-Definition (CIRCLE+2 LINE,
   ~200 units, Handle-Beispiel EG 1EC01) ≠ Bibliotheks-Definition (nested „rm").
   Bei Block-Importen in Fremdpläne droht Redefinition mit anderem Erscheinungsbild.
10. **„Generelunternehmer"** (Tippfehler) im Vorlagen-Schriftfeld — Owner-Original,
    nur zur Kenntnis.

## Phase B (PDF↔DXF-Abgleich, 2026-09-18)

### Widersprüche PDF-Text vs. DXF (alle geometrisch aufgeklärt)
**Update 2026-09-18 ABEND (PDF-Fassung 20:09): ALLE 4 Widersprüche KORRIGIERT ✓**
— #11 (EG S.10 jetzt (G)/(H) + Screenshot erneuert), #12 (1OG S.19 jetzt „(B)"),
#13 (2OG S.23 „links"), #14 (4OG S.38 „rechts"). Recheck per Text-Extraktion +
S.10-Render.
11. ~~EG S.10 (D)/(E)~~ **KORRIGIERT ✓** (Text (G)/(H), Screenshot zeigt (G)/(H)).
12. ~~1OG S.19 Linie zu (A)~~ **KORRIGIERT ✓** (Text jetzt „zur Notleuchte (B)").
13. **2OG S.23:** „(D) mit Pfeil nach RECHTS" — DXF `852E4` ist ARR-**left**
    (Welt 179,55° West); PDF-Bild S.23 UND PDF-Text S.25 sagen ebenfalls links.
    Schreibfehler; Regelbasis folgt DXF+S.25.
14. **4OG S.38:** „(C) mit Pfeil nach links" — DXF: (C) = RIVO-RZ-ARR_**right**
    rot 89,9 (Welt Nord); die PDF-eigene S.37-Regel fordert hier „rechts".
    Schreibfehler?

### Unerklärte Leuchten (nicht Legende, echte Klärung nötig)
15. **EG `202CC` + `2137C`:** DOPPELTES down-RZ am Süd-Ausgang des linken
    Stiegenhauses (70 mm Versatz, Skalen 25,2 vs. 41,2) — Versehen oder Absicht?
    Das zugehörige Tür-Beispiel fehlt im PDF.
16. **EG `2072F`:** Antipanikleuchte zwischen Fahrradraum und rechtem STGH —
    im PDF-EG-Kapitel nicht erklärt.
17. **2OG `8532F`:** unbeschriftetes down-RZ (−72431, 61139), Welt-Pfeil Ost —
    kein Label, keine Sichtlinien; Rest/Kopie?
18. **3OG `78DFD` (A, West-STGH-2):** Pfeil Welt 179,7° (West), aber die grünen
    Fluchtpfeile derselben Route zeigen Ost — falsch rotiert oder andere
    Personengruppe? (Plus Kopier-Fragmente A1 `78D6A/78D6C/78D6D` ohne
    Plan-Geometrie.)
19. **1OG `9568D`, 4OG `41221`, DG `206D6`/`206DB`:** isolierte Streuner-/
    Arbeitskopien außerhalb des Grundrisses (4OG-Exemplar = die
    „falsch"-Vergleichsvariante S.35/36) — im PDF nicht erklärt, als
    Kopier-Reste eingestuft.

### Konventions-/Datenfragen
20. **UG-Erklärungs-DXF fehlt** (PDF kündigt „1.UG, 2UG, EG-DG" an; Ordner hat
    nur EG–DG). 1.UG/2.UG-Wissen fehlt der Regelbasis komplett.
21. **Frontalitäts-Ausnahme Tür-RZ:** Tür-RZ am Gangende werden von den
    Wohnungstüren unter 86–90° (Seitenansicht) gesehen (1OG (D), 2OG St.1 (D))
    — gilt die Vorderseiten-Regel (S.31 ff.) für Tür-RZ bewusst nicht/schwächer?
22. ~~2OG St.1-Gang-Läufer blicken Ost~~ **GEKLÄRT 2026-09-18 (Owner + Render-
    Nachprüfung):** Analysefehler unsererseits — Regel #8 (xs>0 → Blick =
    180°+rot) war beim Trio `852C7/852C8/8531B` nicht angewandt. rot 348,7°
    ⇒ Blick 168,7° ≈ **West = Fluchtrichtung, korrekt.** Nahaufnahme bestätigt
    (Läufer läuft nach West). Kein DXF-Fehler, kein Owner-TODO.
23. **EG „FREIHEIT/KEINE FREIHEIT"-Texte + rote Sperr-Rechtecke + Fluchtweg-
    Teilungs-Text** (Mollgasse vs. Anastasius-Grüngasse) sind im PDF nicht
    erläutert — späteres Kapitel?
24. **DG Sichtlinie `208DA`** (Top 27) endet in der Lichtkuppel-Box — Blick auf
    die unversetzte A-Ursprungsposition? Nicht belegbar.
25. **DG Podest-Höhenlage** (FOK PODEST +12,09 vs. STGH +13,45) mit dem grünen
    Fluss nicht auflösbar — woher kommt die Podest-Person?
26. **Blaue „ÜBERGABESTATION"-Schraffur (2OG)** ist keine Lichtkuppel —
    Haustechnik ohne Notbeleuchtungs-Bezug? (Blau = Hindernis-Konvention wäre
    sonst mehrdeutig.)

### Abdeckung (gelabelte + ungelabelte NB-Leuchten je Erklärungs-DXF)
| Geschoss | gesamt | zugeordnet | unerklärt | davon Legende | davon Streuner/Kopie | echt offen |
|---|---|---|---|---|---|---|
| EG | 26 | 15 | 11 | 8 | 1 (`2137C` Duplikat) | 2 (`202CC`+`2072F`) |
| 1OG | 17 | 10 | 7 | 6 | 1 (`9568D`) | 0 |
| 2OG | 11 | 10 | 1 | 0 | 0 | 1 (`8532F`) |
| 3OG | 7 | 3 | 4 | 0 | 3 (Fragment A1) | 1 (`78DFD`-Szene) |
| 4OG | 8 | 7 | 1 | 0 | 1 (`41221`) | 0 |
| DG | 6 | 4 | 2 | 0 | 2 (`206D6`/`206DB`) | 0 |
| **Σ** | **75** | **49** | **26** | **14** | **8** | **4** |
