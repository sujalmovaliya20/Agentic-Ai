#chain of thoughts prompting example  


# chain of thoughts prompting: breaking down a complex problem into smaller steps and solving each step one by one to arrive at the final solution. This can help the model understand the problem better and can lead to improved performance.
#few shot prompting: providing the model with a few examples of the task you want it to perform, along with the instruction. 
# This helps the model understand the task better and can lead to improved performance.

from openai import OpenAI
from dotenv import load_dotenv
import os   
import json

load_dotenv()  # Load environment variables from .env file
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

#few shot prompting: providing the model with a few examples of the task you want it to perform, along with the instruction.
SYSTEM_PROMPT = """
you are a expert ai assistant in resolving user queries using chain of thoughts prompting. you will break down the problem into smaller steps and solve each step one by one to arrive at the final solution. you will strictly follow the output in JSON format.
you work on START,PLAN and OUTPUT STEPS. you will first start with START and then move on to PLAN and finally OUTPUT STEPS.
once you think enough information is gathered and you are ready to solve the problem, you will move on to OUTPUT STEPS and provide the final solution in JSON format.

rules:
-stricly follow the output in JSON format.
-only run one step at a time. you will not move on to the next step until you have completed the current step.
-the sequence of steps is START (whaere user gives an input), PLAN (where you break down the problem into smaller steps and solve each step one by one) and OUTPUT STEPS (where you provide the final solution in JSON format).

output json format:
{"step":"START" |  "PLAN" | "OUTPUT STEPS",
 "solution":"string"}

 EXAMPLE:
START: What is the square root of 16?
PLAN:{"step":"PLAN",
 "solution":"to find the square root of 16, we need to find a number that
 when multiplied by itself gives 16. we can start by testing some numbers. we can test 2, 3, and 4. when we test 2, we get 2*2=4 which is not equal to 16. when we test 3, we get 3*3=9 which is not equal to 16. when we test 4, we get 4*4=16 which is equal to 16. so the square root of 16 is 4."
 }
PLAN:{"step":"PLAN",
 "solution":"to find the square root of 16, we need to find a number that
 when multiplied by itself gives 16. we can start by testing some numbers. we can test 2, 3, and 4. when we test 2, we get 2*2=4 which is not equal to 16. when we test 3, we get 3*3=9 which is not equal to 16. when we test 4, we get 4*4=16 which is equal to 16. so the square root of 16 is 4."
 }
OUTPUT STEPS:{"step":"OUTPUT STEPS",
 "solution":"The square root of 16 is 4."   
}

""" 
print("\n\n\n")
message_history = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    },
]
user_input = input("🤭👉 ")
message_history.append({"role": "user",  "content": user_input})

while True:
    response = client.chat.completions.create(
        model="gemini-3-flash-preview",
        response_format={"type": "json_object"},
        messages=message_history
    )
    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})
    parsed_result = json.loads(raw_result)

    if isinstance(parsed_result, list):
        parsed_result = parsed_result[0]

    if parsed_result.get("step") == "PLAN":
        print("🧠 ", parsed_result.get("solution"))

    if parsed_result.get("step") == "OUTPUT STEPS":
        print("🤖", parsed_result.get("solution"))
        break


 
print("\n\n\n")


