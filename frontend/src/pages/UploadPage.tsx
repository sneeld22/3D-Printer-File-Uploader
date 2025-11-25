// src/pages/UploadPage.tsx
import { Box, Typography } from "@mui/material";
import FileUpload from "../components/upload/FileUpload";
import MyUploadsTable from "../components/upload/MyUploadsTable";

const UploadPage = () => {
    return (
        <Box sx={{ p: 3, maxWidth: 1000, mx: "auto" }}>
            <Typography variant="h4" gutterBottom>
                Upload 3D Model
            </Typography>
            <Typography variant="body1" sx={{ mb: 3 }}>
                Upload your 3D model file. After upload, it must be verified before it
                is sent to the printer.
            </Typography>

            <FileUpload />

            <MyUploadsTable />
        </Box>
    );
};

export default UploadPage;
