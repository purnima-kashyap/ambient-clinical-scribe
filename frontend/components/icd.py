import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def show_icd():

    st.subheader("④ ICD-10 Recommendation")

    soap = st.session_state.get("soap")

    if not soap:

        return

    assessment = soap.get("Assessment","")

    if st.button("Recommend ICD"):

        response = requests.post(

            f"{API_URL}/recommend-icd",

            json={
                "query":assessment
            }

        )

        if response.status_code==200:

            st.session_state.icd=response.json()["recommendations"]

    icd=st.session_state.get("icd",[])

    for item in icd:

        st.checkbox(

            f'{item["code"]} - {item["description"]}'

        )