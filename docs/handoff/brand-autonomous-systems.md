---
slug: brand-autonomous-systems
issue: (filed with the PR)
pr: (this PR)
status: in-progress
last_agent: claude-code
updated: 2026-11-09 13:45
---

## Goal and success metric
Goal: one source of truth for Rowan's brand as an autonomous AI systems researcher (not a software engineer). Metric: every surface listed in docs/BRAND.md section 8 uses the section 2 headline; `grep -ri "research systems builder"` across the surfaces returns nothing.

## Stage reached
research done, design done (docs/BRAND.md). Surface rollout not started.

## Decisions made (and why)
- Home is rwnq8/resume, not career-engine: career-engine is marked superseded.
- Headline "Autonomous AI systems researcher"; "AI safety" only as adjacent until there is direct safety work to cite.
- Quantum JPCUB work kept as published work, reframed through the agentic-inference paper.
- Unverified claims held in section 7, not used.

## What is next (single concrete step)
Owner confirms section 7, then apply section 8 surface by surface, CV first.

## How to verify
`grep -rli "research systems builder" RESUME.md README.md ../rwnq8/README.md ../rwnq8.github.io/index.html` returns no files once rollout is done.

## Open items
- Section 7 confirmations: owner.
- Surface rollout: claude-code; probe as above.
