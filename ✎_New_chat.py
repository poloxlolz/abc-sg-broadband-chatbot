import streamlit as st

import utils.auth_utils as auth_utils
import utils.sqlite_patch
from utils.copywriting_utils import Copies
from utils.streamlit_utils import StreamlitUtils

st.set_page_config(page_title="SG Broadband Chatbot", page_icon="🛜", layout="centered")

st.title(body=Copies.TITLE.value)
st.caption(body=Copies.CAPTION.value)


with st.expander(label=Copies.DISCLAIMER.name.title()):
    st.markdown(body=Copies.DISCLAIMER.value, unsafe_allow_html=True)


def main():
    if not auth_utils.check_password():
        st.stop()

    st_utils = StreamlitUtils()

    st_utils.render_chat_history()
    st_utils.render_question_and_answer()


if __name__ == "__main__":
    main()
