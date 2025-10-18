# Background Job System API Documentation

## Overview

The Imperial Court incident processing system now supports background job execution. Instead of waiting for long-running incident analysis to complete, you can submit jobs and poll for their status.

## API Endpoints

### Submit Incident for Background Processing

**POST** `/incident/run`

Submit an incident for background processing and receive a `run_id` immediately.

**Request:**

```bash
curl -X POST http://localhost:8001/incident/run \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "incident_text=Container MSKU1234567 is missing from terminal"
```

**Response:**

```json
{
  "run_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "queued",
  "created_at": "2025-10-18T10:30:00.123456Z",
  "started_at": null,
  "completed_at": null,
  "result": null,
  "error": null
}
```

### Check Job Status

**GET** `/incident/run/{run_id}`

Get the current status and results of a background job.

**Request:**

```bash
curl http://localhost:8001/incident/run/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Response (Completed):**

```json
{
  "run_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "completed",
  "created_at": "2025-10-18T10:30:00.123456Z",
  "started_at": "2025-10-18T10:30:01.234567Z",
  "completed_at": "2025-10-18T10:30:45.678901Z",
  "result": {
    "incident_analysis": {
      "incident_type": "Container Management",
      "severity": "Medium",
      "recommendations": [...]
    }
  },
  "error": null
}
```

### List All Jobs

**GET** `/incident/jobs?limit=20`

List recent jobs with their status.

**Request:**

```bash
curl http://localhost:8001/incident/jobs?limit=10
```

**Response:**

```json
{
  "jobs": [
    {
      "run_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "status": "completed",
      "created_at": "2025-10-18T10:30:00.123456Z",
      "started_at": "2025-10-18T10:30:01.234567Z",
      "completed_at": "2025-10-18T10:30:45.678901Z",
      "result": {...},
      "error": null
    }
  ]
}
```

### Clean Up Old Jobs

**POST** `/incident/cleanup?max_age_hours=24`

Remove completed/failed jobs older than the specified age.

**Request:**

```bash
curl -X POST http://localhost:8001/incident/cleanup?max_age_hours=24
```

**Response:**

```json
{
  "message": "Cleaned up 5 old jobs",
  "remaining_jobs": 3
}
```

## Job Status Values

- **`queued`** - Job has been submitted and is waiting to start
- **`running`** - Job is currently being processed
- **`completed`** - Job finished successfully, results available
- **`failed`** - Job failed due to an error

## Frontend Integration Example

Here's how you might integrate this into a frontend application:

```javascript
// Submit an incident
async function submitIncident(incidentText) {
  const formData = new FormData();
  formData.append("incident_text", incidentText);

  const response = await fetch("/incident/run", {
    method: "POST",
    body: formData,
  });

  const job = await response.json();
  return job.run_id;
}

// Poll for job completion
async function pollJobStatus(runId, onUpdate) {
  while (true) {
    const response = await fetch(`/incident/run/${runId}`);
    const job = await response.json();

    onUpdate(job);

    if (job.status === "completed" || job.status === "failed") {
      return job;
    }

    // Wait 2 seconds before next poll
    await new Promise((resolve) => setTimeout(resolve, 2000));
  }
}

// Usage
const runId = await submitIncident("Container issue...");
const finalJob = await pollJobStatus(runId, (job) => {
  console.log(`Job ${job.status}...`);
});

if (finalJob.status === "completed") {
  console.log("Results:", finalJob.result);
} else {
  console.error("Job failed:", finalJob.error);
}
```

## PowerShell Examples

```powershell
# Submit job
$response = Invoke-RestMethod -Uri "http://localhost:8001/incident/run" -Method POST -Body @{incident_text="Test incident"}
$runId = $response.run_id

# Poll status
do {
    $status = Invoke-RestMethod -Uri "http://localhost:8001/incident/run/$runId"
    Write-Host "Status: $($status.status)"
    Start-Sleep -Seconds 2
} while ($status.status -in @("queued", "running"))

# Show results
if ($status.status -eq "completed") {
    $status.result | ConvertTo-Json -Depth 10
}
```
