from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from google import genai
import os
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="langchain_docs",
    embedding=embedding_model
)

SYSTEM_PROMPT = """You are a helpful assistant for answering questions based on the following retrieved documents
from a pdf file along with page_contents and page numbers.

You should only answer based on the following context and navigate the user to open the right page number to know more.

context: {context}
"""

def process_query(query: str):
    print(f"searching chunks: {query}")
    
    search_results = vector_db.similarity_search(query=query)
    
    context = "\n\n\n".join([result.page_content for result in search_results])
    
    system_prompt = SYSTEM_PROMPT.format(context=context)
    
    genai_response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=query,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
        )
    )
    
    print(f"🤖: {genai_response.text}")


# if __name__ == "__main__":
#     while True:
#         user_input = input("You: ").strip()
#         if user_input.lower() in ["exit", "quit"]:  
#             break
#         if user_input:
#             process_query(user_input)