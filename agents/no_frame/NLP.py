import json
import re
from typing import List, Tuple, Optional
from openai import OpenAI

class NLPAgent:
    _ALLOWED_TRIGGERS = {"dork", "arp", "db", "map"}

    def __init__(self, db_schemas: List[str]):
        self.db_schemas = db_schemas
        self.client = self._load_apikey()

    def _load_apikey(self):
        try:
            with open(".apikey", "r") as f:
                config = {}
                for line in f:
                    key, value = line.strip().split('=')
                    config[key] = value
                api_key = config.get('SF')  
                return OpenAI(api_key=api_key, base_url="https://api.siliconflow.cn/v1")
        except Exception as e:
            raise RuntimeError(f"Failed due to wrong key: {str(e)}")
#         finally:
#             print("Parsed config:", config, value, key)

    def _build_prompt(self) -> str:
        return f"""
        # 角色
        您是多源数据路由专家，需要完成以下任务：

        # 输入
        - 用户查询（支持中/英/俄文）
        - 可用数据库结构：{self.db_schemas}

        # 输出要求
        严格返回JSON对象，包含以下字段：
        {{
            "triggers": ["dork", "arp", "db"]的子集,
            "keywords": ["关键词1", "关键词2", ...],
            "raw_query": "原始用户输入"
        }}

        # 规则
        1. triggers选择逻辑：
           - 当需要深网搜索时添加"dork"
           - 当涉及设备扫描时添加"arp"
           - 当匹配数据库字段时添加"db"
        2. 多个trigger可同时存在（如同时需要db和dork）
        3. keywords需从查询中提取3-5个核心词

        # 示例
        输入：北京市PM2.5数据和附近开放WiFi
        输出：{{
            "triggers": ["db", "arp"],
            "keywords": ["北京", "PM2.5", "开放WiFi"],
            "raw_query": "北京市PM2.5数据和附近开放WiFi"
        }}
        """

    def _validate_output(self, data: dict) -> bool:
        return (
            isinstance(data.get("triggers"), list) and
            all(t in self._ALLOWED_TRIGGERS for t in data["triggers"]) and
            isinstance(data.get("keywords"), list) and
            len(data["keywords"]) > 0 and
            isinstance(data.get("raw_query"), str)
        )

    def analyze(self, query: str) -> Optional[Tuple[List[str], List[str], str]]:
        """return (triggers, keywords, raw_query) triple tuple"""
        try:
            response = self.client.chat.completions.create(
                model='deepseek-ai/DeepSeek-R1-Distill-Qwen-7B',
                messages=[
                    {'role': 'user', 'content': self._build_prompt()},
                    {'role': 'user', 'content': query}
                ],
                stream=False
            )

            raw_output = response.choices[0].message.content
            parsed = json.loads(raw_output.strip("```json\n").rstrip("```"))

            if self._validate_output(parsed):
                return (
                    parsed["triggers"],
                    parsed["keywords"],
                    parsed["raw_query"]
                )
            else:
                print("输出格式验证失败")
                return None

        except Exception as e:
            print(f"分析失败：{str(e)}")
            return None

def main():
    db_schemas = [
        "空气质量表：城市(city), PM2.5值(pm25), 监测日期(date)",
        "电车数据表：地区(region), 车辆数(count), 充电桩(chargers)"
    ]

    try:
        nlp_processor = NLPAgent(db_schemas)
    except Exception as e:
        print(f"初始化失败：{str(e)}")
        return

    test_queries = [
        "北京市朝阳区最近三天的PM2.5数值",
        "使用scapy扫描192.168.1.0/24网段的开放端口",
        "2024年全球电动汽车市场趋势分析",
        "上海市空气质量数据与东京都的对比报告，并检查本地网络设备",
        "последние данные о качестве воздуха в Москве",
        "How to build a quantum computer and find nearby IoT devices"
    ]

    print("="*40)
    print("NLP模块测试报告")
    print("="*40)

    for idx, query in enumerate(test_queries, 1):
        print(f"\n测试用例 #{idx}")
        print(f"输入：{query}")

        result = nlp_processor.analyze(query)

        if result:
            triggers, keywords, raw = result
            print(f"[输出]")
            print(f"触发器：{', '.join(triggers)}")
            print(f"关键词：{keywords}")
            print(f"原始查询：{raw}")
        else:
            print("!! 分析失败")

if __name__ == "__main__":
    main()
