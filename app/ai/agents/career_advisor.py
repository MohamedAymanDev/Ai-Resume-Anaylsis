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
- Return ALL six fields.
- If a field has no items, return an empty list.
- Keep recommendations practical and specific.

You MUST return:

1. strengths
2. weaknesses
3. missing_skills
4. improvement_suggestions
5. recommended_certifications
6. learning_resources

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
        )

        self.structured_model = self.model.with_structured_output(
            CareerAdvice
        )

    def advise(
        self,
        resume_analysis: str,
        job_information: str,
    ) -> tuple[CareerAdvice, list[str]]:

        query = f"""
        Career advice for this resume and target job.

        Resume:
        {resume_analysis}

        Target Job:
        {job_information}
        """

        retrieved_context, sources = get_relevant_context(
        query=query,
        top_k=5,
        )

        prompt = CAREER_ADVISOR_PROMPT.format(
            resume_analysis=resume_analysis,
            job_information=job_information,
            retrieved_context=retrieved_context,
        )

        advice = self.structured_model.invoke(prompt)

        return advice, sources