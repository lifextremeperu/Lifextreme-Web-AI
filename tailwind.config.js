/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./*.html",
    "./partners/**/*.html",
    "./js/**/*.js",
    "./api/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#4338ca',    /* Indigo 700 */
        secondary: '#f43f5e',  /* Rose 500 */
        accent: '#ffbf00',     /* Amber Custom */
        slate: { 900: '#0f172a', 910: '#020617' }
      },
      container: { center: true, padding: '2rem' },
      boxShadow: { '3xl': '0 35px 60px -15px rgba(0, 0, 0, 0.3)' }
    },
  },
  plugins: [],
}
