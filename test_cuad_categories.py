import json
from collections import Counter
from pathlib import Path
import re

DATASET_PATH = Path("dataset/processed/cuad_training_data.json")

with open(DATASET_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

categories = []

for record in data:
    question = record.get("question", "")

    match = re.search(r'related to "([^"]+)"', question)

    if match:
        categories.append(match.group(1))

counts = Counter(categories)

print("\n========== CUAD CATEGORY DISTRIBUTION ==========\n")

print("Total records:", len(data))
print("Total categories:", len(counts))

for category, count in sorted(counts.items()):
    print(f"{category}: {count}")

print("\nCategory distribution test completed!")