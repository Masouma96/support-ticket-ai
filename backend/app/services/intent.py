import joblib
import os

# Path to ml/models directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(os.path.dirname(BASE_DIR), "ml", "models")

model = joblib.load(os.path.join(MODELS_DIR, "intent_model.pkl"))
vectorizer = joblib.load(os.path.join(MODELS_DIR, "intent_vectorizer.pkl"))

def predict_intent(text:str):
    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]
    return prediction