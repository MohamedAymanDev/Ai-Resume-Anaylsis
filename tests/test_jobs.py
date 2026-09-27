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


def test_create_job():
    headers = get_auth_headers()

    response = client.post(
        "/jobs/",
        headers=headers,
        json={
            "title": "Test Machine Learning Intern",
            "company": "Test AI Company",
            "location": "Cairo",
            "description": "Machine learning internship for testing.",
            "required_skills": [
                "Python",
                "Machine Learning",
                "SQL",
            ],
            "preferred_skills": [
                "FastAPI",
                "LangChain",
            ],
            "experience_level": "Internship",
            "education": "Computer Science",
        },
    )

    assert response.status_code in [200, 201]

    data = response.json()

    assert data["title"] == "Test Machine Learning Intern"
    assert data["company"] == "Test AI Company"

    


def test_get_jobs():
    headers = get_auth_headers()

    response = client.get(
        "/jobs/",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_search_jobs():
    headers = get_auth_headers()

    response = client.get(
        "/jobs/search?q=Machine%20Learning",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_update_job():
    headers = get_auth_headers()

    create_response = client.post(
        "/jobs/",
        headers=headers,
        json={
            "title": "Original Job",
            "company": "Original Company",
            "location": "Cairo",
            "description": "Original description.",
            "required_skills": ["Python"],
            "preferred_skills": [],
            "experience_level": "Internship",
            "education": "Computer Science",
        },
    )

    assert create_response.status_code in [200, 201]

    job_id = create_response.json()["id"]

    response = client.put(
        f"/jobs/{job_id}",
        headers=headers,
        json={
            "title": "Updated Job",
            "company": "Updated Company",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated Job"
    assert data["company"] == "Updated Company"


def test_delete_job():
    headers = get_auth_headers()

    create_response = client.post(
        "/jobs/",
        headers=headers,
        json={
            "title": "Job To Delete",
            "company": "Delete Company",
            "description": "This job will be deleted.",
            "required_skills": ["Python"],
            "preferred_skills": [],
            "experience_level": "Internship",
            "education": "Computer Science",
        },
    )

    assert create_response.status_code in [200, 201]

    job_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/jobs/{job_id}",
        headers=headers,
    )

    assert delete_response.status_code in [200, 204]

    get_response = client.get(
        f"/jobs/{job_id}",
        headers=headers,
    )

    assert get_response.status_code == 404