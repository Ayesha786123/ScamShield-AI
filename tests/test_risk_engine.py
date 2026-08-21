import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.risk_engine import get_risk_level, format_unified_result


def test_risk_level_safe():
    assert get_risk_level(0) == "SAFE"
    assert get_risk_level(19) == "SAFE"

def test_risk_level_low():
    assert get_risk_level(20) == "LOW"
    assert get_risk_level(39) == "LOW"

def test_risk_level_medium():
    assert get_risk_level(40) == "MEDIUM"
    assert get_risk_level(59) == "MEDIUM"

def test_risk_level_high():
    assert get_risk_level(60) == "HIGH"
    assert get_risk_level(79) == "HIGH"

def test_risk_level_critical():
    assert get_risk_level(80) == "CRITICAL"
    assert get_risk_level(100) == "CRITICAL"

def test_format_unified_result_structure():
    result = format_unified_result(
        risk_score=75,
        confidence=90,
        category="OTP & Credential Theft",
        indicators=["OTP request detected"],
        raw_text="Share your OTP now"
    )
    required = ["risk_score", "risk_level", "confidence", "category", "indicators", "recommendation", "explanation", "scam_dna", "attack_chain"]
    for key in required:
        assert key in result, f"Missing key: {key}"

def test_score_clamped():
    result = format_unified_result(risk_score=999, confidence=50, category="Test", indicators=[])
    assert result["risk_score"] <= 100

def test_confidence_clamped():
    result = format_unified_result(risk_score=50, confidence=-5, category="Test", indicators=[])
    assert result["confidence"] >= 0
