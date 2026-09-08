---
name: sync-review
description: >
  Fremd-Owner-Stand (Selman-/Enis-PR oder git-Bundle) isoliert prüfen und ein GO/NO-GO
  geben, ohne den eigenen Arbeitsstand, Branches oder das venv zu gefährden. Prüft
  Contract-Drift + Naht-Invarianten, Suite/ruff, Symbol-Bänder und (bei Render-Änderung)
  die Ausgabe. Schließt mit „zur Übernahme empfohlen" oder „vor Übernahme fixen: …";
  irreversible Schritte (Merge/Push/Kommentar) nur mit Owner-GO.
when_to_use: >
  Bei "review PR #<n>", "prüf Selmans/Enis' Stand", "bundle-recheck",
  "sync + prüfen", "ist der Stand übernehmbar", oder wenn ein Bundle/PR eines anderen
  Owners hereinkommt. NICHT für eigene, schon lokale Arbeit (dafür pytest/ruff direkt).
---

# sync-review — Fremd-Stand isoliert prüfen, GO/NO-GO

## Warum
Der Cross-Owner-Review (Selman/Enis-PR oder -Bundle) ist wiederkehrende Handarbeit:
Herkunft verifizieren, isoliert testen ohne den eigenen Tree/venv zu zerschießen,
Contract-Naht + Bänder prüfen, ehrlich abschließen. Diese Skill kanonisiert genau das
(2026-09-08 mehrfach von Hand gefahren: `19c987d`, `0b66485`, #129).

## Schritt 0 — Herkunft & Isolation (nicht verhandelbar)
- **PR:** `gh pr view <n>` (Basis, Mergeability, Reviews) → `gh pr checkout <n>` ODER
  besser ein **isolierter Worktree** auf dem PR-Head.
- **Bundle:** `sha256sum` gegen die genannte Prüfsumme · `git bundle verify` (Ziel-Ref +
  benötigte Basis) · Basis ggf. `git fetch origin` · Import in einen **neuen**
  Vergleichsbranch (nie bestehende überschreiben).
- **Immer** `git worktree add --detach <dir> <commit>`; bestehende Branches/Stände/venv
  unangetastet. **Editable-Install-Falle:** ein geteiltes `pip install -e <main>`
  überschattet den Worktree (PEP-660-Meta-Finder) → temporär
  `pip install -e <worktree> --no-deps`, testen, danach `pip install -e <main>` restaurieren.
  Import-Pfad nachweisen (`python -c "import notbeleuchtung, os; print(...)"`).

## Schritt 1 — Contract & Naht (das konsens-gebundene Stück)
- Berührt der Stand `hauptengine/contracts/**`? → `contract_version` gebumpt +
  `python scripts/gen_schema.py --check` grün? (Drift-Gate.)
- Naht-Invarianten: `pytest tests/contract -q` — `covers_segment ∈ RaumModell.segmente`
  · `norm_quelle ∈ NormRegelwerk.quellen` · `catalog_key ∈ schrack_symbol_mapping.yaml`.
- Greift der Change in eine **fremde Lane** (z.B. Selman in `platzierung/`)? → gesondert
  ausweisen; das ist ein Naht-/Ownership-Befund, kein stiller Durchwink.

## Schritt 2 — Verhalten
- `pytest -q` grün + `ruff check .`; Ergebnis mit dem behaupteten Vergleich (z.B.
  „macOS: 101 passed") abgleichen, Abweichungen erklären.
- Symbol-/Prüf-Bänder der E2E-Familien: kippt ein Band → **bewusste Änderung?** Dann
  Begründung verlangen, nicht still nachziehen.
- Bei „rebasiert, inhaltlich identisch": Patch-/range-diff-Gleichheit gegen den schon
  abgenommenen Stand zeigen (Absolut-Datei-Diff ist bei anderer Basis irreführend).
- Ändert der Stand Render-Ausgabe? → `plan-verify`-Batterie anhängen (PDF %%EOF,
  DXF-Read-back, Vermerk-Breiten).

## Schritt 3 — Verdikt (ehrlich, getrennt)
- Klarer Abschluss: **„<X> zur Übernahme empfohlen"** ODER **„vor Übernahme fixen: <konkret>"**.
- Bekannte, separate Baustellen (L2-xfail, template_path/T1, Photometrie …) **getrennt**
  ausweisen — eine Empfehlung fürs eine ist keine Freigabe fürs andere.
- **Kein Merge/Push/GitHub-Kommentar ohne explizites Owner-GO.** Aufräumen:
  `git worktree remove --force`, Editable-Install restauriert, Vergleichsbranch als
  Referenz behalten.

## Tools
- `gh` (PR-State/Checkout/Checks) · `git bundle`/`git worktree` · `sha256sum`.
- `scripts/gen_schema.py --check` (Contract-Drift) · `pytest tests/contract` (Naht).
- E2E-Bänder (`tests/e2e/…`, `tests/naht/…`) als Referenz.
- optional die `plan-verify`-Batterie, wenn Render-Ausgabe betroffen ist.

## Grenzen
- Prüft Naht/Contract/Verhalten/Integrität — **ersetzt keine fachliche Norm-Abnahme**.
- Rührt fremde Branches/Tree/venv nur temporär + restauriert; nichts Irreversibles ohne GO.
