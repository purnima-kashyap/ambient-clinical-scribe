import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def show_soap():

    st.subheader("③ SOAP Note")

    transcript = st.session_state.get("transcript", [])

    if not transcript:
        return

    if st.button("Generate SOAP"):

        text = ""

        for t in transcript:

            text += f'{t["speaker"]}: {t["text"]}\n'

        with st.spinner("Generating SOAP..."):

            response = requests.post(
                f"{API_URL}/generate-soap",
                json={
                    "transcript": text
                }
            )

        if response.status_code == 200:

            st.session_state.soap = response.json()

        else:

            st.error(response.text)

    soap = st.session_state.get("soap")

    if not soap:
        return

    cols = st.columns(2)

    colors = [
        "#E3F2FD",
        "#E8F5E9",
        "#F3E5F5",
        "#FFF8E1"
    ]

    sections = [
        "Subjective",
        "Objective",
        "Assessment",
        "Plan"
    ]

    for i, sec in enumerate(sections):

        with cols[i % 2]:

            st.markdown(
                f"""
<div style="
background:{colors[i]};
padding:15px;
border-radius:12px;
min-height:180px">

<h4>{sec}</h4>

{soap.get(sec,"")}

</div>
""",
                unsafe_allow_html=True,
            )