"use client"

import React, { useMemo, useState } from 'react'
import useRunManager from '@/hooks/useRunManager'
import JobRow from './job-row'
import { Button } from './ui/button'
import type { UploadedFile } from '@/types/chat-interface'

/**
 * JobDashboard - High-level component that shows all jobs and their statuses.
 * - Delegates job lifecycle to useRunManager (SRP)
 * - UI-only behaviors kept local
 */
export function JobDashboard() {
  const { jobs, startRun, refreshAll } = useRunManager()
  const [uploadFiles, setUploadFiles] = useState<UploadedFile[]>([])
  const [label, setLabel] = useState('')

  const canStart = useMemo(() => true, [])

  const handleStart = async () => {
    // Build payload: if files present, backend must accept them via FormData elsewhere.
    const payload: any = {
      // example fields — adapt to your backend API
      incident_type: 'USER_UPLOAD',
      payload: { label },
      // Note: files should be attached via FormData in the actual startRun implementation if needed
      input_files: uploadFiles.map((f) => ({ id: f.id, name: f.name }))
    }

    const j = await startRun({ payload, label })
    console.log('started job', j)
  }

  return (
    <div className="p-4">
      <div className="flex items-center justify-between gap-4 mb-4">
        <h2 className="text-lg font-semibold">Jobs Dashboard</h2>
        <div className="flex gap-2">
          <Button onClick={() => refreshAll()} variant="ghost" size="sm">Refresh All</Button>
        </div>
      </div>

      <div className="mb-4 flex gap-2">
        <input className="input rounded px-3 py-2" placeholder="Label (optional)" value={label} onChange={(e) => setLabel(e.target.value)} />
        <Button onClick={handleStart} disabled={!canStart}>Start Job</Button>
      </div>

      <div className="overflow-auto rounded-lg border">
        <table className="w-full table-fixed">
          <thead className="bg-muted">
            <tr>
              <th className="text-left px-4 py-2">Run ID</th>
              <th className="text-left px-4 py-2">Created</th>
              <th className="text-left px-4 py-2">Status</th>
              <th className="text-left px-4 py-2">Input Files</th>
              <th className="text-left px-4 py-2">Output</th>
              <th className="text-left px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {jobs.map((job) => (
              <JobRow key={job.run_id} job={job} onRefresh={(id) => { /* could call runService.getRun and update manually */ }} />
            ))}
            {jobs.length === 0 && (
              <tr>
                <td colSpan={6} className="p-6 text-center text-sm text-muted-foreground">No jobs yet</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default JobDashboard
