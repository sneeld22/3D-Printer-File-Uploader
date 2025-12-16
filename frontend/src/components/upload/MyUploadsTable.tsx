import { useEffect, useState } from "react";
import {
  Alert,
  Box,
  CircularProgress,
  IconButton,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
  Tooltip,
  Chip,
} from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";
import DownloadIcon from "@mui/icons-material/Download";
import { getMyFiles, downloadFile } from "../../services/fileService.ts";
import type { ModelFile, VerificationStatus, PrinterJobStatus } from "../../common/models.ts";
import { formatFileSize } from "../../utils/utils.ts";

const printStatusColor: Record<PrinterJobStatus, "success" | "warning" | "error" | "info" | "primary"> = {
  pending: "warning",
  queued: "info",
  printing: "success",
  completed: "primary",
  failed: "error",
};

const verificationStatusColor: Record<VerificationStatus, "success" | "warning" | "error"> = {
  approved: "success",
  pending: "warning",
  rejected: "error",
};

const MyUploadsTable = () => {
  const [files, setFiles] = useState<ModelFile[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const loadFiles = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getMyFiles();
      setFiles(data);
    } catch (err: unknown) {
      console.error(err);
      setError("Could not load your files. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (fileId: string, filename: string) => {
    try {
      const blob = await downloadFile(fileId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename; // set download filename
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(error);
      alert("Failed to download file.");
    }
  };

  useEffect(() => {
    void loadFiles();
  }, []);

  return (
    <Paper sx={{ mt: 4, p: 2 }}>
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          mb: 2,
          gap: 1,
        }}
      >
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          My uploads
        </Typography>
        <Tooltip title="Reload">
          <IconButton onClick={() => void loadFiles()} disabled={loading}>
            <RefreshIcon />
          </IconButton>
        </Tooltip>
      </Box>

      {loading && (
        <Box sx={{ display: "flex", justifyContent: "center", py: 4 }}>
          <CircularProgress />
        </Box>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {!loading && files.length === 0 && !error && (
        <Typography variant="body2" color="text.secondary">
          You haven’t uploaded any files yet.
        </Typography>
      )}

      {!loading && files.length > 0 && (
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Filename</TableCell>
              <TableCell>Size</TableCell>
              <TableCell>Uploaded</TableCell>
              <TableCell>Verification</TableCell>
              <TableCell>Print Status</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {files.map((file) => (
              <TableRow key={file.id} hover>
                <TableCell>{file.filename}</TableCell>
                <TableCell>{formatFileSize(file.size)}</TableCell>
                <TableCell>{new Date(file.created_at).toLocaleString()}</TableCell>
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
                <TableCell align="right">
                  <Tooltip title="Download file">
                    <IconButton
                      onClick={() => handleDownload(file.id, file.filename)}
                      size="small"
                    >
                      <DownloadIcon />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </Paper>
  );
};

export default MyUploadsTable;
