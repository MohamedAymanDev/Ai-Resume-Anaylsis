def calculate_final_match_score(
    skill_match_score: float,
    semantic_similarity_score: float,
    experience_match_score: float,
    education_match_score: float,
) -> float:
    final_score = (
        (skill_match_score * 0.45)
        + (semantic_similarity_score * 0.30)
        + (experience_match_score * 0.15)
        + (education_match_score * 0.10)
    )

    return round(final_score, 2)