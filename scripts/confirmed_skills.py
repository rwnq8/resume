"""Write the skills Rowan confirmed by tap into RESUME.md (JOBSEARCH-SKILLS-1).

Reads the open endpoint GET https://jobs.q08.org/api/cv-skills (qnfo-jobsearch). Only skills whose prompted-recall card
Rowan answered "yes" on fleet.qnfo.org/focus or jobs.q08.org are listed; a later "no" removes the line on the next run.
Usage: python scripts/confirmed_skills.py [--file data.json]  (exit 0 always; prints "changed" when RESUME.md changed)
"""
import json, re, sys, urllib.request

URL = "https://jobs.q08.org/api/cv-skills"
START, END = "<!-- CONFIRMED-SKILLS:START", "<!-- CONFIRMED-SKILLS:END -->"


def block(data):
    rows = [c for c in data.get("confirmed", []) if c.get("skill") and c.get("text")]
    if not rows:
        return ""
    lines = ["**Confirmed by Rowan:** " + " · ".join(c["skill"] for c in rows), ""]
    lines += ["- " + c["text"] + " (confirmed by owner, " + c.get("confirmed_at", "") + ")" for c in rows]
    return "\n".join(lines) + "\n"


def render(text, data):
    i, j = text.find(START), text.find(END)
    if i < 0 or j < i:
        raise SystemExit("RESUME.md has no CONFIRMED-SKILLS markers")
    head_end = text.index("-->", i) + 3
    return text[:head_end] + "\n" + block(data) + text[j:]


def main():
    if "--file" in sys.argv:
        data = json.load(open(sys.argv[sys.argv.index("--file") + 1]))
    else:
        req = urllib.request.Request(URL, headers={"User-Agent": "resume-confirmed-skills"})
        data = json.load(urllib.request.urlopen(req, timeout=30))
    if data.get("schema_version") != "cv-skills/v1":
        raise SystemExit("unexpected answer from " + URL)
    old = open("RESUME.md", encoding="utf-8").read()
    new = render(old, data)
    if new != old:
        open("RESUME.md", "w", encoding="utf-8").write(new)
        print("changed")


if __name__ == "__main__":
    main()
