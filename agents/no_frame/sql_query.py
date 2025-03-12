import json
import sqlite3
from typing import List, Dict, Optional
from NLP import NLPAgent  # 引入 NLP 模块
from choose_data import SourceRouter  # 引入 choose_data 模块
from openai import OpenAI
class SQLExecutor:
    def __init__(self, db_schemas: List[str], db_path: str = "data.db"):
        self.db_schemas = db_schemas
        self.db_path = db_path
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

    def _build_prompt(self, keywords: List[str], raw_query: str) -> str:
        """构建 LLM 提示词"""
        return f"""
        # 角色
        您是 SQL 生成专家，需要根据用户查询生成 SQL 语句。

        # 输入
        - 用户查询：{raw_query}
        - 关键词：{keywords}
        - 数据库结构：{self.db_schemas}

        # 输出要求
        严格返回 JSON 对象，包含以下字段：
        {{
            "sql": "生成的 SQL 语句",
            "tables": ["涉及的表名"],
            "fields": ["涉及的字段名"]
        }}

        # 规则
        1. SQL 语句必须符合 SQLite 语法。
        2. 仅生成 SELECT 查询语句。
        3. 如果查询涉及多个表，请使用 JOIN。
        4. 如果查询条件不明确，请使用通配符（如 %）或默认值。

        # 示例
        输入：查询北京市最近三天的 PM2.5 数据
        输出：{{
            "sql": "SELECT city, pm25, date FROM air_quality WHERE city = '北京' AND date >= date('now', '-3 days')",
            "tables": ["air_quality"],
            "fields": ["city", "pm25", "date"]
        }}
        """

    def _validate_sql(self, sql: str) -> bool:
        """验证 SQL 语句的合法性"""
        # 简单检查是否为 SELECT 语句
        return sql.strip().lower().startswith("select")

    def _execute_sql(self, sql: str) -> List[Dict]:
        """执行 SQL 语句并返回结果"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row  # 返回字典格式的结果
                cursor = conn.cursor()
                cursor.execute(sql)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            print(f"SQL 执行失败：{str(e)}")
            return []

    def generate_and_execute(self, keywords: List[str], raw_query: str) -> Optional[Dict]:
        """生成 SQL 并执行查询"""
        try:
            # 生成 SQL
            response = self.client.chat.completions.create(
                model='deepseek-ai/DeepSeek-R1-Distill-Qwen-7B',
                messages=[
                    {'role': 'user', 'content': self._build_prompt(keywords, raw_query)},
                    {'role': 'user', 'content': raw_query}
                ],
                stream=False
            )

            raw_output = response.choices[0].message.content
            parsed = json.loads(raw_output.strip("```json\n").rstrip("```"))

            if self._validate_sql(parsed.get("sql")):
                sql = parsed["sql"]
                print(f"生成的 SQL：{sql}")

                # 执行 SQL
                results = self._execute_sql(sql)
                return {
                    "results": results,
                    "tables": parsed.get("tables", []),
                    "fields": parsed.get("fields", [])
                }
            else:
                print("生成的 SQL 语句不合法")
                return None

        except Exception as e:
            print(f"SQL 生成或执行失败：{str(e)}")
            return None

    def fallback_execute(self, keywords: List[str], tables: List[str]) -> List[Dict]:
        """传统方法生成并执行 SQL 语句（备用方案）"""
        # 简单实现：根据关键词和表名生成 SQL
        conditions = " AND ".join([f"{field} LIKE '%{keyword}%'" for keyword in keywords for field in ["city", "region"]])
        sql = f"SELECT * FROM {tables[0]} WHERE {conditions}"
        print(f"备用 SQL：{sql}")
        return self._execute_sql(sql)

def main():
    # 初始化 NLPAgent 和 SourceRouter
    db_schemas = [
        "空气质量表：城市(city), PM2.5值(pm25), 监测日期(date)",
        "电车数据表：地区(region), 车辆数(count), 充电桩(chargers)"
    ]
    nlp = NLPAgent(db_schemas)
    router = SourceRouter()

    # 测试查询
    query = "查询北京市最近三天的 PM2.5 数据"
    analysis = nlp.analyze(query)

    if analysis:
        triggers, keywords, raw_query = analysis
        print(f"Triggers: {triggers}")
        print(f"Keywords: {keywords}")
        print(f"Raw Query: {raw_query}")

        # 路由到 DB 处理器
        if "db" in triggers:
            db_results = router.route(["db"], keywords, raw_query)
            print("DB 处理结果：", db_results)

            # 生成并执行 SQL
            sql_executor = SQLExecutor(db_schemas)
            sql_result = sql_executor.generate_and_execute(keywords, raw_query)

            if sql_result:
                print("查询结果：", sql_result["results"])
                print("涉及的表：", sql_result["tables"])
                print("涉及的字段：", sql_result["fields"])
            else:
                # 备用方案
                print("使用传统方法生成并执行 SQL")
                fallback_results = sql_executor.fallback_execute(keywords, db_results["db"]["data"])
                print("备用查询结果：", fallback_results)
        else:
            print("无需生成 SQL")
    else:
        print("分析失败")

if __name__ == "__main__":
    main()
