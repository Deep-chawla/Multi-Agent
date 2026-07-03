import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    DG_API_KEY = os.getenv("DG_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    # MODEL_NAME = "llama-3.3-70b-versatile"
    MODEL_NAME = "openai/gpt-oss-120b"
    TEMPERATURE = 0.7
    MAX_TOKENS = 2048  # from 1024 to 512 to reduce token
    # config/settings.py
    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))


settings = Settings()