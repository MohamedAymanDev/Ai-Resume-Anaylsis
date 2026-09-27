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


def test_upload_pdf_resume():
    headers = get_auth_headers()

    pdf_path = Path("tests/test_resume.pdf")

    assert pdf_path.exists(), "Test PDF file does not exist."

    with open(pdf_path, "rb") as file:
        response = client.post(
            "/resumes/upload",
            headers=headers,
            files={
                "file": (
                    "test_resume.pdf",
                    file,
                    "application/pdf",
                )
            },
        )

    assert response.status_code in [200, 201]

    data = response.json()

    assert "id" in data
    assert data["filename"] == "test_resume.pdf"
    assert data["file_type"] == "pdf"
    assert data["status"] == "parsed"
    

def test_analyze_resume():
    headers = get_auth_headers()

    pdf_path = Path("tests/test_resume.pdf")

    with open(pdf_path, "rb") as file:
        upload_response = client.post(
            "/resumes/upload",
            headers=headers,
            files={
                "file": (
                    "test_resume_analysis.pdf",
                    file,
                    "application/pdf",
                )
            },
        )

    assert upload_response.status_code in [200, 201]

    resume_id = upload_response.json()["id"]

    response = client.post(
        f"/resumes/{resume_id}/analyze",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "summary" in data
    assert "technical_skills" in data
    assert "soft_skills" in data
    assert "education" in data
    assert "experience" in data

    assert isinstance(data["technical_skills"], list)
    assert isinstance(data["soft_skills"], list)
    assert isinstance(data["education"], list)
    assert isinstance(data["experience"], list)    