from elasticsearch import Elasticsearch, Helpers
from typing import List, Dict

class DorkAgent:
    def __init__(self, es_hosts:list[str], index_name: str = "air_quality"):
        self.es = Elasticsearch(
                es_hosts
                # 开启es调用, 留空部分填上密码
                basic_auth=("elastics", "")
                # 禁用证书验证
                verify_certs=False
                )
        self.index = index_name
        self._init_index()
       
    def _init_index(self):
        if not self.es.indices.exists(index=self.index):
            self.es.indices.create(
                index = self.index
                body= {"settings": {
                        "analysis": {
                            "analyzer": {
                                "cn_analyzer": {
                                    "type": "custom",
                                    # 目前只有英文素材，如有其他，添加如ik分词器等插件
                                    "tokenizer": "english"
                                }
                            }
                        }
                    },
                    "mappings": {
                        "properties": {
                            "city": {"type": "keyword"},
                            "pm25": {"type": "float"},
                            "measure_info": {
                                "type": "text",
                                "analyzer": "cn_analyzer"
                            },
                            "timestamp": {"type": "date"}
                        }
                    }
                }
            )


    def dork_search(self, index: str, dsl: Dict) -> List[Dict]:
        resp = self.es.search(
            index=self.index,
            # 填入json形式的关键词混合搜索结构
            body={}
                )
        return self._format_results(resp)

    def _format_results(self, resp: Dict) -> List[Dict]
        return [
            {
                **hit["*_source"],
                "highlight": hit.get("highlight", {})
            }
            for hit in resp["hits"]["hits"]
        ]

    # update from sqlite3 per 5 min
    def sync_from_sqlte(self, sqlite_path: str):
        import sqlite3
        import pandas as pd
        conn = sqlite3.connect(sqlite_path)
        df = pd.read_sql("select * from air_quality", conn)
        records = df.to_dict(orient="records")
        actions = [
                {"_index":self.index, "_source": record}
                for record in records
            ]
        Helpers.bulk(self.es, actions)

