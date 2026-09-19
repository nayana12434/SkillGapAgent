# 18-Hour Plan — Track C4 (Skill-Gap-to-Job Matching Agent)

Scope cut for time: 30–50 hardcoded job postings (JSON, not scraped) and a
~20-course curated catalog (Coursera/NPTEL/Skill India links pasted in
manually). No live scraping, no auth, single API endpoint.

## Roles (team of 4)
| Role | Owns |
|---|---|
| A — Backend/Orchestration | LangGraph graph.py, FastAPI, deployment |
| B — ML | Embedding matcher, gap-analysis LLM prompts |
| C — Frontend | Intake form, results page, calling the API |
| D — Data/Demo | jobs.json + courses.json curation, architecture diagram, video/pitch |

## Timeline
- **0–1 hr** — Confirm scope, split repo, agree on JSON schemas for
  Profile / Job / Gap / Recommendation. Push schemas first so everyone
  codes against the same shape.
- **1–4 hr** — Parallel build:
  - A: FastAPI skeleton + LangGraph skeleton (stub nodes returning fake data)
  - B: sentence-transformers matching on dummy data
  - C: intake form UI hitting a stubbed endpoint
  - D: finalize jobs.json (30–50 entries) + courses.json
- **4–8 hr** — Real logic: profile_parser (LLM extraction), job_matcher
  (real embeddings + ranking), first pass at gap_analyzer.
- **8–11 hr** — recommender node (gap → course mapping + ranking by jobs
  unlocked), wire full graph end-to-end.
- **11–13 hr** — Integrate frontend with real API, fix contract mismatches.
- **13–15 hr** — Testing with 5–10 sample profiles, tune prompts, handle
  edge cases (empty resume, no matches).
- **15–16.5 hr** — Polish UI, error states, architecture diagram (draw.io).
- **16.5–18 hr** — Record 3-min demo video, write submission doc, final
  push.

## Deliverables checklist (from problem statement)
- [ ] Functional app link/demo
- [ ] Prompt documentation (Google AI Studio / LLM prompts used)
- [ ] System architecture diagram
- [ ] 3-minute video demo
