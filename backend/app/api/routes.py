from fastapi import APIRouter
from pydantic import BaseModel
from app.services.intent import predict_intent
from app.services.ner import extract_entities
from app.services.priority import predict_priority
from app.services.response import generate_response

router = APIRouter()
INTENT_CONFIDENCE_THRESHOLD = 0.70


class TicketRequest(BaseModel):
    text: str


@router.post("/analyze")
def analyze_ticket(request: TicketRequest):
    text = request.text.strip()
    if not text:
        return {
            "intent": "unknown",
            "confidence": None,
            "entities": {},
            "priority": "Low",
            "response": "Please provide a non-empty ticket description."
        }

    # -------- Intent --------
    try:
        intent_result = predict_intent(text)
        if isinstance(intent_result, dict):
            intent = intent_result.get("intent")
            confidence = intent_result.get("confidence")
        else:
            intent = intent_result
            confidence = None
    except Exception:
        intent = "unknown"
        confidence = None
    if confidence is not None:
        confidence = float(confidence)
    needs_review = bool(confidence is None or confidence < INTENT_CONFIDENCE_THRESHOLD)

    # -------- Entities --------
    try:
        entities = extract_entities(text)
    except Exception:
        entities = {}

    # -------- Priority --------
    try:
        priority = predict_priority(text)
    except Exception:
        priority = "Medium"

    # -------- Response --------
    try:
        response = generate_response(text, intent, priority)
    except Exception:
        response = "Sorry, something went wrong while generating a response."

    return {
        "intent": str(intent),
        "confidence": confidence,
        "needs_review": needs_review,
        "entities": entities,
        "priority": priority,
        "response": response
    }