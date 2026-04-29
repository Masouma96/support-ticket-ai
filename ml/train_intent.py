import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split

print("=" * 50)
print("Starting Fast Intent Model Training (TF-IDF + LogisticRegression)")
print("=" * 50)
sys.stdout.flush()

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "dataset" / "prepared_tickets.csv"
MODEL_PATH = BASE_DIR / "models" / "intent_model.pkl"
VECTORIZER_PATH = BASE_DIR / "models" / "intent_vectorizer.pkl"

print("\n[1/5] Loading dataset...")
df = pd.read_csv(DATASET_PATH)
df = df.dropna(subset=["text", "label"])
df["text"] = df["text"].astype(str).str.strip()
df["label"] = df["label"].astype(str).str.strip()
df = df[df["text"] != ""]

print(f"Total samples: {len(df)}")
print(f"Unique texts: {df['text'].nunique()}")
print("Class distribution:")
print(df["label"].value_counts())
sys.stdout.flush()

print("\n[2/5] Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    df["text"],
    df["label"],
    test_size=0.2,
    random_state=42,
    stratify=df["label"],
)
print(f"Train samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")
sys.stdout.flush()

print("\n[3/5] Vectorizing text...")
vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True,
)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)
sys.stdout.flush()

print("\n[4/5] Training classifier...")
model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced",
    random_state=42,
)
model.fit(X_train_vec, y_train)
sys.stdout.flush()

print("\n[5/5] Evaluating and saving...")
preds = model.predict(X_test_vec)
acc = accuracy_score(y_test, preds)
f1 = f1_score(y_test, preds, average="macro")
print(f"Accuracy: {acc:.2%}")
print(f"F1 Score: {f1:.2%}")
print("\nClassification report:")
print(classification_report(y_test, preds))

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)

print("\nSaved:")
print(f"- Model: {MODEL_PATH}")
print(f"- Vectorizer: {VECTORIZER_PATH}")
print("\nTraining complete.")
sys.stdout.flush()