# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from core.confidence_estimator import ConfidenceEstimator, detect_negation

app = FastAPI(title="LYRAx AI Reliability Engine")

estimator = ConfidenceEstimator()

# Request model
class CheckRequest(BaseModel):
    sentences: List[str]

# Response model
class ComparisonResult(BaseModel):
    sentence_1: str
    sentence_2: str
    type: str
    confidence: float

class CheckResponse(BaseModel):
    results: List[ComparisonResult]

# Thresholds
CONTRADICTION_THRESHOLD = 0.65
ENTAILMENT_THRESHOLD = 0.75
NEGATION_BOOST = 0.35

@app.get("/")
def root():
    return {"status": "LYRAx API running"}

@app.post("/check", response_model=CheckResponse)
def check_claims(request: CheckRequest):
    sentences = request.sentences
    results = []

    # Compare all unique pairs
    for i in range(len(sentences)):
        for j in range(i+1, len(sentences)):
            s1 = sentences[i]
            s2 = sentences[j]

            scores = estimator.get_scores(s1, s2)

            # Apply negation detection
            if detect_negation(s1, s2):
                scores["contradiction"] = max(scores["contradiction"], NEGATION_BOOST)

            # Determine type based on scores
            if scores["contradiction"] >= CONTRADICTION_THRESHOLD:
                t = "contradiction"
                conf = scores["contradiction"]
            elif scores["entailment"] >= ENTAILMENT_THRESHOLD:
                t = "entailment"
                conf = scores["entailment"]
            else:
                t = "neutral"
                conf = scores["neutral"]

            results.append({
                "sentence_1": s1,
                "sentence_2": s2,
                "type": t,
                "confidence": round(conf, 2)
            })

    return {"results": results}
