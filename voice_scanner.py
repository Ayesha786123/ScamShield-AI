# ============================================================
# ScamShield AI - Voice Scanner
# ============================================================

import os
import subprocess
import tempfile
import imageio_ffmpeg
import whisper


# ============================================================
# FFmpeg
# ============================================================

def get_ffmpeg_path():
    """
    Get the FFmpeg executable bundled with imageio-ffmpeg.
    """
    path = imageio_ffmpeg.get_ffmpeg_exe()

    if not path:
        raise RuntimeError("FFmpeg executable was not found.")

    if not os.path.exists(path):
        raise RuntimeError(f"FFmpeg does not exist at:\n{path}")

    return path


def check_ffmpeg():
    """
    Check whether FFmpeg can actually execute.
    """
    try:
        ffmpeg = get_ffmpeg_path()

        result = subprocess.run(
            [ffmpeg, "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW
            if os.name == "nt"
            else 0
        )

        return result.returncode == 0

    except Exception:
        return False


# ============================================================
# Convert audio to WAV
# ============================================================

def convert_to_wav(input_file, output_file):
    """
    Convert any supported audio file to mono 16 kHz WAV.
    """

    ffmpeg = get_ffmpeg_path()

    command = [
        ffmpeg,
        "-y",
        "-i",
        input_file,
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-sample_fmt",
        "s16",
        output_file
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW
        if os.name == "nt"
        else 0
    )

    if result.returncode != 0:
        raise RuntimeError(
            "FFmpeg conversion failed.\n\n"
            + result.stderr[-3000:]
        )

    if not os.path.exists(output_file):
        raise RuntimeError("WAV file was not created.")

    if os.path.getsize(output_file) == 0:
        raise RuntimeError("Created WAV file is empty.")

    return output_file


# ============================================================
# Whisper transcription
# ============================================================

_model = None


def load_whisper_model():
    """
    Load Whisper only once.
    """

    global _model

    if _model is None:
        print("Loading Whisper model...")
        _model = whisper.load_model("base")
        print("Whisper model loaded.")

    return _model


def transcribe_audio(audio_file):
    """
    Convert audio to WAV first and then transcribe using Whisper.
    """

    if not os.path.exists(audio_file):
        raise FileNotFoundError(
            f"Audio file does not exist:\n{audio_file}"
        )

    # Create temporary folder
    temp_dir = os.path.join(
        os.getcwd(),
        "voice_temp"
    )

    os.makedirs(temp_dir, exist_ok=True)

    wav_file = os.path.join(
        temp_dir,
        "whisper_input.wav"
    )

    # --------------------------------------------------------
    # Convert audio
    # --------------------------------------------------------

    convert_to_wav(
        audio_file,
        wav_file
    )

    # --------------------------------------------------------
    # Load Whisper
    # --------------------------------------------------------

    model = load_whisper_model()

    # --------------------------------------------------------
    # IMPORTANT:
    # Do NOT give Whisper the WAV filename.
    #
    # Give Whisper the NumPy audio array instead.
    #
    # This prevents Whisper from trying to launch FFmpeg
    # again internally.
    # --------------------------------------------------------

    import wave
    import numpy as np

    with wave.open(wav_file, "rb") as wav:

        frames = wav.readframes(
            wav.getnframes()
        )

        sample_width = wav.getsampwidth()
        sample_rate = wav.getframerate()
        channels = wav.getnchannels()

    # Only 16-bit PCM is expected
    if sample_width != 2:
        raise RuntimeError(
            "Unexpected WAV sample format."
        )

    audio = np.frombuffer(
        frames,
        dtype=np.int16
    ).astype(np.float32)

    # Convert integer PCM to -1.0 ... +1.0
    audio = audio / 32768.0

    # Convert stereo -> mono if needed
    if channels > 1:
        audio = audio.reshape(
            -1,
            channels
        ).mean(axis=1)

    # --------------------------------------------------------
    # Whisper
    # --------------------------------------------------------

    result = model.transcribe(
        audio,
        fp16=False,
        language="en"
    )

    text = result.get(
        "text",
        ""
    ).strip()

    return text


# ============================================================
# Scam analysis
# ============================================================

def analyze_scam(text):
    """
    Simple rule-based scam indicator analysis.
    """

    if not text:
        return {
            "risk": "UNKNOWN",
            "score": 0,
            "indicators": [
                "No speech detected."
            ]
        }

    text_lower = text.lower()

    indicators = []

    scam_keywords = {
        "otp": 15,
        "one time password": 20,
        "password": 10,
        "pin": 15,
        "cvv": 20,
        "bank account": 15,
        "credit card": 15,
        "debit card": 15,
        "upi": 15,
        "payment": 10,
        "transfer money": 20,
        "send money": 20,
        "pay now": 20,
        "urgent": 10,
        "immediately": 10,
        "verify your account": 20,
        "account will be blocked": 25,
        "account will be closed": 25,
        "police": 10,
        "arrest": 20,
        "legal action": 20,
        "government": 10,
        "tax": 10,
        "refund": 10,
        "lottery": 20,
        "prize": 15,
        "winner": 15,
        "gift card": 20,
        "remote access": 25,
        "install an app": 15,
        "download this app": 15,
        "screen sharing": 20,
        "do not tell anyone": 20,
        "keep this secret": 20,
        "click the link": 15,
        "send otp": 25
    }

    score = 0

    for keyword, points in scam_keywords.items():

        if keyword in text_lower:

            score += points

            indicators.append(
                f"Suspicious phrase detected: '{keyword}'"
            )

    # --------------------------------------------------------
    # Limit score
    # --------------------------------------------------------

    score = min(score, 100)

    # --------------------------------------------------------
    # Risk level
    # --------------------------------------------------------

    if score >= 60:

        risk = "HIGH"

    elif score >= 30:

        risk = "MEDIUM"

    else:

        risk = "LOW"

    return {
        "risk": risk,
        "score": score,
        "indicators": indicators
    }


# ============================================================
# Combined scanner
# ============================================================

def scan_voice(audio_file):

    text = transcribe_audio(
        audio_file
    )

    analysis = analyze_scam(
        text
    )

    return {
        "text": text,
        "risk": analysis["risk"],
        "score": analysis["score"],
        "indicators": analysis["indicators"]
    }