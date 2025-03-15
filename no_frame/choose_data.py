from typing import List, Dict, Tuple, Optional
from NLP import NLPAgent
class SourceRouter:
    def __init__(self):
        self.processors = {
            "db": self._handle_db,
            "arp": self._handle_arp,
            "dork": self._handle_dork
        }

    def route(self, triggers: List[str], keywords: List[str], raw_query: str) -> dict:
        """动态路由到多个处理器"""
        results = {}
        # now we can trigger multiple triggers
        for trigger in triggers:
            if handler := self.processors.get(trigger):
                results[trigger] = handler(keywords, raw_query)
        return results

    def _handle_db(self, keywords, _):
        print(f"[DB] 查询关键词：{keywords}")
        return {"status": "success", "data": ["example_db_result_1", "example_db_result_2"]}

    def _handle_arp(self, _, raw_query):
        print(f"[ARP] 原始查询：{raw_query}")
        return {"devices": ["device_1", "device_2"]}

    def _handle_dork(self, keywords, _):
        print(f"[DORK] 搜索关键词：{keywords}")
        return {"links": ["link_1", "link_2"]}

if __name__ == "__main__":
    # Initialize NLPAgent with database schemas
    nlp = NLPAgent([
        "空气质量表：城市(city), PM2.5值(pm25), 监测日期(date)",
        "电车数据表：地区(region), 车辆数(count), 充电桩(chargers)"
    ])

    query = "上海市空气质量数据和东京的开放网络设备"
    analysis = nlp.analyze(query)

    if analysis:
        triggers, keywords, raw_query = analysis
        print(f"Triggers: {triggers}")
        print(f"Keywords: {keywords}")
        print(f"Raw Query: {raw_query}")

        # Process the results
        router = SourceRouter()
        results = router.route(triggers, keywords, raw_query)
        print("处理结果：", results)
    else:
        print("分析失败")

