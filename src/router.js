import { createRouter, createWebHistory } from "vue-router";
import Home from "./pages/Home.vue";
import AddSubject from "./pages/AddSubject.vue";
import UploadDocument from "./pages/UploadDocument.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/add-subject",
    name: "AddSubject",
    component: AddSubject,
  },
  {
    path: "/upload-document",
    name: "UploadDocument",
    component: UploadDocument,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
