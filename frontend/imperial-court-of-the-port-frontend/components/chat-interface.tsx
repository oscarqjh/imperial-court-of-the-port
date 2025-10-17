"use client"

import { useState } from "react"
import { ChatHeader } from "./chat-header"
import { ChatMessages } from "./chat-messages"
import { ChatInput } from "./chat-input"
import { FileUploadArea } from "./file-upload-area"
import ResponsiveImage from "./responsive-image"
import dbRAGService from "@/services/dbRAGService"
import { Message, UploadedFile } from "@/types/chat-interface"



export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSendMessage = async (content: string) => {
    if (!content.trim() && uploadedFiles.length === 0) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
      files: uploadedFiles.length > 0 ? [...uploadedFiles] : undefined,
      timestamp: new Date(),
    }
    //pass data into service
    dbRAGService(userMessage)
    setMessages((prev) => [...prev, userMessage])
    setUploadedFiles([])
    setIsLoading(true)
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
        <ResponsiveImage path="/eureka-court.png"/>
        {messages.length === 0 ? (
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
                  onClick={() => handleSendMessage("Analyze my data and provide insights")}
                  className="rounded-xl border border-border bg-card p-4 text-left transition-colors hover:bg-accent"
                >
                  <div className="text-sm font-medium">Analyze Data</div>
                  <div className="text-xs text-muted-foreground mt-1">Get insights from your files</div>
                </button>
                <button
                  onClick={() => handleSendMessage("Help me solve a complex problem")}
                  className="rounded-xl border border-border bg-card p-4 text-left transition-colors hover:bg-accent"
                >
                  <div className="text-sm font-medium">Problem Solving</div>
                  <div className="text-xs text-muted-foreground mt-1">Find solutions to challenges</div>
                </button>
                <button
                  onClick={() => handleSendMessage("Create a summary of my documents")}
                  className="rounded-xl border border-border bg-card p-4 text-left transition-colors hover:bg-accent sm:col-span-2 lg:col-span-1"
                >
                  <div className="text-sm font-medium">Summarize</div>
                  <div className="text-xs text-muted-foreground mt-1">Get concise summaries</div>
                </button>
              </div>
            </div>
          </div>
        ) : (
          <ChatMessages messages={messages} isLoading={isLoading} />
        )}
      </div>

      <ChatInput
        onSendMessage={handleSendMessage}
        onFilesSelected={handleFilesSelected}
        uploadedFiles={uploadedFiles}
        onRemoveFile={handleRemoveFile}
        disabled={isLoading}
      />
    </div>
  )
}
