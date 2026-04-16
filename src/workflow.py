from langgraph.graph import StateGraph, END
from .state import AppState

from agents.planner import planner_agent
from agents.writer import writer_agent
from agents.verifier import verifier_agent
from agents.cover_letter_agent import cover_letter_agent

#Create Graph

builder=StateGraph(AppState)

builder.add_node("planner",planner_agent)
builder.add_node("writer",writer_agent)
builder.add_node("verifier",verifier_agent)
builder.add_node("cover_letter",cover_letter_agent)

#Define the Agentic Flow

builder.set_entry_point("planner")
builder.add_edge("planner","writer")
builder.add_edge("writer","cover_letter")
builder.add_edge("cover_letter","verifier")


def route_after_verifier(state):
   if state["verification_passed"]:
       return END
   if state["retry_count"]>=2:
       return END
   else:
       return "writer"
   
builder.add_conditional_edges("verifier",route_after_verifier)

graph=builder.compile()
