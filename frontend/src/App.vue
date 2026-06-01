<template>
  <div class="app-shell">
    <header class="topbar">
      <div class="brand">
        <span class="brand-mark">PSR</span>
        <div>
          <p class="brand-title">Public Service Reporter</p>
          <p class="brand-subtitle">Panel mieszkanca</p>
        </div>
      </div>
      <span class="badge">beta</span>
    </header>

    <main class="page">
      <router-view />
    </main>

    <div class="orb orb-1" aria-hidden="true"></div>
    <div class="orb orb-2" aria-hidden="true"></div>
  </div>
</template>

<script setup>
</script>

<style>
.app-shell {
  min-height: 100vh;
  padding: 40px clamp(20px, 4vw, 60px) 80px;
  position: relative;
  overflow: hidden;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 48px;
}

.brand {
  display: flex;
  gap: 16px;
  align-items: center;
}

.brand-mark {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: var(--accent);
  color: var(--ink-inverse);
  display: grid;
  place-items: center;
  font-weight: 700;
  letter-spacing: 1px;
}

.brand-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
}

.brand-subtitle {
  margin: 0;
  color: var(--ink-muted);
  font-size: 14px;
}

.badge {
  padding: 6px 12px;
  border-radius: 999px;
  background: var(--surface-glass);
  color: var(--ink);
  border: 1px solid rgba(15, 23, 42, 0.12);
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.page {
  position: relative;
  z-index: 1;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(0px);
  opacity: 0.5;
  animation: float 12s ease-in-out infinite;
}

.orb-1 {
  width: 320px;
  height: 320px;
  background: radial-gradient(circle at 30% 30%, #f4c9d2, transparent 70%);
  top: -80px;
  right: -100px;
}

.orb-2 {
  width: 420px;
  height: 420px;
  background: radial-gradient(circle at 70% 30%, #b8d8f5, transparent 70%);
  bottom: -180px;
  left: -140px;
  animation-delay: -4s;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

@media (max-width: 640px) {
  .topbar {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
}
</style>
