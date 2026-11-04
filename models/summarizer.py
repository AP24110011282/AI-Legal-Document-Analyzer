
import re


# ==========================================
# TEXT NORMALIZATION
# ==========================================

def normalize_text(text):

    text = text.replace("\r", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==========================================
# SENTENCE EXTRACTION
# ==========================================

def split_sentences(text):

    text = normalize_text(text)

    # Remove clause headings
    text = re.sub(
        r"\b(PAYMENT|CONFIDENTIALITY|TERMINATION|LIABILITY)"
        r"\s+CLAUSE\s*:",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove standalone document headings
    text = re.sub(
        r"\b(EMPLOYMENT AGREEMENT|SERVICE AGREEMENT|"
        r"NON-DISCLOSURE AGREEMENT|LEASE AGREEMENT)\b",
        "",
        text,
        flags=re.IGNORECASE
    )

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
# KEYWORD MATCHING
# ==========================================

def find_sentences(sentences, keywords):

    matches = []

    for sentence in sentences:

        lower = sentence.lower()

        for keyword in keywords:

            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, lower):

                if sentence not in matches:
                    matches.append(sentence)

                break

    return matches


# ==========================================
# EXTRACT CONTRACT PARTIES
# ==========================================

def extract_parties(sentences):

    parties = []

    for sentence in sentences:

        lower = sentence.lower()

        if " between " in " " + lower + " ":

            match = re.search(
                r"\bbetween\s+(.+?)\s+and\s+(.+?)"
                r"(?=\s+on\s+|\s+dated\s+|[.;]|$)",
                sentence,
                re.IGNORECASE
            )

            if match:

                first_party = match.group(1).strip()
                second_party = match.group(2).strip()

                parties.append(first_party)
                parties.append(second_party)

                return parties

    return parties


# ==========================================
# CONTRACT OVERVIEW
# ==========================================

def extract_overview(text):

    headings = [
        "employment agreement",
        "service agreement",
        "lease agreement",
        "non-disclosure agreement",
        "nda",
        "loan agreement",
        "partnership agreement",
        "consulting agreement",
        "sales agreement"
    ]

    lower = text.lower()

    for heading in headings:

        if heading in lower:
            return heading.title()

    if "agreement" in lower:
        return "Agreement"

    if "contract" in lower:
        return "Contract"

    return "Contract type not identified."


# ==========================================
# GENERATE CONTRACT SUMMARY
# ==========================================

def generate_summary(text):

    if not text or not text.strip():
        return "No document text available."

    normalized_text = normalize_text(text)

    sentences = split_sentences(text)

    if not sentences:
        return "No readable contract information found."

    sections = {

        "Payment Details": [
            "payment",
            "salary",
            "pay",
            "amount",
            "fee",
            "price",
            "compensation"
        ],

        "Confidentiality": [
            "confidential",
            "confidentiality",
            "non-disclosure"
        ],

        "Termination Conditions": [
            "terminate",
            "termination",
            "notice",
            "expire",
            "renewal"
        ],

        "Liability Provisions": [
            "liability",
            "liable",
            "damages",
            "responsible",
            "indemnify"
        ],

        "Governing Law": [
            "governed",
            "governing law",
            "jurisdiction",
            "laws of"
        ]
    }

    output = []

    output.append("CONTRACT SUMMARY")
    output.append("=" * 40)

    # CONTRACT OVERVIEW
    output.append("")
    output.append("Contract Overview:")

    overview = extract_overview(normalized_text)

    output.append("- " + overview)

    # PARTIES INVOLVED
    output.append("")
    output.append("Parties Involved:")

    parties = extract_parties(sentences)

    if parties:

        output.append("- " + parties[0])
        output.append("- " + parties[1])

    else:

        output.append(
            "- Parties could not be identified automatically."
        )

    # OTHER CONTRACT SECTIONS
    for section, keywords in sections.items():

        output.append("")
        output.append(section + ":")

        matches = find_sentences(
            sentences,
            keywords
        )

        if matches:

            for sentence in matches[:3]:

                output.append("- " + sentence)

        else:

            output.append(
                "- Not identified in the document."
            )

    # FOOTER
    output.append("")
    output.append("=" * 40)

    output.append(
        "Note: Automated summary for informational purposes only. "
        "Verify all details against the original contract."
    )

    return "\n".join(output)


# ==========================================
# TEST SUMMARIZER
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

    print("\n========== CONTRACT SUMMARY ==========\n")

    summary = generate_summary(sample)

    print(summary)

    print("\nSummary test completed!")
