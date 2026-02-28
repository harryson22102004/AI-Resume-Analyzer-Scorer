import io
from pathlib import Path
from pypdf import PdfReader
from docx import Document

class ResumeParser:
    """Extract text from PDF and DOCX files."""

    @staticmethod
    def parse(content: bytes, filename: str) -> str:
        ext = Path(filename).suffix.lower()
        if ext == ".pdf":
            return ResumeParser._parse_pdf(content)
        elif ext == ".docx":
            return ResumeParser._parse_docx(content)
        elif ext == ".txt":
            return content.decode("utf-8")
        raise ValueError(f"Unsupported format: {ext}")

    @staticmethod
    def _parse_pdf(content: bytes) -> str:
        reader = PdfReader(io.BytesIO(content))
        text = []
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text.append(extracted)
        return "\n".join(text)

    @staticmethod
    def _parse_docx(content: bytes) -> str:
        doc = Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
