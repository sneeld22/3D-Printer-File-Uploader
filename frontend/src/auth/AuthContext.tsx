import { useCallback, useEffect, useState } from "react";
import apiClient from "../api/api-client";
import { AuthContext } from "./auth-context";
import type { User } from "./auth-context";

const getCurrentUser = async (): Promise<User> => {
    const response = await apiClient.get<User>("/auth/me");
    return response.data;
};

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [initialToken] = useState(() => localStorage.getItem("token"));
    const [token, setToken] = useState<string | null>(initialToken);
    const [loading, setLoading] = useState(Boolean(initialToken));

    const logout = useCallback(() => {
        localStorage.removeItem("token");
        setToken(null);
        setUser(null);
    }, []);

    useEffect(() => {
        if (initialToken) {
            void getCurrentUser().then(setUser).catch(logout).finally(() => setLoading(false));
        }
    }, [initialToken, logout]);

    const login = async (username: string, password: string): Promise<User> => {
        const res = await apiClient.post("/auth/login", { username, password });

        const accessToken = res.data.access_token;
        localStorage.setItem("token", accessToken);
        setToken(accessToken);

        try {
            const currentUser = await getCurrentUser();
            setUser(currentUser);
            return currentUser;
        } catch (error) {
            logout();
            throw error;
        }
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
