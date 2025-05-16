import { createApp } from "vue";
import "./style.css";
import "./assets/components.css"; // Import our new components style sheet
import App from "./App.vue";
import router from "./router"; // Import the router

createApp(App).use(router).mount("#app"); // Use the router
