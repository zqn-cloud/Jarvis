from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.agents.jarvis_agent import jarvis_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    success: bool
    response: str
    intermediate_steps: Optional[list] = None
    error: Optional[str] = None

@router.post("/chat", response_model=ChatResponse)
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
            intermediate_steps=result.get("intermediate_steps"),
            error=result.get("error")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/history")
async def get_chat_history():
    """获取对话历史"""
    try:
        memory = jarvis_agent.get_memory()
        return {
            "success": True,
            "history": [
                {
                    "role": msg.type,
                    "content": msg.content
                }
                for msg in memory
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/chat/history")
async def clear_chat_history():
    """清除对话历史"""
    try:
        jarvis_agent.clear_memory()
        return {"success": True, "message": "对话历史已清除"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))