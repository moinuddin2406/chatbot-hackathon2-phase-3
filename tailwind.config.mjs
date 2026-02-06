/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        'theme-primary': 'var(--color-primary)',
        'theme-primary-hover': 'var(--color-primary-hover)',
        'theme-secondary': 'var(--color-secondary)',
        'theme-accent': 'var(--color-accent)',
        'theme-text-primary': 'var(--color-text-primary)',
        'theme-text-secondary': 'var(--color-text-secondary)',
        'theme-success': 'var(--color-success)',
        'theme-danger': 'var(--color-danger)',
        'theme-background': 'var(--color-background)',
        'theme-foreground': 'var(--color-foreground)',
        'theme-card-bg': 'var(--color-card-bg)',
        'theme-card-border': 'var(--color-card-border)',
      }
    },
  },
  plugins: [],
};