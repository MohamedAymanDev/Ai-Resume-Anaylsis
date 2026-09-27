# ER Diagram

## Database Schema

```mermaid
erDiagram

    USERS ||--o{ RESUMES : owns
    RESUMES ||--|| RESUME_ANALYSES : has

    USERS {
        int id PK
        string email UK
        string hashed_password
        string full_name
    }

    RESUMES {
        int id PK
        int user_id FK
        string filename
        string file_path
        string file_type
        string extracted_text
        string status
        datetime uploaded_at
    }

    RESUME_ANALYSES {
        int id PK
        int resume_id FK UK
        string summary
        string technical_skills
        string soft_skills
        string education
        string experience
        datetime created_at
    }

    JOBS {
        int id PK
        string title
        string company
        string location
        string description
        string required_skills
        string preferred_skills
        string experience_level
        string education
        datetime created_at
    }