import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME",'AI Resume Analyaer')
    APP_VERSION = os.getenv('APP_VERSION','0.1.0')
    DEBUG = os.getenv('DEBUG','flase').lower()=='true'
    
    DATABASE_URL = os.getenv('DATABASE_URL','sqlite:///./data/app.db')
    

setting = Settings()    