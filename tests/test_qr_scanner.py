import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.qr_scanner import scan_qr_image
from PIL import Image
import io


def test_no_qr_graceful():
    """Plain white image should return no QR detected gracefully."""
    img = Image.new("RGB", (200, 200), color="white")
    result = scan_qr_image(img)
    assert "risk_score" in result
    assert result.get("qr_detected") == False

def test_unified_keys():
    img = Image.new("RGB", (200, 200), color="white")
    result = scan_qr_image(img)
    required = ["risk_score", "risk_level", "confidence", "category", "indicators"]
    for key in required:
        assert key in result, f"Missing key: {key}"

def test_invalid_image_no_crash():
    """BytesIO with no valid image data should not crash."""
    buf = io.BytesIO(b"this is not an image")
    result = scan_qr_image(buf)
    assert "risk_score" in result

def test_score_range():
    img = Image.new("RGB", (200, 200), color="white")
    result = scan_qr_image(img)
    assert 0 <= result["risk_score"] <= 100
