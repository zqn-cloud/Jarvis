import os
import requests
from typing import Optional

def get_weather(city: str, date: Optional[str] = None) -> str:
    """获取指定城市的天气信息。"""
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY", "")
        
        if not api_key:
            return "请设置 OPENWEATHER_API_KEY 环境变量"
        
        # 直接使用城市名查询当前天气
        weather_url = "http://api.openweathermap.org/data/2.5/weather"
        weather_params = {
            'q': city,
            'appid': api_key,
            'units': 'metric',  # 使用摄氏度
            'lang': 'zh_cn'     # 中文描述
        }
        
        response = requests.get(weather_url, params=weather_params)
        weather_data = response.json()
        
        if weather_data.get('cod') != 200:
            error_msg = weather_data.get('message', 'Unknown error')
            return f"获取天气失败: {error_msg}"
        
        # 解析天气数据
        main_weather = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind'].get('speed', 0)
        city_name = weather_data.get('name', city)
        country = weather_data['sys'].get('country', '')
        
        # 生成天气报告
        location_info = f"{city_name}, {country}" if country else city_name
        date_info = f"在 {date}" if date else "当前"
        
        weather_report = (
            f"🌤️ {location_info}{date_info}天气：\n"
            f"• 天气状况：{description}\n"
            f"• 温度：{temp}°C (体感{feels_like}°C)\n"
            f"• 湿度：{humidity}%\n"
            f"• 风速：{wind_speed} m/s"
        )
        
        # 添加智能提醒
        reminders = generate_weather_reminders(main_weather, temp, humidity)
        if reminders:
            weather_report += f"\n📝 提醒：{'; '.join(reminders)}"
        
        return weather_report
        
    except Exception as e:
        return f"获取天气信息时出错: {str(e)}"

def generate_weather_reminders(weather_condition: str, temperature: float, humidity: float) -> list:
    """根据天气条件生成智能提醒"""
    reminders = []
    
    weather_lower = weather_condition.lower()
    
    # 基于天气状况的提醒
    if any(rain_word in weather_lower for rain_word in ['rain', 'drizzle', 'shower']):
        reminders.append("🌧️ 有雨，记得带伞")
    elif any(snow_word in weather_lower for snow_word in ['snow', 'sleet']):
        reminders.append("❄️ 下雪了，注意保暖和防滑")
    elif 'thunderstorm' in weather_lower:
        reminders.append("⚡ 雷雨天气，避免户外活动")
    elif 'fog' in weather_lower or 'mist' in weather_lower:
        reminders.append("🌫️ 有雾，注意交通安全")
    
    # 基于温度的提醒
    if temperature > 30:
        reminders.append("🔥 天气炎热，注意防晒补水")
    elif temperature < 5:
        reminders.append("🥶 天气寒冷，记得多穿衣服")
    elif 20 <= temperature <= 26:
        reminders.append("😊 温度舒适，适合户外活动")
    
    # 基于湿度的提醒
    if humidity > 80:
        reminders.append("💦 湿度较高，可能感觉闷热")
    elif humidity < 30:
        reminders.append("🍃 空气干燥，注意补水")
    
    return reminders