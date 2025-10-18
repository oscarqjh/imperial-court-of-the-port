export type RunStatus = 'pending' | 'running' | 'completed' | 'failed' | 'unknown'

export interface JobFile {
  id: string
  name: string
  size?: number
  type?: string
}

export interface JobResult {
  output_file?: string // URL or path to output file when available
  result?: any
}

export interface Job {
  run_id: string
  status: RunStatus
  created_at: string // ISO timestamp
  input_files: JobFile[]
  result?: JobResult
  // optional metadata to show in UI
  label?: string
}
