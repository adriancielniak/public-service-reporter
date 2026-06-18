import axios from "axios";

const baseURL =
  process.env.VUE_APP_API_BASE_URL || "http://localhost:5001";

const api = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json"
  }
});

export const getStoredToken = () => localStorage.getItem("psr_token");

export const storeToken = (token) => {
  localStorage.setItem("psr_token", token);
  api.defaults.headers.common.Authorization = `Token ${token}`;
};

export const clearToken = () => {
  localStorage.removeItem("psr_token");
  delete api.defaults.headers.common.Authorization;
};



const existingToken = getStoredToken();
if (existingToken) {
  api.defaults.headers.common.Authorization = `Token ${existingToken}`;
}

export default api;
