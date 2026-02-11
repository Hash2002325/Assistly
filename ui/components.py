"""
Reusable UI components for Assistly
"""
import streamlit as st
from database.db_manager import DatabaseManager

def show_billing_history(customer_id: str):
    """Display customer's billing history"""
    db = DatabaseManager()
    billing = db.get_billing_history(customer_id)
    
    if not billing:
        st.info("No billing history found")
        return
    
    st.subheader("💳 Billing History")
    
    for record in billing[:5]:  # Show last 5
        status_emoji = "✅" if record['status'] == 'paid' else "❌" if record['status'] == 'failed' else "⏳"
        
        with st.expander(f"{status_emoji} {record['billing_date']} - ${record['amount']}"):
            st.write(f"**Invoice:** {record['invoice_number']}")
            st.write(f"**Status:** {record['status']}")
            st.write(f"**Payment Method:** {record['payment_method']}")

def show_tickets(customer_id: str):
    """Display customer's support tickets"""
    db = DatabaseManager()
    tickets = db.get_tickets(customer_id)
    
    if not tickets:
        st.info("No support tickets found")
        return
    
    st.subheader("🎫 Support Tickets")
    
    # Filter by status
    status_filter = st.radio("Filter", ["All", "Open", "In Progress", "Resolved"], horizontal=True)
    
    filtered_tickets = tickets
    if status_filter != "All":
        filtered_tickets = [t for t in tickets if t['status'] == status_filter.lower().replace(" ", "_")]
    
    for ticket in filtered_tickets:
        status_color = {
            'open': '🔴',
            'in_progress': '🟡',
            'resolved': '🟢'
        }.get(ticket['status'], '⚪')
        
        with st.expander(f"{status_color} Ticket #{ticket['ticket_id']}: {ticket['subject']}"):
            st.write(f"**Type:** {ticket['issue_type']}")
            st.write(f"**Priority:** {ticket['priority']}")
            st.write(f"**Status:** {ticket['status']}")
            st.write(f"**Created:** {ticket['created_at']}")
            st.write(f"**Description:** {ticket['description']}")