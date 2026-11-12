#!/usr/bin/env python3
"""RESUME-CLAIMS-1: fails when a resume claim Rowan answered "no" to is still in RESUME.md.

Reads docs/CLAIMS.json and the answers from jobs.q08.org/api/resume-claims (taps on fleet.qnfo.org/focus). An unreachable endpoint
or an unanswered claim never fails the build; it is reported. Unconfirmed claims stay listed until answered.
"""
import json, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = "https://qnfo-jobsearch.q08.workers.dev/api/resume-claims"

def check(claims, answers, resume):
    bad, open_ = [], []
    for c in claims:
        a = answers.get(c["ref"])
        if a == "no" and c["marker"] in resume:
            bad.append(c)
        elif a not in ("yes", "no"):
            open_.append(c["ref"])
    return bad, open_

def main():
    claims = json.loads((ROOT / "docs/CLAIMS.json").read_text(encoding="utf-8"))["claims"]
    resume = (ROOT / "RESUME.md").read_text(encoding="utf-8")
    try:
        with urllib.request.urlopen(URL, timeout=20) as r:
            answers = {x["ref"]: x["answer"] for x in json.load(r)["claims"]}
    except Exception as e:  # reported, not swallowed: the endpoint being down must not block the build
        print(f"claims_check: endpoint unreachable ({e}); answers not checked")
        answers = {}
    bad, open_ = check(claims, answers, resume)
    for c in bad:
        print(f"claims_check: {c['ref']} was answered no but RESUME.md still says: {c['marker']}")
    print(f"claims_check: {len(bad)} denied claim(s) still present, {len(open_)} unanswered")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
