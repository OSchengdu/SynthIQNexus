from elasticsearch import Elasticsearch

class ElasticsearchWrapper:
    def __init__(self):
        self.es = Elasticsearch()

    def index_document(self, index, doc):
        return self.es.index(index=index, document=doc)
