/** @type {import('postcss-load-config').Config} */
module.exports = {
  plugins: {
    // Usamos el nuevo plugin de PostCSS para Tailwind CSS v4.
    '@tailwindcss/postcss': {},
    // Agregamos Autoprefixer para compatibilidad con navegadores.
    'autoprefixer': {},
  },
};
