"""
Billing Agent - Handles payment, refund, and subscription queries
"""
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from database.db_manager import DatabaseManager
from rag.retriever import RAGRetriever
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class BillingAgent:
    def __init__(self):
        self.llm = ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.1"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=0.3
        )
        self.db = DatabaseManager()
        self.retriever = RAGRetriever()
        
        self.system_prompt = """You are a billing specialist at Assistly customer support.

Your responsibilities:
- Help with payment issues, refunds, invoices
- Explain billing policies clearly
- Check customer billing history in database
- Resolve billing disputes professionally

Guidelines:
- Be empathetic and understanding about billing concerns
- Always check the database for customer's actual billing data
- Use the knowledge base for policy information
- Provide specific invoice numbers and dates
- Offer concrete solutions, not just explanations
- Escalate complex issues to human support if needed
- If this is a follow-up message, acknowledge previous conversation

Tone: Professional, empathetic, solution-oriented
"""
    
    def handle_query(self, customer_id: str, query: str, history: List[Dict] = None) -> str:
        """Handle billing-related query with conversation history"""
        
        # Get customer data
        customer = self.db.get_customer(customer_id)
        if not customer:
            return "I couldn't find your account. Please verify your customer ID."
        
        # Get billing history
        billing_history = self.db.get_billing_history(customer_id)
        failed_payments = self.db.get_failed_payments(customer_id)
        
        # Get relevant knowledge from RAG
        knowledge_context = self.retriever.retrieve_for_billing(query)
        
        # Format conversation history
        history_text = ""
        if history and len(history) > 0:
            history_text = "PREVIOUS CONVERSATION:\n"
            # Show last 6 messages (3 exchanges)
            for msg in history[-6:]:
                role = "Customer" if msg['role'] == 'user' else "Agent"
                history_text += f"{role}: {msg['content']}\n"
            history_text += "\n"
        
        # Build context
        context = f"""
{history_text}CUSTOMER INFORMATION:
- Name: {customer['name']}
- Email: {customer['email']}
- Current Plan: {customer['plan']}

RECENT BILLING HISTORY:
{self._format_billing_history(billing_history[:5])}

FAILED PAYMENTS:
{self._format_billing_history(failed_payments) if failed_payments else "None"}

RELEVANT POLICIES:
{knowledge_context}

CURRENT CUSTOMER MESSAGE:
{query}

INSTRUCTIONS:
- If this is a follow-up to previous conversation, acknowledge the context
- Answer the current question while considering conversation history
- Be conversational and natural
"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=context)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def _format_billing_history(self, billing_records):
        """Format billing records for context"""
        if not billing_records:
            return "No billing history found."
        
        formatted = []
        for record in billing_records:
            formatted.append(
                f"- {record['billing_date']}: ${record['amount']} ({record['status']}) "
                f"Invoice: {record['invoice_number']}"
            )
        return "\n".join(formatted)