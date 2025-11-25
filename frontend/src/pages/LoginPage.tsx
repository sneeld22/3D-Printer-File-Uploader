import { Box, Button, Typography, Paper } from "@mui/material";
import {useNavigate} from "react-router-dom";

const LoginPage = () => {
  // later: "Login with school account" button that redirects to AD

    const navigate = useNavigate();

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
          Log in with your school account to upload and verify 3D models.
        </Typography>
        <Button variant="contained" fullWidth onClick={()=>{navigate("/upload")}}>
          Login with School Account
        </Button>
      </Paper>
    </Box>
  );
};

export default LoginPage;
