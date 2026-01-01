from core.db import SessionLocal, Claim, Contradiction
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class ContradictionChecker:
    def __init__(self, model_name="roberta-large-mnli", threshold=0.9):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.threshold = threshold
        self.session = SessionLocal()

    def check_contradiction(self, new_claim: str):
        # Get previous claims from DB
        claims = self.session.query(Claim).all()
        for old in claims:
            score = self._compute_contradiction_score(old.text, new_claim)
            if score > self.threshold:
                # store contradiction
                contradiction = Contradiction(
                    new_claim=new_claim, against=old.text, score=score
                )
                self.session.add(contradiction)
                self.session.commit()
                return {"contradiction": True, "against": old.text, "score": score}

        # store new claim
        claim_obj = Claim(text=new_claim, claim_type="factual")
        self.session.add(claim_obj)
        self.session.commit()
        return {"contradiction": False}

    def _compute_contradiction_score(self, claim1, claim2):
        inputs = self.tokenizer(claim1, claim2, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = torch.softmax(logits, dim=1)
            # contradiction is index 2 in MNLI
            return probs[0][2].item()
