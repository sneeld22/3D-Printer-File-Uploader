// src/auth/AuthContext.tsx
import { createContext, useContext, useState } from "react";
import type { ReactNode } from "react";

export type UserRole = "student" | "verifier" | "admin";

export interface User {
    id: string;
    name: string;
    role: UserRole;
}

interface AuthContextValue {
    user: User | null;
    loginAsRole: (role: UserRole) => void; // mock login for now
    logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);

    const loginAsRole = (role: UserRole) => {
        setUser({
            id: "demo-user-id",
            name: `Demo ${role}`,
            role,
        });
    };

    const logout = () => setUser(null);

    return (
        <AuthContext.Provider value={{ user, loginAsRole, logout }}>
            {children}
        </AuthContext.Provider>
    );
};


export const useAuth = (): AuthContextValue => {
    const ctx = useContext(AuthContext);
    if (!ctx) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return ctx;
};

