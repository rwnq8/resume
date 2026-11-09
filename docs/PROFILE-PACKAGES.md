# Ready-to-paste profile packages

Status: 2026-11-09. Every line below is copied from `docs/BRAND.md` and the verified record (`RESUME.md`, `linkedin-profile-update.json`). These are the surfaces no agent can edit (no write API or no connector), so each block is ready to paste as is. Character counts are measured against each site's limit.

When a surface is updated, tick it in the table at the end, so the next session knows what is live.

---

## 1. LinkedIn

The full machine-readable package is `linkedin-profile-update.json` (headline, About, every experience entry, skills, featured). It can be applied in a signed-in browser with `linkedin-apply-profile.py`. The two fields that matter most:

**Headline** (156 of 220 characters)
```
Autonomous AI systems researcher · How agentic systems behave, fail and are governed · 20 years of network and systems modeling (FHWA, AARP) · Founder, QNFO
```

**About**: copy the `about` field of `linkedin-profile-update.json` (1,501 of 2,600 characters).

**Current position title**: `Founder and Systems Researcher`, company line `QNFO (independent research on autonomous AI systems)`.

**Open to work, job titles** (from BRAND.md section 8): Autonomous Systems Researcher · AI Systems Researcher · AI Evaluation and Assurance · AI Governance Research · Research Program Manager, AI

---

## 2. GitHub

**Profile bio** (154 of 160 characters), at github.com/settings/profile
```
Autonomous AI systems researcher. How agentic systems behave, fail and are governed. 20 years of network and systems modeling (FHWA, AARP). Founder, QNFO.
```

**Repository About descriptions** (gear icon next to "About" on each repository page). Current text was read on 2026-11-09.

| Repository | Current About | Paste this |
|:--|:--|:--|
| rwnq8/resume | "Research & Technology Leader \| Quantum Computing, AI, National-Scale Systems" | `CV and portfolio of Rowan Brad Quni-Gudzinas, autonomous AI systems researcher: 20 years of network and systems modeling (FHWA, AARP) leading to research on how autonomous AI systems behave, fail and are governed.` |
| rwnq8/rwnq8 | (empty) | `Profile of Rowan Brad Quni-Gudzinas, autonomous AI systems researcher.` |
| rwnq8/.github | "personal GitHub profile" | `Profile of Rowan Brad Quni-Gudzinas, autonomous AI systems researcher.` |
| rwnq8/rwnq8.github.io | (empty) | `Personal site of Rowan Brad Quni-Gudzinas, autonomous AI systems researcher: career record, selected work and a sourced description for AI systems.` |
| rwnq8/agent-operating-system | (empty) | `One written agreement that keeps autonomous coding agents from different vendors inside the same limits, with human oversight. Part of Rowan Quni-Gudzinas's autonomous AI systems research.` |
| rwnq8/AIOS | "AI-Driven Operating System Kernel ..." | `Design experiment in autonomous AI systems: how far a local, offline AI can take itself from bare hardware to a working OS, and which safety gates keep that autonomy accountable.` |
| rwnq8/career-engine | (empty) | `Retired prototype of a prompted-recall CV and job-matching tool; superseded by jobs.q08.org.` |
| rwnq8/ipatent | "Leverage AI to analyze disclosures ..." | `LLM-assisted prior-art and patentability analysis prototype. Reports are machine-generated and are not legal advice.` |
| QNFO/qnfo-research | "QNFO Research Artifacts ..." | `Published papers and full provenance of an autonomous AI research pipeline: drafts, adversarial reviews, verification runs and failure records.` |

**Topics** to add on the profile, site and resume repositories: `autonomous-systems`, `ai-agents`, `ai-governance`, `ai-evaluation`, `systems-research`.

**Pinned repositories** (Customize your pins on the profile page): resume, agent-operating-system, AIOS, solo-scientist, qwav-research-pipeline, joules-per-compute-benchmark. These show the autonomous-systems thread first; the physics repositories stay public but unpinned.

---

## 3. ORCID (orcid.org, signed in)

**Biography**
```
Rowan Quni-Gudzinas is a systems researcher focused on autonomous AI systems: how they behave, fail and can be audited and governed. Their career began in transportation network modeling, continued with a national travel forecasting model for the U.S. Federal Highway Administration and a data-driven national decision tool at AARP, and now centres on autonomous AI. As founder of QNFO, Rowan runs an autonomous research system in production and publishes its objectives, costs and failure record openly. Earlier work is published under Brad Gudzinas.
```

**Keywords**
```
autonomous AI systems, agentic systems, systems research, AI evaluation and auditability, AI governance and oversight, network modeling, travel demand modeling, evidence-based decision systems
```

Other ORCID fixes (other names, employment history, public email) are listed in `rwnq8/rwnq8.github.io` `ORCID-UPDATE-SPEC.md`.

---

## 4. Google Scholar (scholar.google.com/citations?user=eHIbqxkAAAAJ, Edit profile)

**Affiliation**
```
Autonomous AI systems researcher, QNFO
```

**Areas of interest** (five fields)
```
Autonomous AI systems
AI evaluation
AI governance
Network modeling
Travel demand modeling
```

**Homepage**: `https://rwnq8.github.io/`

---

## 5. X and Bluesky

**X bio** (149 of 160 characters)
```
Autonomous AI systems researcher: how agentic systems behave, fail and are governed. 20 yrs network and systems modeling (FHWA, AARP). Founder, QNFO.
```

**Bluesky bio** (233 of 256 characters)
```
Autonomous AI systems researcher. I study how agentic AI systems behave, fail and can be audited and governed, building on 20 years of network and systems modeling for the U.S. Federal Highway Administration and AARP. Founder, QNFO.
```

**Website field** on both: `https://rwnq8.github.io/`

---

## 6. Email signature (Gmail, Settings, Signature)

```
Rowan Brad Quni-Gudzinas
Autonomous AI systems researcher · Founder, QNFO
https://rwnq8.github.io · ORCID 0009-0002-4317-5604
```

---

## 7. Which connectors would let agents apply these

| Surface | What would unlock it |
|:--|:--|
| GitHub About, topics, profile bio | A GitHub token with repository administration and user profile scope in the fleet's secret store (the cloud session's GitHub tools cannot edit repository settings). The REST endpoints exist (`PATCH /repos/{o}/{r}`, `PATCH /user`). |
| LinkedIn | No public profile-write API. Applying needs a signed-in browser: Claude in Chrome on Rowan's computer, running `linkedin-apply-profile.py` or the steps by hand. |
| ORCID | The ORCID Member API is for member institutions only; same signed-in browser route as LinkedIn. |
| Google Scholar | No API; signed-in browser only. |
| X and Bluesky | Bluesky's AT Protocol allows a profile update with an app password; X's API v1.1 `account/update_profile` needs a paid developer tier. |
| Gmail signature | The Gmail connector here has no settings scope; signed-in browser only. |

## 8. Applied

| Surface | Applied on | By |
|:--|:--|:--|
| LinkedIn headline and About | | |
| GitHub bio, About lines, topics, pins | | |
| ORCID | | |
| Google Scholar | | |
| X | | |
| Bluesky | | |
| Gmail signature | | |
