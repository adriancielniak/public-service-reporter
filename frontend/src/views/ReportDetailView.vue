<template>
  <section class="detail">
    <button class="back-btn" @click="$router.back()">← Wróć</button>

    <div v-if="loading" class="hint">Ładowanie...</div>
    <div v-if="loadError" class="error">{{ loadError }}</div>

    <template v-if="report">
      <!-- Nagłówek -->
      <div class="detail-header">
        <div class="header-meta">
          <span class="report-id">#{{ report.id }}</span>
          <span :class="`status-badge status-badge--${report.status}`">{{ STATUS_LABELS[report.status] }}</span>
        </div>
        <p class="report-date">{{ formatDate(report.created_at) }}</p>
      </div>

      <!-- Treść -->
      <div class="card">
        <p class="section-label">Opis zgłoszenia</p>
        <p class="report-content">{{ report.content }}</p>
        <p v-if="report.latitude" class="location-info">
          📍 {{ report.latitude.toFixed(4) }}, {{ report.longitude.toFixed(4) }}
        </p>
        <p class="confirm-count">✓ {{ report.likes }} potwierdzeń</p>

        <button
          class="confirm-btn"
          :class="{ confirmed: report.user_has_liked, own: report.user_id === currentUserId }"
          :disabled="report.user_id === currentUserId"
          :title="report.user_id === currentUserId ? 'Nie możesz potwierdzić własnego zgłoszenia' : ''"
          @click="handleLike"
        >
          {{ report.user_has_liked ? '✓ Cofnij potwierdzenie' : '✓ Potwierdź problem' }}
        </button>
      </div>

      <!-- Mapa -->
      <div v-if="report.latitude" class="card map-card">
        <p class="section-label">Lokalizacja</p>
        <div ref="mapContainer" class="map"></div>
      </div>

      <!-- Komentarze urzędu -->
      <div class="card" v-if="report.admin_comments && report.admin_comments.length">
        <p class="section-label">Komentarze urzędu</p>
        <div v-for="c in report.admin_comments" :key="c.id" class="admin-comment">
          <p class="comment-text">{{ c.text }}</p>
          <p class="comment-meta">{{ c.author_username }} · {{ formatDate(c.created_at) }}</p>
        </div>
      </div>
      <div class="card empty-comments" v-else>
        <p class="hint">Brak komentarzy urzędu do tego zgłoszenia.</p>
      </div>

      <!-- Komentarze mieszkańców -->
      <div class="card">
        <p class="section-label">Komentarze mieszkańców</p>

        <div v-if="report.user_comments && report.user_comments.length" class="user-comments-list">
          <div v-for="c in report.user_comments" :key="c.id" class="user-comment">
            <div class="user-comment-header">
              <span class="user-comment-author">{{ c.author_username }}</span>
              <span class="user-comment-date">{{ formatDate(c.created_at) }}</span>
              <button v-if="c.is_own" class="delete-btn" @click="deleteComment(c.id)" title="Usuń komentarz">✕</button>
            </div>
            <p class="user-comment-text">{{ c.text }}</p>
          </div>
        </div>
        <p v-else class="hint">Brak komentarzy. Bądź pierwszy!</p>

        <div class="add-user-comment">
          <textarea
            v-model="newComment"
            class="comment-input"
            rows="2"
            placeholder="Napisz komentarz..."
          ></textarea>
          <button class="comment-submit" :disabled="!newComment.trim()" @click="addComment">
            Wyślij
          </button>
        </div>
      </div>

      <!-- Historia statusów -->
      <div class="card" v-if="report.status_history && report.status_history.length">
        <p class="section-label">Historia statusów</p>
        <div v-for="h in report.status_history" :key="h.changed_at" class="history-item">
          <span :class="`status-badge status-badge--${h.old_status}`">{{ STATUS_LABELS[h.old_status] }}</span>
          <span class="arrow">→</span>
          <span :class="`status-badge status-badge--${h.new_status}`">{{ STATUS_LABELS[h.new_status] }}</span>
          <span class="history-meta">{{ h.changed_by_username }} · {{ formatDate(h.changed_at) }}</span>
        </div>
      </div>
    </template>
  </section>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import api, { currentUserId } from '../services/api';

const route = useRoute();
const report = ref(null);
const loading = ref(false);
const loadError = ref('');
const mapContainer = ref(null);
const newComment = ref('');

const STATUS_LABELS = {
  new: 'Nowe',
  in_progress: 'W realizacji',
  resolved: 'Rozwiązane',
  rejected: 'Odrzucone',
};

const fetchReport = async () => {
  loading.value = true;
  loadError.value = '';
  try {
    const res = await api.get(`/api/reports/${route.params.id}/`);
    report.value = res.data;
    if (res.data.latitude) {
      await nextTick();
      initMap(res.data.latitude, res.data.longitude);
    }
  } catch {
    loadError.value = 'Nie udało się pobrać zgłoszenia.';
  } finally {
    loading.value = false;
  }
};

const initMap = (lat, lng) => {
  import('leaflet').then((L) => {
    const map = L.map(mapContainer.value, { zoomControl: true }).setView([lat, lng], 16);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '© OpenStreetMap © CARTO',
      maxZoom: 19,
    }).addTo(map);

    const icon = L.divIcon({ className: 'report-pin', iconSize: [14, 14], iconAnchor: [7, 7] });
    L.marker([lat, lng], { icon }).addTo(map);
  });
};

const addComment = async () => {
  const text = newComment.value.trim();
  if (!text) return;
  try {
    const res = await api.post(`/api/reports/${report.value.id}/comments/`, { text });
    report.value.user_comments.push(res.data);
    newComment.value = '';
  } catch {
    // ignoruj
  }
};

const deleteComment = async (commentId) => {
  try {
    await api.delete(`/api/reports/${report.value.id}/comments/${commentId}/`);
    report.value.user_comments = report.value.user_comments.filter(c => c.id !== commentId);
  } catch {
    // ignoruj
  }
};

const handleLike = async () => {
  try {
    const res = await api.post(`/api/reports/${report.value.id}/like/`);
    report.value = { ...report.value, likes: res.data.likes, user_has_liked: res.data.user_has_liked };
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

onMounted(fetchReport);
</script>

<style scoped>
.detail {
  display: grid;
  gap: 20px;
  max-width: 720px;
  margin: 0 auto;
}

.back-btn {
  justify-self: start;
  background: transparent;
  border: 1px solid rgba(15,23,42,.15);
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  color: var(--ink-muted);
}
.back-btn:hover { color: var(--accent); border-color: var(--accent); }

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.header-meta { display: flex; align-items: center; gap: 10px; }

.report-id { font-weight: 700; color: var(--ink-muted); font-size: 15px; }

.report-date { font-size: 13px; color: var(--ink-muted); }

.card {
  background: var(--surface);
  border-radius: 16px;
  padding: 20px 24px;
  box-shadow: 0 2px 12px rgba(15,23,42,.09);
  display: grid;
  gap: 12px;
}

.section-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--ink-muted);
  margin: 0;
}

.report-content { font-size: 16px; line-height: 1.6; margin: 0; }
.location-info  { font-size: 13px; color: var(--ink-muted); margin: 0; }
.confirm-count  { font-size: 14px; font-weight: 700; color: #22c55e; margin: 0; }

.confirm-btn {
  justify-self: start;
  border: 1.5px solid rgba(15,23,42,.2);
  border-radius: 10px;
  background: #fff;
  padding: 9px 18px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: all .2s;
  color: var(--ink-muted);
}
.confirm-btn:hover:not(:disabled) { background: #f0faf5; border-color: #22c55e; color: #16a34a; }
.confirm-btn.confirmed { background: #f0faf5; border-color: #22c55e; color: #16a34a; }
.confirm-btn.own { opacity: .35; cursor: not-allowed; }

/* Mapa */
.map-card { padding: 20px 24px; }
.map { height: 300px; border-radius: 10px; overflow: hidden; }

/* Komentarze mieszkańców */
.user-comments-list { display: grid; gap: 10px; }

.user-comment {
  background: #f8fafc;
  border-radius: 10px;
  padding: 10px 14px;
  display: grid;
  gap: 4px;
}

.user-comment-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-comment-author { font-weight: 700; font-size: 13px; color: var(--accent); }
.user-comment-date   { font-size: 11px; color: var(--ink-muted); flex: 1; }
.user-comment-text   { margin: 0; font-size: 14px; line-height: 1.5; }

.delete-btn {
  background: transparent;
  border: none;
  color: var(--ink-muted);
  cursor: pointer;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 4px;
  line-height: 1;
}
.delete-btn:hover { color: #c0362c; background: #fee2e2; }

.add-user-comment { display: flex; gap: 10px; align-items: flex-start; }

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

/* Komentarze urzędu */
.admin-comment {
  background: #faf5ff;
  border-left: 3px solid #7c3aed;
  padding: 10px 14px;
  border-radius: 0 8px 8px 0;
  display: grid;
  gap: 4px;
}
.comment-text { margin: 0; font-size: 14px; line-height: 1.5; }
.comment-meta { margin: 0; font-size: 11px; color: var(--ink-muted); }

/* Historia statusów */
.history-item {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.arrow { color: var(--ink-muted); }
.history-meta { font-size: 11px; color: var(--ink-muted); }

/* Badges */
.status-badge {
  padding: 3px 9px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
}
.status-badge--new         { background: #dbeafe; color: #1d4ed8; }
.status-badge--in_progress { background: #fef3c7; color: #92400e; }
.status-badge--resolved    { background: #dcfce7; color: #166534; }
.status-badge--rejected    { background: #fee2e2; color: #991b1b; }

.empty-comments { padding: 16px 24px; }
.hint  { color: var(--ink-muted); font-size: 14px; margin: 0; }
.error { color: #c0362c; font-weight: 600; }
</style>

<style>
.report-pin {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #3b82f6;
  border: 2px solid #fff;
  box-shadow: 0 0 0 2px #3b82f6;
}
</style>
