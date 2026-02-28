/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'acreage-dark': '#1e293b',
        'acreage-primary': '#3b82f6',
      }
    },
  },
  plugins: [],
}