import streamlit as st

import utils.auth_utils as auth_utils
import utils.sqlite_patch
from utils.streamlit_utils import StreamlitUtils

st.set_page_config(layout="centered", page_title="My Streamlit App")
st.title("Singapore Broadband Bot! 🚀")
st.caption(
    "Stop getting swindled! Find out about Singapore's best broadband deals today!"
)
st.caption("A Streamlit chatbot powered by OpenAI")


def main():
    if not auth_utils.check_password():
        st.stop()

    st_utils = StreamlitUtils()

    st_utils.render_chat_history()
    st_utils.render_question_and_answer()


if __name__ == "__main__":
    main()
