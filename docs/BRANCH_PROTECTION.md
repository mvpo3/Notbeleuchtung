# Branch Protection für `main` — Anleitung für den Repo-Owner

Diese Datei ist eine **Handlungsanweisung an den Kontoinhaber (@mvpo3)**. Wir
können die Einstellungen nicht selbst setzen (Token `admin:false`), deshalb hier
Ist-Stand, Anlass und beide Wege (UI und API).

## 1. Gemessener Ist-Stand (2026-09-10, nur lesende `gh api`-Aufrufe)

```
$ gh api repos/mvpo3/Notbeleuchtung/branches/main/protection
{"message":"Not Found", ... ,"status":"404"}
→ Auf main ist KEINE Branch Protection gesetzt.

$ gh api repos/mvpo3/Notbeleuchtung --jq '.permissions'
{"admin":false,"maintain":false,"pull":true,"push":true,"triage":true}
→ Unser Token darf sie nicht setzen.

$ gh api repos/mvpo3/Notbeleuchtung/rulesets
{"message":"Upgrade to GitHub Pro or make this repository public to enable this feature.","status":"403"}

$ gh api repos/mvpo3/Notbeleuchtung --jq '{private,visibility,owner_type:.owner.type,plan:.owner.plan}'
{"owner_type":"User","plan":null,"private":true,"visibility":"private"}
→ Privates Repo auf einem User-Account ohne Plan: Branch Protection und Rulesets
  sind auf diesem Plan gar nicht verfügbar. Der 404 hat damit zwei Gründe.
```

**Konsequenz:** Solange kein Upgrade auf GitHub Pro/Team erfolgt (oder das Repo
public geschaltet wird), ist der Check `contract-freeze`
(`.github/workflows/contract-freeze.yml`) der **einzige verfügbare Riegel** — er
läuft ohne Branch Protection, kann einen Merge aber nur *anzeigen*, nicht
*verhindern*. Erst als Required Status Check blockiert er wirklich.

## 2. Was Vorfall PR #149 gezeigt hat

Gemessen (`gh api`):

| Befund | Wert |
|---|---|
| angelegt / gemerged | 2026-09-09T18:42:58Z / 2026-09-10T10:04:20Z |
| Commits / geänderte Dateien | 55 / 121 |
| Reviews | `[]` — **null** |
| Check `test` (ci.yml) auf head_sha | **failure** (Run 34463575540) |
| Check `contracts` (contract.yml) | success |
| gemerged von | polatselman |

Der PR wurde am 09.09. mit anderem Inhalt und altem Titel angelegt, die 55
Commits kamen später dazu — darunter der Contract-Bump `raum_modell` → 1.4.0.
Gemerged wurde er mit **0 Reviews und rotem `test`-Check**.

Drei getrennte Lücken:
1. Kein Review erzwungen → `required_approving_review_count`.
2. Kein grüner Check erzwungen → `required_status_checks` (hätte #149 allein
   schon blockiert, `test` war rot).
3. Nachgeschobene Commits entwerten kein Approval → `dismiss_stale_reviews`
   (bzw. bei uns heute: der Check `contract-freeze`).

## 3. Weg A — Web-UI

**Settings → Branches → Branch protection rules → Add rule**, Branch name
pattern: `main`. Dann anhaken:

| Pflichtpunkt | Checkbox |
|---|---|
| Reviews vor Merge | „Require a pull request before merging" → „Require approvals", **Required number of approvals = 3** |
| Code-Owner-Review | „Require review from Code Owners" |
| **Stale Approvals verwerfen** | „Dismiss stale pull request approvals when new commits are pushed" |
| Required status checks | „Require status checks to pass before merging" → suchen und wählen: **`test`**, **`contracts`**, **`contract-freeze`** |
| Branch aktuell | „Require branches to be up to date before merging" |
| gilt auch für Admins | „Do not allow bypassing the above settings" |
| Force-Push/Delete | „Allow force pushes" und „Allow deletions" **aus** lassen (Default) |

## 4. Weg B — `gh api` (identisches Ergebnis)

```bash
gh api --method PUT repos/mvpo3/Notbeleuchtung/branches/main/protection \
  --input - <<'JSON'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["test", "contracts", "contract-freeze"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 3,
    "require_code_owner_reviews": true,
    "dismiss_stale_reviews": true
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON
```

Kontrolle danach:

```bash
gh api repos/mvpo3/Notbeleuchtung/branches/main/protection \
  --jq '{checks:.required_status_checks.contexts,
         strict:.required_status_checks.strict,
         approvals:.required_pull_request_reviews.required_approving_review_count,
         code_owners:.required_pull_request_reviews.require_code_owner_reviews,
         dismiss_stale:.required_pull_request_reviews.dismiss_stale_reviews,
         admins:.enforce_admins.enabled}'
```

## 5. Check-Namen

Gemessen an PR #149 existieren heute genau zwei Check-Runs (App `github-actions`,
keine Commit-Statuses): **`test`** (Job in `ci.yml`) und **`contracts`** (Job in
`contract.yml`). Neu dazu kommt **`contract-freeze`** (Job in
`contract-freeze.yml`). Genau diese drei Namen in `contexts` eintragen.

`contract-freeze` ist absichtlich **grün, wenn ein PR die Contracts nicht
berührt** (nicht „skipped") — nur so ist er als Required Check brauchbar.

## 6. Reihenfolge

1. Plan-Upgrade (Pro/Team) oder Repo public schalten — sonst greift Abschnitt 3/4 nicht.
2. `contract-freeze` einmal auf einem PR laufen lassen, damit der Name in der
   Check-Auswahl der UI auftaucht.
3. Regel setzen, danach mit dem `--jq`-Aufruf aus Abschnitt 4 gegenprüfen.

## 7. Stand 2026-09-11 — was `b00420a` schließt und was offen bleibt

Mit PR #152 ist Enis' Korrektur `b00420a` auf `main` (gemerged 2026-09-10
23:31 UTC). `owners()` las `.github/CODEOWNERS` bisher mit `open()` aus dem
Arbeitsbaum — bei `on: pull_request` ist das der **PR-Stand**, ein PR konnte sich
die benötigte Zustimmung also im selben Commit wegdefinieren. Jetzt kommt die
Owner-Liste über die API aus `CODEOWNERS` am **`BASE_SHA`** des PR; jede
unlesbare Prüfgrundlage endet in `sys.exit` („Abbruch statt Freigabe").
Unabhängig nachgeprüft am Stand `804e6af`: `tests/ci` 14 passed,
`tests/ci tests/contract` 70 passed, `ruff check .` clean.

Das schließt **eine** Lücke, nicht zwei. Offen bleiben zwei **verschiedene**
Fragen, die nicht vermischt werden dürfen:

### 7.1 Vertrauenswürdige Ausführung des Prüfers — eine Workflow-Umstellung

Bei `on: pull_request` laufen `contract-freeze.yml` **und**
`.github/scripts/contract_freeze_check.py` aus dem **PR-Head**. Ein PR, der eine
der beiden Dateien ändert, verändert damit den Prüfer selbst — Workflow und
Prüfskript sind **vom PR beeinflussbar**. Abhilfe wäre eine
**Workflow-Umstellung**, die den Prüfer in einer Fassung laufen lässt, die der PR
nicht bestimmt (z. B. Ausführung der Basis-Fassung des Workflows, ohne
PR-Inhalte auszuführen). Das ist mit GitHub-Mitteln erreichbar und **bewusst
nicht** Teil von Enis' Paket. Stand: nicht beauftragt, nicht entschieden.

### 7.2 Von GitHub erzwungene Mergesperre — eine Repo-Einstellung

Davon unabhängig: ein **Required Status Check** (`contract-freeze` in
`required_status_checks`, Abschnitte 3 und 4) ist keine Code-, sondern eine
**Repo-Einstellung**. Sie liegt beim Kontoinhaber **@mvpo3 (Leonis)** und ist
laut aktuellem Plan **möglicherweise nicht verfügbar**. Heute lesend
nachgemessen (2026-09-11 21:19 UTC), unverändert gegen Abschnitt 1:

```
branches/main/protection → 404 Not Found
permissions              → {"admin":false,"maintain":false,"pull":true,"push":true,"triage":true}
rulesets                 → 403 "Upgrade to GitHub Pro or make this repository public to enable this feature."
repo                     → {"owner_type":"User","plan":null,"private":true,"visibility":"private"}
```

Keiner der beiden Punkte ersetzt den anderen: 7.2 allein sperrt zwar den Merge,
lässt aber einen PR durch, der den Prüfer selbst umschreibt; 7.1 allein macht den
Prüfer unbeeinflussbar, verhindert aber keinen Merge.

> **Bis beides geklärt ist, ist `contract-freeze` eine verlässliche Anzeige,
> keine technisch erzwungene Sperre.** (Enis, Übergabe zu `b00420a`, § 6)
