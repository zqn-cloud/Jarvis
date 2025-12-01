from datetime import datetime, timedelta
from typing import Optional, Dict, List
import json

# 简单的内存存储（实际项目中应该用数据库）
calendar_events = []

def create_calendar_event(
    title: str,
    start_time: str,
    end_time: Optional[str] = None,
    location: Optional[str] = None,
    description: Optional[str] = None
) -> str:
    """创建日历事件。"""
    try:
        # 解析开始时间
        start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        
        # 如果没有结束时间，默认1小时
        if end_time:
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        else:
            end_dt = start_dt + timedelta(hours=1)
        
        event = {
            "id": len(calendar_events) + 1,
            "title": title,
            "start_time": start_dt.isoformat(),
            "end_time": end_dt.isoformat(),
            "location": location,
            "description": description,
            "created_at": datetime.now().isoformat()
        }
        
        calendar_events.append(event)
        
        return f"已创建事件: {title} ({start_dt.strftime('%Y年%m月%d日 %H:%M')})"
        
    except Exception as e:
        return f"创建事件失败: {str(e)}"

def get_calendar_events(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """获取日历事件。"""
    try:
        filtered_events = calendar_events
        
        if start_date:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            filtered_events = [
                e for e in filtered_events 
                if datetime.fromisoformat(e["start_time"].replace('Z', '+00:00')) >= start_dt
            ]
        
        if end_date:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            filtered_events = [
                e for e in filtered_events
                if datetime.fromisoformat(e["start_time"].replace('Z', '+00:00')) <= end_dt
            ]
        
        if not filtered_events:
            return "没有找到相关事件。"
        
        result = f"找到 {len(filtered_events)} 个事件:\n"
        for event in filtered_events:
            start_dt = datetime.fromisoformat(event["start_time"].replace('Z', '+00:00'))
            result += f"• {event['title']} - {start_dt.strftime('%m月%d日 %H:%M')}"
            if event.get('location'):
                result += f" @ {event['location']}"
            result += "\n"
        
        return result
        
    except Exception as e:
        return f"获取事件失败: {str(e)}"