import pandas as pd
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import requests

def load_dataset(file_path):
    df=pd.read_csv(file_path)
    docs=[]
    for _,row in df.iterrows():
        content="\n".join([f"{col}: {row[col]}" for col in df.columns if pd.notna(row[col])])
        docs.append(Document(page_content=content))
    return docs

def create_vectorstore(docs):
    splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    split_docs=splitter.split_documents(docs)
    embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore=FAISS.from_documents(split_docs,embedding=embeddings)
    return vectorstore

def call_groq_llm(prompt,api_key,context):
    url="https://api.groq.com/openai/v1/chat/completions"
    headers={
        "Authorization":f"Bearer {api_key}",
        "Content-Type":"application/json"
    }
    data={
        "model":"mixtral-8x7b-32768",
        "messages":[
            {"role":"system","content":"You are a loan data assistant who answers based on provided context. Keep it factual."},
            {"role":"user","content":f"Context:\n{context}\n\nQuestion:\n{prompt}\n\nAnswer:"}
        ],
        "temperature":0.5
    }
    res=requests.post(url,headers=headers,json=data)
    if res.status_code==200:
        return res.json()["choices"][0]["message"]["content"]
    else:
        return f"API Error {res.status_code}: {res.text}"
