"""
Matches a user's profile with suitable jobs using sentence embeddings.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

from sentence_transformers import SentenceTransformer, util


# Lazy-loaded model.
# The model loads only when the first matching request is made.
_model = None


def get_model() -> SentenceTransformer:
    """
    Load the embedding model only once.
    """

    global _model

    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    return _model


def load_jobs(
    jobs_path: str = "data/jobs.json",
) -> List[Dict[str, Any]]:
    """
    Load job postings from the JSON dataset.
    """

    path = Path(jobs_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Job dataset not found: {jobs_path}"
        )

    with path.open("r", encoding="utf-8") as file:
        jobs = json.load(file)

    if not isinstance(jobs, list):
        raise ValueError(
            "The jobs dataset must contain a list of jobs."
        )

    return jobs


def normalize_skill(skill: str) -> str:
    """
    Normalize a skill for comparison.
    """

    return " ".join(skill.lower().strip().split())


def missing_skills_for(
    user_skills: List[str],
    required_skills: List[str],
) -> List[str]:
    """
    Find required skills that the user does not have.

    This exact-match comparison is retained for transparency
    and for use by the skill-gap analyzer.
    """

    normalized_user = {
        normalize_skill(skill)
        for skill in user_skills
    }

    return [
        skill
        for skill in required_skills
        if normalize_skill(skill) not in normalized_user
    ]


def match_jobs(
    profile: Dict[str, Any],
    jobs_path: str = "data/jobs.json",
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Match the user's profile against jobs using embedding similarity.

    The user's skills and interests are compared with each job's
    required skills and description.
    """

    if not isinstance(profile, dict):
        raise TypeError(
            "Profile must be provided as a dictionary."
        )

    user_skills = profile.get("skills", []) or []
    user_interests = profile.get("interests", []) or []

    profile_text = ", ".join(
        user_skills + user_interests
    ) or "general"

    jobs = load_jobs(jobs_path)

    if not jobs:
        return []

    model = get_model()

    # Convert the user's skills and interests into an embedding.
    profile_embedding = model.encode(
        profile_text,
        convert_to_tensor=True,
    )

    # Create a text representation for every job.
    job_texts = []

    for job in jobs:
        required_skills = job.get("required_skills", []) or []
        description = job.get("description") or ""

        job_text = (
            ", ".join(required_skills)
            + ". "
            + description
        )

        job_texts.append(job_text)

    # Convert all jobs into embeddings.
    job_embeddings = model.encode(
        job_texts,
        convert_to_tensor=True,
    )

    # Calculate semantic similarity scores.
    similarities = util.cos_sim(
        profile_embedding,
        job_embeddings,
    )[0]

    matched_jobs = []

    for job, similarity in zip(jobs, similarities):
        required_skills = job.get("required_skills", []) or []

        matched_jobs.append(
            {
                "job": job,
                "match_score": round(
                    float(similarity),
                    3,
                ),
                "missing_skills": missing_skills_for(
                    user_skills,
                    required_skills,
                ),
            }
        )

    # Highest similarity scores appear first.
    matched_jobs.sort(
        key=lambda item: item["match_score"],
        reverse=True,
    )

    return matched_jobs[:top_k]