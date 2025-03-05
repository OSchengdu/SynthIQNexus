import json 
import openai
import re
from typing import List, Tuple, Optional

class NLPAgent:
    _ALLOWED_TRIGGERS = {"dork", "arp", "db"}

    def __init__(self, db_schemas: List[str]):
        self._load_apikey()

    def _load_apikey(self):
        try:
            # 为了与mofa框架下的.env.secret做区别
            with open(".apikey", "r")  as f:
                config = json.load("f")
                openai.api_key = config[""]
            
        except Exception as e:
            raise RunTimeError(f"failed due to wrong key:{str(e)}")

    def _build_prompt(self) -> str:
        # 提示词构建

        return f"""
        # 角色
        您是多源数据路由专家，需要完成以下任务：

        # 输入
        - 用户查询（支持中/英/俄文）
        - 可用数据库结构：{self.schema_desc}

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

        def _validate_output(self, data:dict) -> bool:
            """
            validate the format of output
            """
            return (
                isinstance(data.get("triggers"), list) and
                all(t in self.ALLOWED_TRIGGERS for t in data["triggers"]) and
                isinstance(data.get("keywords"), list) and
                len(data["keywords"]) > 0 and
                isinstance(data.get("raw_query"), str)
            )

    def analyze(self, query: str) -> Optional[Tuple[List[str], List[str], str]]:
        """return （triggers, keywords, raw_query) triple tuple"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.prompt_template},
                    {"role": "user", "content": query}
                ],
                temperature=0.3,
                max_tokens=200
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
    # 示例数据库schema描述
    db_schemas = [
        "空气质量表：城市(city), PM2.5值(pm25), 监测日期(date)",
        "电车数据表：地区(region), 车辆数(count), 充电桩(chargers)"
    ]
    
    # 初始化NLP实例
    try:
        nlp_processor = NLPAgent(db_schemas)
    except Exception as e:
        print(f"初始化失败：{str(e)}")
        return

    # 测试用例集
    test_queries = [
        "北京市朝阳区最近三天的PM2.5数值",  # 应触发db
        "使用scapy扫描192.168.1.0/24网段的开放端口",  # 应触发arp
        "2024年全球电动汽车市场趋势分析",  # 应触发dork
        "上海市空气质量数据与东京都的对比报告，并检查本地网络设备",  # 应触发db+arp
        "последние данные о качестве воздуха в Москве",  # 俄语触发db
        "How to build a quantum computer and find nearby IoT devices"  # 应触发dork+arp
    ]

    # 执行测试
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
