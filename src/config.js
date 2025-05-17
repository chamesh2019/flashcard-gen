const config = {
  // API endpoint base URL
  apiBaseUrl: "https://csmanager2020.pythonanywhere.com",
};

// check if there is BASE_URL in the environment
if (import.meta.env.BACKEND_URL) {
  config.apiBaseUrl = import.meta.env.BACKEND_URL;
}
export default config;
