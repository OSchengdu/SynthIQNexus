class QueryRanker:
    def rank(self, queries):
        return sorted(queries, key=lambda x: x['frequency'], reverse=True)
