/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        canvas: '#FBFAF7',
        surface: '#FFFFFF',
        line: '#EAEAEA',
        ink: '#111111',
        muted: '#787774',
        bone: '#F7F6F3',
      },
      fontFamily: {
        sans: ['Geist', 'SF Pro Display', 'Helvetica Neue', 'system-ui', 'sans-serif'],
        serif: ['Newsreader', 'Georgia', 'serif'],
        mono: ['Geist Mono', 'SF Mono', 'JetBrains Mono', 'monospace'],
      },
      letterSpacing: {
        tightest: '-0.03em',
      },
    },
  },
  plugins: [],
}
