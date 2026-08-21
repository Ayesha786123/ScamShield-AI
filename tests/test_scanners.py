import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.predict import predict_message
from src.url_scanner import analyze_url
from src.voice_scanner import analyze_voice_transcript


REQUIRED_KEYS = [
    "risk_score", "risk_level", "confidence", "category",
    "indicators", "recommendation", "explanation", "scam_dna", "attack_chain"
]


def _check_keys(result, label):
    for key in REQUIRED_KEYS:
        assert key in result, f"[{label}] Missing unified result key: '{key}'"


def test_message_scanner_integration():
    r = predict_message("Your bank account has been suspended. Share OTP immediately.")
    _check_keys(r, "MessageScanner")
    assert r["risk_level"] in ["HIGH", "CRITICAL"]


def test_url_scanner_integration():
    r = analyze_url("http://free-prize-claim.xyz/winner?otp=123")
    _check_keys(r, "URLScanner")
    assert r["risk_score"] > 20


def test_voice_scanner_integration():
    r = analyze_voice_transcript("This is the RBI. Your account will be blocked. Please share your PIN immediately.")
    _check_keys(r, "VoiceScanner")
    assert r["risk_score"] >= 20


def test_safe_message_integration():
    r = predict_message("Your appointment is confirmed for tomorrow at 10 AM.")
    _check_keys(r, "SafeMessage")
    assert r["risk_level"] in ["SAFE", "LOW"]


def test_safe_url_integration():
    r = analyze_url("https://github.com")
    _check_keys(r, "SafeURL")
    assert r["risk_score"] <= 50
