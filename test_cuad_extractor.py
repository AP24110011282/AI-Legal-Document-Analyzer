from models.cuad_clause_extractor import extract_cuad_clauses


sample_contract = """
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


print("\n========== CUAD EXTRACTION TEST ==========\n")

results = extract_cuad_clauses(sample_contract)

if results:

    for result in results:

        print("Category:", result["category"])

        print("Matches:")

        for match in result["matches"]:
            print(" -", match)

        print("-" * 60)

else:

    print("No CUAD clauses matched.")


print("\nCUAD extraction test completed!")