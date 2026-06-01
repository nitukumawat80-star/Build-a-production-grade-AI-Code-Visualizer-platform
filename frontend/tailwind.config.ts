import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        ink: "#04080f",
        slate: "#111827",
        pulse: "#00d9c0",
        ember: "#ff7a00",
        moon: "#89a6fb"
      },
      boxShadow: {
        soft: "0 12px 40px rgba(0,0,0,0.35)"
      }
    }
  },
  plugins: []
};

export default config;
