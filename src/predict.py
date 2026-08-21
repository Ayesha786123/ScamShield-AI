import os
import re
import joblib

from src.utils import get_model_path, get_vectorizer_path
from src.risk_engine import format_unified_result
from src.scam_categories import (
    BANK_FRAUD, OTP_THEFT, UPI_FRAUD, JOB_SCAM, INVESTMENT_SCAM,
    LOTTERY_SCAM, DELIVERY_SCAM, TECH_SUPPORT, PHISHING_LINK,
    ACCOUNT_TAKEOVER, LEGITIMATE
)

# =========================================================
# PATHS & MODEL LOADING
# =========================================================

MODEL_PATH = get_model_path()
VECTORIZER_PATH = get_vectorizer_path()

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
except Exception:
    model = None
    vectorizer = None


# =========================================================
# RULE-BASED RISK ANALYSIS
# =========================================================

def calculate_risk(message):
    message_lower = message.lower()
    risk_score = 0
    indicators = []
    category = LEGITIMATE

    # 1. URGENCY
    urgency_words = [
        "urgent", "immediately", "immediate", "now", "today", "act fast",
        "act now", "hurry", "within 24 hours", "last warning", "final warning",
        "expires", "as soon as possible"
    ]
    if any(w in message_lower for w in urgency_words):
        risk_score += 15
        indicators.append("Urgency or pressure tactics detected")

    # 2. THREAT / ACCOUNT SUSPENSION
    threat_words = [
        "blocked", "block", "suspended", "suspend", "deactivated", "deactivate",
        "account will be closed", "legal action", "police", "arrest", "penalty",
        "fine", "expired", "kyc has expired", "kyc"
    ]
    if any(w in message_lower for w in threat_words):
        risk_score += 20
        indicators.append("Threat or account suspension language detected")
        category = ACCOUNT_TAKEOVER

    # 3. BANKING / FINANCIAL
    financial_words = [
        "bank", "account", "upi", "payment", "refund", "loan", "credit card",
        "debit card", "transaction", "money", "cash", "wallet", "banking details",
        "processing fee", "registration fee"
    ]
    if any(w in message_lower for w in financial_words):
        risk_score += 15
        indicators.append("Financial or banking-related content detected")

    # 4. OTP / CREDENTIALS / VERIFICATION
    credential_words = [
        "otp", "one time password", "password", "pin", "cvv", "verify your account",
        "verify account", "verification", "login", "username", "credentials", "kyc"
    ]
    if any(w in message_lower for w in credential_words):
        risk_score += 20
        indicators.append("Credential or verification request detected")
        if category == LEGITIMATE:
            category = OTP_THEFT

    # 5. URL
    urls = re.findall(r"(https?://\S+|www\.\S+)", message, re.IGNORECASE)
    if urls:
        risk_score += 20
        indicators.append("Link detected in message")

    # 6. SUSPICIOUS URL KEYWORDS
    suspicious_url_words = [
        "verify", "verification", "login", "secure", "update", "account",
        "claim", "reward", "prize", "refund", "kyc", "example.com"
    ]
    for url in urls:
        if any(w in url.lower() for w in suspicious_url_words):
            risk_score += 15
            indicators.append("Suspicious URL keywords detected")
            if category == LEGITIMATE:
                category = PHISHING_LINK
            break

    # 7. PRIZE / REWARD
    reward_words = [
        "winner", "won", "prize", "reward", "lottery", "cash prize",
        "free gift", "congratulations"
    ]
    if any(w in message_lower for w in reward_words):
        risk_score += 25
        indicators.append("Prize or reward scam language detected")
        category = LOTTERY_SCAM

    # 8. PAYMENT REQUEST
    payment_words = [
        "send money", "send payment", "pay now", "make payment", "transfer money",
        "transfer amount", "deposit", "pay immediately", "processing fee",
        "registration fee", "pay the fee"
    ]
    if any(w in message_lower for w in payment_words):
        risk_score += 25
        indicators.append("Suspicious payment or fee request detected")
        if category == LEGITIMATE:
            category = UPI_FRAUD

    # 9. BRAND / AUTHORITY IMPERSONATION
    impersonation_words = [
        "sbi", "hdfc", "icici", "axis bank", "phonepe", "paytm", "google pay",
        "amazon", "flipkart", "income tax", "government", "police"
    ]
    if any(w in message_lower for w in impersonation_words):
        risk_score += 15
        indicators.append("Possible brand or authority impersonation detected")
        if category in [LEGITIMATE, ACCOUNT_TAKEOVER]:
            category = BANK_FRAUD

    # 10. PARCEL / DELIVERY SCAM
    delivery_words = ["parcel", "delivery", "courier", "package", "shipment"]
    if any(w in message_lower for w in delivery_words) and (urls or "fee" in message_lower or "pay" in message_lower):
        risk_score += 25
        indicators.append("Delivery / Parcel scam pattern detected")
        category = DELIVERY_SCAM

    # 11. JOB / WORK FROM HOME SCAM
    job_words = ["work from home", "job", "recruitment", "salary", "selected for a job"]
    if any(w in message_lower for w in job_words) and ("fee" in message_lower or "pay" in message_lower or "registration" in message_lower):
        risk_score += 30
        indicators.append("Work-from-home job / fee request scam pattern detected")
        category = JOB_SCAM

    risk_score = min(risk_score, 100)
    return risk_score, indicators, category


# =========================================================
# MESSAGE PREDICTION ENGINE
# =========================================================

def predict_message(message):
    if not isinstance(message, str):
        message = str(message)
    message = message.strip()

    if not message:
        return format_unified_result(
            risk_score=0,
            confidence=100,
            category=LEGITIMATE,
            indicators=[],
            raw_text="",
            scanner_type="message"
        )

    # ML Prediction
    ml_says_scam = False
    confidence = 85
    if model and vectorizer:
        try:
            text_vec = vectorizer.transform([message])
            pred = model.predict(text_vec)[0]
            pred_text = str(pred).lower()
            ml_says_scam = (pred == 1 or pred_text in ["spam", "scam", "1"])
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(text_vec)[0]
                confidence = int(max(probs) * 100)
        except Exception:
            pass

    # Heuristic Rule Analysis
    risk_score, indicators, category = calculate_risk(message)

    if ml_says_scam:
        risk_score = max(risk_score, 70)

    # Strong scam signals evaluation
    message_lower = message.lower()
    strong_signals = 0

    if any(w in message_lower for w in ["blocked", "suspended", "deactivated", "account will be closed", "expired", "kyc"]):
        strong_signals += 1
    if any(w in message_lower for w in ["urgent", "immediately", "today", "act now", "now", "within 24 hours"]):
        strong_signals += 1
    if any(w in message_lower for w in ["verify", "verification", "otp", "password", "pin", "cvv", "kyc"]):
        strong_signals += 1
    if re.search(r"(https?://|www\.)", message, re.IGNORECASE):
        strong_signals += 1
    if any(w in message_lower for w in ["bank", "account", "upi", "payment", "transaction", "fee", "registration fee"]):
        strong_signals += 1
    if any(w in message_lower for w in ["parcel", "delivery", "work from home", "job", "salary", "lottery", "won"]):
        strong_signals += 1

    if strong_signals >= 3:
        risk_score = max(risk_score, 75)

    if risk_score < 40 and not ml_says_scam:
        category = LEGITIMATE

    result = format_unified_result(
        risk_score=risk_score,
        confidence=confidence,
        category=category,
        indicators=indicators,
        raw_text=message,
        scanner_type="message",
        extra_data={
            "prediction": "SCAM" if risk_score >= 60 else "LEGITIMATE",
            "scam_type": category,
            "raw_input": message
        }
    )

    return result