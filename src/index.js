import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Selecciona el elemento con id="root" en el HTML
const root = ReactDOM.createRoot(document.getElementById('root'));

// Renderiza el componente principal de la aplicación, <App />
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
