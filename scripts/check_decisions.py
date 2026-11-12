#!/usr/bin/env python3
"""DURABLE-STORAGE-1 / INFO-USEFUL-1 check (practice what you preach: the record must hold what it claims).

Fails (exit 1) when:
  - a REQUIRED standing decision is missing from docs/DECISIONS.json, or has no text, date, source or home;
  - a home or ingest destination inside this repository does not exist or no longer contains its marker;
  - an ingest-log input has a fact with no destination, or an application lacks never_reshow;
  - an answer in docs/ANSWER-BANK.json is empty or calls Rowan an engineer.
Homes in other repositories are listed for the reader and are checked when --siblings DIR holds a checkout of them.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIRED = ["POSITIONING-1", "QUANTUM-OUTREACH-STOP-1", "CAREER-THREAD-1", "ULTRASTABLE-BRAND-1", "SURFACES-AUTOMATED-1",
            "PROMPTED-RECALL-1", "JOB-ENGINE-1", "CODE-IS-DONE-1", "PRACTICE-WHAT-YOU-PREACH-1", "DESIGN-STANDARD-1",
            "SESSION-HYGIENE-1", "PATENT-100-PAGES-1", "TOUCHPOINTS-1", "INFO-USEFUL-1", "DURABLE-STORAGE-1", "ANSWER-BANK-1"]
BANNED = re.compile(r"\b(software engineer|developer|coder|programmer)\b", re.I)


def load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def holds(home, siblings, errors, where):
    repo, path = home.get("repo"), home.get("path", "")
    if repo:
        if not siblings:
            return
        base = os.path.join(siblings, repo.split("/")[-1])
        fp = os.path.join(base, path.split(" ")[0])
        if os.path.isdir(base) and not os.path.exists(fp):
            errors.append(f"{where}: {repo}/{path.split(' ')[0]} does not exist")
        return
    fp = os.path.join(ROOT, path)
    if not os.path.exists(fp):
        errors.append(f"{where}: {path} does not exist")
        return
    marker = home.get("contains")
    if marker and marker not in open(fp, encoding="utf-8").read():
        errors.append(f"{where}: {path} no longer contains {marker!r}")


def main(argv):
    siblings = argv[argv.index("--siblings") + 1] if "--siblings" in argv else None
    errors = []
    dec = {d.get("id"): d for d in load("docs/DECISIONS.json")["decisions"]}
    for rid in REQUIRED:
        if rid not in dec:
            errors.append(f"decision {rid} is missing from docs/DECISIONS.json")
    for did, d in dec.items():
        for k in ("decision", "date", "source"):
            if not str(d.get(k, "")).strip():
                errors.append(f"decision {did}: no {k}")
        if not d.get("homes"):
            errors.append(f"decision {did}: no home")
        for h in d.get("homes", []):
            holds(h, siblings, errors, f"decision {did}")
    for inp in load("docs/INGEST-LOG.json")["inputs"]:
        if not inp.get("facts"):
            errors.append(f"ingest {inp.get('id')}: no facts drawn")
        for f in inp.get("facts", []):
            if not f.get("destinations"):
                errors.append(f"ingest {inp.get('id')}: fact {f.get('fact')!r} went nowhere")
            for h in f.get("destinations", []):
                holds(h, siblings, errors, f"ingest {inp.get('id')}")
    for a in load("docs/APPLICATIONS.json")["applications"]:
        if a.get("status") in ("applied", "dismissed") and a.get("never_reshow") is not True:
            errors.append(f"application {a.get('id')}: never_reshow is not set")
    for a in load("docs/ANSWER-BANK.json")["answers"]:
        if len(a.get("answer", "")) < 80:
            errors.append(f"answer {a.get('type')}: empty or too short")
        if BANNED.search(a.get("answer", "")):
            errors.append(f"answer {a.get('type')}: describes Rowan as an engineer")
    for e in errors:
        print("FAIL " + e)
    print(f"check_decisions: {len(dec)} decisions, {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
