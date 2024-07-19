from typing import Callable
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda
from classes.state import State
from langgraph.prebuilt import ToolNode

def create_entry_node(agent_name: str, new_dialog_state: str) -> Callable:
    def entry_node(state: State) -> dict:
        tool_call_id = state["messages"][-1].tool_calls[0]["id"]
        return {
            "messages": [
                ToolMessage(
                    content=f"The agent is now the {agent_name}. Reflect on the above conversation between the host agent and the user."
                    f" The user's intent is unsatisfied. Use the provided tools to assist the user. Remember, you are {agent_name},"
                    " and the library search (explore), create course, create lesson and other action is not complete until after you have successfully invoked the appropriate tool."
                    " If the user changes their mind or needs help for other tasks, call the CompleteOrEscalate function to let the primary host agent take control."
                    " Do not mention who you are - just act as the proxy for the agent.",
                    tool_call_id=tool_call_id,
                )
            ],
            "dialog_state": new_dialog_state,
        }

    return entry_node

def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }

def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )