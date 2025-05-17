import { createRouter, createWebHistory } from "vue-router";
import Home from "./pages/Home.vue";
import AddSubject from "./pages/AddSubject.vue";
import UploadDocument from "./pages/UploadDocument.vue";
import FlashcardPractice from "./pages/FlashcardPractice.vue";
import DocumentInfo from "./pages/DocumentInfo.vue";
import DocumentSelection from "./pages/DocumentSelection.vue";

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
  {
    path: "/document-info",
    name: "DocumentInfo",
    component: DocumentInfo,
  },
  {
    path: "/subjects/:subjectId/documents",
    name: "DocumentSelection",
    component: DocumentSelection,
    props: true,
  },
  {
    path: "/flashcards/:subjectId/:documentId?", // Optional documentId parameter
    name: "FlashcardPractice",
    component: FlashcardPractice,
    props: true, // Pass route params as props to the component
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
