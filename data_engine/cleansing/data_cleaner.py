import re

class DataCleaner:
    @staticmethod
    def clean_text(text):
        return re.sub(r'\s+', ' ', text).strip()
