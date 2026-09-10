#!/usr/bin/env python3
"""Contract-Freeze-Gate: Approval aller CODEOWNERS auf dem AKTUELLEN head_sha.

Beruehrt ein PR weder `hauptengine/contracts/` noch `CONTRACT_VERSION`, endet der
Check GRUEN (exit 0) — er taugt damit als Required Status Check.

Frische-Kriterium ist `review.commit_id == head_sha`, nicht `submitted_at`:
committer-Daten sind client-gesetzt und nach Rebase/Amend beliebig alt, das
commit_id ist die Tatsache, die GitHub am Review festhaelt.

Env: GH_TOKEN, REPO, PR, HEAD_SHA. NO_COMMENT=1 unterdrueckt den PR-Kommentar
(fuer lokales Durchspielen gegen echte PR-Daten).
"""
import json
import os
import subprocess
import sys

CONTRACTS_PREFIX = "src/notbeleuchtung/hauptengine/contracts/"
CODEOWNERS_PATH = ".github/CODEOWNERS"
CODEOWNERS_MATCH = "hauptengine/contracts/"
MARKER = "<!-- contract-freeze-stale-approval -->"

REPO = os.environ["REPO"]
PR = os.environ["PR"]
HEAD_SHA = os.environ.get("HEAD_SHA", "")


def gh(path, *args):
    out = subprocess.run(
        ["gh", "api", path, *args], capture_output=True, text=True,
        encoding="utf-8", check=True
    ).stdout
    return json.loads(out)


def owners():
    """Drei Logins aus der CODEOWNERS-Zeile fuer hauptengine/contracts/ lesen.

    Eine Zeile, ein Praefix — kein Glob-Parser noetig, kein zweiter Pflegeort.
    """
    with open(CODEOWNERS_PATH, encoding="utf-8") as fh:
        for line in fh:
            line = line.split("#", 1)[0].strip()
            if line.startswith("/") and CODEOWNERS_MATCH in line.split()[0]:
                return [t.lstrip("@") for t in line.split()[1:] if t.startswith("@")]
    sys.exit(f"CODEOWNERS-Zeile fuer {CODEOWNERS_MATCH} nicht gefunden")


def summary(text):
    print(text)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(text + "\n")


def upsert_comment(body):
    """Vorhandenen Bot-Kommentar am Marker erkennen und aktualisieren statt anhaengen."""
    if os.environ.get("NO_COMMENT") == "1":
        return
    body = MARKER + "\n" + body
    for c in gh(f"repos/{REPO}/issues/{PR}/comments", "--paginate"):
        if MARKER in c["body"]:
            subprocess.run(
                ["gh", "api", "--method", "PATCH",
                 f"repos/{REPO}/issues/comments/{c['id']}", "-f", f"body={body}"],
                check=True, capture_output=True,
            )
            return
    subprocess.run(
        ["gh", "api", "--method", "POST", f"repos/{REPO}/issues/{PR}/comments",
         "-f", f"body={body}"], check=True, capture_output=True,
    )


def main():
    files = gh(f"repos/{REPO}/pulls/{PR}/files", "--paginate")
    touched = sorted(
        f["filename"] for f in files
        if f["filename"].startswith(CONTRACTS_PREFIX)
        # CONTRACT_VERSION nur in Python-Quellen werten — in Doku/Berichten steht
        # der Bezeichner als Prosa und wuerde jeden Doku-PR faelschlich rot faerben.
        or (f["filename"].endswith(".py")
            and "CONTRACT_VERSION" in (f.get("patch") or ""))
    )
    if not touched:
        summary("contract-freeze: PR beruehrt keine Contracts - nichts zu pruefen.")
        return 0

    soll = owners()
    reviews = gh(f"repos/{REPO}/pulls/{PR}/reviews", "--paginate")
    # Pro Login zaehlt nur das juengste wertende Review; COMMENTED wertet nicht.
    latest = {}
    for r in sorted(reviews, key=lambda r: r["submitted_at"] or ""):
        if r["state"] in ("APPROVED", "CHANGES_REQUESTED", "DISMISSED"):
            latest[r["user"]["login"]] = r

    frisch = [o for o in soll if o in latest
              and latest[o]["state"] == "APPROVED"
              and latest[o]["commit_id"] == HEAD_SHA]
    veraltet = [o for o in soll if o in latest
                and latest[o]["state"] == "APPROVED"
                and latest[o]["commit_id"] != HEAD_SHA]
    fehlend = [o for o in soll if o not in frisch]

    summary("## contract-freeze\n\nGeaenderte Contract-Dateien:\n"
            + "\n".join(f"- `{f}`" for f in touched)
            + f"\n\nhead_sha: `{HEAD_SHA}`\n"
            f"\n- Approval auf diesem Stand: {', '.join(frisch) or 'keine'}"
            f"\n- Approval auf altem Stand (veraltet): {', '.join(veraltet) or 'keine'}"
            f"\n- Fehlend: {', '.join(fehlend) or 'keine'}")

    if veraltet:
        shas = [c["sha"] for c in gh(f"repos/{REPO}/pulls/{PR}/commits", "--paginate")]
        zeilen = []
        for o in veraltet:
            cid = latest[o]["commit_id"]
            n = len(shas) - shas.index(cid) - 1 if cid in shas else "?"
            zeilen.append(f"- @{o}: Approval auf `{cid[:7]}`, seither {n} Commits")
        upsert_comment(
            "**Approval veraltet.** Nach dem Approval kamen neue Commits dazu — "
            "der Contract-Freeze gilt nur fuer den Stand, auf dem approved wurde.\n\n"
            + "\n".join(zeilen)
            + f"\n\nAktueller Stand: `{HEAD_SHA[:7]}`. Bitte erneut reviewen."
        )

    if fehlend:
        summary(f"\n**FEHLGESCHLAGEN** - Approval aller CODEOWNERS "
                f"({', '.join(soll)}) auf `{HEAD_SHA[:7]}` noetig.")
        return 1
    summary("\n**OK** — alle CODEOWNERS haben diesen Stand approved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
