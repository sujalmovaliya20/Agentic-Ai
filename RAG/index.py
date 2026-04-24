from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings


load_dotenv()  # Load environment variables from .env file
pdf_path=Path(__file__).parent/"technical.pdf"

#load this file in python program

loader=PyPDFLoader(file_path=pdf_path)
doc=loader.load()          #it give you pages 

#split the docs into smaller chunks
text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,chunk_overlap=200)

chunks=text_splitter.split_documents(documents=doc)

#vector Embeddings
embedding_model=GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")

vector_store=QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="langchain_docs"

)

print("Documents have been indexed successfully!")