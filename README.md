# Notbeleuchtung

Engine: **leerer Architekturplan (DXF) + Leistungsbeschreibung (LB)** → fertiger
ÖNorm-konformer **Notbeleuchtungsplan** (EN 1838) → DXF/PDF.
**Nordstern:** Chat-Interface — Plan hochladen → Notbeleuchtungsplan zurück.

3-Owner-Contract-Architektur (Dependency-Inversion): die Hauptengine besitzt die
Contracts, Selman/Leonis/Enis implementieren je ein Protocol.

```
Architekturplan ─► Selman: RaumModell ─┐
                                        ├─► Leonis: Platzierer(Raum, Norm, LB) ─► Render → Notbeleuchtungsplan ─► POST /plan ─► Chat
LB ─► Enis: LBVorgabe / NormRegelwerk ──┘
```

## Erste Schritte (Enis · Selman · Leonis)

**1. Repo holen** (privat → GitHub-Login nötig):
```bash
gh auth login                          # einmalig, Browser-Login
gh repo clone mvpo3/Notbeleuchtung
cd Notbeleuchtung
```
*(Ohne `gh`: `git clone https://github.com/mvpo3/Notbeleuchtung.git`.)*
⚠️ Clone lädt ~772 MB (CAD-Pläne in `Projekte/`) — dauert ein paar Minuten.

**2. Ordner öffnen + Claude/Cursor darin starten.** In Cursor: *File → Open Folder →
Notbeleuchtung*. Claude Code **im Ordner** starten (sonst lädt die falsche CLAUDE.md).

**3. In den Chat schreiben:** `Handoff Enis` (bzw. `Handoff Selman` / `Handoff Leonis`).
→ Dein Claude liest `Handoff/<NAME>.md`, richtet alles ein (venv, Install, Tests) und
startet deinen Auftrag. Manuell geht's auch:
```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -e ".[dev,api]"   # Mac/Linux: .venv/bin/python
.venv/Scripts/python.exe -m pytest -q                     # erwartet: 13 passed, 1 skipped
```

## Wegweiser
- Regeln + Owner-Grenzen: [`CLAUDE.md`](CLAUDE.md)
- Start je Owner: [`Handoff/`](Handoff/) · Onboarding: [`docs/ONBOARDING.md`](docs/ONBOARDING.md)
- Contracts: [`docs/CONTRACTS.md`](docs/CONTRACTS.md) · Status-Board: [`docs/PROGRAMM_NOTBELEUCHTUNG.md`](docs/PROGRAMM_NOTBELEUCHTUNG.md)
- Port-Herkunft: [`docs/PORT_LOG.md`](docs/PORT_LOG.md) · Infrastruktur: [`docs/INFRASTRUKTUR.md`](docs/INFRASTRUKTUR.md)

## Status
Slice 0 — Repo-Skelett + 3 Contracts + Fake-Provider-Durchstich (grün). Echte
Provider parallel: Enis (Slice 1, Norm+LB) · Leonis (Slice 2, Platzierung + Render)
· Selman (Slice 4, Raumerkennung) → E2E + FastAPI (Slice 5) → Chat-Interface (Slice 6).
