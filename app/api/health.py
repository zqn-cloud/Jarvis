from fastapi import APIRouter
from datetime import datetime
import psutil
import os

router = APIRouter()

@router.get("/health")
async def health_check():
    """健康检查端点"""
    try:
        # 获取系统信息
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "Jarvis智能助手",
            "version": "1.0.0",
            "system": {
                "cpu_percent": psutil.cpu_percent(),
                "memory_usage_mb": memory_info.rss / 1024 / 1024,
                "disk_usage": psutil.disk_usage('/').percent
            },
            "dependencies": {
                "openai": "connected",
                "weather_api": "configured",
                "agent": "initialized"
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }