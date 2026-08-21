import os
import tempfile
import streamlit as st

from src.utils import detect_ffmpeg, detect_whisper
from src.voice_scanner import scan_voice_file, analyze_voice_transcript
from pages.result_ui import render_pipeline_animation, render_unified_result_ui

def show_voice_scanner_page():
    st.title("🎙️ Voice Scanner")
    st.write("Record or upload audio of a suspicious call, or analyze call transcripts.")

    has_ffmpeg, ffmpeg_msg = detect_ffmpeg()
    has_whisper, whisper_msg = detect_whisper()

    if not has_ffmpeg or not has_whisper:
        st.info(f"ℹ️ Speech-to-Text Status: {whisper_msg}. FFmpeg: {'Available' if has_ffmpeg else 'Not found'}. Manual call transcript analysis is available below.")

    tab1, tab2, tab3 = st.tabs(["📁 Upload Audio File", "🎙️ Record Microphone", "📝 Analyze Call Transcript"])

    # Tab 1: Upload Audio File
    with tab1:
        uploaded_audio = st.file_uploader(
            "Choose Audio File",
            type=["wav", "mp3", "m4a", "ogg"],
            key="voice_upload"
        )

        if uploaded_audio:
            st.audio(uploaded_audio)
            if st.button("🔍 Transcribe & Analyze Audio", type="primary", use_container_width=True):
                suffix = os.path.splitext(uploaded_audio.name)[1] or ".wav"
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_audio.getvalue())
                    tmp_path = tmp.name

                with st.spinner("Transcribing audio via Whisper STT and scanning speech content..."):
                    render_pipeline_animation()
                    result = scan_voice_file(tmp_path)

                try:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
                except Exception:
                    pass

                text_transcribed = result.get("text", "")
                if text_transcribed:
                    with st.expander("📝 View Speech Transcript"):
                        st.write(text_transcribed)

                render_unified_result_ui(result, scanner_name="Voice", raw_input=f"[Audio File: {uploaded_audio.name}]")

    # Tab 2: Record Microphone
    with tab2:
        st.write("Record a suspicious conversation using your microphone:")
        try:
            from streamlit_mic_recorder import mic_recorder
            rec_audio = mic_recorder(
                start_prompt="🎙️ Start Recording",
                stop_prompt="⏹️ Stop Recording",
                just_once=False,
                format="wav",
                key="voice_page_mic"
            )
            if rec_audio and rec_audio.get("bytes"):
                st.audio(rec_audio["bytes"], format="audio/wav")
                if st.button("🔍 Analyze Recording", type="primary", use_container_width=True):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                        tmp.write(rec_audio["bytes"])
                        tmp_path = tmp.name

                    with st.spinner("Analyzing recorded conversation..."):
                        render_pipeline_animation()
                        result = scan_voice_file(tmp_path)

                    try:
                        if os.path.exists(tmp_path):
                            os.remove(tmp_path)
                    except Exception:
                        pass

                    text_transcribed = result.get("text", "")
                    if text_transcribed:
                        with st.expander("📝 View Speech Transcript"):
                            st.write(text_transcribed)

                    render_unified_result_ui(result, scanner_name="Voice", raw_input="[Microphone Voice Recording]")
        except Exception as e:
            st.warning(f"Microphone recording module notice: {e}")

    # Tab 3: Call Transcript Input (Fallback)
    with tab3:
        transcript_input = st.text_area(
            "Paste Call Transcript Text",
            height=160,
            placeholder="Example: Hello, this is bank security. Your account will be blocked immediately unless you tell me your OTP..."
        )

        if st.button("🔍 Analyze Call Transcript", type="primary", use_container_width=True):
            if not transcript_input.strip():
                st.warning("Please enter a call transcript.")
            else:
                with st.spinner("Analyzing call transcript for scam indicators..."):
                    render_pipeline_animation()
                    result = analyze_voice_transcript(transcript_input)
                    render_unified_result_ui(result, scanner_name="Voice", raw_input=transcript_input)
