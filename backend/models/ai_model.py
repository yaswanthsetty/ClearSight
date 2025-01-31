from transformers import pipeline

classifier = pipeline("text-classification", model="facebook/roberta-hate-speech-dynabench-r4-target")

def analyze_text(text):
    return classifier(text)
