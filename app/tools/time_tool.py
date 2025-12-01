import pytz
from datetime import datetime
from typing import Optional

def get_current_time(location: str = None) -> str:
    """获取指定地点的当前时间。"""
    timezones = {
        "new york": "America/New_York",
        "san francisco": "America/Los_Angeles", 
        "london": "Europe/London",
        "tokyo": "Asia/Tokyo",
        "beijing": "Asia/Shanghai",
        "paris": "Europe/Paris",
        "shenzhen": "Asia/Shanghai",
        "shanghai": "Asia/Shanghai",
        "hong kong": "Asia/Hong_Kong",
        "seoul": "Asia/Seoul",
        "singapore": "Asia/Singapore"
    }
    
    if location and location.lower() in timezones:
        tz = pytz.timezone(timezones[location.lower()])
        now = datetime.now(tz)
        return f"📍 {location} 当前时间: {now.strftime('%Y年%m月%d日 %H:%M:%S %Z')}"
    else:
        now = datetime.now()
        return f"🕐 当前时间: {now.strftime('%Y年%m月%d日 %H:%M:%S')}"

def parse_time_expression(text: str) -> str:
    """解析自然语言时间表达式，如'明天下午三点'或'next Monday at 2pm'。"""
    try:
        # 这里可以集成更复杂的时间解析库，如dateparser
        # 暂时返回简单解析
        import dateparser
        
        parsed = dateparser.parse(text, languages=['zh', 'en'])
        if parsed:
            return f"✅ 解析 '{text}' 为: {parsed.strftime('%Y年%m月%d日 %H:%M')}"
        else:
            return f"❌ 无法解析时间表达式: {text}"
    except ImportError:
        return "⚠️ 请安装 dateparser 库来解析时间表达式: pip install dateparser"