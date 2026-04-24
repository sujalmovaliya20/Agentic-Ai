from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from google import genai
import os
from google.genai import types

load_dotenv()  # Load environment variables from .env file
#vector Embeddings

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
embedding_model=GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")

vector_db=QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="langchain_docs",
    embedding=embedding_model
)

#take  query from user
user_query=input("Enter your query: ") 

#relvent chunks from vector db
search_results=vector_db.similarity_search(query=user_query)

context=["\n\n\n".join([f"Page content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])]

context="\n\n\n".join([result.page_content for result in search_results])  

SYSTEM_PROMPT="""You are a helpful assistant for answering questions based on the following retrieved documents
from a pdf file along with page_contents and page numbers. 

you should only answer the based on the following context and navigate the user to open the right page number to know more.

context: {context}
"""

genai_response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=user_query,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
    )
)

print(f"🤖:{genai_response.text}")
