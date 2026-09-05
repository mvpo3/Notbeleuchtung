"""Hauptengine-Architektur v2 — Swimlanes je Owner, NetworkX-Topologie, PNG+SVG."""
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyArrowPatch, Patch

sys.stdout.reconfigure(encoding="utf-8")

C = {
    "input": "#7b5ea7", "selman": "#2f6fc4", "enis": "#d97f1f",
    "leonis": "#1f9d55", "haupt": "#4a4f58", "out": "#c0334f",
}
LANES = [  # (label, farbe, y_unten, y_oben)
    ("Selman — raumerkennung/", "selman", 8.55, 10.05),
    ("Enis — normwissen/",      "enis",   6.25, 8.35),
    ("Hauptengine (gemeinsam)", "haupt",  2.45, 6.05),
    ("Leonis — platzierung/",   "leonis", 0.10, 2.25),
]

N = [
    ("dxf",      "Architekturplan\nDXF / DWG",                                  "input",  (1.0, 5.35)),
    ("lb",       "Leistungsbeschreibung\n(Text / PDF)",                          "input",  (1.0, 6.70)),
    ("raum",     "DxfRaumProvider\nRäume · Türen · Ausgänge\nZirkulation · Raumtyp", "selman", (6.6, 9.3)),
    ("normdata", "data/*.yaml\nEN 1838 · OVE · Regeln\nSonderstellen",           "enis",   (5.2, 7.90)),
    ("photo",    "photometrie/\nLDT/IES · Schrack-Katalog",                      "enis",   (8.4, 7.90)),
    ("norm",     "NormProvider\nregelwerk_snapshot()",                           "enis",   (7.0, 6.70)),
    ("lbp",      "lb/parser.py\nLbTextProvider → LBVorgabe",                     "enis",   (4.0, 6.70)),
    ("dwg",      "dwg_input.py\nODA (DWG→DXF)",                                  "haupt",  (3.6, 5.35)),
    ("registry", "registry.py\nbuild_default_bundle()",                          "haupt",  (3.6, 3.1)),
    ("api",      "api/main.py\nPOST /plan · /projekt",                           "haupt",  (1.0, 3.1)),
    ("pipe",     "pipeline.run()\nOrchestrierung",                               "haupt",  (6.3, 4.15)),
    ("contracts","contracts/  (3-Owner-Naht)\nRaumModell · NormRegelwerk\nLBVorgabe · PlatzierungsErgebnis", "haupt", (9.6, 5.1)),
    ("valid",    "validierung.py — pruefe()\nNorm-/LB-/Plausi-Regeln\nRedundanz · Umschaltzeit · 8b/8c/10b", "haupt", (13.2, 5.35)),
    ("symbols",  "symbols/ library + inserter\nNotbeleuchtungssymbole.dxf",      "haupt",  (13.2, 3.0)),
    ("render",   "render/dxf_renderer.py\nDIN_SIBEL · NODEID + Stromkreisnr.\nBelegungsliste · Stückliste · Prüfbericht", "haupt", (16.2, 4.3)),
    ("pdf",      "render/pdf_export.py",                                         "haupt",  (16.2, 2.9)),
    ("place",    "NotlichtPlatzierer.place()",                                   "leonis", (9.6, 1.75)),
    ("strat",    "Strategien\nanker (Kreuzung · Pfeil-durch-Tür · l=z·h)\ngang · flaechen (Antipanik 0,5 lx)", "leonis", (6.4, 0.95)),
    ("graph",    "graph.py (NetworkX)\nKreuzungs-Anker · Dijkstra",              "leonis", (3.4, 0.95)),
    ("passes",   "Nachpässe  1→2→3\nabstand_nachpass · deckungs_zuordnung\ncircuit_zuordnung (DL/BL · Cap 20)", "leonis", (13.2, 1.1)),
    ("outplan",  "Notbeleuchtungsplan\nDXF + PDF\nSummary / Prüfbericht",        "out",    (19.3, 4.3)),
]

E = [
    ("dxf", "dwg"), ("dwg", "pipe"), ("lb", "lbp"),
    ("api", "pipe"), ("registry", "pipe"),
    ("pipe", "raum"), ("raum", "contracts"),
    ("normdata", "norm"), ("photo", "norm"), ("norm", "contracts"), ("lbp", "contracts"),
    ("contracts", "place"),
    ("place", "strat"), ("strat", "graph"), ("place", "passes"),
    ("place", "valid"), ("norm", "valid"),
    ("place", "render"), ("valid", "render"), ("symbols", "render"),
    ("render", "pdf"), ("render", "outplan"), ("pdf", "outplan"),
]

G = nx.DiGraph()
for nid, label, owner, xy in N:
    G.add_node(nid, label=label, owner=owner, pos=xy)
G.add_edges_from(E)
pos = {n: d["pos"] for n, d in G.nodes(data=True)}

fig, ax = plt.subplots(figsize=(22, 12), dpi=220)
fig.patch.set_facecolor("#fbfbfd")

for label, key, y0, y1 in LANES:
    ax.axhspan(y0, y1, xmin=0.0, xmax=1.0, color=C[key], alpha=0.055, zorder=0)
    ax.text(0.12, y1 - 0.16, label, fontsize=11, fontweight="bold",
            color=C[key], va="top", ha="left", alpha=0.9)

for u, v in G.edges():
    src_owner = G.nodes[u]["owner"]
    arrow = FancyArrowPatch(pos[u], pos[v], arrowstyle="-|>", mutation_scale=17,
                            connectionstyle="arc3,rad=0.08", lw=1.7,
                            color=C[src_owner], alpha=0.55, zorder=2,
                            shrinkA=34, shrinkB=34)
    ax.add_patch(arrow)

for nid, d in G.nodes(data=True):
    x, y = d["pos"]
    ax.text(x, y, d["label"], ha="center", va="center", fontsize=9.6,
            fontweight="bold", color="white", zorder=5, linespacing=1.35,
            bbox={"boxstyle": "round,pad=0.55", "fc": C[d["owner"]],
                  "ec": "white", "lw": 1.2, "alpha": 0.97})

ax.legend(handles=[
    Patch(color=C["input"], label="Inputs — die 2 Säulen der Mission"),
    Patch(color=C["selman"], label="Selman · raumerkennung/"),
    Patch(color=C["enis"], label="Enis · normwissen/"),
    Patch(color=C["leonis"], label="Leonis · platzierung/"),
    Patch(color=C["haupt"], label="Hauptengine · contracts/pipeline/render/api"),
    Patch(color=C["out"], label="Output"),
], loc="lower right", fontsize=10, framealpha=0.9)

ax.set_title("Notbeleuchtung — Hauptengine-Architektur · Ist-Stand main 2026-09-05\n"
             "Plugin-Modell (Ports & Adapters): Owner-Packages kommunizieren NUR über die Contracts",
             fontsize=15, pad=18)
ax.set_xlim(-0.1, 20.9)
ax.set_ylim(-0.35, 10.35)
ax.axis("off")
fig.tight_layout()
fig.savefig("docs/architektur.png", facecolor=fig.get_facecolor())
fig.savefig("docs/architektur.svg", facecolor=fig.get_facecolor())
print("ok png+svg")
