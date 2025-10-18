import { Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "./theme-toggle";
import Link from "next/link";

export function ChatHeader() {
  return (
    <header className="border-b border-border bg-card/50 backdrop-blur-sm">
      <div className="flex h-14 items-center justify-between px-3 sm:px-4 md:px-6">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-primary to-accent">
            <Sparkles className="h-5 w-5 text-primary-foreground" />
          </div>
          <span className="text-base sm:text-lg font-semibold">Eureka</span>
        </div>

        <div className="flex items-center gap-1 sm:gap-2">
          <ThemeToggle />
          <Link href="/dashboard">
            <Button variant="ghost" size="sm" className="hidden sm:inline-flex">
              Dashboard
            </Button>
          </Link>
          <Link href="/">
            <Button variant="ghost" size="sm" className="hidden sm:inline-flex">
              Home
            </Button>
          </Link>
          <Link href="/about">
            <Button variant="ghost" size="sm" className="hidden sm:inline-flex">
              About
            </Button>
          </Link>
          <Button variant="ghost" size="icon" className="sm:hidden h-9 w-9">
            <span className="text-lg">+</span>
          </Button>
        </div>
      </div>
    </header>
  );
}
