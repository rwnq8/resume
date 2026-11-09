---
slug: autonomous-systems-rebrand
issue: none (owner request in the Personal Brand project, 2026-11-09)
pr: see branch claude/project-thread-26so28
status: in-progress
last_agent: claude-code
updated: 2026-11-09 13:40
---

## Goal and success metric
Position Rowan as a systems researcher in autonomous AI systems (not a software engineer, not quantum-first) on the CV, portfolio, skills page and LinkedIn package.
Metric: replies and interviews from autonomous-systems and AI-safety-adjacent applications, read from jobs.q08.org `GET /api/outcomes` (the job search worker in QNFO/qnfo-workers).

## Stage reached
define, design, build done; PDF rebuilt (v5.0). Deploy is the owner's merge; LinkedIn is applied by the owner (no profile-write API).

## Decisions made (and why)
- Headline "Systems researcher · Autonomous AI systems" (owner, 2026-11-09).
- Network-modeling thread from the first transport role (2004) through the FHWA Tour-Based Model System is owner-stated; the FHWA bullet now calls that model a network model of long-distance travel.
- Programming languages removed from skills: the owner states that they do not write software. "Built" became "Led" for the Empowering Change LLM tool for the same reason.
- Quantum papers dropped from Selected Work and LinkedIn Featured; JPCUB kept through its agentic-inference extension.
- No new claims: every bullet is in the v4.0 verified CV or was stated by the owner on 2026-11-09.

## What is next (single concrete step)
- Owner reviews and merges; then apply `linkedin-profile-update.json` with `linkedin-apply-profile.py`.

## How to verify
`grep -i quantum RESUME.md` returns nothing; `pdftotext rowan-quni-cv-v5.0.pdf - | head -3` shows the new headline.

## Open items
- Website and GitHub profile copy: sibling thread "Rebrand website and GitHub profiles".
