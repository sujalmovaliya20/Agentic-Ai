from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyAMKzB3W2qc4oEjeKqJ_3gu4Tyj-cgNsWc",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
        
        {
            "role": "user",
            "content": input("Enter your question: ")
        }
    ]
)

print(response.choices[0].message.content)