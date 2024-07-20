from typing import Literal
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph
from langgraph.prebuilt import tools_condition
from classes.state import State
from classes.assistant import Assistant
from agents.primary.primary_agent import PrimaryAgent
from workflow.util import create_tool_node_with_fallback
from tools.user_info import UserInfo
from langgraph.graph import END, START

class Graph:
    def __init__(self):
        self.memory = SqliteSaver.from_conn_string(":memory:")
        self.builder = StateGraph(State)

    def compile(self):
        graph = self.builder.compile(checkpointer=self.memory)
        return graph
    
    def workflow(self):
        def user_info(state: State):
            return {"user_info": UserInfo.get_user_info.invoke({})}
        
        self.builder.add_node("fetch_user_info", user_info)
        self.builder.add_edge(START, "fetch_user_info")

        self.builder.add_node("primary_agent", Assistant(PrimaryAgent.runnable))
        self.builder.add_node(
            "primary_agent_tools", create_tool_node_with_fallback(PrimaryAgent.get_primary_agent_tools)
        )

builder = StateGraph(State)

""" 
def user_info(state: State):
    return {"user_info": fetch_user_flight_information.invoke({})}


builder.add_node("fetch_user_info", user_info)
builder.add_edge(START, "fetch_user_info")
 """

# Primary agent
builder.add_node("primary_agent", Assistant(PrimaryAgent.runnable))
builder.add_node(
    "primary_agent_tools", create_tool_node_with_fallback(PrimaryAgent.get_primary_agent_tools)
)


# Compile graph
memory = SqliteSaver.from_conn_string(":memory:")
part_4_graph = builder.compile(
    checkpointer=memory
)

# --------------------------- Basid Graph ----------------------
"""
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import tools_condition

builder = StateGraph(State)


# Define nodes: these do the work
builder.add_node("assistant", Assistant(part_1_assistant_runnable))
builder.add_node("tools", create_tool_node_with_fallback(part_1_tools))
# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")

# The checkpointer lets the graph persist its state
# this is a complete memory for the entire graph.
memory = SqliteSaver.from_conn_string(":memory:")
part_1_graph = builder.compile(checkpointer=memory) 
"""

# --------------------------- Advanced Graph ----------------------
