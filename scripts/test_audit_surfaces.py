"""The surface audit fails on a banned claim and on a missing expertise area, and lets a negation through."""
import json, os, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def run(text):
    with tempfile.TemporaryDirectory() as t:
        os.makedirs(os.path.join(t, "x"))
        open(os.path.join(t, "x", "a.md"), "w").write(text)
        cfg = json.load(open(os.path.join(ROOT, "docs", "SURFACES.json")))
        cfg["surfaces"] = [{"id": "t", "local": "x/a.md", "areas": ["autonomous-ai", "governance"]}]
        os.makedirs(os.path.join(t, "docs")); os.makedirs(os.path.join(t, "scripts"))
        json.dump(cfg, open(os.path.join(t, "docs", "SURFACES.json"), "w"))
        open(os.path.join(t, "scripts", "audit_surfaces.py"), "w").write(open(os.path.join(ROOT, "scripts", "audit_surfaces.py")).read())
        return subprocess.run([sys.executable, os.path.join(t, "scripts", "audit_surfaces.py"), "--local", t, "--out", os.path.join(t, "o.json")], capture_output=True).returncode
good = "Autonomous AI systems researcher focused on governance and oversight. I am not a software engineer."
assert run(good) == 0, "good text passes"
assert run(good.replace("I am not a", "I am a")) == 1, "a banned self-description fails"
assert run("Autonomous AI systems researcher.") == 1, "a missing expertise area fails"
print("test_audit_surfaces: 3 passed")
