from elasticsearch import Elasticsearch

class DorkAgent:
    def __init__(self, es_host:str = "https://localhost:9200")
        self.es = Elasticsearch(es_host)

    def dork_search(self, index: str, dsl: Dict) -> List[Dict]:
        resp = self.search(index)

