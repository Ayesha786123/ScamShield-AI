import os
import re
import joblib
from PIL import Image
from urllib.parse import urlparse

from src.utils import get_model_path, get_vectorizer_path, detect_tesseract
from src.risk_engine import format_unified_result
from src.scam_categories import (
    BANK_FRAUD, OTP_THEFT, UPI_FRAUD, JOB_SCAM, LOTTERY_SCAM,
    DELIVERY_SCAM, PHISHING_LINK, ACCOUNT_TAKEOVER, LEGITIMATE
)

# Safe Tesseract Configuration
has_tesseract, tesseract_cmd_path = detect_tesseract()
if has_tesseract:
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path
else:
    pytesseract = None

# Safe Model Loading
MODEL_PATH = get_model_path()
VECTORIZER_PATH = get_vectorizer_path()

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
except Exception:
    model = None
    vectorizer = None


def analyze_screenshot(uploaded_file):
    """
    Analyzes an uploaded screenshot image using OCR and ML + Rule Engine.
    """
    if not has_tesseract or pytesseract is None:
        res = format_unified_result(
            risk_score=0,
            confidence=0,
            category="OCR Unavailable",
            indicators=["Tesseract OCR is not installed on this system."],
            raw_text="",
            scanner_type="screenshot",
            extra_data={
                "success": False,
                "message": "Tesseract OCR engine is not installed or available on this system. Screenshot analysis requires Tesseract OCR.",
                "ocr_status": "Unavailable"
            }
        )
        return res

    try:
        if isinstance(uploaded_file, str):
            image = Image.open(uploaded_file)
        else:
            image = Image.open(uploaded_file)

        extracted_text = pytesseract.image_to_string(image)
        clean_text = extracted_text.strip()

        if not clean_text:
            return format_unified_result(
                risk_score=0,
                confidence=100,
                category=LEGITIMATE,
                indicators=["No readable text found in screenshot."],
                raw_text="",
                scanner_type="screenshot",
                extra_data={
                    "success": True,
                    "text": "",
                    "ocr_status": "No text detected",
                    "urls": []
                }
            )

        # ML Prediction on extracted text
        ml_scam = False
        if model and vectorizer:
            try:
                vec = vectorizer.transform([clean_text])
                pred = model.predict(vec)[0]
                ml_scam = (pred == 1 or str(pred).lower() in ["spam", "scam", "1"])
            except Exception:
                pass

        # Text risk analysis
        text_lower = clean_text.lower()
        score = 0
        indicators = []
        category = LEGITIMATE

        # Keyword checks
        if any(w in text_lower for w in ["otp", "one time password", "share otp", "enter otp"]):
            score += 30
            indicators.append("OTP request detected in screenshot")
            category = OTP_THEFT
        if any(w in text_lower for w in ["password", "pin", "cvv", "card number"]):
            score += 30
            indicators.append("Credential or payment card request detected")
            category = OTP_THEFT
        if any(w in text_lower for w in ["blocked", "suspended", "deactivated", "urgent", "immediately", "kyc"]):
            score += 25
            indicators.append("Account threat or urgency language detected")
            category = ACCOUNT_TAKEOVER
        if any(w in text_lower for w in ["pay now", "send money", "registration fee", "processing fee"]):
            score += 25
            indicators.append("Payment or upfront fee request detected")
            category = UPI_FRAUD
        if any(w in text_lower for w in ["winner", "lottery", "prize", "won"]):
            score += 30
            indicators.append("Lottery or prize scam pattern detected")
            category = LOTTERY_SCAM
        if any(w in text_lower for w in ["parcel", "delivery", "courier"]):
            score += 25
            indicators.append("Parcel delivery notice pattern detected")
            category = DELIVERY_SCAM

        urls = re.findall(r"(https?://\S+|www\.\S+)", clean_text)
        if urls:
            score += 20
            indicators.append(f"URLs found in screenshot ({len(urls)})")
            if category == LEGITIMATE:
                category = PHISHING_LINK

        if ml_scam:
            score = max(score, 70)

        score = min(score, 100)
        unique_indicators = list(dict.fromkeys(indicators))

        result = format_unified_result(
            risk_score=score,
            confidence=85 if clean_text else 50,
            category=category,
            indicators=unique_indicators,
            raw_text=clean_text,
            scanner_type="screenshot",
            extra_data={
                "success": True,
                "text": clean_text,
                "urls": urls,
                "ocr_status": "Success",
                "ml_prediction": "SCAM" if ml_scam else "LEGITIMATE",
                "raw_input": f"[Screenshot Image with {len(clean_text)} extracted characters]"
            }
        )
        return result

    except Exception as e:
        return format_unified_result(
            risk_score=0,
            confidence=0,
            category="Error",
            indicators=[f"Screenshot analysis error: {str(e)}"],
            raw_text="",
            scanner_type="screenshot",
            extra_data={
                "success": False,
                "message": f"Failed to process screenshot: {str(e)}",
                "ocr_status": "Error"
            }
        )