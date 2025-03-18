import json
import requests
from pydantic import BaseModel
from typing import Dict, Any, Optional
from openai import OpenAI



class WeatherRequestPackage(BaseModel):
    """气象数据请求参数模型"""
    lat: Optional[float] = None
    lon: Optional[float] = None
    model: str = "gfs"
    parameters: list[str] = ["wind", "temp", "pressure"]
    levels: list[str] = ["surface", "800h"]
    metadata: Optional[Dict[str, Any]] = None


class WeatherAnalysisAgent:
    def __init__(self):
        self.windy_key, self.siliconflow_key = self._load_apikey()
        self.siliconflow_client = OpenAI(
            api_key=self.siliconflow_key,
            base_url="https://api.siliconflow.cn/v1"
        )

    def _load_apikey(self) -> tuple[str, str]:
        """加载 API 密钥"""
        try:
            with open(".apikey", "r") as f:
                config = {}
                for line in f:
                    key, value = line.strip().split('=')
                    config[key] = value
                return config["WINDY_KEY"], config["SF"]
        except Exception as e:
            raise RuntimeError(f"Failed to load API key: {str(e)}")

    def _get_current_location(self) -> tuple[float, float]:
        """三级定位策略（IP定位 -> 手动输入 -> 默认坐标）"""
        IP_SERVICES = [
            ("ipapi.co", "https://ipapi.co/json/"),
            ("ipinfo.io", "https://ipinfo.io/json"),
            ("ip.sb", "https://api.ip.sb/geoip")
        ]

        # 尝试IP定位
        for service_name, url in IP_SERVICES:
            try:
                response = requests.get(url, timeout=5)
                data = response.json()
                if 'latitude' in data and 'longitude' in data:
                    print(f"IP定位成功 ({service_name}): {data.get('city', '未知地区')}")
                    return float(data['latitude']), float(data['longitude'])
            except Exception as e:
                print(f"{service_name} 定位失败: {str(e)}")
                continue

        # 默认坐标
        print("使用默认坐标：纽约")
        return (40.7128, -74.0060)

    def _validate_coordinates(self, pkg: WeatherRequestPackage):
        """验证或获取坐标"""
        if pkg.lat is None or pkg.lon is None:
            pkg.lat, pkg.lon = self._get_current_location()
        return pkg

    def _call_windy_api(self, pkg: WeatherRequestPackage) -> Dict:
        """调用Windy API核心方法"""
        pkg = self._validate_coordinates(pkg)
        try:
            response = requests.post(
                "https://api.windy.com/api/point-forecast/v2",
                json={
                    "lat": pkg.lat,
                    "lon": pkg.lon,
                    "model": pkg.model,
                    "parameters": pkg.parameters,
                    "levels": pkg.levels,
                    "key": self.windy_key
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"API调用失败: {str(e)}")
            return {}

    def _generate_analysis_prompt(self, data: Dict) -> str:
        """构建LLM分析提示词"""
        return f"""
        请根据以下JSON格式的气象数据，生成包含关键指标的Markdown表格。要求：

        **表格结构：**
        | 时间 (UTC) | 地面温度 (°C) | 地面风速 (m/s) | 地面风向 | 高空温度 (°C) | 高空风速 (m/s) | 地面气压 (hPa) |
        |------------|----------------|----------------|----------|----------------|----------------|-----------------|

        **处理逻辑：**
        1. 时间转换：将`ts`中的Unix时间戳（毫秒）转换为`YYYY-MM-DD HH:MM`格式
        2. 单位转换：
           - 温度：开尔文→摄氏度（`℃ = K - 273.15`）
           - 气压：帕斯卡→百帕（`hPa = Pa / 100`）
        3. 风速计算：
           - 实际风速 = √(wind_u² + wind_v²)
           - 风向 = arctan2(wind_v, wind_u) 角度转换（0-360°，正北为0°）
        4. 数据筛选：
           - 展示最早5个时间点和最晚5个时间点
           - 标注风速>10m/s的极端值（用**加粗**显示）

        5.输出文件效果示例：
        | 时间 (UTC)       | 地面温度 (°C) | 地面风速 (m/s) | 地面风向 | 高空温度 (°C) | 高空风速 (m/s) | 地面气压 (hPa) |
        |------------------|---------------|----------------|----------|---------------|----------------|----------------|
        | 2025-03-15 05:00 | 7.19          | 5.00           | 343.8°   | -0.04         | 16.51          | 1016.34        |
        | 2025-03-15 08:00 | 14.91         | 1.65           | 214.2°   | 0.86          | 3.80           | 1033.68        |
        | 2025-03-15 11:00 | 1.86          | 3.76           | 108.7°   | 1.43          | 5.35           | 1016.52        |
        | 2025-03-15 14:00 | 5.32          | 7.57           | 13.3°    | 0.48          | 3.25           | 1013.21        |
        | 2025-03-15 17:00 | 9.13          | 0.59           | 182.6°   | -0.64         | 5.58           | 1011.17        |
        | 2025-03-15 20:00 | -0.80         | 2.40           | 203.3°   | -13.95        | **10.34**      | 1013.61        |
        | 2025-03-15 23:00 | 1.64          | 1.07           | 155.3°   | -0.12         | **13.01**      | 1005.34        |
        | 2025-03-16 02:00 | 11.42         | 3.37           | 213.6°   | -4.04         | 2.00           | 1005.70        |
        | 2025-03-16 05:00 | 5.41          | 4.26           | 130.2°   | -4.30         | 6.10           | 1026.81        |
        | 2025-03-16 08:00 | 3.02          | 0.70           | 132.7°   | 2.14          | 0.97           | 1029.41        |



        请按照要求处理成Markdown格式的表格，并且确保相同类型的数据的格式应该一致。
        请按照要求处理成Markdown格式的表格。只需要表格。

        完整数据：
        {json.dumps(data, indent=2)}
        """

    def analyze_weather(self, pkg: WeatherRequestPackage) -> str:
        """端到端分析流程"""
        # 获取原始数据
        raw_data = self._call_windy_api(pkg)


        # 调用LLM分析
        try:
            response = self.siliconflow_client.chat.completions.create(
                model='deepseek-ai/DeepSeek-R1-Distill-Qwen-7B',
                messages=[
                    {'role': 'user', 'content': self._generate_analysis_prompt(raw_data)}
                ],
                stream=False,
                temperature=0.3,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"分析失败: {str(e)}")
            return ""


class ReportGenerator:
    @staticmethod
    def save_report(content: str, filename: str = "weather_report.md"):
        """报告保存模块"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# 气象分析报告\n\n")
            f.write(content)
        print(f"报告已保存至 {filename}")


# 修改使用示例
if __name__ == "__main__":
    # 自动获取位置的请求参数
    request_pkg = WeatherRequestPackage()

    # 执行分析流程
    analyzer = WeatherAnalysisAgent()
    report = analyzer.analyze_weather(request_pkg)

    # 生成并保存报告
    if report:
        ReportGenerator.save_report(report)