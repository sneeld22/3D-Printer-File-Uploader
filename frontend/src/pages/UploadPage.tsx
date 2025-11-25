import { Box, Typography } from "@mui/material";
import FileUpload from "../components/upload/FileUpload";

const UploadPage = () => {
    return (
        <Box sx={{ p: 3, maxWidth: 800, mx: "auto" }}>
            <Typography variant="h4" gutterBottom>
                Upload 3D Model
            </Typography>
            <Typography variant="body1" sx={{ mb: 3 }}>
                Upload your 3D model file. After upload, other students can verify it
                before it’s sent to the printer.
            </Typography>

            <FileUpload />
        </Box>
    );
};

export default UploadPage;
