"use client";

import React, { useEffect, useState } from "react";
import useRunManager from "@/hooks/useRunManager";
import JobRow from "./job-row";
import { Button } from "./ui/button";
import Link from "next/link";
import { ChatHeader } from "./chat-header";

/**
 * JobDashboard - Shows all submitted jobs and their statuses.
 * - Auto-refreshes every 5 seconds via useRunManager
 * - Displays real-time progress and status updates
 * - Provides navigation back to incident submission
 */
export function JobDashboard() {
  const { jobs, loadJobs, refreshAll } = useRunManager();
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);

  // Load jobs on mount
  useEffect(() => {
    const initialLoad = async () => {
      try {
        setIsLoading(true);
        setLoadError(null);
        await loadJobs(50); // Load more jobs for dashboard view
      } catch (error) {
        setLoadError(
          error instanceof Error ? error.message : "Failed to load jobs"
        );
      } finally {
        setIsLoading(false);
      }
    };

    initialLoad();
  }, [loadJobs]);

  // Auto-refresh every 5 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      refreshAll();
    }, 5000);

    return () => clearInterval(interval);
  }, [refreshAll]);

  const handleManualRefresh = async () => {
    try {
      setLoadError(null);
      await refreshAll();
    } catch (error) {
      setLoadError(
        error instanceof Error ? error.message : "Failed to refresh jobs"
      );
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation Header */}
      <ChatHeader />

      {/* Main Content */}
      <div className="p-4 mx-auto">
        <div className="flex items-center justify-between gap-4 mb-6">
          <div>
            <h1 className="text-2xl font-bold">Incident Dashboard</h1>
            <p className="text-muted-foreground mt-1">
              Track all submitted incidents and their analysis progress
            </p>
          </div>
          <div className="flex gap-2">
            <Link href="/">
              <Button variant="outline" size="sm">
                📝 Submit New Incident
              </Button>
            </Link>
            <Button onClick={handleManualRefresh} variant="ghost" size="sm">
              🔄 Refresh
            </Button>
          </div>
        </div>

        {/* Error Display */}
        {loadError && (
          <div className="mb-4 rounded-lg border border-destructive/20 bg-destructive/10 p-4">
            <div className="text-sm text-destructive">
              <strong>❌ Error loading jobs:</strong> {loadError}
            </div>
            <Button
              onClick={handleManualRefresh}
              variant="outline"
              size="sm"
              className="mt-2"
            >
              Try Again
            </Button>
          </div>
        )}

        {/* Loading State */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-2 border-primary/30 border-t-primary mx-auto mb-4"></div>
            <p className="text-muted-foreground">Loading incidents...</p>
          </div>
        ) : jobs.length === 0 ? (
          <div className="text-center py-12">
            <div className="mx-auto w-24 h-24 bg-muted rounded-full flex items-center justify-center mb-4">
              <svg
                className="w-12 h-12 text-muted-foreground"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <h3 className="text-lg font-medium mb-2">No incidents found</h3>
            <p className="text-muted-foreground mb-4">
              Submit your first incident to see it tracked here
            </p>
            <Link href="/">
              <Button>Submit First Incident</Button>
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="bg-muted/50 rounded-lg p-4">
              <p className="text-sm text-muted-foreground">
                🔄 Dashboard auto-refreshes every 5 seconds • Found{" "}
                {jobs.length} incidents • Click on any row to view detailed
                results
              </p>
            </div>

            <div className="overflow-auto rounded-lg border">
              <table className="w-full">
                <thead className="bg-muted/50">
                  <tr>
                    <th className="text-left px-4 py-3 font-medium">Run ID</th>
                    <th className="text-left px-4 py-3 font-medium">Status</th>
                    <th className="text-left px-4 py-3 font-medium">
                      Progress
                    </th>
                    <th className="text-left px-4 py-3 font-medium">
                      Current Step
                    </th>
                    <th className="text-left px-4 py-3 font-medium">Created</th>
                    <th className="text-left px-4 py-3 font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {jobs.map((job) => (
                    <JobRow
                      key={job.run_id}
                      job={job}
                      onRefresh={handleManualRefresh}
                    />
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default JobDashboard;
