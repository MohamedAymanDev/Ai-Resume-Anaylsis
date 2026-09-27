def calculate_skill_match(
    resume_skills: list[str],
    job_required_skills: list[str],
) -> float:

    if not job_required_skills:
        return 0.0

    resume_skills_set = {
        skill.strip().lower()
        for skill in resume_skills
    }

    job_skills_set = {
        skill.strip().lower()
        for skill in job_required_skills
    }

    matched_skills = (
        resume_skills_set & job_skills_set
    )

    score = (
        len(matched_skills)
        / len(job_skills_set)
    )

    return round(score * 100, 2)


def get_skill_match_details(
    resume_skills: list[str],
    job_required_skills: list[str],
) -> dict:

    resume_skills_map = {
        skill.strip().lower(): skill
        for skill in resume_skills
    }

    job_skills_map = {
        skill.strip().lower(): skill
        for skill in job_required_skills
    }

    resume_skills_set = set(
        resume_skills_map.keys()
    )

    job_skills_set = set(
        job_skills_map.keys()
    )

    matched = resume_skills_set & job_skills_set
    missing = job_skills_set - resume_skills_set

    score = calculate_skill_match(
        resume_skills,
        job_required_skills,
    )

    return {
        "score": score,
        "matched_skills": [
            resume_skills_map[skill]
            for skill in matched
        ],
        "missing_skills": [
            job_skills_map[skill]
            for skill in missing
        ],
    }
    
def calculate_experience_match(
    resume_experience: list[str],
    job_experience_level: str | None,
) -> float:
    if not job_experience_level:
        return 100.0

    if not resume_experience:
        return 0.0

    job_level = job_experience_level.lower()

    resume_text = " ".join(resume_experience).lower()

    if "intern" in job_level or "entry" in job_level:
        return 100.0

    if "junior" in job_level:
        if "intern" in resume_text or "junior" in resume_text:
            return 100.0
        return 50.0

    return 50.0   
def calculate_education_match(
    resume_education: list[str],
    job_education: str | None,
) -> float:
    if not job_education:
        return 100.0

    if not resume_education:
        return 0.0

    job_education_text = job_education.lower()
    resume_education_text = " ".join(resume_education).lower()

    education_keywords = [
        "computer science",
        "artificial intelligence",
        "information technology",
        "software engineering",
        "data science",
        "computer engineering",
    ]

    for keyword in education_keywords:
        if keyword in job_education_text and keyword in resume_education_text:
            return 100.0

    return 50.0 
