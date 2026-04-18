from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(
    api_key="AIzaSyAMKzB3W2qc4oEjeKqJ_3gu4Tyj-cgNsWc"

)

response = client.models.generate_content(
    model="gemini-3-flash-preview", contents=input("pro")
)
print(response.text)