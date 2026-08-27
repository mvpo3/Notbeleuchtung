"""Schema-Drift-Gate — eingecheckte contracts/schema/*.json == aus Pydantic generiert.

Bricht, wenn jemand ein Contract-Feld ändert ohne 'python scripts/gen_schema.py'
zu laufen + zu committen → erzwingt bewussten contract_version-Bump.
"""
import subprocess
import sys


def test_schema_in_sync():
    result = subprocess.run(
        [sys.executable, "scripts/gen_schema.py", "--check"],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, f"Schema-Drift:\n{result.stdout}\n{result.stderr}"
