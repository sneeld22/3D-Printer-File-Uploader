import axios from "axios";

const apiClient = axios.create({
    baseURL: "http://localhost:8000/api/v1",
});

// Add token from localStorage to every request
apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Auto-logout on expired token
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        const status = error.response?.status;
        const hasToken = !!localStorage.getItem("token");

        if (status === 401 && hasToken) {
            localStorage.removeItem("token");
        }
        return Promise.reject(error);
    }
);

export default apiClient;