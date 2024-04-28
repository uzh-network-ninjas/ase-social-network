/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#B1BF41',
        'secondary': '#5C917F',
        'high-emphasis': 'rgba(0,0,0,0.89)',
        'medium-emphasis': 'rgba(0,0,0,0.60)',
        'disabled': 'rgba(0,0,0,0.38)',
        'background': '#FFFFFF',
        'contrast': '#FFFFFF',
        'success': '#A1CB4D',
        'warning': '#EDBE5E',
        'error': '#E25336',
        'selection-indicator': '#000000',
        'google-maps-star': '#fbbc04'
      },
      fontFamily: {
        sans: [
          '"Inter", sans-serif'
        ]
      },
      opacity: {
        '38': '.38',
        '89': '.89',
      },
      spacing: {
        '1/4': '25%'
      }
    },
  },
  plugins: [],
}

