
from utils.document_reader import extract_text
from models.summarizer import generate_summary

file_path = "dataset/sample_contracts/sample_agreement.txt"

# Read legal document
document_text = extract_text(file_path)

print("\n========== ORIGINAL DOCUMENT ==========")
print(document_text)

# Generate AI summary
summary = generate_summary(document_text)

print("\n========== AI GENERATED SUMMARY ==========")
print(summary)
