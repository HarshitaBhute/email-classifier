import re

PII_PATTERNS = {
    "full_name": r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b",
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}",
    "phone_number": r"\b(?:\+91)?[6-9]\d{9}\b",
    "dob": r"\b(?:\d{1,2}[-/th|st|nd|rd\s]*)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[-/\s,]*\d{2,4}\b",
    "aadhar_num": r"\b\d{4}\s\d{4}\s\d{4}\b",
    "credit_debit_no": r"\b(?:\d[ -]*?){13,16}\b",
    "cvv_no": r"\b\d{3}\b",
    "expiry_no": r"\b(0[1-9]|1[0-2])\/?([0-9]{2})\b"
}

def mask_email(text):
    masked_entities = []
    for key, pattern in PII_PATTERNS.items():
        for match in re.finditer(pattern, text):
            start, end = match.span()
            entity_value = match.group()
            masked_entities.append({
                "position": [start, end],
                "classification": key,
                "entity": entity_value
            })
            text = text[:start] + f"[{key}]" + text[end:]
    return text, masked_entities
