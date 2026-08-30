# COORDINATION — 2-Fenster-Parallelbetrieb

**Zweck:** Zwei Claude-Code-Sessions arbeiten parallel in getrennten Worktrees. Diese
Datei ist das gemeinsame Board — **beide Fenster lesen + pflegen sie**. Da Sessions
keinen Live-Speicher teilen, läuft die Kommunikation über **Git** + diese Datei.

## Aufteilung (kein Datei-Overlap)

| Fenster | Ordner | Branch | Bereich |
|---|---|---|---|
| **F1** | `Notbeleuchtung/` | `leonis/anker-platzierer` | `src/notbeleuchtung/platzierung/` + `hauptengine/` — Platzier-Pipeline (Anker/Linie/Fläche/Deckung) |
| **F2** | `Notbeleuchtung-F2/` | `leonis/ldt-photometrie` | `src/notbeleuchtung/normwissen/photometrie/` — (b) IES/LDT-Import → exakte Lux |

## Regeln (bindend)
- **Eigenes Package = frei** parallel bearbeiten.
- **`hauptengine/contracts/**` = Konsens** (Contract-Freeze-Regel, beide Fenster + Version-Bump). Wer einen Contract ändern will → hier eintragen + abwarten.
- **Kleine Commits**, eine Sache pro Commit. Nach jedem Schritt Status unten aktualisieren + committen.
- **Sync:** `git fetch` + `git show origin/<other-branch>:docs/COORDINATION.md` (oder Board unten lesen). Das andere Fenster sieht Änderungen erst nach Fetch/Pull.
- **Naht/Lux:** F2 liefert `photometrie`-API; F1 konsumiert sie später in `platzierung/lux.py`. Schnittstelle unten festhalten, bevor F1 sie einbaut.

## Schnittstelle F2 → F1 (Lux-Photometrie)
F2 baut: `normwissen/photometrie/ldt.py` mit
`lade_ldt(pfad) -> Photometrie` und `Photometrie.intensitaet(gamma_grad, c_grad) -> cd`.
F1 tauscht dann in `platzierung/lux.py` das konstante `i_cd` gegen `Photometrie.intensitaet`.
**Contract bleibt unberührt** (rein additives Modul). → wenn API steht, hier „READY" markieren.

**READY** (F2, 2026-08-30): `normwissen/photometrie/{ldt.py,__init__.py}` steht.
`lade_ldt(pfad) -> Photometrie` (EULUMDAT, alle Isym-Symmetrien) +
`Photometrie.intensitaet(gamma_grad, c_grad=0.0) -> cd` (bilinear γ×C, cd über
`lampen_lumen` skaliert). F1 kann `lux.py` umstellen. Noch offen: Test gegen echte
Schrack-LDT (Owner besorgt Datei) — bis dahin synthetische Fixture `tests/fixtures/photometrie/mini.ldt`.

## Status-Board (live — nach jedem Schritt updaten + committen)

### F1 (Platzierung)
- [x] (a) Anker-Platzierer (`anker_strategy`) — committed
- [x] (b-vorbereitet) `mittellinie` + `lux` — committed
- [x] (c) `place()` Durchstich Anker→Linie→Fläche→Deckung (`deckung.py`) — committed
- [x] `lux.py`/`deckung.py` auf F2-Photometrie umstellbar: neues `i_cd_fn(γ)`-Callable
  (Dependency-Injection, KEIN `normwissen`-Import → Import-Grenze gewahrt); Hauptengine
  baut es aus `Photometrie.intensitaet`. Fallback bleibt konstant `i_cd`. (Branch `leonis/lux-photometrie`)
- [ ] offen: PR für anker-platzierer-Branch; Hauptengine/pipeline: `i_cd_fn` real verdrahten

### F2 (Photometrie / LDT)
- [x] `normwissen/photometrie/ldt.py` — LDT/EULUMDAT-Parser (Kopf + Lampensatz + Isym-Expansion)
- [x] `Photometrie.intensitaet(gamma, c)` mit Winkel-Interpolation (bilinear γ×C, periodisch)
- [ ] Test gegen eine echte Schrack-LDT (Owner besorgt Datei) — bis dahin synthetische Fixture
- [x] API READY-Meldung hier → F1 baut sie in `lux.py` ein

## Log (append-only, neueste oben)
- 2026-08-30 F1-Naht: `lux.py`+`deckung.py` bekommen `i_cd_fn(γ)`-Callable (Photometrie-Injektion, grenz-sauber). 77 Tests grün. Verdrahtung in Hauptengine/pipeline noch offen.
- 2026-08-30 F2: `photometrie/ldt.py` + `__init__.py` + Fixture `mini.ldt` + `tests/normwissen/test_ldt.py`. 74 Tests grün, ruff clean. Schnittstelle READY (siehe oben).
- <setup> F1 legt Worktree + dieses Board an. F2 startet mit (b) LDT.
