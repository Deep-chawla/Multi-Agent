import os
from dotenv import load_dotenv
import logging
load_dotenv()


class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    DG_API_KEY = os.getenv("DG_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    # MODEL_NAME = "llama-3.3-70b-versatile"
    MODEL_NAME = "openai/gpt-oss-120b"
    SUPERVISOR_MODEL="openai/gpt-oss-120b"
    TEMPERATURE = 0.7
    # MAX_TOKENS = 5000  # from 1024 to 512 to reduce token
    # config/settings.py
    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
    DATABASE_URL = os.getenv("DB_URL")
    MAX_HISTORY = 10

    # Auth (must match the auth service's SECRET_KEY / ALGORITHM exactly,
    # so a token minted by signup-login-main can be verified here)
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")

settings = Settings()

logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
file = logging.FileHandler("my_log.log",mode='a',encoding='utf-8')
file.setFormatter(formatter)
logger.addHandler(file)