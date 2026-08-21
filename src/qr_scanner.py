import cv2
import numpy as np
from PIL import Image

from src.url_scanner import analyze_url
from src.predict import predict_message
from src.risk_engine import format_unified_result
from src.scam_categories import UPI_FRAUD, LEGITIMATE


def scan_qr_image(image_input):
    """
    Real OpenCV QR Code Detector.
    Supports file path, PIL Image, or numpy array.
    """
    try:
        if isinstance(image_input, str):
            img_np = cv2.imread(image_input)
        elif isinstance(image_input, Image.Image):
            img_np = cv2.cvtColor(np.array(image_input), cv2.COLOR_RGB2BGR)
        elif isinstance(image_input, np.ndarray):
            img_np = image_input
        else:
            try:
                pil_img = Image.open(image_input)
                img_np = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            except Exception:
                img_np = None

        if img_np is None:
            return format_unified_result(
                risk_score=0,
                confidence=0,
                category="Invalid Image",
                indicators=["Could not read or decode image file."],
                raw_text="",
                scanner_type="qr",
                extra_data={"qr_detected": False, "raw_input": "[Corrupt / Invalid Image]"}
            )

        detector = cv2.QRCodeDetector()
        payload, bbox, _ = detector.detectAndDecode(img_np)

        if not payload or not payload.strip():
            return format_unified_result(
                risk_score=0,
                confidence=100,
                category=LEGITIMATE,
                indicators=["No QR code detected in image."],
                raw_text="",
                scanner_type="qr",
                extra_data={
                    "qr_detected": False,
                    "payload": "",
                    "payload_type": "None",
                    "raw_input": "[Image without QR code]"
                }
            )

        payload_clean = payload.strip()
        payload_lower = payload_clean.lower()

        # Check payload type
        if payload_lower.startswith("upi://") or "pa=" in payload_lower or "pn=" in payload_lower:
            # UPI Payment QR Code
            score = 50
            indicators = ["UPI payment link embedded in QR code"]
            category = UPI_FRAUD

            if "am=" in payload_lower or "tr=" in payload_lower:
                score += 20
                indicators.append("Pre-filled monetary amount request in UPI QR")

            if any(susp in payload_lower for susp in ["refund", "cashback", "winner", "reward", "verify"]):
                score += 25
                indicators.append("Suspicious promotional/reward term in UPI payload")

            res = format_unified_result(
                risk_score=min(score, 100),
                confidence=95,
                category=category,
                indicators=indicators,
                raw_text=payload_clean,
                scanner_type="qr",
                extra_data={
                    "qr_detected": True,
                    "payload": payload_clean,
                    "payload_type": "UPI Payment Request",
                    "raw_input": payload_clean
                }
            )
            return res

        elif payload_lower.startswith("http://") or payload_lower.startswith("https://") or "www." in payload_lower:
            # URL QR Code -> Pass through URL Scanner
            url_res = analyze_url(payload_clean)
            url_res["qr_detected"] = True
            url_res["payload"] = payload_clean
            url_res["payload_type"] = "URL Redirection"
            url_res["raw_input"] = payload_clean
            return url_res

        else:
            # Plain Text QR Code -> Pass through Message Scanner
            msg_res = predict_message(payload_clean)
            msg_res["qr_detected"] = True
            msg_res["payload"] = payload_clean
            msg_res["payload_type"] = "Plain Text Payload"
            msg_res["raw_input"] = payload_clean
            return msg_res

    except Exception as e:
        return format_unified_result(
            risk_score=0,
            confidence=0,
            category="QR Scan Error",
            indicators=[f"QR analysis failed: {str(e)}"],
            raw_text="",
            scanner_type="qr",
            extra_data={"qr_detected": False, "error": str(e), "raw_input": "[QR Processing Error]"}
        )
