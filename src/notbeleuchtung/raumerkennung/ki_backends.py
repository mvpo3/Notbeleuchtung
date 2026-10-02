"""ki_backends — die Anbieter hinter ``ki_zweitmeinung.ZweitmeinungBackend``.

- ``codex_abo``: offizielle Codex-CLI nicht-interaktiv (``codex exec --json``) über den
  eingeloggten ChatGPT-Account. Heute aktiv. Nur lesen: Sandbox ``read-only``,
  ``--ephemeral`` (keine Session auf der Platte), ``--skip-git-repo-check``, ein Durchgang
  je Frage, Zeitlimit je Aufruf, Bild(er) per ``--image=<Datei>``, Modell und Stufe immer
  explizit (``-m``, ``-c model_reasoning_effort=…``), Antwortform per ``--output-schema``.
  Der Prompt geht über stdin (Argument ``-``) — kein Quoting-Problem mit ``"`` oder ``<``;
  Pfade mit Leerzeichen stehen als eigenes Element der Argumentliste, nie in einem
  Shell-String. Die Umgebung des Kindprozesses verliert jede Key-/Token-Variable
  (``_KEYS_RAUS`` und jedes ``*_API_KEY``), damit sicher das Abo genutzt wird. Login-Daten
  werden nie gelesen.
- Abo-Regel (Owner 2026-10-01, ``KiKonfig.nur_abo``, fest): „Die KI läuft ausschließlich über
  das ChatGPT-Abo. Keine Credits, keine API-Keys, kein Aufladen, jetzt nicht und später nicht.
  Ist das Abo-Kontingent erschöpft, wird gewartet, nichts anderes." Deshalb fragt
  ``codex_abo`` einmal je Lauf vor dem ersten ``exec`` ``codex login status`` und wertet nur
  „ChatGPT" gegen „API key" aus (nie ``auth.json``); alles außer ChatGPT → ``KiFehler login``
  ohne Aufruf. Kein Aufruf übergibt einen Key oder meldet sich an.
- ``openai_api``: OpenAI-API, nur Gerüst; unter der Abo-Regel nicht aktivierbar (liefert
  ``KiFehler sonstig`` „nur ChatGPT-Abo erlaubt", kein Abbruch), liest keinen Key.
- Registry ``BACKENDS``: ein späteres ``claude_abo`` (``claude -p``) ist nur eine weitere
  Klasse mit ``name`` und ``frage`` — ohne Änderung an der Engine; aktiv wird unter
  ``nur_abo`` trotzdem nur ``codex_abo`` (jedes andere → ``GesperrtesBackend``).

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
    NUR_ABO,
    Antwort,
    GeschossAnfrage,
    KiFehler,
    KiKonfig,
    baue_prompt,
    parse_antwort,
)

#: Nie an den Kindprozess (Abo-Regel). codex-cli 0.159.2 ``--help``: ``login --with-api-key``
#: (OPENAI_API_KEY), ``login --with-access-token`` (CODEX_ACCESS_TOKEN); dazu CODEX_API_KEY
#: (Owner-Auftrag Abo-Regel; in der Hilfe nicht genannt) und ANTHROPIC_API_KEY (Auftrag § 3).
#: Zusätzlich fällt jede Variable ``*_API_KEY`` weg (z. B. Key eines Modell-Anbieters).
_KEYS_RAUS = ("OPENAI_API_KEY", "CODEX_API_KEY", "CODEX_ACCESS_TOKEN", "ANTHROPIC_API_KEY")
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


def _key_variable(name: str) -> bool:
    n = name.upper()
    return n in _KEYS_RAUS or n.endswith("_API_KEY")


class CodexAboBackend:
    name = "codex_abo"

    def __init__(self, konfig: KiKonfig, run=subprocess.run):
        self.konfig = konfig
        self._run = run
        self._login: KiFehler | None | bool = False   # False = in diesem Lauf noch nicht geprüft

    def umgebung(self) -> dict[str, str]:
        return {k: v for k, v in os.environ.items() if not _key_variable(k)}

    def login_fehler(self, exe: Path) -> KiFehler | None:
        """``codex login status`` einmal je Lauf (= je Backend-Instanz): None nur bei Anmeldung
        über ChatGPT. Die Ausgabe wird nur auf „ChatGPT" gegen „API key" ausgewertet und nie
        weitergegeben; ``auth.json`` wird nie geöffnet. Nicht prüfbar = nicht ChatGPT."""
        if self._login is not False:
            return self._login
        try:
            r = self._run([str(exe), "login", "status"], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=self.umgebung(),
                          timeout=self.konfig.zeitlimit_s)
            ausgabe = f"{r.stdout or ''}\n{r.stderr or ''}"
            if "api key" in ausgabe.lower():
                grund = "codex ist mit API-Key angemeldet"
            elif r.returncode == 0 and "ChatGPT" in ausgabe:
                grund = ""
            else:
                grund = f"codex ist nicht mit ChatGPT angemeldet (login status Exit {r.returncode})"
        except (OSError, subprocess.TimeoutExpired) as e:
            grund = f"Login-Status nicht prüfbar ({type(e).__name__})"
        self._login = KiFehler("login", f"{grund} — {NUR_ABO}, kein Aufruf") if grund else None
        return self._login

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
        if (login := self.login_fehler(exe)) is not None:
            return Antwort(fehler=login)
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


class GesperrtesBackend:
    """Unter der Abo-Regel jedes Backend außer codex_abo: kein Aufruf, ``KiFehler sonstig``."""

    def __init__(self, name: str):
        self.name = name

    def frage(self, anfrage: GeschossAnfrage, modell: str | None = None) -> Antwort:
        return Antwort(fehler=KiFehler(
            "sonstig", f"Backend {self.name} gesperrt — {NUR_ABO} (Owner-Regel 2026-10-01)"))


class OpenaiApiBackend(GesperrtesBackend):
    """Gerüst: Klasse, Konfiguration, kein Aufruf, liest keinen Key. Unter der Abo-Regel nicht
    aktivierbar — auch direkt erzeugt liefert es nur den Fehler."""

    name = "openai_api"

    def __init__(self, konfig: KiKonfig):
        super().__init__(self.name)
        self.konfig = konfig


BACKENDS: dict[str, type] = {
    CodexAboBackend.name: CodexAboBackend,
    OpenaiApiBackend.name: OpenaiApiBackend,
    # "claude_abo": später eine weitere Klasse (claude -p) — nur hier eintragen.
}


def backend_aus_konfig(konfig: KiKonfig):
    if konfig.backend not in BACKENDS:
        raise ValueError(f"KI-Backend {konfig.backend!r} unbekannt — bekannt: {sorted(BACKENDS)}")
    if konfig.nur_abo and konfig.backend != CodexAboBackend.name:
        return GesperrtesBackend(konfig.backend)
    return BACKENDS[konfig.backend](konfig)
