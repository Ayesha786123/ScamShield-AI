"""
Standardized taxonomy of scam categories for ScamShield AI V2.
"""

BANK_FRAUD = "Bank Fraud & Impersonation"
OTP_THEFT = "OTP & Credential Theft"
UPI_FRAUD = "UPI & Payment Fraud"
JOB_SCAM = "Fake Job & Recruitment Scam"
INVESTMENT_SCAM = "Investment & Crypto Scam"
LOTTERY_SCAM = "Lottery & Prize Scam"
DELIVERY_SCAM = "Parcel & Delivery Scam"
TECH_SUPPORT = "Tech Support Scam"
PHISHING_LINK = "Phishing & Malicious Link"
ACCOUNT_TAKEOVER = "Account Takeover Threat"
LEGITIMATE = "Legitimate Content"

CATEGORIES = [
    BANK_FRAUD,
    OTP_THEFT,
    UPI_FRAUD,
    JOB_SCAM,
    INVESTMENT_SCAM,
    LOTTERY_SCAM,
    DELIVERY_SCAM,
    TECH_SUPPORT,
    PHISHING_LINK,
    ACCOUNT_TAKEOVER,
    LEGITIMATE,
]

CATEGORY_DESCRIPTIONS = {
    BANK_FRAUD: "Impersonation of financial institutions, fake bank alerts, or KYC expiration traps.",
    OTP_THEFT: "Direct attempts to elicit One-Time Passwords, PINs, or confidential login credentials.",
    UPI_FRAUD: "Unsolicited money requests, fake cashback claims, or suspicious payment gateways.",
    JOB_SCAM: "Work-from-home offers requiring upfront registration fees or security deposits.",
    INVESTMENT_SCAM: "High-return guaranteed crypto/stock schemes demanding immediate deposits.",
    LOTTERY_SCAM: "Unsolicited winnings, lottery prizes, or cash rewards requiring processing fees.",
    DELIVERY_SCAM: "Failed parcel delivery notices pressuring victims into clicking untrusted tracking links.",
    TECH_SUPPORT: "Fake system infection alerts or remote access requests (AnyDesk, TeamViewer).",
    PHISHING_LINK: "Suspicious domains, spoofed URLs, or malicious link shorteners.",
    ACCOUNT_TAKEOVER: "Coercive warnings threatening legal action, police arrest, or immediate account deactivation.",
    LEGITIMATE: "Normal operational message, invoice, or notification with no elevated risk signals."
}
