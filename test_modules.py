
from utils.document_reader import extract_text
from models.entity_extractor import extract_entities
from models.clause_extractor import extract_clauses
from models.obligation_extractor import extract_obligations

file_path = "dataset/sample_contracts/sample_agreement.txt"

text = extract_text(file_path)

print("\n========== DOCUMENT TEXT ==========")
print(text)

print("\n========== ENTITIES ==========")
print(extract_entities(text))

print("\n========== CLAUSES ==========")
print(extract_clauses(text))

print("\n========== OBLIGATIONS ==========")
print(extract_obligations(text))
