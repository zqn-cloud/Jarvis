from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class BaseJarvisTool(ABC):
    """所有Jarvis工具的基类"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """工具名称"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """工具描述"""
        pass
    
    @property
    @abstractmethod
    def args_schema(self) -> type:
        """参数模式"""
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """执行工具"""
        pass
    
    def to_langchain_tool(self) -> BaseTool:
        """转换为LangChain工具"""
        class ToolInputSchema(self.args_schema):
            pass
        
        async def _arun(**kwargs):
            return await self.execute(**kwargs)
        
        def _run(**kwargs):
            import asyncio
            return asyncio.run(self.execute(**kwargs))
        
        return BaseTool(
            name=self.name,
            description=self.description,
            args_schema=ToolInputSchema,
            func=_run,
            coroutine=_arun
        )