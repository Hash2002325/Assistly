"""
Main LangGraph workflow for Assistly
Orchestrates the multi-agent customer support system
"""
from langgraph.graph import StateGraph, END
from graph.state import AssistlyState
from graph.nodes import (
    route_query,
    handle_billing,
    handle_technical,
    handle_sales,
    determine_route
)
from typing import List, Dict

def create_assistly_workflow():
    """Create the LangGraph workflow"""
    
    # Initialize graph
    workflow = StateGraph(AssistlyState)
    
    # Add nodes (each step in the process)
    workflow.add_node("route_query", route_query)
    workflow.add_node("handle_billing", handle_billing)
    workflow.add_node("handle_technical", handle_technical)
    workflow.add_node("handle_sales", handle_sales)
    
    # Set entry point
    workflow.set_entry_point("route_query")
    
    # Add conditional edges (routing logic)
    workflow.add_conditional_edges(
        "route_query",
        determine_route,
        {
            "billing": "handle_billing",
            "technical": "handle_technical",
            "sales": "handle_sales"
        }
    )
    
    # All specialist nodes end the workflow
    workflow.add_edge("handle_billing", END)
    workflow.add_edge("handle_technical", END)
    workflow.add_edge("handle_sales", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app

def run_assistly(customer_id: str, query: str, history: List[Dict] = None) -> str:
    """
    Main function to run Assistly workflow with conversation memory
    
    Args:
        customer_id: Customer identifier (e.g., 'CUST001')
        query: Customer's question or issue
        history: List of previous messages [{"role": "user/assistant", "content": "..."}]
    
    Returns:
        Agent's response
    """
    print("=" * 60)
    print("🤖 ASSISTLY - AI CUSTOMER SUPPORT")
    print("=" * 60)
    
    # Create workflow
    app = create_assistly_workflow()
    
    # Initial state
    initial_state = {
        "customer_id": customer_id,
        "query": query,
        "route": "",
        "response": "",
        "conversation_history": history if history else []
    }
    
    # Run workflow
    result = app.invoke(initial_state)
    
    print("\n" + "=" * 60)
    print("✅ RESPONSE READY")
    print("=" * 60)
    
    return result['response']