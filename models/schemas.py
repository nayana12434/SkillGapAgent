from typing import List, Optional

from pydantic import BaseModel, Field


class Profile(BaseModel):
    """
    Structured information extracted from a user's resume or profile.
    """

    name: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    education: Optional[str] = None
    location: Optional[str] = None
    interests: List[str] = Field(default_factory=list)
    experience: Optional[str] = None


class ProfileInput(BaseModel):
    """
    Input received from the frontend.
    """

    raw_text: str = Field(
        ...,
        min_length=1,
        description="Resume text or user profile description",
    )


class Job(BaseModel):
    """
    Represents a job posting from data/jobs.json.
    """

    id: str
    title: str
    company: Optional[str] = None
    description: Optional[str] = None
    required_skills: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    experience_required: Optional[str] = None
    application_url: Optional[str] = None


class JobMatch(BaseModel):
    """
    A job matched with the user's profile.
    """

    job: Job
    match_score: float = Field(ge=0.0, le=1.0)
    missing_skills: List[str] = Field(default_factory=list)


class SkillGap(BaseModel):
    """
    A skill the user should learn or improve.
    """

    skill: str
    importance: Optional[str] = "medium"
    related_jobs: List[str] = Field(default_factory=list)
    explanation: Optional[str] = None


class Course(BaseModel):
    """
    Represents a learning resource from data/courses.json.
    """

    id: str
    title: str
    platform: Optional[str] = None
    description: Optional[str] = None
    skills_taught: List[str] = Field(default_factory=list)
    level: Optional[str] = None
    url: Optional[str] = None


class CourseRecommendation(BaseModel):
    """
    A recommended course for improving a missing skill.
    """

    course: Course
    related_skills: List[str] = Field(default_factory=list)
    reason: Optional[str] = None


class AnalyzeResponse(BaseModel):
    """
    Final response returned by the SkillBridge API.
    """

    profile: Profile
    matched_jobs: List[JobMatch] = Field(default_factory=list)
    skill_gaps: List[SkillGap] = Field(default_factory=list)
    recommended_courses: List[CourseRecommendation] = Field(
        default_factory=list
    )