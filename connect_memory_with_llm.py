from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
from langchain_groq import ChatGroq


def get_api_key():
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        load_dotenv()  # Load environment variables from .env
        api_key = os.getenv("GROQ_API_KEY")

    return api_key
#1)Initialize Groq LLM
llm_model = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.6,
    max_tokens=512
)

#2)Custom prompt
custom_prompt_templet = """You are HealthVis, a medical advisor chatbot. Use only the pieces of information provided in the context to answer the user's question accurately. 
If you don't know the answer, say that you don't know or if the word is similar but has spelling mistake ask user to spell properly— do NOT make up an answer. 
Do NOT provide information outside the given context. 
If the user asks about your creator, respond with: "I was created by Prathamesh Lawande." 
Always provide clear and direct answers. You can give health tips, explain symptoms, and provide guidance based on the context, but never go beyond it. 
Do not include small talk. 

Context: {context}
Question: {question}
Start the answer immediately.
"""

from langchain_core.prompts import PromptTemplate

def set_custom_prompt(custom_prompt_templet):
    return PromptTemplate(template=custom_prompt_templet, input_variables=["context","question"])

#3)Load FAISS DB
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
DB_FAISS_PATH = 'Vectorstore/db_faiss'
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)

#4)Create QA chain
from langchain.chains import RetrievalQA
qa_chain = RetrievalQA.from_chain_type(
    llm=llm_model,
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={"k":7}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": set_custom_prompt(custom_prompt_templet)}
)

#5)Run chatbot
def get_response(user_query : str):
    full_response = qa_chain.invoke({"query":user_query})
    if isinstance(full_response, dict) and "result" in full_response:
        return full_response["result"]
    return str(full_response)

