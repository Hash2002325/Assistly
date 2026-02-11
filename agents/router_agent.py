"""
Router Agent - Analyzes customer query and routes to appropriate specialist
"""
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()

class RouterAgent:
    def __init__(self):
        self.llm = ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.1"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=0.1  # Low temperature for consistent routing
        )
        
        self.system_prompt = """You are a routing agent for Assistly customer support.

Your job is to analyze the customer's query and determine which specialist should handle it.

Available specialists:
- BILLING: Payment issues, refunds, invoices, subscription changes, billing errors
- TECHNICAL: Login problems, bugs, performance issues, integration problems, errors
- SALES: Product questions, plan upgrades, feature inquiries, pricing, demos

Rules:
- Respond with ONLY ONE WORD: BILLING, TECHNICAL, or SALES
- If query mentions money/payment/invoice/refund → BILLING
- If query mentions error/bug/not working/slow/login → TECHNICAL  
- If query mentions features/plans/pricing/upgrade → SALES
- If unclear, default to TECHNICAL

Examples:
"I was charged twice" → BILLING
"Can't login to my account" → TECHNICAL
"What features are in Pro plan?" → SALES
"My dashboard is slow" → TECHNICAL
"""
    
    def route(self, customer_query: str) -> str:
        """
        Route customer query to appropriate department
        Returns: 'billing', 'technical', or 'sales'
        """
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"Customer query: {customer_query}")
        ]
        
        response = self.llm.invoke(messages)
        route_decision = response.content.strip().upper()
        
        # Normalize response
        if "BILLING" in route_decision:
            return "billing"
        elif "TECHNICAL" in route_decision:
            return "technical"
        elif "SALES" in route_decision:
            return "sales"
        else:
            # Default fallback
            return "technical"