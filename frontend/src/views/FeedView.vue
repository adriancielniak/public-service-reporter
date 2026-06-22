<template>
  <section class="feed">
    <div class="feed-header">
      <p class="eyebrow">Wszyscy mieszkańcy</p>
      <h1>Feed problemów</h1>
      <p class="lead">Kliknij zgłoszenie aby zobaczyć je na mapie.</p>
    </div>

    <div class="feed-body">
      <!-- Lista -->
      <div class="feed-list-panel">
        <p v-if="loading" class="hint">Ładowanie...</p>
        <p v-if="loadError" class="error">{{ loadError }}</p>

        <ul v-if="!loading && reports.length" class="feed-list">
          <li
            v-for="report in reports"
            :key="report.id"
            :data-report-id="report.id"
            class="feed-item"
            :class="{ active: report.id === focusedId }"
            @click="focusReport(report)"
          >
            <div class="feed-content">
              <p class="report-text">{{ report.content }}</p>
              <p class="report-meta">
                {{ formatDate(report.created_at) }}
                <span v-if="report.latitude"> · 📍</span>
              </p>
            </div>
            <button
              class="confirm-btn"
              :class="{ confirmed: report.user_has_liked, own: report.user_id === currentUserId }"
              :disabled="report.user_id === currentUserId"
              :title="report.user_id === currentUserId ? 'Nie możesz potwierdzić własnego zgłoszenia' : ''"
              @click.stop="handleLike(report.id)"
            >
              <span v-if="report.user_has_liked">✓ {{ report.likes }}</span>
              <span v-else>✓ {{ report.likes }}</span>
            </button>
          </li>
        </ul>

        <p v-if="!loading && !reports.length" class="hint">
          Brak zgłoszeń.
        </p>
      </div>

      <!-- Mapa -->
      <div class="feed-map-panel">
        <ReportsMap
          :reports="reports"
          :focusedReportId="focusedId"
          @reportClick="focusById"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import api, { currentUserId } from "../services/api";
import ReportsMap from "../components/ReportsMap.vue";

const reports = ref([]);
const loading = ref(false);
const loadError = ref("");
const focusedId = ref(null);

const fetchReports = async () => {
  loadError.value = "";
  loading.value = true;
  try {
    const response = await api.get("/api/reports/all/");
    reports.value = Array.isArray(response.data) ? response.data : [];
  } catch {
    loadError.value = "Nie udało się pobrać problemów.";
  } finally {
    loading.value = false;
  }
};

const focusReport = (report) => {
  focusedId.value = report.id;
};

const focusById = (id) => {
  focusedId.value = id;
  const el = document.querySelector(`[data-report-id="${id}"]`);
  el?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
};

const handleLike = async (reportId) => {
  try {
    const response = await api.post(`/api/reports/${reportId}/like/`);
    const index = reports.value.findIndex((r) => r.id === reportId);
    if (index !== -1) {
      reports.value[index] = response.data;
      reports.value.sort((a, b) => b.likes - a.likes || new Date(b.created_at) - new Date(a.created_at));
    }
  } catch {
    // ignoruj
  }
};

const formatDate = (value) => {
  if (!value) return "-";
  return new Date(value).toLocaleString("pl-PL", {
    day: "2-digit", month: "2-digit", year: "numeric",
    hour: "2-digit", minute: "2-digit"
  });
};

onMounted(fetchReports);
</script>

<style scoped>
.feed {
  display: grid;
  gap: 20px;
}

.feed-header {
  display: grid;
  gap: 4px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: 12px;
  color: var(--ink-muted);
  margin: 0;
}

.lead {
  font-size: 15px;
  color: var(--ink-muted);
  margin: 0;
}

.feed-body {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 20px;
  align-items: start;
}

/* Lista */
.feed-list-panel {
  display: grid;
  gap: 12px;
  max-height: 600px;
  overflow-y: auto;
  padding-right: 4px;
}

.feed-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 10px;
}

.feed-item {
  background: var(--surface);
  border-radius: 14px;
  padding: 14px 16px;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.feed-item:hover {
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.14);
}

.feed-item.active {
  border-color: var(--accent);
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.18);
}

.feed-content {
  flex: 1;
  min-width: 0;
}

.report-text {
  margin: 0 0 6px;
  font-weight: 600;
  font-size: 14px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.report-meta {
  margin: 0;
  color: var(--ink-muted);
  font-size: 11px;
}

/* Przycisk potwierdzenia */
.confirm-btn {
  flex-shrink: 0;
  border: 1px solid rgba(15, 23, 42, 0.15);
  border-radius: 10px;
  background: #fff;
  padding: 6px 10px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 700;
  transition: all 0.2s ease;
  color: var(--ink-muted);
}

.confirm-btn:hover:not(:disabled) {
  background: #f0faf5;
  border-color: #28a745;
  color: #28a745;
}

.confirm-btn.confirmed {
  background: #f0faf5;
  border-color: #28a745;
  color: #28a745;
  cursor: pointer;
}

.confirm-btn.own {
  opacity: 0.35;
  cursor: not-allowed;
}

/* Mapa */
.feed-map-panel {
  position: sticky;
  top: 20px;
  height: 600px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(15, 23, 42, 0.12);
}

.hint {
  color: var(--ink-muted);
  margin: 0;
  font-size: 14px;
}

.error {
  color: #c0362c;
  font-weight: 600;
  font-size: 14px;
}

@media (max-width: 768px) {
  .feed-body {
    grid-template-columns: 1fr;
  }

  .feed-map-panel {
    position: static;
    height: 320px;
  }
}
</style>
