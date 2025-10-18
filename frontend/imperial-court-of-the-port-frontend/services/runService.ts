import axios from "axios";
import type { Job, IncidentRequest } from "@/types/job";

const API_BASE = "http://localhost:8000"; // leave empty to use relative URLs or set to backend base if needed

/**
 * Start a new incident run. Expects the backend to return { run_id, status, ... }
 * Keep this small and focused (Single Responsibility Principle).
 */
export async function startRun(request: IncidentRequest): Promise<Job> {
  const url = `${API_BASE}/incident/run`;

  // Ensure the request has the required structure
  const payload: IncidentRequest = {
    incident_type: request.incident_type,
    severity: request.severity,
    payload: request.payload,
  };

  const resp = await axios.post(url, payload, {
    headers: {
      "Content-Type": "application/json",
    },
  });

  return resp.data as Job;
}

/**
 * Get the status of a run by id. Returns a Job object containing latest status.
 */
export async function getRun(run_id: string): Promise<Job> {
  const url = `${API_BASE}/incident/run/${encodeURIComponent(run_id)}`;
  const resp = await axios.get(url);
  return resp.data as Job;
}

/**
 * Get list of all jobs with optional limit.
 */
export async function getJobs(limit: number = 20): Promise<Job[]> {
  const url = `${API_BASE}/incident/jobs?limit=${limit}`;
  const resp = await axios.get(url);

  // The backend returns { jobs: [...] }
  return resp.data.jobs as Job[];
}

export default { startRun, getRun, getJobs };
