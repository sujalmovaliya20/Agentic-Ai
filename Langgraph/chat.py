from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import StateGraph, add_messages
from langgraph.graph import StateGraph,START,END
from langchain_nvidia_ai_endpoints import ChatNVIDIA

llm= ChatNVIDIA(
  model="minimaxai/minimax-m2.7",
  api_key="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", 
)


class State(TypedDict):
   messages: Annotated[list, add_messages]

def chatbot(state: State):
   response=llm.invoke(state.get("messages"))
   return {"messages":[response ]}
 
def samplenode(state:State):
   return {"messages":["sample message append"]}
    

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("samplenode",samplenode)

graph_builder.add_edge(START,'chatbot')
graph_builder.add_edge('chatbot','samplenode')
graph_builder.add_edge('samplenode',END)

graph=graph_builder.compile()

updated_state=graph.invoke(State({"messages":["hi,my name is sujal movaliya"]}))

print(updated_state) 