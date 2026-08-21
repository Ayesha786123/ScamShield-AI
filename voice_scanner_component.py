import os
import tempfile
import subprocess

import streamlit as st
import imageio_ffmpeg
import whisper


# ============================================================
# FFmpeg FIX FOR WHISPER
# ============================================================

def get_ffmpeg_path():

    return imageio_ffmpeg.get_ffmpeg_exe()


def setup_ffmpeg():

    ffmpeg_path = get_ffmpeg_path()

    # Folder containing ffmpeg.exe
    ffmpeg_folder = os.path.dirname(ffmpeg_path)

    # Add FFmpeg folder to Windows PATH
    current_path = os.environ.get("PATH", "")

    if ffmpeg_folder not in current_path:

        os.environ["PATH"] = (
            ffmpeg_folder
            + os.pathsep
            + current_path
        )

    # Also tell common FFmpeg environment variables
    os.environ["FFMPEG_BINARY"] = ffmpeg_path

    return ffmpeg_path


def check_ffmpeg():

    try:

        ffmpeg = setup_ffmpeg()

        result = subprocess.run(
            [
                ffmpeg,
                "-version"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=(
                subprocess.CREATE_NO_WINDOW
                if os.name == "nt"
                else 0
            )
        )

        return result.returncode == 0

    except Exception:

        return False


# ============================================================
# WHISPER MODEL
# ============================================================

@st.cache_resource
def load_whisper_model():

    # IMPORTANT:
    # Setup FFmpeg BEFORE loading/using Whisper

    setup_ffmpeg()

    model = whisper.load_model("base")

    return model


# ============================================================
# SCAM ANALYSIS
# ============================================================

def analyze_voice_text(text):

    text_lower = text.lower()

    indicators = []

    score = 0

    scam_keywords = {

        "otp": 25,
        "one time password": 25,

        "password": 20,

        "pin": 20,

        "cvv": 25,

        "credit card": 15,

        "debit card": 15,

        "bank account": 15,

        "account blocked": 25,

        "account will be blocked": 30,

        "urgent": 10,

        "immediately": 10,

        "send money": 25,

        "transfer money": 25,

        "pay now": 20,

        "payment": 10,

        "verify your account": 20,

        "click the link": 20,

        "link": 10,

        "prize": 20,

        "lottery": 25,

        "winner": 20,

        "refund": 15,

        "police": 15,

        "arrest": 25,

        "legal action": 25,

        "gift card": 25,

        "remote access": 30,

        "screen sharing": 25,

        "download this app": 25

    }

    for keyword, points in scam_keywords.items():

        if keyword in text_lower:

            indicators.append(
                f"Suspicious phrase detected: '{keyword}'"
            )

            score += points

    score = min(score, 100)

    if score >= 70:

        level = "HIGH RISK"

    elif score >= 40:

        level = "MEDIUM RISK"

    else:

        level = "LOW RISK"

    return {
        "score": score,
        "level": level,
        "indicators": indicators
    }


# ============================================================
# VOICE SCANNER
# ============================================================

def show_voice_scanner():

    # Make absolutely sure FFmpeg is configured
    setup_ffmpeg()

    # ========================================================
    # HEADER
    # ========================================================

    st.markdown(
        """
        <div style="
            display:flex;
            align-items:center;
            gap:18px;
            margin-bottom:25px;
        ">

            <div style="
                font-size:48px;
            ">
                🎙️
            </div>

            <div>

                <h1 style="
                    margin:0;
                    padding:0;
                ">
                    Voice Scanner
                </h1>

                <div style="
                    color:#94a3b8;
                    font-size:16px;
                    margin-top:5px;
                ">
                    Analyze suspicious calls and voice
                    conversations for scam indicators.
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # DESCRIPTION
    # ========================================================

    st.markdown(
        """
        <div style="
            padding:22px;
            border-radius:18px;
            background:rgba(30,41,59,0.75);
            border:1px solid rgba(255,255,255,0.08);
            margin-bottom:25px;
        ">

            <h3>
                🛡️ ScamShield Voice Protection
            </h3>

            <p style="color:#cbd5e1;">
                Record a suspicious conversation or upload
                an audio file. ScamShield AI converts speech
                into text using Whisper AI and checks the
                conversation for scam indicators.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # RECORDING
    # ========================================================

    st.subheader("🎙️ Record a Voice Conversation")

    st.write(
        "Press Start Recording, speak normally, "
        "then press Stop Recording."
    )

    try:

        from streamlit_mic_recorder import mic_recorder

        recorded_audio = mic_recorder(
            start_prompt="🎙️ Start Recording",
            stop_prompt="⏹️ Stop Recording",
            just_once=False,
            format="wav",
            key="scamshield_voice_recorder"
        )

    except Exception as e:

        recorded_audio = None

        st.error(
            f"Microphone recorder error: {e}"
        )

    # ========================================================
    # UPLOAD
    # ========================================================

    st.subheader("📁 Or Upload Audio")

    uploaded_audio = st.file_uploader(
        "Choose an audio file",
        type=[
            "wav",
            "mp3",
            "ogg",
            "m4a"
        ],
        key="scamshield_audio_upload"
    )

    # ========================================================
    # AUDIO SELECTION
    # ========================================================

    audio_bytes = None
    audio_name = None

    if recorded_audio:

        audio_bytes = recorded_audio.get("bytes")

        audio_name = "recorded_voice.wav"

        if audio_bytes:

            st.success(
                "Recorded audio captured successfully."
            )

            st.audio(
                audio_bytes,
                format="audio/wav"
            )

    elif uploaded_audio:

        audio_bytes = uploaded_audio.getvalue()

        audio_name = uploaded_audio.name

        st.success(
            f"{uploaded_audio.name} uploaded successfully."
        )

        st.audio(
            audio_bytes,
            format=uploaded_audio.type
        )

    # ========================================================
    # ANALYZE
    # ========================================================

    if audio_bytes:

        st.divider()

        st.subheader("🔎 Voice Analysis")

        # ----------------------------------------------------
        # ANALYZE BUTTON
        # ----------------------------------------------------

        analyze = st.button(
            "🔍 Analyze Voice",
            use_container_width=True,
            type="primary"
        )

        if analyze:

            temp_input = None
            temp_wav = None

            try:

                # ============================================
                # FFmpeg
                # ============================================

                ffmpeg = setup_ffmpeg()

                if not check_ffmpeg():

                    st.error(
                        "❌ FFmpeg is not working."
                    )

                    return

                st.success(
                    "✅ FFmpeg is available."
                )

                # ============================================
                # SAVE ORIGINAL AUDIO
                # ============================================

                extension = os.path.splitext(
                    audio_name
                )[1]

                if not extension:

                    extension = ".wav"

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=extension
                ) as file:

                    file.write(audio_bytes)

                    temp_input = file.name

                # ============================================
                # CREATE WAV FILE
                # ============================================

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".wav"
                ) as file:

                    temp_wav = file.name

                conversion = subprocess.run(
                    [
                        ffmpeg,

                        "-y",

                        "-i",
                        temp_input,

                        "-ar",
                        "16000",

                        "-ac",
                        "1",

                        "-c:a",
                        "pcm_s16le",

                        temp_wav
                    ],

                    stdout=subprocess.PIPE,

                    stderr=subprocess.PIPE,

                    creationflags=(
                        subprocess.CREATE_NO_WINDOW
                        if os.name == "nt"
                        else 0
                    )
                )

                if conversion.returncode != 0:

                    st.error(
                        "❌ Audio conversion failed."
                    )

                    st.code(
                        conversion.stderr.decode(
                            errors="ignore"
                        )
                    )

                    return

                st.success(
                    "✅ Audio processing completed."
                )

                # ============================================
                # VERIFY WAV
                # ============================================

                if not os.path.exists(temp_wav):

                    st.error(
                        "❌ WAV file was not created."
                    )

                    return

                wav_size = os.path.getsize(
                    temp_wav
                )

                if wav_size == 0:

                    st.error(
                        "❌ WAV file is empty."
                    )

                    return

                st.success(
                    f"✅ WAV file ready: "
                    f"{wav_size:,} bytes"
                )

                # ============================================
                # WHISPER
                # ============================================

                st.subheader(
                    "2️⃣ Speech Recognition"
                )

                st.info(
                    "🎧 Loading Whisper AI..."
                )

                # IMPORTANT:
                # Setup PATH again immediately
                # before Whisper transcription

                setup_ffmpeg()

                model = load_whisper_model()

                st.info(
                    "🎙️ Whisper is analyzing the audio..."
                )

                # ============================================
                # TRANSCRIBE
                # ============================================

                result = model.transcribe(
                    temp_wav,

                    fp16=False,

                    language="en"
                )

                text = result.get(
                    "text",
                    ""
                ).strip()

                # ============================================
                # NO SPEECH
                # ============================================

                if not text:

                    st.warning(
                        "⚠️ Whisper could not detect "
                        "clear speech in this audio."
                    )

                    return

                # ============================================
                # SUCCESS
                # ============================================

                st.success(
                    "✅ Speech detected successfully."
                )

                # ============================================
                # TRANSCRIPTION
                # ============================================

                st.subheader(
                    "📝 Transcription"
                )

                st.text_area(
                    "Detected Speech",
                    text,
                    height=180
                )

                # ============================================
                # SCAM DETECTION
                # ============================================

                st.subheader(
                    "3️⃣ Scam Detection"
                )

                analysis = analyze_voice_text(
                    text
                )

                score = analysis["score"]

                level = analysis["level"]

                indicators = analysis["indicators"]

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "🛡️ Scam Score",
                        f"{score}/100"
                    )

                with col2:

                    st.metric(
                        "⚠️ Risk Level",
                        level
                    )

                # ============================================
                # RISK RESULT
                # ============================================

                if score >= 70:

                    st.error(
                        "🚨 HIGH RISK"
                    )

                    st.write(
                        "This conversation contains "
                        "multiple strong scam indicators."
                    )

                elif score >= 40:

                    st.warning(
                        "⚠️ MEDIUM RISK"
                    )

                    st.write(
                        "This conversation contains "
                        "some suspicious indicators."
                    )

                else:

                    st.success(
                        "✅ LOW RISK"
                    )

                    st.write(
                        "No strong scam indicators "
                        "were detected."
                    )

                # ============================================
                # INDICATORS
                # ============================================

                st.subheader(
                    "⚠️ Why is this suspicious?"
                )

                if indicators:

                    for indicator in indicators:

                        st.warning(
                            f"• {indicator}"
                        )

                else:

                    st.success(
                        "No obvious scam indicators detected."
                    )

                # ============================================
                # NEXT STEPS
                # ============================================

                st.subheader(
                    "🛡️ What should you do next?"
                )

                if score >= 70:

                    st.markdown(
                        """
                        **🚨 Immediate action recommended**

                        - 🛑 End the conversation.
                        - 🔐 Do NOT share OTP, PIN, CVV or passwords.
                        - 💳 Do NOT transfer money.
                        - 🔗 Do NOT click links sent by the caller.
                        - 📞 Contact the organization using its official number.
                        - 🚨 Report the suspected scam.
                        """
                    )

                elif score >= 40:

                    st.markdown(
                        """
                        **⚠️ Stay cautious**

                        - 🔎 Verify the caller independently.
                        - 🔐 Don't share financial information.
                        - 🚫 Don't click unknown links.
                        - 💳 Don't make payments until verified.
                        - 📞 Contact the organization directly.
                        """
                    )

                else:

                    st.markdown(
                        """
                        **✅ General safety advice**

                        - 🔐 Never share OTPs or passwords.
                        - 🔎 Verify unexpected requests.
                        - 🚫 Avoid unknown links.
                        - 💳 Don't make unexpected payments.
                        """
                    )

            except Exception as e:

                st.error(
                    "❌ Whisper transcription failed."
                )

                st.code(
                    str(e)
                )

            finally:

                # ============================================
                # CLEAN TEMP FILES
                # ============================================

                try:

                    if (
                        temp_input
                        and os.path.exists(temp_input)
                    ):

                        os.remove(temp_input)

                except Exception:
                    pass

                try:

                    if (
                        temp_wav
                        and os.path.exists(temp_wav)
                    ):

                        os.remove(temp_wav)

                except Exception:
                    pass

    else:

        st.info(
            "🎙️ Record a conversation or upload an "
            "audio file to enable the Analyze Voice button."
        )