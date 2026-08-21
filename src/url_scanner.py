import re
import ipaddress
from urllib.parse import urlparse

from src.risk_engine import format_unified_result
from src.scam_categories import (
    PHISHING_LINK, BANK_FRAUD, LEGITIMATE
)

TRUSTED_DOMAINS = {
    "google.com", "youtube.com", "microsoft.com", "apple.com", "amazon.com",
    "amazon.in", "flipkart.com", "paypal.com", "linkedin.com", "github.com",
    "wikipedia.org", "instagram.com", "facebook.com", "whatsapp.com", "openai.com",
}

SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly",
    "shorturl.at", "ow.ly", "rb.gy", "tiny.cc",
}

SUSPICIOUS_TLDS = {
    ".xyz", ".top", ".click", ".buzz", ".monster", ".zip", ".tk",
    ".ml", ".ga", ".cf", ".gq", ".work", ".rest", ".fit", ".live",
}

STRONG_WORDS = [
    "claim-prize", "claimprize", "winner", "lottery", "free-money",
    "free-reward", "verify-account", "verify-account-now", "account-suspended",
    "account-blocked", "confirm-account", "secure-login", "bank-login",
    "otp", "password", "credential", "payment-verification",
    "wallet-verification", "login-verification",
]

MEDIUM_WORDS = [
    "login", "signin", "verify", "verification", "account", "secure",
    "security", "update", "confirm", "claim", "prize", "reward",
    "payment", "wallet", "bank", "bonus", "suspended", "blocked",
    "refund", "cash",
]

BRANDS = [
    "paypal", "amazon", "google", "microsoft", "apple", "facebook",
    "instagram", "netflix", "whatsapp", "flipkart", "sbi", "hdfc",
    "icici", "axisbank",
]


def analyze_url(url):
    if not url or not isinstance(url, str):
        return format_unified_result(
            risk_score=0,
            confidence=100,
            category=LEGITIMATE,
            indicators=[],
            raw_text="",
            scanner_type="url"
        )

    original_url = url.strip()
    if not original_url:
        return format_unified_result(
            risk_score=0,
            confidence=100,
            category=LEGITIMATE,
            indicators=[],
            raw_text="",
            scanner_type="url"
        )

    test_url = original_url if re.match(r"^[a-zA-Z]+://", original_url) else "https://" + original_url

    try:
        parsed = urlparse(test_url)
        hostname = (parsed.hostname or "").lower()
    except Exception:
        return format_unified_result(
            risk_score=100,
            confidence=95,
            category=PHISHING_LINK,
            indicators=["Invalid URL structure"],
            raw_text=original_url,
            scanner_type="url"
        )

    if not hostname:
        return format_unified_result(
            risk_score=100,
            confidence=95,
            category=PHISHING_LINK,
            indicators=["No valid domain found"],
            raw_text=original_url,
            scanner_type="url"
        )

    text = original_url.lower()
    score = 0
    indicators = []
    category = PHISHING_LINK

    # 1. HTTPS
    if parsed.scheme.lower() != "https":
        score += 20
        indicators.append("Website does not use HTTPS")

    # 2. IP ADDRESS
    try:
        ipaddress.ip_address(hostname)
        score += 50
        indicators.append("Website uses an IP address instead of a domain")
    except ValueError:
        pass

    # 3. @ SYMBOL
    if "@" in original_url:
        score += 40
        indicators.append("Suspicious @ symbol found in URL")

    # 4. PUNYCODE
    if "xn--" in hostname:
        score += 35
        indicators.append("Punycode domain detected")

    # 5. URL SHORTENER
    if hostname in SHORTENERS:
        score += 45
        indicators.append("URL shortening service detected")

    # 6. SUSPICIOUS TLD
    if any(hostname.endswith(tld) for tld in SUSPICIOUS_TLDS):
        score += 30
        indicators.append("Potentially suspicious domain extension")

    # 7. STRONG PHISHING WORDS
    found_strong = [w for w in STRONG_WORDS if w in text]
    if found_strong:
        score += min(len(found_strong) * 25, 65)
        indicators.append("Strong phishing keywords: " + ", ".join(found_strong))

    # 8. MEDIUM WORDS
    found_medium = [w for w in MEDIUM_WORDS if w in text and w not in found_strong]
    if found_medium:
        score += min(len(found_medium) * 7, 28)
        indicators.append("Suspicious keywords: " + ", ".join(found_medium))

    # 9. BRAND IMPERSONATION
    for brand in BRANDS:
        if brand in hostname:
            legitimate = any(
                hostname == domain or hostname.endswith("." + domain)
                for domain in TRUSTED_DOMAINS
                if domain.startswith(brand) or domain == brand + ".com"
            )
            if not legitimate:
                score += 35
                indicators.append(f"Possible impersonation of {brand}")
                category = BANK_FRAUD
                break

    # 10. SUBDOMAINS
    parts = hostname.split(".")
    if len(parts) >= 5:
        score += 25
        indicators.append("Unusually large number of subdomains")

    # 11. HYPHENS
    if hostname.count("-") >= 2:
        score += 20
        indicators.append("Domain contains multiple hyphens")

    # 12 & 13. LENGTH
    if len(hostname) > 50:
        score += 20
        indicators.append("Unusually long domain name")
    if len(original_url) > 150:
        score += 20
        indicators.append("Unusually long URL")

    # 14. ENCODED CHARS
    if "%" in original_url:
        score += 15
        indicators.append("Encoded characters found in URL")

    # 15. DOUBLE SLASH
    if "//" in parsed.path:
        score += 20
        indicators.append("Unusual URL path structure")

    # 16. SUSPICIOUS PORT
    try:
        if parsed.port not in (None, 80, 443):
            score += 25
            indicators.append("Unusual network port detected")
    except ValueError:
        score += 40
        indicators.append("Invalid network port")

    # 17. DANGEROUS EXTENSIONS
    dangerous_extensions = [".exe", ".scr", ".apk", ".msi", ".bat", ".cmd", ".ps1", ".zip"]
    if any(parsed.path.lower().endswith(ext) for ext in dangerous_extensions):
        score += 40
        indicators.append("Potentially dangerous downloadable file extension")

    # 18. MULTIPLE DOTS
    if hostname.count(".") >= 4:
        score += 15
        indicators.append("Complex domain structure detected")

    # 19. QUERY PARAMETERS
    suspicious_params = ["password=", "passwd=", "otp=", "cvv=", "card=", "creditcard=", "account=", "login="]
    found_params = [p.rstrip("=") for p in suspicious_params if p in text]
    if found_params:
        score += 30
        indicators.append("Sensitive information requested in URL: " + ", ".join(found_params))

    # 20. RANDOM PATTERN
    if re.search(r"[A-Za-z0-9]{18,}", hostname):
        score += 15
        indicators.append("Domain contains an unusually long random string")

    # TRUSTED DOMAIN CHECK
    is_trusted = any(hostname == domain or hostname.endswith("." + domain) for domain in TRUSTED_DOMAINS)
    if is_trusted and score < 40:
        score = 5
        indicators = ["Domain belongs to trusted domains whitelist"]
        category = LEGITIMATE

    score = min(score, 100)
    unique_indicators = list(dict.fromkeys(indicators))

    result = format_unified_result(
        risk_score=score,
        confidence=90,
        category=category,
        indicators=unique_indicators,
        raw_text=original_url,
        scanner_type="url",
        extra_data={
            "url": original_url,
            "hostname": hostname,
            "is_trusted": is_trusted,
            "raw_input": original_url
        }
    )

    return result