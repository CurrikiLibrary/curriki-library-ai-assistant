from typing import Annotated, TypedDict
from langgraph.graph import END, START, StateGraph
from classes.assistant import Assistant

print(Assistant)
exit()

def reduce_value(existing_value: int, new_value: int) -> int:
    return existing_value + new_value

class StateA(TypedDict):
    value: Annotated[int, reduce_value]

builder = StateGraph(StateA)

builder.add_node("my_node", lambda state: {"value": 1})

builder.add_edge(START, "my_node")
builder.add_edge("my_node", END)

graph = builder.compile()

thread_id = "some-thread"
config = {"configurable": {"thread_id": thread_id}}

result = graph.invoke({"value": 5}, config)

print(result)
