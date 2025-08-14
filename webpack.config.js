const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');

module.exports = {
  // Modo de desarrollo
  mode: "development",
  
  // Punto de entrada principal (React y CSS)
  entry: {
    bundle: "./src/index.js",
  },
  
  output: {
    // Directorio de salida final para el JavaScript y CSS
    path: path.resolve(__dirname, 'static/dist'),
    // Nombres de los archivos de salida
    filename: "[name].js",
    // Limpia el directorio de salida antes de cada compilación
    clean: true,
  },
  
  devServer: {
    static: {
      directory: path.join(__dirname, "./static/dist"),
    },
    compress: true,
    port: 3000,
    hot: true,
  },

  // Módulos (Loaders)
  module: {
    rules: [
      // Regla para archivos JavaScript y JSX
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
      // Regla para archivos CSS (procesa Tailwind)
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'postcss-loader',
        ],
      },
      // Regla para manejar archivos de imagen
      {
        test: /\.(png|svg|jpg|jpeg|gif|ico)$/i,
        type: 'asset/resource',
        generator: {
          filename: 'images/[name][ext]',
        },
      },
    ],
  },
  
  // Plugins
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
  ],
  
  // Opciones de optimización
  optimization: {
    minimizer: [
      new CssMinimizerPlugin(),
    ],
  },
};
