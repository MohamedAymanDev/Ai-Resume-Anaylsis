from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_auth_headers():
    response = client.post(
        "/auth/login",
        data={
            "username": "test@gmail.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def create_test_resume(headers):
    pdf_path = Path("tests/test_resume.pdf")

    with open(pdf_path, "rb") as file:
        upload_response = client.post(
            "/resumes/upload",
            headers=headers,
            files={
                "file": (
                    "matching_test_resume.pdf",
                    file,
                    "application/pdf",
                )
            },
        )

    assert upload_response.status_code in [200, 201]

    resume_id = upload_response.json()["id"]

    analyze_response = client.post(
        f"/resumes/{resume_id}/analyze",
        headers=headers,
    )

    assert analyze_response.status_code == 200

    return resume_id


def create_test_job(headers):
    response = client.post(
        "/jobs/",
        headers=headers,
        json={
            "title": "Machine Learning Intern",
            "company": "Matching Test Company",
            "location": "Cairo",
            "description": (
                "Machine learning internship for students "
                "with Python, Machine Learning, SQL and FastAPI skills."
            ),
            "required_skills": [
                "Python",
                "Machine Learning",
                "SQL",
            ],
            "preferred_skills": [
                "FastAPI",
            ],
            "experience_level": "Internship",
            "education": "Computer Science",
        },
    )

    assert response.status_code in [200, 201]

    return response.json()["id"]


def test_job_matching():
    headers = get_auth_headers()

    resume_id = create_test_resume(headers)
    job_id = create_test_job(headers)

    response = client.post(
        f"/matching/resume/{resume_id}/job/{job_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["resume_id"] == resume_id
    assert data["job_id"] == job_id

    assert "match_score" in data
    assert "skill_match_score" in data
    assert "semantic_similarity_score" in data
    assert "experience_match_score" in data
    assert "education_match_score" in data

    assert "matched_skills" in data
    assert "missing_skills" in data

    assert 0 <= data["match_score"] <= 100
    assert 0 <= data["skill_match_score"] <= 100
    assert 0 <= data["semantic_similarity_score"] <= 100
    assert 0 <= data["experience_match_score"] <= 100
    assert 0 <= data["education_match_score"] <= 100

    assert isinstance(data["matched_skills"], list)
    assert isinstance(data["missing_skills"], list)