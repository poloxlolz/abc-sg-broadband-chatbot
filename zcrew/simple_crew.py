from concurrent.futures import ThreadPoolExecutor, as_completed
from enum import Enum

import requests
import tiktoken
from bs4 import BeautifulSoup
from crewai import Agent, Crew, Task
from crewai_tools import ScrapeWebsiteTool
from langchain import hub
from langchain.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# def count_tokens(text):
#     encoding = tiktoken.encoding_for_model("gpt-4.1-mini")
#     return len(encoding.encode(text))


# class BroadbandURLs(Enum):
#     STARHUB = "https://www.starhub.com/personal/broadband.html"
#     MYREPUBLIC = "https://myrepublic.net/sg/broadband/"

#     SINGTEL = "https://www.singtel.com/personal/products-services/broadband/fibre-broadband-plans"
#     WHIZCOMMS = "https://whizcomms.com.sg/promo/"

#     # SIMBA = "https://www.simba.sg/broadband"
#     # M1 = "https://www.m1.com.sg/home-broadband"

#     VIEWQUEST = "https://viewqwest.com/sg/residential/broadband/"


# class ThirdParty(Enum):
#     HARDWAREZONE = "https://forums.hardwarezone.com.sg/threads/official-readme-first-2025-sg-isp-comparison-latest-promo-deals.6665380/"


# tool = ScrapeWebsiteTool(website_url=ThirdParty.HARDWAREZONE.value)

# agent = Agent(
#     role="BroadbandScraper",
#     goal=f"Scrape all broadband-related information from {ThirdParty.HARDWAREZONE.value} and output as markdown.",
#     backstory=(
#         "You are an expert web scraper and content extractor. "
#         "Focus only on broadband-related content such as plans, pricing, promotions, speeds, and availability. "
#         "Ignore unrelated content such as forums, ads, or hardware discussions."
#     ),
#     tools=[tool],
#     verbose=True,
# )

# task = Task(
#     description=f"Scrape broadband-related content from {ThirdParty.HARDWAREZONE.value} and return markdown",
#     expected_output="Markdown containing broadband information only",
#     agent=agent,
#     async_execution=True,
# )

# crew = Crew(
#     agents=[agent],
#     tasks=[task],
#     verbose=True,
# )

# results = crew.kickoff()


# doc = Document(
#     page_content=results.raw, metadata={"source": ThirdParty.HARDWAREZONE.value}
# )

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1000,
#     chunk_overlap=100,
#     separators=["\n## ", "\n# ", "\n", " "],  # hierarchical splitting
# )

# chunked_docs = splitter.split_documents([doc])

llm = ChatOpenAI(model="gpt-4.1-mini")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectordb = Chroma(
    persist_directory="./broadband_vectorstore", embedding_function=embeddings
)
retriever = vectordb.as_retriever(search_kwargs={"k": 3})

prompt = hub.pull("rlm/rag-prompt")
# vectordb = Chroma.from_documents(
#     documents=chunked_docs,
#     embedding=embeddings,
#     persist_directory="./broadband_vectorstore",
# )

# vectordb.persist()


rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, just "
    "reformulate it if needed and otherwise return it as is."
)
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)


qa_system_prompt = """You are an assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question. \
If you don't know the answer, just say that you don't know. \
Use three sentences maximum and keep the answer concise.\

{context}"""
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


# print(qa_chain.invoke("Value of plans around $50?"))

# answer = qa_chain.run("What is the cheapest fibre broadband plan in Singapore?")
# print(answer)


# embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
# semantic_chunker = SemanticChunker(embeddings=embedding_model)

# results = {}
# with ThreadPoolExecutor(max_workers=5) as executor:
#     future_to_site = {
#         executor.submit(
#             lambda url: ScrapeWebsiteTool(website_url=url).run(), provider.value
#         ): provider
#         for provider in BroadbandURLs
#     }

#     for future in as_completed(future_to_site):
#         provider = future_to_site[future]
#         try:
#             results[provider] = future.result()

#             print(f"{provider.name} scraped {len(results[provider])} characters")
#         except Exception as e:
#             print(f"Error scraping {provider.name}: {e}")


# semantic_chunker = RecursiveCharacterTextSplitter(
#     separators=["\n\n", "\n", " ", ""],
#     chunk_size=250,
#     chunk_overlap=50,
#     length_function=count_tokens,
# )


# splitted_documents = semantic_chunker.split_documents(
#     documents=[
#         Document(
#             page_content=text,
#             metadata={"provider": provider.name, "source": provider.value},
#         )
#         for provider, text in results.items()
#     ]
# )


# vector_store = Chroma.from_documents(
#     collection_name="prompt_engineering_playbook",
#     documents=splitted_documents,
#     embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
#     persist_directory="./chroma_langchain_db",
# )


# qa_chain = RetrievalQA.from_llm(
#     retriever=vector_store.as_retriever(),
#     llm=ChatOpenAI(model="gpt-4o-mini"),
# )


# # Build prompt
# template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer.
# {context}
# Question: {question}
# Helpful Answer:"""
# QA_CHAIN_PROMPT = PromptTemplate.from_template(template)


# qa_chain = RetrievalQA.from_chain_type(
#     ChatOpenAI(model="gpt-4.1-mini"),
#     retriever=vector_store.as_retriever(),
#     chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
# )
