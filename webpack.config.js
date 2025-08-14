const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');

module.exports = {
  // Modo de desarrollo para activar herramientas de depuración
  mode: "development",
  
  // Punto de entrada principal para la aplicación
  entry: "./src/index.js",
  
  output: {
    // Directorio de salida para los archivos de producción
    path: path.resolve(__dirname, 'static/dist'),
    filename: "[name].js",
    clean: true,
  },
  
  // Configuración del servidor de desarrollo de Webpack
  devServer: {
    port: 3000,
    hot: true,
    historyApiFallback: true, // Crucial para el enrutamiento del lado del cliente
    open: true, // Abre el navegador automáticamente al iniciar
    // Configuración del proxy para redirigir peticiones a la API de Django
    // ¡Aquí está la corrección! El proxy ahora es un array.
    proxy: [{
      context: ['/api'],
      target: 'http://localhost:8000',
    }],
  },

  // Módulos (Loaders) para procesar diferentes tipos de archivos
  module: {
    rules: [
      // Configuración para archivos JavaScript y JSX con Babel
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'],
          },
        },
      },
      // Configuración para archivos CSS, incluyendo Tailwind
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'postcss-loader',
        ],
      },
      // Configuración para manejar imágenes y otros assets
      {
        test: /\.(png|svg|jpg|jpeg|gif|ico)$/i,
        type: 'asset/resource',
        generator: {
          filename: 'images/[name][ext]',
        },
      },
    ],
  },
  
  // Plugins para añadir funcionalidades adicionales a Webpack
  plugins: [
    new CleanWebpackPlugin(),
    new MiniCssExtractPlugin({
      filename: "style.css",
    }),
    new CopyWebpackPlugin({
      patterns: [
        {
          from: path.resolve(__dirname, 'node_modules/leaflet/dist/images'),
          to: path.resolve(__dirname, 'static/dist/images'),
        },
        {
          from: path.resolve(__dirname, 'src/images/favicon.ico'),
          to: path.resolve(__dirname, 'static/dist/favicon.ico'),
        },
      ],
    }),
    new HtmlWebpackPlugin({
      template: './public/index.html',
      filename: 'index.html',
    }),
  ],
  
  // Opciones de optimización para producción
  optimization: {
    minimizer: [
      new CssMinimizerPlugin(),
    ],
  },
};
