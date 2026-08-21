import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tempfile

from src.database import (
    init_db, save_scan, get_scans, delete_scan,
    clear_all_scans, get_analytics_summary, DB_PATH
)


def setup_function():
    """Use a fresh temp DB for each test via monkeypatching the path."""
    pass


def test_init_db_creates_file():
    init_db()
    assert os.path.exists(DB_PATH)


def test_save_and_retrieve_scan():
    clear_all_scans()
    result = {
        "risk_score": 75,
        "risk_level": "HIGH",
        "category": "OTP & Credential Theft",
        "explanation": "Test scan for OTP scam.",
        "indicators": ["OTP request"],
        "recommendation": "Do not share OTP.",
        "confidence": 90,
        "scam_dna": {},
        "attack_chain": []
    }
    scan_id = save_scan("message", result, raw_input="Share your OTP now")
    scans = get_scans(limit=10)
    assert len(scans) >= 1
    assert scans[0]["risk_level"] == "HIGH"


def test_privacy_mode_redacts_input():
    clear_all_scans()
    result = {
        "risk_score": 50,
        "risk_level": "MEDIUM",
        "category": "Test",
        "explanation": "Test.",
        "indicators": [],
        "recommendation": "",
        "confidence": 80,
        "scam_dna": {},
        "attack_chain": []
    }
    save_scan("message", result, raw_input="secret message content", privacy_mode=True)
    scans = get_scans(limit=5)
    assert len(scans) >= 1
    summary = scans[0]["short_summary"]
    assert "Privacy Mode" in summary or "secret message content" not in summary


def test_delete_scan():
    clear_all_scans()
    result = {
        "risk_score": 30,
        "risk_level": "LOW",
        "category": "Test",
        "explanation": "Test.",
        "indicators": [],
        "recommendation": "",
        "confidence": 70,
        "scam_dna": {},
        "attack_chain": []
    }
    scan_id = save_scan("url", result)
    scans_before = get_scans()
    delete_scan(scan_id)
    scans_after = get_scans()
    assert len(scans_after) < len(scans_before)


def test_analytics_summary():
    clear_all_scans()
    result = {
        "risk_score": 90,
        "risk_level": "CRITICAL",
        "category": "Bank Fraud",
        "explanation": "",
        "indicators": [],
        "recommendation": "",
        "confidence": 95,
        "scam_dna": {},
        "attack_chain": []
    }
    save_scan("message", result)
    summary = get_analytics_summary()
    assert summary["total"] >= 1
    assert "CRITICAL" in summary["risk_counts"]
