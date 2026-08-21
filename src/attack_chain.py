def generate_attack_chain(category, risk_level, indicators, text=""):
    """
    Generates dynamic step-by-step attack progression chain.
    """
    if risk_level == "SAFE":
        return [
            {"step": 1, "title": "Normal Interaction", "desc": "Message received via standard communication channels."},
            {"step": 2, "title": "Safety Check", "desc": "No threat indicators or coercive language flagged."}
        ]

    text_lower = text.lower() if text else ""
    chain = []
    step_num = 1

    # Step 1: Initial Hook / Pretexting
    if any(b in text_lower for b in ["sbi", "bank", "hdfc", "icici", "paytm", "police", "income tax", "amazon", "delivery"]):
        chain.append({
            "step": step_num,
            "title": "Trusted Entity Impersonation",
            "desc": "Attacker poses as a legitimate bank, government agency, or merchant service."
        })
    elif "won" in text_lower or "lottery" in text_lower or "prize" in text_lower or "reward" in text_lower:
        chain.append({
            "step": step_num,
            "title": "Lure & Prize Baiting",
            "desc": "Attacker promises unexpected rewards, lottery winnings, or lucrative job offers."
        })
    else:
        chain.append({
            "step": step_num,
            "title": "Unsolicited Outreach",
            "desc": "Attacker initiates contact via SMS, email, messaging apps, or call."
        })
    step_num += 1

    # Step 2: Psychological Pressure
    if any(u in text_lower for u in ["urgent", "immediately", "today", "within 24 hours", "blocked", "suspended", "police"]):
        chain.append({
            "step": step_num,
            "title": "Urgency & Threat Coercion",
            "desc": "Attacker induces panic by threatening account blocking, legal fines, or time expiry."
        })
        step_num += 1

    # Step 3: Exploitation Vector
    if re_search := any(link in text_lower for link in ["http", "www", ".com", ".xyz", "link", "bit.ly"]):
        chain.append({
            "step": step_num,
            "title": "Malicious Link Redirection",
            "desc": "Victim is instructed to click a spoofed phishing URL or unverified site."
        })
        step_num += 1

    if any(cred in text_lower for cred in ["otp", "password", "pin", "cvv", "credentials", "verify"]):
        chain.append({
            "step": step_num,
            "title": "Credential & OTP Harvesting",
            "desc": "Attacker prompts victim to enter or share 2FA OTP codes, passwords, or PINs."
        })
        step_num += 1

    if any(pay in text_lower for pay in ["pay", "fee", "transfer", "registration", "deposit", "upi", "card"]):
        chain.append({
            "step": step_num,
            "title": "Fraudulent Payment Trap",
            "desc": "Victim is coerced into making an upfront fee payment or transferring money via UPI/card."
        })
        step_num += 1

    # Final Step: Adversary Impact
    if "otp" in text_lower or "password" in text_lower:
        chain.append({
            "step": step_num,
            "title": "Account Takeover & Compromise",
            "desc": "Unauthorized login, bypass of security factors, and full account compromise."
        })
    else:
        chain.append({
            "step": step_num,
            "title": "Financial / Data Exploitation",
            "desc": "Direct monetary loss, identity theft, or subscription to malicious services."
        })

    return chain
