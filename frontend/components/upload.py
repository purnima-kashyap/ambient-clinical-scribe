import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


def show_upload():

    st.subheader("① Upload Consultation Audio")

    uploaded_file = st.file_uploader(
        "",
        type=["wav", "mp3", "m4a"]
    )

    if uploaded_file:

        st.audio(uploaded_file)

        if st.button("🚀 Process Audio", use_container_width=True):

            with st.spinner("Transcribing consultation..."):

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                response = requests.post(
                    f"{API_URL}/transcribe",
                    files=files
                )

            if response.status_code == 200:

                st.success("Audio processed!")

                st.session_state.transcript = response.json()["segments"]

            else:

                st.error(response.text)