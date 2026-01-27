import { useState } from "react";
import { Box, Button, TextField, Typography, Paper, Stack } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

const LoginPage = () => {
    const navigate = useNavigate();
    const { login } = useAuth();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async (e: any) => {
        e.preventDefault();
        try {
            setError("");
            await login(username, password);
            navigate("/upload");
        } catch (err) {
            setError("Invalid username or password");
        }
    };

    return (
        <Box
            sx={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}
        >
            <Paper sx={{ p: 4, width: 400, textAlign: "center" }}>
                <Typography variant="h5" gutterBottom>
                    Login
                </Typography>

                <Box component="form" onSubmit={handleLogin}>
                    <Stack spacing={2} sx={{ mt: 2 }}>
                        <TextField
                            label="Username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            fullWidth
                        />

                        <TextField
                            label="Password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            fullWidth
                        />

                        {error && <Typography color="error">{error}</Typography>}

                        <Button variant="contained" type="submit">
                            Login
                        </Button>
                    </Stack>
                </Box>
            </Paper>
        </Box>
    );
};

export default LoginPage;
