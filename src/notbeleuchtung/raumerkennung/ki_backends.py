"""ki_backends — die Anbieter hinter ``ki_zweitmeinung.ZweitmeinungBackend``.

- ``codex_abo``: offizielle Codex-CLI nicht-interaktiv (``codex exec --json``) über den
  eingeloggten ChatGPT-Account. Heute aktiv. Nur lesen: Sandbox ``read-only``,
  ``--ephemeral`` (keine Session auf der Platte), ``--skip-git-repo-check``, ein Durchgang
  je Frage, Zeitlimit je Aufruf, Bild(er) per ``--image=<Datei>``, Modell und Stufe immer
  explizit (``-m``, ``-c model_reasoning_effort=…``), Antwortform per ``--output-schema``.
  Der Prompt geht über stdin (Argument ``-``) — kein Quoting-Problem mit ``"`` oder ``<``;
  Pfade mit Leerzeichen stehen als eigenes Element der Argumentliste, nie in einem
  Shell-String. Die Umgebung des Kindprozesses verliert ``OPENAI_API_KEY`` und
  ``ANTHROPIC_API_KEY``, damit sicher das Abo genutzt wird. Login-Daten werden nie
  gelesen.
- ``openai_api``: OpenAI-API, nur Gerüst, per Konfiguration schaltbar, heute aus (liefert
  ein Fehlerobjekt, kein Abbruch). Kein Key im Repo oder in der Konfiguration; wenn es
  einmal aktiv wird, kommt der Key ausschließlich aus der Umgebung des Nutzers.
- Registry ``BACKENDS``: ein späteres ``claude_abo`` (``claude -p``) ist nur eine weitere
  Klasse mit ``name`` und ``frage`` — ohne Änderung an der Engine.

Binary-Suche ``finde_codex``: Konfiguration → ``PATH`` → App-Bundle der Codex-Desktop-App
(``%LOCALAPPDATA%/OpenAI/Codex/bin/*/codex.exe``, jüngstes zuerst).
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from .ki_zweitmeinung import (
    ANTWORT_SCHEMA,
    Antwort,
    GeschossAnfrage,
    KiFehler,
    KiKonfig,
    baue_prompt,
    parse_antwort,
)

_KEYS_RAUS = ("OPENAI_API_KEY", "ANTHROPIC_API_KEY")
_LIMIT = re.compile(r"usage limit|rate limit|quota|too many requests|429", re.IGNORECASE)
_LOGIN = re.compile(r"logged in|log in|login|sign in|auth|unauthori[sz]ed|401|403", re.IGNORECASE)


def finde_codex(konfig_pfad: str | None) -> Path | None:
    """Konfiguration → PATH → App-Bundle-Glob. None, wenn nichts davon eine Datei ist."""
    if konfig_pfad:
        p = Path(konfig_pfad)
        return p if p.is_file() else None
    im_pfad = shutil.which("codex")
    if im_pfad:
        return Path(im_pfad)
    basis = os.environ.get("LOCALAPPDATA")
    if not basis:
        return None
    kandidaten = sorted(Path(basis, "OpenAI", "Codex", "bin").glob("*/codex.exe"),
                        key=lambda p: p.stat().st_mtime, reverse=True)
    return kandidaten[0] if kandidaten else None


def _klassifiziere(meldung: str) -> str:
    if _LIMIT.search(meldung):
        return "limit"
    if _LOGIN.search(meldung):
        return "login"
    return "sonstig"


def _jsonl(stdout: str) -> tuple[str | None, list[str]]:
    """JSONL-Events → (letzter agent_message-Text oder None, Fehlermeldungen)."""
    text, fehler = None, []
    for zeile in stdout.splitlines():
        zeile = zeile.strip()
        if not zeile.startswith("{"):
            continue
        try:
            ev = json.loads(zeile)
        except json.JSONDecodeError:
            continue
        art = ev.get("type")
        if art == "error":
            fehler.append(str(ev.get("message", "")))
        elif art == "turn.failed":
            fehler.append(str((ev.get("error") or {}).get("message", "")))
        elif art == "item.completed":
            item = ev.get("item") or {}
            if item.get("type") == "agent_message" and isinstance(item.get("text"), str):
                text = item["text"]
    return text, [f for f in fehler if f]


class CodexAboBackend:
    name = "codex_abo"

    def __init__(self, konfig: KiKonfig, run=subprocess.run):
        self.konfig = konfig
        self._run = run

    def umgebung(self) -> dict[str, str]:
        return {k: v for k, v in os.environ.items() if k not in _KEYS_RAUS}

    def argumente(self, exe: Path, anfrage: GeschossAnfrage, modell: str, schema: Path,
                  letzte: Path) -> list[str]:
        args = [str(exe), "exec", "--json", "--ephemeral", "--skip-git-repo-check",
                "-s", "read-only", "-m", modell, "-c", f"model_reasoning_effort={self.konfig.effort}",
                "--output-schema", str(schema), "-o", str(letzte)]
        args += [f"--image={b}" for b in anfrage.bilder]   # „=“: ein Bild je Element, kein ``...``
        return args + ["-"]                                 # Prompt aus stdin

    def frage(self, anfrage: GeschossAnfrage, modell: str | None = None) -> Antwort:
        modell = modell or self.konfig.modell
        exe = finde_codex(self.konfig.codex_binary)
        if exe is None:
            return Antwort(fehler=KiFehler(
                "sonstig", "codex-Binary nicht gefunden (Konfiguration codex_binary, PATH, "
                           "App-Bundle unter LOCALAPPDATA/OpenAI/Codex/bin)"))
        fehlend = [b.name for b in anfrage.bilder if not Path(b).is_file()]
        if fehlend:
            return Antwort(fehler=KiFehler("sonstig", "Bild fehlt: " + ", ".join(fehlend)))
        prompt = baue_prompt(anfrage)
        with tempfile.TemporaryDirectory(prefix="nb_ki_") as td:
            schema, letzte = Path(td, "antwort_schema.json"), Path(td, "letzte_nachricht.txt")
            schema.write_text(json.dumps(ANTWORT_SCHEMA), encoding="utf-8")
            args = self.argumente(exe, anfrage, modell, schema, letzte)
            try:
                ergebnis = self._run(args, input=prompt, capture_output=True, text=True,
                                     encoding="utf-8", errors="replace", env=self.umgebung(),
                                     cwd=td, timeout=self.konfig.zeitlimit_s)
            except subprocess.TimeoutExpired:
                return Antwort(fehler=KiFehler(
                    "timeout", f"codex exec nach {self.konfig.zeitlimit_s:g} s abgebrochen"))
            text, fehler = _jsonl(ergebnis.stdout or "")
            if text is None and letzte.is_file():
                text = letzte.read_text(encoding="utf-8", errors="replace").strip() or None
        if fehler:
            meldung = fehler[-1]
            return Antwort(fehler=KiFehler(_klassifiziere(meldung), meldung), roh=text or "")
        if text is None:
            return Antwort(fehler=KiFehler(
                "format", f"keine Antwort im JSONL (Exit {ergebnis.returncode}, "
                          f"stderr: {(ergebnis.stderr or '').strip()[-200:]!r})"))
        raeume, verworfen, formfehler = parse_antwort(text, anfrage.raum_ids)
        return Antwort(raeume=raeume, verworfen=verworfen, fehler=formfehler, roh=text)


class OpenaiApiBackend:
    """Gerüst: Klasse, Konfiguration, kein Aufruf. Heute aus; Key nie im Repo."""

    name = "openai_api"

    def __init__(self, konfig: KiKonfig):
        self.konfig = konfig

    def frage(self, anfrage: GeschossAnfrage, modell: str | None = None) -> Antwort:
        return Antwort(fehler=KiFehler(
            "sonstig", "Backend openai_api ist nicht freigeschaltet (Gerüst; Key käme nur aus "
                       "der Umgebung des Nutzers, nie aus Repo oder Konfiguration)"))


BACKENDS: dict[str, type] = {
    CodexAboBackend.name: CodexAboBackend,
    OpenaiApiBackend.name: OpenaiApiBackend,
    # "claude_abo": später eine weitere Klasse (claude -p) — nur hier eintragen.
}


def backend_aus_konfig(konfig: KiKonfig):
    try:
        return BACKENDS[konfig.backend](konfig)
    except KeyError:
        raise ValueError(
            f"KI-Backend {konfig.backend!r} unbekannt — bekannt: {sorted(BACKENDS)}") from None
