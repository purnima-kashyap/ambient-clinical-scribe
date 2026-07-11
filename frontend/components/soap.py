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
            st.session_state["soap"] = response.json()

        else:
            st.error(response.text)

    # Get the SOAP note after generation
    soap = st.session_state.get("soap")

    if not soap:
        return

    st.markdown("## 👨‍⚕️ Human-in-the-Loop Review")
    st.info("Review and edit the SOAP note before finalizing.")

    subjective = st.text_area(
        "🗣 Subjective",
        value=soap.get("subjective", ""),
        height=180
    )

    objective = st.text_area(
        "🔬 Objective",
        value=soap.get("objective", ""),
        height=180
    )

    assessment = st.text_area(
        "🩺 Assessment",
        value=soap.get("assessment", ""),
        height=180
    )

    plan = st.text_area(
        "💊 Plan",
        value=soap.get("plan", ""),
        height=180
    )
    if st.button(
        "✅ Finalize SOAP Note",
        use_container_width=True
        ):

        st.session_state["final_soap"] = {
            "subjective": subjective,
            "objective": objective,
            "assessment": assessment,
            "plan": plan
        }

        st.success("🎉 SOAP Note finalized successfully!")

    if "final_soap" in st.session_state:

        st.divider()

        st.subheader("✅ Doctor Approved SOAP Note")

        st.write("This is the finalized version after doctor's review.")

        st.json(st.session_state["final_soap"])
