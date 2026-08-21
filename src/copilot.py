def generate_copilot_recommendations(risk_level, category, indicators):
    """
    Generates actionable safety advice and immediate action items.
    """
    if risk_level == "SAFE":
        return [
            "✅ No immediate action needed. The content appears benign.",
            "🔒 Standard Practice: Always verify sender addresses before sharing personal details.",
            "🛡️ Keep device security and app software updated."
        ]

    advice = []

    if risk_level in ["HIGH", "CRITICAL"]:
        advice.append("🚨 DO NOT click any links, open attachments, or reply to this message.")
        advice.append("🔐 DO NOT share OTPs, PINs, passwords, or banking/card information.")
        advice.append("💳 DO NOT transfer money or pay upfront registration fees.")
        advice.append("🚫 Block the sender's phone number or email address immediately.")
        advice.append("📞 Verify through official banking apps or customer support numbers listed on official websites.")
    elif risk_level == "MEDIUM":
        advice.append("⚠️ Treat this message with elevated caution.")
        advice.append("🔎 Inspect any embedded links carefully for spelling anomalies before clicking.")
        advice.append("🔐 Never share confidential security codes or login credentials.")
        advice.append("📞 Contact the sender independently via trusted official channels.")
    else:
        advice.append("ℹ️ Low risk detected, but exercise standard digital caution.")
        advice.append("🔒 Be cautious of unexpected attachments or requests.")

    return advice
