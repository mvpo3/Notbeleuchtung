"""Generiert die JSON-Schemas aus den Pydantic-Contracts (Single Source: Code).

    python scripts/gen_schema.py          # schreibt contracts/schema/*.json
    python scripts/gen_schema.py --check   # exit 1 bei Drift (CI-Gate)

Drift-Gate: nach jeder Contract-Änderung neu generieren + committen, sonst bricht
CI. Erzwingt bewussten contract_version-Bump.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from notbeleuchtung.hauptengine.contracts import SCHEMA_MODELS

SCHEMA_DIR = (
    Path(__file__).resolve().parents[1]
    / "src" / "notbeleuchtung" / "hauptengine" / "contracts" / "schema"
)


def _dump(model) -> str:
    return json.dumps(model.model_json_schema(), indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    check = "--check" in sys.argv
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    drift = []
    for name, model in SCHEMA_MODELS.items():
        target = SCHEMA_DIR / f"{name}.schema.json"
        new = _dump(model)
        if check:
            old = target.read_text(encoding="utf-8") if target.exists() else ""
            if old != new:
                drift.append(name)
        else:
            target.write_text(new, encoding="utf-8")
            print(f"wrote {target.relative_to(SCHEMA_DIR.parents[4])}")
    if check and drift:
        print(f"SCHEMA-DRIFT in: {', '.join(drift)} — 'python scripts/gen_schema.py' + committen.")
        return 1
    if check:
        print("schema in sync")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
