import json

from langchain_groq import ChatGroq

from app.core.config import settings
from app.schemas.career import CareerAdvice
from app.rag.service import get_relevant_context


CAREER_ADVISOR_PROMPT = """
You are an expert career advisor and resume improvement assistant.

Analyze the provided resume and target job.

Use the retrieved knowledge context to provide practical,
evidence-grounded career recommendations.

Important rules:

- Use only information supported by the resume, target job,
  and retrieved knowledge.
- Do not invent experience, skills, education, or achievements.
- Do not claim that the candidate has a skill unless it appears
  in the resume.
- Recommendations should be relevant to the target job.
- Return valid JSON only.
- Do not use Markdown.
- Do not wrap the JSON in ```json or ```.

The JSON MUST contain exactly these six fields:

{{
    "strengths": [],
    "weaknesses": [],
    "missing_skills": [],
    "improvement_suggestions": [],
    "recommended_certifications": [],
    "learning_resources": []
}}

If a field has no items, return an empty list.

Resume Analysis:
{resume_analysis}

Target Job:
{job_information}

Retrieved Knowledge:
{retrieved_context}
"""


class CareerAdvisor:

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

    def advise(
        self,
        resume_analysis: str,
        job_information: str,
    ) -> tuple[CareerAdvice, list[str]]:

        # =========================
        # 1. Build RAG Query
        # =========================

        query = f"""
        Career advice for this resume and target job.

        Resume:
        {resume_analysis}

        Target Job:
        {job_information}
        """

        # =========================
        # 2. Retrieve Knowledge
        # =========================

        retrieved_context, sources = get_relevant_context(
            query=query,
            top_k=5,
        )

        # =========================
        # 3. Build Prompt
        # =========================

        prompt = CAREER_ADVISOR_PROMPT.format(
            resume_analysis=resume_analysis,
            job_information=job_information,
            retrieved_context=retrieved_context,
        )

        # =========================
        # 4. Ask LLM
        # =========================

        response = self.model.invoke(prompt)

        # =========================
        # 5. Get Response Text
        # =========================

        response_text = response.content

        # =========================
        # 6. Remove Markdown Fences
        # =========================

        response_text = response_text.strip()

        if response_text.startswith("```"):
            response_text = response_text.replace(
                "```json",
                "",
            )

            response_text = response_text.replace(
                "```",
                "",
            )

            response_text = response_text.strip()

        # =========================
        # 7. Parse JSON
        # =========================

        try:
            advice_data = json.loads(response_text)

        except json.JSONDecodeError as exc:
            raise ValueError(
                "Career Advisor returned invalid JSON"
            ) from exc

        # =========================
        # 8. Validate with Pydantic
        # =========================

        advice = CareerAdvice.model_validate(
            advice_data
        )

        # =========================
        # 9. Return Advice + Sources
        # =========================

        return advice, sources