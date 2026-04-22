from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="http://localhost:3000/api"
)

response = client.chat.completions.create(
    model="deepseek-v3.1:671b-cloud",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful mathematics assistant.you only answer the question related to mathematics and you will not answer any other question"
        },
        {
            "role": "user",
            "content": input("Enter your question: ")
        }
    ]
)

print(response.choices[0].message.content)