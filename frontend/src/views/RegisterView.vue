<template>
  <section class="register-grid">
    <div class="welcome">
      <p class="eyebrow">Nowe konto</p>
      <h1>Zarejestruj konto mieszkanca.</h1>
      <p class="lead">
        Podaj podstawowe dane, aby uzyskac dostep do panelu zgloszen.
      </p>
      <div class="feature-card">
        <p class="feature-title">Wymagane dane</p>
        <ul>
          <li>Login i haslo</li>
          <li>Adres e-mail</li>
          <li>Rola uzytkownika</li>
        </ul>
      </div>
    </div>

    <form class="register-card" @submit.prevent="handleRegister">
      <h2>Rejestracja</h2>
      <p class="hint">Utworz konto, aby zglaszac problemy w gminie.</p>

      <label class="field">
        <span>Login</span>
        <input
          v-model.trim="form.username"
          type="text"
          autocomplete="username"
          placeholder="np. jan.kowalski"
          required
        />
      </label>

      <label class="field">
        <span>E-mail</span>
        <input
          v-model.trim="form.email"
          type="email"
          autocomplete="email"
          placeholder="jan.kowalski@email.com"
          required
        />
      </label>

      <label class="field">
        <span>Haslo</span>
        <input
          v-model.trim="form.password"
          type="password"
          autocomplete="new-password"
          placeholder="Minimum 8 znakow"
          required
        />
      </label>

      <label class="field">
        <span>Rola</span>
        <select v-model="form.role" required>
          <option value="standard">Mieszkaniec</option>
          <option value="worker">Pracownik</option>
          <option value="admin">Administrator</option>
        </select>
      </label>

      <label class="field">
        <span>Dodatkowe informacje</span>
        <textarea
          v-model.trim="form.data"
          rows="3"
          placeholder="np. osiedle, numer kontaktowy"
        ></textarea>
      </label>

      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="success" class="success">{{ success }}</p>

      <button type="submit" :disabled="loading">
        <span v-if="loading">Tworzenie konta...</span>
        <span v-else>Zarejestruj</span>
      </button>

      <p class="note">
        Masz juz konto?
        <router-link class="link" to="/login">Zaloguj sie</router-link>
      </p>
    </form>
  </section>
</template>

<script setup>
import { reactive, ref } from "vue";
import api from "../services/api";

const form = reactive({
  username: "",
  email: "",
  password: "",
  role: "standard",
  data: ""
});

const loading = ref(false);
const error = ref("");
const success = ref("");

const handleRegister = async () => {
  error.value = "";
  success.value = "";
  loading.value = true;

  try {
    await api.post("/api/register/", {
      username: form.username,
      email: form.email,
      password: form.password,
      role: form.role,
      data: form.data
    });

    success.value = "Konto utworzone. Mozesz sie teraz zalogowac.";
  } catch (err) {
    const apiErrors = err?.response?.data;
    if (apiErrors && typeof apiErrors === "object") {
      const firstKey = Object.keys(apiErrors)[0];
      error.value = Array.isArray(apiErrors[firstKey])
        ? apiErrors[firstKey][0]
        : "Nie udalo sie utworzyc konta.";
    } else {
      error.value = "Nie udalo sie utworzyc konta.";
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-grid {
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

.register-card {
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

.field input,
.field select,
.field textarea {
  border: 1px solid rgba(15, 23, 42, 0.15);
  border-radius: 12px;
  padding: 12px 14px;
  font-size: 14px;
  background: #fff;
  font-family: inherit;
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
