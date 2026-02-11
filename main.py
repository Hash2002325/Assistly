"""
Main entry point to test Assistly with conversation memory
"""
from graph.workflow import run_assistly

if __name__ == "__main__":
    print("\n" + "="*70)
    print("TESTING ASSISTLY WITH CONVERSATION MEMORY")
    print("="*70)
    
    # Simulate a conversation with memory
    customer_id = "CUST002"
    conversation_history = []
    
    # First message
    print("\n" + "="*70)
    print("MESSAGE 1: Initial Query")
    print("="*70)
    query1 = "I can't login to my account"
    print(f"\n👤 Customer: {query1}")
    response1 = run_assistly(customer_id, query1, conversation_history)
    print(f"\n🤖 Agent: {response1}\n")
    
    # Add to history
    conversation_history.append({"role": "user", "content": query1})
    conversation_history.append({"role": "assistant", "content": response1})
    
    input("\n[Press Enter to continue to next message...]")
    
    # Second message (follow-up with context)
    print("\n" + "="*70)
    print("MESSAGE 2: Follow-up with Additional Info")
    print("="*70)
    query2 = "Wrong password and I'm using Chrome browser"
    print(f"\n👤 Customer: {query2}")
    response2 = run_assistly(customer_id, query2, conversation_history)
    print(f"\n🤖 Agent: {response2}\n")
    
    # Add to history
    conversation_history.append({"role": "user", "content": query2})
    conversation_history.append({"role": "assistant", "content": response2})
    
    input("\n[Press Enter to continue to next message...]")
    
    # Third message (further follow-up)
    print("\n" + "="*70)
    print("MESSAGE 3: Another Follow-up")
    print("="*70)
    query3 = "Yes, I already tried the forgot password option"
    print(f"\n👤 Customer: {query3}")
    response3 = run_assistly(customer_id, query3, conversation_history)
    print(f"\n🤖 Agent: {response3}\n")
    
    print("\n" + "="*70)
    print("✅ CONVERSATION MEMORY TEST COMPLETE!")
    print("="*70)
    print("\nNotice how the agent remembers:")
    print("- The login issue from message 1")
    print("- Browser and password info from message 2")
    print("- References previous troubleshooting attempts")