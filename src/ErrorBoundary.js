import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    // Establecemos el estado inicial sin errores
    this.state = { hasError: false };
  }

  // Método estático para capturar errores y actualizar el estado
  static getDerivedStateFromError(error) {
    // Actualiza el estado para que el próximo render muestre la UI de fallback
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Puedes también registrar el error en un servicio de reporte de errores
    console.error("Uncaught error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      // Si hay un error, puedes renderizar cualquier UI de fallback personalizada
      return (
        <div className="flex items-center justify-center min-h-screen bg-red-100 text-red-700 p-8 rounded-lg shadow-lg">
          <div className="text-center">
            <h1 className="text-3xl font-bold mb-4">¡Algo salió mal!</h1>
            <p className="text-lg">Lo sentimos, la aplicación ha encontrado un error. Por favor, intenta recargar la página.</p>
          </div>
        </div>
      );
    }

    // Si no hay errores, renderiza el componente hijo
    return this.props.children;
  }
}

export default ErrorBoundary;
