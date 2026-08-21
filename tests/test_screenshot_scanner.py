import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.screenshot_scanner import analyze_screenshot


def test_no_tesseract_graceful():
    """Should return a result (not crash) even if Tesseract is unavailable."""
    from PIL import Image
    import io
    img = Image.new("RGB", (100, 100), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    result = analyze_screenshot(buf)
    assert "risk_score" in result
    assert "risk_level" in result

def test_returns_unified_keys():
    from PIL import Image
    import io
    img = Image.new("RGB", (100, 100), color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    result = analyze_screenshot(buf)
    required = ["risk_score", "risk_level", "confidence", "category", "indicators"]
    for key in required:
        assert key in result, f"Missing key: {key}"
