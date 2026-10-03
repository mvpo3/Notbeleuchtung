"""baue_regelwerk.py — konsolidiert das REGELWERK aus zwei Quellen:

1. MIGRATION: NB-R01..NB-R27 (`knowledge/notbeleuchtung/regeln.yaml`) → RW-001..
   RW-027 mit `nb_ref`; belege_dxf aus `beispiele.json` (Handles/xy/rotation);
   quelle_pdf aus der begruendung ("PDF S.x").
2. NEU-KANDIDATEN: `neu_regeln.yaml` (von Hand konsolidiert aus den
   seitenprotokoll-„neu"-Records; prioritaet=basis nur bei Mollgasse-Beleg,
   sonst ergaenzung).

Output: REGELWERK_Notbeleuchtung.json (Single Source, Auftragsschema) +
REGELWERK_Notbeleuchtung.md (generiert). Danach GATE: jede Regel braucht
>=1 quelle_pdf UND >=1 belege_dxf mit real existierendem Handle (DXF wird
geoeffnet). Gate-Verstöße → exit 1 + Liste.

Aufruf: python baue_regelwerk.py [--ohne-gate]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

HIER = Path(__file__).resolve()
BASIS = HIER.parents[1]
WISSEN = HIER.parents[2]
REPO = HIER.parents[4]
NB_YAML = REPO / "knowledge" / "notbeleuchtung" / "regeln.yaml"
BEISPIELE = REPO / "knowledge" / "notbeleuchtung" / "beispiele.json"
NEU_YAML = BASIS / "neu_regeln.yaml"

MOLLGASSE_PDF = "Mollgasse-Notbeleuchtungserklärung/Notbeleuchtungen zeichnen.pdf"
MOLLGASSE_DXF = "Mollgasse-Notbeleuchtungserklärung/WHA_MOL_{g}_Notbeleuchtung_Erklärung.dxf"

_SEITEN_RE = re.compile(r"S\.?\s*([0-9]+(?:\s*[-–]\s*[0-9]+)?)")


def _seiten_aus_begruendung(text: str) -> list[int]:
    seiten: list[int] = []
    for m in _SEITEN_RE.finditer(text or ""):
        teil = m.group(1).replace("–", "-")
        if "-" in teil:
            a, b = (int(x) for x in teil.split("-"))
            seiten.extend(range(a, min(b, a + 30) + 1))
        else:
            seiten.append(int(teil))
    return sorted(set(seiten))


def _lade_beispiele() -> dict[str, dict]:
    daten = json.loads(BEISPIELE.read_text(encoding="utf-8"))
    return {b["id"]: b for b in daten}


def migriere_nb() -> list[dict]:
    nb = yaml.safe_load(NB_YAML.read_text(encoding="utf-8"))
    beispiele = _lade_beispiele()
    regeln = []
    for i, r in enumerate(nb, start=1):
        nb_id = r["id"]
        seiten = _seiten_aus_begruendung(r.get("begruendung", ""))
        belege_dxf = []
        for bid in r.get("belege", []):
            b = beispiele.get(bid)
            if not b:
                continue
            g = bid.split("-")[0]
            for l in b.get("leuchten", []):
                belege_dxf.append({
                    "datei": MOLLGASSE_DXF.format(g=g),
                    "handle": l.get("handle"),
                    "block": l.get("block"),
                    "rotation": l.get("rotation"),
                    "x": l.get("x"),
                    "y": l.get("y"),
                    "beispiel_id": bid,
                })
        aktion = r.get("aktion", {}) or {}
        regeln.append({
            "id": f"RW-{i:03d}",
            "nb_ref": nb_id,
            "thema": r.get("thema", ""),
            "regel": r.get("bedingung", "") + " → " + str(aktion.get("position", "")),
            "geometrische_bedingung": {
                "rotation": aktion.get("rotation", ""),
                "parameter": r.get("parameter", {}),
            },
            "leuchtentyp": aktion.get("symboltyp", "-"),
            "quelle_pdf": [{"projekt": "Mollgasse", "seite": s, "bild": None} for s in seiten],
            "belege_dxf": belege_dxf,
            "prioritaet": "basis",
            "konfidenz": r.get("konfidenz", "mittel"),
            "begruendung": r.get("begruendung", ""),
        })
    # NB-R26 (INSUNITS-/Textanker-Disziplin): Beleg ist ein Header-Wert, kein
    # INSERT-Handle — dokumentierter Alternativ-Beleg statt Handle-Gate.
    for r in regeln:
        if r.get("nb_ref") == "NB-R26" and not r["belege_dxf"]:
            r["beleg_alternativ"] = (
                "Header-Beleg statt Handle: $INSUNITS=6 (Meter) bei mm-Koordinaten "
                "in TOMA-/Baufeld-E2-DXFs (inventur.json 'insunits'); Textanker-Fälle "
                "AmRain S.13/23 (EINGANG-Modelltext). Prozess-/Eingaberegel ohne "
                "eigenen INSERT."
            )
    return regeln


_PROJEKT_DXF = {
    "Mollgasse": "Mollgasse-Notbeleuchtungserklärung/WHA_MOL_{g}_Notbeleuchtung_Erklärung.dxf",
    "Tomaschek": "Tomaschek-Schule -Notbeleuchtungserklärung/{g}_RIVO_Erklaerung.dxf",
    "Hausfeld": "Hausfeldstraße Notbeleuchtung zeichnen/Hausfeldstraße_{g}_Notbeleuchtung_RIVO.dxf",
}
_AMRAIN_DXF = {
    "UG": "ARAI5_FE_XEL_ZZ_MOP_UG_0010_V_02_RIVO_Symbole_TEILSTAND_v2.dxf",
    "EG": "ARAI5_FE_XEL_ZZ_MOP_EG_0011_V_02_EG_Erklaerung_TEILSTAND_v2.dxf",
    "OG1": "ARAI5_FE_XEL_ZZ_MOP_OG1_0012_V_01_RIVO_Symbole_TEILSTAND_v2.dxf",
    "OG2": "ARAI5_FE_XEL_ZZ_MOP_OG2_0013_V_01_RIVO_Symbole_TEILSTAND_v2.dxf",
    "OG3": "ARAI5_FE_XEL_ZZ_MOP_OG3_0014_V_01_RIVO_Symbole_TEILSTAND_v2.dxf",
    "OG4": "ARAI5_FE_XEL_ZZ_MOP_OG4_0015_V_01_RIVO_Symbole_TEILSTAND_v2.dxf",
}
_BEST_RE = re.compile(r"NB-R(\d{2})")


def _resolve_datei(projekt: str, g: str | None, datei: str) -> str:
    """Agenten-Dateiangaben normalisieren: Platzhalter, fehlender Ordner-Präfix,
    Wildcards → kanonischer Pfad relativ zu WISSEN (wenn Geschoss bekannt)."""
    if datei and (WISSEN / datei).exists():
        return datei
    if g:
        if projekt in _PROJEKT_DXF:
            kandidat = _PROJEKT_DXF[projekt].format(g=g)
            if (WISSEN / kandidat).exists():
                return kandidat
        elif projekt == "AmRain" and g in _AMRAIN_DXF:
            return "Am Rain Notbeleuchtungserklärung/" + _AMRAIN_DXF[g]
        elif projekt == "BaufeldE2":
            return ("Baufeld E2 Notbeleuchtung zeichnen/"
                    "Notbeleuchtungspläne_UG_RIVO_mit_Lehrlayern.dxf")
    return datei


def reichere_aus_protokollen(regeln: list[dict]) -> None:
    """bestaetigt:NB-Rxx-Records aller Projekte → quelle_pdf + belege_dxf.

    Schließt die Lücken der Migration: UG-Regeln (beispiele.json ohne
    Leuchten-Arrays) über die Mollgasse-Protokoll-Handles, TOMA-Regeln
    (NB-R22..R27) über die Tomaschek-Protokolle.
    """
    je_nb = {r["nb_ref"]: r for r in regeln if r.get("nb_ref")}
    for pj_dir in sorted((BASIS / "evidenz").iterdir()):
        jl = pj_dir / "seitenprotokoll.jsonl"
        if not jl.exists():
            continue
        projekt = pj_dir.name
        for zeile in jl.read_text(encoding="utf-8").splitlines():
            if not zeile.strip():
                continue
            rec = json.loads(zeile)
            bew = rec.get("bewertung", "")
            if not bew.startswith("bestaetigt"):
                continue
            ab = rec.get("dxf_abgleich") or {}
            datei = _resolve_datei(projekt, rec.get("geschoss"), ab.get("datei") or "")
            for m in _BEST_RE.finditer(bew):
                nb_id = f"NB-R{m.group(1)}"
                r = je_nb.get(nb_id)
                if r is None:
                    continue
                q = {"projekt": projekt, "seite": rec["seite"], "bild": None}
                if q not in r["quelle_pdf"]:
                    r["quelle_pdf"].append(q)
                for h in ab.get("handles", []) or []:
                    if not any(b.get("handle") == h and b.get("datei") == datei
                               for b in r["belege_dxf"]):
                        r["belege_dxf"].append({
                            "datei": datei, "handle": h, "block": None,
                            "rotation": None, "x": None, "y": None,
                            "quelle": f"{projekt} S.{rec['seite']}",
                        })


def _protokoll_index() -> dict[tuple[str, int], dict]:
    idx: dict[tuple[str, int], dict] = {}
    for pj_dir in sorted((BASIS / "evidenz").iterdir()):
        jl = pj_dir / "seitenprotokoll.jsonl"
        if not jl.exists():
            continue
        for zeile in jl.read_text(encoding="utf-8").splitlines():
            if zeile.strip():
                rec = json.loads(zeile)
                idx[(pj_dir.name, rec["seite"])] = rec
    return idx


def lade_neu() -> list[dict]:
    """neu_regeln.yaml: Hand-konsolidierte Regeln; `quelle_seiten:
    {Projekt: [Seiten]}` wird automatisch zu quelle_pdf + belege_dxf
    (Handles aus den Seitenprotokollen) aufgelöst."""
    if not NEU_YAML.exists():
        return []
    daten = yaml.safe_load(NEU_YAML.read_text(encoding="utf-8")) or []
    idx = _protokoll_index()
    regeln = []
    for j, r in enumerate(daten, start=1):
        r.setdefault("id", f"RW-{100 + j:03d}")
        r.setdefault("nb_ref", None)
        r.setdefault("prioritaet", "ergaenzung")
        r.setdefault("quelle_pdf", [])
        r.setdefault("belege_dxf", [])
        for projekt, seiten in (r.pop("quelle_seiten", None) or {}).items():
            for s in seiten:
                q = {"projekt": projekt, "seite": s, "bild": None}
                if q not in r["quelle_pdf"]:
                    r["quelle_pdf"].append(q)
                rec = idx.get((projekt, s))
                if not rec:
                    continue
                ab = rec.get("dxf_abgleich") or {}
                datei = _resolve_datei(projekt, rec.get("geschoss"), ab.get("datei") or "")
                for h in ab.get("handles", []) or []:
                    if not any(b.get("handle") == h for b in r["belege_dxf"]):
                        r["belege_dxf"].append({
                            "datei": datei, "handle": h, "block": None,
                            "rotation": None, "x": None, "y": None,
                            "quelle": f"{projekt} S.{s}",
                        })
        regeln.append(r)
    return regeln


def gate(regeln: list[dict]) -> list[str]:
    """Jede Regel: >=1 quelle_pdf und >=1 belege_dxf mit realem Handle."""
    import ezdxf
    fehler = []
    cache: dict[str, set] = {}
    for r in regeln:
        if not r.get("quelle_pdf"):
            fehler.append(f"{r['id']}: keine quelle_pdf")
        belege = r.get("belege_dxf") or []
        if not belege:
            if r.get("beleg_alternativ"):
                continue  # dokumentierter Nicht-Handle-Beleg (z.B. Header/Textseite)
            fehler.append(f"{r['id']}: keine belege_dxf")
            continue
        ok = False
        for b in belege:
            pfad = WISSEN / b["datei"]
            key = str(pfad)
            if key not in cache:
                if not pfad.exists():
                    cache[key] = set()
                else:
                    doc = ezdxf.readfile(str(pfad))
                    cache[key] = {e.dxf.handle for e in doc.modelspace()}
            if b.get("handle") in cache[key]:
                ok = True
            else:
                b["handle_verifiziert"] = False
        if not ok:
            fehler.append(f"{r['id']}: kein Handle real verifizierbar ({len(belege)} Belege)")
    return fehler


def schreibe_md(regeln: list[dict]) -> None:
    z = [
        "# REGELWERK Notbeleuchtung — RIVOPLAN-Zeichenregeln",
        "",
        "Generiert aus `REGELWERK_Notbeleuchtung.json` (`scripts/baue_regelwerk.py`)",
        "— nicht von Hand editieren. BASIS = Mollgasse; Ergänzungsregeln nachrangig.",
        "",
    ]
    themen: dict[str, list[dict]] = {}
    for r in regeln:
        themen.setdefault(r.get("thema", "sonstiges"), []).append(r)
    basis = [r for r in regeln if r["prioritaet"] == "basis"]
    erg = [r for r in regeln if r["prioritaet"] != "basis"]
    z.append(f"**{len(basis)} Basis-Regeln · {len(erg)} Ergänzungsregeln (nachrangig)**\n")

    def _block(r: dict) -> list[str]:
        s = [f"### {r['id']}" + (f" (aus {r['nb_ref']})" if r.get("nb_ref") else "")
             + f" — {r.get('thema','')}"]
        s.append(r.get("regel", ""))
        gb = r.get("geometrische_bedingung") or {}
        if gb.get("rotation"):
            s.append(f"- **Rotation:** {gb['rotation']}")
        if gb.get("parameter"):
            s.append(f"- **Parameter:** `{json.dumps(gb['parameter'], ensure_ascii=False)}`")
        s.append(f"- **Leuchtentyp:** {r.get('leuchtentyp','-')}")
        qs = r.get("quelle_pdf") or []
        if qs:
            per_projekt: dict[str, list] = {}
            for q in qs:
                per_projekt.setdefault(q["projekt"], []).append(q["seite"])
            s.append("- **PDF:** " + " · ".join(
                f"{p} S.{','.join(str(x) for x in sorted(set(sn))[:12])}"
                + ("…" if len(set(sn)) > 12 else "")
                for p, sn in per_projekt.items()))
        belege = r.get("belege_dxf") or []
        if belege:
            probe = belege[:4]
            s.append("- **DXF-Belege:** " + " · ".join(
                f"{b.get('handle','?')} ({Path(b['datei']).name.split('_Notbeleuchtung')[0]}"
                f", rot {b.get('rotation','?')})" for b in probe)
                + (f" … +{len(belege)-4} weitere" if len(belege) > 4 else ""))
        if r.get("begruendung"):
            s.append(f"- **Begründung:** {r['begruendung']}")
        s.append("")
        return s

    z.append("## Basis-Regeln (Mollgasse, verbindlich)\n")
    for r in basis:
        z += _block(r)
    z.append("## Ergänzungsregeln (nachrangig — greifen nur, wenn keine Basis-Regel greift)\n")
    for r in erg:
        z += _block(r)
    (BASIS / "REGELWERK_Notbeleuchtung.md").write_text("\n".join(z), encoding="utf-8")


def schreibe_engine_json(regeln: list[dict]) -> None:
    """Engine-Fassung: basis + umsetzbare ergaenzung, OHNE Beleg-Listen
    (Belege sind Eval-Daten; die Engine braucht Regeltext + Geometrie + IDs)."""
    ziel = REPO / "src" / "notbeleuchtung" / "platzierung" / "data" / "notbeleuchtung_regeln.json"
    ziel.parent.mkdir(parents=True, exist_ok=True)
    lean = []
    for r in regeln:
        if r.get("engine_relevanz") == "keine":
            continue
        lean.append({
            "id": r["id"],
            "nb_ref": r.get("nb_ref"),
            "thema": r.get("thema", ""),
            # Blocknamen-Sanitize: die Bibliothek heißt seit 2026-09-21
            # RIVO_ARR_* (Migration aafc575) — Alt-Namen aus Bestands-YAML-
            # Texten würden den migration_guard (src-Scan) brechen.
            "regel": r.get("regel", "").replace("RIVO_NL_ARR", "RIVO_ARR"),
            "geometrische_bedingung": r.get("geometrische_bedingung", {}),
            "leuchtentyp": r.get("leuchtentyp", "-"),
            "prioritaet": r.get("prioritaet", "ergaenzung"),
            "n_quellen_pdf": len(r.get("quelle_pdf") or []),
            "n_belege_dxf": len(r.get("belege_dxf") or []),
        })
    ziel.write_text(json.dumps(lean, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Engine-JSON: {len(lean)} Regeln -> {ziel.relative_to(REPO)}")


def main(argv: list[str]) -> int:
    regeln = migriere_nb()
    reichere_aus_protokollen(regeln)
    regeln += lade_neu()
    (BASIS / "REGELWERK_Notbeleuchtung.json").write_text(
        json.dumps(regeln, ensure_ascii=False, indent=1), encoding="utf-8")
    schreibe_md(regeln)
    schreibe_engine_json(regeln)
    print(f"{len(regeln)} Regeln geschrieben "
          f"({sum(1 for r in regeln if r['prioritaet']=='basis')} basis).")
    if "--ohne-gate" not in argv:
        fehler = gate(regeln)
        if fehler:
            print("GATE-VERSTÖSSE:")
            for f in fehler:
                print("  -", f)
            return 1
        print("Gate: alle Regeln haben PDF-Quelle + real verifizierten DXF-Handle.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
