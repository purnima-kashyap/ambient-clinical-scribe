import streamlit as st


def show_transcript():

    st.subheader("📝 Consultation Transcript")

    transcript = st.session_state.get("transcript", [])

    if not transcript:

        st.info("Upload a consultation recording to view the transcript.")
        return

    container = st.container(height=600)

    with container:

        for segment in transcript:

            speaker = segment.get("speaker", "Unknown")

            if speaker == "Doctor":
                color = "#1565C0"
                emoji = "👨‍⚕️"

            else:
                color = "#2E7D32"
                emoji = "🧑"

            st.markdown(
                f"""
<div style="
    border-left:6px solid {color};
    padding:18px;
    margin-bottom:18px;
    background:#F8FAFC;
    border-radius:16px;
    box-shadow:0 8px 18px rgba(0,0,0,.08);
">

<b style="
    color:{color};
    font-size:17px;
    font-weight:700;
">
    {emoji} {speaker}
</b>

<br><br>

{segment.get("text", "")}

<div style="
    text-align:right;
    color:#64748B;
    font-size:12px;
    margin-top:12px;
">
    ⏱ {segment.get("start", 0):.2f}s
</div>

</div>
                """,
                unsafe_allow_html=True,
            )
