from fastapi import APIRouter, Body
from pydantic import BaseModel
from app.services.intent import predict_intent
from app.services.ner import extract_entities
from app.services.priority import predict_priority
from app.services.response import generate_response

router = APIRouter()

class TicketRequest(BaseModel):
    text: str

@router.post("/analyze")
def analyze_ticket(request: TicketRequest):
    text = request.text
    intent = predict_intent(text)
    entities = extract_entities(text)
    priority = predict_priority(text)
    response = generate_response(text, intent)

    return {
        "intent": intent,
        "entities": entities,
        "priority": priority,
        "response": response
    }