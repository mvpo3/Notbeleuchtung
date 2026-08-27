# Contracts — menschenlesbare Spezifikation

Code = Wahrheit (`src/notbeleuchtung/hauptengine/contracts/*.py`, Pydantic).
JSON-Schema generiert nach `contracts/schema/`. Dieses Doc = Prosa-Referenz.

## RaumModell (Selman → Engine)
Reine Geometrie/Topologie, kein Norm-Urteil.
- `floor`, `coordinate_system="mm"`, `bounds_mm`
- `raeume[]`: `id, raum_typ, polygon_mm, flaeche_m2, ist_fluchtweg, ist_communal`
- `tueren[]`: `id, xy_mm, breite_mm, von_raum, nach_raum, ist_notausgang, schwenk_richtung`
- `ausgaenge[]`: `id, xy_mm, typ ∈ {final_exit, stair_exit, door}`
- `zirkulation`: `nodes[], edges[], segmente[]`
  - `segment`: `segment_id, polyline_mm, laenge_mm, reason ∈ {exit, corner, long_run, direction_change}`
  - `segment_id` = Verankerungs-Schlüssel für Leonis.

## NormRegelwerk (Enis → Engine) — Query-API
Leonis FRAGT, parst nie YAML. `NormProvider`:
- `fuer_raum(raum_typ, ist_fluchtweg) → NormAnforderung`
- `fuer_fluchtweg_abschnitt(segment) → NormAnforderung`
- `erkennungsweite_m(piktogramm_hoehe_m, hinterleuchtet) → float`  (l = z·h, z=200/100)
- `regelwerk_snapshot() → NormRegelwerk`

`NormAnforderung`: `min_lux (1.0 Rettungsweg / 0.5 Antipanik), klassifikation ∈
{rz, antipanik, sicherheitsleuchte}, montagehoehe_mm (≥2000), erkennungsweite_m,
symbol_katalog_keys[], mindest_anzahl (RZ=2), dauer_min (60), quelle`.

## PlatzierungsErgebnis (Leonis → Engine)
- `platzierungen[]`: `xy_mm, catalog_key, rotation_deg, mirror_x, height_mm,
  kind ∈ {rz, sicherheitsleuchte, antipanik}, richtung, circuit_hint,
  covers_segment[], norm_quelle`

## Naht-Invarianten (CI-Gate)
- `covers_segment ∈ RaumModell.zirkulation.segmente[].segment_id`
- `norm_quelle ∈ NormRegelwerk.quellen`
- `catalog_key ∈ schrack_symbol_mapping.yaml` (aktiv ab Slice 2/3)
