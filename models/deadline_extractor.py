
import re
from datetime import datetime


def extract_deadlines(text):

    deadlines = []

    # Date patterns
    date_pattern = (
        r'\b\d{1,2}\s+'
        r'(?:January|February|March|April|May|June|July|August|September|October|November|December)'
        r'\s+\d{4}\b'
        r'|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
    )

    # Duration patterns
    duration_pattern = (
        r'\b\d+\s+(?:days?|weeks?|months?|years?)\b'
    )

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        lower = line.lower()

        dates = re.findall(
            date_pattern,
            line,
            re.IGNORECASE
        )

        durations = re.findall(
            duration_pattern,
            line,
            re.IGNORECASE
        )

        for date in dates:

            try:
                parsed_date = None

                for fmt in ("%d %B %Y", "%d/%m/%Y",
                            "%d-%m-%Y", "%d/%m/%y",
                            "%d-%m-%y"):

                    try:
                        parsed_date = datetime.strptime(date, fmt)
                        break
                    except ValueError:
                        continue

                deadlines.append({
                    "type": "Date",
                    "value": date,
                    "context": line,
                    "iso_date": (
                        parsed_date.strftime("%Y-%m-%d")
                        if parsed_date else ""
                    )
                })

            except Exception:
                continue

        for duration in durations:

            deadlines.append({
                "type": "Duration",
                "value": duration,
                "context": line,
                "iso_date": ""
            })

    return deadlines
