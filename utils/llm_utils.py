from langchain.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters.markdown import MarkdownTextSplitter

import utils.prompt_templates as prompt_templates
from utils.Copywriting_utils import Copies
from utils.crewai_utils import BroadbandCrew


class LLM_Utils:
    def __init__(self, model="gpt-4.1-mini"):
        self.llm = ChatOpenAI(model=model)
        self.embedding = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vectorize_markdown()

    def vectorize_markdown(self):
        results = BroadbandCrew().crew().kickoff()
        document = Document(page_content=results.raw)
        list_of_docs = MarkdownTextSplitter().split_documents(documents=[document])

        self.vectorstore = Chroma.from_documents(
            documents=list_of_docs,
            embedding=self.embedding,
            persist_directory="./broadband_vectorstore",
        )

        # self.vectorstore.persist()

        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

    def conversational_rag_chain(self, prompt: str, chat_history):
        retriever = create_history_aware_retriever(
            llm=self.llm,
            retriever=self.retriever,
            prompt=prompt_templates.get_contextualize_q_prompt(),
        )

        combine_docs_chain = create_stuff_documents_chain(
            llm=self.llm, prompt=prompt_templates.qa_system_prompt()
        )

        rag_chain = create_retrieval_chain(
            retriever=retriever, combine_docs_chain=combine_docs_chain
        )

        conv_rag_chain = RunnableWithMessageHistory(
            runnable=rag_chain,
            get_session_history=chat_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        try:
            response = conv_rag_chain.invoke({"input": prompt})
        except Exception as e:
            return f"Error : {e}"

        return response.get("answer", Copies.TRY_AGAIN.value).replace("$", r"\$")
