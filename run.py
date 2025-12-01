#!/usr/bin/env python3
import uvicorn
from app.config import config

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 启动 Jarvis 智能助手")
    print("=" * 50)
    print(f"🌐 地址: http://{config.HOST}:{config.PORT}")
    print(f"📚 文档: http://{config.HOST}:{config.PORT}/docs")
    print("=" * 50)
    
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level="info"
    )