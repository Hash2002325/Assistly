"""
Technical Agent - Handles technical support and troubleshooting
"""
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from database.db_manager import DatabaseManager
from rag.retriever import RAGRetriever
import os
from dotenv import load_dotenv

load_dotenv()

class TechnicalAgent:
    def __init__(self):
        self.llm = ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.1"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=0.3
        )
        self.db = DatabaseManager()
        self.retriever = RAGRetriever()
        
        self.system_prompt = """You are a technical support specialist at Assistly.

Your responsibilities:
- Troubleshoot technical issues (login, performance, bugs)
- Provide step-by-step solutions
- Reference troubleshooting guides from knowledge base
- Check customer's past tickets for recurring issues

Guidelines:
- Be patient and clear with technical instructions
- Provide numbered step-by-step solutions
- Use simple language, avoid jargon
- Ask clarifying questions if needed
- Reference specific error messages or symptoms
- Offer alternative solutions if first doesn't work
- Create support tickets for unresolved issues

Tone: Patient, helpful, technically accurate
"""
    
    def handle_query(self, customer_id: str, query: str) -> str:
        """Handle technical support query"""
        
        # Get customer data
        customer = self.db.get_customer(customer_id)
        if not customer:
            return "I couldn't find your account. Please verify your customer ID."
        
        # Get past tickets
        past_tickets = self.db.get_tickets(customer_id)
        
        # Get troubleshooting guides from RAG
        knowledge_context = self.retriever.retrieve_for_technical(query)
        
        # Build context
        context = f"""
CUSTOMER INFORMATION:
- Name: {customer['name']}
- Plan: {customer['plan']} (determines available features)

PAST TECHNICAL ISSUES:
{self._format_tickets(past_tickets[:3])}

TROUBLESHOOTING GUIDES:
{knowledge_context}

CUSTOMER ISSUE:
{query}
"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=context)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def _format_tickets(self, tickets):
        """Format past tickets for context"""
        if not tickets:
            return "No previous tickets found."
        
        formatted = []
        for ticket in tickets:
            formatted.append(
                f"- Ticket #{ticket['ticket_id']}: {ticket['subject']} "
                f"({ticket['status']}) - {ticket['created_at']}"
            )
        return "\n".join(formatted)