# imperial-court-of-the-port

An agentic AI system to manage and escalate port incidents using a small multi-agent "court" that analyzes incidents, consults knowledge, and produces a human-ready escalation summary.

This README gives a concise developer and operator guide: quick setup, the main features, how to call important endpoints (PowerShell + curl examples), and where to look in the code.

## Quickstart (Windows PowerShell)

1. Create a virtualenv and install dependencies:

```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Set environment variables (create a `.env` file or set them in your shell). Minimum required variables:

```
OPENAI_API_KEY = 'sk-...'
QDRANT_URL = 'https://YOUR-CLUSTER-URL'
QDRANT_API_KEY = 'YOUR_QDRANT_API_KEY'
QDRANT_COLLECTION = 'imperial_court_kb'
SUPABASE_DB_URL = 'postgresql+asyncpg://USER:PASS@HOST:PORT/DB'
DB_SSL_ALLOW_SELF_SIGNED=true
CREWAI_TRACING_ENABLED=true
EMBED_MODEL=text-embedding-3-small
MOCK_MODE=false
CREWAI_TRACING_ENABLED=true
CELERY_BROKER_URL=redis://default:7VbDua.....
```

3. Start Celery server:

```powershell
python start_celery_worker.py
```

3. Run the server (development):

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

If you prefer curl on the same machine use the equivalent command in PowerShell or a Linux/macOS terminal.

## Features

- Multi-agent incident analysis: a "court" of specialist agents analyzes an incoming incident in phases (intelligence, technical, business, comms, strategy, validation).
- Historical-solution synthesis: a dedicated Solution Archivist agent reads RAG results (case history + knowledge base) and writes a "HISTORICAL SOLUTION ANALYSIS" section.
- Safe escalation: a dedicated Escalation Manager agent builds the final, human-ready escalation summary and selects real contacts from `app/data/contacts.json` (no invented contacts). The escalation path (steps) is taken from the contacts file.
- RAG support: chunking, embeddings, and Qdrant-backed search for contextual grounding and case history retrieval.
- Extensible tools: agents can consult DB helpers and other local utilities when needed; the orchestration is in `app/orchestrator.py`.

## Important endpoints

All endpoints are mounted in the FastAPI app (see `app/main.py`). Below are the most-used endpoints and examples showing how to call them.

1. Health check

GET /health

Response example:

```json
{ "status": "ok" }
```

PowerShell:

```powershell
Invoke-RestMethod -Uri http://localhost:8000/health -Method Get
```

curl:

```bash
curl http://localhost:8000/health
```

2. Run an incident analysis + escalation flow

POST /incident/run

Request body JSON fields:

- incident_type: string (e.g. "container_conflict", "network_outage")
- severity: string (e.g. "low", "medium", "high")
- payload: object (arbitrary incident payload; may include logs, IDs, timestamps)

PowerShell example (Invoke-RestMethod):

```powershell
$body = @{
    incident_type = 'container_conflict'
    severity = 'high'
    payload = @{ incident_id = 'INC-20231003-103000'; notes = 'Duplicate container allocation' }
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Uri http://localhost:8000/incident/run -Method Post -Body $body -ContentType 'application/json'
```

curl example:

```bash
curl -X POST http://localhost:8000/incident/run \
  -H "Content-Type: application/json" \
  -d '{"incident_type":"container_conflict","severity":"high","payload":{"incident_id":"INC-20231003-103000","notes":"Duplicate container allocation"}}'
```

What to expect in the response:

- The system runs a multi-agent workflow and returns a structured result string in the `crew_output` field (it typically contains the full escalation summary). The Escalation Manager includes a formatted escalation summary with:
  - incident id / metadata
  - incident type & severity
  - primary contact (selected from `app/data/contacts.json`)
  - HISTORICAL SOLUTION ANALYSIS (synthesized from RAG case_history)
  - ESCALATION PATH (the exact steps listed in contacts.json)

Note: some consumers/tests may look for a top-level `escalation_summary` field — if you don't see it, read `crew_output` which always contains the agent-produced summary.

3. RAG (Retrieval-Augmented Generation) endpoints

- POST /rag/ingest (upload DOCX and create embeddings)
- POST /rag/ingest_parsed (upload a plain text file for ingestion)
- POST /rag/search (search the vector DB)

Example: search the KB

PowerShell:

```powershell
$q = @{ query = 'What is the response to a crane failure?'; top_k = 5 } | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:8000/rag/search -Method Post -Body $q -ContentType 'application/json'
```

curl:

```bash
curl -X POST http://localhost:8000/rag/search \
  -H "Content-Type: application/json" \
  -d '{"query":"What is the response to a crane failure?","top_k":5}'
```

Typical response shape:

{
"results": [ { "id": "chunk-abc123", "score": 0.92, "text": "..." }, ... ]
}

4. Ingesting documents

Use the `/rag/ingest` and `/rag/ingest_parsed` endpoints to add knowledge base documents. The ingestion pipeline performs tokenizer-aware chunking (~400 tokens per chunk, ~60 token overlap) and pushes 1536-d vectors to Qdrant (OpenAI embeddings).

## Agents and where to look in code

- Orchestration: `app/orchestrator.py` — builds the Crew, creates agent roles/tasks, runs the multi-phase workflow, and returns the final output.
- API wiring: `app/main.py` and `app/router_rag.py` — FastAPI endpoints.
- RAG helpers: `app/rag_chunking.py`, `app/rag_embeddings.py`, `app/rag_qdrant.py`, `app/rag_ingest.py`.
- Tools & DB: `app/db.py`, `app/agents_db.py`, `app/agent_tools.py`.
- Contacts and escalation policy: `app/data/contacts.json` — the Escalation Manager uses this file to pick primary contacts and the escalation_steps array for the ESCALATION PATH.

Key agent behaviors (high-level):

- Solution Archivist (史官): reads `rag_context['case_history']` and `rag_context['knowledge_base']` and produces a HISTORICAL SOLUTION ANALYSIS section.
- Escalation Manager (朝廷): composes the final escalation summary and selects real contacts from `app/data/contacts.json`. It must not invent contacts and must list the escalation_steps verbatim.

## Example of a (truncated) agent-produced escalation summary

INCIDENT ESCALATION SUMMARY

- Incident ID: INC-20231003-103000
- Incident Type: Container Conflict
- Severity: High
- Primary Contact: Mark Lee (mark.lee@psa123.com)

HISTORICAL SOLUTION ANALYSIS:

- Prior incidents: CNTR-202309... — resolution: reassign container, notify berth ops, reconcile inventory in 24–72 hours.

ESCALATION PATH:

1. Notify Product Duty immediately.
2. If unresolved in 2 hours, escalate to Manager on-call (Mark Lee).
3. Engage SRE/Infra team if systems are implicated.

The full `crew_output` contains more detailed diagnostics, recommended steps, and timings.

## Troubleshooting & tips

- If you see connectivity errors:
  - Verify `QDRANT_URL` and `QDRANT_API_KEY`.
  - Confirm `SUPABASE_DB_URL` uses the pooled port for `asyncpg` (e.g. 6543) and is reachable from your machine.
- If embeddings/search return empty results, check your `QDRANT_COLLECTION` and that documents were successfully ingested.
- Tests: a quick verification is to run the example workflow test in the repo:

```powershell
.venv\Scripts\python.exe test_enhanced_workflow.py
```

## Developer notes

- Add new contacts or change escalation steps in `app/data/contacts.json`. The Escalation Manager will use this file directly.
- To add new agent behavior, modify `app/orchestrator.py` and the agent's instruction/backstory there.
- Keep the agent output contract in mind: `crew_output` contains the agent-produced text. If your consumer code expects a dedicated `escalation_summary` field, adapt the consumer or update `app/orchestrator.py` to populate that field explicitly.

## Files of interest

- `app/main.py` — FastAPI app and routes.
- `app/orchestrator.py` — multi-agent orchestration and task setup.
- `app/data/contacts.json` — canonical contacts and escalation steps.
- `app/rag_*` — ingestion, chunking, embeddings, and Qdrant wrapper.

If you'd like, I can also add a small example script (Python) that calls `/incident/run`, waits for the response, and extracts the primary contact and historical solution section automatically. Tell me which format you prefer (PowerShell, Python, or Node.js) and I will add it.

## Background jobs (Celery + Redis)

The `/incident/run` endpoint now submits incident analysis jobs to a background queue (Celery) and immediately returns a `run_id` (the Celery task id). This lets the frontend submit work without blocking and poll for progress using the `run_id`.

Key points

- `POST /incident/run` returns JSON with the Celery `run_id` (task id). Save this id in the frontend to poll status.
- `GET /incident/run/{run_id}` returns a status object with:
  - `status`: one of `pending`, `processing`/`started`, `success`, or `failure`.
  - `progress`: integer percent (0-100) estimated by the orchestrator.
  - `current_step`: short string describing the current phase (e.g. "Gathering RAG context", "Executing CrewAI workflow").
  - `result`: present when status is `success` — the task return value (includes `crew_output`, `rag_results`, etc.).

Starting the server and the worker (PowerShell)

1. Start the FastAPI server (development):

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

2. Start a Celery worker (use the same environment variables as the server so Celery can reach Redis/Qdrant/etc). Replace the broker/backend URL in `app/celery_config.py` or set `CELERY_BROKER_URL` / `CELERY_RESULT_BACKEND` in your environment.

```powershell
# from the repo root, with your venv activated
celery -A app.celery_tasks worker --loglevel=info --concurrency=2
```

Notes on Redis and configuration

- The project uses Redis as the Celery broker and result backend. If you use a hosted Redis (Redis Cloud), use the full connection string (including password) in `app/celery_config.py` or export it to `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND`.
- If Redis previously contained corrupted task metadata (worker crashes with ValueError about exception info), flush the Redis DB used by Celery (careful: this removes all data in that Redis instance). Only do this for development/test instances.

Polling example (PowerShell)

After you receive a `run_id` from `POST /incident/run`, poll like this:

```powershell
$runId = 'the-task-id-from-post'
while ($true) {
    $status = Invoke-RestMethod -Uri "http://localhost:8000/incident/run/$runId" -Method Get
    Write-Host "Status: $($status.status) - $($status.progress)% - $($status.current_step)"
    if ($status.status -eq 'success' -or $status.status -eq 'failure') { break }
    Start-Sleep -Seconds 2
}
```

Quick curl example:

```bash
RUN_ID=the-task-id-from-post
while true; do
  curl -s http://localhost:8000/incident/run/$RUN_ID | jq -r '.status,.progress,.current_step'
  sleep 2
done
```

Test scripts

- `debug_progress.py` — submits a job and polls until complete, printing progress updates.
- `test_persistence.py` — useful to verify that `run_id` persists across server reloads (uvicorn --reload) because task state is stored in Redis/Celery.
- `simple_test.py` — minimal example that posts a job and prints the final `crew_output`.

Troubleshooting

- If you see `404` when polling a `run_id`, ensure the Celery worker is running and the `run_id` you received is the Celery task id returned by the POST call. Uvicorn reload will clear any in-memory job store — using Celery task ids avoids that problem.
- If workers crash on startup or when updating task metadata, check Redis for corrupted entries. For development you can flush the DB with `redis-cli FLUSHDB` (or the equivalent command in your hosted Redis console).
- If you need finer-grained per-agent visibility inside CrewAI, note that CrewAI's `crew.kickoff()` is an internal execution step. The repo includes extra progress callbacks during agent creation and pre/post kickoff phases to make progress more informative, but precise live per-agent step reporting may require instrumenting or running agents under explicit orchestration.

If you'd like, I can add a small example Python script that calls `/incident/run`, waits, and extracts the primary contact and historical solution sections from `crew_output`.
