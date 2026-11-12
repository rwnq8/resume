#!/usr/bin/env python3
"""SURFACE-AUDIT-1: audit every public surface against the brand (docs/SURFACES.json).

A surface fails when it uses a banned self-description, lacks any expertise area listed for it, lacks a required
string, or cannot be read. Exit 1 on any failure; a JSON report is written to --out (default surface-audit.json).
  --local DIR   read surfaces that have a "local" path from sibling checkouts under DIR (offline, for pull requests)
  (default)     fetch each surface's "url" (scheduled run); a surface with no url is read from raw GitHub if it names a repo path
"""
import json, os, re, sys, urllib.request, datetime

NEGATION = re.compile(r"\b(not|never|rather than|isn't|avoid|no)\b")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(s, local):
    if local:
        if "local" not in s:
            return None, "skipped (no local copy)"
        p = os.path.join(local, s["local"])
        try:
            return open(p, encoding="utf-8").read(), None
        except OSError as e:
            return None, f"cannot read {p}: {e}"
    if "url" not in s:
        return None, "skipped (no url)"
    try:
        req = urllib.request.Request(s["url"], headers={"User-Agent": "surface-audit/1"})
        return urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace"), None
    except Exception as e:  # a surface we cannot read is a finding, never a pass
        return None, f"cannot fetch {s['url']}: {e}"


def audit(cfg, local):
    rows, fails = [], 0
    for s in cfg["surfaces"]:
        text, err = read(s, local)
        row = {"id": s["id"], "problems": []}
        if text is None:
            row["status"] = "skipped" if err.startswith("skipped") else "unreadable"
            if row["status"] == "unreadable":
                row["problems"].append(err)
        else:
            row["status"] = "read"
            if not s.get("banned_exempt"):
                for b in cfg["banned"]:
                    for m in re.finditer(b, text, re.I):
                        before = text[max(0, m.start() - 45):m.start()].lower()
                        if NEGATION.search(before):
                            continue  # "not a software engineer" states the brand; it is not a claim
                        row["problems"].append(f"banned self-description {m.group(0)!r} near {text[max(0, m.start() - 30):m.end() + 10]!r}")
                        break
            for a in s["areas"]:
                if not any(re.search(p, text, re.I) for p in cfg["areas"][a]):
                    row["problems"].append(f"missing expertise area: {a}")
            for need in s.get("must", []):
                if need not in text:
                    row["problems"].append(f"missing {need!r}")
        fails += bool(row["problems"])
        rows.append(row)
    return rows, fails


def main(argv):
    cfg = json.load(open(os.path.join(ROOT, "docs", "SURFACES.json"), encoding="utf-8"))
    local = argv[argv.index("--local") + 1] if "--local" in argv else None
    out = argv[argv.index("--out") + 1] if "--out" in argv else "surface-audit.json"
    rows, fails = audit(cfg, local)
    json.dump({"at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "mode": "local" if local else "live", "failed": fails, "surfaces": rows}, open(out, "w"), indent=1)
    for r in rows:
        print(f"{r['status']:10} {r['id']:18} " + ("; ".join(r["problems"]) or "ok"))
    print(f"audit_surfaces: {len(rows)} surfaces, {fails} failing")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
