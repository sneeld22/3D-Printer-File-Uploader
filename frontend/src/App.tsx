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
import type { ReactNode } from "react";
import AllFilesPage from "./pages/AllFilesPage";

// Helper: check if user has any role in allowedRoles
const hasRole = (user: any, allowedRoles: string[]) =>
    user?.roles?.some((r: string) => allowedRoles.includes(r));

interface RequireAuthProps {
    children: ReactNode;
    allowedRoles?: string[];
}

const RequireAuth = ({ children, allowedRoles }: RequireAuthProps) => {
    const { user, loading } = useAuth();

    if (loading) {
        return <Typography>Loading...</Typography>;
    }

    if (!user) {
        return <Navigate to="/login" replace />;
    }

    if (allowedRoles && !hasRole(user, allowedRoles)) {
        return (
            <Box sx={{ p: 3 }}>
                <Typography variant="h5">Not authorized</Typography>
                <Typography>You do not have permission to access this page.</Typography>
            </Box>
        );
    }

    return children;
};

const App = () => {
    const { user, logout } = useAuth();
    const location = useLocation();

    const isLoginRoute =
        location.pathname === "/login" || location.pathname === "/";

    return (
        <Box sx={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
            {/* Top navigation bar */}
            {!isLoginRoute && user && (
                <AppBar position="static">
                    <Toolbar>
                        <Typography variant="h6" sx={{ flexGrow: 1 }}>
                            3D Print Portal
                        </Typography>

                        {/* Upload: users with uploader/verifier/admin roles */}
                        {hasRole(user, ["uploader", "verifier", "admin"]) && (
                            <Button color="inherit" component={Link} to="/upload">
                                Upload
                            </Button>
                        )}

                        {/* Verification: verifier/admin */}
                        {hasRole(user, ["verifier", "admin"]) && (
                            <Button color="inherit" component={Link} to="/verify">
                                Verify
                            </Button>
                        )}

                        {/* Print Queue: admin only */}
                        {hasRole(user, ["admin"]) && (
                            <Button color="inherit" component={Link} to="/printer">
                                Printer Queue
                            </Button>
                        )}

                        {/* Files Page: admin only */}
                        {hasRole(user, ["admin"]) && (
                            <Button color="inherit" component={Link} to="/files">
                                All Files
                            </Button>
                        )}

                        {/* Display logged-in user */}
                        <Typography variant="body2" sx={{ ml: 2, mr: 1 }}>
                            {user.username}
                        </Typography>

                        <Button color="inherit" onClick={logout}>
                            Logout
                        </Button>
                    </Toolbar>
                </AppBar>
            )}

            {/* Main app content */}
            <Container sx={{ flexGrow: 1, py: 3 }}>
                <Routes>
                    <Route path="/" element={<Navigate to="/login" replace />} />
                    <Route path="/login" element={<LoginPage />} />

                    {/* Upload: uploader + verifier + admin */}
                    <Route
                        path="/upload"
                        element={
                            <RequireAuth allowedRoles={["uploader", "verifier", "admin"]}>
                                <UploadPage />
                            </RequireAuth>
                        }
                    />

                    {/* Verification */}
                    <Route
                        path="/verify"
                        element={
                            <RequireAuth allowedRoles={["verifier", "admin"]}>
                                <VerificationPage />
                            </RequireAuth>
                        }
                    />

                    {/* Printer Queue */}
                    <Route
                        path="/printer"
                        element={
                            <RequireAuth allowedRoles={["admin"]}>
                                <PrinterPage />
                            </RequireAuth>
                        }
                    />

                    <Route
                        path="/files"
                        element={
                            <RequireAuth allowedRoles={["admin"]}>
                                <AllFilesPage />
                            </RequireAuth>
                        }
                    />
                </Routes>
            </Container>
        </Box>
    );
};

export default App;
