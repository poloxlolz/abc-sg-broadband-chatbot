import streamlit as st
from graphviz import Digraph

st.set_page_config(page_title="Methodology", layout="centered")

st.title("📖 Methodology")

st.markdown("""
### 🔄 Data Flow & Implementation Details

This application is designed to help users explore and compare broadband plans in Singapore using a **Retrieval-Augmented Generation (RAG)** chatbot.  
The pipeline combines **automated data collection (via CrewAI agents)**, **document processing**, and **LLM-powered question answering**.  

**1. Data Collection (Scraping & Curation)**  
- The system uses **CrewAI agents** to scrape and consolidate information from reliable sources such as:
  - Broadband provider websites (Starhub, Singtel, M1, etc.).  
  - Third-party curated sources like **HardwareZone forums**.  
- The **thirdparty_scraper agent** handles raw extraction.  
- The **content_curator agent** processes and cleans the scraped data, ensuring it is structured for later embedding.  

**2. Data Preparation & Storage**  
- Scraped text is stored as documents and split into smaller chunks using a **Markdown text splitter**.  
- Each chunk is embedded into vector representations using **OpenAI Embeddings**.  
- The embeddings are indexed into a **Chroma vector store**, enabling efficient similarity search.  

**3. User Interaction (Chat Interface)**  
- The chatbot is deployed via **Streamlit**.  
- Users can ask broadband-related queries in natural language.  
- A **multi-turn chat history** is maintained so responses remain context-aware across conversation turns.  

**4. Retrieval & Augmentation (RAG Pipeline)**  
- When a user submits a query:
  - The system uses a **history-aware retriever** to reformulate the question, taking conversation history into account.  
  - The retriever searches the Chroma vector store for the most relevant broadband documents.  

**5. Response Generation**  
- Retrieved context is combined with the user query.  
- A **ChatGPT model (e.g., GPT-4.1-mini)** generates an answer that:  
  - Summarizes plan details (price, speed, promotions).  
  - Compares pros and cons.  
  - Provides friendly recommendations tailored to user needs (gaming, streaming, work-from-home).  

**6. Output Delivery**  
- Responses are displayed in a **chat-style UI**, with a typing animation for realism.  
- Users can continue asking follow-up questions, and the process repeats seamlessly.  
""")

st.markdown("---")
st.subheader("📊 Flowchart of the Chatbot Pipeline")

# Create a styled flowchart
flow = Digraph()

flow.attr(rankdir="TB", size="8")

# Styles
input_style = {"shape": "parallelogram", "style": "filled", "fillcolor": "#AED6F1"}
agent_style = {"shape": "box", "style": "filled", "fillcolor": "#F9E79F"}
process_style = {"shape": "box", "style": "filled", "fillcolor": "#ABEBC6"}
retrieval_style = {"shape": "cylinder", "style": "filled", "fillcolor": "#F5B7B1"}
llm_style = {"shape": "diamond", "style": "filled", "fillcolor": "#D2B4DE"}
output_style = {"shape": "oval", "style": "filled", "fillcolor": "#A3E4D7"}

# Nodes
flow.node("A", "CrewAI Agents\n(Scraper & Curator)", **agent_style)
flow.node("B", "Cleaned Broadband Data\n(Markdown docs)", **process_style)
flow.node("C", "Split into Chunks\n(Markdown Splitter)", **process_style)
flow.node("D", "Embed with OpenAI\n(Vector Embeddings)", **process_style)
flow.node("E", "Store in Chroma\n(Vector Database)", **retrieval_style)
flow.node("F", "User Query via Streamlit UI", **input_style)
flow.node("G", "History-Aware Retriever\n(Reformulates Query)", **process_style)
flow.node("H", "Retrieve Top-k Docs\nfrom Chroma", **retrieval_style)
flow.node("I", "Combine Query + Context\n(RAG Pipeline)", **process_style)
flow.node("J", "LLM Reasoning &\nResponse Generation", **llm_style)
flow.node("K", "Streamlit Chat UI\nDisplays Answer", **output_style)

# Edges
flow.edge("A", "B")
flow.edge("B", "C")
flow.edge("C", "D")
flow.edge("D", "E")
flow.edge("F", "G")
flow.edge("G", "H")
flow.edge("E", "H")
flow.edge("H", "I")
flow.edge("I", "J")
flow.edge("J", "K")

st.graphviz_chart(flow)
