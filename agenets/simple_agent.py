import os
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent 
from langchain_core.messages import AnyMessage
from langchain_openai import  ChatOpenAI 
from langgraph.store.memory import InMemoryStore
from langgraph.config import get_store 
from langgraph.prebuilt.chat_agent_executor import AgentState
# Import tools from separate module
from inmemory_store import bootstrap_memory_store 
from insurance_tools import TOOLS
from utils import get_logger

# Load environment variables from .env file

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")

# Configure logging

logger = get_logger(__name__)
logger.info("Starting Simple Agent setup...")

llm = ChatOpenAI(model="gpt-4o")

INSURANCE_SSTEM_PROMPT = """
You are an insurance assistant that helps customers manage their policies and claims.
You have access to the following tools to help customers with their insurance needs:
- Get customer information and contact details
- Retrieve all policies for a customer
- Get detailed policy information including coverage amounts, deductibles, and premiums
- Check if claims exist in the system
- View all claims for a specific customer
- Get current status of any claim (Processing, Approved, Closed, Under Investigation, Denied)
- Add new claims (with validation that customer has active policy)
- Update claim status
- Calculate coverage remaining after potential claims
- Get premium breakdown (annual, monthly, quarterly payments)
- Filter claims by status across all customers
- Get current system date
Always be helpful and professional when assisting customers with their insurance matters.
Before creating new claims, verify the customer has an active policy that covers the claim type.
Provide clear explanations of policy coverage, deductibles, and claim processes.
When discussing claim amounts, always explain the customer's responsibility (deductible) and what insurance will cover.
The customer you are helping is:
"""

langgraph_server = False
active_store = None
try:
    active_store = get_store()
    langgraph_server = True
    logger.info("Connected to LangGraph server store.")
except Exception as e:
    logger.warning(f"Could not connect to LangGraph server store: {e}")
    active_store = InMemoryStore()

bootstrap_memory_store(active_store)

logger.info("building prompted agent...")

def prompt(state: AgentState,) -> list[AnyMessage]:
    system_msg = f"{INSURANCE_SSTEM_PROMPT}. If you are asked about your name ,respond with 'InsureBot'."
    return [{"role": "system", "content": system_msg}] + state["messages"]
logger.info("creating react agent...")
agent = create_react_agent(
    model=llm,
    tools=[ *TOOLS],
    store=active_store if not langgraph_server else None,
    prompt=prompt,
)