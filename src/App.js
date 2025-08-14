import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ErrorBoundary from './ErrorBoundary'; // Importamos el componente Límite de Error

function App() {
  // Estado para almacenar la lista de repuestos
  const [repuestos, setRepuestos] = useState([]);
  // Estado para manejar el estado de carga
  const [cargando, setCargando] = useState(true);
  // Estado para manejar los errores
  const [error, setError] = useState(null);

  // useEffect para realizar la llamada a la API cuando el componente se monte
  useEffect(() => {
    const fetchRepuestos = async () => {
      try {
        // Asumiendo que esta es la URL de tu API de Django
        const response = await axios.get('http://localhost:8000/api/repuestos/');
        
        // Se añade una comprobación para asegurar que response.data es un array
        // antes de actualizar el estado.
        if (Array.isArray(response.data)) {
          setRepuestos(response.data);
        } else {
          // Si los datos no son un array, registramos un error y establecemos
          // un array vacío para evitar que la aplicación se bloquee.
          console.error("La API no devolvió una lista de repuestos, sino:", response.data);
          setRepuestos([]);
          setError("Error en los datos de la API. Por favor, contacta con soporte.");
        }
        
        setError(null);
      } catch (err) {
        // En caso de error, guardamos el mensaje en el estado
        setError('No se pudieron cargar los repuestos. Intente de nuevo más tarde.');
        console.error("Error al obtener repuestos:", err);
      } finally {
        // Independientemente del resultado, la carga ha terminado
        setCargando(false);
      }
    };
    fetchRepuestos();
  }, []); // El array vacío asegura que se ejecute solo una vez

  // Lógica de renderizado condicional
  if (cargando) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100">
        <p className="text-xl text-gray-700">Cargando repuestos...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100">
        <p className="text-red-500 text-xl">{error}</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-8">
      <h1 className="text-4xl font-bold text-gray-800 mb-8">Catálogo de Repuestos</h1>
      
      {Array.isArray(repuestos) && repuestos.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full max-w-6xl">
          {repuestos.map(repuesto => (
            <div key={repuesto.id} className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300">
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">{repuesto.nombre}</h2>
              <p className="text-gray-600 mb-4">{repuesto.descripcion}</p>
              <div className="text-sm text-gray-500">
                {/* CORRECCIÓN: Ahora accedemos a repuesto.categoria.nombre */}
                <p><strong>Categoría:</strong> {repuesto.categoria.nombre}</p>
                {/* La corrección anterior para 'compatibilidad' sigue siendo válida */}
                <p>
                  <strong>Vehículos compatibles:</strong>
                  {repuesto.compatibilidad?.length > 0
                    ? repuesto.compatibilidad.map(v => `${v.marca} ${v.modelo} (${v.anio})`).join(', ')
                    : 'No se especifican'}
                </p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center p-12">
          <p className="text-xl text-gray-500">No se encontraron repuestos.</p>
        </div>
      )}
    </div>
  );
}

// Envolvemos el componente App con el ErrorBoundary.
export default function AppWithErrorBoundary() {
  return (
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  );
}
