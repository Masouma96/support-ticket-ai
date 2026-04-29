import os

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

# global (lazy load)
_generator = None
_generator_error = None


def get_generator():
    global _generator, _generator_error

    if _generator is not None or _generator_error is not None:
        return _generator

    # LLM generation is optional to keep the API stable on low-resource systems.
    if os.getenv("USE_LLM_RESPONSE", "0") != "1":
        return None

    try:
        tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
        model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
        _generator = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
        )
    except Exception as exc:
        _generator_error = exc
        _generator = None

    return _generator


# -----------------------------
# Rule-based fallback
# -----------------------------
def handle_known_issues(text: str):
    text = text.lower()

    if "login" in text or "log in" in text:
        return """I'm sorry you're having trouble logging in.

Please try the following:
1. Check your username and password
2. Reset your password using 'Forgot Password'
3. Clear browser cache or try another browser
4. Ensure your account is not locked

If the issue continues, please contact support."""

    return None


def _build_professional_fallback(text: str, intent: str = "support", priority: str = "Medium"):
    intent_lower = (intent or "support").lower()
    priority_value = priority or "Medium"

    reasons = {
        "billing": "a duplicate charge, an authorization hold, or an outdated payment method",
        "technical": "a temporary service issue, browser/app cache problems, or a recent configuration change",
        "support": "an account access issue, verification mismatch, or temporary authentication delays",
    }
    actions = {
        "billing": [
            "Review your latest invoice and payment history",
            "Confirm the payment method and billing cycle in your account settings",
            "If a duplicate charge appears, share the transaction date and amount for investigation",
        ],
        "technical": [
            "Refresh the page or restart the app and try again",
            "Clear browser/app cache and test in another browser or device",
            "Capture the exact error message and steps to reproduce the issue",
        ],
        "support": [
            "Verify your account email/username and try password reset",
            "Check for verification emails or codes (including spam folder)",
            "Retry after a few minutes in case of temporary authentication delays",
        ],
    }

    reason_text = reasons.get(intent_lower, reasons["support"])
    action_list = actions.get(intent_lower, actions["support"])

    return (
        "Thanks for reporting this issue. I understand this can be frustrating.\n\n"
        f"Based on your request, this may be related to {reason_text}.\n\n"
        "Please try the following steps:\n"
        f"1. {action_list[0]}\n"
        f"2. {action_list[1]}\n"
        f"3. {action_list[2]}\n\n"
        f"Current priority: {priority_value}.\n"
        "If the issue continues, please share any error screenshot or reference number so support can help faster."
    )


def generate_response(text: str, intent: str = "support", priority: str = "Medium"):
    # 1) Rule-based first
    rule_response = handle_known_issues(text)
    if rule_response:
        return rule_response

    # 2) Try LLM only when explicitly enabled via env variable.
    generator = get_generator()
    if generator is None:
        return _build_professional_fallback(text, intent, priority)

    prompt = f"""
You are a professional customer support assistant.

User issue: {text}
Detected intent: {intent}
Priority: {priority}

Write a helpful response that includes:
- possible reasons
- clear steps to fix the issue
- polite tone

Answer:
"""

    try:
        result = generator(prompt, max_length=160, temperature=0.3)
        response = result[0]["generated_text"].strip()
        if response:
            return response
    except Exception:
        pass

    return _build_professional_fallback(text, intent, priority)