from transformers import pipeline

class NLPEngine:
    def __init__(self):
        self.classifier = pipeline("text-classification")

    def classify_text(self, text):
        return self.classifier(text)
