import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import DashboardView from "../views/DashboardView.vue";
import { getStoredToken } from "../services/api";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", name: "login", component: LoginView, meta: { public: true } },
  { path: "/register", name: "register", component: RegisterView, meta: { public: true } },
  { path: "/dashboard", name: "dashboard", component: DashboardView }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to) => {
  const hasToken = Boolean(getStoredToken());

  if (!to.meta.public && !hasToken) {
    return { name: "login" };
  }

  if (hasToken && (to.name === "login" || to.name === "register")) {
    return { name: "dashboard" };
  }

  return true;
});

export default router;
