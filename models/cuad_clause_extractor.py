import json
import re
from pathlib import Path

from utils.cuad_loader import load_cuad_dataset


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    BASE_DIR / "dataset" / "processed" / "cuad_training_data.json"
)


def extract_category(question):
    """
    Extract the CUAD category name from the question.
    """

    match = re.search(r'related to "([^"]+)"', question)

    if match:
        return match.group(1).strip()

    return None


def load_cuad_examples():
    """
    Load CUAD examples containing category, context and answers.
    """

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        records = json.load(file)

    examples = []

    for record in records:

        question = record.get("question", "")
        context = record.get("text", "")
        answers = record.get("answers", [])

        category = extract_category(question)

        if not category:
            continue

        if not context:
            continue

        if not answers:
            continue

        for answer in answers:

            answer = answer.strip()

            if len(answer) < 3:
                continue

            examples.append({
                "category": category,
                "context": context,
                "answer": answer
            })

    return examples


def normalize_text(text):
    """
    Normalize whitespace and lowercase text.
    """

    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def find_clause_in_document(document_text, answer):
    """
    Find an annotated CUAD answer inside a document.
    """

    normalized_document = normalize_text(document_text)
    normalized_answer = normalize_text(answer)

    if normalized_answer in normalized_document:
        return answer

    return None


def extract_cuad_clauses(document_text):
    """
    Match CUAD annotated clause examples against
    an uploaded legal document.

    Returns detected categories and matching text.
    """

    examples = load_cuad_examples()

    results = {}

    normalized_document = normalize_text(document_text)

    for example in examples:

        category = example["category"]
        answer = example["answer"]

        normalized_answer = normalize_text(answer)

        if len(normalized_answer) < 5:
            continue

        if normalized_answer in normalized_document:

            if category not in results:
                results[category] = []

            if answer not in results[category]:
                results[category].append(answer)

    formatted_results = []

    for category, matches in results.items():

        formatted_results.append({
            "category": category,
            "matches": matches[:5]
        })

    return formatted_results


if __name__ == "__main__":

    print("\n========== CUAD CLAUSE EXTRACTOR ==========\n")

    examples = load_cuad_examples()

    print("Total CUAD answer examples:", len(examples))

    print("\nSample examples:")

    for example in examples[:5]:

        print("\nCategory:", example["category"])
        print("Answer:", example["answer"][:200])

    print("\nCUAD clause extractor loaded successfully!")