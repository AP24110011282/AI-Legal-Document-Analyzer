
import json
from pathlib import Path

file_path = Path("dataset/processed/cuad_training_data.json")

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

print("\n========== PROCESSED DATA TEST ==========")
print("Total training records:", len(data))

if data:
    print("\nFirst training record:")
    print("Contract:", data[0]["contract"])
    print("Question:", data[0]["question"])
    print("Answers:", data[0]["answers"][:3])
    print("Text preview:", data[0]["text"][:300])

print("\nProcessed dataset verification completed!")
