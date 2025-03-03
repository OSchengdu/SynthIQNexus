import json
import os 
import openai
import sqlite3
from typing import Optional, List, Tuple
 
apikey=""

class NLP:
    def __init_(self, db_schema_names:list[str]):
        self._load_apikey()
        self.schemas = self._get_db_schema(db_schema_names)
        self.role_prompt = self.role()

    def _load_apikey():
        try:
            with open(."apikey". "r") as f :
                config = json.load(f)
                self.apikey = config.get("")
                if not self.apikey:
                    raise ValueError("没找到apikey")
                
                openai.api_key
    
    def _get_db_schema():
        pass
    
    def role():
        # generated by ai,如果你专业的话可以帮帮忙
        return """
         你是一个专业的自然语言处理智能体，负责将用户输入的自然语言转化成易于下下级智能体（dork语言生成智能体和sqlLite语言生成智能体）理解需求的自然语言描述
         ### 已有信息
         1. 已有的数据库及其息：
         2. dork搜索工具链接：
         3. dork搜索工具规则
         4. dork语言：
         5. 已知数据库的schema信息
         
         ### 示例：
         案例1：
            用户输入：电动车投入使用后，对气候的影响如何

            你输出：
            
         案例2：
         用户输入：我想探索太空

         你输出：
         
         ---

         ### 


        """

# NOTE: 测试完成
    def generate(self, query: str, max_retries: int=6)-> Optional[str]:
        prompt = f"""
        {self.role_prompt}
        可用的数据库
        {self.schemas}
        可用的dork源
        {self.dork_src}
        """
        for _ in range(max_retries):
            try:
                response = openai.ChatCompletion.create(
                    model="",
                    messages=[
                        {"role": "system", "content": "你是一个自然语言处理专家"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=200
                )
                raw_sql = response.choices[0].message.content.strip()

                # 清洗输出
                sql = self._sanitize_sql(raw_sql)
                if self._validate_sql(sql):
                    return sql

            except Exception as e:
                print(f"生成失败：{str(e)}")
                continue

        return None

if __name__ == "__main__":
    apikey_content = """
    {
        "":"sk-"
    }
    """
    with open('.apikey', 'w') as f:
        f.write(apikey_content)



