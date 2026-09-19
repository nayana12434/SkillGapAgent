"""
FastAPI entry point for the SkillBridge application.
"""

from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agents.graph import run_pipeline


app = FastAPI(
    title="SkillBridge API",
    description="AI-powered career guidance and skill-gap analysis system",
    version="1.0.0",
)

# Allow the frontend to communicate with the backend
# Suitable for a hackathon demonstration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    """
    Request model for career analysis.
    """

    raw_text: str = Field(
        ...,
        min_length=10,
        description="User's profile, skills, education, and interests",
    )


@app.get("/")
def home() -> dict[str, str]:
    """
    Health-check endpoint.
    """

    return {
        "message": "SkillBridge API is running successfully!"
    }


@app.post("/analyze")
def analyze_profile(request: AnalyzeRequest) -> dict[str, Any]:
    """
    Runs the complete SkillBridge pipeline.
    """

    try:
        result = run_pipeline(request.raw_text)

        return {
            "success": True,
            "data": result,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline error: {str(error)}",
        )