"""
Interactive Chat Interface for Insurance Agent
Allows users to have a continuous conversation with the insurance agent.
"""

import sys
from langchain_core.messages import HumanMessage
from agenets.simple_agent import agent
from agenets.utils import get_logger

logger = get_logger(__name__)


def print_banner():
    """Print welcome banner."""
    print("\n" + "="*80)
    print("INSURANCE AGENT - INTERACTIVE CHAT")
    print("="*80)
    print("\nWelcome! I'm your insurance assistant. I can help you with:")
    print("  • Customer information and contact details")
    print("  • Policy information, coverage, and premiums")
    print("  • Claims status and history")
    print("  • Coverage calculations and deductible information")
    print("\nType 'quit' or 'exit' to end the conversation.")
    print("="*80 + "\n")


def get_user_question() -> str:
    """
    Get question from user with proper prompting.
    
    Returns:
        User's question or command
    """
    try:
        user_input = input("You: ").strip()
        return user_input
    except EOFError:
        # Handle EOF (Ctrl+D or End of Input)
        return "exit"
    except KeyboardInterrupt:
        # Handle Ctrl+C
        print("\n\nGoodbye!")
        sys.exit(0)


def should_exit(user_input: str) -> bool:
    """
    Check if user wants to exit the chat.
    
    Args:
        user_input: User's input string
    
    Returns:
        True if user wants to exit, False otherwise
    """
    exit_commands = {"quit", "exit", "bye", "goodbye", "q"}
    return user_input.lower() in exit_commands


def extract_response(result: dict) -> str:
    """
    Extract agent response from result dictionary.
    
    Args:
        result: Result from agent.invoke()
    
    Returns:
        Formatted response string
    """
    if not result or "messages" not in result:
        return "I encountered an error processing your request. Please try again."
    
    messages = result["messages"]
    if not messages:
        return "No response generated. Please try again."
    
    # Get the last message (should be the agent's response)
    last_message = messages[-1]
    
    # Extract content from message
    if hasattr(last_message, "content"):
        return last_message.content
    elif isinstance(last_message, dict) and "content" in last_message:
        return last_message["content"]
    else:
        return str(last_message)


def run_chat_loop():
    """Run the interactive chat loop."""
    print_banner()
    
    thread_id = 0  # Session ID for message threading
    
    try:
        while True:
            # Get user question
            user_question = get_user_question()
            
            # Check if user wants to exit
            if should_exit(user_question):
                print("\nThank you for using the Insurance Agent. Goodbye!\n")
                break
            
            # Skip empty input
            if not user_question:
                print("Please ask a question or type 'quit' to exit.\n")
                continue
            
            logger.info(f"User question: {user_question}")
            
            try:
                # Invoke agent with user question
                print("\nAgent: ", end="", flush=True)
                
                result = agent.invoke(
                    {"messages": [HumanMessage(content=user_question)]},
                    config={"configurable": {"thread_id": f"chat_session_{thread_id}"}}
                )
                
                # Extract and print response
                response = extract_response(result)
                print(response)
                print()
                
                logger.info(f"Agent response sent successfully")
                thread_id += 1
                
            except Exception as e:
                logger.error(f"Error invoking agent: {str(e)}")
                print(f"\nSorry, I encountered an error: {str(e)}")
                print("Please try again.\n")
    
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error in chat loop: {str(e)}")
        print(f"\nAn unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    try:
        run_chat_loop()
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f"Fatal error: {str(e)}")
        sys.exit(1)
