import joblib
import os

# Path to ml/models directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(os.path.dirname(BASE_DIR), "ml", "models")

model = None
vectorizer = None

model_path = os.path.join(MODELS_DIR, "intent_model.pkl")
vectorizer_path = os.path.join(MODELS_DIR, "intent_vectorizer.pkl")

if os.path.exists(model_path) and os.path.exists(vectorizer_path):
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)


def _fallback_intent(text: str):
    lowered = text.lower()
    if any(word in lowered for word in ["bill", "payment", "charge", "refund", "subscription"]):
        return "billing"
    if any(word in lowered for word in ["error", "crash", "bug", "slow", "not working"]):
        return "technical"
    if any(word in lowered for word in ["login", "password", "account", "access"]):
        return "support"
    return "support"

def predict_intent(text: str):
    if model is None or vectorizer is None:
        return {"intent": _fallback_intent(text), "confidence": None}

    vec = vectorizer.transform([text])
    prediction = str(model.predict(vec)[0])

    try:
        prob = model.predict_proba(vec)[0]
        confidence = float(round(float(max(prob)), 2))
    except (AttributeError, TypeError):
        confidence = None

    return {
        "intent": prediction,
        "confidence": confidence
    }