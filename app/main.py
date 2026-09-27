from fastapi import FastAPI

app = FastAPI(title="AI Resume Analyzer",
               description="AI-powered Resume Analysis and Career Intelligence Platform",
               version="0.1.0")

@app.get('/')

def root():
    return{
        "message": "AI Resume Analyzer API is running",
        "version": "0.1.0"
        
    }

@app.get('/health')

def health_check():
    return{
        "status": "healthy"
    }
