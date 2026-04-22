#persona based prompting: providing the model with a specific persona or character to adopt while generating responses. This can help guide the model's behavior and make it more consistent in its responses.
from openai import OpenAI
from dotenv import load_dotenv
import os   

load_dotenv()  # Load environment variables from .env file
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
SYSTEM_PROMPT = """
you are an ai presona assistant named Sujal movaliya.
you are acting behalf of sujal movaliya who is 20 years old tech enthusiatic and ai enginner
your main stack is javascript and pyhton 

Examples:
Q:hey
A:hey whats up!

"""

response = client.chat.completions.create(
        model="gemini-3-flash-preview",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": input("Enter your question: ")}
         ]
    )

print("response: ",response.choices[0].message.content)