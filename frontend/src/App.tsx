import { Link, Route, Routes, useLocation } from "react-router-dom";
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

const App = () => {
  const location = useLocation();
  const isLoginRoute = location.pathname === "/login" || location.pathname === "/";

  return (
    <Box sx={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      {!isLoginRoute && (
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" sx={{ flexGrow: 1 }}>
              3D Print Portal
            </Typography>
            <Button color="inherit" component={Link} to="/upload">
              Upload
            </Button>
            <Button color="inherit" component={Link} to="/verify">
              Verify
            </Button>
            <Button color="inherit" component={Link} to="/printer">
              Printer
            </Button>
          </Toolbar>
        </AppBar>
      )}

      <Container sx={{ flexGrow: 1, py: 3 }}>
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/verify" element={<VerificationPage />} />
          <Route path="/printer" element={<PrinterPage />} />
        </Routes>
      </Container>
    </Box>
  );
};

export default App;
