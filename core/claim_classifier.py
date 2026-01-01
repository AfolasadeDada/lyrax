# core/claim_classifier.py

def classify_claims(claims):
    """
    Very simple classifier prototype:
    Labels claims as 'factual' or 'opinion'.
    """
    classified = []
    for claim in claims:
        # Very naive: if contains "I think", mark as opinion, else factual
        if "I think" in claim or "I believe" in claim:
            classified.append(f"{claim} [opinion]")
        else:
            classified.append(f"{claim} [factual]")
    return classified
