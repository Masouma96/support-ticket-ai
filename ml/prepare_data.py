import pandas as pd
from pathlib import Path

RAW_TO_INTENT = {
    "payment problem": "billing",
    "refund request": "billing",
    "billing issue": "billing",
    "subscription cancellation": "cancellation",
    "account suspension": "support",
    "login issue": "support",
    "security concern": "security",
    "performance issue": "technical",
    "bug report": "technical",
    "feature request": "feature_request",
}


def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    return " ".join(text.strip().lower().split())


def main():
    dataset_dir = Path(__file__).resolve().parent / "dataset"
    input_path = dataset_dir / "customer_support_tickets.csv"
    output_path = dataset_dir / "prepared_tickets.csv"

    df = pd.read_csv(input_path)
    df = df.rename(columns={"issue_description": "text", "category": "label"})

    df["text"] = df["text"].map(normalize_text)
    df["label"] = df["label"].astype(str).str.strip().str.lower().map(RAW_TO_INTENT)
    df = df.dropna(subset=["text", "label"])
    df = df[df["text"] != ""]

    # Some descriptions appear with conflicting labels.
    # Resolve to the strongest label per text, then keep all rows.
    label_counts = (
        df.groupby(["text", "label"]).size().reset_index(name="count")
        .sort_values(["text", "count"], ascending=[True, False])
    )
    text_to_label = dict(
        label_counts.drop_duplicates(subset=["text"], keep="first")[["text", "label"]].values
    )
    df["label"] = df["text"].map(text_to_label)

    prepared = df[["text", "label"]].sample(frac=1, random_state=42).reset_index(drop=True)
    unique_texts = prepared["text"].nunique()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    prepared.to_csv(output_path, index=False)

    print(f"Input rows: {len(df)}")
    print(f"Prepared rows: {len(prepared)}")
    print(f"Unique texts: {unique_texts}")
    print(f"Classes: {prepared['label'].nunique()}")
    print(prepared["label"].value_counts())
    if unique_texts < 100:
        print("\nWARNING: Very low unique text count. Model confidence on real traffic may stay low.")
    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()
