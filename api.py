# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from core.contradiction_checker import ContradictionChecker  # your checker class

# Initialize FastAPI app
app = FastAPI()

# Initialize your contradiction checker
contradiction_checker = ContradictionChecker(threshold=0.75)  # if you have threshold

# Define the request body model
class ClaimRequest(BaseModel):
    sentences: list  # <-- this matches your JSON key

# This is where your endpoint goes
@app.post("/check")
def check_claims(request: ClaimRequest):
    results = []
    for claim in request.sentences:
        result = contradiction_checker.check_contradiction(claim)
        results.append(result)
    return results  # returns a JSON array of results
