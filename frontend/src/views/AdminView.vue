<template>
  <section class="admin">
    <div class="admin-header">
      <p class="eyebrow">Panel administracyjny</p>
      <h1>Zarządzanie zgłoszeniami</h1>
    </div>

    <!-- Statystyki -->
    <div class="stats-row">
      <div class="stat-card">
        <p class="stat-value">{{ stats.total }}</p>
        <p class="stat-label">Wszystkich</p>
      </div>
      <div class="stat-card stat-card--new">
        <p class="stat-value">{{ stats.new }}</p>
        <p class="stat-label">Nowych</p>
      </div>
      <div class="stat-card stat-card--progress">
        <p class="stat-value">{{ stats.in_progress }}</p>
        <p class="stat-label">W realizacji</p>
      </div>
      <div class="stat-card stat-card--resolved">
        <p class="stat-value">{{ stats.resolved }}</p>
        <p class="stat-label">Rozwiązanych</p>
      </div>
      <div class="stat-card stat-card--rejected">
        <p class="stat-value">{{ stats.rejected }}</p>
        <p class="stat-label">Odrzuconych</p>
      </div>
    </div>

    <!-- Filtry -->
    <div class="filters">
      <button
        v-for="f in filterOptions"
        :key="f.value"
        class="filter-btn"
        :class="{ active: activeFilter === f.value }"
        @click="setFilter(f.value)"
      >
        {{ f.label }}
      </button>
    </div>

    <!-- Lista -->
    <div v-if="loading" class="hint">Ładowanie...</div>
    <div v-if="loadError" class="error">{{ loadError }}</div>

    <ul v-if="!loading && filtered.length" class="report-list">
      <li v-for="report in filtered" :key="report.id" class="report-card">

        <!-- Nagłówek karty -->
        <div class="report-card-header">
          <div class="report-meta">
            <span class="report-id">#{{ report.id }}</span>
            <span class="report-author">{{ report.username || 'Anonim' }}</span>
            <span class="report-date">{{ formatDate(report.created_at) }}</span>
            <span class="confirm-count">✓ {{ report.likes }}</span>
          </div>
          <select
            class="status-select"
            :class="`status-select--${report.status}`"
            :value="report.status"
            @change="updateStatus(report, $event.target.value)"
          >
            <option value="new">Nowe</option>
            <option value="in_progress">W realizacji</option>
            <option value="resolved">Rozwiązane</option>
            <option value="rejected">Odrzucone</option>
          </select>
        </div>

        <!-- Treść -->
        <p class="report-content">{{ report.content }}</p>
        <p v-if="report.latitude" class="report-location">
          📍 {{ report.latitude.toFixed(4) }}, {{ report.longitude.toFixed(4) }}
        </p>

        <!-- Historia statusów -->
        <div v-if="report.status_history.length" class="history">
          <p class="section-label">Historia statusów</p>
          <div v-for="h in report.status_history" :key="h.changed_at" class="history-item">
            <span :class="`badge badge--${h.old_status}`">{{ statusLabel(h.old_status) }}</span>
            <span class="arrow">→</span>
            <span :class="`badge badge--${h.new_status}`">{{ statusLabel(h.new_status) }}</span>
            <span class="history-meta">{{ h.changed_by_username }} · {{ formatDate(h.changed_at) }}</span>
          </div>
        </div>

        <!-- Komentarze admina -->
        <div v-if="report.admin_comments.length" class="comments">
          <p class="section-label">Komentarze</p>
          <div v-for="c in report.admin_comments" :key="c.id" class="comment-item">
            <span class="comment-author">{{ c.author_username }}</span>
            <span class="comment-date">{{ formatDate(c.created_at) }}</span>
            <p class="comment-text">{{ c.text }}</p>
          </div>
        </div>

        <!-- Dodaj komentarz -->
        <div class="add-comment">
          <textarea
            v-model="commentDraft[report.id]"
            class="comment-input"
            rows="2"
            placeholder="Dodaj komentarz do zgłoszenia..."
          ></textarea>
          <button
            class="comment-submit"
            :disabled="!commentDraft[report.id]?.trim()"
            @click="addComment(report)"
          >
            Dodaj
          </button>
        </div>

      </li>
    </ul>

    <p v-if="!loading && !filtered.length" class="hint">Brak zgłoszeń dla wybranego filtra.</p>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue';
import api from '../services/api';

const reports = ref([]);
const loading = ref(false);
const loadError = ref('');
const activeFilter = ref('all');
const commentDraft = reactive({});

const filterOptions = [
  { value: 'all', label: 'Wszystkie' },
  { value: 'new', label: 'Nowe' },
  { value: 'in_progress', label: 'W realizacji' },
  { value: 'resolved', label: 'Rozwiązane' },
  { value: 'rejected', label: 'Odrzucone' },
];

const STATUS_LABELS = {
  new: 'Nowe',
  in_progress: 'W realizacji',
  resolved: 'Rozwiązane',
  rejected: 'Odrzucone',
};

const statusLabel = (s) => STATUS_LABELS[s] || s;

const stats = computed(() => ({
  total: reports.value.length,
  new: reports.value.filter(r => r.status === 'new').length,
  in_progress: reports.value.filter(r => r.status === 'in_progress').length,
  resolved: reports.value.filter(r => r.status === 'resolved').length,
  rejected: reports.value.filter(r => r.status === 'rejected').length,
}));

const filtered = computed(() =>
  activeFilter.value === 'all'
    ? reports.value
    : reports.value.filter(r => r.status === activeFilter.value)
);

const setFilter = (val) => { activeFilter.value = val; };

const fetchReports = async () => {
  loading.value = true;
  loadError.value = '';
  try {
    const res = await api.get('/api/admin/reports/');
    reports.value = res.data;
  } catch {
    loadError.value = 'Nie udało się pobrać zgłoszeń.';
  } finally {
    loading.value = false;
  }
};

const updateStatus = async (report, newStatus) => {
  try {
    const res = await api.patch(`/api/admin/reports/${report.id}/status/`, { status: newStatus });
    const idx = reports.value.findIndex(r => r.id === report.id);
    if (idx !== -1) reports.value[idx] = res.data;
  } catch {
    // ignoruj
  }
};

const addComment = async (report) => {
  const text = commentDraft[report.id]?.trim();
  if (!text) return;
  try {
    const res = await api.post(`/api/admin/reports/${report.id}/comments/`, { text });
    const idx = reports.value.findIndex(r => r.id === report.id);
    if (idx !== -1) reports.value[idx].admin_comments.push(res.data);
    commentDraft[report.id] = '';
  } catch {
    // ignoruj
  }
};

const formatDate = (value) => {
  if (!value) return '-';
  return new Date(value).toLocaleString('pl-PL', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
};

onMounted(fetchReports);
</script>

<style scoped>
.admin {
  display: grid;
  gap: 24px;
}

.admin-header { display: grid; gap: 4px; }

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: 12px;
  color: var(--ink-muted);
  margin: 0;
}

/* Stats */
.stats-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.stat-card {
  flex: 1;
  min-width: 100px;
  background: var(--surface);
  border-radius: 14px;
  padding: 16px 20px;
  box-shadow: 0 2px 8px rgba(15,23,42,.08);
  border-left: 4px solid #94a3b8;
}
.stat-card--new        { border-left-color: #3b82f6; }
.stat-card--progress   { border-left-color: #f59e0b; }
.stat-card--resolved   { border-left-color: #22c55e; }
.stat-card--rejected   { border-left-color: #ef4444; }

.stat-value { font-size: 28px; font-weight: 700; margin: 0; }
.stat-label { font-size: 12px; color: var(--ink-muted); margin: 4px 0 0; }

/* Filtry */
.filters { display: flex; gap: 8px; flex-wrap: wrap; }

.filter-btn {
  padding: 7px 16px;
  border-radius: 999px;
  border: 1px solid rgba(15,23,42,.15);
  background: #fff;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  color: var(--ink-muted);
  transition: all .15s;
}
.filter-btn.active {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}

/* Lista */
.report-list { list-style: none; margin: 0; padding: 0; display: grid; gap: 16px; }

.report-card {
  background: var(--surface);
  border-radius: 16px;
  padding: 20px 24px;
  box-shadow: 0 2px 12px rgba(15,23,42,.09);
  display: grid;
  gap: 14px;
}

.report-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.report-meta { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
.report-id   { font-weight: 700; color: var(--ink-muted); font-size: 13px; }
.report-author { font-weight: 600; font-size: 13px; }
.report-date { color: var(--ink-muted); font-size: 12px; }
.confirm-count { color: #22c55e; font-weight: 700; font-size: 13px; }

.report-content { margin: 0; font-size: 15px; line-height: 1.5; }
.report-location { margin: 0; font-size: 12px; color: var(--ink-muted); }

/* Status select */
.status-select {
  padding: 6px 10px;
  border-radius: 8px;
  border: 1.5px solid rgba(15,23,42,.2);
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  background: #fff;
}
.status-select--new        { border-color: #3b82f6; color: #3b82f6; }
.status-select--in_progress{ border-color: #f59e0b; color: #d97706; }
.status-select--resolved   { border-color: #22c55e; color: #16a34a; }
.status-select--rejected   { border-color: #ef4444; color: #dc2626; }

/* Historia */
.section-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: var(--ink-muted); margin: 0 0 8px; }

.history { display: grid; gap: 6px; }
.history-item { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.arrow { color: var(--ink-muted); }
.history-meta { font-size: 11px; color: var(--ink-muted); }

.badge {
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
}
.badge--new        { background: #dbeafe; color: #1d4ed8; }
.badge--in_progress{ background: #fef3c7; color: #92400e; }
.badge--resolved   { background: #dcfce7; color: #166534; }
.badge--rejected   { background: #fee2e2; color: #991b1b; }

/* Komentarze */
.comments { display: grid; gap: 8px; }
.comment-item { background: #f8fafc; border-radius: 10px; padding: 10px 14px; display: grid; gap: 4px; }
.comment-author { font-weight: 700; font-size: 12px; color: var(--accent); }
.comment-date   { font-size: 11px; color: var(--ink-muted); }
.comment-text   { margin: 0; font-size: 14px; }

/* Dodaj komentarz */
.add-comment { display: flex; gap: 10px; align-items: flex-start; }

.comment-input {
  flex: 1;
  border: 1px solid rgba(15,23,42,.15);
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 13px;
  font-family: inherit;
  resize: vertical;
}

.comment-submit {
  border: none;
  border-radius: 10px;
  background: var(--accent);
  color: #fff;
  font-weight: 600;
  padding: 10px 18px;
  cursor: pointer;
  white-space: nowrap;
}
.comment-submit:disabled { opacity: .4; cursor: not-allowed; }

.hint  { color: var(--ink-muted); font-size: 14px; }
.error { color: #c0362c; font-weight: 600; }
</style>
