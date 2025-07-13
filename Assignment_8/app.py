import streamlit as st
from rag_utils import load_dataset, create_vectorstore, call_groq_llm

st.set_page_config(page_title="Loan Dataset RAG Chatbot")

st.title("Loan Approval Dataset Q&A Bot")
st.markdown("Ask any question about the loan dataset using a free LLM (Groq).")

@st.cache_resource
def load_vector_db():
    docs=load_dataset("data/Training Dataset.csv")
    vectorstore=create_vectorstore(docs)
    return vectorstore

vectorstore=load_vector_db()

query=st.text_input("Enter your question about the loan data")
api_key=st.text_input("Enter your Groq API key",type="password")

if query and api_key:
    with st.spinner("Retrieving relevant data..."):
        docs=vectorstore.similarity_search(query,k=4)
        context="\n\n".join([doc.page_content for doc in docs])
    
    with st.spinner("Generating answer..."):
        answer=call_groq_llm(query,api_key,context)
        st.subheader("Answer")
        st.write(answer)
