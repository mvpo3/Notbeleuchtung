# Handoff — Perfekter Start je Owner

Jeder von euch arbeitet in einer **eigenen Claude-Code-Session im Repo-Ordner**.
Damit dein Claude sofort weiß, wer du bist und was zu tun ist:

> **Erster Prompt in deiner Session:** „Lies `Handoff/<DEINNAME>.md` und leg los."

- Selman → [`Handoff/SELMAN.md`](SELMAN.md)  (Raumerkennung)
- Leonis → [`Handoff/LEONIS.md`](LEONIS.md)  (Platzierung)
- Enis   → [`Handoff/ENIS.md`](ENIS.md)      (Normwissen + LB)

## Für alle gleich (dein Claude soll das kennen)
- **Was wir bauen:** Engine — leerer Architekturplan (DXF) **+ Leistungsbeschreibung
  (LB)** → fertiger ÖNorm-Notbeleuchtungsplan (EN 1838). Nordstern: Chat-Interface
  (Plan hoch → Plan zurück). Regeln: `CLAUDE.md`.
- **Architektur:** Hauptengine besitzt die Contracts; du implementierst dein
  `Protocol` (`hauptengine/contracts/ports.py`). **Kein Owner-Package importiert ein
  anderes** — nur `notbeleuchtung.hauptengine.contracts`. Naht = Contracts + Fixtures.
- **Fake-first:** der E2E-Durchstich (`tests/e2e/`) ist schon grün (Fakes liefern
  4OG-Fixtures). Du ersetzt „deinen" Fake in `tests/fakes.py` durch echten Code.
  Bis dahin blockierst du niemanden.
- **Port-Material liegt schon im Repo** (ihr habt keinen elektro-planer-Zugriff —
  Leonis hat es gestaged): Enis → `normwissen/_port_source/`, Selman →
  `raumerkennung/_port/`.
- **Setup:** `python -m venv .venv` → `pip install -e ".[dev,api]"` → `pytest -q`
  (13✓/1s). Details: `docs/ONBOARDING.md`.
- **Workflow:** Branch `<name>/<thema>` → im eigenen Package bauen → `pytest` grün →
  PR. CODEOWNERS fragt den Reviewer, CI (`contract`+`ci`) muss grün.
- **Board/Status:** `docs/PROGRAMM_NOTBELEUCHTUNG.md`. Dein Task: GitHub-Issue #1/#2/#3.
