"use client"

import { useCallback, useEffect, useRef, useState } from 'react'
import type { Job, JobFile } from '@/types/job'
import runService from '@/services/runService'

type StartRunOptions = {
  // payload shape expected by backend (files handled elsewhere)
  payload: any
  label?: string
}

/**
 * useRunManager
 * - Responsible for starting runs and polling their status until completion.
 * - Keeps a list of jobs and exposes actions to start and refresh.
 * - Each running job is polled every 5s until status becomes completed/failed.
 *
 * SOLID notes:
 * - Single Responsibility: hook only manages run lifecycle and state.
 * - Open/Closed: behaviors can be extended via callbacks and options.
 */
export function useRunManager() {
  const [jobs, setJobs] = useState<Job[]>([])

  // Keep timers in ref so we can clear later
  const timers = useRef<Record<string, number>>({})

  useEffect(() => {
    return () => {
      // cleanup timers on unmount
      Object.values(timers.current).forEach((id) => window.clearInterval(id))
    }
  }, [])

  const addOrUpdateJob = useCallback((job: Job) => {
    setJobs((prev) => {
      const idx = prev.findIndex((j) => j.run_id === job.run_id)
      if (idx === -1) return [job, ...prev]
      const copy = [...prev]
      copy[idx] = { ...copy[idx], ...job }
      return copy
    })
  }, [])

  const pollJob = useCallback((run_id: string) => {
    // avoid double timers
    if (timers.current[run_id]) return

    const id = window.setInterval(async () => {
      try {
        const updated = await runService.getRun(run_id)
        addOrUpdateJob(updated)

        if (updated.status === 'completed' || updated.status === 'failed') {
          window.clearInterval(id)
          delete timers.current[run_id]
        }
      } catch (err) {
        // on error, mark job as unknown and stop polling after some tries
        addOrUpdateJob({ run_id, status: 'unknown', created_at: new Date().toISOString(), input_files: [] })
        window.clearInterval(id)
        delete timers.current[run_id]
      }
    }, 5000)

    timers.current[run_id] = id
  }, [addOrUpdateJob])

  const startRun = useCallback(async ({ payload, label }: StartRunOptions) => {
    // start run via service
    const job = await runService.startRun(payload)
    const normalized: Job = {
      run_id: job.run_id,
      status: job.status,
      created_at: job.created_at || new Date().toISOString(),
      input_files: (job.input_files || []) as JobFile[],
      result: job.result,
      label: label,
    }
    addOrUpdateJob(normalized)

    // if not finished, start polling
    if (normalized.status !== 'completed' && normalized.status !== 'failed') {
      pollJob(normalized.run_id)
    }

    return normalized
  }, [addOrUpdateJob, pollJob])

  const refreshAll = useCallback(() => {
    jobs.forEach((j) => {
      if (j.status !== 'completed' && j.status !== 'failed') pollJob(j.run_id)
    })
  }, [jobs, pollJob])

  const stopPolling = useCallback((run_id: string) => {
    const t = timers.current[run_id]
    if (t) {
      window.clearInterval(t)
      delete timers.current[run_id]
    }
  }, [])

  return {
    jobs,
    startRun,
    refreshAll,
    stopPolling,
    setJobs,
  }
}

export default useRunManager
