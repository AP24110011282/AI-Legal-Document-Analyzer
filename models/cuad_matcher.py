
from utils.cuad_loader import (
    load_cuad_dataset,
    extract_contract_information
)

def match_cuad_clauses(document_text):
    """
    Find CUAD clause categories whose annotated answers
    appear in the uploaded contract.
    This is a basic text-matching baseline, not an AI
    legal interpretation.
    """

    contracts = load_cuad_dataset()
    annotations = extract_contract_information(contracts)

    document_lower = document_text.lower()
    matches = {}

    for item in annotations:
        category = item["question"]
        answers = item["answers"]

        for answer in answers:
            answer = answer.strip()

            if len(answer) < 5:
                continue

            if answer.lower() in document_lower:
                matches.setdefault(category, []).append(answer)

    results = []

    for category, answers in matches.items():
        results.append({
            "category": category,
            "matched_answers": list(set(answers))
        })

    return results
