import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

from models.schemas import SkillGap


class SkillGapList(BaseModel):
    """
    Structured output containing identified skill gaps.
    """

    skill_gaps: List[SkillGap] = Field(default_factory=list)


def analyze_skill_gaps(
    profile: dict,
    matched_jobs: list[dict],
) -> list[dict]:
    """
    Identifies missing or weak skills based on the user's profile
    and the matched job requirements.
    """

    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from the .env file.")

    llm = ChatGroq(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        temperature=0,
        api_key=api_key,
    )

    structured_llm = llm.with_structured_output(SkillGapList)

    prompt = f"""
You are a professional career skill-gap analysis assistant.

Your task is to identify the skills that the user should learn or improve
to become more suitable for the matched job opportunities.

USER PROFILE:
{profile}

MATCHED JOBS:
{matched_jobs}

Rules:
1. Identify only relevant technical or professional skills.
2. Do not invent skills that are unrelated to the jobs.
3. Compare the user's existing skills with the required skills of the jobs.
4. Do not list a skill as missing if the user already has that skill.
5. Assign importance as "high", "medium", or "low".
6. Include the IDs or titles of relevant jobs in related_jobs.
7. Explain briefly why each skill is useful.
8. Return an empty list if no skill gaps are found.
"""

    result = structured_llm.invoke(prompt)

    return [
        skill_gap.model_dump()
        for skill_gap in result.skill_gaps
    ]


# Alias for easy use in the project pipeline
def analyze_gaps(
    profile: dict,
    matched_jobs: list[dict],
) -> list[dict]:
    """
    Alternative function name for the pipeline.
    """

    return analyze_skill_gaps(profile, matched_jobs)


if __name__ == "__main__":
    sample_profile = {
        "name": "Test User",
        "skills": ["Python", "Java"],
        "education": "Computer Science",
        "location": None,
        "interests": ["Data Analytics"],
        "experience": None,
    }

    sample_jobs = [
        {
            "job": {
                "id": "1",
                "title": "Data Analyst",
                "required_skills": [
                    "Python",
                    "SQL",
                    "Excel",
                    "Power BI",
                ],
            },
            "match_score": 0.6,
            "missing_skills": ["SQL", "Excel", "Power BI"],
        }
    ]

    gaps = analyze_skill_gaps(sample_profile, sample_jobs)

    print("Identified Skill Gaps:")
    for gap in gaps:
        print(gap)