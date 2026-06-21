<template>
  <section class="login-grid">
    <div class="welcome">
      <p class="eyebrow">Szybkie zgloszenia</p>
      <h1>Zaloguj sie i przekaz problem w gminie.</h1>
      <p class="lead">
        Panel pozwala dodawac nowe zgloszenia, sledzic status i szybko
        edytowac tresc raportu.
      </p>
      <div class="feature-card">
        <p class="feature-title">Co potrafi panel?</p>
        <ul>
          <li>Nowe zgloszenie w kilka sekund</li>
          <li>Historia i edycja raportow</li>
          <li>Bezpieczny dostep przez token</li>
        </ul>
      </div>
    </div>

    <form class="login-card" @submit.prevent="handleLogin">
      <h2>Logowanie</h2>
      <p class="hint">Uzyj loginu i hasla zarejestrowanego w systemie.</p>

      <label class="field">
        <span>Login</span>
        <input
          v-model.trim="form.username"
          type="text"
          autocomplete="username"
          placeholder="np. jana.kowalska"
          required
        />
      </label>

      <label class="field">
        <span>Haslo</span>
        <input
          v-model.trim="form.password"
          type="password"
          autocomplete="current-password"
          placeholder="Twoje haslo"
          required
        />
      </label>

      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="success" class="success">{{ success }}</p>

      <button type="submit" :disabled="loading">
        <span v-if="loading">Logowanie...</span>
        <span v-else>Zaloguj</span>
      </button>

      <p class="note">Po zalogowaniu token zostanie zapisany lokalnie.</p>
      <p class="note">
        Nie masz konta?
        <router-link class="link" to="/register">Zarejestruj sie</router-link>
      </p>
    </form>
  </section>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import api, { storeToken } from "../services/api";

const form = reactive({
  username: "",
  password: ""
});

const loading = ref(false);
const error = ref("");
const success = ref("");
const router = useRouter();

const handleLogin = async () => {
  error.value = "";
  success.value = "";
  loading.value = true;

  try {
    const response = await api.post("/api/login/", {
      username: form.username,
      password: form.password
    });

    if (!response.data?.token) {
      throw new Error("Brak tokena w odpowiedzi API.");
    }

    storeToken(response.data.token, response.data.user_id);
    success.value = "Zalogowano. Token zapisany lokalnie.";
    await router.push({ name: "feed" });
  } catch (err) {
    const apiMessage = err?.response?.data?.error;
    error.value = apiMessage || "Nie udalo sie zalogowac. Sprobuj ponownie.";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 32px;
  align-items: start;
}

.welcome h1 {
  font-size: clamp(28px, 3vw, 40px);
  line-height: 1.1;
  margin-bottom: 16px;
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
  max-width: 440px;
}

.feature-card {
  margin-top: 24px;
  padding: 20px;
  border-radius: 16px;
  background: var(--surface-glass);
  border: 1px solid rgba(15, 23, 42, 0.12);
}

.feature-title {
  font-weight: 600;
  margin-bottom: 12px;
}

.feature-card ul {
  padding-left: 18px;
  margin: 0;
  color: var(--ink-muted);
}

.login-card {
  background: var(--surface);
  border-radius: 18px;
  padding: 28px;
  box-shadow: 0 30px 60px rgba(15, 23, 42, 0.12);
  display: grid;
  gap: 16px;
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

.field input {
  border: 1px solid rgba(15, 23, 42, 0.15);
  border-radius: 12px;
  padding: 12px 14px;
  font-size: 14px;
  background: #fff;
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

.error {
  color: #c0362c;
  font-weight: 600;
}

.success {
  color: #1b7f4b;
  font-weight: 600;
}

.note {
  color: var(--ink-muted);
  font-size: 12px;
}

.link {
  color: var(--accent);
  font-weight: 600;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}
</style>
