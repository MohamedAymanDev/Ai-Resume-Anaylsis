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
    
   
 
