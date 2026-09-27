from langchain_groq import ChatGroq

from app.core.config import settings
from app.schemas.resume import ResumeAnalysis
from app.ai.prompts.resume_analyzer import RESUME_ANALYZER_PROMPT


class ResumeAnalyzer:
    def __init__(self):
        self.model = ChatGroq(
            model=settings.LLM_MODEL,
            api_key=settings.LLM_API_KEY,
        )

        self.structured_model = self.model.with_structured_output(
            ResumeAnalysis
        )

    def analyze(self, resume_text: str) -> ResumeAnalysis:
        prompt = RESUME_ANALYZER_PROMPT.format(
            resume_text=resume_text
        )

        result = self.structured_model.invoke(prompt)

        return result