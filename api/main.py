"""
FastAPI entry point for the SkillBridge application.
"""

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from agents.graph import run_pipeline


# --------------------------------------------------
# Paths
# --------------------------------------------------

# Project root:
# SkillGapAgent/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

FRONTEND_DIR = PROJECT_ROOT / "public"
FRONTEND_FILE = FRONTEND_DIR / "index.html"


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="SkillBridge API",
    description="AI-powered career guidance and skill-gap analysis system",
    version="1.0.0",
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Request model
# --------------------------------------------------

class AnalyzeRequest(BaseModel):
    """
    Request model for career analysis.
    """

    raw_text: str = Field(
        ...,
        min_length=10,
        description="User's profile, skills, education, and interests",
    )


# --------------------------------------------------
# Frontend
# --------------------------------------------------

@app.get("/")
def home():
    """
    Serve the SkillBridge frontend.
    """

    if not FRONTEND_FILE.exists():
        raise HTTPException(
            status_code=404,
            detail="Frontend index.html not found.",
        )

    return FileResponse(FRONTEND_FILE)


# Serve CSS, JavaScript and other frontend files
if FRONTEND_DIR.exists():
    app.mount(
        "/static",
        StaticFiles(directory=FRONTEND_DIR),
        name="static",
    )


# --------------------------------------------------
# API
# --------------------------------------------------

@app.post("/analyze")
def analyze_profile(
    request: AnalyzeRequest,
) -> dict[str, Any]:
    """
    Run the complete SkillBridge AI pipeline.
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


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/health")
def health_check():
    """
    Health-check endpoint.
    """

    return {
        "status": "healthy",
        "message": "SkillBridge API is running successfully!",
    }