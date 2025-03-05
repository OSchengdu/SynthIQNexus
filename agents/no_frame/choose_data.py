from NLP import NLPAgent
from typing import List, Dict, Tuple, Optional

class SourceRouter:
    def __init__(self):
        self.processors = {
            "db": self._handle_db,
            "arp": self._handle_arp,
            "dork": self._handle_dork
        }

    def route(self, triggers: List[str], keywords: List[str], raw_query: str) -> dict:
        # 用户的输入也可能有多个领域
        """动态路由到多个处理器"""
        results = {}
        # now we can trigger  multiple triggers       
        for trigger in triggers:
            if handler := self.processors.get(trigger):
                results[trigger] = handler(keywords, raw_query)
                
        return results

    def _handle_db(self, keywords, _):
        print(f"[DB] 查询关键词：{keywords}")
        return {"status": "success", "data": [...]}

    def _handle_arp(self, _, raw_query):
        print(f"[ARP] 原始查询：{raw_query}")
        return {"devices": [...]}

    def _handle_dork(self, keywords, _):
        print(f"[DORK] 搜索关键词：{keywords}")
        return {"links": [...]}

# if __name__ == "__main__":
#     # NLP
#     nlp = NLP([
#         "空气质量表：城市/PM2.5值/日期",
#         "电车数据表：地区/车辆数/充电桩"
#     ])
#     
#     query = "上海市空气质量数据和东京的开放网络设备"
#     analysis = nlp.analyze(query)
#     
#     if analysis:
#         triggers, keywords, raw_query = analysis
#         print(f"Triggers: {triggers}")
#         print(f"Keywords: {keywords}")
#         print(f"Raw Query: {raw_query}")
#     # process       
#         router = SourceRouter()
#         results = router.route(triggers, keywords, raw_query)
#         print("处理结果：", results)
