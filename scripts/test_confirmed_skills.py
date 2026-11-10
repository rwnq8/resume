import importlib.util, os
spec = importlib.util.spec_from_file_location("cs", os.path.join(os.path.dirname(__file__), "confirmed_skills.py"))
cs = importlib.util.module_from_spec(spec); spec.loader.exec_module(cs)
md = "a\n" + cs.START + " note -->\n" + cs.END + "\nb\n"
one = {"confirmed": [{"skill": "People management", "text": "Managed people.", "confirmed_at": "2026-11-10"}]}
out = cs.render(md, one)
assert "**Confirmed by Rowan:** People management" in out and "(confirmed by owner, 2026-11-10)" in out
assert cs.render(out, {"confirmed": []}) == md, "a no removes the line"
assert cs.render(cs.render(md, one), one) == out, "idempotent"
real = open(os.path.join(os.path.dirname(__file__), "..", "RESUME.md"), encoding="utf-8").read()
assert cs.START in real and cs.END in real
print("confirmed_skills: ok")
