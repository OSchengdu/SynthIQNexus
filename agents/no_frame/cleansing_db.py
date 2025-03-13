from NLP import NLPAgent  
from choose_data import SourceRouter
from openai import OpenAI
import json
from typing import List, Dict, Any

class DataCleanser:
    def __init__(self, results: List[Dict[str, Any]]):
        """
        初始化 DataCleanser。

        :param results: 查询结果，格式为字典列表。
        """
        self.results = results
        self.client = self._load_apikey()

    def _load_apikey(self):
        """加载 API 密钥"""
        try:
            with open(".apikey", "r") as f:
                config = {}
                for line in f:
                    key, value = line.strip().split('=')
                    config[key] = value
                api_key = config.get('SF')
                return OpenAI(api_key=api_key, base_url="https://api.siliconflow.cn/v1")
        except Exception as e:
            raise RuntimeError(f"Failed to load API key: {str(e)}")

    def _build_prompt(self, results: List[Dict[str, Any]]) -> str:
        """
        构建大模型提示词，用于生成数据总结和初步结论。

        :param results: 查询结果，格式为字典列表。
        :return: 提示词字符串。
        """
        # 将结果转换为 JSON 字符串
        results_json = json.dumps(results, indent=2)
        return f"""
        # 角色
        您是数据分析专家，需要根据以下数据生成总结、提取特征并得出初步结论。

        # 输入
        - 数据：{results_json}

        # 输出要求
        严格返回 JSON 对象，包含以下字段：
        {{
            "summary": "数据的基本统计信息和特征",
            "key_info": {{
                "fields": ["关键字段1", "关键字段2"],
                "values": ["关键值1", "关键值2"]
            }},
            "conclusions": ["初步结论1", "初步结论2"]
        }}

        # 规则
        1. 总结应包括数据的基本统计信息（如行数、列数、数值字段的均值、最大值、最小值等）。
        2. 提取关键字段和值，用于生成 Markdown 表格和 URL。
        3. 基于数据分析生成初步结论（如异常值、高频值等）。

        # 示例
        输入：[
            {{
                "Unique ID": 221956,
                "Indicator ID": 386,
                "Name": "Ozone (O3)",
                "Measure": "Mean",
                "Measure Info": "ppb",
                "Geo Type Name": "UHF34",
                "Geo Join ID": 305307,
                "Geo Place Name": "Upper East Side-Gramercy",
                "Time Period": "Summer 2014",
                "Start_Date": "06/01/2014",
                "Data Value": 24.9,
                "Message": "http://example.com/data/221956"
            }}
        ]
        输出：{{
            "summary": "数据包含 1 行，12 列。数值字段 'Data Value' 的均值为 24.9，最大值为 24.9，最小值为 24.9。",
            "key_info": {{
                "fields": ["Name", "Geo Place Name", "Data Value"],
                "values": ["Ozone (O3)", "Upper East Side-Gramercy", 24.9]
            }},
            "conclusions": [
                "数据中未发现异常值。",
                "高频地点：Upper East Side-Gramercy"
            ]
        }}
        """

    def cleanse(self) -> Dict[str, Any]:
        """
        使用大模型对查询结果进行处理，生成总结、关键信息和初步结论。

        :return: 包含总结、关键信息和初步结论的字典。
        """
        try:
            # 构建提示词
            prompt = self._build_prompt(self.results)

            # 调用大模型
            response = self.client.chat.completions.create(
                model='deepseek-ai/DeepSeek-R1-Distill-Qwen-7B',
                messages=[
                    {'role': 'user', 'content': prompt}
                ],
                stream=False
            )

            # 解析大模型输出
            raw_output = response.choices[0].message.content
            parsed = json.loads(raw_output.strip("```json\n").rstrip("```"))

            return parsed

        except Exception as e:
            print(f"数据清洗失败：{str(e)}")
            return {}


# 示例用法
if __name__ == "__main__":
    # 示例数据
    example_results = [
        {
            "Unique ID": 221956,
            "Indicator ID": 386,
            "Name": "Ozone (O3)",
            "Measure": "Mean",
            "Measure Info": "ppb",
            "Geo Type Name": "UHF34",
            "Geo Join ID": 305307,
            "Geo Place Name": "Upper East Side-Gramercy",
            "Time Period": "Summer 2014",
            "Start_Date": "06/01/2014",
            "Data Value": 24.9,
            "Message": "http://example.com/data/221956",
        },
        {
            "Unique ID": 221806,
            "Indicator ID": 386,
            "Name": "Ozone (O3)",
            "Measure": "Mean",
            "Measure Info": "ppb",
            "Geo Type Name": "UHF34",
            "Geo Join ID": 103,
            "Geo Place Name": "Fordham - Bronx Pk",
            "Time Period": "Summer 2014",
            "Start_Date": "06/01/2014",
            "Data Value": 30.7,
            "Message": "http://example.com/data/221806",
        },
    ]

    # 初始化 DataCleanser
    cleanser = DataCleanser(example_results)

    # 执行清洗和总结
    result = cleanser.cleanse()

    # 打印结果
    print("数据总结：", result.get("summary", "无"))
    print("关键信息：", result.get("key_info", "无"))
    print("初步结论：", result.get("conclusions", "无"))
