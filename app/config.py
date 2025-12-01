import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # # OpenAI 配置
    # OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "")
    # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("MODEL", "gpt-3.5-turbo")
    
    os.environ["OPENAI_API_BASE"] = ''
    os.environ["OPENAI_API_KEY"] = ''
    os.environ["OPENWEATHER_API_KEY"] = ''

    # 天气 API
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    
    # 服务器配置
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

config = Config()
