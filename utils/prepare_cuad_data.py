
import json
from pathlib import Path
from utils.cuad_loader import (
    load_cuad_dataset,
    extract_contract_information
)

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "dataset" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "cuad_training_data.json"

def prepare_data():
    contracts = load_cuad_dataset()
    annotations = extract_contract_information(contracts)

    training_data = []

    for item in annotations:
        if not item["answers"]:
            continue

        training_data.append({
            "contract": item["contract_title"],
            "text": item["context"],
            "question": item["question"],
            "answers": item["answers"]
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(training_data, file, indent=4, ensure_ascii=False)

    print("CUAD preprocessing completed!")
    print("Total training records:", len(training_data))
    print("Saved to:", OUTPUT_FILE)

if __name__ == "__main__":
    prepare_data()
