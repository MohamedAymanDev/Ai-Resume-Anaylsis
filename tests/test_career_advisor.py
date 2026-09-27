from app.ai.agents.career_advisor import CareerAdvisor


def test_career_advisor():
    advisor = CareerAdvisor()

    resume_analysis = """
    {
        "summary": "Artificial Intelligence student interested in Machine Learning.",
        "technical_skills": [
            "Python",
            "Machine Learning",
            "Scikit-learn",
            "TensorFlow",
            "FastAPI"
        ],
        "soft_skills": [
            "Problem Solving",
            "Teamwork"
        ],
        "education": [
            "Bachelor of Artificial Intelligence"
        ],
        "experience": [
            "Machine Learning Intern"
        ]
    }
    """

    job_information = """
    {
        "title": "Machine Learning Intern",
        "company": "AI Solutions",
        "location": "Cairo",
        "description": "Work on machine learning and artificial intelligence projects.",
        "required_skills": [
            "Python",
            "Machine Learning",
            "SQL",
            "Scikit-learn"
        ],
        "preferred_skills": [
            "TensorFlow",
            "FastAPI",
            "LangChain"
        ],
        "experience_level": "Internship",
        "education": "Computer Science or Artificial Intelligence"
    }
    """

    advice, sources = advisor.advise(
        resume_analysis=resume_analysis,
        job_information=job_information,
    )

    assert advice is not None

    assert isinstance(advice.strengths, list)
    assert isinstance(advice.weaknesses, list)
    assert isinstance(advice.missing_skills, list)
    assert isinstance(advice.improvement_suggestions, list)
    assert isinstance(advice.recommended_certifications, list)
    assert isinstance(advice.learning_resources, list)

    assert isinstance(sources, list)

    print("\n===== CAREER ADVISOR RESULT =====")
    print("Strengths:", advice.strengths)
    print("Weaknesses:", advice.weaknesses)
    print("Missing Skills:", advice.missing_skills)
    print("Suggestions:", advice.improvement_suggestions)
    print("Certifications:", advice.recommended_certifications)
    print("Learning Resources:", advice.learning_resources)
    print("Sources:", sources)