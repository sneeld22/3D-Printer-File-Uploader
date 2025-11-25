import { Box, Button, Typography, Paper, Stack } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

const LoginPage = () => {
    const { loginAsRole } = useAuth();
    const navigate = useNavigate();

    const handleLogin = (role: "student" | "verifier" | "admin") => {
        loginAsRole(role);
        navigate("/upload"); // redirect after login
    };

    return (
        <Box
            sx={{
                minHeight: "100vh",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
            }}
        >
            <Paper sx={{ p: 4, width: 400, textAlign: "center" }}>
                <Typography variant="h5" gutterBottom>
                    3D Print Portal
                </Typography>

                <Typography variant="body1" sx={{ mb: 3 }}>
                    Log in with a role (temporary).
                    Real school Active Directory login will be added later.
                </Typography>

                <Stack spacing={2}>
                    <Button
                        variant="contained"
                        onClick={() => handleLogin("student")}
                    >
                        Login as Student
                    </Button>

                    <Button
                        variant="contained"
                        color="secondary"
                        onClick={() => handleLogin("verifier")}
                    >
                        Login as Verifier
                    </Button>

                    <Button
                        variant="outlined"
                        onClick={() => handleLogin("admin")}
                    >
                        Login as Admin
                    </Button>
                </Stack>
            </Paper>
        </Box>
    );
};

export default LoginPage;
