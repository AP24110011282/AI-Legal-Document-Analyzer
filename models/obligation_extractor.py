
import re


# ==========================================
# OBLIGATION KEYWORDS
# ==========================================

OBLIGATION_WORDS = [
    "shall",
    "must",
    "is required to",
    "are required to",
    "agrees to",
    "undertakes to",
    "will be responsible for",
    "is responsible for",
    "are responsible for",
    "may",
    "will"
]


# ==========================================
# TEXT NORMALIZATION
# ==========================================

def normalize_text(text):

    text = text.replace("\r", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==========================================
# SENTENCE SPLITTING
# ==========================================

def split_sentences(text):

    text = normalize_text(text)

    sentences = re.split(
        r"(?<=[.!?])\s+(?=[A-Z0-9])",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if len(sentence.strip()) > 10
    ]


# ==========================================
# OBLIGATION CLASSIFICATION
# ==========================================

def classify_obligation(sentence):

    lower = sentence.lower()

    if any(word in lower for word in [
        "pay",
        "payment",
        "salary",
        "fee",
        "amount",
        "compensation"
    ]):
        return "Payment Obligation"

    elif any(word in lower for word in [
        "confidential",
        "confidentiality",
        "non-disclosure"
    ]):
        return "Confidentiality Obligation"

    elif any(word in lower for word in [
        "terminate",
        "termination",
        "notice",
        "renewal",
        "expire"
    ]):
        return "Termination / Notice Rights"

    elif any(word in lower for word in [
        "liability",
        "liable",
        "damages",
        "responsible",
        "indemnify"
    ]):
        return "Liability Obligation"

    elif any(word in lower for word in [
        "deliver",
        "provide",
        "perform",
        "maintain",
        "submit"
    ]):
        return "Performance Obligation"

    else:
        return "General Obligation"


# ==========================================
# CHECK OBLIGATION KEYWORDS
# ==========================================

def is_obligation(sentence):

    lower = sentence.lower()

    for keyword in OBLIGATION_WORDS:

        pattern = r"\b" + re.escape(keyword) + r"\b"

        if re.search(pattern, lower):
            return True

    return False


# ==========================================
# EXTRACT OBLIGATIONS
# ==========================================

def extract_obligations(text):

    if not text or not text.strip():
        return []

    sentences = split_sentences(text)

    obligations = []

    seen = set()

    for sentence in sentences:

        if is_obligation(sentence):

            normalized_sentence = sentence.lower()

            if normalized_sentence not in seen:

                seen.add(normalized_sentence)

                obligations.append({
                    "category": classify_obligation(sentence),
                    "text": sentence
                })

    return obligations


# ==========================================
# TEST OBLIGATION EXTRACTOR
# ==========================================

if __name__ == "__main__":

    sample = """
    EMPLOYMENT AGREEMENT

    This agreement is made between ABC Technologies Pvt Ltd
    and John Smith on 1 January 2026.

    PAYMENT CLAUSE:
    The company shall pay the employee a monthly salary
    of INR 50000.

    CONFIDENTIALITY CLAUSE:
    The employee must keep all company information confidential.

    TERMINATION CLAUSE:
    Either party may terminate this agreement by providing
    30 days written notice.

    LIABILITY CLAUSE:
    The employee shall be responsible for damages caused
    by intentional misconduct.
    """

    print("\n========== OBLIGATION EXTRACTION ==========\n")

    results = extract_obligations(sample)

    if results:

        for index, obligation in enumerate(results, start=1):

            print(f"Obligation {index}")
            print("Category:", obligation["category"])
            print("Text:", obligation["text"])
            print("-" * 50)

    else:

        print("No obligations identified.")

    print("\nObligation extraction test completed!")
