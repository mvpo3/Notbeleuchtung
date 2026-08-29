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

## Status-Board (live — nach jedem Schritt updaten + committen)

### F1 (Platzierung)
- [x] (a) Anker-Platzierer (`anker_strategy`) — committed
- [x] (b-vorbereitet) `mittellinie` + `lux` — committed
- [x] (c) `place()` Durchstich Anker→Linie→Fläche→Deckung (`deckung.py`) — committed
- [ ] offen: PR für anker-platzierer-Branch; ggf. `lux.py` auf F2-Photometrie umstellen (nach READY)

### F2 (Photometrie / LDT)
- [ ] `normwissen/photometrie/ldt.py` — LDT/EULUMDAT-Parser
- [ ] `Photometrie.intensitaet(gamma, c)` mit Winkel-Interpolation
- [ ] Test gegen eine echte Schrack-LDT (Owner besorgt Datei)
- [ ] API READY-Meldung hier → F1 baut sie in `lux.py` ein

### F2 → umgelenkt auf Raumerkennung (Selman-Package)
Branch `selman/raumerkennung-dxf`. Baut echten `ArchitekturRaumProvider.parse(dxf, floor)
-> RaumModell` (ersetzt `FakeRaumProvider` schrittweise). Schlanker Neubau in
`raumerkennung/`, wiederverwendet pure Port-Helfer (`room_faces`, `classify_room`).
Primärziel Mollgasse (mm). **Kein Contract-Touch** (rein additiv). E2E bleibt vorerst
auf Fake (4OG-Golden matcht keinen echten DXF) — Fake-Swap = späterer Slice mit F1-Konsens.
- [x] S0 Scaffold (`provider.py` Stub, `tests/raumerkennung/`) — Suite grün (69), committed
- [ ] S1 dxf_load · [ ] S2 waende→räume · [ ] S3 raumtyp · [ ] S4 tueren · [ ] S5 zirkulation · [ ] S6 provider full → READY

## Log (append-only, neueste oben)
- <S0> F2 umgelenkt → Raumerkennung. Branch `selman/raumerkennung-dxf`, Scaffold + Test grün (69 passed).
- <setup> F1 legt Worktree + dieses Board an. F2 startet mit (b) LDT.
