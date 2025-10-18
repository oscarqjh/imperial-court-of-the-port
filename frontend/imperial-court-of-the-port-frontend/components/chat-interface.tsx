"use client"

import { useState } from "react"
import Link from 'next/link'
import { ChatHeader } from "./chat-header"
import { ChatInput } from "./chat-input"
import { FileUploadArea } from "./file-upload-area"
import ResponsiveImage from "./responsive-image"
import LocalVideoPlayer from "./videoEmbed"
import runService from '@/services/runService'
import { UploadedFile } from "@/types/chat-interface"



export function ChatInterface() {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([])
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitSuccess, setSubmitSuccess] = useState<null | { run_id: string }>(null)
  const [error, setError] = useState<string | null>(null)

  // Accept an optional intent (from buttons) or freeform text (from ChatInput)
  const handleSubmitJob = async (intent?: string, text?: string) => {
    if (uploadedFiles.length === 0 && !intent && !text) return
    setIsSubmitting(true)
    setError(null)

    try {
      // Build a payload for the run. If you need to attach files as FormData,
      // move this into a FormData posting helper. Here we send metadata and file names.
      const payload: any = {
        incident_type: 'USER_UPLOAD',
        payload: { intent },
        input_files: uploadedFiles.map((f) => ({ id: f.id, name: f.name }))
      }

      if (text) payload.payload.text = text

      const job = await runService.startRun(payload)
      setSubmitSuccess({ run_id: job.run_id })
      setUploadedFiles([])
    } catch (e: any) {
      setError(e?.message || 'Failed to submit job')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleFilesSelected = (files: UploadedFile[]) => {
    setUploadedFiles((prev) => [...prev, ...files])
  }

  const handleRemoveFile = (fileId: string) => {
    setUploadedFiles((prev) => prev.filter((f) => f.id !== fileId))
  }

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
                  Eureka
                </h1>
                <p className="text-base sm:text-lg text-muted-foreground text-pretty px-4">
                  Upload your files and get AI-powered solutions
                </p>
              </div>

                <FileUploadArea onFilesSelected={handleFilesSelected} maxFiles={100} />

              <div className="grid gap-3 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
                <button
                  onClick={() => handleSubmitJob('ANALYZE')}
                  className="rounded-xl border border-border bg-card p-4 text-left transition-colors hover:bg-accent"
                  disabled={isSubmitting || uploadedFiles.length === 0}
                >
                  <div className="text-sm font-medium">Analyze Data</div>
                  <div className="text-xs text-muted-foreground mt-1">Get insights from your files</div>
                </button>
                <button
                  onClick={() => handleSubmitJob('PROBLEM_SOLVE')}
                  className="rounded-xl border border-border bg-card p-4 text-left transition-colors hover:bg-accent"
                  disabled={isSubmitting || uploadedFiles.length === 0}
                >
                  <div className="text-sm font-medium">Problem Solving</div>
                  <div className="text-xs text-muted-foreground mt-1">Find solutions to challenges</div>
                </button>
                <button
                  onClick={() => handleSubmitJob('SUMMARIZE')}
                  className="rounded-xl border border-border bg-card p-4 text-left transition-colors hover:bg-accent sm:col-span-2 lg:col-span-1"
                  disabled={isSubmitting || uploadedFiles.length === 0}
                >
                  <div className="text-sm font-medium">Summarize</div>
                  <div className="text-xs text-muted-foreground mt-1">Get concise summaries</div>
                </button>
              </div>

              {error && <div className="text-sm text-destructive">{error}</div>}
            </div>
          </div>
        ) : (
          // Success panel: show behind-the-scenes video and dashboard CTA
          <div className="flex items-center justify-center p-6">
            <div className="w-full max-w-3xl space-y-6 text-center">
              <h2 className="text-2xl font-semibold">Job submitted successfully</h2>
              <p className="text-sm text-muted-foreground">Run ID: {submitSuccess.run_id}</p>

              <div className="rounded overflow-hidden">
                {/* LocalVideoPlayer expects an mp4 - put court.mp4 in public/ */}
                <LocalVideoPlayer
                  src="https://drive.google.com/file/d/1OM2g1TBI4ZltZKz0G4gCGcGhwIPXvhom/view?usp=sharing"
                  width="100%"
                  caption="Behind the scenes: How our agents process your files"
                  transcript={`This short clip shows the processing pipeline: files are uploaded, queued, processed by AI agents, and results are produced as output files. The video is a conceptual visualization and does not contain sensitive data.`}
                />
              </div>

              <div className="flex justify-center gap-3">
                <Link href="/dashboard">
                  <button className="rounded-md bg-primary px-4 py-2 text-white">Go to Dashboard</button>
                </Link>
                <button
                  className="rounded-md border px-4 py-2"
                  onClick={() => {
                    // reset to allow submitting again
                    setSubmitSuccess(null)
                  }}
                >
                  Submit another
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Keep a minimal input area for attaching files and removing them. The send button will submit a job using the text or attached files. */}
      <ChatInput
        onSendMessage={(content) => {
          // content is freeform text from the input; forward to job submission
          void handleSubmitJob(undefined, content)
        }}
        onFilesSelected={handleFilesSelected}
        uploadedFiles={uploadedFiles}
        onRemoveFile={handleRemoveFile}
        disabled={isSubmitting}
      />
    </div>
  )
}
