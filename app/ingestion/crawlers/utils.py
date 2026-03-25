import re

import re

def clean_text(text: str) -> str:
    # ---------------------------
    # 1. Normalize whitespace
    # ---------------------------
    text = re.sub(r"\s+", " ", text)

    # ---------------------------
    # 2. Remove boilerplate lines
    # ---------------------------
    boilerplate_patterns = [
        r"This information was given.*",
        r"This was stated by.*",
        r"In a written reply.*",
        r"This information was provided by.*"
    ]
    for pattern in boilerplate_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    # ---------------------------
    # 4. Normalize bullets / numbering
    # ---------------------------
    text = re.sub(r"\b[i,v,x]+\.\s*", " ", text, flags=re.IGNORECASE)  # i. ii. iii.
    text = re.sub(r"[•·\-]\s*", " ", text)  # bullets

    # ---------------------------
    # 5. Fix punctuation spacing
    # ---------------------------
    text = re.sub(r"\s+([.,;:])", r"\1", text)

    # ---------------------------
    # 6. Remove duplicate spaces again
    # ---------------------------
    text = re.sub(r"\s{2,}", " ", text)

    return text.strip()


def remove_boilerplate(text: str) -> str:
    if "This information was provided by" in text:
        text = text.split("This information was provided by")[0]
    return text