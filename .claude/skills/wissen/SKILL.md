---
name: wissen
description: >
  Second-Brain über den Projekt-Wissens-Korpus (Digests, ADRs/Vokabular/Koordination,
  Handoffs, autoritatives Norm-Wissen). Beantwortet Fragen MIT Quellen-Zitat
  (Datei:Zeile), hält einen generierten Index (`knowledge/INDEX.md`) frisch und meldet
  Widersprüche/Dubletten/tote Links — ohne die Quell-Dateien umzuschreiben. Norm-Werte
  kommen IMMER exakt aus der autoritativen YAML/dem Contract, nie paraphrasiert.
when_to_use: >
  Bei "frag das Wissen …", "was wissen wir über X", "wo steht Y", "welche Norm/welcher
  Wert für Z", "räum das Wissen auf / index aktualisieren", "gibt es Widersprüche im
  Wissen", oder wenn neues Digest-/Referenz-Material abgelegt wurde. NICHT für externe
  Web-Recherche (dafür `deep-research`) und NICHT zum Ändern von Norm-Werten (Enis' Lane).
---

# wissen — Second-Brain für den Projekt-Korpus

## Warum
Wissen liegt verstreut: `knowledge/extracted/` (Digests), `docs/` (ADRs, VOKABULAR,
COORDINATION, OFFENE_FRAGEN, PORT_LOG), `Handoff/`, `src/notbeleuchtung/normwissen/data/`
(autoritative Norm-YAMLs) + die Session-Memories. Die KI ist der Bibliothekar: du fragst,
sie findet + verknüpft + belegt. **Aber sie schreibt Fakten nicht um** — sie verlinkt und
meldet Drift. Das bewahrt die Auditierbarkeit, die ein ÖNorm-Plan braucht.

## Zwei Wissens-Arten — GEGENSÄTZLICHE Regeln (bindend)
- **Autoritativ (Norm, Enis' Lane):** `normwissen/data/*.yaml` → `NormRegelwerk`-Contract.
  Die Skill **zitiert den exakten Wert + Fundstelle**, formuliert ihn NIE um, „räumt" ihn
  NIE auf, ändert ihn NIE. Änderungen laufen ausschließlich über Enis + Contract-Freeze.
- **Weich (Digests/ADRs/Handoffs/Memories):** Prosa — hier darf die Skill zusammenfassen,
  verknüpfen, indexieren. Auch hier: Quell-Datei bleibt die Wahrheit, Antwort trägt Zitat.

## Ablauf

### Frage beantworten ("was wissen wir über X / welcher Wert für Y")
1. Korpus durchsuchen — deterministisch mit **Grep/Glob** über die Sektionen des Index
   (kein Vektor-DB nötig bei dieser Größe). `knowledge/INDEX.md` als Landkarte.
2. Antwort **synthetisieren MIT Beleg**: jede Aussage trägt `Datei:Zeile` zurück zur Quelle.
   Norm-Werte wörtlich aus der YAML/dem Contract (nicht aus einem Digest, der veralten kann).
3. Widersprüchliche Quellen NICHT stillschweigend auflösen — beide zeigen + Datum/Owner
   nennen, damit der Owner entscheidet (z.B. „Digest: Cap 20 · ADR: Cap 18").

### Index frisch halten ("räum das Wissen auf / index aktualisieren")
- `python scripts/wissen_index.py` regeneriert `knowledge/INDEX.md` (deterministisch,
  verlinkt nur — kein Umschreiben). CI-Wächter: `--check` (Exit≠0, wenn veraltet).
- Das ist der „keeps it tidy month over month"-Teil — **generiert, nicht paraphrasiert**.

### Drift-Report ("gibt es Widersprüche / Lücken")
Ein Lese-Durchgang, der MELDET (nicht fixt):
- **Widersprüche:** zwei Quellen mit unvereinbaren Werten (Cap, Lux, Schwellen).
- **Dubletten:** dieselbe Aussage in mehreren Digests → Kandidat für Konsolidierung.
- **Tote Verweise / Waisen:** Datei referenziert `[[x]]`/Pfad, den es nicht gibt; oder
  Quelle im Korpus, die nirgends verlinkt ist.
- **Norm-Digest-Drift:** ein Prosa-Digest nennt einen Norm-Wert, der von der autoritativen
  YAML abweicht → **immer** die YAML gewinnt; Digest als „nachziehen" flaggen.
Ergebnis = eine To-do-Liste für den Owner/Enis, keine automatische Änderung.

## Tools
- `scripts/wissen_index.py` (GEBAUT) — Index-Generator + `--check`.
- Grep/Glob (deterministische Suche) · die Session-Memories (`MEMORY.md`-Index) als
  Präzedenz/Ergänzung.
- `deep-research`-Skill für ALLES Externe (Web) — diese Skill ist strikt intern.
- optional Embeddings/RAG **erst**, wenn der Korpus zu groß für Grep wird (heute nicht).

## Grenzen
- Ändert nie Quell-Dateien; Norm-Werte nie umformulieren (Enis + Contract).
- Kein Web (→ `deep-research`). Kein Push/Commit ohne Owner-GO.
- Antworten ohne auffindbaren Beleg werden als „nicht im Korpus belegt" markiert — nie geraten.
