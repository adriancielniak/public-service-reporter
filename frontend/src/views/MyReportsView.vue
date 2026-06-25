<template>
  <section class="my-reports">
    <p class="eyebrow">Twoje zgłoszenia</p>
    <h1>Moje problemy</h1>
    <p class="lead">Historia Twoich zgłoszonych problemów.</p>

    <div class="reports-container">
      <p v-if="loading" class="hint">Ładowanie Twoich raportów...</p>
      <p v-if="loadError" class="error">{{ loadError }}</p>

      <ul v-if="!loading && reports.length" class="reports-list">
        <li v-for="report in reports" :key="report.id" class="report-item">
          <div class="report-row">
            <p class="report-content">{{ report.content }}</p>
            <span :class="`status-badge status-badge--${report.status}`">{{ STATUS_LABELS[report.status] }}</span>
          </div>
          <p class="report-meta">
            {{ formatDate(report.created_at) }} · ID {{ report.id }}
          </p>
          <p v-if="report.latitude" class="location-info">
            📍 {{ report.latitude.toFixed(4) }}, {{ report.longitude.toFixed(4) }}
          </p>
          <p class="likes-info">✓ {{ report.likes }} potwierdzeń</p>

          <div v-if="report.admin_comments && report.admin_comments.length" class="admin-comments">
            <p class="comments-label">Komentarze urzędu</p>
            <div v-for="c in report.admin_comments" :key="c.id" class="admin-comment">
              <p class="comment-text">{{ c.text }}</p>
              <p class="comment-meta">{{ c.author_username }} · {{ formatDate(c.created_at) }}</p>
            </div>
          </div>
        </li>
      </ul>

      <p v-if="!loading && !reports.length" class="hint">
        Brak Twoich zgłoszeń. Dodaj pierwsze raporty.
      </p>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";

const STATUS_LABELS = {
  new: 'Nowe',
  in_progress: 'W realizacji',
  resolved: 'Rozwiązane',
  rejected: 'Odrzucone',
};
import api from "../services/api";

const reports = ref([]);
const loading = ref(false);
const loadError = ref("");

const fetchReports = async () => {
  loadError.value = "";
  loading.value = true;

  try {
    const response = await api.get("/api/reports/");
    reports.value = Array.isArray(response.data) ? response.data : [];
  } catch (err) {
    loadError.value = "Nie udało się pobrać Twoich zgłoszeń.";
  } finally {
    loading.value = false;
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
.my-reports {
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


.reports-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 12px;
}

.report-item {
  padding: 16px;
  border-radius: 12px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  background: rgba(255, 255, 255, 0.7);
}

.report-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 6px;
}

.report-content {
  margin: 0;
  font-weight: 600;
  font-size: 15px;
}

.report-meta {
  margin: 0 0 6px;
  color: var(--ink-muted);
  font-size: 12px;
}

.location-info {
  margin: 4px 0;
  color: #666;
  font-size: 13px;
}

.likes-info {
  margin: 4px 0 0;
  color: #22c55e;
  font-weight: 700;
  font-size: 13px;
}

.status-badge {
  flex-shrink: 0;
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
}
.status-badge--new        { background: #dbeafe; color: #1d4ed8; }
.status-badge--in_progress{ background: #fef3c7; color: #92400e; }
.status-badge--resolved   { background: #dcfce7; color: #166534; }
.status-badge--rejected   { background: #fee2e2; color: #991b1b; }

.admin-comments {
  margin-top: 10px;
  border-top: 1px solid rgba(15, 23, 42, 0.08);
  padding-top: 10px;
  display: grid;
  gap: 8px;
}

.comments-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #7c3aed;
  margin: 0 0 4px;
}

.admin-comment {
  background: #faf5ff;
  border-left: 3px solid #7c3aed;
  padding: 8px 10px;
  border-radius: 0 8px 8px 0;
}

.comment-text {
  margin: 0 0 4px;
  font-size: 13px;
}

.comment-meta {
  margin: 0;
  font-size: 11px;
  color: var(--ink-muted);
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
