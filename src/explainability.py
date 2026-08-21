import re

def generate_explanation(risk_score, risk_level, category, indicators):
    """
    Generates human-readable explanation of why ScamShield flagged content.
    """
    if risk_level == "SAFE":
        return "No significant risk signals or suspicious patterns were detected in the analyzed content."

    explanation_parts = [
        f"ScamShield AI evaluated this content with a risk score of {risk_score}/100 ({risk_level} Risk), classified primarily as {category}."
    ]

    if indicators:
        top_indicators = indicators[:4]
        explanation_parts.append("Key triggers identified include: " + "; ".join(top_indicators) + ".")

    if risk_level in ["HIGH", "CRITICAL"]:
        explanation_parts.append("High-severity social engineering tactics or direct credential/financial exploitation vectors were detected.")

    return " ".join(explanation_parts)


def highlight_suspicious_phrases(text, indicators):
    """
    Returns text annotated with HTML span tags highlighting suspicious terms.
    """
    if not text:
        return ""

    keywords = [
        "otp", "one time password", "password", "pin", "cvv",
        "blocked", "suspended", "deactivated", "urgent", "immediately",
        "verify your account", "verify account", "bank account", "refund",
        "cashback", "lottery", "winner", "pay now", "registration fee",
        "gift card", "remote access", "legal action", "arrest"
    ]

    pattern = re.compile(r"\b(" + "|".join([re.escape(k) for k in keywords]) + r")\b", re.IGNORECASE)

    def replace_match(match):
        return f'<mark style="background-color: rgba(239, 68, 68, 0.3); color: #fca5a5; padding: 2px 6px; border-radius: 4px;">{match.group(0)}</mark>'

    return pattern.sub(replace_match, text)
