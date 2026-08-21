import re

BRAND_PATTERNS = {
    "SBI": [r"\bsbi\b", r"state bank of india"],
    "HDFC": [r"\bhdfc\b"],
    "ICICI": [r"\bicici\b"],
    "Axis Bank": [r"\baxis bank\b"],
    "Paytm": [r"\bpaytm\b"],
    "PhonePe": [r"\bphonepe\b"],
    "Google Pay": [r"\bgpay\b", r"google pay"],
    "Amazon": [r"\bamazon\b"],
    "Flipkart": [r"\bflipkart\b"],
    "Netflix": [r"\bnetflix\b"],
    "PayPal": [r"\bpaypal\b"],
    "Income Tax Department": [r"income tax", r"\bitr\b", r"tax refund"],
    "Police / Law Enforcement": [r"\bpolice\b", r"cyber cell", r"cbi", r"trai"]
}


def detect_brand_impersonation(text):
    if not text:
        return []

    text_lower = text.lower()
    detected_brands = []

    for brand, patterns in BRAND_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, text_lower):
                detected_brands.append(brand)
                break

    return detected_brands
