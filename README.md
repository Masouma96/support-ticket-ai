# TicketAI - Support Ticket Analyzer

End-to-end AI project for support ticket analysis with:
- FastAPI backend
- React frontend
- ML pipeline for intent classification
- NER + priority + response generation

This README is written as a full project walkthrough from start to finish.

## 1) Project Goal

Given a ticket text, return:
- `intent` (billing, technical, support, ...)
- `confidence` (model probability)
- `needs_review` (true if confidence is low)
- `entities` (NER extraction)
- `priority` (High/Medium/Low)
- `response` (suggested support response)

## 2) Current Architecture

```
support-ticket-ai/
├── backend/
│   └── app/
│       ├── main.py
│       ├── api/routes.py
│       └── services/
│           ├── intent.py
│           ├── ner.py
│           ├── priority.py
│           └── response.py
├── frontend/
│   └── src/
│       ├── App.js
│       ├── App.css
│       └── index.js
├── ml/
│   ├── prepare_data.py
│   ├── train_intent.py
│   ├── dataset/
│   │   ├── customer_support_tickets.csv
│   │   └── prepared_tickets.csv
│   └── models/
│       ├── intent_model.pkl
│       └── intent_vectorizer.pkl
└── requirements.txt
```

## 3) Environment Setup (Windows)

### Backend

```bat
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r ..\requirements.txt
uvicorn app.main:app --reload
```

Backend docs:
- [http://localhost:8000/docs](http://localhost:8000/docs)

### Frontend

```bat
cd frontend
npm install
npm start
```

Frontend:
- [http://localhost:3000](http://localhost:3000)

## 4) ML Pipeline (Step by Step)

### Step A: Prepare real data

Use:

```bat
cd ml
python prepare_data.py
```

What it does:
- Reads `ml/dataset/customer_support_tickets.csv`
- Renames columns to `text` and `label`
- Normalizes text
- Maps raw categories to unified intent labels
- Resolves noisy conflicting labels
- Saves final output to `ml/dataset/prepared_tickets.csv`

### Step B: Train intent model

Use:

```bat
cd ml
python train_intent.py
```

Current trainer:
- `TF-IDF` vectorizer
- `LogisticRegression` classifier
- Saves:
  - `ml/models/intent_model.pkl`
  - `ml/models/intent_vectorizer.pkl`

Why this approach:
- Fast on CPU
- Stable for small unique-text datasets
- Compatible with backend inference code

### Step C: Run inference through API

`POST /analyze` with:

```json
{
  "text": "I was charged twice for one payment."
}
```

Typical response:

```json
{
  "intent": "billing",
  "confidence": 0.74,
  "needs_review": false,
  "entities": {},
  "priority": "Low",
  "response": "..."
}
```

## 5) Why `needs_review` Exists

`needs_review` is true when:
- confidence is missing, or
- confidence < `0.70`

This avoids over-trusting weak predictions in production.

## 6) Full Development Flow (From Zero to Delivery)

1. Define output contract (`intent`, `confidence`, `entities`, `priority`, `response`).
2. Build baseline backend endpoint.
3. Prepare real dataset from raw tickets.
4. Train baseline intent model and evaluate.
5. Connect model artifacts to backend service.
6. Add fallback logic for missing model/resources.
7. Build frontend for input + output visualization.
8. Add confidence threshold and manual review logic.
9. Validate API and UI with real examples.
10. Iterate on data quality and retraining.

## 7) Common Issues and Fixes

- **500 + `numpy.bool` serialization error**
  - Ensure API response values are Python native types (`bool`, `float`, `str`).

- **`ModuleNotFoundError` for extra ML packages**
  - Install dependencies via root `requirements.txt`.

- **Low confidence (~0.5)**
  - Main root cause is low `Unique texts`, not only model type.

- **Slow transformer training on CPU**
  - Use TF-IDF + Logistic Regression baseline first.

## 8) Important Note About Your Dataset

If `prepared_tickets.csv` has very high rows but very low `Unique texts` (e.g., 10),
model confidence on unseen real text will remain limited.

To improve confidence meaningfully:
- Increase unique ticket phrasing
- Collect more true user-written examples per class
- Reduce contradictory labels for identical texts

## 9) Tech Stack

- FastAPI
- React
- scikit-learn
- transformers
- pandas / numpy

## 10) License

MIT
