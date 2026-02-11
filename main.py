"""
Main entry point to test Assistly
"""
from graph.workflow import run_assistly

if __name__ == "__main__":
    # Test cases
    test_cases = [
        {
            "customer_id": "CUST001",
            "query": "I was charged twice for my subscription this month!"
        },
        {
            "customer_id": "CUST002",
            "query": "I can't login to my account, getting an error message"
        },
        {
            "customer_id": "CUST003",
            "query": "What features are included in the Enterprise plan?"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n\n{'#' * 70}")
        print(f"TEST CASE {i}")
        print(f"{'#' * 70}\n")
        
        response = run_assistly(
            customer_id=test['customer_id'],
            query=test['query']
        )
        
        print(f"\n📝 Response:\n{response}\n")
        input("\nPress Enter to continue to next test...")