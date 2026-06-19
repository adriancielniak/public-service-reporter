<template>
  <section class="dashboard">
    <header class="dashboard-header">
      <div>
        <p class="eyebrow">Twoje zgloszenia</p>
        <h1>Panel zgloszen</h1>
        <p class="lead">Dodawaj nowe raporty i sprawdz historie.</p>
      </div>
      <button class="ghost" type="button" @click="handleLogout">Wyloguj</button>
    </header>

    <div class="dashboard-grid">
      <form class="card" @submit.prevent="handleCreate">
        <h2>Nowe zgloszenie</h2>
        <p class="hint">Opisz problem w kilku zdaniach.</p>

        <label class="field">
          <span>Tresc</span>
          <textarea
            v-model.trim="newReport"
            rows="5"
            placeholder="np. uszkodzona latarnia na ulicy..."
            required
          ></textarea>
        </label>

        <!-- Komponent mapy do wyboru lokalizacji -->
        <MapaPicker
          @locationSelected="handleLocationSelected"
          :latitude="newReportLocation.latitude"
          :longitude="newReportLocation.longitude"
        />

        <p v-if="newReportLocation.latitude" class="location-selected">
          ✓ Lokalizacja wybrana: ({{ newReportLocation.latitude.toFixed(6) }}, {{ newReportLocation.longitude.toFixed(6) }})
        </p>

        <p v-if="createError" class="error">{{ createError }}</p>
        <p v-if="createSuccess" class="success">{{ createSuccess }}</p>

        <button type="submit" :disabled="creating">
          <span v-if="creating">Zapisywanie...</span>
          <span v-else>Dodaj zgloszenie</span>
        </button>
      </form>

      <div class="card">
        <div class="card-header">
          <h2>Historia</h2>
          <button class="ghost" type="button" @click="fetchReports">
            Odswiez
          </button>
        </div>

        <p v-if="loading" class="hint">Ladowanie raportow...</p>
        <p v-if="loadError" class="error">{{ loadError }}</p>

        <ul v-if="!loading && reports.length" class="report-list">
          <li v-for="report in reports" :key="report.id" class="report-item">
            <div>
              <p class="report-content">{{ report.content }}</p>
              <p class="report-meta">
                {{ formatDate(report.created_at) }} · ID {{ report.id }}
              </p>
            </div>
          </li>
        </ul>

        <p v-if="!loading && !reports.length" class="hint">
          Brak zgloszen. Dodaj pierwsze raporty.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import api, { clearToken } from "../services/api";
import MapaPicker from "../components/MapaPicker.vue";

const router = useRouter();

const reports = ref([]);
const loading = ref(false);
const loadError = ref("");

const newReport = ref("");
const newReportLocation = ref({
  latitude: null,
  longitude: null,
  address: ""
});
const creating = ref(false);
const createError = ref("");
const createSuccess = ref("");

const fetchReports = async () => {
  loadError.value = "";
  loading.value = true;

  try {
    const response = await api.get("/api/reports/");
    reports.value = Array.isArray(response.data) ? response.data : [];
  } catch (err) {
    loadError.value = "Nie udalo sie pobrac zgloszen.";
  } finally {
    loading.value = false;
  }
};

const handleCreate = async () => {
  createError.value = "";
  createSuccess.value = "";
  creating.value = true;

  try {
    const response = await api.post("/api/reports/create/", {
      content: newReport.value,
      latitude: newReportLocation.value.latitude,
      longitude: newReportLocation.value.longitude
    });

    if (response.data) {
      reports.value = [response.data, ...reports.value];
    }

    newReport.value = "";
    newReportLocation.value = {
      latitude: null,
      longitude: null,
      address: ""
    };
    createSuccess.value = "Zgloszenie dodane.";
  } catch (err) {
    createError.value = "Nie udalo sie dodac zgloszenia.";
  } finally {
    creating.value = false;
  }
};

const handleLogout = async () => {
  clearToken();
  await router.push({ name: "login" });
};

const handleLocationSelected = (location) => {
  newReportLocation.value = {
    latitude: location.latitude,
    longitude: location.longitude,
    address: location.address
  };
  createError.value = "";
};

const formatDate = (value) => {
  if (!value) return "-";
  const date = new Date(value);
  return date.toLocaleString("pl-PL", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  });
};

onMounted(fetchReports);
</script>

<style scoped>
.dashboard {
  display: grid;
  gap: 24px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: 12px;
  color: var(--ink-muted);
  margin: 0 0 12px;
}

.lead {
  font-size: 16px;
  color: var(--ink-muted);
  margin: 0;
}

.card {
  background: var(--surface);
  border-radius: 18px;
  padding: 24px;
  box-shadow: 0 20px 40px rgba(15, 23, 42, 0.12);
  display: grid;
  gap: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hint {
  color: var(--ink-muted);
  margin: 0;
}

.field {
  display: grid;
  gap: 8px;
  font-weight: 500;
}

.field textarea {
  border: 1px solid rgba(15, 23, 42, 0.15);
  border-radius: 12px;
  padding: 12px 14px;
  font-size: 14px;
  background: #fff;
  font-family: inherit;
  resize: vertical;
}

button {
  border: none;
  border-radius: 12px;
  background: var(--accent);
  color: var(--ink-inverse);
  font-weight: 600;
  padding: 12px 16px;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

button:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 30px rgba(15, 23, 42, 0.2);
}

.ghost {
  background: transparent;
  color: var(--accent);
  border: 1px solid rgba(15, 23, 42, 0.15);
  box-shadow: none;
}

.report-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 12px;
}

.report-item {
  padding: 12px 14px;
  border-radius: 12px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  background: rgba(255, 255, 255, 0.7);
}

.report-content {
  margin: 0 0 8px;
  font-weight: 600;
}

.report-meta {
  margin: 0;
  color: var(--ink-muted);
  font-size: 12px;
}

.error {
  color: #c0362c;
  font-weight: 600;
}

.success {
  color: #1b7f4b;
  font-weight: 600;
}

.location-selected {
  color: #1b7f4b;
  font-size: 0.9rem;
  margin: 0;
  padding: 0.75rem;
  background-color: #d4edda;
  border-left: 3px solid #1b7f4b;
  border-radius: 0.25rem;
}

@media (max-width: 720px) {
  .dashboard-header {
    flex-direction: column;
  }
}
</style>
