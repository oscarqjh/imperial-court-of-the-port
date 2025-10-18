"use client"

import React from 'react'
import type { Job } from '@/types/job'
import { Button } from './ui/button'
import { FileText } from 'lucide-react'

type Props = {
  job: Job
  onRefresh?: (run_id: string) => void
}

/**
 * JobRow - responsible for rendering a single job's information.
 * Keeps UI rendering concerns isolated from data management.
 */
export function JobRow({ job, onRefresh }: Props) {
  return (
    <tr className="border-b last:border-b-0">
      <td className="px-4 py-2 text-sm font-medium">{job.label || job.run_id}</td>
      <td className="px-4 py-2 text-sm">{new Date(job.created_at).toLocaleString()}</td>
      <td className="px-4 py-2 text-sm">{job.status}</td>
      <td className="px-4 py-2 text-sm">
        <div className="flex gap-2 flex-wrap">
          {job.input_files.map((f) => (
            <div key={f.id} className="flex items-center gap-1 text-xs bg-muted rounded px-2 py-1">
              <FileText className="h-3 w-3" />
              <span className="max-w-[140px] truncate">{f.name}</span>
            </div>
          ))}
        </div>
      </td>
      <td className="px-4 py-2 text-sm">
        {job.result?.output_file ? (
          <a className="text-primary underline" href={job.result.output_file} target="_blank" rel="noreferrer">Download</a>
        ) : (
          <span className="text-muted-foreground text-xs">—</span>
        )}
      </td>
      <td className="px-4 py-2 text-sm">
        <div className="flex gap-2">
          <Button size="sm" variant="outline" onClick={() => onRefresh?.(job.run_id)}>Refresh</Button>
        </div>
      </td>
    </tr>
  )
}

export default JobRow
