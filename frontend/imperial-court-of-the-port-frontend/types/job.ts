export type RunStatus =
  | "pending"
  | "processing"
  | "success"
  | "failure"
  | "unknown";

export interface IncidentRequest {
  incident_type: string;
  severity: string;
  payload: Record<string, any>;
}

export interface JobFile {
  id: string;
  name: string;
  size?: number;
  type?: string;
}

export interface JobResult {
  output_file?: string; // URL or path to output file when available
  result?: any;
}

export interface Job {
  run_id: string;
  status: RunStatus;
  created_at: string; // ISO timestamp
  started_at?: string | null;
  completed_at?: string | null;
  result?: any;
  error?: string | null;
  progress?: number | null;
  current_step?: string | null;
  // optional metadata to show in UI
  label?: string;
}
