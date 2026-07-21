import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


def show_upload():

    st.subheader("🎤 Consultation Input")

    st.caption(
        "Upload or record a doctor-patient consultation to generate a transcript, SOAP note, and ICD-10 recommendations."
    )

    # Choose input method
    option = st.radio(
        "Choose Consultation Input",
        ["Upload Audio", "Record Audio"],
        horizontal=True
    )

    audio_source = None

    # -------------------------------
    # Upload Audio
    # -------------------------------
    if option == "Upload Audio":

        uploaded_file = st.file_uploader(
            "Choose an audio file",
            type=["wav", "mp3", "m4a"],
            help="Supported formats: WAV, MP3, M4A"
        )

        if uploaded_file:

            st.audio(uploaded_file)

            st.success(f"Selected file: **{uploaded_file.name}**")

            audio_source = (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )

    # -------------------------------
    # Record Audio
    # -------------------------------
    elif option == "Record Audio":

        recorded_audio = st.audio_input("🎙️ Record Consultation")

        if recorded_audio:

            st.audio(recorded_audio)

            st.success("Recording captured successfully.")

            audio_source = (
                "consultation.wav",
                recorded_audio.getvalue(),
                "audio/wav"
            )

    # -------------------------------
    # Generate Report
    # -------------------------------
    if audio_source:

        if st.button(
            "🩺 Generate Clinical Report",
            use_container_width=True
        ):

            with st.spinner("Generating clinical report..."):

                files = {
                    "file": audio_source
                }

                try:
                    response = requests.post(
                        f"{API_URL}/process-consultation",
                        files=files
                    )

                except requests.exceptions.ConnectionError:
                    st.error("❌ Backend server is not running.")
                    st.stop()

            if response.status_code == 200:

                st.success("✅ Clinical report generated successfully.")

                result = response.json()

                # Transcript
                st.session_state.transcript = result["transcript"]["segments"]
                st.session_state.transcript_text = result["transcript"]["text"]
                st.session_state.language = result["transcript"]["language"]

                # SOAP Note
                st.session_state.soap = result["soap_note"]

                # ICD Recommendations
                st.session_state.icd = result["icd_recommendations"]

                # Audio Information
                st.session_state.audio = result["audio"]

            else:

                st.error(response.text)