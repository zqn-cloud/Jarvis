from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn
from datetime import datetime

from app.agents.jarvis_agent import jarvis_agent
from app.config import config

app = FastAPI(
    title="Jarvis 智能助手 API",
    description="基于 LLM 的智能日程管理助手",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    success: bool
    response: str
    timestamp: str
    error: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    print("🚀 Jarvis 智能助手正在启动...")
    print(f"📡 模型: {config.MODEL}")
    print(f"🔧 已加载工具: {len(jarvis_agent.get_tools_info())}个")
    print("✅ Jarvis 启动完成！")

@app.get("/")
async def root():
    return {
        "message": "欢迎使用 Jarvis 智能助手 API",
        "version": "1.0.0",
        "endpoints": {
            "文档": "/docs",
            "健康检查": "/health",
            "聊天": "/chat (POST)",
            "工具列表": "/tools"
        }
    }

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Jarvis 智能助手",
        "version": "1.0.0"
    }

@app.get("/tools")
async def list_tools():
    """列出所有可用工具"""
    return {
        "success": True,
        "tools": jarvis_agent.get_tools_info(),
        "count": len(jarvis_agent.get_tools_info())
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """处理用户聊天请求"""
    try:
        if not request.message or request.message.strip() == "":
            raise HTTPException(status_code=400, detail="消息不能为空")
        
        print(f"📨 收到用户消息: {request.message}")
        
        result = await jarvis_agent.process_query(request.message)
        
        return ChatResponse(
            success=result["success"],
            response=result["response"],
            timestamp=datetime.now().isoformat(),
            error=result.get("error")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/direct")
async def direct_chat_endpoint(request: ChatRequest):
    """直接调用 Agent（不通过 FastAPI 包装）"""
    try:
        # 直接使用 create_agent（适用于测试）
        from langchain.agents import create_agent
        from langchain_openai import ChatOpenAI
        from app.tools.weather_tool import get_weather
        from app.tools.time_tool import get_current_time
        
        llm = ChatOpenAI(
            model=config.MODEL,
            openai_api_base=config.OPENAI_API_BASE,
            openai_api_key=config.OPENAI_API_KEY,
            temperature=0.7
        )
        
        agent = create_agent(
            model=llm,
            tools=[get_weather, get_current_time],
            system_prompt="You are a helpful assistant.",
        )
        
        result = agent.invoke(
            {"messages": [{"role": "user", "content": request.message}]}
        )
        
        return {
            "success": True,
            "response": result['messages'][-1].content,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level="info"
    )