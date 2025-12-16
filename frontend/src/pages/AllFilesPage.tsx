import { useEffect, useState } from "react";
import {
  Alert,
  Box,
  IconButton,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Tooltip,
} from "@mui/material";
import DownloadIcon from "@mui/icons-material/Download";
import DeleteIcon from "@mui/icons-material/Delete";
import apiClient from "../api/api-client";
import { formatFileSize } from "../utils/utils";
import {
  PrinterJobStatus,
  VerificationStatus,
} from "../common/models";
import type { ModelFile } from "../common/models";

const printStatusColor: Record<
  PrinterJobStatus,
  "success" | "warning" | "error" | "info" | "primary"
> = {
  pending: "warning",
  queued: "info",
  printing: "success",
  completed: "primary",
  failed: "error",
};

const verificationStatusColor: Record<
  VerificationStatus,
  "success" | "warning" | "error"
> = {
  approved: "success",
  pending: "warning",
  rejected: "error",
};

type ModelFileApi = Omit<ModelFile, "created_at"> & { created_at: string };

export default function AllFilesPage() {
  const [files, setFiles] = useState<ModelFile[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const loadFiles = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiClient.get<ModelFileApi[]>("/files/all");
      const converted = res.data.map((f) => ({
        ...f,
        created_at: new Date(f.created_at),
      }));
      setFiles(converted);
    } catch (err) {
      console.error(err);
      setError("Failed to load files.");
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (fileId: string, filename: string) => {
    try {
      const response = await apiClient.get(`/files/${fileId}/download`, {
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(response.data);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
      alert("Failed to download file.");
    }
  };

  const handleDelete = async (fileId: string) => {
    if (!window.confirm("Are you sure you want to delete this file?")) return;
    setDeletingId(fileId);
    try {
      await apiClient.delete(`/files/${fileId}`);
      await loadFiles();
    } catch (err) {
      console.error(err);
      alert("Failed to delete file.");
    } finally {
      setDeletingId(null);
    }
  };

  useEffect(() => {
    void loadFiles();
  }, []);

  // Sort FIFO by created_at ascending
  const sortedFiles = [...files].sort(
    (a, b) => a.created_at.getTime() - b.created_at.getTime()
  );

  return (
    <Box sx={{ p: 4 }}>
      <Stack spacing={3}>
        <Box>
          <Typography variant="h4" fontWeight={600}>
            All Files
          </Typography>
          <Typography variant="body2" color="text.secondary">
            All uploaded files with actions
          </Typography>
        </Box>

        <Card>
          <CardContent>
            {loading ? (
              <Box sx={{ display: "flex", justifyContent: "center", p: 4 }}>
                <CircularProgress />
              </Box>
            ) : error ? (
              <Alert severity="error">{error}</Alert>
            ) : sortedFiles.length === 0 ? (
              <Typography color="text.secondary" align="center">
                No files found.
              </Typography>
            ) : (
              <TableContainer component={Paper} variant="outlined">
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Position</TableCell>
                      <TableCell>Filename</TableCell>
                      <TableCell>Size</TableCell>
                      <TableCell>Uploaded</TableCell>
                      <TableCell>Verification</TableCell>
                      <TableCell>Print Status</TableCell>
                      <TableCell align="right">Actions</TableCell>
                    </TableRow>
                  </TableHead>

                  <TableBody>
                    {sortedFiles.map((file, index) => (
                      <TableRow key={file.id} hover>
                        <TableCell>{index + 1}</TableCell>
                        <TableCell>{file.filename}</TableCell>
                        <TableCell>{formatFileSize(file.size)}</TableCell>
                        <TableCell>{file.created_at.toLocaleString()}</TableCell>
                        <TableCell>
                          <Chip
                            size="small"
                            label={file.verification_status}
                            color={verificationStatusColor[file.verification_status]}
                          />
                        </TableCell>
                        <TableCell>
                          <Chip
                            size="small"
                            label={file.print_status}
                            color={printStatusColor[file.print_status]}
                          />
                        </TableCell>
                        <TableCell align="right" sx={{ whiteSpace: "nowrap" }}>
                          <Tooltip title="Download file">
                            <IconButton
                              onClick={() => handleDownload(file.id, file.filename)}
                              size="small"
                            >
                              <DownloadIcon />
                            </IconButton>
                          </Tooltip>
                          <Tooltip title="Delete file">
                            <span>
                              <IconButton
                                onClick={() => handleDelete(file.id)}
                                size="small"
                                disabled={deletingId === file.id}
                              >
                                <DeleteIcon />
                              </IconButton>
                            </span>
                          </Tooltip>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </CardContent>
        </Card>
      </Stack>
    </Box>
  );
}
