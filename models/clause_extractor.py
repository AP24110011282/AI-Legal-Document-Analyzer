
import re


def extract_clauses(text):

    results = []

    clause_pattern = re.compile(
        r"^\s*([A-Z][A-Z\s/&-]*CLAUSE)\s*:\s*$",
        re.MULTILINE
    )

    matches = list(clause_pattern.finditer(text))

    # Extract clauses using their headings
    if matches:

        for i, match in enumerate(matches):

            start = match.end()

            end = (
                matches[i + 1].start()
                if i + 1 < len(matches)
                else len(text)
            )

            content = text[start:end].strip()

            results.append({
                "clause": match.group(1).strip().title(),
                "content": content
            })

        return results

    # Fallback for documents without explicit clause headings
    keywords = {
        "Payment Clause": ["payment", "salary", "compensation"],
        "Termination Clause": ["termination", "terminate"],
        "Confidentiality Clause": ["confidentiality", "confidential"],
        "Liability Clause": ["liability", "liable", "damages"],
        "Indemnification Clause": ["indemnification", "indemnify"],
        "Dispute Resolution Clause": ["arbitration", "dispute resolution"]
    }

    for sentence in re.split(r'(?<=[.!?])\s+|\n+', text):

        sentence = sentence.strip()
        lower = sentence.lower()

        for clause, words in keywords.items():

            if any(word in lower for word in words):

                results.append({
                    "clause": clause,
                    "content": sentence
                })

    return results
