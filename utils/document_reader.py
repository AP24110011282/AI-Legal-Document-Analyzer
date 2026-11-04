
import fitz
from docx import Document
from pathlib import Path


def extract_text(file_path):
    """Extract text from PDF, DOCX or TXT documents."""

    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".pdf":
        text = ""

        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text() + "\n"

        return text

    elif extension == ".docx":
        document = Document(file_path)
        return "\n".join(
            paragraph.text for paragraph in document.paragraphs
        )

    elif extension == ".txt":
        return path.read_text(encoding="utf-8")

    else:
        raise ValueError("Unsupported document format")
