# 🛡️ ScamShield AI V2 — Multimodal Scam Intelligence SaaS

**ScamShield AI** is an advanced, AI-powered cybersecurity platform designed to detect, analyze, and defend against digital scams across text messages, URLs, screenshots, QR codes, and voice calls.

Built with Python, Streamlit, Scikit-Learn, PyTesseract, OpenCV, and OpenAI Whisper, ScamShield AI provides transparent risk engine scoring, dynamic Scam DNA profiling, attack chain progression visuals, and privacy-focused scan history tracking.

---

## ⚡ Key Features

- **💬 Message Scanner**: Hybrid ML model (LinearSVC + TF-IDF) combined with heuristic rule analysis to identify phishing, OTP requests, threats, job scams, and financial extortion.
- **🔗 URL Scanner**: 22-vector heuristic domain analyzer checking HTTPS, IP hosts, url shorteners, suspicious TLDs, punycode, brand spoofing, and dangerous file extensions.
- **🖼️ Screenshot Scanner**: OCR text extraction via PyTesseract combined with computer vision analysis and embedded URL extraction.
- **🎙️ Voice Scanner**: Speech recognition powered by OpenAI Whisper and FFmpeg audio conversion to transcribe and analyze suspicious phone conversations.
- **📱 QR Scanner**: Native OpenCV QR code detector extracting URL and UPI payment payloads.
- **🧠 Unified Risk Engine**: Transparent 0-100 risk scoring with strict risk thresholds (`SAFE`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).
- **🧬 Scam DNA & Attack Chain**: Generates dynamic adversary profiling and step-by-step threat escalation vectors.
- **🔒 Privacy Mode & SQLite Storage**: Scan history stored in SQLite with Privacy Mode option to prevent raw text/media persistence.
- **📊 Security Analytics**: Interactive Plotly dashboard tracking risk distributions, category trends, and scanner usage.

---

## 🛠️ System Requirements & Installation

- **Python**: 3.9+
- **OS**: Windows / Linux / macOS (CPU compatible)
- **Tesseract OCR** (Optional, for screenshot text extraction)
- **FFmpeg** (Included automatically via `imageio-ffmpeg`)

### Setup Instructions

1. **Clone or Navigate to the Workspace**:
   ```bash
   cd ScamShield-AI
   ```

2. **Activate Virtual Environment**:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch Application**:
   ```bash
   streamlit run app.py
   ```

---

## 🧪 Testing

Run the full automated test suite:
```bash
python -m pytest tests/
```

Run the message scanner evaluation test:
```powershell
$env:PYTHONPATH="."
python tests/test_messages.py
```

---

## 📁 Project Architecture

```
ScamShield-AI/
├── app.py                      # Main Streamlit SaaS application shell
├── requirements.txt            # Package dependencies
├── README.md                   # Project documentation
├── models/                     # Pre-trained ML artifacts
├── data/                       # Training datasets
├── src/                        # Core AI & Risk Engine modules
│   ├── risk_engine.py          # Unified transparent risk scoring engine
│   ├── message_scanner.py      # V2 message scanner integration
│   ├── url_scanner.py          # Heuristic URL analyzer
│   ├── screenshot_scanner.py   # OCR & Screenshot analyzer
│   ├── voice_scanner.py        # Whisper STT & Audio analyzer
│   ├── qr_scanner.py           # OpenCV QR Code analyzer
│   ├── database.py             # SQLite persistence & Privacy Mode
│   ├── scam_dna.py             # Dynamic Scam DNA profiler
│   ├── attack_chain.py         # Dynamic attack chain generator
│   └── ...
├── pages/                      # Streamlit UI page components
└── tests/                      # Pytest automated test suites
```

---

© 2026 ScamShield AI • Powered by Team ScamSentries