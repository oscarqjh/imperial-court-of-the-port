"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import type { Job, IncidentRequest } from "@/types/job";
import runService from "@/services/runService";

/**
 * Map backend status values to frontend status values
 */
function mapBackendStatusToFrontend(backendStatus: string): Job["status"] {
  switch (backendStatus) {
    case "queued":
      return "pending";
    case "processing":
      return "processing";
    case "completed":
      return "success";
    case "failed":
      return "failure";
    default:
      return "unknown";
  }
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
  const [jobs, setJobs] = useState<Job[]>([]);

  // Keep timers in ref so we can clear later
  const timers = useRef<Record<string, number>>({});

  useEffect(() => {
    return () => {
      // cleanup timers on unmount
      Object.values(timers.current).forEach((id) => window.clearInterval(id));
    };
  }, []);

  const addOrUpdateJob = useCallback((job: Job) => {
    setJobs((prev) => {
      const idx = prev.findIndex((j) => j.run_id === job.run_id);
      if (idx === -1) return [job, ...prev];
      const copy = [...prev];
      copy[idx] = { ...copy[idx], ...job };
      return copy;
    });
  }, []);

  const pollJob = useCallback(
    (run_id: string) => {
      // avoid double timers
      if (timers.current[run_id]) return;

      const id = window.setInterval(async () => {
        try {
          const updated = await runService.getRun(run_id);
          // Map backend status to frontend status
          const normalizedJob: Job = {
            ...updated,
            status: mapBackendStatusToFrontend(updated.status as string),
          };
          addOrUpdateJob(normalizedJob);

          if (
            normalizedJob.status === "success" ||
            normalizedJob.status === "failure"
          ) {
            window.clearInterval(id);
            delete timers.current[run_id];
          }
        } catch (err) {
          console.error(`Error polling job ${run_id}:`, err);
          // on error, mark job as unknown and stop polling after some tries
          addOrUpdateJob({
            run_id,
            status: "unknown",
            created_at: new Date().toISOString(),
          });
          window.clearInterval(id);
          delete timers.current[run_id];
        }
      }, 5000);

      timers.current[run_id] = id;
    },
    [addOrUpdateJob]
  );

  const startRun = useCallback(
    async (request: IncidentRequest, label?: string) => {
      // start run via service
      const job = await runService.startRun(request);
      const normalized: Job = {
        ...job,
        status: mapBackendStatusToFrontend(job.status as string),
        label: label,
      };
      addOrUpdateJob(normalized);

      // if not finished, start polling
      if (normalized.status !== "success" && normalized.status !== "failure") {
        pollJob(normalized.run_id);
      }

      return normalized;
    },
    [addOrUpdateJob, pollJob]
  );

  const loadJobs = useCallback(
    async (limit: number = 20) => {
      try {
        console.log("📋 Loading jobs from backend...");
        const loadedJobs = await runService.getJobs(limit);

        console.log("📊 Loaded jobs data:", loadedJobs);

        if (Array.isArray(loadedJobs)) {
          // Convert backend status to frontend status
          const normalizedJobs: Job[] = loadedJobs.map((jobData: any) => ({
            run_id: jobData.run_id,
            status: mapBackendStatusToFrontend(jobData.status),
            created_at: jobData.created_at,
            started_at: jobData.started_at,
            completed_at: jobData.completed_at,
            result: jobData.result,
            error: jobData.error,
            progress: jobData.progress,
            current_step: jobData.current_step,
          }));

          console.log(`✅ Loaded ${normalizedJobs.length} jobs from backend`);
          setJobs(normalizedJobs);

          // Start polling for any active jobs
          normalizedJobs.forEach((job) => {
            if (job.status === "pending" || job.status === "processing") {
              pollJob(job.run_id);
            }
          });

          return normalizedJobs;
        } else {
          console.warn("❌ Invalid jobs response format:", loadedJobs);
          return [];
        }
      } catch (error) {
        console.error("❌ Error loading jobs:", error);
        throw error; // Re-throw so components can handle the error
      }
    },
    [pollJob]
  );

  const refreshAll = useCallback(async () => {
    // Reload all jobs from backend instead of just polling existing ones
    await loadJobs();
  }, [loadJobs]);

  const stopPolling = useCallback((run_id: string) => {
    const t = timers.current[run_id];
    if (t) {
      window.clearInterval(t);
      delete timers.current[run_id];
    }
  }, []);

  return {
    jobs,
    startRun,
    loadJobs,
    refreshAll,
    stopPolling,
    setJobs,
  };
}

export default useRunManager;
