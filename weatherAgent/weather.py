from openai import OpenAI
from dotenv import load_dotenv
import os
import requests

load_dotenv()  # Load environment variables from .env file
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="http://localhost:3000/api"
)
def get_weather_info(city:str):
    url=f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The current weather in {city} is: {response.text}"
    return "Sorry, I couldn't fetch the weather information at the moment."


     

def main():
    user_input = input("Enter your question: ")
    response = client.chat.completions.create(
        model="deepseek-v3.1:671b-cloud",
        messages=[
            {"role" :"user", "content": user_input }
        ]
    )

    print(f"🤖 : {response.choices[0].message.content}")

print(get_weather_info("surat"))