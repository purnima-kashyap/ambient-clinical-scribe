import streamlit as st

def show_transcript():

    st.subheader("② Transcript")

    transcript = st.session_state.get("transcript", [])

    if not transcript:

        st.info("Upload audio to generate transcript.")

        return

    container = st.container(height=520)

    with container:

        for segment in transcript:

            speaker = segment["speaker"]

            if speaker == "Doctor":

                color = "#1565C0"

                emoji = "👨‍⚕️"

            else:

                color = "#2E7D32"

                emoji = "🧑"

            st.markdown(
                f"""
<div style="border-left:5px solid {color};
padding:12px;
margin-bottom:12px;
background:white;
border-radius:10px;
box-shadow:0 1px 5px rgba(0,0,0,.08);">

<b style="color:{color}">
{emoji} {speaker}
</b>

<br><br>

{segment["text"]}

<div style="text-align:right;color:gray;font-size:12px">
{segment["start"]:.2f}s
</div>

</div>
""",
                unsafe_allow_html=True,
            )