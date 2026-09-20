"""
Connects all SkillBridge agents into one LangGraph pipeline.

Pipeline:
Profile Parser
      ↓
Job Matcher
      ↓
Skill Gap Analyzer
      ↓
Course Recommender
"""

import json
from pathlib import Path
from typing import Any, TypedDict

from langgraph.graph import StateGraph, START, END

from agents.profile_parser import parse_profile
from agents.job_matcher import match_jobs
from agents.gap_analyzer import analyze_gaps
from agents.recommender import recommend_courses 


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

JOBS_PATH = BASE_DIR / "data" / "jobs.json"
COURSES_PATH = BASE_DIR / "data" / "courses.json"


class PipelineState(TypedDict, total=False):
    raw_text: str
    profile: dict[str, Any]
    matched_jobs: list[dict[str, Any]]
    skill_gaps: list[dict[str, Any]]
    recommendations: list[dict[str, Any]]


def load_courses() -> list[dict[str, Any]]:
    """Load courses from the course dataset."""

    if not COURSES_PATH.exists():
        raise FileNotFoundError(
            f"Course dataset not found: {COURSES_PATH}"
        )

    with COURSES_PATH.open("r", encoding="utf-8") as file:
        courses = json.load(file)

    if not isinstance(courses, list):
        raise ValueError("The courses dataset must contain a list.")

    return courses


def profile_parser_node(state: PipelineState) -> dict:
    """Extract structured information from the user's input."""

    raw_text = state.get("raw_text", "").strip()

    if not raw_text:
        raise ValueError("User profile text cannot be empty.")

    profile = parse_profile(raw_text)

    return {
        "profile": profile
    }


def job_matcher_node(state: PipelineState) -> dict:
    """Match the user's profile with suitable jobs."""

    profile = state.get("profile", {})

    matched_jobs = match_jobs(
        profile=profile,
        jobs_path=str(JOBS_PATH),
        top_k=5,
    )

    return {
        "matched_jobs": matched_jobs
    }


def skill_gap_node(state: PipelineState) -> dict:
    """Identify missing skills for the matched jobs."""

    profile = state.get("profile", {})
    matched_jobs = state.get("matched_jobs", [])

    skill_gaps = analyze_gaps(
        profile=profile,
        matched_jobs=matched_jobs,
    )

    return {
        "skill_gaps": skill_gaps
    }


def recommender_node(state: PipelineState) -> dict:
    """Recommend courses based on the identified skill gaps."""

    skill_gaps = state.get("skill_gaps", [])
    courses = load_courses()

    # Convert skill-gap dictionaries into skill names
    gap_skills = []

    for gap in skill_gaps:
        if isinstance(gap, dict):
            skill = gap.get("skill")

            if skill:
                gap_skills.append(skill)

        elif isinstance(gap, str):
            gap_skills.append(gap)
    print("ABOUT TO CALL RECOMMENDER")
    print("recommender function:",recommend_courses)

    recommendations = recommend_courses(
        gaps=gap_skills,
        courses=courses,
    )
    print("FInished")
    return {
        "recommendations": recommendations
    }


def build_graph():
    """Build and compile the complete SkillBridge pipeline."""

    workflow = StateGraph(PipelineState)

    workflow.add_node("profile_parser", profile_parser_node)
    workflow.add_node("job_matcher", job_matcher_node)
    workflow.add_node("skill_gap_analyzer", skill_gap_node)
    workflow.add_node("recommender", recommender_node)

    workflow.add_edge(START, "profile_parser")
    workflow.add_edge("profile_parser", "job_matcher")
    workflow.add_edge("job_matcher", "skill_gap_analyzer")
    workflow.add_edge("skill_gap_analyzer", "recommender")
    workflow.add_edge("recommender", END)

    return workflow.compile()


def run_pipeline(raw_text: str) -> dict:
    """Run the complete SkillBridge pipeline."""

    graph = build_graph()

    result = graph.invoke(
        {
            "raw_text": raw_text
        }
    )

    return result


if __name__ == "__main__":
    print("===== SkillBridge Career Analysis =====")

    user_input = input(
        "\nEnter your profile, skills, education and interests:\n"
    )

    try:
        result = run_pipeline(user_input)

        print("\n===== PARSED PROFILE =====")
        print(result.get("profile", {}))

        print("\n===== MATCHED JOBS =====")
        for item in result.get("matched_jobs", []):
            job = item.get("job", {})

            print(
                f"\nJob: {job.get('title', 'Unknown')}"
            )
            print(
                f"Match Score: {item.get('match_score', 0)}"
            )
            print(
                f"Missing Skills: {item.get('missing_skills', [])}"
            )

        print("\n===== IDENTIFIED SKILL GAPS =====")
        for gap in result.get("skill_gaps", []):
            print(gap)

        print("\n===== RECOMMENDED COURSES =====")
        recommendations = result.get("recommendations", [])

        if recommendations:
            for course in recommendations:
                print(course)
        else:
            print("No matching courses found.")

    except Exception as error:
        print(f"\nPipeline error: {error}")