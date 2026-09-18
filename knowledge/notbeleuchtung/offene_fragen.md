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
5. **Antipanik-Skala uneinheitlich:** Erklärungspläne inserieren
   Antipanikleuchte-RIVO mit 25,25 (296 mm, 3×), 45,96 (539 mm, 4×) und 53,7
   (630 mm, 1×). Registry nutzt die häufigste (46,0 → 539 mm). Owner-Sollgröße?
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

## Phase B (wird während des Abgleichs ergänzt)

_(noch leer — Einträge folgen mit dem PDF↔DXF-Abgleich)_
