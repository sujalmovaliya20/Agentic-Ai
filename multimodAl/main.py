from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()  # Load environment variables from .env file
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "user",
          "content": [
              {"type":"text","text":"generate a caption for this image in about 50 words."},
              {"type":"image","source":"https://images.pexels.com/photos/34822448/pexels-photo-34822448.jpeg?_gl=1*19i78pe*_ga*MjExMDQwOTEzOC4xNzc4NDk1ODgz*_ga_8JE65Q40S6*czE3Nzg0OTU4ODIkbzEkZzEkdDE3Nzg0OTU4OTMkajQ5JGwwJGgw"}
              
          ]}
    ]
)

print("response:", response.choices[0].message.content) 





 












# https://images.pexels.com/photos/34822448/pexels-photo-34822448.jpeg?_gl=1*19i78pe*_ga*MjExMDQwOTEzOC4xNzc4NDk1ODgz*_ga_8JE65Q40S6*czE3Nzg0OTU4ODIkbzEkZzEkdDE3Nzg0OTU4OTMkajQ5JGwwJGgw