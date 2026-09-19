"""
Maps skill gaps to relevant courses and ranks them
based on how many skill gaps each course covers.
"""

import json
from pathlib import Path
from typing import Any, Dict, List


def load_courses(
    courses_path: str = "data/courses.json",
) -> List[Dict[str, Any]]:
    """Loads courses from the JSON dataset."""

    path = Path(courses_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Course dataset not found: {courses_path}"
        )

    with path.open("r", encoding="utf-8") as file:
        courses = json.load(file)

    if not isinstance(courses, list):
        raise ValueError("The courses dataset must contain a list.")

    return courses


def normalize_skill(skill: str) -> str:
    """Normalizes skill names for comparison."""

    return " ".join(str(skill).lower().strip().split())


def extract_gap_skills(gaps: List[Any]) -> List[str]:
    """Extracts skill names from skill-gap results."""

    extracted_skills = []

    for gap in gaps:
        if isinstance(gap, str):
            extracted_skills.append(gap)

        elif isinstance(gap, dict):
            skill = gap.get("skill")

            if skill:
                extracted_skills.append(skill)

    return [
        normalize_skill(skill)
        for skill in extracted_skills
    ]


def extract_course_skills(course: Dict[str, Any]) -> List[str]:
    """Extracts skills covered by a course."""

    possible_fields = [
        "skills",
        "teaches",
        "related_skills",
        "covered_skills",
    ]

    for field in possible_fields:
        skills = course.get(field)

        if isinstance(skills, list):
            return [
                normalize_skill(skill)
                for skill in skills
            ]

        if isinstance(skills, str):
            return [normalize_skill(skills)]

    return []


def recommend_courses(
    gaps: List[Any],
    courses: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Recommends courses based on identified skill gaps.

    Courses are ranked by the number of skill gaps they cover.
    """

    gap_skills = set(extract_gap_skills(gaps))
    recommendations = []

    if not gap_skills:
        return []

    for course in courses:
        course_skills = set(extract_course_skills(course))
        covered_skills = gap_skills.intersection(course_skills)

        if covered_skills:
            recommendation = dict(course)

            recommendation["covered_skills"] = sorted(
                covered_skills
            )

            recommendation["coverage_count"] = len(
                covered_skills
            )

            recommendations.append(recommendation)

    recommendations.sort(
        key=lambda item: item["coverage_count"],
        reverse=True,
    )

    return recommendations


if __name__ == "__main__":
    sample_gaps = [
        {"skill": "SQL"},
        {"skill": "Excel"},
        {"skill": "Power BI"},
    ]

    available_courses = load_courses()

    results = recommend_courses(
        gaps=sample_gaps,
        courses=available_courses,
    )

    print("Recommended Courses:")

    if not results:
        print("No matching courses found.")

    else:
        for course in results:
            print(
                f"\nCourse: "
                f"{course.get('title', course.get('name', 'Untitled'))}"
            )
            print(
                f"Covered skills: "
                f"{course['covered_skills']}"
            )
            print(
                f"Coverage count: "
                f"{course['coverage_count']}"
            )