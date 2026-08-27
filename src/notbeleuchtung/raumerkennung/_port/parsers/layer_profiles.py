"""Layer-profile loader for architecture DXF dialects.

Track-A config only: profiles describe CAD layer/block conventions, not
domain rules. Domain YAMLs under backend/rules remain untouched.
"""
from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import yaml


PROFILE_DIR = Path(__file__).resolve().parent / "profiles"

_LOCK = threading.Lock()
_CACHE: dict[tuple[Path, str], "LayerProfile"] = {}


@dataclass(frozen=True)
class LayerProfile:
    profile_id: str
    version: int
    layout: dict[str, Any]
    scale: dict[str, Any]
    roles: dict[str, dict[str, Any]]
    # Slice 1.0.0: Bauteil-/TOP-Stempel-Konvention (Wohnungs-Inventur).
    # Projekt-Daten aus der BAB (rule:lb_override), keine Norm-Werte.
    building_units: dict[str, Any] = field(default_factory=dict)
    # Slice N3: KG-Rekonstruktions-Vokabular (Wand-/HID-Layer-Regexe,
    # Zonen-Stempel-Tokens). Fehlt die Sektion → Mollgasse-Default in
    # parsers.keller_geometry (Feld-basierte is_wall_layer-Semantik).
    keller: dict[str, Any] = field(default_factory=dict)
    # Slice N6: Auto-Detection-Fingerprint (layer_patterns + min_matches).
    # Fehlt die Sektion → Profil nimmt an der Detection nicht teil.
    detect: dict[str, Any] = field(default_factory=dict)

    def role_strategy(self, role: str) -> str:
        section = self.roles.get(role) or {}
        return str(section.get("strategy", ""))


def load_profile(profile_id: str = "mollgasse",
                 profile_dir: Path | None = None) -> LayerProfile:
    """Load one parser layer profile by id, cached and read-only."""
    root = profile_dir or PROFILE_DIR
    path = root / f"{profile_id}.yaml"
    key = (path.resolve(), profile_id)
    with _LOCK:
        cached = _CACHE.get(key)
        if cached is not None:
            return cached
        if not path.exists():
            raise FileNotFoundError(f"Layer profile not found: {path}")
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        loaded_id = str(data.get("profile_id", ""))
        if loaded_id != profile_id:
            raise ValueError(
                f"Layer profile id mismatch: expected {profile_id!r}, "
                f"got {loaded_id!r} in {path}"
            )
        profile = LayerProfile(
            profile_id=loaded_id,
            version=int(data.get("version", 1)),
            layout=dict(data.get("layout") or {}),
            scale=dict(data.get("scale") or {}),
            roles=dict(data.get("roles") or {}),
            building_units=dict(data.get("building_units") or {}),
            keller=dict(data.get("keller") or {}),
            detect=dict(data.get("detect") or {}),
        )
        _CACHE[key] = profile
        return profile


def list_profile_ids(profile_dir: Path | None = None) -> list[str]:
    root = profile_dir or PROFILE_DIR
    return sorted(p.stem for p in root.glob("*.yaml"))


def detect_profile_id(
    layer_names: Iterable[str],
    profile_dir: Path | None = None,
) -> str | None:
    """Infer profile_id from a DXF layer-table (Slice N6).

    Pro Profil mit `detect:`-Sektion: Anteil der Fingerprint-Patterns, die
    mindestens einen Layer-Namen treffen. Qualifiziert ab `min_matches`
    (Default: alle Patterns). Bester Score gewinnt; echter Gleichstand →
    None (explizit uneindeutig, kein Raten).
    """
    names = [str(n) for n in layer_names]
    scored: list[tuple[float, int, str]] = []
    for pid in list_profile_ids(profile_dir):
        profile = load_profile(pid, profile_dir)
        patterns = list(profile.detect.get("layer_patterns") or [])
        if not patterns:
            continue
        min_matches = int(profile.detect.get("min_matches", len(patterns)))
        hits = sum(
            1 for pat in patterns
            if any(re.search(pat, name) for name in names)
        )
        if hits >= min_matches:
            scored.append((hits / len(patterns), hits, pid))
    if not scored:
        return None
    scored.sort(reverse=True)
    if len(scored) > 1 and scored[0][:2] == scored[1][:2]:
        return None
    return scored[0][2]


def detect_profile_for_dxf(
    dxf_path: Path | str,
    profile_dir: Path | None = None,
) -> str | None:
    """Layer-Tabelle eines DXF lesen und Profil inferieren."""
    import ezdxf

    doc = ezdxf.readfile(str(dxf_path))
    return detect_profile_id(
        (layer.dxf.name for layer in doc.layers), profile_dir
    )


def _reset_cache_for_tests() -> None:
    with _LOCK:
        _CACHE.clear()
