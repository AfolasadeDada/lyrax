# core/claim_extractor.py

import re

def extract_claims(text: str):
    """
    Very simple v0.1 claim extractor.
    Splits text into declarative factual-like statements.
    """

    if not text or not isinstance(text, str):
        return []

    # Split by sentence-like boundaries
    sentences = re.split(r'[.!?]\s+', text)

    claims = []
    for s in sentences:
        s = s.strip()
        if len(s) < 10:
            continue

        # Heuristic: factual claims often contain these
        if any(word in s.lower() for word in [
            "is", "are", "was", "were",
            "has", "have", "causes",
            "leads to", "results in",
            "according to", "because"
        ]):
            claims.append(s)

    return claims

