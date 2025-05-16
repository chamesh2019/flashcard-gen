// public/service-worker.js

const FIRST_NOTIFICATION_HOUR = 9; // 9 AM
const SECOND_NOTIFICATION_HOUR = 20; // 8 PM
const NOTIFICATION_TAG_PREFIX = "flashcard-reminder-";

let notificationTimeoutId1 = null;
let notificationTimeoutId2 = null;

self.addEventListener("install", (event) => {
  console.log("Service Worker: Installing...");
  self.skipWaiting(); // Activate worker immediately
});

self.addEventListener("activate", (event) => {
  console.log("Service Worker: Activating...");
  event.waitUntil(
    self.clients.claim().then(() => {
      console.log("Service Worker: Claimed clients.");
      // Initial schedule attempt on activation if permission is already granted
      scheduleNotifications();
    })
  );
});

function showNotification(title, body, tag) {
  if (Notification.permission === "granted") {
    self.registration.showNotification(title, {
      body: body,
      icon: "/vite.svg", // Optional: replace with your app's icon
      tag: tag, // Tag to prevent multiple notifications if one is already scheduled/visible
    });
    console.log(`Service Worker: Notification shown - ${title} (Tag: ${tag})`);
  } else {
    console.warn(
      "Service Worker: Notification permission not granted. Cannot show notification."
    );
  }
}

function scheduleNotification(targetHour, isFirstNotification) {
  const now = new Date();
  let nextNotificationTime = new Date(
    now.getFullYear(),
    now.getMonth(),
    now.getDate(),
    targetHour,
    0,
    0,
    0
  );

  if (now.getTime() > nextNotificationTime.getTime()) {
    // If the target time has already passed for today, schedule it for tomorrow
    nextNotificationTime.setDate(nextNotificationTime.getDate() + 1);
  }

  const delay = nextNotificationTime.getTime() - now.getTime();
  const notificationTag = NOTIFICATION_TAG_PREFIX + targetHour;

  // Clear any existing timeout for this specific notification slot
  if (isFirstNotification && notificationTimeoutId1) {
    clearTimeout(notificationTimeoutId1);
  } else if (!isFirstNotification && notificationTimeoutId2) {
    clearTimeout(notificationTimeoutId2);
  }

  console.log(
    `Service Worker: Scheduling notification for ${targetHour}:00 at ${nextNotificationTime.toLocaleString()} (Tag: ${notificationTag}). Will trigger in approx ${Math.round(
      delay / 60000
    )} mins.`
  );

  const timeoutId = setTimeout(() => {
    const title = isFirstNotification ? "Study Time! 📚" : "Quick Review! 🧠";
    const body = `Time for your flashcard session. Keep up the great work!`;
    showNotification(title, body, notificationTag);

    // Reschedule for the next occurrence
    if (isFirstNotification) {
      // This was the first notification, schedule the second one for today (or tomorrow if 3 PM passed)
      scheduleNotification(SECOND_NOTIFICATION_HOUR, false);
      // And schedule this first one for tomorrow
      scheduleNotification(FIRST_NOTIFICATION_HOUR, true);
    } else {
      // This was the second notification, schedule the first one for tomorrow
      scheduleNotification(FIRST_NOTIFICATION_HOUR, true);
      // And schedule this second one for tomorrow
      scheduleNotification(SECOND_NOTIFICATION_HOUR, false);
    }
  }, delay);

  if (isFirstNotification) {
    notificationTimeoutId1 = timeoutId;
  } else {
    notificationTimeoutId2 = timeoutId;
  }
}

function scheduleNotifications() {
  if (Notification.permission !== "granted") {
    console.log(
      "Service Worker: Notification permission not granted. Waiting for permission."
    );
    // The main thread should request permission and then can message the SW
    // or the SW can re-check on next activation.
    return;
  }

  console.log(
    "Service Worker: Permission granted. Proceeding with scheduling."
  );

  // Clear any existing timeouts before rescheduling to avoid duplicates if SW restarts
  if (notificationTimeoutId1) clearTimeout(notificationTimeoutId1);
  if (notificationTimeoutId2) clearTimeout(notificationTimeoutId2);

  const now = new Date();
  const currentHour = now.getHours();

  // Schedule the 9 AM notification
  scheduleNotification(FIRST_NOTIFICATION_HOUR, true);
  // Schedule the 3 PM notification
  scheduleNotification(SECOND_NOTIFICATION_HOUR, false);

  console.log("Service Worker: Initial daily notifications scheduled.");
}

// Listen for messages from the main thread
self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "PERMISSION_GRANTED") {
    console.log(
      "Service Worker: Received PERMISSION_GRANTED message. Scheduling notifications."
    );
    scheduleNotifications();
  }
  if (event.data && event.data.type === "SCHEDULE_NOTIFICATIONS") {
    console.log("Service Worker: Received SCHEDULE_NOTIFICATIONS message.");
    scheduleNotifications();
  }
});
