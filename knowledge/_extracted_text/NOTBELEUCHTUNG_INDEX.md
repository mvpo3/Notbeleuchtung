# Notbeleuchtungs-Index über den elektro-planer-Rohimport

Dieser Ordner (`knowledge/_extracted_text/`) ist der **komplette** Wissens-Rohimport
aus dem elektro-planer-Projekt: ~1140 extrahierte Dokumente (Volltext + vorgefertigte
Teil-Digests) über Normen, Bücher und Hersteller-Kataloge. Der Großteil betrifft
allgemeine Elektroplanung (Blitzschutz, RCD/AFDD, Antennen, Netzwerk, PV …) und ist
für dieses Projekt **nicht** relevant.

Dieser Index kartiert die **Notbeleuchtungs-relevante Teilmenge**, damit der Kontext
auffindbar bleibt. Die daraus verdichteten fokussierten Digests liegen in
`../extracted/aus_elektroplaner/` (dort auch die Erkenntnis-Zusammenfassung).

## Ordnerstruktur

- `normen/` — 167 Norm-/Rechts-Volltexte (`===== PAGE n =====`-Marker)
- `buecher/` — 20 Bücher/Hersteller-Kataloge (Volltext)
- `digests/normen/`, `digests/buecher/` — 572 vorgefertigte Teil-Digests (`.partN.md`)
  aus dem elektro-planer-Projekt (allgemein-elektrisch fokussiert, nicht Notlicht)
- `_chunks/` — 375 Roh-Chunks
- `manifest.json`, `chunks_manifest.json` — Metadaten (Seiten, Zeichen, Pfade)

## Notbeleuchtungs-relevante Primärquellen (nach Relevanz)

| Datei | Thema | verdichtet in |
|-------|-------|---------------|
| `buecher/k-sibe-at9.txt` (400 S.) | **Schrack Not-/Sicherheitsbeleuchtungs-Katalog** — Leuchtenfamilien, Erkennungsweiten, Batteriesysteme | ✅ [Schrack_Katalog](../extracted/aus_elektroplaner/Schrack_Katalog_NotSicherheitsbeleuchtung.md) |
| `normen/OVE E8101_2025.txt` (852 S.) | **OVE E 8101:2025** aktuelle Errichtungsnorm | ✅ [E8101-2025-Deltas](../extracted/aus_elektroplaner/OVE_E_8101_2025_Deltas.md) (Δ zu 2019) |
| `normen/OVE E 8101_2019.txt` | OVE E 8101:2019 | ✅ [OVE_E_8101](../extracted/OVE_E_8101_niederspannungsanlagen.md) (Haupt-Digest) |
| `normen/OEVE_OENORM_E_8002-1…9.txt` | **E 8002** Sicherheitsstrom für Menschenansammlungen | ✅ [E_8002](../extracted/aus_elektroplaner/OENORM_E_8002_Menschenansammlungen.md) |
| `normen/OEVE_OENORM_E_8007(_A1/_A2).txt` | **E 8007** medizinisch (SV-Klassen) | ✅ [E_8007](../extracted/aus_elektroplaner/OENORM_E_8007_medizinisch.md) |
| `normen/EN 1838 - Notbeleuchtung 2019.txt` | **EN 1838** Kernnorm | ✅ [EN_1838](../extracted/EN_1838_notbeleuchtung.md) |
| `normen/Fachinfo_E-05/E-06/E-07…txt` | OVE-Fachinfos Sicherheitsbeleuchtung | ✅ [Fachinfos_E05-07](../extracted/aus_elektroplaner/OVE_Fachinfos_E05_E06_E07.md) |
| `normen/Fachinfo_E-08…txt` | OVE-Fachinfo Arbeitsstätten (AStV §9) | ✅ [Fachinfo_E08](../extracted/Fachinfo_E08_Arbeitsstaetten.md) |
| `normen/OEVE-EN_7.txt` (1991) | Vorgänger-Norm (medizinisch/Sicherheit), OCR-teilzerstört, **superseded** | ⚠️ nur historisch — nicht verdichtet |
| `buecher/k-sort-a20.txt` (1568 S.) | Schrack Gesamtsortiment; Sicherheitsbeleuchtungs-Teil **redundant** zu k-sibe | ⚠️ redundant — nicht separat verdichtet |

Vorgefertigte elektro-planer-Teil-Digests dieser Quellen liegen unter
`digests/normen/` bzw. `digests/buecher/` (z.B. `k-sibe-at9.part0…9.md`,
`OVE E8101_2025.part0…21.md`, `OEVE_OENORM_E_8002-*.partN.md`).

## Nicht relevant (Beispiele, nicht übernommen)

Blitzschutz-Fachinfos, RCD/AFDD-Anwendung (IS-02/IS-03), Antennen (BL-02),
Überspannungsschutz, Nullung, ETG/ETV/ESV (Rechtsrahmen bereits in `../extracted/`),
Hochspannung (R 1000-3), Gebäudetechnik-/CAD-/BIM-Bücher, CCTV/Sprechanlagen-Kataloge.

## Wartung

Kommen neue Quellen dazu, nach demselben Muster verdichten →
`../extracted/aus_elektroplaner/` + diese Tabelle ergänzen.
