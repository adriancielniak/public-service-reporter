import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import FeedView from "../views/FeedView.vue";
import MyReportsView from "../views/MyReportsView.vue";
import CreateReportView from "../views/CreateReportView.vue";
import { getStoredToken } from "../services/api";

const routes = [
  { path: "/", redirect: "/feed" },
  { path: "/login", name: "login", component: LoginView, meta: { public: true } },
  { path: "/register", name: "register", component: RegisterView, meta: { public: true } },
  { path: "/feed", name: "feed", component: FeedView },
  { path: "/my-reports", name: "my-reports", component: MyReportsView },
  { path: "/create-report", name: "create-report", component: CreateReportView }
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
    return { name: "feed" };
  }

  return true;
});

export default router;
