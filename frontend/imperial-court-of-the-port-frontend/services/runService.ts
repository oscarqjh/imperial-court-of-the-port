import axios from 'axios'
import type { Job } from '@/types/job'

const API_BASE = '' // leave empty to use relative URLs or set to backend base if needed

/**
 * Start a new incident run. Expects the backend to return { run_id, status, ... }
 * Keep this small and focused (Single Responsibility Principle).
 */
export async function startRun(payload: any): Promise<Job> {
  const url = `${API_BASE}/incident/run`
  const resp = await axios.post(url, payload)
  return resp.data as Job
}

/**
 * Get the status of a run by id. Returns a Job object containing latest status.
 */
export async function getRun(run_id: string): Promise<Job> {
  const url = `${API_BASE}/incident/run/${encodeURIComponent(run_id)}`
  const resp = await axios.get(url)
  return resp.data as Job
}

export default { startRun, getRun }
