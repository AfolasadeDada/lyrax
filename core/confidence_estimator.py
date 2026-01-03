# confidence_estimator.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class ConfidenceEstimator:
    def __init__(self, model_name="roberta-large-mnli"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

    def get_scores(self, sentence1: str, sentence2: str):
        """
        Returns a dict with entailment, neutral, and contradiction scores
        """
        inputs = self.tokenizer(sentence1, sentence2, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = torch.softmax(logits, dim=1)
            return {
                "entailment": probs[0][0].item(),
                "neutral": probs[0][1].item(),
                "contradiction": probs[0][2].item()
            }

def detect_negation(s1: str, s2: str) -> bool:
    """
    Returns True if s2 negates s1
    """
    neg_words = ["not", "never", "no", "none"]
    s1_words = s1.lower().split()
    s2_words = s2.lower().split()
    for word in neg_words:
        if (word in s1_words and word not in s2_words) or (word in s2_words and word not in s1_words):
            return True
    return False
