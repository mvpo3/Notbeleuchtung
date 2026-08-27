# Notbeleuchtung

Architektplan (DXF) → ÖNorm-konforme **Notbeleuchtung** (EN 1838) → DXF/PDF.

3-Owner-Contract-Architektur (Dependency-Inversion): die Hauptengine besitzt die
Contracts, Selman/Leonis/Enis implementieren je ein Protocol.

```
Selman: RaumProvider ─► RaumModell ─┐
                                     ├─► Leonis: Platzierer(Raum, Norm) ─► PlatzierungsErgebnis ─► Render → DXF
Enis:   NormProvider ─► NormRegelwerk┘
```

## Quickstart

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -e ".[dev]"
.venv/Scripts/python.exe -m pytest -q
```

Details: [`CLAUDE.md`](CLAUDE.md) · Status: [`docs/PROGRAMM_NOTBELEUCHTUNG.md`](docs/PROGRAMM_NOTBELEUCHTUNG.md)
· Contracts: [`docs/CONTRACTS.md`](docs/CONTRACTS.md) · Port-Herkunft: [`docs/PORT_LOG.md`](docs/PORT_LOG.md)

## Status

Slice 0 — Repo-Skelett + 3 Contracts + Fake-Provider-Durchstich (grün). Echte
Provider folgen: Enis (Slice 1) → Leonis (Slice 2) → Render (Slice 3) → Selman
(Slice 4) → E2E + API (Slice 5).
