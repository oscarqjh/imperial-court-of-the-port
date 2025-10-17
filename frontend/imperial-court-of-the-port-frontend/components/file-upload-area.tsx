"use client"

import type React from "react"

import { useCallback, useState } from "react"
import { Upload, FileText } from "lucide-react"
import { cn } from "@/lib/utils"
import type { UploadedFile } from "./chat-interface"

interface FileUploadAreaProps {
  onFilesSelected: (files: UploadedFile[]) => void
  maxFiles?: number
}

export function FileUploadArea({ onFilesSelected, maxFiles = 100 }: FileUploadAreaProps) {
  const [isDragging, setIsDragging] = useState(false)

  const handleFiles = useCallback(
    (files: FileList) => {
      const fileArray = Array.from(files).slice(0, maxFiles)
      const uploadedFiles: UploadedFile[] = fileArray.map((file) => ({
        id: `${Date.now()}-${file.name}`,
        name: file.name,
        size: file.size,
        type: file.type,
      }))
      onFilesSelected(uploadedFiles)
    },
    [onFilesSelected, maxFiles],
  )

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setIsDragging(false)
      if (e.dataTransfer.files) {
        handleFiles(e.dataTransfer.files)
      }
    },
    [handleFiles],
  )

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      if (e.target.files) {
        handleFiles(e.target.files)
      }
    },
    [handleFiles],
  )

  return (
    <div
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      className={cn(
        "relative rounded-xl sm:rounded-2xl border-2 border-dashed border-border bg-card p-6 sm:p-8 md:p-12 text-center transition-colors",
        isDragging && "border-primary bg-primary/5",
      )}
    >
      <input
        type="file"
        multiple
        accept=".csv,.xlsx,.xls,.doc,.docx,.pdf,.txt,.html,.eml,.msg"
        onChange={handleFileInput}
        className="absolute inset-0 cursor-pointer opacity-0"
        id="file-upload"
      />

      <div className="flex flex-col items-center gap-3 sm:gap-4">
        <div className="rounded-full bg-primary/10 p-3 sm:p-4">
          <Upload className="h-6 w-6 sm:h-8 sm:w-8 text-primary" />
        </div>

        <div className="space-y-1 sm:space-y-2">
          <p className="text-base sm:text-lg font-medium text-balance">Drop files here or click to upload</p>
          <p className="text-xs sm:text-sm text-muted-foreground text-pretty px-2">
            Upload up to {maxFiles} files • CSV, Excel, Word, PDF, TXT, HTML, Email
          </p>
        </div>

        <div className="flex flex-wrap justify-center gap-1.5 sm:gap-2 text-[10px] sm:text-xs text-muted-foreground">
          <span className="flex items-center gap-1">
            <FileText className="h-3 w-3" />
            .csv
          </span>
          <span className="flex items-center gap-1">
            <FileText className="h-3 w-3" />
            .xlsx
          </span>
          <span className="flex items-center gap-1">
            <FileText className="h-3 w-3" />
            .docx
          </span>
          <span className="flex items-center gap-1">
            <FileText className="h-3 w-3" />
            .pdf
          </span>
          <span className="flex items-center gap-1">
            <FileText className="h-3 w-3" />
            .txt
          </span>
          <span className="flex items-center gap-1">
            <FileText className="h-3 w-3" />
            .html
          </span>
        </div>
      </div>
    </div>
  )
}
