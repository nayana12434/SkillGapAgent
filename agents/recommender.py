"""
Maps skill gaps to relevant courses and ranks them
based on how many skill gaps each course covers.
"""

import json
from pathlib import Path
from typing import Any, Dict, List


def normalize_skill(skill: str) -> str:
    """Normalizes skill names for comparison."""
    return " ".join(str(skill).lower().strip().split())


def skills_overlap(gap_skill: str, course_skill: str) -> bool:
    """
    Checks whether two skills match using normalized
    exact or substring-based matching.

    Examples:
        React      <-> React.js
        Docker     <-> Docker Fundamentals
        FastAPI    <-> FastAPI framework
    """
    a = normalize_skill(gap_skill)
    b = normalize_skill(course_skill)

    if not a or not b:
        return False

    return a == b or a in b or b in a


def extract_gap_skills(gaps: List[Any]) -> List[str]:
    """Extracts skill names from skill-gap results (strings or dicts)."""
    extracted_skills = []

    for gap in gaps or []:
        if isinstance(gap, str):
            extracted_skills.append(gap)
        elif isinstance(gap, dict):
            skill = gap.get("skill")
            if skill:
                extracted_skills.append(str(skill))

    return [
        normalize_skill(skill)
        for skill in extracted_skills
        if normalize_skill(skill)
    ]


def extract_course_skills(course: Dict[str, Any]) -> List[str]:
    """Extracts skills covered by a course."""
    possible_fields = ["skills", "teaches", "related_skills", "covered_skills"]

    for field in possible_fields:
        skills = course.get(field)

        if isinstance(skills, list):
            return [
                normalize_skill(skill)
                for skill in skills
                if normalize_skill(skill)
            ]

        if isinstance(skills, str):
            normalized_skill = normalize_skill(skills)
            if normalized_skill:
                return [normalized_skill]

    return []


def recommend_courses(
    gaps: List[Any],
    courses: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Recommends courses based on identified skill gaps.
    Courses are ranked by how many gaps they cover.
    """

    print("[DEBUG] recommend_courses called")
    print("[DEBUG] raw gaps:", gaps)
    print("[DEBUG] number of courses:", len(courses or []))

    gap_skills = extract_gap_skills(gaps)
    print("[DEBUG] normalized gap_skills:", gap_skills)

    recommendations = []

    if not gap_skills:
        print("[DEBUG] no gap skills — returning []")
        return []

    for course in courses or []:
        course_skills = extract_course_skills(course)

        covered_skills = [
            gap_skill
            for gap_skill in gap_skills
            if any(skills_overlap(gap_skill, cs) for cs in course_skills)
        ]

        unique_covered = list(dict.fromkeys(covered_skills))

        print(
            f"[DEBUG] course '{course.get('title')}' skills={course_skills} "
            f"-> covered={unique_covered}"
        )

        if unique_covered:
            recommendation = dict(course)
            recommendation["covered_skills"] = sorted(unique_covered)
            recommendation["coverage_count"] = len(unique_covered)
            recommendations.append(recommendation)

    recommendations.sort(key=lambda item: item["coverage_count"], reverse=True)
    print("[DEBUG] final recommendation count:", len(recommendations))

    return recommendations