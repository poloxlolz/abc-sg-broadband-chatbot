from enum import Enum


class Copies(str, Enum):
    GREETINGS = "Hello! Let's talk broadband! How can I help you today?"
    CHAT_INPUT_PLACEHOLDER = "Ask anything"
    TRY_AGAIN = "Sorry, unexpected issue encountered, please try again later!"
    DISCLAIMER = """
                <span style="color:#FF82B2">**IMPORTANT NOTICE:**</span>. This web application is a prototype developed for <span style="color:#FF82B2">**educational purposes only.**</span> The information provided here is <span style="color:#FF82B2">**NOT intended for real-world usage**</span> and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

                <span style="color:#FF82B2">**Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.**</span>

                Always consult with qualified professionals for accurate and personalized advice.

                """
