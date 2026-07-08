import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


def show_soap():

    st.subheader("📋 SOAP Note")

    transcript = st.session_state.get("transcript", [])

    if not transcript:
        st.info("Generate a transcript to view the SOAP note.")
        return

    if st.button(
        "📝 Generate SOAP Note",
        use_container_width=True
    ):

        text = ""

        for t in transcript:
            text += f'{t["speaker"]}: {t["text"]}\n'

        with st.spinner("Generating SOAP Note..."):

            try:
                response = requests.post(
                    f"{API_URL}/generate-soap",
                    json={
                        "transcript": text
                    }
                )

            except requests.exceptions.ConnectionError:
                st.error("Backend server is not running.")
                st.stop()

        if response.status_code == 200:

            st.success("✅ SOAP Note generated successfully.")

            st.session_state.soap = response.json()

        else:

            st.error(response.text)

    soap = st.session_state.get("soap")

    if not soap:
        return

    cards = [
        ("🗣 Subjective", "#E3F2FD", soap.get("Subjective", "Not available")),
        ("🔬 Objective", "#E8F5E9", soap.get("Objective", "Not available")),
        ("🩺 Assessment", "#FFF3E0", soap.get("Assessment", "Not available")),
        ("💊 Plan", "#F3E5F5", soap.get("Plan", "Not available"))
    ]

    col1, col2 = st.columns(2)

    for i, (title, color, content) in enumerate(cards):

        with (col1 if i % 2 == 0 else col2):

            st.markdown(
                f"""
<div style="
background:{color};
padding:18px;
border-radius:16px;
margin-bottom:18px;
border-left:6px solid #2563EB;
box-shadow:0 4px 12px rgba(0,0,0,.08);
min-height:220px;
">

<h4 style="
margin-top:0;
margin-bottom:12px;
color:#1E293B;
">
{title}
</h4>

<p style="
font-size:15px;
line-height:1.7;
color:#334155;
">
{content}
</p>

</div>
                """,
                unsafe_allow_html=True
            )