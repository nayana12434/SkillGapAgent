<<<<<<< HEAD
# SkillGapAgent
Capabl AI hackathon project
=======
# SkillBridge — Skill-Gap-to-Job Matching Agent
Capabl AI Hackathon 2026 — Track C4

Compares a candidate's skills against local job postings, finds specific
gaps, and recommends a ranked training path to close them.

## Pipeline (LangGraph)
`profile_parser → job_matcher → gap_analyzer → recommender`

1. **profile_parser** — extracts structured skills/education/location from
   free-text resume or form input (LLM-based extraction).
2. **job_matcher** — embeds candidate skills + job postings
   (sentence-transformers), returns top-N matches by cosine similarity.
3. **gap_analyzer** — LLM diff between candidate skills and each matched
   job's required skills → specific missing-skill list.
4. **recommender** — maps each gap to a real course from the curated
   catalog, ranked by "jobs unlocked."

## Repo layout
```
agents/       LangGraph nodes: profile_parser.py, job_matcher.py,
              gap_analyzer.py, recommender.py, graph.py (wires them up)
api/          FastAPI app exposing POST /analyze
data/         jobs.json (30–50 curated postings), courses.json
frontend/     minimal form + results UI
docs/         architecture diagram, demo script
```

## Setup
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload
```

## Team roles
- **Backend/orchestration** — LangGraph pipeline, FastAPI, agent wiring
- **ML** — embedding matching, gap-analysis prompts
- **Frontend** — intake form, results view
- **Data/demo** — job+course dataset, architecture diagram, pitch video

See `docs/plan.md` for the 18-hour schedule.
>>>>>>> 1213305 (Add SkillBridge project files)
