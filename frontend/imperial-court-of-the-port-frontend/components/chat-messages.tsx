import type { Message } from "@/types/chat-interface"
import { Avatar } from "@/components/ui/avatar"
import { Sparkles, User, FileText } from "lucide-react"
import { cn } from "@/lib/utils"
import LocalVideoPlayer from "./videoEmbed"

interface ChatMessagesProps {
  messages: Message[]
  isLoading: boolean
}

export function ChatMessages({ messages, isLoading }: ChatMessagesProps) {
  return (
    <div className="h-full overflow-y-auto">
      <div className="mx-auto max-w-3xl space-y-4 sm:space-y-6 p-3 sm:p-4 md:p-6 pb-32">
        {messages.map((message) => (
          <div
            key={message.id}
            className={cn("flex gap-2 sm:gap-4", message.role === "user" ? "justify-end" : "justify-start")}
          >
            {message.role === "assistant" && (
              <Avatar className="h-7 w-7 sm:h-8 sm:w-8 shrink-0 bg-gradient-to-br from-primary to-accent">
                <div className="flex h-full w-full items-center justify-center">
                  <Sparkles className="h-3.5 w-3.5 sm:h-4 sm:w-4 text-primary-foreground" />
                </div>
              </Avatar>
            )}

            <div
              className={cn(
                "max-w-[85%] sm:max-w-[80%] space-y-2 rounded-2xl px-3 py-2.5 sm:px-4 sm:py-3",
                message.role === "user" ? "bg-primary text-primary-foreground" : "bg-card border border-border",
              )}
            >
              {message.files && message.files.length > 0 && (
                <div className="flex flex-wrap gap-1.5 sm:gap-2 pb-2">
                  {message.files.map((file: any) => (
                    <div
                      key={file.id}
                      className={cn(
                        "flex items-center gap-1.5 sm:gap-2 rounded-lg px-2 py-1 sm:px-3 sm:py-1.5 text-xs",
                        message.role === "user" ? "bg-primary-foreground/20" : "bg-muted",
                      )}
                    >
                      <FileText className="h-3 w-3 shrink-0" />
                      <span className="max-w-[100px] sm:max-w-[150px] truncate">{file.name}</span>
                    </div>
                  ))}
                </div>
              )}

              <p className="whitespace-pre-wrap text-sm leading-relaxed">{message.content}</p>
            </div>

            {message.role === "user" && (
              <Avatar className="h-7 w-7 sm:h-8 sm:w-8 shrink-0 bg-muted">
                <div className="flex h-full w-full items-center justify-center">
                  <User className="h-3.5 w-3.5 sm:h-4 sm:w-4 text-muted-foreground" />
                </div>
              </Avatar>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="flex gap-2 sm:gap-4">
            <Avatar className="h-7 w-7 sm:h-8 sm:w-8 shrink-0 bg-gradient-to-br from-primary to-accent">
              <div className="flex h-full w-full items-center justify-center">
                <Sparkles className="h-3.5 w-3.5 sm:h-4 sm:w-4 text-primary-foreground" />
              </div>
            </Avatar>
            <div className="rounded-2xl border border-border bg-card px-3 py-2.5 sm:px-4 sm:py-3">
              <div className="flex flex-col gap-4">
              <p>Our agents are hard at work. We will provide you with a response shortly. Here is a look behind the scenes:</p>
              <LocalVideoPlayer src="https://drive.google.com/file/d/1OM2g1TBI4ZltZKz0G4gCGcGhwIPXvhom/view?usp=sharing"/>
              <div className="flex gap-1">
                <div className="h-2 w-2 animate-bounce rounded-full bg-primary [animation-delay:-0.3s]" />
                <div className="h-2 w-2 animate-bounce rounded-full bg-primary [animation-delay:-0.15s]" />
                <div className="h-2 w-2 animate-bounce rounded-full bg-primary" />
              </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
