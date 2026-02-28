import spacy
from typing import Dict, List

class NLPExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        # Custom skill patterns
        self.skill_patterns = self._load_skill_patterns()

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        doc = self.nlp(text)
        entities = {
            "PERSON": [], "ORG": [], "DATE": [],
            "GPE": [], "SKILLS": [], "EDUCATION": [],
        }
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)

        # Custom skill extraction using pattern matching
        skills = self._extract_skills(doc)
        entities["SKILLS"] = list(set(skills))
        return entities

    def _extract_skills(self, doc) -> List[str]:
        found = []
        text_lower = doc.text.lower()
        for skill in self.skill_patterns:
            if skill.lower() in text_lower:
                found.append(skill)
        return found

    def _load_skill_patterns(self) -> List[str]:
        return [
            "Python", "JavaScript", "TypeScript", "React", "Angular", "Vue",
            "Node.js", "FastAPI", "Django", "Flask", "TensorFlow", "PyTorch",
            "AWS", "Azure", "GCP", "Docker", "Kubernetes", "PostgreSQL",
            "MongoDB", "Redis", "Git", "CI/CD", "Machine Learning",
            "Deep Learning", "NLP", "Computer Vision", "SQL", "GraphQL",
        ]
