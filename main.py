from core.claim_extractor import extract_claims
from core.claim_classifier import classify_claims
from core.contradiction_checker import ContradictionChecker
from core.db import init_db

# Initialize DB
init_db()

checker = ContradictionChecker(threshold=0.9)

text = """
The sky is blue. The sky is not blue. Water is wet.
"""

claims = extract_claims(text)
classified_claims = classify_claims(claims)

print("Extracted Claims:", claims)
print("Classified Claims:", classified_claims)

for c in classified_claims:
    result = checker.check_contradiction(c)
    print(result)

