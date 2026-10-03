# -*- coding: utf-8 -*-
"""gen_fallbeispiele_md.py — FALLBEISPIELE_REVIEW.md aus evidenz/fallbeispiele.json
(Ultracode-Workflow 2026-09-30: 8 Finder → Dedupe → adversarialer DXF-Verifikator
je Fall → Engine-Richter je Fall; 90 Agenten)."""
from __future__ import annotations

import json
from pathlib import Path

HIER = Path(__file__).resolve()
ANALYSE = HIER.parents[1]

URTEIL_LABEL = {
    "richtig": "✅ Engine wählt RICHTIG",
    "falsche_variante": "❌ Engine wählt die FALSCH-Variante",
    "position_daneben": "📍 richtig, aber Position daneben",
    "nicht_platziert": "⬜ Engine setzt hier NICHTS",
    "unentscheidbar": "❔ unentscheidbar",
    None: "— (nicht DXF-bestätigt, kein Urteil)",
}


def main() -> int:
    obj = json.loads((ANALYSE / "evidenz" / "fallbeispiele.json").read_text(encoding="utf-8"))
    faelle = obj["faelle"]
    from collections import Counter
    c = Counter((f.get("urteil") or {}).get("engine_verhalten") for f in faelle)
    z = [
        "# FALLBEISPIELE-REVIEW — Warum diese Leuchte und keine andere (Ultracode-Pass)",
        "",
        "Erhebung 2026-09-30, Multi-Agent-Workflow (90 Agenten): 8 Seiten-Jäger über",
        "alle 95 Seiten → Dedupe → je Fall ein ADVERSARIALER DXF-Verifikator (Auftrag:",
        "widerlegen!) → je bestätigtem Fall ein Engine-Richter gegen ENGINE_WISSEN_IST",
        "+ den echten Validierungslauf. Rohdaten: `evidenz/fallbeispiele.json`.",
        "",
        f"**{obj['n_faelle']} Fallbeispiele** (aus {obj['n_kandidaten']} Kandidaten) · "
        f"**{obj['n_bestaetigt']} im DXF mm-genau bestätigt** · Engine-Urteile: "
        f"{c.get('richtig',0)}× richtig · {c.get('falsche_variante',0)}× falsche Variante · "
        f"{c.get('position_daneben',0)}× Position daneben · "
        f"{c.get('nicht_platziert',0)}× nicht platziert · "
        f"{sum(v for k,v in c.items() if k is None)}× ohne Urteil (Verifikator nicht überzeugt).",
        "",
        "## Übersicht",
        "",
        "| Seiten | G | Prinzip | DXF | Engine-Urteil |",
        "|---|---|---|---|---|",
    ]
    for f in faelle:
        v = f.get("verdikt") or {}
        u = (f.get("urteil") or {}).get("engine_verhalten")
        z.append(f"| S.{','.join(str(s) for s in f['seiten'])} | {f['geschoss']} | "
                 f"{f['prinzip'][:110]} | {'✓' if v.get('bestaetigt') else '✗'} | "
                 f"{URTEIL_LABEL.get(u, u)} |")
    z += ["", "## Die Fälle im Detail", ""]
    for i, f in enumerate(faelle, 1):
        v = f.get("verdikt") or {}
        u = f.get("urteil") or {}
        z.append(f"### Fall {i} — S.{','.join(str(s) for s in f['seiten'])} · "
                 f"{f['geschoss']} · {f['ort']}")
        z.append(f"**Prinzip:** {f['prinzip']}")
        if f.get("zitat"):
            z.append(f"> „{f['zitat']}“")
        r = f.get("richtig") or {}
        z.append(f"**RICHTIG:** {r.get('typ','')}"
                 + (f" · Handle {r['dxf_handle']}" if r.get("dxf_handle") else "")
                 + (f" · {r['rotation']}" if r.get("rotation") else ""))
        if r.get("begruendung"):
            z.append(f"  Begründung: {r['begruendung']}")
        for fv in f.get("falsch_varianten") or []:
            z.append(f"**FALSCH wäre:** {fv.get('variante','')} — {fv.get('warum_falsch','')}"
                     + (f" (im DXF als Negativ-Beispiel gezeichnet: {fv.get('dxf_handle')})"
                        if fv.get("im_dxf_gezeichnet") else ""))
        z.append(f"**DXF-Verifikation:** {'BESTÄTIGT' if v.get('bestaetigt') else 'NICHT bestätigt'}"
                 + (f" — {v.get('messwerte','')[:400]}" if v.get("messwerte") else ""))
        if v.get("korrekturen"):
            z.append(f"  Korrekturen: {v['korrekturen'][:300]}")
        if u:
            z.append(f"**Engine heute:** {URTEIL_LABEL.get(u.get('engine_verhalten'))} — "
                     f"{u.get('begruendung','')[:600]}")
            if u.get("engine_fundstelle"):
                z.append(f"  Fundstelle: `{u['engine_fundstelle'][:160]}`")
            if u.get("lauf_beleg"):
                z.append(f"  Lauf-Beleg: {u['lauf_beleg'][:250]}")
        z.append("")
    (ANALYSE / "FALLBEISPIELE_REVIEW.md").write_text("\n".join(z), encoding="utf-8")
    print(f"{len(faelle)} Fälle -> FALLBEISPIELE_REVIEW.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
