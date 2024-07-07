from typing import TypedDict, Annotated, Literal, Optional
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

def update_dialog_stack(left: list[str], right: Optional[str]) -> list[str]:
    """Push or pop the state."""
    if right is None:
        return left
    if right == "pop":
        return left[:-1]
    return left + [right]

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_info: str
    diaglog_state: Annotated[
        list[
            Literal[
                "assistant",
                "curriki_library_explorer",
                "create_course",
                "create_lesson",
            ]
        ],
        update_dialog_stack
    ]