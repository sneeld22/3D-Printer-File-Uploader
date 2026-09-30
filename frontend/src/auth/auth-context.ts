import { createContext } from "react";

export interface User {
    id: string;
    username: string;
    roles: string[];
}

export interface AuthContextValue {
    user: User | null;
    token: string | null;
    login: (username: string, password: string) => Promise<User>;
    logout: () => void;
    isAuthenticated: boolean;
    loading: boolean;
}

export const AuthContext = createContext<AuthContextValue | undefined>(undefined);
