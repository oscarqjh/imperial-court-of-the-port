/**
 * Example of how to use the updated runService with proper typing
 */

import { startRun, getRun } from "@/services/runService";
import type { IncidentRequest } from "@/types/job";

// Example 1: Start a new incident run
export async function submitIncident() {
  try {
    const incidentRequest: IncidentRequest = {
      incident_type: "container_conflict",
      severity: "high",
      payload: {
        incident_id: "INC-20231003-103000",
        notes: "Duplicate container allocation",
        affected_systems: ["container_management", "berth_allocation"],
        timestamp: new Date().toISOString(),
      },
    };

    const job = await startRun(incidentRequest);
    console.log("✅ Incident submitted successfully:", job.run_id);

    return job;
  } catch (error) {
    console.error("❌ Failed to submit incident:", error);
    throw error;
  }
}

// Example 2: Poll for job status with progress updates
export async function pollJobStatus(
  runId: string,
  onProgress?: (job: any) => void
) {
  try {
    const job = await getRun(runId);

    // Call progress callback if provided
    if (onProgress) {
      onProgress(job);
    }

    console.log(
      `📊 Job ${runId}: ${job.status} (${job.progress || 0}%) - ${
        job.current_step || "Unknown"
      }`
    );

    return job;
  } catch (error) {
    console.error("❌ Failed to get job status:", error);
    throw error;
  }
}

// Example 3: Complete polling workflow
export async function runIncidentWorkflow() {
  try {
    // Step 1: Submit incident
    const job = await submitIncident();

    // Step 2: Poll until complete
    let finalJob = job;
    while (finalJob.status === "pending" || finalJob.status === "processing") {
      // Wait 2 seconds before next poll
      await new Promise((resolve) => setTimeout(resolve, 2000));

      // Get updated status
      finalJob = await pollJobStatus(job.run_id, (job) => {
        console.log(`Progress: ${job.progress}% - ${job.current_step}`);
      });
    }

    // Step 3: Handle final result
    if (finalJob.status === "success") {
      console.log("🎉 Incident analysis completed successfully!");
      console.log("Result:", finalJob.result);
    } else if (finalJob.status === "failure") {
      console.error("💥 Incident analysis failed:", finalJob.error);
    }

    return finalJob;
  } catch (error) {
    console.error("❌ Workflow failed:", error);
    throw error;
  }
}
