<template>
  <div class="mapa-picker">
    <h3>Lokalizacja zgłoszenia</h3>
    
    <div class="mapa-input-group">
      <label class="field">
        <span>Adres</span>
        <input
          v-model.trim="address"
          type="text"
          placeholder="Wpisz adres (np. Kraków, ul. Floriańska 1)"
          @keyup.enter="searchAddress"
        />
      </label>
      <button type="button" @click="searchAddress" class="btn-search">
        Szukaj
      </button>
    </div>

    <button type="button" @click="getUserLocation" class="btn-location">
      📍 Moja lokalizacja
    </button>

    <!-- Mapa -->
    <div id="mapa-container" class="mapa-container"></div>

    <!-- Wyświetlenie wybranych koordynat -->
    <div v-if="selectedLocation" class="location-info">
      <p><strong>Szerokość:</strong> {{ selectedLocation.lat.toFixed(6) }}</p>
      <p><strong>Długość:</strong> {{ selectedLocation.lng.toFixed(6) }}</p>
      <button type="button" @click="saveLocation" class="btn-save">
        Zatwierdź lokalizację
      </button>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const props = defineProps({
  latitude: Number,
  longitude: Number
});

const emit = defineEmits(['locationSelected']);

const address = ref('');
const selectedLocation = ref(null);
const error = ref('');
const success = ref('');
let map = null;
let marker = null;

// Inicjalizacja mapy
onMounted(() => {
  // Domyślna lokalizacja (Kraków)
  const defaultLat = props.latitude || 50.0647;
  const defaultLng = props.longitude || 19.9450;

  map = L.map('mapa-container').setView([defaultLat, defaultLng], 13);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map);

  // Dodanie markera jeśli są już koordynaty
  if (props.latitude && props.longitude) {
    addMarker(props.latitude, props.longitude);
    selectedLocation.value = {
      lat: props.latitude,
      lng: props.longitude
    };
  }

  // Klik na mapę - dodanie markera
  map.on('click', (e) => {
    addMarker(e.latlng.lat, e.latlng.lng);
  });
});

// Dodanie lub przeniesienie markera
const addMarker = (lat, lng) => {
  if (marker) {
    map.removeLayer(marker);
  }

  marker = L.marker([lat, lng])
    .addTo(map)
    .bindPopup(`Szerokość: ${lat.toFixed(6)}<br>Długość: ${lng.toFixed(6)}`);

  selectedLocation.value = { lat, lng };
  map.setView([lat, lng], 15);
};

// Wyszukiwanie adresu
const searchAddress = async () => {
  if (!address.value.trim()) {
    error.value = 'Wpisz adres';
    return;
  }

  try {
    error.value = '';
    success.value = '';

    // Używamy Nominatim API (OpenStreetMap)
    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address.value)}`
    );
    const results = await response.json();

    if (results.length === 0) {
      error.value = 'Nie znaleziono adresu';
      return;
    }

    const result = results[0];
    const lat = parseFloat(result.lat);
    const lng = parseFloat(result.lon);

    addMarker(lat, lng);
    success.value = `Znaleziono: ${result.display_name}`;
  } catch (err) {
    error.value = 'Błąd wyszukiwania: ' + err.message;
  }
};

// Pobranie lokalizacji użytkownika
const getUserLocation = () => {
  error.value = '';
  success.value = '';

  if (!navigator.geolocation) {
    error.value = 'Geolokalizacja nie jest dostępna w Twojej przeglądarce';
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude } = position.coords;
      addMarker(latitude, longitude);
      
      // Odwrotne geocodowanie (koordynaty -> adres)
      reverseGeocode(latitude, longitude);
      success.value = 'Lokalizacja pobrana!';
    },
    (err) => {
      error.value = 'Nie udało się pobrać lokalizacji: ' + err.message;
    }
  );
};

// Odwrotne geocodowanie
const reverseGeocode = async (lat, lng) => {
  try {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`
    );
    const result = await response.json();
    if (result.address) {
      address.value = result.display_name || result.address.road || 'Lokalizacja pobrana';
    }
  } catch (err) {
    console.error('Błąd reverse geocode:', err);
  }
};

// Zapis lokalizacji
const saveLocation = () => {
  if (!selectedLocation.value) {
    error.value = 'Wybierz lokalizację na mapie';
    return;
  }

  emit('locationSelected', {
    latitude: selectedLocation.value.lat,
    longitude: selectedLocation.value.lng,
    address: address.value
  });

  success.value = 'Lokalizacja zatwierdzona!';
};
</script>

<style scoped>
.mapa-picker {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

h3 {
  margin: 0;
  font-size: 1.2rem;
}

.mapa-input-group {
  display: flex;
  gap: 0.5rem;
}

.mapa-input-group .field {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin: 0;
}

.mapa-input-group input {
  padding: 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 0.5rem;
  font-size: 1rem;
}

.btn-search,
.btn-location,
.btn-save {
  padding: 0.75rem 1.5rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s;
}

.btn-search:hover,
.btn-location:hover,
.btn-save:hover {
  background-color: #0056b3;
}

.btn-location {
  align-self: flex-start;
  background-color: #28a745;
}

.btn-location:hover {
  background-color: #218838;
}

.btn-save {
  background-color: #17a2b8;
}

.btn-save:hover {
  background-color: #138496;
}

.mapa-container {
  width: 100%;
  height: 400px;
  border: 1px solid #e0e0e0;
  border-radius: 0.5rem;
  z-index: 1;
}

.location-info {
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 0.5rem;
  border-left: 4px solid #17a2b8;
}

.location-info p {
  margin: 0.5rem 0;
  font-size: 0.95rem;
}

.error {
  color: #dc3545;
  padding: 0.75rem;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 0.5rem;
  margin: 0;
}

.success {
  color: #155724;
  padding: 0.75rem;
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
  border-radius: 0.5rem;
  margin: 0;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.field span {
  font-weight: 500;
  font-size: 0.95rem;
}
</style>
