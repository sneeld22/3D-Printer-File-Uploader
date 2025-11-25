// src/App.tsx
import { Link, Route, Routes, useLocation, Navigate } from "react-router-dom";
import {
    AppBar,
    Box,
    Button,
    Container,
    Toolbar,
    Typography,
} from "@mui/material";
import LoginPage from "./pages/LoginPage";
import UploadPage from "./pages/UploadPage";
import VerificationPage from "./pages/VerificationPage";
import PrinterPage from "./pages/PrinterPage";
import { useAuth } from "./auth/AuthContext";
import type { UserRole } from "./auth/AuthContext";
import type { ReactNode } from "react";


interface RequireAuthProps {
    children: ReactNode;
    allowedRoles: UserRole[];
}


const RequireAuth = ({ children, allowedRoles }: RequireAuthProps) => {
    const { user } = useAuth();

    if (!user) {
        return <Navigate to="/login" replace />;
    }

    if (!allowedRoles.includes(user.role)) {
        return (
            <Box sx={{ p: 3 }}>
                <Typography variant="h5">Not authorized</Typography>
                <Typography variant="body1">
                    You do not have permission to access this page.
                </Typography>
            </Box>
        );
    }

    return children;
};

const App = () => {
    const location = useLocation();
    const { user, logout } = useAuth();
    const isLoginRoute = location.pathname === "/login" || location.pathname === "/";

    return (
        <Box sx={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
            {!isLoginRoute && user && (
                <AppBar position="static">
                    <Toolbar>
                        <Typography variant="h6" sx={{ flexGrow: 1 }}>
                            3D Print Portal
                        </Typography>

                        <Button color="inherit" component={Link} to="/upload">
                            Upload
                        </Button>

                        {(user.role === "verifier" || user.role === "admin") && (
                            <Button color="inherit" component={Link} to="/verify">
                                Verify
                            </Button>
                        )}

                        {user.role === "admin" && (
                            <Button color="inherit" component={Link} to="/printer">
                                Printer Queue
                            </Button>
                        )}

                        <Typography variant="body2" sx={{ ml: 2, mr: 1 }}>
                            {user.name} ({user.role})
                        </Typography>

                        <Button color="inherit" onClick={logout}>
                            Logout
                        </Button>
                    </Toolbar>
                </AppBar>
            )}

            <Container sx={{ flexGrow: 1, py: 3 }}>
                <Routes>
                    <Route path="/" element={<Navigate to="/login" replace />} />
                    <Route path="/login" element={<LoginPage />} />

                    {/* Student + Verifier + Admin */}
                    <Route
                        path="/upload"
                        element={
                            <RequireAuth allowedRoles={["student", "verifier", "admin"]}>
                                <UploadPage />
                            </RequireAuth>
                        }
                    />

                    {/* Verifier + Admin */}
                    <Route
                        path="/verify"
                        element={
                            <RequireAuth allowedRoles={["verifier", "admin"]}>
                                <VerificationPage />
                            </RequireAuth>
                        }
                    />

                    {/* Admin only */}
                    <Route
                        path="/printer"
                        element={
                            <RequireAuth allowedRoles={["admin"]}>
                                <PrinterPage />
                            </RequireAuth>
                        }
                    />
                </Routes>
            </Container>
        </Box>
    );
};

export default App;
