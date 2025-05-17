const config = {
  // API endpoint base URL
  apiBaseUrl: "http://localhost:5000",
};

// check if there is BASE_URL in the environment
if (import.meta.env.BACKEND_URL) {
  config.apiBaseUrl = import.meta.env.BACKEND_URL;
}
export default config;
