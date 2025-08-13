// Este archivo define las variables globales que usa la plantilla de Alpine.js

// Usa el evento 'alpine:init' para registrar las variables globales
document.addEventListener('alpine:init', () => {
    // Define las variables para el estado de la barra lateral y los menús
    Alpine.store('global', {
        sidebarToggle: Alpine.$persist(false).as('sidebar-toggle'),
        page: 'blank', // Establece la página actual
        selected: '',  // Controla el menú desplegable activo
    });
});
