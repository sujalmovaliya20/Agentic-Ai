#chain of thoughts prompting example  


# chain of thoughts prompting: breaking down a complex problem into smaller steps and solving each step one by one to arrive at the final solution. This can help the model understand the problem better and can lead to improved performance.
#few shot prompting: providing the model with a few examples of the task you want it to perform, along with the instruction. 
# This helps the model understand the task better and can lead to improved performance.

from openai import OpenAI
from dotenv import load_dotenv
import os   
import json
import requests 
from pydantic import BaseModel
from typing import Optional
from pydantic import Field

load_dotenv()  # Load environment variables from .env file

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
def get_weather_info(city:str):
    url=f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The current weather in {city} is: {response.text}"
    return "Sorry, I couldn't fetch the weather information at the moment."

available_tools={
    "get_weather_info": get_weather_info
}
#few shot prompting: providing the model with a few examples of the task you want it to perform, along with the instruction.
SYSTEM_PROMPT = """
you are a expert ai assistant in resolving user queries using chain of thoughts prompting. you will break down the problem into smaller steps and solve each step one by one to arrive at the final solution. you will strictly follow the output in JSON format.
you work on START,PLAN and OUTPUT. you will first start with START and then move on to PLAN and finally OUTPUT.
once you think enough information is gathered and you are ready to solve the problem, you will move on to OUTPUT and provide the final solution in JSON format.
you can also call tool if required from the list of available tools.
for every tool call wait for the observe step which is the response of the tool call and then move forward with your next step.

rules:
-stricly follow the output in JSON format.
-only run one step at a time. you will not move on to the next step until you have completed the current step.
-the sequence of steps is START (whaere user gives an input), PLAN (where you break down the problem into smaller steps and solve each step one by one) and OUTPUT (where you provide the final solution in JSON format).

output json format:
{"step":"START" |  "PLAN" | "OUTPUT" | "TOOL" | "OBSERVE",
 "solution":"string","tool":"string","tool_input":"string"}

Available tools:
1. get_weather_info(city:str): this tool takes a city name as input and returns the current weather information for that city.
 
 EXAMPLE:
EXAMPLE 1:
START: What is the square root of 16?
PLAN:{"step":"PLAN",
 "solution":"to find the square root of 16, we need to find a number that
 when multiplied by itself gives 16. we can start by testing some numbers. we can test 2, 3, and 4. when we test 2, we get 2*2=4 which is not equal to 16. when we test 3, we get 3*3=9 which is not equal to 16. when we test 4, we get 4*4=16 which is equal to 16. so the square root of 16 is 4."
 }
PLAN:{"step":"PLAN",
 "solution":"to find the square root of 16, we need to find a number that
 when multiplied by itself gives 16. we can start by testing some numbers. we can test 2, 3, and 4. when we test 2, we get 2*2=4 which is not equal to 16. when we test 3, we get 3*3=9 which is not equal to 16. when we test 4, we get 4*4=16 which is equal to 16. so the square root of 16 is 4."
 }
OUTPUT:{"step":"OUTPUT",
 "solution":"The square root of 16 is 4."   
}
EXAMPLE 2:
START: what is the weather of delhi?
PLAN:{"step":"PLAN":
 "solution":"user is interseted in in getting weather to delhi in india"
 }
PLAN:{"step":"PLAN":
 "solution":"lets see if we have any tool avilable for this input"
 }
PLAN:{"step":"PLAN":
 "solution":"i need to call get_weather tool for dehli input as a city"
 }
PLAN:{"step":"TOOL","tool_name":"get_weather_info","tool_input":"delhi"}
PLAN:{"step":"OBSERVE","tool_name":"get_weather_info","tool_input":"THE CURRENT WEATHER IN DELHI IS: PARTLY CLOUDY 30°C"}

OUTPUT:{"step":"OUTPUT",
 "solution":"The current weather in Delhi is: Partly cloudy 30°C."   
}

""" 
print("\n\n\n")

class Myoutputformat(BaseModel):
    step:str = Field(..., description="the step can be START, PLAN, OUTPUT, TOOL or OBSERVE")
    content:Optional[str] = Field(None, description="the solution for the current step")
    tool_name:Optional[str] = Field(None, description="the name of the tool to be called if step is TOOL or OBSERVE")
    tool_input:Optional[str] = Field(None, description="the input for the tool if step is TOOL or OBSERVE") 

   

message_history = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    },
]
while True:
    user_input = input("🤭👉 ")
    message_history.append({"role": "user",  "content": user_input})

    while True:
      response = client.chat.completions.parse(
        model="gemini-3-flash-preview",
        response_format=Myoutputformat,
        messages=message_history
      )
      raw_result = response.choices[0].message.content
      message_history.append({"role": "assistant", "content": raw_result})
      parsed_result =  response.choices[0].message.parsed

      if parsed_result.step == "START":
        print("🧠 ", parsed_result.content)

      if parsed_result.step == "PLAN":
        print("🧠 ", parsed_result.solution)

      if parsed_result.step == "TOOL":
        tool_name = parsed_result.tool_name
        tool_input = parsed_result.tool_input
        print(f"🔧 Calling tool: {tool_name} with input: {tool_input}")
        tool_response = available_tools[tool_name](tool_input)
        message_history.append({"role":"user","content":json.dumps(
            {"step":"OBSERVE","tool":"tool_name","input":tool_input,"output":tool_response }
        )})
        continue
      if parsed_result.step == "OUTPUT":
        print("🤖", parsed_result.solution)
        break


 
    print("\n\n\n")



