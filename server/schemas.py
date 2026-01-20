from pydantic import BaseModel, Field
from typing import List, Optional

class ResumeContent(BaseModel):
    text: str = Field(..., description="The full text content of the resume")

class JobDescription(BaseModel):
    text: str = Field(..., description="The full text content of the job description or URL text")

class SkillGap(BaseModel):
    missing_skill: str = Field(..., description="A skill found in JD but missing in Resume")
    importance: str = Field(..., description="High, Medium, or Low")

class TailoredPoint(BaseModel):
    original: str = Field(..., description="Original bullet point from resume")
    improved: str = Field(..., description="Rewritten bullet point including keywords")
    reason: str = Field(..., description="Why this change increases the match score")

class AnalysisResult(BaseModel):
    match_score: int = Field(..., description="0-100 match score")
    summary: str = Field(..., description="Brief summary of the fit")
    missing_keywords: List[str] = Field(..., description="List of critical missing keywords")
    # skill_gaps removed as it is not used in frontend
    tailored_suggestions: List[TailoredPoint] = Field(..., description="Suggested rewrites for experience")
    interview_questions: List[str] = Field(..., description="8-10 generated high-end interview questions specific to this candidate/role")

class AnalysisRequest(BaseModel):
    resume: str
    job_description: str
