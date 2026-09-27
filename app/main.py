from fastapi import FastAPI
from app.core.config import Settings
app = FastAPI(title=Settings.APP_NAME,
               description="AI-powered Resume Analysis and Career Intelligence Platform",
               version=Settings.APP_VERSION)

@app.get('/')

def root():
    return{
        "message": "AI Resume Analyzer API is running",
        "version": Settings.APP_VERSION
        
    }

@app.get('/health')

def health_check():
    return{
        "status": "healthy"
    }
