import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


def show_icd():

    st.subheader("🏥 ICD-10 Code Recommendation")

    soap = st.session_state.get("soap")

    if not soap:
        st.info("Generate a SOAP note to receive ICD-10 recommendations.")
        return

    assessment = soap.get("Assessment", "")

    if st.button("🔍 Recommend ICD-10 Codes", use_container_width=True):

        with st.spinner("Finding the most relevant ICD-10 codes..."):

            try:
                response = requests.post(
                    f"{API_URL}/recommend-icd",
                    json={
                        "query": assessment
                    }
                )

            except requests.exceptions.ConnectionError:
                st.error("Backend server is not running.")
                st.stop()

        if response.status_code == 200:

            st.success("✅ ICD-10 recommendations generated.")

            st.session_state.icd = response.json()["recommendations"]

        else:

            st.error(response.text)

    icd = st.session_state.get("icd", [])

    if not icd:
        return

    st.markdown("### Recommended ICD-10 Codes")

    for item in icd:

        st.markdown(
            f"""
<div style="
background:#F8F9FA;
padding:14px;
border-radius:12px;
margin-bottom:12px;
border-left:5px solid #1976D2;
box-shadow:0 3px 10px rgba(0,0,0,.08);
">

<b>{item["code"]}</b>

<br>

{item["description"]}

</div>
""",
            unsafe_allow_html=True,
        )