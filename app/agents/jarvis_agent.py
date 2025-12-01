import os
from typing import Dict, Any, List
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

# 导入工具
from app.tools.weather_tool import get_weather
from app.tools.time_tool import get_current_time, parse_time_expression
from app.tools.calendar_tool import create_calendar_event, get_calendar_events
from app.config import config

os.environ["OPENAI_API_BASE"] = ''
os.environ["OPENAI_API_KEY"] = 'sk-'
os.environ["OPENWEATHER_API_KEY"] = ''


class JarvisAgent:
    """Jarvis 智能助手"""
    
    def __init__(self):
        self.llm = self._initialize_llm()
        self.tools = self._initialize_tools()
        self.system_prompt = self._create_system_prompt()
        self.agent = self._create_agent()
    
    def _initialize_llm(self):
        """初始化 LLM"""
        return ChatOpenAI(
            model='gpt-3.5-turbo',
            # openai_api_base=config.OPENAI_API_BASE,
            # openai_api_key=config.OPENAI_API_KEY,
            temperature=0.7,
            streaming=False
        )
    
    def _initialize_tools(self) -> List:
        """初始化工具列表"""
        return [
            get_weather,
            get_current_time,
            parse_time_expression,
            create_calendar_event,
            get_calendar_events
        ]
    
    def _create_system_prompt(self) -> str:
        """创建系统提示词"""
        return """你是 Jarvis，一个智能日程管理助手。你的职责包括：

1. **时间管理**：帮助用户解析自然语言时间，查询各地时间
2. **天气查询**：提供天气信息和智能提醒
3. **日历管理**：创建、查看日历事件

请友好、专业地帮助用户。如果信息不完整，请主动询问用户。

工具使用说明：
- get_weather: 查询城市天气，参数: city (城市名), date (可选日期)
- get_current_time: 查询当前时间，参数: location (可选地点)
- parse_time_expression: 解析时间表达式，参数: text (时间文本)
- create_calendar_event: 创建日历事件，参数: title, start_time, end_time(可选), location(可选), description(可选)
- get_calendar_events: 获取日历事件，参数: start_date(可选), end_date(可选)
"""
    
    def _create_agent(self):
        """创建 Agent"""
        return create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.system_prompt,
        )
    
    async def process_query(self, user_input: str) -> Dict[str, Any]:
        """处理用户查询"""
        try:
            result = self.agent.invoke(
                {"messages": [{"role": "user", "content": user_input}]}
            )
            
            return {
                "success": True,
                "response": result['messages'][-1].content,
                "raw_result": result
            }
            
        except Exception as e:
            return {
                "success": False,
                "response": f"抱歉，处理请求时出现错误：{str(e)}",
                "error": str(e)
            }
    
    def get_tools_info(self) -> List[Dict]:
        """获取工具信息"""
        return [
            {
                "name": tool.__name__,
                "description": tool.__doc__ or "没有描述",
                "module": tool.__module__
            }
            for tool in self.tools
        ]

# 全局 Agent 实例
jarvis_agent = JarvisAgent()
