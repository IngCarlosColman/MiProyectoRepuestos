import React, { useState, useEffect } from 'react';

function App() {
  const [repuestos, setRepuestos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRepuestos = async () => {
      try {
        // La URL es relativa gracias a la configuración del proxy en package.json
        const response = await fetch('/api/repuestos/');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setRepuestos(data);
      } catch (e) {
        console.error("No se pudo obtener la lista de repuestos:", e);
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };

    fetchRepuestos();
  }, []);

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">Inventario de Repuestos</h1>
      
      {/* Mostrar estado de carga */}
      {loading && (
        <p className="text-gray-600 text-center">Cargando repuestos...</p>
      )}

      {/* Mostrar mensaje de error */}
      {error && (
        <p className="text-red-500 text-center">Error al cargar los datos: {error}</p>
      )}

      {/* Mostrar la lista de repuestos */}
      {!loading && !error && (
        <div>
          {repuestos.length > 0 ? (
            <ul className="space-y-4">
              {repuestos.map(repuesto => (
                <li key={repuesto.id} className="p-4 bg-gray-50 rounded-md shadow-sm border border-gray-200 hover:bg-gray-100 transition-colors duration-200">
                  <div className="text-lg font-semibold text-gray-900">{repuesto.nombre}</div>
                  <div className="text-sm text-gray-500">Código: {repuesto.codigo}</div>
                  <div className="text-sm text-gray-500">Cantidad: {repuesto.cantidad}</div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-600 text-center">No hay repuestos para mostrar.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
