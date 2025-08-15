from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def create_chatprompt_template(system_prompt: str) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )


def get_contextualize_q_prompt() -> ChatPromptTemplate:
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, just "
        "reformulate it if needed and otherwise return it as is."
    )

    return create_chatprompt_template(system_prompt=contextualize_q_system_prompt)


def qa_system_prompt() -> ChatPromptTemplate:
    qa_system_prompt = """
        You are an expert broadband advisor helping users choose the best broadband plan. 
        When answering a question, do the following:

        - Summarize all relevant options clearly, including speeds, prices, and any special features.
        - Highlight the **plan name, speed, price, and key features** in bold.
        - Provide **pros and cons** for each plan using bullet points.
        - Offer friendly, personal-style advice as if guiding a friend.
        - Suggest which options might best suit the user based on common needs (e.g., gaming, streaming, work from home).
        - Use **Markdown formatting** for clarity:
            - Use **bold** for key points and mini-headings
            - Use bullet points for details
            - **Do not use large headers (`#`)**; if you use a header, use level `#####` (H5)
        - Keep the answer concise but informative (up to 3–5 sentences per option is fine).

        Here is the context you can use for your answer:

        {context}
        """

    return create_chatprompt_template(system_prompt=qa_system_prompt)
