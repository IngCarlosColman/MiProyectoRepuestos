import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './css/style.css'; // Asegúrate de que esta ruta sea correcta

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);