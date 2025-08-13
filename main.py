# Set up and run this Streamlit App
# from helper_functions import llm

import os
import time
from enum import Enum

import streamlit as st
from dotenv import load_dotenv
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from openai import OpenAI

from helper_functions import sqlite_fix
from helper_functions.utility import check_password
from zcrew import simple_crew

load_dotenv(".env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


st.set_page_config(layout="centered", page_title="My Streamlit App")
st.title("Singapore Broadband Bot! 🚀")
st.caption("A Streamlit chatbot powered by OpenAI")


if not check_password():
    st.stop()


class Roles(str, Enum):
    AI = "ai"
    HUMAN = "human"


def get_session_history():
    chat_history = ChatMessageHistory()
    for msg in st.session_state.get("messages", []):
        if msg["role"] == Roles.HUMAN:
            chat_history.add_user_message(message=msg["content"])
        else:
            chat_history.add_ai_message(message=msg["content"])

    return chat_history


conversational_rag_chain = RunnableWithMessageHistory(
    simple_crew.rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)


def stream_markdown(msg, placeholder, chunk_size=4, delay=0.03):
    content = ""
    for i in range(0, len(msg), chunk_size):
        content += msg[i : i + chunk_size]
        placeholder.markdown(
            content,
            unsafe_allow_html=True,
        )
        time.sleep(delay)


def render_message(msg):
    """Render a chat message with proper styling and alignment."""
    if msg["role"] == Roles.HUMAN:
        # User messages: bubble on right with gray background
        st.markdown(
            f"""
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
                    {msg["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(msg["content"])


# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": Roles.AI, "content": "Hello! How can I help you today?"}
    ]

# Render chat history
for msg in st.session_state.messages:
    render_message(msg)

# Chat input
if prompt := st.chat_input("Ask anything", max_chars=1000):
    user_msg = {"role": Roles.HUMAN, "content": prompt}
    st.session_state.messages.append(user_msg)
    render_message(user_msg)

    # Placeholder for assistant message
    assistant_placeholder = st.empty()
    assistant_placeholder.markdown(
        """
        <div id="typing-container">
            <img src="https://i.gifer.com/YlWC.gif" width="50" />
        </div>
        """,
        unsafe_allow_html=True,
    )

    # response = client.chat.completions.create(
    #     model="gpt-4.1-mini", messages=st.session_state.messages
    # )

    try:
        response = conversational_rag_chain.invoke({"input": prompt})
        assistant_content = response["answer"]
    except Exception as e:
        assistant_content = f"Error: {e}"

    assistant_msg = {
        "role": Roles.AI,
        "content": assistant_content,
    }
    st.session_state.messages.append(assistant_msg)
    stream_markdown(assistant_msg["content"], assistant_placeholder)
