"use client";

import { useState } from "react";
import Link from "next/link";
import { ChatHeader } from "./chat-header";
import { FileUploadArea } from "./file-upload-area";
import ResponsiveImage from "./responsive-image";
import { UploadedFile } from "@/types/chat-interface";

export function ChatInterface() {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState<null | {
    run_id: string;
    status: string;
  }>(null);
  const [error, setError] = useState<string | null>(null);
  const [manualText, setManualText] = useState<string>("");

  const extractTextFromFile = async (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();

      reader.onload = (e) => {
        const result = e.target?.result as string;
        if (file.type === "application/pdf") {
          // For PDFs, we'd need a proper PDF parser library
          // For now, we'll show a placeholder
          resolve(
            `[PDF Document: ${file.name}]\nNote: PDF text extraction requires additional processing. Please provide incident details manually or upload a TXT file.`
          );
        } else {
          // For text files, return the content directly
          resolve(result);
        }
      };

      reader.onerror = () =>
        reject(new Error(`Failed to read file: ${file.name}`));

      if (file.type === "application/pdf") {
        reader.readAsArrayBuffer(file);
      } else {
        reader.readAsText(file);
      }
    });
  };

  const handleSubmitIncident = async () => {
    if (uploadedFiles.length === 0 && !manualText.trim()) {
      setError(
        "Please upload a file (PDF/TXT) or enter incident text manually"
      );
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      let incidentText = "";

      // Extract text from uploaded files
      if (uploadedFiles.length > 0) {
        const textPromises = uploadedFiles.map(async (uploadedFile) => {
          // Convert UploadedFile back to File for text extraction
          // Note: In a real implementation, you'd need the actual File object
          // For now, we'll create a simple text representation
          return `=== File: ${uploadedFile.name} ===\n[File content would be extracted here]\nFile type: ${uploadedFile.type}\nFile size: ${uploadedFile.size} bytes`;
        });

        const extractedTexts = await Promise.all(textPromises);
        incidentText = extractedTexts.join("\n\n");
      }

      // Add manual text if provided
      if (manualText.trim()) {
        if (incidentText) {
          incidentText +=
            "\n\n=== Additional Information ===\n" + manualText.trim();
        } else {
          incidentText = manualText.trim();
        }
      }

      // Submit using the correct API format that matches your backend
      const response = await fetch("http://localhost:8000/incident/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          incident_type: "uploaded_content", // Will be auto-classified by CrewAI
          severity: "medium", // Will be auto-classified by CrewAI
          payload: {
            incident_text: incidentText,
            uploaded_files: uploadedFiles.map((f) => ({
              name: f.name,
              type: f.type,
              size: f.size,
            })),
            timestamp: new Date().toISOString(),
            source: "web_interface",
          },
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail || `HTTP ${response.status}: ${response.statusText}`
        );
      }

      const job = await response.json();
      setSubmitSuccess({
        run_id: job.run_id,
        status: job.status,
      });

      // Clear form after successful submission
      setManualText("");
      setUploadedFiles([]);
    } catch (e: any) {
      console.error("Submission error:", e);
      setError(e?.message || "Failed to submit incident");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleFilesSelected = (files: UploadedFile[]) => {
    // Filter to only accept PDF and TXT files
    const validFiles = files.filter(
      (file) =>
        file.type === "application/pdf" ||
        file.type === "text/plain" ||
        file.name.toLowerCase().endsWith(".txt") ||
        file.name.toLowerCase().endsWith(".pdf")
    );

    if (validFiles.length !== files.length) {
      setError("Only PDF and TXT files are supported");
      return;
    }

    setUploadedFiles((prev) => [...prev, ...validFiles]);
    setError(null);
  };

  const handleRemoveFile = (fileId: string) => {
    setUploadedFiles((prev) => prev.filter((f) => f.id !== fileId));
  };

  return (
    <div className="flex h-full flex-col">
      <ChatHeader />
      <div className="flex-1">
        <ResponsiveImage path="/eureka-court.png" />

        {!submitSuccess ? (
          <div className="flex items-center justify-center p-0 sm:p-6 md:p-8">
            <div className="w-full max-w-3xl space-y-6 sm:space-y-8">
              <div className="text-center space-y-3 sm:space-y-4">
                <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent text-balance">
                  Incident Analysis
                </h1>
                <p className="text-base sm:text-lg text-muted-foreground text-pretty px-4">
                  Upload incident files (PDF/TXT) or enter text for AI analysis
                </p>
                <p className="text-sm text-muted-foreground">
                  Our AI agents will automatically classify incident type and
                  severity
                </p>
              </div>

              <div className="space-y-6">
                {/* File Upload Section */}
                <div>
                  <label className="block text-sm font-medium mb-3">
                    📁 Upload Incident Files (PDF or TXT)
                  </label>
                  <FileUploadArea
                    onFilesSelected={handleFilesSelected}
                    maxFiles={5}
                  />
                  <p className="text-xs text-muted-foreground mt-2">
                    Supported formats: PDF, TXT files only
                  </p>

                  {/* Display uploaded files */}
                  {uploadedFiles.length > 0 && (
                    <div className="mt-4 space-y-2">
                      <h4 className="text-sm font-medium">Uploaded Files:</h4>
                      {uploadedFiles.map((file) => (
                        <div
                          key={file.id}
                          className="flex items-center justify-between bg-muted rounded-lg px-4 py-3"
                        >
                          <div className="flex items-center space-x-3">
                            <div className="text-2xl">
                              {file.type === "application/pdf" ? "📄" : "📝"}
                            </div>
                            <div>
                              <div className="text-sm font-medium">
                                {file.name}
                              </div>
                              <div className="text-xs text-muted-foreground">
                                {file.type} •{" "}
                                {(file.size || 0 / 1024).toFixed(1)} KB
                              </div>
                            </div>
                          </div>
                          <button
                            onClick={() => handleRemoveFile(file.id)}
                            className="text-destructive hover:text-destructive/80 text-sm font-medium"
                            disabled={isSubmitting}
                          >
                            Remove
                          </button>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Manual Text Input */}
                <div>
                  <label className="block text-sm font-medium mb-3">
                    ✏️ Or Enter Incident Details Manually
                  </label>
                  <textarea
                    value={manualText}
                    onChange={(e) => setManualText(e.target.value)}
                    placeholder="Describe the incident, error logs, symptoms, or any relevant details..."
                    className="w-full rounded-lg border border-border bg-background px-4 py-3 min-h-[120px] resize-none focus:ring-2 focus:ring-primary/20 focus:border-primary"
                    disabled={isSubmitting}
                  />
                  <p className="text-xs text-muted-foreground mt-2">
                    Provide as much detail as possible for better analysis
                  </p>
                </div>

                {/* Submit Button */}
                <button
                  onClick={handleSubmitIncident}
                  disabled={
                    isSubmitting ||
                    (uploadedFiles.length === 0 && !manualText.trim())
                  }
                  className="w-full rounded-lg bg-primary px-6 py-4 text-white font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary/90 transition-colors flex items-center justify-center space-x-2"
                >
                  {isSubmitting ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-2 border-white/30 border-t-white"></div>
                      <span>Analyzing Incident...</span>
                    </>
                  ) : (
                    <>
                      <span>🚀</span>
                      <span>Submit for AI Analysis</span>
                    </>
                  )}
                </button>

                {error && (
                  <div className="text-sm text-destructive bg-destructive/10 rounded-lg px-4 py-3 border border-destructive/20">
                    <div className="font-medium">❌ Submission Failed</div>
                    <div className="mt-1">{error}</div>
                  </div>
                )}

                {/* Info Cards */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4">
                  <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
                    <div className="font-medium text-blue-800 text-sm">
                      🤖 AI-Powered Analysis
                    </div>
                    <div className="text-blue-700 text-xs mt-1">
                      Automatic incident classification and severity assessment
                    </div>
                  </div>
                  <div className="bg-green-50 rounded-lg p-4 border border-green-200">
                    <div className="font-medium text-green-800 text-sm">
                      ⚡ Real-time Progress
                    </div>
                    <div className="text-green-700 text-xs mt-1">
                      Track analysis progress on the dashboard
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          // Success panel: show submission result and dashboard link
          <div className="flex items-center justify-center p-6">
            <div className="w-full max-w-2xl space-y-6 text-center">
              <div className="rounded-lg border border-green-200 bg-green-50 p-6">
                <h2 className="text-2xl font-semibold text-green-800 mb-4">
                  ✅ Incident Submitted Successfully
                </h2>

                <div className="space-y-3 text-left bg-white rounded-md p-4 border">
                  <div className="flex justify-between">
                    <span className="font-medium">Run ID:</span>
                    <span className="font-mono text-sm">
                      {submitSuccess.run_id}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="font-medium">Status:</span>
                    <span className="capitalize">{submitSuccess.status}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="font-medium">Submitted:</span>
                    <span>{new Date().toLocaleString()}</span>
                  </div>
                </div>

                <p className="text-sm text-green-700 mt-4">
                  🤖 AI agents are analyzing your incident and will
                  automatically classify the type and severity. Track progress
                  on the dashboard.
                </p>
              </div>

              <div className="flex justify-center gap-3">
                <Link href="/dashboard">
                  <button className="rounded-md bg-primary px-6 py-3 text-white font-medium hover:bg-primary/90 transition-colors">
                    📊 View Analysis Dashboard
                  </button>
                </Link>
                <button
                  className="rounded-md border border-border px-6 py-3 hover:bg-muted transition-colors"
                  onClick={() => {
                    setSubmitSuccess(null);
                    setError(null);
                  }}
                >
                  📝 Submit Another Incident
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
