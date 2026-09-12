"""Contract-Freeze-Gate: Approval aller CODEOWNERS auf dem AKTUELLEN head_sha.

Beruehrt ein PR weder `hauptengine/contracts/` noch `CONTRACT_VERSION`, endet der
Check GRUEN (exit 0) — er taugt damit als Required Status Check.

Frische-Kriterium ist `review.commit_id == head_sha`, nicht `submitted_at`:
committer-Daten sind client-gesetzt und nach Rebase/Amend beliebig alt, das
commit_id ist die Tatsache, die GitHub am Review festhaelt.

Die Owner-Liste kommt aus `.github/CODEOWNERS` am BASE_SHA des PR, ueber die API —
nicht aus dem Arbeitsbaum. Sonst koennte ein PR die Liste im selben Commit aendern
und sich damit die eigene Pruefgrundlage setzen. Ist die Grundlage nicht lesbar,
bricht der Check ab (exit 1); "nicht lesbar" darf nie "freigegeben" bedeuten.

⚠️ Reichweite, damit sie nicht ueberschaetzt wird: diese Korrektur schliesst EINE
Luecke — die Pruefgrundlage CODEOWNERS gehoert jetzt dem Base. Sie ist KEIN
vollstaendiger Freigabeschutz. Bei `on: pull_request` laufen Workflow und Skript
aus dem PR-HEAD; ein PR, der eine der beiden Dateien aendert, veraendert damit den
Pruefer selbst. Wer den Check liest, muss diesen Diff mitlesen.

Das sind zwei verschiedene Fragen, und keine davon ist hier geloest:
  (1) VERTRAUENSWUERDIGE AUSFUEHRUNG des Pruefers — dass er in einer Fassung
      laeuft, die der PR nicht bestimmt. Das ist mit GitHub-Mitteln erreichbar
      (z. B. Ausfuehrung der Basis-Fassung des Workflows, ohne PR-Inhalte
      auszufuehren); es waere eine Workflow-Umstellung und ist hier bewusst
      NICHT enthalten. Es ist ausdruecklich NICHT technisch unmoeglich.
  (2) EINE VON GITHUB ERZWUNGENE MERGESPERRE — ein Required Status Check. Das ist
      eine Repo-Einstellung (Branch Protection / Ruleset), unabhaengig von (1),
      und laut docs/BRANCH_PROTECTION.md auf dem aktuellen Plan nicht verfuegbar.
Bis beides geklaert ist, ist dieser Check eine verlaessliche ANZEIGE, keine Sperre.

Env: GH_TOKEN, REPO, PR, HEAD_SHA, BASE_SHA. NO_COMMENT=1 unterdrueckt den
PR-Kommentar (fuer lokales Durchspielen gegen echte PR-Daten).
"""
import base64
import json
import os
import subprocess
import sys

CONTRACTS_PREFIX = "src/notbeleuchtung/hauptengine/contracts/"
SRC_PREFIX = "src/"
CODEOWNERS_PATH = ".github/CODEOWNERS"
CODEOWNERS_MATCH = "hauptengine/contracts/"
MARKER = "<!-- contract-freeze-stale-approval -->"

REPO = os.environ["REPO"]
PR = os.environ["PR"]
HEAD_SHA = os.environ.get("HEAD_SHA", "")
BASE_SHA = os.environ.get("BASE_SHA", "")


def gh(path, *args):
    out = subprocess.run(
        ["gh", "api", path, *args], capture_output=True, text=True,
        encoding="utf-8", check=True
    ).stdout
    return json.loads(out)   # CalledProcessError/JSONDecodeError bleiben sichtbar


def codeowners_am_base():
    """Rohtext von CODEOWNERS am BASE-Commit des PR.

    Feste Commit-ID, keine bewegliche Branch-Referenz: `base.sha` ist der Stand,
    gegen den DIESER PR gemessen wird. Jeder Fehlerweg endet in sys.exit(1) mit
    Klartext — eine nicht lesbare Pruefgrundlage darf nie zu einer Freigabe
    fuehren.
    """
    if not BASE_SHA:
        sys.exit("BASE_SHA fehlt — ohne Base-Commit gibt es keine verlaessliche "
                 "Pruefgrundlage fuer CODEOWNERS. Abbruch statt Freigabe.")
    try:
        blob = gh(f"repos/{REPO}/contents/{CODEOWNERS_PATH}?ref={BASE_SHA}")
    except subprocess.CalledProcessError as exc:
        sys.exit(f"CODEOWNERS am Base-Commit {BASE_SHA[:7]} nicht lesbar "
                 f"(gh api: {(exc.stderr or '').strip()[:200]}). Abbruch statt Freigabe.")
    except json.JSONDecodeError:
        sys.exit(f"Antwort fuer CODEOWNERS am Base-Commit {BASE_SHA[:7]} ist kein "
                 f"gueltiges JSON. Abbruch statt Freigabe.")
    if blob.get("encoding") != "base64" or not blob.get("content"):
        sys.exit(f"CODEOWNERS am Base-Commit {BASE_SHA[:7]} liefert keinen "
                 f"base64-Inhalt (encoding={blob.get('encoding')!r}). Abbruch statt Freigabe.")
    try:
        return base64.b64decode(blob["content"]).decode("utf-8")
    except (ValueError, UnicodeDecodeError) as exc:
        sys.exit(f"CODEOWNERS am Base-Commit {BASE_SHA[:7]} nicht dekodierbar "
                 f"({exc}). Abbruch statt Freigabe.")


def owners():
    """Logins aus der CODEOWNERS-Zeile fuer hauptengine/contracts/ — AM BASE.

    Eine Zeile, ein Praefix — kein Glob-Parser noetig, kein zweiter Pflegeort.
    Die Datei im Arbeitsbaum wird bewusst NICHT gelesen: sie gehoert dem PR.
    """
    for line in codeowners_am_base().splitlines():
        line = line.split("#", 1)[0].strip()
        if line.startswith("/") and CODEOWNERS_MATCH in line.split()[0]:
            treffer = [t.lstrip("@") for t in line.split()[1:] if t.startswith("@")]
            if not treffer:
                sys.exit(f"CODEOWNERS-Zeile fuer {CODEOWNERS_MATCH} am Base-Commit "
                         f"{BASE_SHA[:7]} nennt keinen Owner. Abbruch statt Freigabe.")
            return treffer
    sys.exit(f"CODEOWNERS-Zeile fuer {CODEOWNERS_MATCH} am Base-Commit "
             f"{BASE_SHA[:7]} nicht gefunden. Abbruch statt Freigabe.")


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
        # CONTRACT_VERSION nur in Python-Quellen UNTER src/ werten. In Doku und
        # Berichten steht der Bezeichner als Prosa; und dieses Pruefskript selbst
        # nennt ihn ebenfalls — beides wuerde den PR sonst faelschlich rot faerben.
        or (f["filename"].startswith(SRC_PREFIX)
            and f["filename"].endswith(".py")
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
            + f"\n\nhead_sha: `{HEAD_SHA}`"
            f"\nCODEOWNERS gelesen am base_sha: `{BASE_SHA}`\n"
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
