import sys
import time
import matplotlib
matplotlib.use("Agg")
import ezdxf
from ezdxf import bbox as _bb
from notbeleuchtung.hauptengine.registry import build_default_bundle
from notbeleuchtung.hauptengine.pipeline import run
from notbeleuchtung.hauptengine.render.pdf_export import dxf_zu_pdf

for fl in sys.argv[1:]:
    t0 = time.time()
    pfad = f"Projekte/Baufeld E2/Elektromontageplan_{fl}.dxf"
    out = f"output/baufeld_e2_{fl.lower()}_notbeleuchtung"
    try:
        o = run(build_default_bundle(), pfad, fl, out_path=out + ".dxf")
        by = {}
        for p in o.platzierung.platzierungen:
            by[p.kind] = by.get(p.kind, 0) + 1
        doc = ezdxf.readfile(out + ".dxf")
        tb = [e for e in doc.modelspace() if e.dxf.layer == "din_SIBEL_99_titleblock"]
        ext = _bb.extents(tb, fast=True)
        dxf_zu_pdf(out + ".dxf", out + ".pdf",
                   ausschnitt=(ext.extmin.x, ext.extmin.y, ext.extmax.x, ext.extmax.y))
        print(f"{fl:4s}: Räume {len(o.raum.raeume):3d} · {by} · "
              f"Unterlage {o.render_summary['unterlage_entities']:5d} · "
              f"{o.render_summary['pruefung']['status']} · {int(time.time()-t0)}s", flush=True)
    except Exception as e:
        print(f"{fl:4s}: FEHLER {type(e).__name__}: {str(e)[:70]}", flush=True)
