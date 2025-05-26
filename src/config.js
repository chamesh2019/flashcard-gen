const config = {
  // API endpoint base URL
  apiBaseUrl: "https://chamma.sytes.net",
};

// check if there is BASE_URL in the environment
if (import.meta.env.BACKEND_URL) {
  config.apiBaseUrl = import.meta.env.BACKEND_URL;
}
export default config;
