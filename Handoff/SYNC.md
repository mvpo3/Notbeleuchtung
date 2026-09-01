# SYNC — Stand nachziehen, ohne Arbeit zu verlieren

**Auslöser:** Der Owner schreibt in seiner Session **„Sync"** (oder „GitHub wurde
aktualisiert", „zieh den Stand nach"). Dann arbeitest du, Claude, diese Datei von oben
nach unten ab — **in dieser Reihenfolge, ohne Schritte zu überspringen.**

Diese Datei ergänzt `Handoff/README.md` (Sitzungsstart) um den Fall *„jemand anderes hat
gepusht"*. Bei einem frischen Sitzungsstart gilt weiterhin zuerst `Handoff/<NAME>.md`.

---

## Grundregel

> **Erst sichern, dann holen.** Kein `git pull`, kein `git checkout`, kein `git reset`,
> kein `git stash drop`, kein `git clean`, solange unversionierte Arbeit im
> Arbeitsverzeichnis liegt.

Der Owner hat oft Stunden unversionierter Arbeit offen. Die ist **immer** wertvoller als
ein schneller Sync. Wenn du unsicher bist: **frag den Owner, statt zu handeln.**

Verboten ohne ausdrückliche Ansage des Owners:
`git reset --hard` · `git checkout -- .` · `git clean -fd` · `git stash drop` ·
`git push --force` · Verwerfen von Konfliktseiten mit `--ours`/`--theirs` im fremden Package.

---

## Schritt 1 — Eigenen Stand sichern

```bash
git status --short
git branch --show-current
```

**Ist etwas unversioniert?** Dann zuerst festhalten, bevor irgendetwas geholt wird:

```bash
git add -A
git commit -m "wip(<bereich>): Zwischenstand vor Sync"
```

Ein WIP-Commit auf dem eigenen Branch ist jederzeit umbaubar (`git commit --amend`,
interaktives Aufräumen später). Ein verlorener Arbeitsstand ist es nicht.

Willst du den Zwischenstand nicht in der Historie: `git stash push -u -m "vor-sync-<datum>"`
— aber **nie** `git stash drop`, und den Stash im Bericht an den Owner nennen, damit er
nicht vergessen wird.

**Melde dem Owner in einem Satz, was du gesichert hast.** Er muss wissen, wo seine Arbeit
gelandet ist.

---

## Schritt 2 — Sehen, was hereinkommt (noch nichts ändern)

```bash
git fetch --all --prune
git log --oneline HEAD..origin/main
git diff --stat HEAD origin/main
```

Ordne die Änderungen den Bereichen zu und **melde sie dem Owner**, bevor du integrierst:

| Pfad | Eigentümer | Bedeutung für dich |
|---|---|---|
| `src/notbeleuchtung/raumerkennung/**` | Selman | RaumModell kann sich geändert haben |
| `src/notbeleuchtung/platzierung/**` | Leonis | Platzierungsverhalten |
| `src/notbeleuchtung/normwissen/**` | Enis | Normwerte, LB-Parsing |
| **`src/notbeleuchtung/hauptengine/contracts/**`** | **gemeinsam** | **Achtung, siehe unten** |
| `docs/COORDINATION.md` | gemeinsam | Board — immer lesen |
| `Handoff/**` | gemeinsam | Auftragslage kann sich geändert haben |

### Contract-Änderung = Sonderfall

Hat sich etwas unter `hauptengine/contracts/**` geändert, gilt die **Contract-Freeze-Regel**
aus `docs/COORDINATION.md`. Dann:

1. Lies den Diff der Contracts **vollständig**, nicht nur die Statistik.
2. Prüfe, ob das eigene Package das Protocol noch erfüllt.
3. **Melde es dem Owner ausdrücklich**, auch wenn die Tests grün sind — eine
   Contract-Änderung betrifft alle drei.

---

## Schritt 3 — Integrieren

Auf dem eigenen Feature-Branch:

```bash
git rebase origin/main
```

**Bei Konflikt:**
- Im **eigenen** Package: auflösen, der Owner kennt seinen Code.
- Im **fremden** Package oder in `hauptengine/`: **nicht raten.** `git rebase --abort`,
  dem Owner melden, was kollidiert. Ein falsch aufgelöster Konflikt in fremdem Code ist
  schlimmer als ein abgebrochener Rebase.

Wer lieber merged statt rebased, macht das — Hauptsache kein `--force` auf einen Branch,
auf dem jemand anderes arbeiten könnte.

---

## Schritt 4 — Testschranke

```bash
.venv/Scripts/python.exe -m pip install -e ".[dev,api]"
.venv/Scripts/python.exe -m pytest -q
```

*(Mac/Linux: `.venv/bin/python`.)*

**Grün** → weiterarbeiten.
**Rot** → **nicht darauf aufbauen.** Ermittle mit `git log --oneline <alt>..<neu>`, welcher
Commit es war, und melde Test, Fehlermeldung und Commit an den Owner. Dann entscheidet er:
zurück auf den vorigen Stand oder Reparatur.

Rot heißt nicht „egal, mein Bereich läuft ja". Ein roter Gesamtlauf blockiert alle drei.

---

## Schritt 5 — Archivieren

Damit der nächste Sync weiß, was war:

1. **`docs/COORDINATION.md`** — Status-Board des eigenen Bereichs aktualisieren.
   Erledigtes abhaken, Neues eintragen, offene Nähte zu den anderen benennen.
2. **`Handoff/<NAME>.md`** — Auftragslage nachziehen, wenn sich das Ziel verschoben hat.
3. Beides committen. Kleine Commits, eine Sache pro Commit (Regel aus `COORDINATION.md`).

Diese zwei Dateien sind das Gedächtnis des Teams. Sessions teilen keinen Speicher —
was hier nicht steht, ist nach dem Schließen des Fensters weg.

---

## Schritt 6 — Bericht an den Owner

Kurz, in dieser Form:

```
Gesichert:   <WIP-Commit / Stash / nichts nötig>
Hereingekommen: <n> Commits — <Bereiche>
Contracts:   unverändert | GEÄNDERT (Details)
Rebase:      sauber | Konflikte in <Pfad>
Tests:       <n> passed, <n> failed
Board:       aktualisiert
Offen:       <was der Owner entscheiden muss>
```

---

## Owner-Grenzen bleiben auch beim Sync bestehen

Kein Owner-Package importiert ein anderes — nur
`notbeleuchtung.hauptengine.contracts`. Beim Auflösen von Konflikten und beim Reparieren
roter Tests gilt dasselbe: **du arbeitest im Package deines Owners.** Ist der Fehler
woanders, wird er gemeldet, nicht repariert.

| Owner | Package |
|---|---|
| Selman | `src/notbeleuchtung/raumerkennung/` |
| Leonis | `src/notbeleuchtung/platzierung/` |
| Enis | `src/notbeleuchtung/normwissen/` |
| gemeinsam | `src/notbeleuchtung/hauptengine/` (Contracts = Konsens) |

---

## Warum die Testschranke doppelt zählt

Die Engine wird inzwischen von der **RIVOPLAN-App** als Dienst angebunden
(FastAPI, `POST /plan`). Die App aktualisiert ihren Engine-Stand auf Knopfdruck und
**übernimmt einen neuen Stand nur, wenn `pytest` grün ist** — bei Rot läuft dort die
vorige Fassung weiter.

Praktisch heißt das: ein roter Testlauf blockiert nicht nur euch, sondern hält auch die
App auf dem alten Stand. Umgekehrt gilt: was hier grün gepusht wird, ist in der App
verfügbar, sobald jemand aktualisiert.

Deshalb: **lieber ein Commit mehr mit grünen Tests als ein großer mit roten.**
