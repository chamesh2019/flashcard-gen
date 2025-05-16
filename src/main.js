import { createApp } from "vue";
import "./style.css";
import "./assets/components.css"; // Import our new components style sheet
import App from "./App.vue";
import router from "./router"; // Import the router

createApp(App).use(router).mount("#app"); // Use the router

/**
 * Registers the service worker and handles notification permission.
 */
async function registerServiceWorkerAndNotifications() {
  if ("serviceWorker" in navigator) {
    try {
      const registration = await navigator.serviceWorker.register(
        "/service-worker.js",
        { scope: "/" }
      );
      console.log("Service Worker registered with scope:", registration.scope);

      // Check/request notification permission
      if (!("Notification" in window)) {
        console.error("This browser does not support desktop notification.");
        return;
      }

      if (Notification.permission === "granted") {
        console.log("Notification permission already granted.");
        // Inform the service worker that permission is granted
        if (navigator.serviceWorker.controller) {
          navigator.serviceWorker.controller.postMessage({
            type: "PERMISSION_GRANTED",
          });
        } else {
          // If controller is not yet available, wait for it
          navigator.serviceWorker.ready.then((reg) => {
            reg.active.postMessage({ type: "PERMISSION_GRANTED" });
          });
        }
      } else if (Notification.permission !== "denied") {
        console.log("Requesting notification permission...");
        const permission = await Notification.requestPermission();
        if (permission === "granted") {
          console.log("Notification permission granted by user.");
          if (navigator.serviceWorker.controller) {
            navigator.serviceWorker.controller.postMessage({
              type: "PERMISSION_GRANTED",
            });
          } else {
            navigator.serviceWorker.ready.then((reg) => {
              reg.active.postMessage({ type: "PERMISSION_GRANTED" });
            });
          }
        } else {
          console.warn("Notification permission denied by user.");
        }
      } else {
        console.warn("Notification permission was previously denied.");
      }
    } catch (error) {
      console.error("Service Worker registration failed:", error);
    }
  }
}

// Call this function when your app initializes
registerServiceWorkerAndNotifications();
