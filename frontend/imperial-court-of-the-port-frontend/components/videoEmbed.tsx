"use client"

import React, { useCallback, useRef, useState } from 'react'

interface LocalVideoPlayerProps {
  src: string
  width?: string | number
  height?: string | number
  isBackground?: boolean
  // Short caption/title for the video for accessibility
  caption?: string
  // Optional short transcript text (displayed below video for accessibility)
  transcript?: string
}

export default function LocalVideoPlayer({
  src,
  width = '100%',
  height = 'auto',
  isBackground = false,
  caption,
  transcript,
}: LocalVideoPlayerProps) {
  const [loading, setLoading] = useState(true)
  const videoRef = useRef<HTMLVideoElement | null>(null)

  const handleCanPlay = useCallback(() => setLoading(false), [])
  const handleWaiting = useCallback(() => setLoading(true), [])
  const handlePlaying = useCallback(() => setLoading(false), [])

  return (
    <figure className="relative">
      <video
        ref={videoRef}
        controls={!isBackground}
        width={width}
        height={height}
        preload={isBackground ? 'auto' : 'metadata'}
        onCanPlay={handleCanPlay}
        onWaiting={handleWaiting}
        onPlaying={handlePlaying}
        className="w-full h-auto bg-black"
      >
        <source src={src} type="video/mp4" />
        <p>
          Your browser does not support HTML5 video. You can download it <a href={src}>here</a>.
        </p>
      </video>

      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/30">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-t-transparent border-white/90" aria-hidden="true" />
          <span className="sr-only">Loading video</span>
        </div>
      )}

      {caption && <figcaption className="mt-2 text-sm text-muted-foreground">{caption}</figcaption>}

      {transcript && (
        <details className="mt-2 text-sm text-muted-foreground">
          <summary className="cursor-pointer">Transcript</summary>
          <div className="whitespace-pre-wrap mt-2">{transcript}</div>
        </details>
      )}
    </figure>
  )
}