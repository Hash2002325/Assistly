"""
Sales Agent - Handles product inquiries, upgrades, and feature questions
"""
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from database.db_manager import DatabaseManager
from rag.retriever import RAGRetriever
import os
from dotenv import load_dotenv

load_dotenv()

class SalesAgent:
    def __init__(self):
        self.llm = ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.1"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=0.4  # Slightly higher for friendlier responses
        )
        self.db = DatabaseManager()
        self.retriever = RAGRetriever()
        
        self.system_prompt = """You are a sales specialist at Assistly.

Your responsibilities:
- Answer questions about features and plans
- Help customers choose the right plan
- Explain upgrade/downgrade processes
- Highlight value and benefits
- Compare plan features

Guidelines:
- Be enthusiastic but not pushy
- Focus on customer needs, not just features
- Provide clear plan comparisons
- Mention current plan and suggest relevant upgrades
- Be honest about limitations of each plan
- Provide specific pricing and feature details
- Make it easy to take next steps

Tone: Friendly, helpful, value-focused
"""
    
    def handle_query(self, customer_id: str, query: str) -> str:
        """Handle sales/product query"""
        
        # Get customer data
        customer = self.db.get_customer(customer_id)
        if not customer:
            return "I couldn't find your account. Please verify your customer ID."
        
        # Get current plan details
        current_plan = self.db.get_plan(customer['plan'])
        
        # Get all available plans
        all_plans = self.db.get_all_plans()
        
        # Get product info from RAG
        knowledge_context = self.retriever.retrieve_for_sales(query)
        
        # Build context
        context = f"""
CUSTOMER INFORMATION:
- Name: {customer['name']}
- Current Plan: {current_plan['plan_name']} (${current_plan['price']}/{current_plan['billing_cycle']})

ALL AVAILABLE PLANS:
{self._format_plans(all_plans)}

PRODUCT INFORMATION:
{knowledge_context}

CUSTOMER QUESTION:
{query}
"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=context)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def _format_plans(self, plans):
        """Format plan information"""
        if not plans:
            return "No plans available."
        
        formatted = []
        for plan in plans:
            formatted.append(
                f"- {plan['plan_name']}: ${plan['price']}/{plan['billing_cycle']}\n"
                f"  Features: {plan['features']}"
            )
        return "\n".join(formatted)