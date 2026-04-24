from openai import OpenAI
from dotenv import load_dotenv
import os   
import json
import requests 

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="http://localhost:3000/api"
)

def get_weather_info(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The current weather in {city} is: {response.text}"
    return "Sorry, I couldn't fetch the weather information at the moment."

available_tools = {
    "get_weather_info": get_weather_info
}

SYSTEM_PROMPT = """
you are a expert ai assistant in resolving user queries using chain of thoughts prompting. you will break down the problem into smaller steps and solve each step one by one to arrive at the final solution. you will strictly follow the output in JSON format.
you work on START, PLAN and OUTPUT. you will first start with START and then move on to PLAN and finally OUTPUT.
once you think enough information is gathered and you are ready to solve the problem, you will move on to OUTPUT and provide the final solution in JSON format.
you can also call tool if required from the list of available tools.
for every tool call wait for the observe step which is the response of the tool call and then move forward with your next step.

rules:
- strictly follow the output in JSON format.
- only run one step at a time. you will not move on to the next step until you have completed the current step.
- the sequence of steps is START, PLAN, OUTPUT.

output json format:
{"step":"START" | "PLAN" | "OUTPUT" | "TOOL" | "OBSERVE", "solution":"string", "tool_name":"string", "tool_input":"string"}

Available tools:
1. get_weather_info(city:str): this tool takes a city name as input and returns the current weather information for that city.

EXAMPLE 1:
START: What is the square root of 16?
{"step":"PLAN", "solution":"to find the square root of 16, I need to find a number that when multiplied by itself gives 16. Testing 4: 4x4=16. So the answer is 4."}
{"step":"OUTPUT", "solution":"The square root of 16 is 4."}

EXAMPLE 2:
START: what is the weather of delhi?
{"step":"PLAN", "solution":"user is interested in getting weather of delhi in india"}
{"step":"PLAN", "solution":"lets see if we have any tool available for this input"}
{"step":"PLAN", "solution":"i need to call get_weather_info tool for delhi input as a city"}
{"step":"TOOL", "tool_name":"get_weather_info", "tool_input":"delhi"}
{"step":"OBSERVE", "tool_name":"get_weather_info", "output":"THE CURRENT WEATHER IN DELHI IS: PARTLY CLOUDY 30 degrees C"}
{"step":"OUTPUT", "solution":"The current weather in Delhi is: Partly cloudy 30 degrees C."}
"""

print("\n\n\n")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

user_input = input("🤭👉 ")
message_history.append({"role": "user", "content": user_input})

while True:
    response = client.chat.completions.create(
        model="deepseek-v3.1:671b-cloud",
        # ✅ FIX 1: removed response_format
        messages=message_history
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})

    if not raw_result or not raw_result.strip():
        print("⚠️ Empty response from model. Check if localhost:3000 is running.")
        break

    # ✅ Strip markdown code fences if present
    clean_result = raw_result.strip()
    if clean_result.startswith("```"):
        clean_result = clean_result.split("```")[1]
        if clean_result.startswith("json"):
            clean_result = clean_result[4:]
        clean_result = clean_result.strip()

    # ✅ Safe JSON parse
    try:
        parsed_result = json.loads(clean_result)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse failed: {e}")
        print(f"❌ Raw was: {repr(raw_result)}")
        break

    if isinstance(parsed_result, list):
        parsed_result = parsed_result[0]

    if parsed_result.get("step") == "PLAN":
        print("🧠 ", parsed_result.get("solution"))
        continue  # ✅ FIX 4: added continue

    if parsed_result.get("step") == "TOOL":
        tool_name = parsed_result.get("tool_name")
        tool_input = parsed_result.get("tool_input")
        print(f"🔧 Calling tool: {tool_name} with input: {tool_input}")
        tool_response = available_tools[tool_name](tool_input)
        message_history.append({"role": "user", "content": json.dumps(
            {"step": "OBSERVE", "tool_name": tool_name, "input": tool_input, "output": tool_response}  # ✅ FIX 3: variable not string
        )})
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("🤖", parsed_result.get("solution"))
        break

print("\n\n\n")