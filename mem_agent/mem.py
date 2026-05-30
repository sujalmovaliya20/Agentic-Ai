# from mem0 import Memory
# import os

# import openai

# OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

# config = {
#     "version": "v1.1",
#     "embedder":{
#         "provider":"openai",
#         "config":{
#             "api_key":"OPENAI_API_KEY","model":"text-embeddings-3-small"
#         },
#     },
#     "llm":{
#         "provider":"openai",
#         "config":{
#             "api_key":"OPENAI_API_KEY","model":"text-embeddings-3-small"
        

#          },
#     },
#     "vector_store":{
#         "provider":"qdrant",
#         "config":{
#                 "host":"localhost",
#                 "port":6333,
#     }

#     }
# }  

# mem_client = Memory.from_config(config)

from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI
import os
import json

load_dotenv()

# API Keys
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_embedder_API_KEY = os.getenv("NVIDIA_embedder_API_KEY")

# NVIDIA OpenAI-Compatible Client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)

# mem0 Configuration
config = {
    "version": "v1.1",

    # Use OpenAI compatible embedder
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": NVIDIA_embedder_API_KEY,
            "model": "nvidia/nv-embed-v1",
            "openai_base_url": "https://integrate.api.nvidia.com/v1"
        },
    },

    # Use OpenAI compatible LLM
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": NVIDIA_API_KEY,
            "model": "minimaxai/minimax-m2.7",
            "openai_base_url": "https://integrate.api.nvidia.com/v1"
        },
    },

    # Vector Store
    "vector_store": {
                  "provider": "qdrant",
                 "config": {
                        "host": "localhost",
                        "port": 6333,
                        "collection_name": "nvidia_mem0",
                        "embedding_model_dims": 4096  # ← add this
        },
    },
}

# Initialize Memory
mem_client = Memory.from_config(config)

# User Input
while True:
    user_input = input("> ")

    search_memory = mem_client.search(
    query=user_input,
    filters={"user_id": "user_123"}
    )

    memories = [
        f"ID:{mem.get('id')}\nMemory:{mem.get('memory')}\nCreated At:{mem.get('created_at')}\n\n"
        for mem in search_memory.get("results")
    ]

    print("found memories:",memories)

    SYSTEM_PROMPT = f"""
     here is the context about user:
     {json.dumps(memories)}
     """

    # Chat Completion
    response = client.chat.completions.create(
        model="minimaxai/minimax-m2.7",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    ai_response = response.choices[0].message.content

    print("AI Response:", ai_response)

    # Store Memory
    mem_client.add(
    messages=[
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": ai_response}
    ],
    user_id="user_123"
)