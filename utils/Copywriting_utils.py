from enum import Enum


class Copies(str, Enum):
    GREETINGS = "Hello! Let's talk broadband! How can I help you today?"
    CHAT_INPUT_PLACEHOLDER = "Ask anything"
    TRY_AGAIN = "Sorry, unexpected issue encountered, please try again later!"
