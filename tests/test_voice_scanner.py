import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.voice_scanner import analyze_voice_transcript


def test_empty_transcript_safe():
    r = analyze_voice_transcript("")
    assert "risk_score" in r

def test_otp_transcript_high_risk():
    r = analyze_voice_transcript("Please tell me your OTP and account number immediately to verify your account.")
    assert r["risk_level"] in ["HIGH", "CRITICAL", "MEDIUM"]
    assert r["risk_score"] >= 20

def test_safe_transcript():
    r = analyze_voice_transcript("Hi, this is John. How are you doing today? Let's meet at 5pm.")
    assert r["risk_level"] in ["SAFE", "LOW"]

def test_unified_keys():
    r = analyze_voice_transcript("Hello, this is a test message.")
    required = ["risk_score", "risk_level", "confidence", "category", "indicators"]
    for key in required:
        assert key in r, f"Missing key: {key}"
