# Insurance AI Agent - LangGraph Based

A sophisticated AI-powered insurance management system built with LangGraph, LangChain, and OpenAI's GPT-4. This agent helps customers manage policies, track claims, and get personalized insurance assistance through natural language interactions.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Agent Logic](#agent-logic)
- [Tools & Capabilities](#tools--capabilities)
- [API Integration](#api-integration)
- [Data Model](#data-model)

---

## 🎯 Overview

The **Insurance AI Agent** is a conversational AI system that understands natural language queries about insurance policies and claims. It uses a ReAct (Reasoning-Acting-Observing) pattern to intelligently select and execute appropriate tools to answer customer questions.

**Key Capabilities:**
- Retrieve customer information and contact details
- Query and manage insurance policies
- Track and manage insurance claims
- Calculate coverage and deductibles
- Generate premium breakdowns
- Filter and analyze claims across customers

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    User Input (Chat)                         │
│              (chat_with_agent.py or main.py)                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 LangGraph React Agent                        │
│         (simple_agent.py - create_react_agent)              │
│                                                              │
│  • LLM: ChatOpenAI (gpt-4o)                                 │
│  • Framework: LangGraph v1.0.4                              │
│  • Pattern: ReAct (Reason-Act-Observe)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Customer    │ │   Policy     │ │   Claims     │
│   Tools      │ │   Tools      │ │   Tools      │
│(insurance_   │ │(insurance_   │ │(insurance_   │
│tools.py)     │ │tools.py)     │ │tools.py)     │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │   InMemoryStore (LangGraph)   │
        │                               │
        │  • Namespace: users           │
        │  • Namespace: policies        │
        │  • Namespace: claims          │
        │                               │
        │  (inmemory_store.py)          │
        └───────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │    Response to User           │
        │   (formatted, readable)       │
        └───────────────────────────────┘
```

### ReAct Agent Flow

The agent operates in a loop:

1. **REASON** - LLM analyzes the user query and available tools
2. **ACT** - LLM selects and invokes the most appropriate tool(s)
3. **OBSERVE** - Agent receives tool output
4. **REPEAT** - If more information needed, go back to step 1
5. **RESPOND** - LLM generates final response to user

---

## ✨ Features

### 1. **Customer Management**
- Get customer information (name, email, phone, address, DOB, join date)
- Search customers by ID
- View customer profiles with associated policies

### 2. **Policy Management**
- Retrieve all policies for a customer
- Get detailed policy information (coverage, deductible, premium, status)
- View policy dates and terms
- Calculate annual/monthly/quarterly premiums

### 3. **Claims Management**
- View all claims for a specific customer
- Get current claim status (Processing, Approved, Closed, Under Investigation, Denied)
- Create new claims with validation
- Update claim status
- Filter claims by status across all customers

### 4. **Coverage Analytics**
- Calculate remaining coverage after approved claims
- Calculate deductibles by policy type
- Generate premium breakdowns
- Track claim utilization percentage

### 5. **Natural Language Interface**
- Ask questions in plain English
- Agent intelligently routes to appropriate tools
- Conversational, user-friendly responses

---

## 📁 Project Structure

```
simple-ai-agent/
├── genets/                          # Main agent package
│   ├── __init__.py
│   ├── simple_agent.py             # Agent initialization & configuration
│   ├── insurance_tools.py          # 12 LangChain tools for insurance operations
│   ├── inmemory_store.py           # Data models & store initialization
│   └── utils.py                    # Logging utilities
│
├── main.py                          # Test harness with 3 sample questions
├── chat_with_agent.py              # Interactive chat interface (main entry point)
├── test_google_api.py              # Google Places API integration test
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (API keys)
├── .gitignore                      # Git ignore patterns
└── README.md                       # This file
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.13+
- UV package manager (or pip)
- OpenAI API key
- Internet connection

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/simple-ai-agent.git
cd simple-ai-agent
```

### Step 2: Create Virtual Environment (UV)
```bash
uv venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source .venv/bin/activate     # macOS/Linux
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create `.env` file in root directory:
```env
OPENAI_API_KEY=sk-proj-your-api-key-here
GOOGLE_API_KEY=your-google-api-key
HUGGINGFACEHUB_API_TOKEN=your-token
ANTHROPIC_API_KEY=your-key
```

### Step 5: Run the Agent
```bash
# Interactive chat mode (recommended)
python chat_with_agent.py

# Run test suite
python main.py

# Test Google Places API
python test_google_api.py
```

---

## 💬 Usage

### Interactive Chat Mode

```bash
python chat_with_agent.py
```

**Example Interactions:**

```
You: Get me the contact information for customer u1

Agent: Here is the contact information for customer **Alice Johnson** (Customer ID: u1):
- Email: alice.johnson@email.com
- Phone: +1-555-0101
- Address: 123 Main St, New York, NY 10001
```

```
You: What are the details of policy p3?

Agent: Here are the details for policy **p3**:
- Policy Type: Home Insurance
- Coverage Amount: $750,000
- Deductible: $2,000
- Premium: $850.00 annually
- Status: Active
```

```
You: Show me all the claims for customer u2

Agent: Here are the claims for customer u2:
1. Claim ID: c2
   - Type: Vehicle Damage
   - Date: 2024-06-20
   - Amount: $15,000
   - Status: Processing

2. Claim ID: c6
   - Type: Liability Claim
   - Date: 2024-03-12
   - Amount: $8,500
   - Status: Closed
```

### Test Suite

```bash
python main.py
```

Runs 3 predefined test questions to validate agent functionality.

---

## 🧠 Agent Logic

### ReAct Pattern Explanation

The agent uses **ReAct (Reasoning-Acting-Observing)** framework:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. REASONING                                                │
│    LLM reads user query and analyzes available tools       │
│    Example: "I need customer info, let me use get_customer │
│    _information tool"                                       │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. ACTING                                                   │
│    LLM invokes selected tool with appropriate parameters   │
│    Example: Tool call: get_customer_information(u1)        │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. OBSERVING                                                │
│    Tool executes and returns result                         │
│    Example: Returns customer Alice Johnson's details       │
└─────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. REASONING AGAIN (if needed)                              │
│    LLM checks if more information needed                    │
│    If yes → go back to ACTING                              │
│    If no → generate final response                         │
└─────────────────────────────────────────────────────────────┘
```

### Key Design Decisions

1. **InMemoryStore**: Local namespace-based persistence for fast prototyping
2. **ReAct Pattern**: Transparent reasoning chain visible in logs
3. **Tool-based Architecture**: Modular, extensible tool system
4. **Error Handling**: Comprehensive validation and user-friendly errors
5. **Logging**: Detailed logging for debugging and monitoring

---

## 🛠️ Tools & Capabilities

### Customer Information Tools (2 tools)

| Tool | Purpose | Parameters | Returns |
|------|---------|-----------|---------|
| `get_customer_information` | Get customer details | customer_id | Name, email, phone, address, DOB, join_date |
| `get_user_policy_info` | Get customer's policy | user_id | User data + associated policy |

### Policy Tools (2 tools)

| Tool | Purpose | Parameters | Returns |
|------|---------|-----------|---------|
| `get_customer_policies` | All policies for customer | customer_id | List of policies |
| `get_policy_details` | Detailed policy info | policy_id | Coverage, deductible, premium, dates, status |

### Claims Tools (5 tools)

| Tool | Purpose | Parameters | Returns |
|------|---------|-----------|---------|
| `check_claims_exist` | Check if customer has claims | customer_id | Boolean + count |
| `get_customer_claims` | All claims for customer | customer_id | List of claims |
| `get_claim_status` | Current claim status | claim_id | Status, amount, date |
| `add_new_claim` | Create new claim | customer_id, policy_id, amount, description | New claim details |
| `update_claim_status` | Update claim status | claim_id, new_status | Updated claim |

### Coverage & Premium Tools (2 tools)

| Tool | Purpose | Parameters | Returns |
|------|---------|-----------|---------|
| `calculate_remaining_coverage` | Remaining coverage after claims | customer_id | Total, claimed, remaining, utilization % |
| `get_premium_breakdown` | Payment schedule | policy_id | Annual, monthly, quarterly amounts |

### Utility Tools (2 tools)

| Tool | Purpose | Parameters | Returns |
|------|---------|-----------|---------|
| `filter_claims_by_status` | Filter all claims by status | status | Claims list by status |
| `get_current_system_date` | Current date/time | none | ISO datetime string |

---

## 🔌 API Integration

### OpenAI Integration
- **Model**: gpt-4o
- **Purpose**: Natural language understanding and response generation
- **Configuration**: `ChatOpenAI(model="gpt-4o")`

### Google Places API Integration
- **Endpoint**: `/v1/places:searchNearby`
- **Purpose**: Find nearby restaurants/businesses
- **Test Script**: `test_google_api.py`
- **Requirements**: Google API key with Places API enabled

### LangGraph Integration
- **Version**: 1.0.4+
- **Purpose**: Agent orchestration and state management
- **Features**: ReAct pattern, store management, message threading

---

## 💾 Data Model

### User Namespace (8 customers)
```python
{
    "user_id": "u1",
    "name": "Alice Johnson",
    "email": "alice.johnson@email.com",
    "phone": "+1-555-0101",
    "address": "123 Main St, New York, NY 10001",
    "date_of_birth": "1994-03-15",
    "join_date": "2020-06-15"
}
```

### Policies Namespace (12 policies)
```python
{
    "policy_id": "p1",
    "user_id": "u1",
    "policy_type": "Health",
    "premium": 1200.00,
    "deductible": 1000,
    "coverage_amount": 500000,
    "start_date": "2020-06-15",
    "end_date": "2025-06-15",
    "status": "Active"
}
```

### Claims Namespace (10 claims)
```python
{
    "claim_id": "c1",
    "policy_id": "p1",
    "user_id": "u1",
    "claim_type": "Medical",
    "claim_date": "2024-01-15",
    "amount": 5000.00,
    "status": "Approved",
    "description": "Hospital visit and surgery"
}
```

---

## 🔧 Configuration

### System Prompt
Located in `simple_agent.py`, defines agent behavior:
```
"You are an insurance assistant that helps customers manage their 
policies and claims. You have access to tools to help customers with 
their insurance needs..."
```

### Environment Variables
```env
OPENAI_API_KEY          # Required: OpenAI API key
GOOGLE_API_KEY          # Optional: Google Places API
HUGGINGFACEHUB_API_TOKEN # Optional: Hugging Face token
ANTHROPIC_API_KEY       # Optional: Anthropic API key
```

---

## 📊 Logging

The agent includes comprehensive logging:

```python
logger.info("Retrieved customer information for u1")
logger.warning("Customer u1 not found")
logger.error("Failed to retrieve customer information: ...")
```

View logs in console output when running the agent.

---

## 🐛 Troubleshooting

### Issue: "OPENAI_API_KEY not found"
**Solution**: Create `.env` file with your OpenAI API key

### Issue: "ModuleNotFoundError: No module named 'langgraph'"
**Solution**: Install dependencies: `pip install -r requirements.txt`

### Issue: Agent not responding to queries
**Solution**: Check logs for errors, ensure API key is valid

### Issue: Google Places API returns 403 error
**Solution**: Whitelist your IP address in Google Cloud Console

---

## 📚 Dependencies

Key packages:
- **langgraph** (1.0.4+) - Agent orchestration
- **langchain-core** (1.1.1+) - LLM tools & messages
- **langchain-openai** - OpenAI integration
- **python-dotenv** - Environment variables
- **pydantic** - Data validation
- **requests** - HTTP requests

See `requirements.txt` for complete list.

---

## 📝 Examples

### Example 1: Get Customer Information
```python
from genets.simple_agent import agent
from langchain_core.messages import HumanMessage

result = agent.invoke(
    {"messages": [HumanMessage(content="Get me contact info for u1")]},
    config={"configurable": {"thread_id": "session_1"}}
)
print(result["messages"][-1].content)
```

### Example 2: Query Policy Details
```python
result = agent.invoke(
    {"messages": [HumanMessage(content="What is policy p3 details?")]},
    config={"configurable": {"thread_id": "session_2"}}
)
```

### Example 3: Check Claims Status
```python
result = agent.invoke(
    {"messages": [HumanMessage(content="Show claims for customer u2")]},
    config={"configurable": {"thread_id": "session_3"}}
)
```

---

## 🚀 Future Enhancements

- [ ] Persistent database backend (PostgreSQL)
- [ ] Web UI dashboard
- [ ] Email notifications
- [ ] PDF report generation
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Real-time claim updates
- [ ] SMS integration

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

Created as a demonstration of LangGraph and LangChain capabilities for building AI agents.

---

## 📞 Support

For issues or questions, please refer to:
- [LangGraph Documentation](https://github.com/langchain-ai/langgraph)
- [LangChain Documentation](https://python.langchain.com)
- [OpenAI API Documentation](https://platform.openai.com/docs)