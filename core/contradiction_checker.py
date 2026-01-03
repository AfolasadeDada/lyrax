# core/contradiction_checker.py

from core.db import SessionLocal, Claim, Contradiction
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class ContradictionChecker:
    def __init__(self, model_name="roberta-large-mnli", threshold=0.9):
        """
        Initializes the contradiction checker with:
        - tokenizer and MNLI model
        - confidence threshold
        - evaluation mode
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.eval()  # important for deterministic outputs
        self.threshold = threshold

    def check_contradiction(self, new_claim: str):
        """
        Checks if a new claim contradicts any previous claims in the DB.
        Returns a dict with contradiction status and relevant info.
        """
        session = SessionLocal()

        # Fetch all previous claims
        claims = session.query(Claim).all()

        for old in claims:
            score = self._compute_contradiction_score(old.text, new_claim)
            if score > self.threshold:
                # Store contradiction in DB
                contradiction = Contradiction(
                    new_claim=new_claim,
                    against=old.text,
                    score=score
                )
                session.add(contradiction)
                session.commit()
                session.close()
                return {
                    "contradiction": True,
                    "against": old.text,
                    "score": score
                }

        # No contradiction found → store new claim
        claim_obj = Claim(text=new_claim, claim_type="factual")
        session.add(claim_obj)
        session.commit()
        session.close()

        return {"contradiction": False}

    def _compute_contradiction_score(self, claim1: str, claim2: str) -> float:
        """
        Uses RoBERTa MNLI to score contradiction probability between two claims.
        """
        inputs = self.tokenizer(claim1, claim2, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = torch.softmax(logits, dim=1)
            # MNLI index 2 = contradiction
            return probs[0][2].item()
