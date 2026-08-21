import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.url_scanner import analyze_url


def test_phishing_url_high_risk():
    r = analyze_url("http://verify-sbi-account-blocked.xyz/login?otp=123")
    assert r["risk_level"] in ["HIGH", "CRITICAL"], f"Expected HIGH/CRITICAL, got {r['risk_level']}"

def test_google_url_safe():
    r = analyze_url("https://google.com")
    assert r["risk_level"] in ["SAFE", "LOW"], f"Expected SAFE/LOW, got {r['risk_level']}"

def test_ip_url_high_risk():
    r = analyze_url("http://192.168.1.1/login")
    assert r["risk_level"] in ["HIGH", "CRITICAL"]

def test_shortener_url():
    r = analyze_url("https://bit.ly/suspicious123")
    assert r["risk_score"] > 20

def test_unified_keys():
    r = analyze_url("https://example.com")
    required = ["risk_score", "risk_level", "confidence", "category", "indicators", "recommendation", "explanation", "scam_dna", "attack_chain"]
    for key in required:
        assert key in r, f"Missing key: {key}"

def test_empty_url():
    r = analyze_url("")
    assert "risk_score" in r

def test_invalid_url():
    r = analyze_url("not_a_url")
    assert "risk_score" in r

def test_score_range():
    r = analyze_url("https://google.com")
    assert 0 <= r["risk_score"] <= 100
