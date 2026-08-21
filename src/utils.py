import os
import shutil
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_project_root():
    return BASE_DIR


def get_model_path(filename="scamshield_model.pkl"):
    return os.path.join(BASE_DIR, "models", filename)


def get_vectorizer_path(filename="tfidf_vectorizer.pkl"):
    return os.path.join(BASE_DIR, "models", filename)


def detect_tesseract():
    """
    Safely detect Tesseract executable without crashing.
    """
    # 1. Check system PATH
    tesseract_in_path = shutil.which("tesseract")
    if tesseract_in_path:
        return True, tesseract_in_path

    # 2. Check standard Windows path
    default_win_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(default_win_path):
        return True, default_win_path

    # 3. Check x86 path
    win_x86_path = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    if os.path.exists(win_x86_path):
        return True, win_x86_path

    return False, "Tesseract OCR executable not found on system."


def detect_ffmpeg():
    """
    Safely detect FFmpeg binary.
    """
    try:
        import imageio_ffmpeg
        path = imageio_ffmpeg.get_ffmpeg_exe()
        if path and os.path.exists(path):
            return True, path
    except Exception:
        pass

    ffmpeg_in_path = shutil.which("ffmpeg")
    if ffmpeg_in_path:
        return True, ffmpeg_in_path

    return False, "FFmpeg executable not found."


def detect_whisper():
    """
    Safely check if whisper is importable.
    """
    try:
        import whisper
        return True, "Whisper library available."
    except ImportError:
        return False, "openai-whisper package not installed."


def sanitize_text(text):
    if not text:
        return ""
    if not isinstance(text, str):
        text = str(text)
    return text.strip()
