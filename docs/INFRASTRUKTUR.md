# Infrastruktur — Entscheidung (Stand 2026-08-27)

**Leitsatz:** Infra folgt der Phase, nicht dem Hype. Solange die Engine gebaut
wird, brauchen wir **keine** Cloud/DB. Erst beim Ausliefern kommt Server dazu,
Datenbank noch später.

## Was die Engine ist
**Stateless Compute:** `pipeline.run(architekturplan_dxf, lb) → Notbeleuchtungsplan
(DXF/PDF)`. Kein User-State, keine DB nötig für den Kern. DXF-Parsing/-Generieren
ist **schwer + langsam** (ezdxf auf bis zu ~95-MB-Plänen, shapely, Sekunden–Minuten
pro Plan, viel RAM).

## Phasen-Fahrplan

| Phase | Was läuft | Infra |
|-------|-----------|-------|
| **Engine bauen** (Slice 0–5) | Contracts, Provider, Render, E2E | **Nichts** — lokal (Python-venv) + GitHub-CI. Infra jetzt = Ballast (YAGNI). |
| **Erster Demo-Deploy** (Slice 6, Chat) | FastAPI + Engine hinter `POST /plan`, dünnes Chat-Frontend | **1× Hetzner-VM.** Kein DB. Uploads/Outputs auf lokaler Disk / temp. |
| **Echtes Produkt** | Accounts, gespeicherte Projekte, Chat-History, Pricing/Billing | **+ Supabase** (Postgres + Auth + Storage) — erst wenn ein Feature es verlangt. |

## Begründungen

**Server = Hetzner (VM), nicht Serverless.**
- Serverless (Vercel-Functions/Lambda) hat Zeit-/Memory-Limits → große DXF-Läufe
  sterben. Wir brauchen eine echte VM mit RAM + Laufzeit.
- Hetzner: billig, stark, **EU/DE-Standort** → Datenresidenz für österreichische
  Baupläne (oft proprietär/DSGVO-relevant) ist ein echter Vorteil ggü. US-Cloud.

**Supabase = erst bei Zustand.**
- Zustandsloser MVP („Plan hoch → verarbeiten → runter") braucht **keine** DB.
- Supabase kommt, sobald: Login/Accounts, gespeicherte Projekte, Chat-History,
  Abrechnung. Dann spart es eigenen Auth-Bau (Postgres + Auth + Storage in einem).
- **Aufschieben** bis dahin — nicht vorbauen.

**Frontend-Hosting (Chat-UI).**
- Statische Seite → Vercel/Netlify/Cloudflare **oder** einfach vom Hetzner-Server
  mitliefern. Klein, später entscheiden.

## Faustregel
```
Engine bauen        → nichts (lokal + GitHub)
Erster Demo-Deploy  → 1× Hetzner-VM (FastAPI + Engine), kein DB
Echtes Produkt      → + Supabase (Auth/Projekte/History/Billing) wenn nötig
```

## Offen (entscheiden wenn Deploy näher rückt)
- Genaue Hetzner-Größe (CPU/RAM) — abhängig von Plan-Größen + Parallel-Last.
- Job-Modell: synchron (Request wartet) vs. Queue/Worker (bei langen Läufen).
- Frontend-Owner (die 3 Owner sind Backend) — siehe `PROGRAMM_NOTBELEUCHTUNG.md`.
