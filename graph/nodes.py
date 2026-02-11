"""
Node functions for LangGraph workflow
Each node is a step in the customer support process
"""
from agents.router_agent import RouterAgent
from agents.billing_agent import BillingAgent
from agents.technical_agent import TechnicalAgent
from agents.sales_agent import SalesAgent
from graph.state import AssistlyState

# Initialize agents (reuse across calls)
router_agent = RouterAgent()
billing_agent = BillingAgent()
technical_agent = TechnicalAgent()
sales_agent = SalesAgent()

def route_query(state: AssistlyState) -> AssistlyState:
    """Node: Route the customer query to appropriate agent"""
    print(f"🔀 Routing query: {state['query'][:50]}...")
    
    route = router_agent.route(state['query'])
    state['route'] = route
    
    print(f"✅ Routed to: {route.upper()}")
    return state

def handle_billing(state: AssistlyState) -> AssistlyState:
    """Node: Handle billing queries"""
    print(f"💰 Billing agent processing...")
    
    response = billing_agent.handle_query(
        customer_id=state['customer_id'],
        query=state['query'],
        history=state.get('conversation_history', [])
    )
    
    state['response'] = response
    return state

def handle_technical(state: AssistlyState) -> AssistlyState:
    """Node: Handle technical queries"""
    print(f"🔧 Technical agent processing...")
    
    response = technical_agent.handle_query(
        customer_id=state['customer_id'],
        query=state['query'],
        history=state.get('conversation_history', [])
    )
    
    state['response'] = response
    return state

def handle_sales(state: AssistlyState) -> AssistlyState:
    """Node: Handle sales queries"""
    print(f"💼 Sales agent processing...")
    
    response = sales_agent.handle_query(
        customer_id=state['customer_id'],
        query=state['query'],
        history=state.get('conversation_history', [])
    )
    
    state['response'] = response
    return state

def determine_route(state: AssistlyState) -> str:
    """Conditional edge: Determine which specialist to call"""
    return state['route']