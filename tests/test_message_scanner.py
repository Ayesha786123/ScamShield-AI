import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.predict import predict_message


def test_otp_scam():
    r = predict_message("Share your OTP immediately to prevent your bank account from being blocked.")
    assert r["risk_level"] in ["HIGH", "CRITICAL"], f"Expected HIGH/CRITICAL, got {r['risk_level']}"

def test_lottery_scam():
    r = predict_message("Congratulations! You have won ₹5,00,000 in our lottery. Pay registration fee to claim.")
    assert r["risk_level"] in ["HIGH", "CRITICAL"]

def test_delivery_scam():
    r = predict_message("Your parcel is waiting. Pay the processing fee immediately at https://example.com")
    assert r["risk_level"] in ["HIGH", "CRITICAL"]

def test_job_scam():
    r = predict_message("You have been selected for work from home job. Pay registration fee to receive salary.")
    assert r["risk_level"] in ["HIGH", "CRITICAL"]

def test_safe_message():
    r = predict_message("Your order has been shipped and will arrive tomorrow.")
    assert r["risk_level"] in ["SAFE", "LOW"]

def test_legitimate_salary():
    r = predict_message("Your monthly salary has been credited to your bank account.")
    assert r["risk_level"] in ["SAFE", "LOW", "MEDIUM"]

def test_unified_keys():
    r = predict_message("Test message.")
    required = ["risk_score", "risk_level", "confidence", "category", "indicators", "recommendation", "explanation", "scam_dna", "attack_chain"]
    for key in required:
        assert key in r, f"Missing key: {key}"

def test_risk_score_range():
    r = predict_message("Your account will be blocked. Send OTP now.")
    assert 0 <= r["risk_score"] <= 100
