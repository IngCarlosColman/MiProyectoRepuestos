// Importa la librería Leaflet.
// Es una buena práctica importar el objeto L directamente aquí.
import L from 'leaflet';

// Importa las imágenes de los íconos de Leaflet
// Webpack se encargará de encontrar y procesar estas imágenes
import icon from 'leaflet/dist/images/marker-icon.png';
import iconRetina from 'leaflet/dist/images/marker-icon-2x.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

// Corrige el problema de Webpack con los íconos de Leaflet
delete L.Icon.Default.prototype._getIconUrl;

// Configura las opciones por defecto de los íconos de Leaflet para usar las imágenes importadas
L.Icon.Default.mergeOptions({
  iconRetinaUrl: iconRetina,
  iconUrl: icon,
  shadowUrl: iconShadow,
});

// Este archivo creará y configurará un mapa de Leaflet
// Asegúrate de que el ID 'map' coincida con el ID del <div> en tu HTML
// La visualización se establece en Asunción, Paraguay.
var map = L.map('map').setView([-25.3007, -57.6358], 8); // Coordenadas de Asunción, Paraguay, con un zoom para ver el país.

// Añadir una capa de tiles (capa base) al mapa
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '© OpenStreetMap'
}).addTo(map);

// Ejemplo: Añadir un marcador en Asunción, Paraguay
var marker = L.marker([-25.3007, -57.6358]).addTo(map);
marker.bindPopup("<b>Hola!</b><br>Estamos en Asunción, Paraguay.").openPopup();
