
from utils.cuad_loader import (
    load_cuad_dataset,
    extract_contract_information,
    get_dataset_statistics
)


print("\n========== CUAD DATASET TEST ==========\n")

contracts = load_cuad_dataset()

print("Dataset loaded successfully!")

print("Total contracts:", len(contracts))

annotations = extract_contract_information(contracts)

print("Total annotations:", len(annotations))

if annotations:
    print("\nSample annotation:")

    print("Contract:", annotations[0]["contract_title"])

    print("Question:", annotations[0]["question"])

    print("Answers:", annotations[0]["answers"][:3])

statistics = get_dataset_statistics()

print("\nTotal categories:", statistics["total_categories"])

print("\nCUAD integration test completed!")
