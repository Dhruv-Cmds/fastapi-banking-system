import axios from "axios";

// 🌐 Base API instance
const API = axios.create({
  // baseURL: "http://localhost:8000/api",
  baseURL: "https://fastapi-banking-system.onrender.com",
  timeout: 10000, 
});


// 🔐 Attach JWT token automatically
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);


// 🚨 Handle responses globally
API.interceptors.response.use(
  (response) => response,

  (error) => {
    // 🔐 If token expired or invalid → logout user
    if (error.response && error.response.status === 401) {
      console.warn("Unauthorized! Logging out...");

      localStorage.removeItem("token");

      // 👉 redirect to login page (adjust path if needed)
      window.location.href = "/login";
    }

    return Promise.reject(error);
  }
);


export default API;