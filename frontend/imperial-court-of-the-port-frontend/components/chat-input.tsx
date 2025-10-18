"use client"

import type React from "react"

import { useState, useRef, type KeyboardEvent } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Paperclip, Send, X } from "lucide-react"
import type { UploadedFile } from "@/types/chat-interface"

interface ChatInputProps {
  onSendMessage: (content: string) => void
  onFilesSelected: (files: UploadedFile[]) => void
  uploadedFiles: UploadedFile[]
  onRemoveFile: (fileId: string) => void
  disabled?: boolean
}

export function ChatInput({ onSendMessage, onFilesSelected, uploadedFiles, onRemoveFile, disabled }: ChatInputProps) {
  const [input, setInput] = useState("")
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleSubmit = () => {
    if (input.trim() || uploadedFiles.length > 0) {
      onSendMessage(input)
      setInput("")
    }
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    const uploadedFileObjects: UploadedFile[] = files.map((file) => ({
      id: `${Date.now()}-${file.name}`,
      name: file.name,
      size: file.size,
      type: file.type,
      data: file, // store native File for uploads
    }))
    onFilesSelected(uploadedFileObjects)
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  return (
    <div className="border-t border-border bg-card/50 backdrop-blur-sm">
      <div className="mx-auto max-w-3xl p-3 sm:p-4">
        {uploadedFiles.length > 0 && (
          <div className="mb-2 sm:mb-3 flex flex-wrap gap-1.5 sm:gap-2">
            {uploadedFiles.map((file) => (
              <div
                key={file.id}
                className="flex items-center gap-1.5 sm:gap-2 rounded-lg border border-border bg-card px-2 py-1 sm:px-3 sm:py-1.5 text-xs sm:text-sm"
              >
                <span className="max-w-[120px] sm:max-w-[200px] truncate">{file.name}</span>
                <button onClick={() => onRemoveFile(file.id)} className="text-muted-foreground hover:text-foreground">
                  <X className="h-3 w-3" />
                </button>
              </div>
            ))}
          </div>
        )}

        <div className="flex items-end gap-1.5 sm:gap-2">
          <div className="relative flex-1">
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask Eureka anything..."
              disabled={disabled}
              className="min-h-[52px] sm:min-h-[56px] resize-none pr-10 sm:pr-12 text-sm sm:text-base"
              rows={1}
            />
            <Button
              type="button"
              size="icon"
              variant="ghost"
              className="absolute bottom-1.5 right-1.5 sm:bottom-2 sm:right-2 h-8 w-8 sm:h-9 sm:w-9"
              onClick={() => fileInputRef.current?.click()}
              disabled={disabled || uploadedFiles.length >= 100}
            >
              <Paperclip className="h-3.5 w-3.5 sm:h-4 sm:w-4" />
            </Button>
            <input
              ref={fileInputRef}
              type="file"
              multiple
              accept=".csv,.xlsx,.xls,.doc,.docx,.pdf,.txt,.html,.eml,.msg"
              onChange={handleFileChange}
              className="hidden"
            />
          </div>

          <Button
            onClick={handleSubmit}
            disabled={disabled || (!input.trim() && uploadedFiles.length === 0)}
            size="icon"
            className="h-[52px] w-[52px] sm:h-14 sm:w-14 shrink-0 bg-gradient-to-br from-primary to-accent hover:opacity-90"
          >
            <Send className="h-4 w-4 sm:h-5 sm:w-5" />
          </Button>
        </div>

        <p className="mt-1.5 sm:mt-2 text-center text-[10px] sm:text-xs text-muted-foreground px-2">
          {uploadedFiles.length > 0 && `${uploadedFiles.length}/100 files • `}
          <span className="hidden sm:inline">Supports CSV, Excel, Word, PDF, TXT, HTML, and email files</span>
          <span className="sm:hidden">CSV, Excel, Word, PDF, TXT, HTML</span>
        </p>
      </div>
    </div>
  )
}
