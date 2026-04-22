import openai

client = openai.OpenAI(
    api_key="sk-8cb1aa2334ab4aa491f66d4a87f27299",
    base_url="http://localhost:3000/api"  # point to OpenWebUI, not Ollama directly
)

response = client.chat.completions.create(
    model="deepseek-v3.1:671b-cloud",  # any model you've pulled in Ollama
    messages=[{"role": "user", "content": input("prompt: ")}]
)
print(response.choices[0].message.content)