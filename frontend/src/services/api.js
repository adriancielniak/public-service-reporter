import axios from "axios";
import { ref } from "vue";

const baseURL =
  process.env.VUE_APP_API_BASE_URL || "http://localhost:5001";

const api = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json"
  }
});

export const getStoredToken = () => localStorage.getItem("psr_token");
export const getStoredUserId = () => Number(localStorage.getItem("psr_user_id")) || null;

export const isAuthenticated = ref(Boolean(localStorage.getItem("psr_token")));
export const currentUserId = ref(getStoredUserId());

export const storeToken = (token, userId) => {
  localStorage.setItem("psr_token", token);
  localStorage.setItem("psr_user_id", userId);
  api.defaults.headers.common.Authorization = `Token ${token}`;
  isAuthenticated.value = true;
  currentUserId.value = userId;
};

export const clearToken = () => {
  localStorage.removeItem("psr_token");
  localStorage.removeItem("psr_user_id");
  delete api.defaults.headers.common.Authorization;
  isAuthenticated.value = false;
  currentUserId.value = null;
};

const existingToken = getStoredToken();
if (existingToken) {
  api.defaults.headers.common.Authorization = `Token ${existingToken}`;
}

export default api;
