#!/usr/bin/env python3
"""STYLE-LINT-1 for the resume: fails on the tells of machine-written prose.

The word and phrase lists mirror styleLint in QNFO/qnfo-workers qnfo-jobsearch/worker.js (which checks drafted answers); change both together.
Usage: python3 scripts/style_lint.py [file ...]   (default RESUME.md docs/BRAND.md is not linted: it is an internal brief)
"""
import re, sys, pathlib

WORDS = re.compile(
    r"\b(?:leverag(?:e|es|ed|ing)|delv(?:e|es|ed|ing)|tapestry|testament|spearhead(?:s|ed|ing)?|synerg(?:y|ies|istic)|cutting[- ]edge|"
    r"state[- ]of[- ]the[- ]art|robust|seamless(?:ly)?|holistic(?:ally)?|passionate|game[- ]chang(?:er|ing)|fast[- ]paced|ever[- ]evolving|myriad|"
    r"pivotal|underscor(?:e|es|ed|ing)|showcas(?:e|es|ed|ing)|realm|endeavou?rs?|thrilled|unlock(?:s|ed|ing)?|elevat(?:e|es|ed|ing)|"
    r"foster(?:s|ed|ing)?|landscape|paradigm|multifaceted|nuanced|commendable|meticulous(?:ly)?|dynamic (?:environment|team)|"
    r"proven track record|results[- ]driven|detail[- ]oriented|team player|hit the ground running|deeply committed|excited (?:to|about|by))\b", re.I)
PHRASES = [
    (re.compile(r"—|–(?=\s)|\s--\s"), "dash used as a pause"),
    (re.compile(r"\bnot (?:just|only|merely)\b[^.?!]{0,80}\bbut (?:also )?\b", re.I), "not-just-but construction"),
    (re.compile(r"\bplays? a (?:crucial|vital|key|pivotal) role\b", re.I), "stock phrase: plays a role"),
    (re.compile(r"\bbridg(?:e|ing) the gap\b|\bbest practices\b|\bstakeholder alignment\b|\bdrive(?:s|n)? (?:innovation|impact|results)\b", re.I), "consulting filler"),
]

def lint(text):
    out = []
    # drop link targets and code so URLs do not trip the dash rule
    t = re.sub(r"\]\([^)]*\)", "]", text)
    for lineno, line in enumerate(t.splitlines(), 1):
        for m in {m.group(0).lower() for m in WORDS.finditer(line)}:
            out.append(f"L{lineno}: stock word: {m}")
        for rx, label in PHRASES:
            if rx.search(line):
                out.append(f"L{lineno}: {label}")
    return out

if __name__ == "__main__":
    files = sys.argv[1:] or ["RESUME.md"]
    bad = 0
    for f in files:
        issues = lint(pathlib.Path(f).read_text(encoding="utf-8"))
        for i in issues:
            print(f"{f}: {i}")
        bad += len(issues)
    print(f"style_lint: {bad} issue(s)")
    sys.exit(1 if bad else 0)
