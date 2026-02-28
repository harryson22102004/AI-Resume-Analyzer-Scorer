from pydantic import BaseModel, Field
from typing import Optional

class AnalysisRequest(BaseModel):
    job_description: str = Field(..., min_length=50)

class SkillMatch(BaseModel):
    skill: str
    found: bool
    context: Optional[str] = None

class AnalysisResponse(BaseModel):
    overall_score: int = Field(..., ge=0, le=100)
    ats_score: int = Field(..., ge=0, le=100)
    skills_found: list[str]
    skills_missing: list[str]
    skill_matches: list[SkillMatch]
    experience_years: Optional[float]
    education: list[str]
    suggestions: list[str]
    summary: str
