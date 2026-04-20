from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
client = OpenAI(
    
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

#zero shot prompting:directly giving the instruction to the model without providing any examples.
SYSTEM_PROMPT = "You are a helpful mathematics assistant. You only answer questions related to mathematics and you will not answer any other questions."    
response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": input("Enter your question: ")
        }
    ]
)

print(response.choices[0].message.content)