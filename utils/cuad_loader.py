
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "dataset" / "CUAD" / "CUADv1.json"


def load_cuad_dataset():

    """
    Load the CUAD legal contract dataset.
    Supports the original CUAD JSON structure.
    """

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"CUAD dataset not found: {DATASET_PATH}"
        )

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    contracts = dataset.get("data", [])

    if not contracts:
        raise ValueError(
            "No contracts found. Check the CUAD JSON format."
        )

    return contracts


def extract_contract_information(contracts):

    """
    Extract contract titles, paragraphs and
    annotated question-answer information.
    """

    results = []

    for contract in contracts:

        contract_title = contract.get("title", "Unknown")

        paragraphs = contract.get("paragraphs", [])

        for paragraph in paragraphs:

            context = paragraph.get("context", "")

            qas = paragraph.get("qas", [])

            for qa in qas:

                answers = qa.get("answers", [])

                answer_texts = [
                    answer.get("text", "")
                    for answer in answers
                ]

                results.append({

                    "contract_title": contract_title,

                    "question": qa.get("question", ""),

                    "clause_category": qa.get("id", ""),

                    "context": context,

                    "answers": answer_texts

                })

    return results


def get_dataset_statistics():

    """
    Generate basic CUAD dataset statistics.
    """

    contracts = load_cuad_dataset()

    annotations = extract_contract_information(contracts)

    categories = set(
        item["question"]
        for item in annotations
    )

    return {

        "total_contracts": len(contracts),

        "total_annotations": len(annotations),

        "total_categories": len(categories),

        "categories": sorted(categories)

    }
