"""
Extracts structured profile information from free-text input using Groq.
"""

import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from models.schemas import Profile

load_dotenv()


def parse_profile(raw_text: str) -> dict:
    """
    Convert resume text or a user description into a structured profile.

    Args:
        raw_text: Resume text or free-form user profile information.

    Returns:
        A dictionary matching the Profile schema.
    """

    if not raw_text or not raw_text.strip():
        raise ValueError("Profile text cannot be empty.")

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from the .env file.")

    llm = ChatGroq(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        temperature=0,
        api_key=api_key,
    )

    structured_llm = llm.with_structured_output(Profile)

    prompt = f"""
You are a professional resume information extraction assistant.

Extract information from the following profile text.

Rules:
- Extract only information supported by the provided text.
- Do not invent skills, education, experience, interests, or location.
- Return an empty list when information is unavailable.
- Keep skills and interests as simple, clear strings.
- Follow the Profile schema exactly.

Profile text:
{raw_text}
"""

    result = structured_llm.invoke(prompt)

    if isinstance(result, Profile):
        profile = result
    else:
        profile = Profile.model_validate(result)

    return profile.model_dump()