
import re


def clean_text(text):
    """
    Clean document text while preserving paragraph breaks.
    """

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove unnecessary spaces
    text = re.sub(r'[ \t]+', ' ', text)

    # Normalize excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()
