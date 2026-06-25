<template>
  <nav class="nav-bar">
    <div class="nav-container">
      <div class="nav-logo">
        <h1>PSR</h1>
        <span>Public Service Reporter</span>
      </div>
      <ul class="nav-links">
        <li>
          <router-link
            to="/feed"
            :class="['nav-link', { active: $route.name === 'feed' }]"
          >
            📊 Feed
          </router-link>
        </li>
        <li>
          <router-link
            to="/my-reports"
            :class="['nav-link', { active: $route.name === 'my-reports' }]"
          >
            📝 Moje zgłoszenia
          </router-link>
        </li>
        <li>
          <router-link
            to="/create-report"
            :class="['nav-link', { active: $route.name === 'create-report' }]"
          >
            ➕ Nowe zgłoszenie
          </router-link>
        </li>
        <li v-if="currentRole === 'admin' || currentRole === 'worker'">
          <router-link
            to="/admin"
            :class="['nav-link', 'nav-link--admin', { active: $route.name === 'admin' }]"
          >
            ⚙️ Panel admina
          </router-link>
        </li>
      </ul>
      <button class="logout-btn" type="button" @click="handleLogout">Wyloguj</button>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { clearToken, currentRole } from '../services/api';

const router = useRouter();

const handleLogout = async () => {
  clearToken();
  await router.push({ name: 'login' });
};
</script>

<style scoped>
.nav-bar {
  background: var(--surface);
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.1);
  border-bottom: 1px solid rgba(15, 23, 42, 0.08);
  padding: 16px 0;
  margin-bottom: 24px;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.nav-logo h1 {
  margin: 0;
  font-size: 24px;
  color: var(--accent);
}

.nav-logo span {
  font-size: 12px;
  color: var(--ink-muted);
  font-weight: 600;
  letter-spacing: 0.5px;
}

.nav-links {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  gap: 8px;
}

.nav-link {
  padding: 8px 16px;
  border-radius: 8px;
  text-decoration: none;
  color: var(--ink-muted);
  font-weight: 600;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.nav-link:hover {
  color: var(--accent);
  background: rgba(15, 23, 42, 0.05);
}

.nav-link.active {
  background: var(--accent);
  color: var(--ink-inverse);
  border-color: var(--accent);
}

.logout-btn {
  background: transparent;
  color: var(--ink-muted);
  border: 1px solid rgba(15, 23, 42, 0.15);
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  color: #c0362c;
  border-color: #c0362c;
}

.nav-link--admin {
  color: #7c3aed;
}
.nav-link--admin:hover {
  background: rgba(124, 58, 237, 0.08);
  color: #7c3aed;
}
.nav-link--admin.active {
  background: #7c3aed;
  border-color: #7c3aed;
  color: #fff;
}
</style>
