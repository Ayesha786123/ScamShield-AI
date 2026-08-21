import os
import subprocess
import tempfile
import numpy as np
import wave

from src.utils import detect_ffmpeg, detect_whisper, get_project_root
from src.risk_engine import format_unified_result
from src.scam_categories import (
    BANK_FRAUD, OTP_THEFT, UPI_FRAUD, TECH_SUPPORT, ACCOUNT_TAKEOVER, LEGITIMATE
)

_whisper_model = None

def get_whisper_model():
    global _whisper_model
    has_whisper, _ = detect_whisper()
    if not has_whisper:
        return None
    if _whisper_model is None:
        import whisper
        _whisper_model = whisper.load_model("base")
    return _whisper_model


def convert_audio_to_wav(input_path, output_path):
    has_ffmpeg, ffmpeg_path = detect_ffmpeg()
    if not has_ffmpeg:
        raise RuntimeError("FFmpeg executable not available on this system.")

    command = [
        ffmpeg_path, "-y", "-i", input_path,
        "-vn", "-ac", "1", "-ar", "16000",
        "-sample_fmt", "s16", output_path
    ]
    res = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    )
    if res.returncode != 0 or not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        raise RuntimeError(f"FFmpeg conversion failed: {res.stderr}")
    return output_path


def transcribe_audio_file(audio_path):
    has_whisper, whisper_msg = detect_whisper()
    if not has_whisper:
        raise RuntimeError(f"Whisper STT unavailable: {whisper_msg}")

    model = get_whisper_model()
    if model is None:
        raise RuntimeError("Failed to load Whisper STT model.")

    temp_dir = os.path.join(get_project_root(), "voice_temp")
    os.makedirs(temp_dir, exist_ok=True)
    wav_path = os.path.join(temp_dir, "temp_transcript.wav")

    convert_audio_to_wav(audio_path, wav_path)

    with wave.open(wav_path, "rb") as wav:
        frames = wav.readframes(wav.getnframes())
        sample_width = wav.getsampwidth()
        channels = wav.getnchannels()

    if sample_width != 2:
        raise RuntimeError("Unexpected WAV sample format.")

    audio_arr = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
    if channels > 1:
        audio_arr = audio_arr.reshape(-1, channels).mean(axis=1)

    result = model.transcribe(audio_arr, fp16=False, language="en")
    text = result.get("text", "").strip()

    try:
        if os.path.exists(wav_path):
            os.remove(wav_path)
    except Exception:
        pass

    return text


def analyze_voice_transcript(text):
    if not text or not isinstance(text, str):
        return format_unified_result(
            risk_score=0,
            confidence=100,
            category=LEGITIMATE,
            indicators=["No speech or transcript text provided."],
            raw_text="",
            scanner_type="voice"
        )

    clean_text = text.strip()
    text_lower = clean_text.lower()

    score = 0
    indicators = []
    category = LEGITIMATE

    scam_keywords = {
        "otp": (45, OTP_THEFT, "OTP request detected in voice conversation"),
        "one time password": (45, OTP_THEFT, "One-Time Password requested"),
        "password": (20, OTP_THEFT, "Password disclosure requested"),
        "pin": (20, OTP_THEFT, "PIN requested by caller"),
        "cvv": (25, OTP_THEFT, "Card CVV requested"),
        "bank account": (15, BANK_FRAUD, "Bank account inquiry"),
        "account blocked": (25, ACCOUNT_TAKEOVER, "Threat of account deactivation"),
        "account will be blocked": (30, ACCOUNT_TAKEOVER, "Coercive threat to block account"),
        "urgent": (10, ACCOUNT_TAKEOVER, "High urgency pressure tactics"),
        "immediately": (10, ACCOUNT_TAKEOVER, "Immediate compliance demanded"),
        "send money": (25, UPI_FRAUD, "Direct request to transfer funds"),
        "transfer money": (25, UPI_FRAUD, "Fund transfer request"),
        "pay now": (20, UPI_FRAUD, "Immediate payment demanded"),
        "remote access": (30, TECH_SUPPORT, "Request for remote computer access (AnyDesk/TeamViewer)"),
        "screen sharing": (25, TECH_SUPPORT, "Screen sharing app request"),
        "gift card": (25, UPI_FRAUD, "Gift card payment demand"),
        "police": (20, ACCOUNT_TAKEOVER, "Impersonation of law enforcement"),
        "arrest": (25, ACCOUNT_TAKEOVER, "Threat of arrest or legal action"),
    }

    for kw, (pts, cat, desc) in scam_keywords.items():
        if kw in text_lower:
            score += pts
            indicators.append(desc)
            if category == LEGITIMATE:
                category = cat

    score = min(score, 100)
    unique_indicators = list(dict.fromkeys(indicators))

    return format_unified_result(
        risk_score=score,
        confidence=85 if clean_text else 50,
        category=category,
        indicators=unique_indicators,
        raw_text=clean_text,
        scanner_type="voice",
        extra_data={
            "text": clean_text,
            "raw_input": clean_text
        }
    )


def scan_voice_file(audio_path):
    """
    Scans an audio file: transcribes via Whisper and evaluates risk.
    """
    try:
        transcript = transcribe_audio_file(audio_path)
        return analyze_voice_transcript(transcript)
    except Exception as e:
        return format_unified_result(
            risk_score=0,
            confidence=0,
            category="Audio Error",
            indicators=[f"Voice scanning error: {str(e)}"],
            raw_text="",
            scanner_type="voice",
            extra_data={
                "error": str(e),
                "message": f"Audio processing failed: {str(e)}"
            }
        )
