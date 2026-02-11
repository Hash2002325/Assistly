"""
Assistly - Streamlit Web Interface with Conversation Memory
"""
import streamlit as st
from graph.workflow import run_assistly
from database.db_manager import DatabaseManager

st.set_page_config(
    page_title="Assistly - AI Customer Support",
    page_icon="🤖",
    layout="wide"
)

@st.cache_resource
def get_db():
    return DatabaseManager()

db = get_db()

# Header
st.title("🤖 Assistly - AI Customer Support")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Customer Login")
    customers = db.execute_query("SELECT customer_id, name, email FROM customers ORDER BY name")
    customer_options = {f"{c['name']} ({c['customer_id']})": c['customer_id'] for c in customers}
    selected_customer = st.selectbox("Select Customer", options=list(customer_options.keys()))
    customer_id = customer_options[selected_customer]
    customer = db.get_customer(customer_id)
    
    if customer:
        st.success(f"✅ {customer['name']}")
        st.info(f"📧 {customer['email']}\n💳 {customer['plan']}")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "🎫 Tickets", "💳 Billing", "ℹ️ About"])

with tab1:
    st.header("Chat with AI Support")
    st.caption("🧠 Conversation memory enabled - the agent remembers your chat history")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("How can we help you?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 Processing your request..."):
                response = run_assistly(
                    customer_id=customer_id, 
                    query=prompt,
                    history=st.session_state.messages
                )
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    if st.session_state.messages:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

with tab2:
    st.header("Support Tickets")
    tickets = db.get_tickets(customer_id)
    
    if tickets:
        for ticket in tickets:
            status_emoji = {'open': '🔴', 'in_progress': '🟡', 'resolved': '🟢'}.get(ticket['status'], '⚪')
            with st.expander(f"{status_emoji} #{ticket['ticket_id']}: {ticket['subject']}"):
                st.write(f"**Type:** {ticket['issue_type']}")
                st.write(f"**Priority:** {ticket['priority']}")
                st.write(f"**Status:** {ticket['status']}")
                st.write(f"**Created:** {ticket['created_at']}")
                st.write(f"**Description:** {ticket['description']}")
    else:
        st.info("No tickets found")

with tab3:
    st.header("Billing History")
    billing = db.get_billing_history(customer_id)
    
    if billing:
        for record in billing:
            status_emoji = "✅" if record['status'] == 'paid' else "❌" if record['status'] == 'failed' else "⏳"
            with st.expander(f"{status_emoji} {record['billing_date']} - ${record['amount']}"):
                st.write(f"**Invoice:** {record['invoice_number']}")
                st.write(f"**Status:** {record['status']}")
                st.write(f"**Method:** {record['payment_method']}")
    else:
        st.info("No billing history")

with tab4:
    st.header("About Assistly")
    st.markdown("""
    ### 🤖 AI-Powered Multi-Agent Customer Support
    
    **Version 2.0 - Now with Conversation Memory!**
    
    **Features:**
    - ✅ Intelligent query routing
    - ✅ Specialized agents (Billing, Technical, Sales)
    - ✅ RAG-powered knowledge base
    - ✅ Real-time database access
    - ✅ **NEW: Conversation memory** - Agents remember your chat history
    
    **How Conversation Memory Works:**
    The system now maintains context across messages. When you ask a follow-up question,
    the agent remembers what you said before and responds accordingly.
    
    **Example:**
    - You: "I can't login"
    - Agent: "Let me help you troubleshoot..."
    - You: "Wrong password, using Chrome"
    - Agent: "Based on your previous message about login issues and now knowing you're using Chrome..." ✨
    
    **Version:** 2.0.0 (with memory)
    """)

# Footer - Production Style
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Assistly 2026</p>
</div>
""", unsafe_allow_html=True)