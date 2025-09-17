#1)load_raw_pdf

from langchain_community.document_loaders import PyPDFLoader , DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_PATH = "Data"


def pdf_data_loader(data):
    loader = DirectoryLoader(data,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)
    document = loader.load()

    return document

documents = pdf_data_loader(data = DATA_PATH)

#2)create_chunks

def create_chunks(extracted_data):
    chunk_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                    chunk_overlap= 50)
    text_chunks = chunk_splitter.split_documents(extracted_data)

    return text_chunks
chunks = create_chunks(documents)

#3)Create_vector_embeddings
from langchain_huggingface import HuggingFaceEmbeddings

def load_embedding_model():
    embedding_model = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2" )

    return embedding_model

embedding_model = load_embedding_model()

#4)Store_Embeddings_in_faiss
from langchain_community.vectorstores import FAISS

DB_FAISS_PATH = 'Vectorstore/db_faiss'

db = FAISS.from_documents(chunks,embedding_model)

db.save_local(DB_FAISS_PATH)
