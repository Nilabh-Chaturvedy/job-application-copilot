from langgraph.graph import StateGraph, END
from .state import AppState
from src.resume_builder import build_resume_text
from src.resume_structurer import structure_resume
from agents.planner import planner_agent
from agents.writer import writer_agent
from agents.verifier import verifier_agent
from agents.cover_letter_agent import cover_letter_agent

#Create Graph

def structure_resume_node(state):
    state["structured_resume"]=structure_resume(state["resume_text"])
    return state

def build_resume_node(state):
    structured=state["structured_resume"]

    if structured.get("experience") and state["rewritten_bullets"]:
        structured["experience"][0]["bullets"] = state["rewritten_bullets"]

    state["final_resume_text"] = build_resume_text(structured)
    return state


builder=StateGraph(AppState)

builder.add_node("structure resume",structure_resume_node)
builder.add_node("planner",planner_agent)
builder.add_node("writer",writer_agent)
builder.add_node("verifier",verifier_agent)
builder.add_node("cover_letter",cover_letter_agent)
builder.add_node("build_resume",build_resume_node)

#Define the Agentic Flow

builder.set_entry_point("structure resume")
builder.add_edge("structure resume","planner")
builder.add_edge("planner","writer")
builder.add_edge("writer","cover_letter")
builder.add_edge("cover_letter","verifier")



def route_after_verifier(state):
   if state["verification_passed"]:
       return "build_resume"
   if state["retry_count"]>=2:
       return "build_resume"
   else:
       return "writer"
   
builder.add_conditional_edges("verifier",route_after_verifier)
builder.add_edge("build_resume",END)

graph=builder.compile()
