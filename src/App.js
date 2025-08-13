// src/App.js

import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';

function App() {
  const [repuestos, setRepuestos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    marca: '',
    modelo: '',
    anio: '',
    categoria: ''
  });
  
  // Aquí puedes definir o buscar dinámicamente las opciones de los filtros.
  // Por ahora, las mantendremos estáticas para el ejemplo.
  const filterOptions = {
    marcas: ['Toyota', 'Ford'],
    modelos: ['Corolla', 'Focus'],
    anios: [2010, 2012, 2015, 2018],
    categorias: [
      { id: 1, nombre: 'Suspensión' },
      { id: 2, nombre: 'Motor' },
      { id: 3, nombre: 'Frenos' }
    ]
  };

  useEffect(() => {
    const fetchRepuestos = async () => {
      try {
        setLoading(true);
        setError(null);

        // Construir la URL con los parámetros de búsqueda y filtros
        const params = new URLSearchParams();
        if (searchTerm) params.append('search', searchTerm);
        if (filters.marca) params.append('marca', filters.marca);
        if (filters.modelo) params.append('modelo', filters.modelo);
        if (filters.anio) params.append('anio', filters.anio);
        if (filters.categoria) params.append('categoria_id', filters.categoria);

        const url = `/api/repuestos/?${params.toString()}`;
        const response = await fetch(url);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        setRepuestos(data);
      } catch (e) {
        console.error("Error al cargar los repuestos:", e);
        setError("Hubo un problema al cargar los repuestos. Inténtelo de nuevo más tarde.");
      } finally {
        setLoading(false);
      }
    };

    // Llamamos a la función de búsqueda cada vez que cambian los filtros o el término de búsqueda
    const delayDebounceFn = setTimeout(() => {
      fetchRepuestos();
    }, 500); // 500ms de "debounce" para no saturar la API en cada pulsación de tecla

    return () => clearTimeout(delayDebounceFn);
    
  }, [searchTerm, filters]);

  // Manejadores de eventos para los inputs del formulario
  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };
  
  const handleFilterChange = (event) => {
    const { name, value } = event.target;
    setFilters(prevFilters => ({
      ...prevFilters,
      [name]: value
    }));
  };

  return (
    <div className="bg-gray-100 min-h-screen p-8 font-inter">
      <header className="bg-white rounded-lg shadow-lg p-6 mb-8 text-center border-t-4 border-blue-500">
        <h1 className="text-4xl font-extrabold text-gray-800">Buscador de Repuestos</h1>
        <p className="text-gray-500 mt-2 text-lg">Encuentra el repuesto ideal para tu vehículo.</p>
      </header>
      
      <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
        <div className="flex flex-col md:flex-row items-center gap-4">
          {/* Input de búsqueda */}
          <div className="w-full md:w-2/3">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                <i className="fas fa-search text-gray-400"></i>
              </div>
              <input
                type="text"
                placeholder="Buscar por nombre, descripción, marca o modelo..."
                value={searchTerm}
                onChange={handleSearchChange}
                className="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-300 shadow-sm"
              />
            </div>
          </div>
          
          {/* Filtros */}
          <div className="w-full md:w-1/3 flex flex-wrap justify-end gap-2">
            <select name="marca" value={filters.marca} onChange={handleFilterChange} className="p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-700">
              <option value="">Marca</option>
              {filterOptions.marcas.map(marca => (
                <option key={marca} value={marca}>{marca}</option>
              ))}
            </select>
            <select name="modelo" value={filters.modelo} onChange={handleFilterChange} className="p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-700">
              <option value="">Modelo</option>
              {filterOptions.modelos.map(modelo => (
                <option key={modelo} value={modelo}>{modelo}</option>
              ))}
            </select>
            <select name="anio" value={filters.anio} onChange={handleFilterChange} className="p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-700">
              <option value="">Año</option>
              {filterOptions.anios.map(anio => (
                <option key={anio} value={anio}>{anio}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {loading && <p className="text-center text-gray-500 col-span-full py-12 text-lg">Cargando...</p>}
        {error && <p className="text-center text-red-500 col-span-full py-12 text-lg">{error}</p>}
        
        {!loading && repuestos.length === 0 && (
          <p className="text-center text-gray-500 col-span-full py-12 text-lg">No se encontraron repuestos con los criterios de búsqueda.</p>
        )}

        {repuestos.map(repuesto => (
          <div key={repuesto.id} className="bg-white rounded-lg shadow-lg p-6 transform hover:scale-105 transition-all duration-300 border-l-4 border-transparent hover:border-blue-500 cursor-pointer">
            <div className="flex items-center space-x-4 mb-4">
              <img 
                src={repuesto.imagen_url || "https://placehold.co/60x60/e2e8f0/64748b?text=IMG"} 
                alt={repuesto.nombre} 
                className="w-16 h-16 object-cover rounded-md shadow-sm"
              />
              <h2 className="text-xl font-bold text-gray-800">{repuesto.nombre}</h2>
            </div>
            
            <p className="text-gray-600 mb-4 text-sm">{repuesto.descripcion}</p>
            
            <div className="flex flex-wrap gap-2 mb-4">
              <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-1 rounded-full">
                {repuesto.categoria.nombre}
              </span>
            </div>
            
            <div className="border-t border-gray-200 pt-4">
              <p className="font-medium text-sm text-gray-700 mb-2">Compatible con:</p>
              <div className="flex flex-wrap gap-2">
                {repuesto.compatibilidad.map(vehiculo => (
                  <span key={vehiculo.id} className="bg-gray-200 text-gray-800 text-xs px-2.5 py-1 rounded-full">
                    {vehiculo.marca} {vehiculo.modelo} ({vehiculo.anio})
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
