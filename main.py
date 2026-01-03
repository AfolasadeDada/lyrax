# main.py

from core.claim_classifier import classify_claims  # your existing claim classifier
from core.contradiction_checker import ContradictionChecker

# Initialize contradiction checker with 90% threshold
checker = ContradictionChecker(threshold=0.9)

# Example input claims
claims_input = [
    "The sky is blue",
    "The sky is not blue",
    "Water is wet"
]

# Step 1: Extract / classify claims
print("Extracted Claims:", claims_input)
classified_claims = classify_claims(claims_input)
print("Classified Claims:", classified_claims)

# Step 2: Check each claim for contradictions
for claim in classified_claims:
    result = checker.check_contradiction(claim)
    if result["contradiction"]:
        print("⚠️ CONTRADICTION DETECTED")
        print("Against:", result["against"])
        print("Score:", result["score"])
    else:
        print("✅ No high-confidence contradiction")


