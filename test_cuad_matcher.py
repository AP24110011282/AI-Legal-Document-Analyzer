
from models.cuad_matcher import match_cuad_clauses

sample_text = """
This Employment Agreement is between ABC Technologies Pvt Ltd
and John Smith.

The employee must keep all company information confidential.

Either party may terminate this agreement by providing
30 days written notice.

The company shall pay a monthly salary of INR 50000.
"""

results = match_cuad_clauses(sample_text)

print("\n========== CUAD CLAUSE MATCHING TEST ==========\n")

if results:
    for result in results:
        print("Category:", result["category"])
        print("Matches:", result["matched_answers"][:5])
        print("-" * 50)
else:
    print("No matching clauses found.")

print("\nCUAD matching test completed!")
