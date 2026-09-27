from app.services.scoring import calculate_final_match_score


def test_calculate_final_match_score():
    score = calculate_final_match_score(
        skill_match_score=80,
        semantic_similarity_score=70,
        experience_match_score=100,
        education_match_score=100,
    )

    assert score == 82.0