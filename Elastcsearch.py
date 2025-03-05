# from elasticsearch official website, a sample

from elasticsearch import Elasticsearch
client = Elasticsearch(
    "https://my-elasticsearch-project-b9f2ee.es.us-east-1.aws.elastic.cloud:443",
    api_key="Ym1UMlhwVUI3anBNRVpJN2d4QmI6YkpxQ2tETGpRWDBuTVpCNzktUUg5dw=="
)
index_name = "poly-nexus"
mappings = {
    "properties": {
        "text": {
            "type": "text"
        }
    }
}
mapping_response = client.indices.put_mapping(index=index_name, body=mappings)
print(mapping_response)
