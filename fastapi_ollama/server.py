from fastapi import FastAPI, Body
from ollama import Client
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

client = Client(
    host=os.getenv("OLLAMA_HOST"),
    headers={
        "Authorization": f"Bearer {os.getenv('OLLAMA_API_KEY')}"
    }
)
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/chat")
def chat(
    message: str = Body(..., description="The message to send to the model")
):
    ollama_response = client.chat(
        model="deepseek-v3.1:671b-cloud",
        messages=[{"role": "user", "content": message}]
    )
    return {"response": ollama_response.message.content}