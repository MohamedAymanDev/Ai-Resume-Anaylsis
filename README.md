# 🤖 AI Resume Analyzer & Career Intelligence Platform

An AI-powered web application that analyzes resumes, matches candidates with job opportunities, and provides personalized career recommendations using **LLMs, RAG, semantic similarity, and AI agents**.

---

## 📌 Overview

The **AI Resume Analyzer & Career Intelligence Platform** helps users understand their resumes and discover suitable career opportunities.

The system can:

* 📄 Upload and analyze PDF/DOCX resumes
* 🤖 Extract technical and soft skills using AI
* 🎯 Match resumes with job opportunities
* 📊 Calculate job matching scores
* 🔎 Search available jobs
* 🚀 Generate personalized career advice
* 📚 Retrieve grounded recommendations from a RAG knowledge base
* 🗂️ Manage job opportunities through CRUD operations
* 🔐 Authenticate users using JWT

---

## 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │      Frontend       │
                         │ HTML / CSS / JS     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │       Backend       │
                         └──────────┬──────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
      ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
      │ Resume AI   │       │ Job Matching │       │ Career AI   │
      │   Agent     │       │   Service    │       │   Advisor   │
      └──────┬──────┘       └──────┬──────┘       └──────┬──────┘
             │                     │                      │
             │                     │                      ▼
             │                     │               ┌─────────────┐
             │                     │               │ RAG System  │
             │                     │               └──────┬──────┘
             │                     │                      │
             ▼                     ▼                      ▼
      ┌────────────────────────────────────────────────────────┐
      │                    SQLite Database                      │
      └────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### 🔐 Authentication

* User registration
* User login
* JWT authentication
* Protected API endpoints
* Password hashing with bcrypt

### 📄 Resume Analysis

Supported formats:

* PDF
* DOCX

The AI extracts:

* Professional summary
* Technical skills
* Soft skills
* Education
* Experience

### 🎯 Job Matching

The matching system combines multiple signals:

```text
Skill Match              → 45%
Semantic Similarity      → 30%
Experience Match         → 15%
Education Match          → 10%
```

Final score:

```text
Final Score =
0.45 × Skill Match
+ 0.30 × Semantic Similarity
+ 0.15 × Experience
+ 0.10 × Education
```

### 🔎 Job Search

Users can search jobs using:

* Job title
* Company
* Description
* Location

The system can then calculate resume-to-job matching scores.

### 🚀 AI Career Advisor

The Career Advisor generates:

* Strengths
* Weaknesses
* Missing skills
* Improvement suggestions
* Recommended certifications
* Learning resources

### 📚 RAG Knowledge Base

The RAG system uses a knowledge base containing:

```text
knowledge_base/
├── job_descriptions/
├── skills/
├── career_roadmaps/
├── learning_resources/
└── resume_guidelines/
```

The pipeline:

```text
Documents
    ↓
Load
    ↓
Chunk
    ↓
Embeddings
    ↓
ChromaDB
    ↓
Retriever
    ↓
Relevant Context
    ↓
LLM
    ↓
Grounded Career Advice
```

---

## 🧠 AI Components

### Resume Analyzer Agent

Responsible for extracting structured information from resumes.

### Job Matching Service

Combines:

* Exact skill matching
* Semantic similarity
* Experience matching
* Education matching

### Career Advisor Agent

Combines resume analysis, job information, and retrieved knowledge-base context to generate career recommendations.

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT
* bcrypt

### AI / ML

* LangChain
* Groq
* LLMs
* Sentence Transformers
* Scikit-learn
* Semantic Similarity
* ChromaDB
* RAG

### Resume Processing

* PyMuPDF
* python-docx

### Frontend

* HTML
* CSS
* Vanilla JavaScript

### Testing

* Pytest
* FastAPI TestClient

---

## 📂 Project Structure

```text
Ai-Resume-Anaylsis/
│
├── app/
│   ├── api/
│   ├── ai/
│   │   ├── agents/
│   │   └── prompts/
│   ├── core/
│   ├── db/
│   ├── rag/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── frontend/
│   ├── css/
│   ├── js/
│   ├── index.html
│   ├── login.html
│   └── register.html
│
├── knowledge_base/
│
├── tests/
│
├── docs/
│   ├── API.md
│   └── ER_DIAGRAM.md
│
├── migrations/
│
├── uploads/
├── data/
│
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── run.py
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Ai-Resume-Anaylsis
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file:

```env
APP_NAME=AI Resume Analyzer
APP_VERSION=0.1.0
DEBUG=true

DATABASE_URL=sqlite:///./data/app.db

JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

LLM_PROVIDER=groq
LLM_MODEL=openai/gpt-oss-20b
LLM_API_KEY=your-groq-api-key
```

---

## ▶️ Running the Backend

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## 🌐 Running the Frontend

Open another terminal:

```powershell
.\.venv\Scripts\python.exe -m http.server 5500 --directory frontend
```

Then open:

```text
http://127.0.0.1:5500
```

---

## 🧪 Running Tests

Run the complete test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -v
```

Current test suite:

```text
17 passed
```

The tests cover:

* Authentication
* Resume upload
* Resume analysis
* Job CRUD
* Job search
* Job matching
* Scoring
* RAG loading
* RAG chunking
* RAG retrieval
* Career Advisor

---

## 🔄 RAG Knowledge Base

Build the knowledge base with:

```powershell
.\.venv\Scripts\python.exe -c "from app.rag.pipeline import build_knowledge_base; build_knowledge_base()"
```

Check the number of stored documents:

```powershell
.\.venv\Scripts\python.exe -c "from app.rag.vector_store import collection; print('Documents:', collection.count())"
```

---

## 📖 API Documentation

Detailed API documentation is available in:

```text
docs/API.md
```

Interactive Swagger documentation:

```text
/docs
```

---

## 🗄️ Database

The project uses **SQLite** with **SQLAlchemy**.

Main entities:

```text
Users
  │
  └── Resumes
        │
        └── Resume Analyses

Jobs
```

The database schema is documented in:

```text
docs/ER_DIAGRAM.md
```

---

## 🔒 Security

The project uses:

* JWT access tokens
* bcrypt password hashing
* Protected API endpoints
* Environment variables for secrets
* `.env` excluded from Git

Never commit your real API keys or secrets.

---

## 🚧 Future Improvements

Possible future extensions include:

* 🌐 Production deployment
* ☁️ Cloud database
* 👤 Role-based access control
* 📈 Resume analytics dashboard
* 📄 Resume improvement generator
* 🔗 LinkedIn profile integration
* 🎯 Advanced job recommendation algorithms
* 🤖 More specialized AI agents
* 📊 Evaluation dashboard for AI/RAG quality
* 🔍 Improved semantic job retrieval
* 🧪 Expanded automated test coverage

---

## 👨‍💻 Author

**Mohamed Ayman**

Artificial Intelligence Student
Aspiring Machine Learning Engineer

Focused on:

* Machine Learning
* Deep Learning
* NLP
* Generative AI
* RAG
* AI Agents

---

## 📜 License

This project is developed for educational and portfolio purposes.
