import pandas as pd
from typing import Dict, List, Any
from pydantic import BaseModel
import json
import openai

class DataPackage(BaseModel):
    source: str  # 来源标识：db/dork/arp
    raw_data: List[Dict[str, Any]]  # 原始数据
    metadata: Dict[str, Any]  # 附加信息（如SQL查询参数）

class CleansingAgent:
    def __init__(self):
        self._load_models()
        
    def _load_models(self):
        """初始化清洗模型（示例使用OpenAI）"""
        with open(".apikey") as f:
            openai.api_key = json.load(f)["openai_key"]

    def _clean_generic(self, data: List[Dict]) -> pd.DataFrame:
        """通用清洗流程"""
        df = pd.DataFrame(data)
        # 基础清洗步骤
        df = df.drop_duplicates()
        df = df.dropna(how='all')
        return df

    def _clean_with_llm(self, df: pd.DataFrame, source: str) -> pd.DataFrame:
        """基于来源的智能清洗"""
        prompt = f"""
        请根据数据来源类型执行清洗操作：
        - 来源：{source}
        - 数据样例：{df.head(1).to_dict()}
        
        需要执行的操作（按优先级）：
        1. 识别并修复明显错误（如负值的PM2.5）
        2. 标准化时间格式为YYYY-MM-DD
        3. 统一地域名称（如"北京"→"北京市"）
        4. 移除测试数据（包含'test'的条目）
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "你是数据清洗专家"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            cleaning_logic = response.choices[0].message.content
            # 此处应解析模型输出为实际清洗代码，简化为示例
            return df.query("pm25 > 0")  # 示例逻辑
        except:
            return df  # 模型失败时返回基础清洗结果

    def process(self, inputs: List[DataPackage]) -> Dict[str, pd.DataFrame]:
        """主清洗流程"""
        cleaned_groups = {}
        
        for pkg in inputs:
            # 阶段1：基础清洗
            df = self._clean_generic(pkg.raw_data)
            
            # 阶段2：智能清洗
            df = self._clean_with_llm(df, pkg.source)
            
            # 按来源分组存储
            if pkg.source not in cleaned_groups:
                cleaned_groups[pkg.source] = []
            cleaned_groups[pkg.source].append(df)
        
        # 合并同源数据
        return {
            source: pd.concat(dfs).reset_index(drop=True)
            for source, dfs in cleaned_groups.items()
        }

class GenerateAgent:
    def receive_data(self, data: Dict[str, pd.DataFrame]):
        """模拟生成智能体接收数据"""
        for source, df in data.items():
            print(f"接收来自 {source} 的数据（{len(df)} 条）")
            print(df.head())

# 测试用例
if __name__ == "__main__":
    # 模拟输入数据
    test_data = [
        DataPackage(
            source="db",
            raw_data=[
                {"city": "北京", "pm25": 45, "date": "2023-01-01"},
                {"city": "test", "pm25": -5, "date": "invalid_date"}
            ],
            metadata={"table": "air_quality"}
        ),
        DataPackage(
            source="dork",
            raw_data=[
                {"title": "北京空气质量报告", "content": "PM2.5值达到80μg/m³", "source": "深网论坛"},
                {"title": "test data", "content": "ignore this", "source": "测试站点"}
            ],
            metadata={"search_keywords": ["北京 PM2.5"]}
        )
    ]

    # 执行清洗
    cleaner = CleansingAgent()
    cleaned_data = cleaner.process(test_data)
    
    # 传递给生成智能体
    generator = GenerateAgent()
    generator.receive_data(cleaned_data)
