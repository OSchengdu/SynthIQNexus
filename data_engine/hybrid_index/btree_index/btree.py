class BTreeIndex:
    def __init__(self):
        self.index = {}

    def insert(self, key, value):
        self.index[key] = value

    def search(self, key):
        return self.index.get(key)
