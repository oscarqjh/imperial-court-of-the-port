"use client";

import React, { useState } from "react";
import type { Job } from "@/types/job";
import { Button } from "./ui/button";
import { Modal } from "./ui/modal";

type Props = {
  job: Job;
  onRefresh?: () => void;
};

/**
 * JobRow - responsible for rendering a single job's information.
 * Keeps UI rendering concerns isolated from data management.
 */
export function JobRow({ job, onRefresh }: Props) {
  const [showResultsModal, setShowResultsModal] = useState(false);
  const [showErrorModal, setShowErrorModal] = useState(false);

  // Format timestamp
  const formatTimestamp = (timestamp?: string | null) => {
    if (!timestamp) return "—";
    return new Date(timestamp).toLocaleString();
  };

  // Get status styling
  const getStatusClass = (status: Job["status"]) => {
    switch (status) {
      case "success":
        return "bg-green-100 text-green-800 border-green-200";
      case "failure":
        return "bg-red-100 text-red-800 border-red-200";
      case "processing":
        return "bg-blue-100 text-blue-800 border-blue-200";
      case "pending":
        return "bg-yellow-100 text-yellow-800 border-yellow-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  // Extract crew output from job result (instead of escalation_summary)
  const getCrewOutput = () => {
    if (!job.result || typeof job.result !== "object") {
      return null;
    }

    return job.result.crew_output || null;
  };

  // Check if there's incident information
  const getIncidentInfo = () => {
    if (!job.result || typeof job.result !== "object") {
      return null;
    }

    return {
      incident_id: job.result.incident_id,
      ticket_priority: job.result.ticket_priority,
      contact_information: job.result.contact_information,
      incident_analysis: job.result.incident_analysis,
    };
  };

  return (
    <>
      <tr className="border-b last:border-b-0 hover:bg-muted/50">
        <td className="px-4 py-3 text-sm font-mono">
          <div className="max-w-[200px] truncate" title={job.run_id}>
            {job.run_id}
          </div>
        </td>
        <td className="px-4 py-3 text-sm">
          <span
            className={`px-2 py-1 rounded-full text-xs font-medium border ${getStatusClass(
              job.status
            )}`}
          >
            {job.status}
          </span>
        </td>
        <td className="px-4 py-3 text-sm">
          {job.progress !== null && job.progress !== undefined ? (
            <div className="flex items-center gap-2">
              <div className="w-16 bg-muted rounded-full h-2">
                <div
                  className="bg-primary h-2 rounded-full transition-all"
                  style={{ width: `${job.progress}%` }}
                />
              </div>
              <span className="text-xs">{job.progress}%</span>
            </div>
          ) : (
            <span className="text-muted-foreground">—</span>
          )}
        </td>
        <td className="px-4 py-3 text-sm">
          {job.current_step ? (
            <span className="text-xs bg-muted rounded px-2 py-1">
              {job.current_step}
            </span>
          ) : (
            <span className="text-muted-foreground">—</span>
          )}
        </td>
        <td className="px-4 py-3 text-sm text-muted-foreground">
          {formatTimestamp(job.created_at)}
        </td>
        <td className="px-4 py-3 text-sm">
          <div className="flex gap-2">
            <Button size="sm" variant="outline" onClick={onRefresh}>
              🔄
            </Button>
            {job.result && (
              <Button
                size="sm"
                variant="outline"
                onClick={() => setShowResultsModal(true)}
              >
                📄 Results
              </Button>
            )}
            {job.error && (
              <Button
                size="sm"
                variant="outline"
                onClick={() => setShowErrorModal(true)}
              >
                ❌ Error
              </Button>
            )}
          </div>
        </td>
      </tr>

      {/* Results Modal */}
      <Modal
        isOpen={showResultsModal}
        onClose={() => setShowResultsModal(false)}
        title={`Job Results - ${job.run_id}`}
        maxWidth="max-w-6xl"
      >
        <div className="space-y-6">
          {/* Job Status Information */}
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <strong>Status:</strong>{" "}
              <span className="capitalize">{job.status}</span>
            </div>
            <div>
              <strong>Progress:</strong> {job.progress}%
            </div>
            <div>
              <strong>Created:</strong> {formatTimestamp(job.created_at)}
            </div>
            <div>
              <strong>Completed:</strong> {formatTimestamp(job.completed_at)}
            </div>
          </div>

          {/* Incident Information Summary */}
          {(() => {
            const incidentInfo = getIncidentInfo();
            if (!incidentInfo) return null;

            return (
              <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                <h3 className="font-semibold mb-3 text-blue-800 dark:text-blue-200">
                  📋 Incident Summary
                </h3>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  {incidentInfo.incident_id && (
                    <div>
                      <strong>Incident ID:</strong> {incidentInfo.incident_id}
                    </div>
                  )}
                  {incidentInfo.ticket_priority && (
                    <div>
                      <strong>Priority:</strong> {incidentInfo.ticket_priority}
                    </div>
                  )}
                  {incidentInfo.incident_analysis && (
                    <>
                      <div>
                        <strong>Type:</strong>{" "}
                        {incidentInfo.incident_analysis.incident_type}
                      </div>
                      <div>
                        <strong>Severity:</strong>{" "}
                        {incidentInfo.incident_analysis.severity}
                      </div>
                    </>
                  )}
                  {incidentInfo.contact_information && (
                    <>
                      <div>
                        <strong>Contact:</strong>{" "}
                        {incidentInfo.contact_information.name}
                      </div>
                      <div>
                        <strong>Email:</strong>{" "}
                        {incidentInfo.contact_information.email}
                      </div>
                    </>
                  )}
                </div>
              </div>
            );
          })()}

          {/* Crew Output Summary */}
          {(() => {
            const crewOutput = getCrewOutput();
            if (!crewOutput) return null;

            // Helper function to render markdown-like content as HTML
            const renderMarkdownContent = (content: string) => {
              return content.split("\n").map((line, index) => {
                // Handle headers (** text **)
                if (line.includes("**") && line.includes("**")) {
                  const parts = line.split("**");
                  return (
                    <div key={index} className="mb-2">
                      {parts.map((part, partIndex) =>
                        partIndex % 2 === 1 ? (
                          <strong
                            key={partIndex}
                            className="text-orange-900 dark:text-orange-100 font-bold"
                          >
                            {part}
                          </strong>
                        ) : (
                          <span key={partIndex}>{part}</span>
                        )
                      )}
                    </div>
                  );
                }

                // Handle bullet points (- text)
                if (line.trim().startsWith("- ")) {
                  return (
                    <div key={index} className="ml-4 mb-1">
                      <span className="text-orange-700 dark:text-orange-300">
                        •
                      </span>
                      <span className="ml-2">{line.trim().substring(2)}</span>
                    </div>
                  );
                }

                // Handle empty lines
                if (line.trim() === "") {
                  return <div key={index} className="mb-2"></div>;
                }

                // Regular lines
                return (
                  <div key={index} className="mb-1">
                    {line}
                  </div>
                );
              });
            };

            return (
              <div>
                <h3 className="font-semibold mb-3 text-orange-800 dark:text-orange-200">
                  🤖 Crew Analysis & Escalation Summary
                </h3>
                <div className="bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800 rounded-lg p-4 overflow-auto max-h-96">
                  <div className="text-sm leading-relaxed text-gray-800 dark:text-gray-200">
                    {renderMarkdownContent(crewOutput)}
                  </div>
                </div>
              </div>
            );
          })()}

          {/* Full Result Data */}
          <div>
            <h3 className="font-semibold mb-3">📊 Complete Result Data</h3>
            <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4 overflow-auto max-h-96">
              <pre className="text-sm whitespace-pre-wrap text-gray-900 dark:text-gray-100">
                {JSON.stringify(job.result, null, 2)}
              </pre>
            </div>
          </div>
        </div>
      </Modal>

      {/* Error Modal */}
      <Modal
        isOpen={showErrorModal}
        onClose={() => setShowErrorModal(false)}
        title={`Job Error - ${job.run_id}`}
        maxWidth="max-w-3xl"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <strong>Status:</strong>{" "}
              <span className="capitalize text-red-600">{job.status}</span>
            </div>
            <div>
              <strong>Progress:</strong> {job.progress}%
            </div>
            <div>
              <strong>Created:</strong> {formatTimestamp(job.created_at)}
            </div>
            <div>
              <strong>Failed:</strong> {formatTimestamp(job.completed_at)}
            </div>
          </div>

          <div>
            <h3 className="font-semibold mb-2 text-red-600 dark:text-red-400">
              Error Details:
            </h3>
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
              <p className="text-sm text-red-700 dark:text-red-300 whitespace-pre-wrap">
                {job.error}
              </p>
            </div>
          </div>
        </div>
      </Modal>
    </>
  );
}

export default JobRow;
