import streamlit as st

st.set_page_config(page_title="About Us", layout="centered")

st.title("About Us")

st.markdown("""
### 🏗️ Project Scope
This project was developed to provide insights and tools for exploring and understanding broadband plans in Singapore.  
Our aim is to make information about pricing, speeds, and promotions more transparent and easier to compare.

---

### 🎯 Objectives
- **Simplify broadband comparison** by aggregating information from multiple providers.  
- **Highlight deals and features** in a clear and structured way.  
- **Help users make informed choices** about which plans fit their needs.  
- **Demonstrate LLM-powered retrieval** in an educational prototype.  

---

### 📊 Data Sources
The information in this app is based on:
- Official broadband provider websites.  
- Third-party curated content (e.g., HardwareZone forums).  
- Publicly available reference materials.  

---

### ⚙️ Features
- **Interactive chatbot** that answers broadband-related questions.  
- **Context-aware responses** with multi-turn memory powered by Retrieval-Augmented Generation (RAG).  
- **Simple, accessible interface** built with Streamlit.  
""")
