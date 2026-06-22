<template>
  <div ref="mapEl" class="reports-map"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const props = defineProps({
  reports: { type: Array, default: () => [] },
  focusedReportId: { type: Number, default: null }
});

const emit = defineEmits(['reportClick']);

const mapEl = ref(null);
let map = null;
const markerMap = {};

const createIcon = (active = false) => L.divIcon({
  className: '',
  html: `<div class="map-pin${active ? ' map-pin--active' : ''}"></div>`,
  iconSize: [16, 16],
  iconAnchor: [8, 8],
  popupAnchor: [0, -12]
});

const buildPopup = (report) => {
  const preview = report.content.length > 90
    ? report.content.substring(0, 90) + '…'
    : report.content;
  return `<div style="max-width:200px">
    <strong style="font-size:13px;line-height:1.4">${preview}</strong>
    <br><span style="color:#28a745;font-size:12px;font-weight:600">✓ ${report.likes} potwierdzeń</span>
  </div>`;
};

const addMarker = (report) => {
  if (!report.latitude || !report.longitude) return;

  const marker = L.marker([report.latitude, report.longitude], { icon: createIcon() })
    .addTo(map)
    .bindPopup(buildPopup(report));

  marker.on('click', () => emit('reportClick', report.id));
  markerMap[report.id] = marker;
};

onMounted(() => {
  map = L.map(mapEl.value, { zoomControl: true }).setView([50.0647, 19.945], 12);

  // CartoDB Positron — czysty, jasny styl
  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> © <a href="https://carto.com/">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 20
  }).addTo(map);

  props.reports.forEach(addMarker);
});

watch(() => props.reports, (newReports) => {
  Object.values(markerMap).forEach(m => m.remove());
  Object.keys(markerMap).forEach(k => delete markerMap[k]);
  newReports.forEach(addMarker);
}, { deep: true });

watch(() => props.focusedReportId, (id, prevId) => {
  if (prevId && markerMap[prevId]) {
    markerMap[prevId].setIcon(createIcon(false));
  }
  if (id && markerMap[id]) {
    markerMap[id].setIcon(createIcon(true));
    map.flyTo(markerMap[id].getLatLng(), 16, { duration: 0.7 });
    markerMap[id].openPopup();
  }
});
</script>

<style scoped>
.reports-map {
  width: 100%;
  height: 100%;
  min-height: 520px;
  border-radius: 16px;
  overflow: hidden;
}
</style>

<style>
.map-pin {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #0f172a;
  border: 2.5px solid #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.35);
  transition: transform 0.15s ease;
}

.map-pin--active {
  background: #16a34a;
  border-color: #fff;
  transform: scale(1.5);
  box-shadow: 0 3px 10px rgba(22, 163, 74, 0.5);
}
</style>
