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
    qa_system_prompt = """You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \
    Use three sentences maximum and keep the answer concise.\

    {context}"""

    return create_chatprompt_template(system_prompt=qa_system_prompt)
