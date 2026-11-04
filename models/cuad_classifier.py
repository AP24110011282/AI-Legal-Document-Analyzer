
import json
import re
from pathlib import Path

import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    BASE_DIR / "dataset" / "processed" / "cuad_training_data.json"
)

MODEL_DIR = BASE_DIR / "models" / "artifacts"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "cuad_classifier.joblib"


def extract_category(question):
    match = re.search(r'related to "([^"]+)"', question)

    if match:
        return match.group(1).strip()

    return None


def train_model():

    print("\nLoading CUAD training data...")

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        records = json.load(file)

    texts = []
    labels = []

    for record in records:

        text = record.get("text", "").strip()
        category = extract_category(record.get("question", ""))

        if text and category:
            texts.append(text[:5000])
            labels.append(category)

    counts = {}

    for label in labels:
        counts[label] = counts.get(label, 0) + 1

    filtered = [
        (text, label)
        for text, label in zip(texts, labels)
        if counts[label] >= 2
    ]

    texts = [item[0] for item in filtered]
    labels = [item[1] for item in filtered]

    print("Total records:", len(texts))
    print("Total categories:", len(set(labels)))

    X_train, X_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.20,
        random_state=42,
        stratify=labels
    )

    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                max_features=5000,
                ngram_range=(1, 1),
                stop_words="english",
                min_df=2,
                dtype="float32"
            )
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=300,
                class_weight="balanced",
                solver="lbfgs"
            )
        )
    ])

    print("\nTraining optimized CUAD model...")
    model.fit(X_train, y_train)

    print("\nTraining completed!")

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("\n========== MODEL EVALUATION ==========")
    print("Accuracy:", round(accuracy * 100, 2), "%")

    print("\nClassification Report:")

    print(classification_report(
        y_test,
        predictions,
        zero_division=0
    ))

    joblib.dump(model, MODEL_PATH)

    print("\nModel saved successfully!")
    print("Location:", MODEL_PATH)


if __name__ == "__main__":
    train_model()
