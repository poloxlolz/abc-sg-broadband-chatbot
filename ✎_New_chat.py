import streamlit as st

import utils.auth_utils as auth_utils
import utils.sqlite_patch
from utils.copywriting_utils import Copies
from utils.streamlit_utils import StreamlitUtils

st.set_page_config(
    page_title=Copies.PAGE_TITLE.value, page_icon="🛜", layout="centered"
)

st.title(body=Copies.TITLE.value)
st.caption(body=Copies.CAPTION.value)


with st.sidebar:
    st.write(Copies.MUSIC.value)
    st.audio(
        data="./assets/Pom Pom - Dalkom Sounds.mp3",
        format="audio/mpeg",
        loop=True,
        autoplay=True,
    )

with st.expander(label=f"**{Copies.DISCLAIMER.name.title()}**"):
    st.markdown(body=Copies.DISCLAIMER.value, unsafe_allow_html=True)


def main():
    if not auth_utils.check_password():
        st.stop()

    st_utils = StreamlitUtils()

    st_utils.render_chat_history()
    st_utils.render_question_and_answer()


if __name__ == "__main__":
    main()
