from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import StateGraph, add_messages
from langgraph.graph import StateGraph,START,END
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.checkpoint.mongodb import MongoDBSaver

llm= ChatNVIDIA(
  model="minimaxai/minimax-m2.7",
  api_key="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", 
)


class State(TypedDict):
   messages: Annotated[list, add_messages]

def chatbot(state: State):
   response=llm.invoke(state.get("messages"))
   return {"messages":[response ]}
 

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot",chatbot)


graph_builder.add_edge(START,'chatbot')
graph_builder.add_edge('chatbot',END)

graph=graph_builder.compile()

def compile_graph_with_checkpoint(checkpointer):
   return graph_builder.compile(checkpointer=checkpointer)

DB_URI = "mongodb://localhost:27017"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
      
      graph_with_checkpointer = compile_graph_with_checkpoint(checkpointer=checkpointer)

      config ={
          "configurable" :{
              "thread_id": "chat_thread_1"
          }
      }
      for chunk in graph_with_checkpointer.stream(
           {"messages": ["what is my name?"]},
          config=config,
          stream_mode="values"
         ):
           chunk["messages"][-1].pretty_print()
      