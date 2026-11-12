"""The decisions check fails when a decision or a logged destination goes missing (it is not a check that always passes)."""
import json, os, shutil, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(mutate):
    with tempfile.TemporaryDirectory() as t:
        for p in ["docs", "scripts", ".github"]:
            shutil.copytree(os.path.join(ROOT, p), os.path.join(t, p))
        for f in ["AGENTS.md", "RESUME.md", "linkedin-profile-update.json"]:
            shutil.copy(os.path.join(ROOT, f), t)
        mutate(t)
        return subprocess.run([sys.executable, os.path.join(t, "scripts", "check_decisions.py")], capture_output=True, text=True).returncode

def drop_decision(t):
    p = os.path.join(t, "docs", "DECISIONS.json"); d = json.load(open(p))
    d["decisions"] = [x for x in d["decisions"] if x["id"] != "INFO-USEFUL-1"]; json.dump(d, open(p, "w"))

def drop_fact(t):
    p = os.path.join(t, "RESUME.md"); s = open(p).read().replace("proxy quality signals", "quality signals"); open(p, "w").write(s)

assert run(lambda t: None) == 0, "clean tree passes"
assert run(drop_decision) == 1, "a missing decision fails"
assert run(drop_fact) == 1, "a logged fact missing from its destination fails"
print("test_check_decisions: 3 passed")
