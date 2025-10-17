# Imperial Court of the Port

An agentic AI system to manage port incidents using FastAPI and CrewAI.

## Overview

This application provides an intelligent system for analyzing and managing port incidents using AI agents powered by CrewAI. The system coordinates multiple specialized agents to provide comprehensive incident analysis, response coordination, and safety recommendations.

## Features

- **FastAPI Backend**: Modern, fast, and async-capable REST API
- **CrewAI Integration**: Multi-agent system with specialized roles:
  - Port Incident Analyst: Analyzes incidents and assesses severity
  - Emergency Response Coordinator: Develops response plans
  - Port Safety Officer: Ensures safety protocols and provides recommendations
- **RESTful API**: Simple endpoints for incident analysis
- **Interactive Documentation**: Auto-generated API docs at `/docs`

## Requirements

- Python 3.8+
- OpenAI API key (for CrewAI agents)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/oscarqjh/imperial-court-of-the-port.git
cd imperial-court-of-the-port
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

### Running the Server

Start the FastAPI server:
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

### API Endpoints

- **GET /**: Root endpoint with API information
- **GET /health**: Health check endpoint
- **GET /docs**: Interactive API documentation (Swagger UI)
- **POST /analyze-incident**: Analyze a port incident

### Example Request

```bash
curl -X POST "http://localhost:8000/analyze-incident" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Container crane malfunction at Terminal 3",
    "severity": "high",
    "location": "Terminal 3, Berth 5"
  }'
```

### Example Response

```json
{
  "status": "success",
  "result": "Detailed analysis from AI agents...",
  "incident_id": "INC-1234"
}
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Architecture

The system uses a multi-agent architecture:

1. **FastAPI Application** (`main.py`): Handles HTTP requests and responses
2. **CrewAI Crew** (`crew.py`): Orchestrates AI agents for incident analysis
3. **Specialized Agents**: Each agent has a specific role and expertise

## Development

### Project Structure

```
imperial-court-of-the-port/
├── main.py              # FastAPI application
├── crew.py              # CrewAI agent definitions
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

### Adding New Features

- To add new agents, modify `crew.py`
- To add new endpoints, modify `main.py`
- To add new dependencies, update `requirements.txt`

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
