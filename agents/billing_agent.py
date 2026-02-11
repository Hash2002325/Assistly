"""
Billing Agent - Handles payment, refund, and subscription queries
"""
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from database.db_manager import DatabaseManager
from rag.retriever import RAGRetriever
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

Tone: Professional, empathetic, solution-oriented
"""
    
    def handle_query(self, customer_id: str, query: str) -> str:
        """Handle billing-related query"""
        
        # Get customer data
        customer = self.db.get_customer(customer_id)
        if not customer:
            return "I couldn't find your account. Please verify your customer ID."
        
        # Get billing history
        billing_history = self.db.get_billing_history(customer_id)
        failed_payments = self.db.get_failed_payments(customer_id)
        
        # Get relevant knowledge from RAG
        knowledge_context = self.retriever.retrieve_for_billing(query)
        
        # Build context
        context = f"""
CUSTOMER INFORMATION:
- Name: {customer['name']}
- Email: {customer['email']}
- Current Plan: {customer['plan']}

RECENT BILLING HISTORY:
{self._format_billing_history(billing_history[:5])}

FAILED PAYMENTS:
{self._format_billing_history(failed_payments) if failed_payments else "None"}

RELEVANT POLICIES:
{knowledge_context}

CUSTOMER QUERY:
{query}
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