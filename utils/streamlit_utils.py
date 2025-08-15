import time
from enum import Enum

import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from utils.Copywriting_utils import Copies
from utils.llm_utils import LLM_Utils


class ChatBubbleStyling(str, Enum):
    HUMAN = """
            <div style="
                display: flex;
                justify-content: flex-end;
                margin-bottom: 35px;
            ">
                <div style="
                    background-color:#F4F4F4;
                    color:black;
                    padding:5px 12px;
                    border-radius:15px;
                    display:inline-block;
                    max-width:60%;
                    text-align:left;
                    word-wrap:break-word;
                    white-space:normal;
                ">
                    {content}
                </div>
            </div>
            """

    SPINNER = """
        <div id="typing-container">
            <img src="https://i.gifer.com/YlWC.gif" width="50" />
        </div>
        """


@st.cache_resource(show_spinner=False)
def get_llm_instance(model="gpt-4.1-mini"):
    return LLM_Utils(model=model)


class StreamlitUtils:
    def __init__(self):
        self.initialise_session_state()
        self.llm = get_llm_instance()

    def initialise_session_state(self):
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = ChatMessageHistory()
            st.session_state.chat_history.add_ai_message(message=Copies.GREETINGS.value)

    @staticmethod
    def render_spinner():
        ai_container = st.empty()
        ai_container.markdown(
            body=ChatBubbleStyling.SPINNER.value, unsafe_allow_html=True
        )

        return ai_container

    @staticmethod
    def write_stream_markdown(
        base_cls: BaseMessage, container, chunk_size=4, delay=0.02
    ):
        stream_content = ""
        for i in range(0, len(base_cls.content), chunk_size):
            stream_content += base_cls.content[i : i + chunk_size]

            container.markdown(
                body=stream_content,
                unsafe_allow_html=True,
            )

            time.sleep(delay)

    def render_content(self, base_cls):
        content = base_cls.content.replace("$", r"\$")

        if isinstance(base_cls, HumanMessage):
            st.markdown(
                body=ChatBubbleStyling.HUMAN.format(content=content),
                unsafe_allow_html=True,
            )
        else:
            st.markdown(body=content, unsafe_allow_html=True)

    def render_chat_history(self):
        for base_cls in st.session_state.chat_history.messages:
            self.render_content(base_cls=base_cls)

    def render_question_and_answer(self):
        if prompt := st.chat_input(
            placeholder=Copies.CHAT_INPUT_PLACEHOLDER.value, max_chars=1000
        ):
            human_msg = HumanMessage(content=prompt)
            # st.session_state.chat_history.add_message(message=human_msg)
            self.render_content(base_cls=human_msg)

            ai_container = self.render_spinner()

            response = self.llm.conversational_rag_chain(
                prompt=prompt, chat_history=lambda: st.session_state.chat_history
            )

            ai_msg = AIMessage(content=response)
            # st.session_state.chat_history.add_message(message=ai_msg)
            self.write_stream_markdown(base_cls=ai_msg, container=ai_container)
