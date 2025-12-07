import { createContext, useContext, useEffect, useState } from "react";
import apiClient from "../api/api-client";

interface User {
    id: string;
    username: string;
}

interface AuthContextValue {
    user: User | null;
    token: string | null;
    login: (username: string, password: string) => Promise<void>;
    logout: () => void;
    isAuthenticated: boolean;
    loading: boolean,
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);

    // Load token on startup
    useEffect(() => {
        const storedToken = localStorage.getItem("token");
        if (storedToken) {
            setToken(storedToken);
            fetchCurrentUser().finally(() => setLoading(false));
        } else {
            setLoading(false);
        }
    }, []);

    const fetchCurrentUser = async () => {
        try {
            const res = await apiClient.get("/auth/me");
            setUser(res.data);
        } catch {
            logout();
        }
    };

    const login = async (username: string, password: string) => {
        const res = await apiClient.post("/auth/login", { username, password });

        const accessToken = res.data.access_token;
        localStorage.setItem("token", accessToken);
        setToken(accessToken);

        await fetchCurrentUser();
    };

    const logout = () => {
        localStorage.removeItem("token");
        setToken(null);
        setUser(null);
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                token,
                login,
                logout,
                isAuthenticated: !!user,
                loading
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
    return ctx;
};