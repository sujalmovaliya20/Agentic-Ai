#few shot prompting: providing the model with a few examples of the task you want it to perform, along with the instruction. 
# This helps the model understand the task better and can lead to improved performance.

from openai import OpenAI
from dotenv import load_dotenv
import os   

load_dotenv()  # Load environment variables from .env file
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

#few shot prompting: providing the model with a few examples of the task you want it to perform, along with the instruction.
SYSTEM_PROMPT = """
-stricly follow the output in JSONformat.
output format:
{{
 "maths problem solution":"string",
 "ismathsproblem":boolean
}}



You are a helpful mathematics assistant. You only answer questions related to mathematics and you will not answer any other questions.
Example 1:
User: What is the square root of 16? 
Assistant: {{
 "maths problem solution":"The square root of 16 is 4.",
 "ismathsproblem":true
}}
Example 2:
User: What is the anger for you?
Assistant: {{
 "maths problem solution":"sorry, iam a mathematics assistant.",
 "ismathsproblem":false
}}
"""    
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