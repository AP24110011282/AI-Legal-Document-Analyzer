# AI Legal Document Analyzer

An AI-assisted web application that analyzes legal documents and identifies important clauses, obligations, risks, entities, and deadlines.

## Features

- Upload PDF, DOCX, and TXT documents.
- Extract text from legal documents.
- Identify important entities.
- Extract legal clauses.
- Identify contractual obligations.
- Generate structured document summaries.
- Detect potential legal risks.
- Extract dates and deadlines.
- Detect clauses using CUAD semantic matching across 41 categories.

## Technologies Used

- Python
- Flask
- HTML and CSS
- Sentence Transformers
- CUAD Dataset
- PyPDF and DOCX processing libraries

## Project Structure

```text
AI-Legal-Document-Analyzer/
├── app.py
├── models/
├── utils/
├── templates/
├── static/
├── uploads/
├── dataset/
├── requirements.txt
└── README.md
```

## How to Run

1. Clone or download this repository.
2. Open the project in VS Code.
3. Create and activate a Python virtual environment.
4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

5. Run the application:

```bash
python app.py
```

6. Open your browser:

```text
http://127.0.0.1:5000/
```

## Disclaimer

This application provides informational analysis only. It does not provide legal advice. All results should be reviewed by a qualified legal professional.

## Dataset

CUAD (Contract Understanding Atticus Dataset) is used as a reference for semantic clause matching.

