import json

from langchain_groq import ChatGroq

from app.core.config import settings
from app.schemas.resume import ResumeAnalysis
from app.ai.prompts.resume_analyzer import RESUME_ANALYZER_PROMPT


class ResumeAnalyzer:

    def __init__(self):

        self.model = ChatGroq(
            model=settings.LLM_MODEL,
            api_key=settings.LLM_API_KEY,
            temperature=0,
            model_kwargs={
                "response_format": {
                    "type": "json_object"
                }
            },
        )

    def analyze(self, resume_text: str) -> ResumeAnalysis:

        prompt = RESUME_ANALYZER_PROMPT.format(
            resume_text=resume_text
        )

        response = self.model.invoke(prompt)

        response_text = response.content.strip()

        # Remove markdown code fences if the model returns them
        if response_text.startswith("```"):
            response_text = response_text.replace("```json", "")
            response_text = response_text.replace("```", "")
            response_text = response_text.strip()

        try:

            result = json.loads(response_text)

        except json.JSONDecodeError as exc:

            raise ValueError(
                "Resume Analyzer returned invalid JSON"
            ) from exc

        return ResumeAnalysis.model_validate(result)