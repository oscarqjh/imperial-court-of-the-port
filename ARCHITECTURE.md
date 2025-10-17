# Architecture Overview

## System Design

The Imperial Court of the Port is an intelligent system for managing port incidents using a multi-agent AI architecture powered by CrewAI.

### Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Request                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Application                       │
│  ┌────────────┬─────────────┬────────────────────────┐     │
│  │ Root       │ Health      │ Analyze Incident       │     │
│  │ Endpoint   │ Check       │ Endpoint               │     │
│  └────────────┴─────────────┴────────────────────────┘     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              CrewAI Multi-Agent System                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Port Incident Crew                         │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │ 1. Port Incident Analyst                    │    │  │
│  │  │    - Analyzes incident details              │    │  │
│  │  │    - Assesses severity and impact           │    │  │
│  │  │    - Evaluates risk levels                  │    │  │
│  │  └─────────────────┬───────────────────────────┘    │  │
│  │                    │                                 │  │
│  │                    ▼                                 │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │ 2. Emergency Response Coordinator           │    │  │
│  │  │    - Develops response plans                │    │  │
│  │  │    - Identifies needed resources            │    │  │
│  │  │    - Coordinates multi-agency actions       │    │  │
│  │  └─────────────────┬───────────────────────────┘    │  │
│  │                    │                                 │  │
│  │                    ▼                                 │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │ 3. Port Safety Officer                      │    │  │
│  │  │    - Reviews safety protocols               │    │  │
│  │  │    - Recommends preventive measures         │    │  │
│  │  │    - Ensures compliance                     │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│          Comprehensive Analysis Result                      │
└─────────────────────────────────────────────────────────────┘
```

## Agent Roles and Responsibilities

### 1. Port Incident Analyst
**Primary Goal:** Analyze port incidents and assess their severity and impact

**Capabilities:**
- Incident classification
- Impact assessment on port operations
- Identification of immediate concerns
- Risk level evaluation

**Output:** Detailed incident analysis report

### 2. Emergency Response Coordinator
**Primary Goal:** Coordinate appropriate response actions for port incidents

**Capabilities:**
- Response action planning
- Resource allocation recommendations
- Multi-agency coordination
- Timeline development for response activities

**Output:** Comprehensive response coordination plan

### 3. Port Safety Officer
**Primary Goal:** Ensure safety protocols are followed and recommend preventive measures

**Capabilities:**
- Safety protocol compliance checking
- Preventive measure recommendations
- Safety assessment of response activities
- Long-term safety improvement suggestions

**Output:** Detailed safety assessment and recommendations

## Data Flow

1. **Request Reception:**
   - Client sends POST request to `/analyze-incident`
   - Request includes: description, severity, location

2. **Task Creation:**
   - CrewAI creates specialized tasks for each agent
   - Each task is configured with specific objectives

3. **Sequential Processing:**
   - Tasks are executed in sequence (Process.sequential)
   - Each agent builds upon the previous agent's analysis
   - Agents work collaboratively without delegation

4. **Result Aggregation:**
   - All agent outputs are combined
   - Comprehensive analysis is generated
   - Response is formatted and returned

## Technology Choices

### FastAPI
- **Why:** Modern, fast, async-capable framework
- **Benefits:** 
  - Automatic API documentation
  - Type validation with Pydantic
  - High performance
  - Easy to learn and use

### CrewAI
- **Why:** Specialized for multi-agent AI orchestration
- **Benefits:**
  - Simple agent definition
  - Built-in task coordination
  - Process management
  - Integration with LLMs

### Pydantic
- **Why:** Data validation and settings management
- **Benefits:**
  - Type safety
  - Automatic validation
  - Clear error messages
  - Serialization support

## API Endpoints

### GET `/`
Returns API information and available endpoints

### GET `/health`
Health check endpoint for monitoring

### POST `/analyze-incident`
Main endpoint for incident analysis

**Request Body:**
```json
{
  "description": "string",
  "severity": "low|medium|high|critical",
  "location": "string (optional)"
}
```

**Response:**
```json
{
  "status": "success",
  "result": "Comprehensive analysis from agents",
  "incident_id": "INC-XXXX"
}
```

## Environment Configuration

Required environment variables:
- `OPENAI_API_KEY`: API key for CrewAI agents (required)
- `OPENAI_MODEL_NAME`: Model to use (optional, default: gpt-4)
- `PORT`: Server port (optional, default: 8000)
- `HOST`: Server host (optional, default: 0.0.0.0)

## Extensibility

The system can be easily extended:

1. **Add New Agents:**
   - Define new agent roles in `crew.py`
   - Add them to the crew configuration

2. **Add New Endpoints:**
   - Define new routes in `main.py`
   - Create corresponding crew methods

3. **Customize Agent Behavior:**
   - Modify agent backstories and goals
   - Adjust task descriptions
   - Change process type (sequential vs. hierarchical)

4. **Add Middleware:**
   - Authentication
   - Rate limiting
   - Logging
   - Caching

## Performance Considerations

- **Async Operations:** FastAPI runs asynchronously for better performance
- **Sequential Processing:** Agents run sequentially to build upon each other's work
- **Stateless Design:** Each request is independent
- **Scalability:** Can be deployed with multiple workers using uvicorn or gunicorn

## Security Considerations

- Store API keys in environment variables (never in code)
- Use `.gitignore` to exclude `.env` files
- Validate all input data with Pydantic models
- Consider adding authentication for production use
- Rate limit the API to prevent abuse

## Future Enhancements

Potential areas for improvement:
1. Add database for incident history
2. Implement user authentication
3. Add real-time notifications
4. Create a web dashboard
5. Integrate with external port systems
6. Add monitoring and logging
7. Implement caching for repeated queries
8. Add support for multiple languages
