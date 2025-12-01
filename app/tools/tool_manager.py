from typing import Dict, List, Any
from langchain.tools import BaseTool
from app.tools.time_tools import time_parser_tool, current_time_tool
from app.tools.weather_tools import weather_tool
from app.tools.calendar_tools import calendar_tool, list_events_tool

class ToolManager:
    """管理所有工具"""
    
    def __init__(self):
        self.tools = {}
        self._register_tools()
    
    def _register_tools(self):
        """注册所有工具"""
        # 时间工具
        self.register_tool(time_parser_tool)
        self.register_tool(current_time_tool)
        
        # 天气工具
        self.register_tool(weather_tool)
        
        # 日历工具
        self.register_tool(calendar_tool)
        self.register_tool(list_events_tool)
    
    def register_tool(self, tool_instance):
        """注册单个工具"""
        langchain_tool = tool_instance.to_langchain_tool()
        self.tools[tool_instance.name] = {
            "instance": tool_instance,
            "langchain_tool": langchain_tool
        }
        print(f"已注册工具: {tool_instance.name}")
    
    def get_langchain_tools(self) -> List[BaseTool]:
        """获取所有LangChain工具"""
        return [tool["langchain_tool"] for tool in self.tools.values()]
    
    def get_tool(self, name: str):
        """获取指定工具"""
        return self.tools.get(name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """列出所有工具信息"""
        return [
            {
                "name": name,
                "description": tool["instance"].description,
                "args_schema": str(tool["instance"].args_schema)
            }
            for name, tool in self.tools.items()
        ]

# 全局工具管理器
tool_manager = ToolManager()