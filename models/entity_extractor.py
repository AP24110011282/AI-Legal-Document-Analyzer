
import spacy
import re

nlp = spacy.load("en_core_web_sm")


def extract_entities(text):

    entities = []
    seen = set()

    # Extract monetary amounts first
    money_pattern = (
        r'\b(?:INR|Rs\.?|₹)\s?[\d,]+(?:\.\d{1,2})?\b'
    )

    money_matches = list(
        re.finditer(money_pattern, text, re.IGNORECASE)
    )

    money_spans = [
        (m.start(), m.end()) for m in money_matches
    ]

    for match in money_matches:

        value = match.group().strip()

        entities.append({
            "text": value,
            "label": "MONEY"
        })

        seen.add(value.lower())

    # Extract contract durations
    duration_pattern = (
        r'\b\d+\s+(?:days?|weeks?|months?|years?)\b'
    )

    duration_matches = list(
        re.finditer(duration_pattern, text, re.IGNORECASE)
    )

    duration_spans = [
        (m.start(), m.end()) for m in duration_matches
    ]

    for match in duration_matches:

        value = match.group().strip()

        entities.append({
            "text": value,
            "label": "DURATION"
        })

        seen.add(value.lower())

    # Extract named entities using spaCy
    doc = nlp(text)

    allowed_labels = {
        "PERSON",
        "ORG",
        "GPE",
        "LOC",
        "DATE"
    }

    for ent in doc.ents:

        value = ent.text.strip()
        label = ent.label_

        if label not in allowed_labels:
            continue

        if value.lower() in {"monthly", "weekly", "daily"}:
            continue

        # Skip entities already extracted as money or duration
        overlaps = any(
            ent.start_char < end and ent.end_char > start
            for start, end in money_spans + duration_spans
        )

        if overlaps:
            continue

        if len(value) < 3:
            continue

        key = value.lower()

        if key not in seen:

            entities.append({
                "text": value,
                "label": label
            })

            seen.add(key)

    return entities
