<template>
  <section class="feed">
    <p class="eyebrow">Wszyscy mieszkańcy</p>
    <h1>Feed problemów</h1>
    <p class="lead">Zobacz problemy w gminie posortowane po popularności.</p>

    <div class="feed-container">
      <p v-if="loading" class="hint">Ładowanie problemów...</p>
      <p v-if="loadError" class="error">{{ loadError }}</p>

      <ul v-if="!loading && reports.length" class="feed-list">
        <li v-for="report in reports" :key="report.id" class="feed-item">
          <div class="feed-content">
            <p class="report-text">{{ report.content }}</p>
            <p class="report-meta">
              {{ formatDate(report.created_at) }} · ID {{ report.id }}
            </p>
            <p v-if="report.latitude" class="location-info">
              📍 {{ report.latitude.toFixed(4) }}, {{ report.longitude.toFixed(4) }}
            </p>
          </div>
          <div class="feed-actions">
            <button
              class="confirm-btn"
              :class="{ confirmed: report.user_has_liked, own: report.user_id === currentUserId }"
              :disabled="report.user_id === currentUserId"
              :title="report.user_id === currentUserId ? 'Nie możesz potwierdzić własnego zgłoszenia' : ''"
              @click="handleLike(report.id)"
            >
              <span v-if="report.user_has_liked">✓ Potwierdzone ({{ report.likes }})</span>
              <span v-else>✓ Potwierdź ({{ report.likes }})</span>
            </button>
          </div>
        </li>
      </ul>

      <p v-if="!loading && !reports.length" class="hint">
        Brak problemów do wyświetlenia.
      </p>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import api, { currentUserId } from "../services/api";

const reports = ref([]);
const loading = ref(false);
const loadError = ref("");

const fetchReports = async () => {
  loadError.value = "";
  loading.value = true;

  try {
    const response = await api.get("/api/reports/all/");
    reports.value = Array.isArray(response.data) ? response.data : [];
  } catch (err) {
    loadError.value = "Nie udało się pobrać problemów.";
  } finally {
    loading.value = false;
  }
};

const handleLike = async (reportId) => {
  try {
    const response = await api.post(`/api/reports/${reportId}/like/`);
    const index = reports.value.findIndex((r) => r.id === reportId);
    if (index !== -1) {
      reports.value[index] = response.data;
      // Ponownie sortuj
      reports.value.sort((a, b) => b.likes - a.likes || new Date(b.created_at) - new Date(a.created_at));
    }
  } catch (err) {
    console.error("Nie udało się polubić problemu");
  }
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
.feed {
  display: grid;
  gap: 24px;
  max-width: 640px;
  margin: 0 auto;
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


.feed-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 16px;
}

.feed-item {
  background: var(--surface);
  border-radius: 18px;
  padding: 20px;
  box-shadow: 0 20px 40px rgba(15, 23, 42, 0.12);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.feed-content {
  flex: 1;
}

.report-text {
  margin: 0 0 12px;
  font-weight: 600;
  font-size: 16px;
}

.report-meta {
  margin: 0 0 8px;
  color: var(--ink-muted);
  font-size: 12px;
}

.location-info {
  margin: 8px 0 0;
  color: #666;
  font-size: 13px;
}

.feed-actions {
  display: flex;
  gap: 8px;
}

.confirm-btn {
  border: 1px solid rgba(15, 23, 42, 0.15);
  border-radius: 12px;
  background: #fff;
  padding: 8px 14px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition: all 0.2s ease;
  white-space: nowrap;
  color: var(--ink-muted);
}

.confirm-btn:hover:not(:disabled) {
  background: #f0faf5;
  border-color: #28a745;
  color: #28a745;
  transform: scale(1.03);
}

.confirm-btn.confirmed {
  background: #f0faf5;
  border-color: #28a745;
  color: #28a745;
  cursor: pointer;
}

.confirm-btn.own {
  opacity: 0.4;
  cursor: not-allowed;
}

button.ghost {
  background: transparent;
  color: var(--accent);
  border: 1px solid rgba(15, 23, 42, 0.15);
  font-weight: 600;
  padding: 12px 16px;
  cursor: pointer;
  border-radius: 12px;
}

.hint {
  color: var(--ink-muted);
  margin: 0;
}

.error {
  color: #c0362c;
  font-weight: 600;
}
</style>
