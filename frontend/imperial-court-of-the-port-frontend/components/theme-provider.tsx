"use client";

import * as React from "react";

type Theme = "dark" | "light" | "system";

type ThemeProviderProps = {
  children: React.ReactNode;
  defaultTheme?: Theme;
  storageKey?: string;
};

type ThemeProviderState = {
  theme: Theme;
  setTheme: (theme: Theme) => void;
};

const initialState: ThemeProviderState = {
  theme: "system",
  setTheme: () => null,
};

const ThemeProviderContext =
  React.createContext<ThemeProviderState>(initialState);

export function ThemeProvider({
  children,
  defaultTheme = "light",
  storageKey = "eureka-theme",
  ...props
}: ThemeProviderProps) {
  // Force light mode by always setting theme to "light"
  const [theme, setTheme] = React.useState<Theme>("light");

  React.useEffect(() => {
    const root = window.document.documentElement;

    root.classList.remove("light", "dark");
    // Always apply light theme
    root.classList.add("light");
  }, []);

  const value = {
    theme: "light" as Theme,
    setTheme: (newTheme: Theme) => {
      // Prevent theme changes - always stay in light mode
      console.log(`Theme change to ${newTheme} blocked - light mode only`);
    },
  };

  return (
    <ThemeProviderContext.Provider {...props} value={value}>
      {children}
    </ThemeProviderContext.Provider>
  );
}

export const useTheme = () => {
  const context = React.useContext(ThemeProviderContext);

  if (context === undefined)
    throw new Error("useTheme must be used within a ThemeProvider");

  return context;
};
