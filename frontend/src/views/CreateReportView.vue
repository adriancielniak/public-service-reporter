<template>
  <section class="create-report">
    <form class="card" @submit.prevent="handleCreate">
      <p class="eyebrow">Nowy raport</p>
      <h1>Zgłoś problem</h1>
      <p class="lead">Dodaj nowe zgłoszenie z lokalizacją.</p>

      <label class="field">
        <span>Treść</span>
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
        <span v-else>Dodaj zgłoszenie</span>
      </button>
    </form>
  </section>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";
import MapaPicker from "../components/MapaPicker.vue";

const router = useRouter();

const newReport = ref("");
const newReportLocation = ref({
  latitude: null,
  longitude: null,
  address: ""
});
const creating = ref(false);
const createError = ref("");
const createSuccess = ref("");

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
      newReport.value = "";
      newReportLocation.value = {
        latitude: null,
        longitude: null,
        address: ""
      };
      createSuccess.value = "Zgłoszenie dodane pomyślnie!";
      setTimeout(() => {
        router.push({ name: "feed" });
      }, 1500);
    }
  } catch (err) {
    createError.value = "Nie udało się dodać zgłoszenia.";
  } finally {
    creating.value = false;
  }
};

const handleLocationSelected = (location) => {
  newReportLocation.value = {
    latitude: location.latitude,
    longitude: location.longitude,
    address: location.address
  };
  createError.value = "";
};
</script>

<style scoped>
.create-report {
  display: grid;
  gap: 0;
  max-width: 600px;
  margin: 0 auto;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: 12px;
  color: var(--ink-muted);
  margin: 0 0 8px;
}

.lead {
  font-size: 15px;
  color: var(--ink-muted);
  margin: 0 0 4px;
}

.card {
  background: var(--surface);
  border-radius: 18px;
  padding: 28px;
  box-shadow: 0 20px 40px rgba(15, 23, 42, 0.12);
  display: grid;
  gap: 16px;
}

.card h1 {
  margin: 0;
  font-size: 22px;
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

.location-selected {
  color: #28a745;
  font-weight: 600;
  padding: 12px;
  background: #f0f8f5;
  border-radius: 8px;
  margin: 0;
}

.error {
  color: #c0362c;
  font-weight: 600;
  padding: 12px;
  background: #fdf0f0;
  border-radius: 8px;
  margin: 0;
}

.success {
  color: #28a745;
  font-weight: 600;
  padding: 12px;
  background: #f0f8f5;
  border-radius: 8px;
  margin: 0;
}
</style>
