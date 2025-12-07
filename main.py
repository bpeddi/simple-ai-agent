"""
Insurance Agent Test Script
Tests the insurance agent with 3 sample questions covering customer info, claims, and policies.
"""

import os
import sys
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

# Add the agenets directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agenets'))

try:
    from simple_agent import agent, active_store
    from utils import get_logger
    from inmemory_store import bootstrap_memory_store
except ImportError as e:
    print(f"Error importing modules: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

logger = get_logger(__name__)


def test_agent():
    """Test the insurance agent with sample questions."""
    
    logger.info("=" * 80)
    logger.info("INSURANCE AGENT TEST SUITE")
    logger.info("=" * 80)
    
    # Test questions covering different aspects
    test_questions = [
        {
            "id": 1,
            "category": "Customer Information",
            "question": "Get me the contact information for customer u1 (Alice Johnson)"
        },
        {
            "id": 2,
            "category": "Policy Information",
            "question": "What are the details of policy p3 including coverage amount, deductible, and premium?"
        },
        {
            "id": 3,
            "category": "Claims Information",
            "question": "Show me all the claims for customer u2 and their current status"
        }
    ]
    
    logger.info(f"\nInitialized InMemoryStore with customer data")
    logger.info(f"Ready to test agent with {len(test_questions)} questions\n")
    
    # Run each test question
    for test in test_questions:
        logger.info(f"\n{'-' * 80}")
        logger.info(f"TEST {test['id']}: {test['category']}")
        logger.info(f"{'-' * 80}")
        logger.info(f"Question: {test['question']}\n")
        
        try:
            # Create input message
            input_message = HumanMessage(content=test['question'])
            
            # Invoke the agent
            logger.info("Invoking agent...\n")
            result = agent.invoke(
                {"messages": [input_message]},
                config={"configurable": {"thread_id": f"test_{test['id']}"}}
            )
            
            # Extract and display the response
            if result and "messages" in result:
                messages = result["messages"]
                if messages:
                    last_message = messages[-1]
                    logger.info(f"Agent Response:")
                    logger.info(f"{last_message.content}\n")
            
            logger.info(f"✅ Test {test['id']} completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Test {test['id']} failed: {str(e)}")
            import traceback
            traceback.print_exc()
    
    logger.info(f"\n{'=' * 80}")
    logger.info("TEST SUITE COMPLETED")
    logger.info(f"{'=' * 80}\n")


if __name__ == "__main__":
    try:
        test_agent()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
