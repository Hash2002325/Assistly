"""
State definition for LangGraph workflow
This is the data that flows between agents
"""
from typing import TypedDict, Literal

class AssistlyState(TypedDict):
    """State object passed between nodes in the graph"""
    customer_id: str
    query: str
    route: Literal["billing", "technical", "sales"]
    response: str
    conversation_history: list