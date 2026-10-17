"""
Matches a user's profile with suitable jobs using lightweight
skill and keyword matching.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List


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

    return " ".join(
        str(skill).lower().strip().split()
    )


def skill_matches(user_skill: str, required_skill: str) -> bool:
    """
    Check whether two skills are similar using
    lightweight substring matching.
    """

    user_skill = normalize_skill(user_skill)
    required_skill = normalize_skill(required_skill)

    if not user_skill or not required_skill:
        return False

    # Exact match
    if user_skill == required_skill:
        return True

    # Substring match
    if user_skill in required_skill:
        return True

    if required_skill in user_skill:
        return True

    # Handle common separators
    user_words = set(re.findall(r"[a-z0-9+#.]+", user_skill))
    required_words = set(
        re.findall(r"[a-z0-9+#.]+", required_skill)
    )

    return bool(user_words & required_words)


def missing_skills_for(
    user_skills: List[str],
    required_skills: List[str],
) -> List[str]:
    """
    Find required skills that the user does not have.
    """

    missing = []

    for required_skill in required_skills:

        found = any(
            skill_matches(user_skill, required_skill)
            for user_skill in user_skills
        )

        if not found:
            missing.append(required_skill)

    return missing


def calculate_match_score(
    user_skills: List[str],
    user_interests: List[str],
    required_skills: List[str],
    description: str,
) -> float:
    """
    Calculate a lightweight job match score.

    The score considers:
    - Matching required skills
    - User interests
    - Relevant keywords in the job description
    """

    if not required_skills:
        return 0.0

    matched_count = 0

    for required_skill in required_skills:
        if any(
            skill_matches(user_skill, required_skill)
            for user_skill in user_skills
        ):
            matched_count += 1

    skill_score = matched_count / len(required_skills)

    # Check whether interests appear in the job information.
    job_text = normalize_skill(
        " ".join(required_skills) + " " + description
    )

    interest_matches = 0

    for interest in user_interests:
        interest = normalize_skill(interest)

        if interest and interest in job_text:
            interest_matches += 1

    if user_interests:
        interest_score = (
            interest_matches / len(user_interests)
        )
    else:
        interest_score = 0.0

    # Skills are more important than interests.
    final_score = (
        skill_score * 0.8
        + interest_score * 0.2
    )

    return round(final_score, 3)


def match_jobs(
    profile: Dict[str, Any],
    jobs_path: str = "data/jobs.json",
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Match the user's profile against jobs using
    lightweight skill matching.
    """

    if not isinstance(profile, dict):
        raise TypeError(
            "Profile must be provided as a dictionary."
        )

    user_skills = profile.get("skills", []) or []
    user_interests = profile.get("interests", []) or []

    jobs = load_jobs(jobs_path)

    if not jobs:
        return []

    matched_jobs = []

    for job in jobs:

        required_skills = (
            job.get("required_skills", []) or []
        )

        description = (
            job.get("description") or ""
        )

        score = calculate_match_score(
            user_skills,
            user_interests,
            required_skills,
            description,
        )

        matched_jobs.append(
            {
                "job": job,
                "match_score": score,
                "missing_skills": missing_skills_for(
                    user_skills,
                    required_skills,
                ),
            }
        )

    # Highest scores first.
    matched_jobs.sort(
        key=lambda item: item["match_score"],
        reverse=True,
    )

    return matched_jobs[:top_k]