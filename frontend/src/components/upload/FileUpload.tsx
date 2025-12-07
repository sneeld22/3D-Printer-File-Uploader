// src/components/upload/FileUpload.tsx
import { useState } from "react";
import type { DragEvent, ChangeEvent } from "react";

import {
    Box,
    Button,
    LinearProgress,
    Paper,
    Stack,
    Typography,
    Alert,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import ErrorIcon from "@mui/icons-material/Error";
import { uploadModelFile } from "../../services/fileService.ts";
import type { UploadedFileResponse } from "../../services/fileService.ts";

const ALLOWED_EXTENSIONS = ["stl", "3mf"];
const MAX_FILE_SIZE_MB = 50;

const getFileExtension = (file: File) =>
    file.name.split(".").pop()?.toLowerCase() || "";

const validateFile = (file: File): string | null => {
    const ext = getFileExtension(file);
    if (!ALLOWED_EXTENSIONS.includes(ext)) {
        return `Invalid file type. Allowed: ${ALLOWED_EXTENSIONS.join(", ")}`;
    }

    const sizeMB = file.size / (1024 * 1024);
    if (sizeMB > MAX_FILE_SIZE_MB) {
        return `File too large. Max ${MAX_FILE_SIZE_MB} MB, got ${sizeMB.toFixed(
            1
        )} MB`;
    }

    return null;
};

const FileUpload = () => {
    const [dragActive, setDragActive] = useState(false);
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [uploadProgress, setUploadProgress] = useState<number>(0);
    const [isUploading, setIsUploading] = useState(false);
    const [uploadResult, setUploadResult] = useState<UploadedFileResponse | null>(
        null
    );

    const handleFiles = (fileList: FileList | null) => {
        if (!fileList || fileList.length === 0) return;

        const file = fileList[0];
        const validationError = validateFile(file);
        if (validationError) {
            setError(validationError);
            setSelectedFile(null);
            setUploadResult(null);
            return;
        }

        setError(null);
        setUploadResult(null);
        setSelectedFile(file);
    };

    const handleDragOver = (event: DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        event.stopPropagation();
        setDragActive(true);
    };

    const handleDragLeave = (event: DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        event.stopPropagation();
        setDragActive(false);
    };

    const handleDrop = (event: DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        event.stopPropagation();
        setDragActive(false);
        handleFiles(event.dataTransfer.files);
    };

    const handleFileInputChange = (event: ChangeEvent<HTMLInputElement>) => {
        handleFiles(event.target.files);
    };

    const handleUpload = async () => {
        if (!selectedFile) return;
        setIsUploading(true);
        setUploadProgress(0);
        setError(null);
        setUploadResult(null);

        try {
            const result = await uploadModelFile(selectedFile, (percent) =>
                setUploadProgress(percent)
            );
            setUploadResult(result);
        } catch (err: unknown) {
            console.error(err);

            if (
                err &&
                typeof err === "object" &&
                "response" in err &&
                err.response &&
                typeof err.response === "object" &&
                "data" in err.response &&
                err.response.data &&
                typeof err.response.data === "object" &&
                "message" in err.response.data
            ) {
                // eslint-disable-next-line @typescript-eslint/no-explicit-any
                const message = (err as any).response.data.message as string;
                setError(message);
            } else {
                setError("Upload failed. Please try again or contact the admin.");
            }
        } finally {

            setIsUploading(false);
        }
    };

    return (
        <Paper sx={{ p: 3 }}>
            <Stack spacing={2}>
                <Typography variant="h5">Upload 3D Model</Typography>
                <Typography variant="body2" color="text.secondary">
                    Allowed file types: <b>.stl</b>, <b>.3mf</b> • Max size:{" "}
                    {MAX_FILE_SIZE_MB} MB
                </Typography>

                <Box
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    sx={{
                        border: "2px dashed",
                        borderColor: dragActive ? "primary.main" : "divider",
                        borderRadius: 2,
                        p: 4,
                        textAlign: "center",
                        backgroundColor: dragActive ? "action.hover" : "background.paper",
                        cursor: "pointer",
                    }}
                >
                    <input
                        id="file-input"
                        type="file"
                        hidden
                        accept=".stl,.3mf"
                        onChange={handleFileInputChange}
                    />
                    <label htmlFor="file-input">
                        <Stack spacing={1} alignItems="center">
                            <CloudUploadIcon fontSize="large" />
                            <Typography variant="body1">
                                Drag &amp; drop a file here, or click to browse
                            </Typography>
                            {selectedFile && (
                                <Typography variant="body2" color="text.secondary">
                                    Selected: <b>{selectedFile.name}</b>
                                </Typography>
                            )}
                        </Stack>
                    </label>
                </Box>

                {isUploading && (
                    <Box>
                        <Typography variant="body2" gutterBottom>
                            Uploading… {uploadProgress}%
                        </Typography>
                        <LinearProgress variant="determinate" value={uploadProgress} />
                    </Box>
                )}

                {error && (
                    <Alert severity="error" icon={<ErrorIcon />}>
                        {error}
                    </Alert>
                )}

                {uploadResult && (
                    <Alert
                        severity="success"
                        icon={<CheckCircleIcon />}
                        sx={{ alignItems: "center" }}
                    >
                        File <b>{uploadResult.filename}</b> uploaded successfully
                    </Alert>
                )}

                <Box>
                    <Button
                        variant="contained"
                        disabled={!selectedFile || isUploading}
                        onClick={handleUpload}
                    >
                        {isUploading ? "Uploading…" : "Upload"}
                    </Button>
                </Box>
            </Stack>
        </Paper>
    );
};

export default FileUpload;
