from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.parser import ResumeParser
from app.services.nlp import NLPExtractor
from app.services.scorer import ResumeScorer
from app.config import settings

router = APIRouter()
parser = ResumeParser()
nlp = NLPExtractor()
scorer = ResumeScorer(api_key=settings.OPENAI_API_KEY)

@router.post("/analyze", response_model=dict)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
):
    if resume.size > 5 * 1024 * 1024:
        raise HTTPException(413, "File too large (max 5MB)")
    content = await resume.read()
    try:
        text = parser.parse(content, resume.filename)
    except ValueError as e:
        raise HTTPException(400, str(e))

    entities = nlp.extract_entities(text)
    result = scorer.score(text, job_description, entities)
    return result.model_dump()
