from openai import OpenAI
from app.models.schemas import AnalysisResponse
import json

class ResumeScorer:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def score(self, resume_text: str, job_description: str,
              entities: dict) -> AnalysisResponse:
        prompt = f"""Analyze this resume against the job description.
Return a JSON object with these exact fields:
- overall_score (0-100)
- ats_score (0-100)
- skills_missing (list of strings)
- experience_years (float or null)
- education (list of degree strings)
- suggestions (list of 5-8 actionable improvements)
- summary (2-3 sentence assessment)

Resume:
{resume_text[:4000]}

Job Description:
{job_description[:2000]}

Skills already found: {', '.join(entities.get('SKILLS', []))}"""

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert HR analyst and ATS specialist. Respond only with valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )
        data = json.loads(response.choices[0].message.content)
        return AnalysisResponse(
            skills_found=entities.get("SKILLS", []),
            skill_matches=[],
            **data,
        )
