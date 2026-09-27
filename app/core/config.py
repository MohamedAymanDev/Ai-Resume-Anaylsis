import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "AI Resume Analyzer")
    APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./data/app.db",
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "development-secret-key",
    )

    JWT_ALGORITHM = os.getenv(
        "JWT_ALGORITHM",
        "HS256",
    )

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv(
            "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
            "60",
        )
    )
    LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "groq",
    )

    LLM_MODEL = os.getenv(
        "LLM_MODEL",
        "openai/gpt-oss-20b",
    )

    LLM_API_KEY = os.getenv(
        "LLM_API_KEY",
        "",
    )


settings = Settings()