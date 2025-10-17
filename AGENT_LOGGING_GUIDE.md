# Agent Logging Enhancement Guide

## 🔍 Enhanced Logging Features Added

Your Imperial Court system now has comprehensive logging to track every step the agents take! Here's what has been implemented:

### 🏛️ **Main Orchestrator Logging** (`app/orchestrator.py`)

**Added detailed logging at every stage:**

1. **Incident Processing Initiation**

   ```
   🏛️ IMPERIAL COURT INCIDENT PROCESSING INITIATED
   📋 Incident Text: [first 100 characters]...
   ```

2. **RAG Context Gathering**

   ```
   🔍 Gathering RAG context from historical cases and knowledge base...
   📚 RAG Context Retrieved - Cases: X, KB: Y
   ```

3. **Workflow Selection**
   ```
   🎭 Running in MOCK_MODE; returning synthesized results
   🤖 Initiating CrewAI Agent Workflow...
   ```

### 🎭 **Mock Mode Enhanced Logging**

**Step-by-step agent simulation with emojis:**

```
🎭 MOCK MODE AGENT SIMULATION INITIATED
📊 Simulating agent database tool usage...
   🔍 Agent retrieving operational overview...
   ✅ Operational data retrieved: X vessels
   🏥 Agent checking system health...
   ✅ System health retrieved: Y% EDI error rate
   📦 Agent detected container-related incident, searching containers...
   🔍 Agent searching for container: MSKU0000001
   ✅ Container details retrieved for MSKU0000001
🧠 Agent analyzing incident type and severity...
   📋 Incident classified as: Container Management
   ⚖️ Severity assessed as: Medium
🎯 Agents formulating strategic response...
   📝 Strategic Analysis (智文): [analysis]
   🔍 Policy Review (明鏡): [review]
   👑 Imperial Decision (太和智君): [decision]
✅ MOCK MODE AGENT PROCESSING COMPLETED
```

### 🤖 **CrewAI Workflow Logging**

**Comprehensive agent workflow tracking:**

```
🤖 CREWAI AGENT WORKFLOW INITIATED
👥 Assembling Imperial Court: 太和智君 (Emperor), 智文 (Strategy), 明鏡 (Review)
🏗️ Creating specialized agents with database tool access...
📋 Creating specialized tasks with database investigation requirements...
🏛️ Assembling Imperial Court crew with agents and tasks...
🚀 INITIATING CREWAI WORKFLOW EXECUTION...
   📊 Strategic Analysis Agent (智文) will investigate incident using database tools
   🔍 Policy Review Agent (明鏡) will validate analysis with database evidence
   👑 Emperor (太和智君) will make final decision based on synthesized intelligence
✅ CREWAI WORKFLOW COMPLETED SUCCESSFULLY
📜 Final Result Length: [X] characters
```

### 🛠️ **Database Tool Usage Logging** (`app/agent_tools.py`)

**Every database tool call is now logged:**

```
🛠️ Agent tool invoked: get_operational_overview()
   ✅ Tool get_operational_overview completed successfully

🛠️ Agent tool invoked: check_system_health()
   ✅ Tool check_system_health completed successfully

🛠️ Agent tool invoked: get_container_details(MSKU0000001)
   ❌ Tool get_container_details returned error: Database not connected
```

### 🔍 **RAG Search Logging**

**RAG collection searches are now tracked:**

```
🔍 Searching imperial_court_case_history collection for: 'Container MSKU0000001 shows duplicate...'
   📊 Found 3 results in imperial_court_case_history
🔍 Searching imperial_court_knowledge_base collection for: 'Container MSKU0000001 shows duplicate...'
   📊 Found 2 results in imperial_court_knowledge_base
```

## 🚀 How to Enable Detailed Logging

### Option 1: Default Loguru Logging (Already Active)

The system uses loguru by default. You'll see logs in your terminal when running the FastAPI server.

### Option 2: Enhanced Console Logging

Add this to your main application startup to see more detailed logs:

```python
from loguru import logger
import sys

# Remove default handler and add enhanced console logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    level="DEBUG"  # Set to INFO for less verbose, DEBUG for maximum detail
)
```

### Option 3: File Logging for Persistent Records

Add this to save agent steps to a file:

```python
logger.add(
    "logs/imperial_court_agents_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    rotation="1 day",
    retention="7 days"
)
```

## 📊 What You'll See in the Logs

### When an Incident is Processed:

1. **🏛️ Initial processing** - Incident received and validated
2. **🔍 RAG search** - Historical cases and knowledge base searched
3. **🤖 Agent assembly** - CrewAI agents created with database tools
4. **🛠️ Tool usage** - Each database query logged with results
5. **🧠 Agent reasoning** - Analysis, review, and decision steps
6. **✅ Completion** - Final results and summary

### When Database Tools are Used:

- **Tool invocation** with parameters
- **Execution status** (success/error)
- **Result summary** (data retrieved or error details)
- **Performance timing** (how long each query took)

### When CrewAI Agents Collaborate:

- **Agent initialization** with roles and capabilities
- **Task assignment** and requirements
- **Inter-agent communication** and data sharing
- **Decision progression** from analysis to final decree

## 🔧 Troubleshooting Logging

### If You Don't See Logs:

1. **Check log level**: Ensure it's set to INFO or DEBUG
2. **Verify output**: Make sure logs are going to console or file as expected
3. **Check mock mode**: In mock mode, you'll see simulation logs instead of real CrewAI logs

### If Logs are Too Verbose:

1. **Set level to INFO**: Reduces debug messages
2. **Filter by logger name**: Focus on specific components
3. **Use file logging**: Keep console clean, save details to file

### If You Want More Detail:

1. **Set level to DEBUG**: Maximum verbosity
2. **Add custom logging**: Insert additional logger.info() calls where needed
3. **Enable CrewAI verbose mode**: Already enabled (verbose=True)

## 🎯 Expected Log Flow for Incident Processing

```
🏛️ IMPERIAL COURT INCIDENT PROCESSING INITIATED
📋 Incident Text: Container MSKU0000001 shows duplicate...
🔍 Gathering RAG context from historical cases and knowledge base...
   🔍 Searching imperial_court_case_history collection...
   📊 Found 3 results in imperial_court_case_history
   🔍 Searching imperial_court_knowledge_base collection...
   📊 Found 2 results in imperial_court_knowledge_base
📚 RAG Context Retrieved - Cases: 3, KB: 2
🤖 Initiating CrewAI Agent Workflow...
👥 Assembling Imperial Court: 太和智君, 智文, 明鏡
🏗️ Creating specialized agents with database tool access...
📋 Creating specialized tasks with database investigation requirements...
🏛️ Assembling Imperial Court crew with agents and tasks...
🚀 INITIATING CREWAI WORKFLOW EXECUTION...
   📊 Strategic Analysis Agent (智文) will investigate incident using database tools
   🛠️ Agent tool invoked: get_operational_overview()
   ✅ Tool get_operational_overview completed successfully
   🛠️ Agent tool invoked: check_system_health()
   ✅ Tool check_system_health completed successfully
   🛠️ Agent tool invoked: get_container_details(MSKU0000001)
   ✅ Tool get_container_details completed successfully
   🔍 Policy Review Agent (明鏡) will validate analysis with database evidence
   🛠️ Agent tool invoked: check_system_health()
   ✅ Tool check_system_health completed successfully
   👑 Emperor (太和智君) will make final decision based on synthesized intelligence
✅ CREWAI WORKFLOW COMPLETED SUCCESSFULLY
📜 Final Result Length: 1247 characters
```

## 💡 Pro Tips

1. **Watch for tool usage patterns**: Agents should call database tools systematically
2. **Monitor error rates**: Tools returning errors indicate database connectivity issues
3. **Track decision progression**: Each agent should build on previous agent's work
4. **Verify evidence-based decisions**: Look for specific database citations in final decisions

**Your Imperial Court agents now provide full transparency into their decision-making process!** 🏛️👑
