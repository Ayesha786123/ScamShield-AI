from src.scam_categories import LEGITIMATE

def generate_scam_dna(category, risk_level, indicators, text=""):
    """
    Generates dynamic Scam DNA profiling based on scan content.
    """
    if risk_level == "SAFE" or category == LEGITIMATE:
        return {
            "attack_type": "Legitimate Traffic",
            "target": "General Public",
            "primary_threat": "None Detected",
            "social_engineering": "Benign Information Flow",
            "attack_vector": "Standard Communication Channel"
        }

    text_lower = text.lower() if text else ""

    # Attack Type
    if "otp" in text_lower or "password" in text_lower or "cvv" in text_lower:
        attack_type = "Credential Harvesting"
    elif "pay" in text_lower or "fee" in text_lower or "transfer" in text_lower or "upi" in text_lower:
        attack_type = "Financial Extortion & Advance Fee Fraud"
    elif "blocked" in text_lower or "suspended" in text_lower or "police" in text_lower:
        attack_type = "Coercive Account Deactivation / Legal Threat"
    elif "job" in text_lower or "salary" in text_lower or "work from home" in text_lower:
        attack_type = "Recruitment & Upfront Deposit Scam"
    elif "winner" in text_lower or "lottery" in text_lower or "prize" in text_lower:
        attack_type = "Reward Baited Advance Fee Scam"
    elif "link" in text_lower or "http" in text_lower:
        attack_type = "Malicious Domain Redirect"
    else:
        attack_type = f"{category} Attack"

    # Target Persona
    if "sbi" in text_lower or "bank" in text_lower or "kyc" in text_lower:
        target = "Banking & Digital Wallet Customers"
    elif "parcel" in text_lower or "delivery" in text_lower or "order" in text_lower:
        target = "E-Commerce & Online Shoppers"
    elif "job" in text_lower or "salary" in text_lower:
        target = "Job Seekers & Remote Workers"
    elif "police" in text_lower or "fine" in text_lower:
        target = "Unwary Citizens & Elderly Individuals"
    else:
        target = "Mobile Device & Web Users"

    # Primary Threat
    if "otp" in text_lower or "password" in text_lower:
        primary_threat = "Account Takeover & Identity Theft"
    elif "pay" in text_lower or "fee" in text_lower:
        primary_threat = "Direct Financial Loss"
    elif "http" in text_lower or "link" in text_lower:
        primary_threat = "Credential Theft & Malware Infection"
    else:
        primary_threat = "Unauthorized Access & Financial Fraud"

    # Social Engineering Tactic
    if "urgent" in text_lower or "immediately" in text_lower or "today" in text_lower:
        social_eng = "Manufactured Urgency & Panic Induction"
    elif "congratulations" in text_lower or "won" in text_lower or "reward" in text_lower:
        social_eng = "Greed Baiting & Artificial Excitement"
    elif "police" in text_lower or "arrest" in text_lower or "suspended" in text_lower:
        social_eng = "Authority Coercion & Fear Tactics"
    else:
        social_eng = "Pretexting & Trust Exploitation"

    # Attack Vector
    if "http" in text_lower or "www" in text_lower:
        attack_vector = "Phishing URL / Embedded Hyperlink"
    elif "audio" in text_lower or "voice" in text_lower or "call" in text_lower:
        attack_vector = "Vishing (Voice Phishing Call)"
    elif "qr" in text_lower:
        attack_vector = "Quishing (QR Code Manipulation)"
    elif "screenshot" in text_lower or "image" in text_lower:
        attack_vector = "Image-based Social Engineering / Visual Bait"
    else:
        attack_vector = "SMS / Instant Messaging Gateway"

    return {
        "attack_type": attack_type,
        "target": target,
        "primary_threat": primary_threat,
        "social_engineering": social_eng,
        "attack_vector": attack_vector
    }
