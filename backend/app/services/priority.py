def predict_priority(text: str):
    text = text.lower()
    if any(word in text for word in ["crash", "error", "failed", "emergency"]):
        return "High"
    elif "password" in text or "login" in text or "account" in text:
        return "Medium"  
    else:
        return "Low"
