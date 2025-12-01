import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # # OpenAI 配置
    # OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-ZPLgXrScHigy0qaE022467729dAd4325B223A487DaA7E189")
    MODEL = os.getenv("MODEL", "gpt-3.5-turbo")
    
    os.environ["OPENAI_API_BASE"] = 'https://xiaoai.plus/v1'
    os.environ["OPENAI_API_KEY"] = 'sk-ZPLgXrScHigy0qaE022467729dAd4325B223A487DaA7E189'
    os.environ["OPENWEATHER_API_KEY"] = '949fb231b7b49c897cc05d449193fcc7'

    # 天气 API
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "949fb231b7b49c897cc05d449193fcc7")
    
    # 服务器配置
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

config = Config()