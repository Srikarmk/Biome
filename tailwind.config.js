/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#eef2ff",
          100: "#e0e7ff",
          500: "#4f46e5",
          600: "#3730a3",
          700: "#312e81",
        },
        accent: {
          500: "#f59e0b",
          600: "#d97706",
        },
        success: "#10b981",
        warning: "#f59e0b",
        error: "#ef4444",
        bg: "#0f172a",
        surface: "#1e293b",
        text: "#f1f5f9",
        "text-secondary": "#94a3b8",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
