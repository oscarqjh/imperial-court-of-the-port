"use client";
import { Sparkles, Menu, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { useState } from "react";

export function ChatHeader() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <>
      <header className="border-b border-border bg-card/50 backdrop-blur-sm">
        <div className="flex h-14 items-center justify-between px-3 sm:px-4 md:px-6">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-primary to-accent">
              <Sparkles className="h-5 w-5 text-primary-foreground" />
            </div>
            <span className="text-base sm:text-lg font-semibold">Eureka</span>
          </div>

          <div className="flex items-center gap-1 sm:gap-2">
            {/* Desktop Navigation */}
            <Link href="/dashboard">
              <Button
                variant="ghost"
                size="sm"
                className="hidden sm:inline-flex"
              >
                Dashboard
              </Button>
            </Link>
            <Link href="/">
              <Button
                variant="ghost"
                size="sm"
                className="hidden sm:inline-flex"
              >
                Home
              </Button>
            </Link>
            <Link href="/about">
              <Button
                variant="ghost"
                size="sm"
                className="hidden sm:inline-flex"
              >
                About
              </Button>
            </Link>
            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              size="icon"
              className="sm:hidden h-9 w-9"
              onClick={toggleMobileMenu}
            >
              {isMobileMenuOpen ? (
                <X className="h-5 w-5" />
              ) : (
                <Menu className="h-5 w-5" />
              )}
            </Button>
          </div>
        </div>
      </header>

      {/* Mobile Navigation Menu */}
      {isMobileMenuOpen && (
        <div className="sm:hidden border-b border-border bg-card/95 backdrop-blur-sm">
          <div className="px-3 py-2 space-y-1">
            <Link href="/dashboard" onClick={() => setIsMobileMenuOpen(false)}>
              <Button
                variant="ghost"
                size="sm"
                className="w-full justify-start"
              >
                Dashboard
              </Button>
            </Link>
            <Link href="/" onClick={() => setIsMobileMenuOpen(false)}>
              <Button
                variant="ghost"
                size="sm"
                className="w-full justify-start"
              >
                Home
              </Button>
            </Link>
            <Link href="/about" onClick={() => setIsMobileMenuOpen(false)}>
              <Button
                variant="ghost"
                size="sm"
                className="w-full justify-start"
              >
                About
              </Button>
            </Link>
          </div>
        </div>
      )}
    </>
  );
}
